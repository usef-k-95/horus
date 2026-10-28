"""From a website request to a running engagement: folder, state, inbox, acknowledgement, kick-off."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .client import IntakeSettings, SiteClient
from .countries import iso3

CONFIG_DIR = Path.home() / ".horus"
LEDGER_FILE = CONFIG_DIR / "intake-ledger.json"
LOG_FILE = CONFIG_DIR / "intake.log"
BACKEND = Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def log(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"{now_iso()} {message}\n")


def notify_mac(title: str, text: str) -> None:
    """A macOS notification for the Supervisor; silent when osascript is unavailable."""
    try:
        subprocess.run(["osascript", "-e", f"display notification {json.dumps(text)} with title {json.dumps(title)}"], check=False, capture_output=True, timeout=10)
    except Exception:  # noqa: BLE001
        pass


# ---- naming ------------------------------------------------------------------------------------
def slugify(text: str, limit: int = 18) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()
    text = re.sub(r"\b(the|of|and|for|ministry|department|authority|agency|government|national|general|office)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(text) > limit:
        text = text[:limit].rsplit("-", 1)[0] if "-" in text[:limit] else text[:limit]
    return text.strip("-") or "scope"


def derive_code(request: dict, engagements_dir: Path) -> str:
    """`EGY-2026-003-finance` for an engagement, `DEMO-2026-001-finance` for a demo; the number is one more than the highest used this year."""
    kind = request.get("kind") or "engagement"
    prefix = "DEMO" if kind == "demo" else (iso3(request.get("country") or "") or "INT")
    year = (request.get("received_at") or now_iso())[:4]
    existing = [p.name for p in engagements_dir.iterdir()] if engagements_dir.exists() else []
    used = [int(m.group(1)) for name in existing for m in [re.match(rf"^[A-Z]+-{year}-(\d{{3}})(-|$)", name)] if m]
    n = max(used, default=0) + 1
    slug = slugify(request.get("organisation") or "")
    while True:
        code = f"{prefix}-{year}-{n:03d}-{slug}"
        if code not in existing:
            return code
        n += 1


def engagement_name(request: dict) -> str:
    org = (request.get("organisation") or "").strip()
    first_line = next((ln.strip() for ln in (request.get("scope_text") or "").splitlines() if ln.strip()), "")
    if not first_line and request.get("attachment"):
        first_line = Path(request["attachment"].get("name", "")).stem.replace("_", " ").replace("-", " ").strip()
    first_line = re.sub(r"\s+", " ", first_line)[:90].rstrip(" .,;:")
    if request.get("kind") == "demo":
        return f"Demo for {org}" + (f": {first_line}" if first_line else "")
    return f"{org}: {first_line}" if first_line else f"{org}: scope of work"


# ---- the ledger: what this Mac has already taken -------------------------------------------------
class Ledger:
    def __init__(self, path: Path = LEDGER_FILE) -> None:
        self.path = path
        self.data: dict = {}
        if path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                self.data = {}

    def has(self, request_id: str) -> bool:
        return request_id in self.data

    def get(self, request_id: str) -> dict:
        return self.data.get(request_id, {})

    def put(self, request_id: str, **fields) -> None:
        entry = self.data.setdefault(request_id, {})
        entry.update(fields)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")


# ---- the engagement folder ---------------------------------------------------------------------
def init_engagement(folder: Path, code: str, request: dict) -> None:
    from horus_state.service import Service

    folder.mkdir(parents=True, exist_ok=True)
    country = iso3(request.get("country") or "") or (request.get("country") or "").strip()[:60] or "unknown"
    svc = Service(folder, actor="principal")
    svc.init_engagement(
        code,
        engagement_name(request),
        {"entity": (request.get("organisation") or "").strip()[:200], "country": country},
        supervisors=[os.environ.get("USER", "supervisor")],
        received=(request.get("received_at") or now_iso())[:10],
    )


def write_request(folder: Path, request: dict, scope_file: Optional[Path]) -> Path:
    inbox = folder / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    kind = "demo request" if request.get("kind") == "demo" else "scope of work"
    if scope_file:
        document = scope_file.name
    elif request.get("attachment"):
        document = "(attached on the site but not downloaded: " + str(request["attachment"].get("name", "")) + ")"
    else:
        document = "(none attached)"
    lines = [
        f"# Website request {request.get('id', '')}: {kind}",
        "",
        f"- Received: {request.get('received_at', '')}",
        f"- Channel: web form at {request.get('page') or 'horushq.ai'}",
        f"- Requester: {request.get('name', '')}",
        f"- Email: {request.get('email', '')}",
        f"- Organisation: {request.get('organisation', '')}",
        f"- Country: {request.get('country', '') or '(not given)'}",
    ]
    if request.get("kind") == "demo":
        lines.append(f"- Preferred week: {request.get('preferred_week') or '(not given)'}")
    lines.append(f"- Scope document: {document}")
    lines += ["", "## Scope as submitted", "", (request.get("scope_text") or "(no text; see the document)").strip(), ""]
    path = inbox / "request.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    (inbox / "request.json").write_text(json.dumps(request, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def git_commit(folder: Path, message: str) -> None:
    try:
        if not (folder / ".git").exists():
            subprocess.run(["git", "init", "-q"], cwd=folder, check=False, capture_output=True, timeout=30)
        subprocess.run(["git", "add", "-A"], cwd=folder, check=False, capture_output=True, timeout=60)
        subprocess.run(["git", "commit", "-q", "-m", message], cwd=folder, check=False, capture_output=True, timeout=60)
    except Exception:  # noqa: BLE001
        pass


# ---- the acknowledgement to the requester -----------------------------------------------------
def acknowledgement_text(request: dict, code: str) -> tuple[str, str]:
    name = (request.get("name") or "").split(",")[0].strip() or "there"
    org = (request.get("organisation") or "your organisation").strip()
    if request.get("kind") == "demo":
        when = f"in the week of {request['preferred_week'].strip()}" if (request.get("preferred_week") or "").strip() else "within one working day"
        subject = f"Your Horus demo · {code}"
        body = (
            f"Dear {name},\n\n"
            f"Thank you. Horus has received the scope for the demo from {org} and has opened {code} for it.\n\n"
            f"Horus is reading the scope now and will propose two times {when}, with a short note on what it will show against your scope: "
            "the questions it would answer, the stakeholders it would consult, the options it would appraise and the documents it would deliver.\n\n"
            "Nothing further is needed from you at this stage. Replies to this email reach the engagement directly.\n"
        )
    else:
        subject = f"Horus has received your scope of work · {code}"
        body = (
            f"Dear {name},\n\n"
            f"Thank you. Horus has received the scope of work from {org} and has opened engagement {code}.\n\n"
            "Horus is reading the scope now. Within one working day you will receive its reading of the problem, the questions it needs answered, "
            "the proposed approach and a proposal for the kickoff meeting.\n\n"
            "Nothing further is needed from you at this stage. Replies to this email reach the engagement directly.\n"
        )
    body += f"\nHorus\nEngagement {code}\nHorus is a technology company. Its AI runs policy engagements for governments end to end.\n"
    return subject, body


def record_acknowledgement(folder: Path, request: dict, code: str, *, sender: str, subject: str, message_id: str, body_path: Path) -> Optional[str]:
    """Record the acknowledgement in the engagement state as a sent communication. The Supervisor's standing instruction
    (HORUS_INTAKE_AUTO_ACK) is the approval: it is requested and decided here in their name, so the audit trail is complete
    and the Principal does not have to ask for a retroactive one. Returns the communication id, or None if the state refused."""
    try:
        from horus_state.service import Service

        svc = Service(folder, actor="principal")
        com = svc.create(
            "communications",
            {
                "channel": "email",
                "direction": "outbound",
                "from": sender,
                "to": [request["email"]],
                "date": datetime.now(timezone.utc),
                "subject": subject,
                "summary": "Automatic acknowledgement of the website request: the engagement is open and Horus's reading of the brief follows within one working day.",
                "body_path": str(body_path.relative_to(folder)),
                "classification": "client_pm",
                "action_class": "client_pm_email",
                "external_ref": message_id or None,
                "status": "draft",
            },
        )
        approval = svc.request_approval(
            {"collection": "communications", "id": com["id"]},
            "client_pm_email",
            "Automatic acknowledgement of the website request (fixed template, no judgement; standing instruction HORUS_INTAKE_AUTO_ACK)",
            risk_class="low",
        )
        if approval.get("status") == "pending":
            svc.decide_approval(
                approval["id"],
                "approved",
                note="Standing instruction: the intake acknowledges every website request at once with the fixed template.",
                actor=f"supervisor:{os.environ.get('USER', 'supervisor')}",
            )
        svc.update("communications", com["id"], {"status": "sent", "approval": approval["id"]}, reason="sent by the intake watcher")
        return com["id"]
    except Exception as exc:  # noqa: BLE001
        log(f"{code}: acknowledgement sent but not recorded in state: {exc}")
        return None


def acknowledge(folder: Path, request: dict, code: str) -> Optional[Path]:
    """Send the acknowledgement through the Supervisor's mail account and record it in the inbox. None when it could not be sent."""
    from horus_mail import MailClient, MailSettings

    settings = MailSettings.load()
    if settings.missing():
        log(f"{code}: acknowledgement not sent, mail not configured ({', '.join(settings.missing())})")
        return None
    subject, body = acknowledgement_text(request, code)
    try:
        message_id = MailClient(settings).send([request["email"]], subject, body)
    except Exception as exc:  # noqa: BLE001
        log(f"{code}: acknowledgement failed: {exc}")
        return None
    path = folder / "inbox" / "acknowledgement-sent.md"
    sender = settings.from_address or settings.user
    path.write_text(
        f"# Acknowledgement sent\n\n- To: {request['email']}\n- From: {settings.from_name} <{sender}>\n- Sent: {now_iso()}\n- Message-ID: {message_id}\n- Subject: {subject}\n\n```\n{body}```\n",
        encoding="utf-8",
    )
    record_id = record_acknowledgement(folder, request, code, sender=sender, subject=subject, message_id=message_id, body_path=path)
    if record_id:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(f"\nRecorded in the engagement state as {record_id} (sent; approved under the Supervisor's standing instruction).\n")
    return path


# ---- the kick-off: the Horus Principal, unattended -----------------------------------------------
SYSTEM_APPEND = (
    "You are running unattended as the Horus Principal in a kick-off session that the website intake started. No one can answer "
    "questions in this session: make reasonable assumptions, record them as provisional notes and open questions, and never wait "
    "for input. A tool that is denied is unavailable in this run; work around it. Bash works only inside this folder; read files "
    "elsewhere (the plugin's references, the project docs) with Read, Glob and Grep. Nothing leaves this folder: no email, no meeting, "
    "no release. Draft what should go out, request the approval in state, and stop; the Supervisor sends approved emails from the "
    "Claude app. Finish with validate and a checkpoint that names what waits for the Supervisor."
)


def kickoff_prompt(request: dict, code: str, ack_path: Optional[Path]) -> str:
    kind = request.get("kind") or "engagement"
    recorded = bool(ack_path) and ack_path.exists() and "Recorded in the engagement state as" in ack_path.read_text(encoding="utf-8")
    if recorded:
        ack = (
            f"An acknowledgement was already emailed to the requester at {request.get('email')} and is recorded in state as a sent communication, approved under "
            "the Supervisor's standing instruction (see inbox/acknowledgement-sent.md); do not record, resend or approve it again."
        )
    elif ack_path:
        ack = (
            f"An acknowledgement was already emailed to the requester at {request.get('email')} (see inbox/acknowledgement-sent.md) but could not be recorded in state; "
            "record it as an outbound communication at status draft with the note ALREADY SENT, and do not request an approval for it."
        )
    else:
        ack = "No acknowledgement has been sent yet; the first email to the requester must open with thanks and confirmation of what was received."
    head = (
        f"A new {'demo request' if kind == 'demo' else 'scope of work'} arrived through the Horus website (horushq.ai) and this engagement folder, {code}, "
        "was created for it automatically; `horus init` has run. The request record is inbox/request.md (who asked, organisation, country, email, "
        "and the scope text as submitted); the attached scope document, if any, is in inbox/ as well. Record the website request itself as the "
        f"inbound communication (channel web form, request id {request.get('id')}), and treat the requester as the client PM until the brief says otherwise. {ack}\n\n"
    )
    if kind == "demo":
        when = f"in the week of {request['preferred_week'].strip()}" if (request.get("preferred_week") or "").strip() else "within the next ten working days"
        task = (
            "Run the Horus method's intake lightly for a demo (/horus:horus-method intake): import the documents, read the scope in full, draft the brief v0 "
            "and classify the problem with its pathway. Then prepare the demo plan as an analysis record: what Horus will show in 45 minutes against this scope, "
            "the questions it would answer, the stakeholders it would consult, the options it would appraise, the deliverables it would produce, and the two or "
            f"three facts about the organisation and the decision maker it should know going in (one researcher run, 20 fetches). Draft the reply proposing two times {when} "
            "(working hours in the requester's country), request the approval on it and stop."
        )
    else:
        task = (
            "Run Phase 0 of the Horus method now (/horus:horus-method intake): import the documents, read them in full, draft the brief v0, list the clarifications "
            "that matter, create the stakeholders, classify the problem and select the pathway, start the two P0 profiles with researcher workers, and draft the AP0 "
            "email to the requester as the client PM with the questions and the kickoff proposal. Request the approval on it and stop there."
        )
    return head + task


def kickoff(folder: Path, request: dict, code: str, ack_path: Optional[Path], settings: IntakeSettings) -> Optional[Path]:
    """Start the Principal in the background and return the log path; None when the claude command is not available."""
    if not settings.claude_bin:
        log(f"{code}: kick-off skipped, the claude command was not found (install the Claude app or set HORUS_CLAUDE_BIN)")
        return None
    runs = folder / ".horus" / "kickoff"
    runs.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    prompt_file = runs / f"{stamp}-prompt.md"
    system_file = runs / f"{stamp}-system.md"
    log_file = runs / f"{stamp}.jsonl"
    err_file = runs / f"{stamp}.err"
    wrapper = runs / f"{stamp}-run.sh"
    prompt_file.write_text(kickoff_prompt(request, code, ack_path), encoding="utf-8")
    system_file.write_text(SYSTEM_APPEND, encoding="utf-8")
    cmd = [
        settings.claude_bin, "-p", "--output-format", "stream-json", "--verbose", "--max-turns", str(settings.max_turns),
        "--permission-mode", "acceptEdits", "--permission-prompts", "none", "--append-system-prompt-file", str(system_file),
        "--allowedTools", *settings.allowed_tools,
    ]
    uvw = BACKEND / "uvw"
    q = shlex.quote
    script = (
        "#!/bin/sh\n"
        f"# Horus kick-off for {code}, started by the intake watcher at {now_iso()}\n"
        f"cd {q(str(folder))} || exit 1\n"
        f"{' '.join(q(c) for c in cmd)} < {q(str(prompt_file))} > {q(str(log_file))} 2> {q(str(err_file))}\n"
        "status=$?\n"
        f"cd {q(str(BACKEND))} && {q(str(uvw))} run --no-sync horus-intake finished {q(code)} \"$status\" {q(str(log_file))} >> {q(str(LOG_FILE))} 2>&1\n"
    )
    wrapper.write_text(script, encoding="utf-8")
    wrapper.chmod(0o700)
    subprocess.Popen(["/bin/sh", str(wrapper)], cwd=folder, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    log(f"{code}: kick-off started (log {log_file})")
    return log_file


def summarise_run(code: str, status: str, log_path: Path) -> dict:
    """Read the stream-json log of a finished kick-off: the result line, cost, turns and whether sign-in is missing."""
    summary = {"code": code, "exit_status": status, "log": str(log_path), "result": "", "is_error": None, "num_turns": None, "cost_usd": None, "duration_s": None, "not_logged_in": False}
    text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path.exists() else ""
    err_path = log_path.with_suffix(".err")
    err_text = err_path.read_text(encoding="utf-8", errors="ignore") if err_path.exists() else ""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "result":
            summary.update(
                result=str(event.get("result") or "")[:4000],
                is_error=bool(event.get("is_error")),
                num_turns=event.get("num_turns"),
                cost_usd=event.get("total_cost_usd"),
                duration_s=round((event.get("duration_ms") or 0) / 1000),
            )
            break
    lowered = (text + err_text).lower()
    if "not logged in" in lowered or "please run /login" in lowered:
        summary["not_logged_in"] = True
    if not summary["result"] and err_text.strip():
        summary["result"] = err_text.strip()[-2000:]
    return summary


# ---- orchestration -----------------------------------------------------------------------------
def process(request: dict, client: SiteClient, settings: IntakeSettings, ledger: Ledger, *, do_ack: bool = True, do_kickoff: bool = True) -> dict:
    rid = request.get("id") or "REQ-unknown"
    if ledger.has(rid):
        entry = ledger.get(rid)
        if not entry.get("acked"):
            try:
                client.ack(rid, "taken", entry.get("code"))
                ledger.put(rid, acked=True)
            except Exception as exc:  # noqa: BLE001
                log(f"{rid}: ack retry failed: {exc}")
        return {"id": rid, "code": entry.get("code"), "skipped": "already taken by this Mac"}

    settings.engagements_dir.mkdir(parents=True, exist_ok=True)
    code = derive_code(request, settings.engagements_dir)
    folder = settings.engagements_dir / code
    try:
        init_engagement(folder, code, request)
    except Exception as exc:  # noqa: BLE001
        log(f"{rid}: could not initialise {code}: {exc}")
        raise
    scope_file = None
    if request.get("attachment"):
        try:
            scope_file = client.download(rid, folder / "inbox", fallback_name=request["attachment"].get("name") or "scope")
        except Exception as exc:  # noqa: BLE001
            log(f"{code}: scope document download failed: {exc}")
    write_request(folder, request, scope_file)
    ledger.put(rid, code=code, folder=str(folder), taken_at=now_iso(), acked=False)
    try:
        client.ack(rid, "taken", code)
        ledger.put(rid, acked=True)
    except Exception as exc:  # noqa: BLE001
        log(f"{code}: ack failed, will retry: {exc}")
    git_commit(folder, f"Engagement {code} opened from website request {rid}")
    org = request.get("organisation") or "an organisation"
    log(f"{rid}: engagement {code} created for {org} ({request.get('kind')})")

    ack_path = None
    if do_ack and settings.auto_ack:
        ack_path = acknowledge(folder, request, code)
        if ack_path:
            log(f"{code}: acknowledgement sent to {request.get('email')}")
            git_commit(folder, "Acknowledgement sent")
    kick_log = None
    if do_kickoff and settings.autostart:
        kick_log = kickoff(folder, request, code, ack_path, settings)
    ledger.put(rid, acknowledged=bool(ack_path), kickoff_log=str(kick_log) if kick_log else None)
    notify_mac("Horus", f"New {'demo request' if request.get('kind') == 'demo' else 'engagement'} {code} from {org}." + (" Kick-off started." if kick_log else ""))
    return {"id": rid, "code": code, "folder": str(folder), "scope_file": str(scope_file) if scope_file else None, "acknowledged": bool(ack_path), "kickoff_log": str(kick_log) if kick_log else None}


def pull(client: SiteClient, settings: IntakeSettings, *, do_ack: bool = True, do_kickoff: bool = True, ledger: Optional[Ledger] = None) -> list[dict]:
    ledger = ledger or Ledger()
    results = []
    for request in client.pending():
        try:
            results.append(process(request, client, settings, ledger, do_ack=do_ack, do_kickoff=do_kickoff))
        except Exception as exc:  # noqa: BLE001
            log(f"{request.get('id')}: failed: {exc}")
            results.append({"id": request.get("id"), "error": str(exc)})
    return results
