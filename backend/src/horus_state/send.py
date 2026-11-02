"""`horus send`: preview, approve and send a pending outbound email from the engagement state.

The Principal drafts the email as a `communications` record (direction outbound, the letter in a
Markdown file at `body_path`, recipients as addresses or stakeholder ids, attachments as document ids)
and requests an approval. The Supervisor previews it here, approves it and sends it from the console,
with no Principal session and no mail tools. The state records the decision, the status `sent`, the
Message-ID as `external_ref` and the time of sending; rule 12 (no sending without an approved
approval) stays enforced by the service.

`horus_mail` is imported lazily so the console keeps working when mail is not configured."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .service import Service
from .store import NotFound, utcnow

SENDABLE_STATUSES = ("draft", "pending_approval", "approved")
HEADER_LINE = re.compile(r"^(?:[-*]\s+)?(?:\*\*)?(?P<key>[A-Za-z][A-Za-z -]{0,30}?)(?:\*\*)?:(?:\*\*)?(?:\s+(?P<value>.*))?$")
TRAILER_KEYS = {"attachments", "attachment", "log", "record", "status", "classification", "approval"}
ADDRESS = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


class SendError(Exception):
    """Why the email cannot be prepared or sent, in plain words for the console."""


@dataclass
class Prepared:
    """Everything `horus send` would do, resolved from the state and ready to preview or send."""

    communication: dict
    approval: Optional[dict]
    other_pending: list[str] = field(default_factory=list)
    to: list[tuple[str, str]] = field(default_factory=list)  # (address, label)
    cc: list[tuple[str, str]] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    body_path: Optional[Path] = None
    attachments: list[tuple[Path, str]] = field(default_factory=list)  # (path, label)
    in_reply_to: Optional[str] = None
    in_reply_to_id: Optional[str] = None
    dropped: list[str] = field(default_factory=list)  # metadata lines below the letter, not sent
    warnings: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.communication["id"]

    @property
    def to_addresses(self) -> list[str]:
        return [a for a, _ in self.to]

    @property
    def cc_addresses(self) -> list[str]:
        return [a for a, _ in self.cc]

    @property
    def sendable(self) -> bool:
        return not self.problems


# ---- body -------------------------------------------------------------------------------------

def split_body(text: str) -> tuple[dict, str]:
    """Separate the Principal's metadata header from the letter.

    Three header conventions are recognised; anything else is the letter, verbatim:
    * a Markdown title (`# AP0 email …`) with metadata lines, then a `---` rule: the letter is what follows the first rule;
    * YAML-style front matter between two `---` rules: the letter is what follows the closing rule;
    * mail-style header lines (`Subject: …`, `To: …`, `Cc: …`) up to the first blank line: the letter is what follows.
    Returns the header fields (lower-case keys) and the letter."""
    text = text.lstrip("﻿")
    lines = text.split("\n")
    header_lines: list[str] = []
    body_lines: list[str] = lines
    if text.startswith("#"):
        for i, line in enumerate(lines):
            if line.strip() == "---":
                header_lines, body_lines = lines[:i], lines[i + 1 :]
                break
    elif lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                header_lines, body_lines = lines[1:i], lines[i + 1 :]
                break
    else:
        block: list[str] = []
        for i, line in enumerate(lines):
            if not line.strip():
                if block and _is_header_block(block):
                    header_lines, body_lines = block, lines[i + 1 :]
                break
            block.append(line)
    header: dict[str, str] = {}
    for line in header_lines:
        m = HEADER_LINE.match(line.strip())
        if m:
            header[m.group("key").strip().lower()] = (m.group("value") or "").strip()
    return header, "\n".join(body_lines)


def _is_header_block(block: list[str]) -> bool:
    keys = []
    for line in block:
        if line[:1].isspace():
            continue  # folded continuation
        m = HEADER_LINE.match(line.strip())
        if not m:
            return False
        keys.append(m.group("key").strip().lower())
    return bool(keys) and any(k in ("subject", "to", "cc") for k in keys)


def strip_markup(text: str) -> str:
    """Plain text for the wire: `**bold**` markers go, everything else stays as written."""
    return text.replace("**", "")


def split_trailer(letter: str) -> tuple[str, list[str]]:
    """Metadata the Principal leaves below the letter (`Attachments: none`, `Log: communications COM-004 {…}`):
    final paragraphs made only of such lines are not part of the email. Returns the letter and the dropped lines."""
    lines = letter.rstrip("\n").split("\n")
    dropped: list[str] = []
    while lines:
        start = len(lines)
        while start > 0 and lines[start - 1].strip():
            start -= 1
        block = lines[start:]
        if start == 0 or not block or not all(_is_trailer_line(line) for line in block):
            break  # the whole text is one paragraph, or the last paragraph is prose: keep it
        dropped = block + dropped
        lines = lines[:start]
        while lines and not lines[-1].strip():
            lines.pop()
    return "\n".join(lines), dropped


def _is_trailer_line(line: str) -> bool:
    m = HEADER_LINE.match(line.strip())
    return bool(m) and m.group("key").strip().lower() in TRAILER_KEYS


def prepare_body(text: str) -> tuple[dict, str, list[str]]:
    """The header fields, the letter as it goes on the wire, and the trailer lines dropped below it."""
    header, letter = split_body(text)
    letter, trailer = split_trailer(strip_markup(letter))
    letter = letter.strip("\n")
    return header, (letter + "\n") if letter else "", trailer


# ---- recipients and attachments ---------------------------------------------------------------

def resolve_recipients(svc: Service, entries: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """Addresses stay addresses; `STK-…` ids resolve through the stakeholder's contact email.
    Returns (address, label) pairs without duplicates and the list of entries that could not be resolved."""
    out: list[tuple[str, str]] = []
    problems: list[str] = []
    seen: set[str] = set()
    for raw in entries or []:
        entry = str(raw or "").strip()
        if not entry:
            continue
        if "@" in entry:
            address, label = entry, ""
        elif entry.upper().startswith("STK-"):
            try:
                person = svc.store.read("stakeholders", entry)
            except NotFound:
                problems.append(f"{entry} is not a stakeholder in this engagement")
                continue
            address = (person.get("contact") or {}).get("email") or person.get("email")
            if not address:
                problems.append(f"{entry} ({person.get('name')}) has no email address in its record: add contact.email or put the address in the communication")
                continue
            label = f"{entry} {person.get('name') or ''}".strip()
        else:
            problems.append(f"recipient {entry!r} is neither an email address nor a stakeholder id")
            continue
        key = address.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append((address, label))
    return out, problems


def resolve_attachments(svc: Service, refs: list[str]) -> tuple[list[tuple[Path, str]], list[str]]:
    """`DOC-…` ids resolve to the document's file under the engagement folder; the file must exist."""
    out: list[tuple[Path, str]] = []
    problems: list[str] = []
    for raw in refs or []:
        ref = str(raw or "").strip()
        if not ref:
            continue
        if not ref.upper().startswith("DOC-"):
            problems.append(f"attachment {ref!r} is not a document id (DOC-…)")
            continue
        try:
            doc = svc.store.read("documents", ref)
        except NotFound:
            problems.append(f"attachment {ref} is not a document in this engagement")
            continue
        rel = doc.get("path") or ""
        path = Path(rel) if Path(rel).is_absolute() else svc.store.workspace / rel
        if not rel or not path.is_file():
            problems.append(f"attachment {ref} ({doc.get('title')}) points to {rel or 'no path'}, which is not a file in the engagement folder")
            continue
        out.append((path, f"{ref} {doc.get('title') or ''}".strip()))
    return out, problems


# ---- approvals and threading --------------------------------------------------------------------

def _as_datetime(value) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(str(value))
        except ValueError:
            return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def expired(approval: dict) -> bool:
    exp = _as_datetime(approval.get("expires_at"))
    return bool(exp and exp < utcnow())


def find_approval(svc: Service, com: dict) -> tuple[Optional[dict], list[str]]:
    """The approval this email rides on: the record's `approval` field, else an approved approval targeting it,
    else the most recent pending one. Also returns the ids of other approvals still pending for the same email."""
    targeting = [a for a in svc.store.iter_records("approvals") if (a.get("target") or {}).get("collection") == "communications" and (a.get("target") or {}).get("id") == com["id"]]
    pending = sorted([a for a in targeting if a.get("status") == "pending"], key=lambda a: (str(a.get("requested_at") or ""), a["id"]))
    chosen: Optional[dict] = None
    if com.get("approval"):
        try:
            chosen = svc.store.read("approvals", com["approval"])
        except NotFound:
            chosen = None
    if chosen is None or chosen.get("status") not in ("approved", "pending"):
        approved = [a for a in targeting if a.get("status") == "approved" and not expired(a)]
        if approved:
            chosen = sorted(approved, key=lambda a: (str(a.get("decided_at") or ""), a["id"]))[-1]
        elif pending:
            chosen = pending[-1]
    others = [a["id"] for a in pending if not chosen or a["id"] != chosen["id"]]
    return chosen, others


def thread_parent(svc: Service, com: dict, addresses: list[str]) -> Optional[dict]:
    """The most recent other outbound communication that was sent (with a Message-ID) to one of the same recipients:
    the new email threads under it. None starts a new thread."""
    ours = {a.lower() for a in addresses}
    candidates = []
    for other in svc.store.iter_records("communications"):
        if other["id"] == com["id"] or other.get("direction") != "outbound" or other.get("status") != "sent" or not str(other.get("external_ref") or "").strip():
            continue
        theirs, _ = resolve_recipients(svc, list(other.get("to") or []) + list(other.get("cc") or []))
        if ours & {a.lower() for a, _ in theirs}:
            candidates.append(other)
    if not candidates:
        return None
    return sorted(candidates, key=lambda c: (str(c.get("date") or ""), c["id"]))[-1]


# ---- preparing ----------------------------------------------------------------------------------

def prepare(svc: Service, com_id: str) -> Prepared:
    """Resolve everything needed to send `com_id`. Raises SendError when the record is not an unsent outbound email;
    anything else that would block sending is collected in `problems` so the preview can show it all."""
    try:
        com = svc.store.read("communications", com_id)
    except NotFound:
        raise SendError(f"{com_id} is not a communication in this engagement ({svc.store.workspace})") from None
    if com.get("direction") != "outbound":
        raise SendError(f"{com_id} is an inbound communication; only outbound emails can be sent")
    if com.get("status") == "sent":
        raise SendError(f"{com_id} was already sent on {com.get('date')} (Message-ID {com.get('external_ref') or 'unknown'}); nothing to do")
    if com.get("status") not in SENDABLE_STATUSES:
        raise SendError(f"{com_id} has status {com.get('status')!r}; only {', '.join(SENDABLE_STATUSES)} can be sent")
    if (com.get("channel") or "email") != "email":
        raise SendError(f"{com_id} uses channel {com.get('channel')!r}; the console sends email only")

    p = Prepared(communication=com, approval=None)
    p.approval, p.other_pending = find_approval(svc, com)
    if p.approval is None:
        p.problems.append("no approval request for this email: the Principal must call request_approval on it first")
    elif p.approval.get("status") == "pending" and expired(p.approval):
        p.problems.append(f"approval {p.approval['id']} expired on {p.approval.get('expires_at')}; ask the Principal for a new request")
    elif p.approval.get("status") not in ("pending", "approved"):
        p.problems.append(f"approval {p.approval['id']} is {p.approval.get('status')}; ask the Principal for a new request")

    p.to, to_problems = resolve_recipients(svc, com.get("to") or [])
    p.cc, cc_problems = resolve_recipients(svc, com.get("cc") or [])
    p.cc = [(a, l) for a, l in p.cc if a.lower() not in {x.lower() for x in p.to_addresses}]
    p.problems.extend(to_problems + cc_problems)
    if not p.to and not to_problems:
        p.problems.append("no recipient: the communication's `to` list is empty")

    p.attachments, attachment_problems = resolve_attachments(svc, com.get("attachments") or [])
    p.problems.extend(attachment_problems)

    header: dict = {}
    rel = com.get("body_path")
    if not rel:
        p.problems.append("no body: the communication has no body_path")
    else:
        p.body_path = Path(rel) if Path(rel).is_absolute() else svc.store.workspace / rel
        if not p.body_path.is_file():
            p.problems.append(f"body file {rel} does not exist in the engagement folder")
        else:
            header, p.body, p.dropped = prepare_body(p.body_path.read_text(encoding="utf-8"))
            if not p.body.strip():
                p.problems.append(f"body file {rel} has no text below its header")

    p.subject = str(com.get("subject") or "").strip() or header.get("subject", "").strip()
    if not p.subject:
        p.problems.append("no subject on the communication (and none in the body file's header)")
    elif header.get("subject") and header["subject"].strip() != p.subject:
        p.warnings.append(f"the body file's header gives a different subject: {header['subject'].strip()!r}; the record's subject is used")
    header_addresses = {a.lower() for key in ("to", "cc") for a in ADDRESS.findall(header.get(key, ""))}
    resolved = {a.lower() for a in p.to_addresses + p.cc_addresses}
    for extra in sorted(header_addresses - resolved):
        p.warnings.append(f"the body file's header names {extra}, which is not among the resolved recipients; the record's to/cc are used")

    parent = thread_parent(svc, com, p.to_addresses + p.cc_addresses)
    if parent:
        p.in_reply_to, p.in_reply_to_id = str(parent.get("external_ref")).strip(), parent["id"]
    return p


# ---- preview -----------------------------------------------------------------------------------

def render_preview(p: Prepared, from_line: Optional[str] = None) -> str:
    com, apv = p.communication, p.approval
    lines = [f"{p.id}  outbound {com.get('channel') or 'email'}  status {com.get('status')}  classification {com.get('classification')}"]
    if apv:
        lines.append(f"Approval:    {apv['id']} {apv.get('status')} ({apv.get('action_class')}, risk {apv.get('risk_class')}) requested {str(apv.get('requested_at') or '')[:16]} by {apv.get('requested_by')}")
        lines.append(f"             {apv.get('summary') or ''}")
        if apv.get("status") == "approved":
            lines.append(f"             approved by {apv.get('decided_by')} on {str(apv.get('decided_at') or '')[:16]}")
    else:
        lines.append("Approval:    none")
    if p.other_pending:
        lines.append(f"             also pending for this email, not decided by this command: {', '.join(p.other_pending)}")
    lines.append(f"From:        {from_line or '(mail settings not available)'}")
    lines.append("To:          " + (", ".join(_fmt_recipient(a, l) for a, l in p.to) or "none"))
    lines.append("Cc:          " + (", ".join(_fmt_recipient(a, l) for a, l in p.cc) or "none"))
    lines.append(f"Subject:     {p.subject or '(none)'}")
    if p.in_reply_to:
        lines.append(f"Threading:   reply to {p.in_reply_to_id} (In-Reply-To {p.in_reply_to})")
    else:
        lines.append("Threading:   new thread (no earlier sent email to these recipients carries a Message-ID)")
    lines.append("Attachments: " + (", ".join(f"{label} → {path}" for path, label in p.attachments) or "none"))
    if com.get("notes"):
        lines.append(f"Notes:       {str(com['notes']).strip()}")
    if p.dropped:
        lines.append(f"Not sent:    {len(p.dropped)} metadata line(s) below the letter: " + " | ".join(x.strip() for x in p.dropped))
    for w in p.warnings:
        lines.append(f"Warning:     {w}")
    body = p.body.rstrip("\n")
    lines.append(f"Body:        {p.body_path or '(none)'} ({len(body.splitlines())} lines, {len(body)} characters)")
    lines.append("-" * 72)
    lines.append(body or "(empty)")
    lines.append("-" * 72)
    if p.problems:
        lines.append("Cannot send until:")
        lines.extend(f"  - {x}" for x in p.problems)
    return "\n".join(lines)


def _fmt_recipient(address: str, label: str) -> str:
    return f"{address} ({label})" if label else address


# ---- actions -----------------------------------------------------------------------------------

def mail_settings():
    """The mail settings from backend/.env, or a SendError naming what is missing. Imported lazily."""
    try:
        from horus_mail.client import MailSettings
    except ImportError as exc:  # pragma: no cover - the package ships with the backend
        raise SendError(f"the mail package is not available: {exc}") from exc
    settings = MailSettings.load()
    missing = settings.missing()
    if missing:
        raise SendError("mail is not configured: " + ", ".join(missing) + ". Run ~/Horus/configure, or set them in backend/.env")
    return settings


def from_line() -> Optional[str]:
    try:
        settings = mail_settings()
    except SendError as exc:
        return f"({exc})"
    return f"{settings.from_name} <{settings.from_address or settings.user}>"


def _require_sendable(p: Prepared) -> None:
    if p.problems:
        raise SendError("cannot send " + p.id + ":\n  - " + "\n  - ".join(p.problems))


def approve_and_send(svc: Service, p: Prepared, note: Optional[str] = None, actor: Optional[str] = None) -> dict:
    """Record the Supervisor's approval (if still pending), send, and mark the communication sent."""
    _require_sendable(p)
    settings = mail_settings()
    actor = actor or svc.actor
    apv = p.approval
    assert apv is not None
    decided = False
    if apv.get("status") == "pending":
        apv = svc.decide_approval(apv["id"], "approved", note, actor=actor)
        decided = True
    elif apv.get("status") != "approved":
        raise SendError(f"approval {apv['id']} is {apv.get('status')}; it cannot be approved from here")
    elif expired(apv):
        raise SendError(f"approval {apv['id']} has expired; ask the Principal for a new request")
    result = _send(svc, p, apv, settings, actor)
    result["approval_decided_now"] = decided
    return result


def send_only(svc: Service, p: Prepared, actor: Optional[str] = None) -> dict:
    """Send an email whose approval was already approved (for example with `horus approve`)."""
    _require_sendable(p)
    settings = mail_settings()
    apv = p.approval
    assert apv is not None
    if apv.get("status") == "pending":
        raise SendError(f"approval {apv['id']} is still pending: use --approve to approve and send, or approve it first with horus approve {apv['id']}")
    if apv.get("status") != "approved":
        raise SendError(f"approval {apv['id']} is {apv.get('status')}; the email cannot be sent")
    if expired(apv):
        raise SendError(f"approval {apv['id']} has expired; ask the Principal for a new request")
    result = _send(svc, p, apv, settings, actor or svc.actor)
    result["approval_decided_now"] = False
    return result


def reject(svc: Service, p: Prepared, reason: str, actor: Optional[str] = None) -> dict:
    """Record a rejection with its reason and return the communication to draft."""
    if not (reason or "").strip():
        raise SendError("a reason is required to reject (--reason)")
    apv = p.approval
    if apv is None:
        raise SendError(f"{p.id} has no approval request to reject")
    if apv.get("status") != "pending":
        raise SendError(f"approval {apv['id']} is already {apv.get('status')}; only a pending approval can be rejected")
    actor = actor or svc.actor
    decided = svc.decide_approval(apv["id"], "rejected", reason, actor=actor)
    com = p.communication
    if com.get("status") != "draft":
        com = svc.update("communications", p.id, {"status": "draft"}, reason=f"rejected by {actor}: {reason}", actor=actor)
    return {"rejected": True, "id": p.id, "approval": decided["id"], "status": com.get("status")}


def _send(svc: Service, p: Prepared, apv: dict, settings, actor: str) -> dict:
    from horus_mail.client import MailClient

    message_id = MailClient(settings).send(p.to_addresses, p.subject, p.body, cc=p.cc_addresses, attachments=[path for path, _ in p.attachments], in_reply_to=p.in_reply_to)
    now = utcnow()
    try:
        record = svc.update("communications", p.id, {"status": "sent", "approval": apv["id"], "external_ref": message_id, "date": now}, reason=f"sent from the console by {actor} under {apv['id']}", actor=actor)
    except Exception as exc:
        raise SendError(f"THE EMAIL WAS SENT (Message-ID {message_id}) but {p.id} could not be marked sent: {exc}. Record it by hand: status sent, external_ref {message_id}, date {now.isoformat()}") from exc
    return {
        "sent": True,
        "id": p.id,
        "status": record.get("status"),
        "approval": apv["id"],
        "message_id": message_id,
        "to": p.to_addresses,
        "cc": p.cc_addresses,
        "subject": p.subject,
        "attachments": [str(path) for path, _ in p.attachments],
        "in_reply_to": p.in_reply_to,
        "date": now,
    }
