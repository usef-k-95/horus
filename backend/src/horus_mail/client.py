from __future__ import annotations

import email.utils
import email
import email.policy
import imaplib
import mimetypes
import os
import re
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, Optional

from dotenv import load_dotenv

SAFE = re.compile(r"[^A-Za-z0-9._ -]+")


@dataclass
class MailSettings:
    user: Optional[str] = None
    app_password: Optional[str] = None
    imap_host: str = "imap.gmail.com"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    from_name: str = "Horus"
    from_address: Optional[str] = None  # a verified Gmail "send as" alias; defaults to the account address

    @classmethod
    def load(cls) -> "MailSettings":
        load_dotenv(override=False)
        return cls(
            user=os.getenv("HORUS_MAIL_USER") or None,
            app_password=os.getenv("HORUS_MAIL_APP_PASSWORD") or None,
            imap_host=os.getenv("HORUS_MAIL_IMAP_HOST", "imap.gmail.com"),
            smtp_host=os.getenv("HORUS_MAIL_SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("HORUS_MAIL_SMTP_PORT", "465")),
            from_name=os.getenv("HORUS_MAIL_FROM_NAME", "Horus"),
            from_address=os.getenv("HORUS_MAIL_FROM_ADDRESS") or None,
        )

    def missing(self) -> list[str]:
        out = []
        if not self.user:
            out.append("HORUS_MAIL_USER")
        if not self.app_password:
            out.append("HORUS_MAIL_APP_PASSWORD (a Google app password; never the account password)")
        return out


def safe_filename(name: str, fallback: str = "attachment") -> str:
    name = (name or "").strip().replace("/", "_")
    name = SAFE.sub("_", name)
    return name[:120] or fallback


def save_attachments(message: EmailMessage, dest: Path, include_inline: bool = False) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for part in message.iter_attachments():
        disposition = part.get_content_disposition()
        if disposition == "inline" and not include_inline:
            continue
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type()) or ".bin"
            filename = f"attachment{ext}"
        target = dest / safe_filename(filename)
        counter = 1
        while target.exists():
            target = dest / f"{target.stem}-{counter}{target.suffix}"
            counter += 1
        target.write_bytes(part.get_payload(decode=True) or b"")
        saved.append(target)
    return saved


MEET_LINK = re.compile(r"https://meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}")
ZOOM_LINK = re.compile(r"https://[\w.-]*zoom\.us/j/\d+(?:\?pwd=[\w.-]+)?")
TEAMS_LINK = re.compile(r"https://teams\.microsoft\.com/l/meetup-join/[^\s\"<>]+")


def find_meeting_link(text: str) -> tuple[Optional[str], Optional[str]]:
    for platform, pattern in (("meet", MEET_LINK), ("zoom", ZOOM_LINK), ("teams", TEAMS_LINK)):
        m = pattern.search(text or "")
        if m:
            return platform, m.group(0)
    return None, None


def parse_ics(text: str) -> dict:
    """Minimal iCalendar parser: unfolds lines, returns the first VEVENT's key fields and the meeting link."""
    lines: list[str] = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        if raw.startswith((" ", "\t")) and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    event: dict = {"attendees": []}
    in_event = False
    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            in_event = True
            continue
        if line.startswith("END:VEVENT"):
            break
        if not in_event or ":" not in line:
            continue
        key_part, value = line.split(":", 1)
        key, *params = key_part.split(";")
        param_map = dict(p.split("=", 1) for p in params if "=" in p)
        if key in ("DTSTART", "DTEND"):
            event[key.lower()] = value
            if "TZID" in param_map:
                event[key.lower() + "_tzid"] = param_map["TZID"]
        elif key in ("SUMMARY", "LOCATION", "DESCRIPTION", "URL", "UID", "ORGANIZER", "STATUS"):
            event[key.lower()] = value.replace("\\n", "\n").replace("\\,", ",")
        elif key == "ATTENDEE":
            event["attendees"].append({"email": value.replace("mailto:", ""), "cn": param_map.get("CN"), "partstat": param_map.get("PARTSTAT")})
    blob = " ".join(str(event.get(k, "")) for k in ("location", "description", "url"))
    platform, link = find_meeting_link(blob)
    event["platform"] = platform
    event["meeting_link"] = link
    return event


class MailClient:
    def __init__(self, settings: Optional[MailSettings] = None) -> None:
        self.settings = settings or MailSettings.load()

    # -- IMAP ------------------------------------------------------------------------------
    def _imap(self) -> imaplib.IMAP4_SSL:
        missing = self.settings.missing()
        if missing:
            raise RuntimeError("mail not configured: " + ", ".join(missing))
        conn = imaplib.IMAP4_SSL(self.settings.imap_host)
        conn.login(self.settings.user, self.settings.app_password)
        return conn

    def fetch_by_gmail_id(self, gmail_message_id_hex: str, folder: str = "[Gmail]/All Mail") -> EmailMessage:
        """The Gmail connector reports hexadecimal message ids; Gmail IMAP searches by the decimal X-GM-MSGID."""
        decimal = int(gmail_message_id_hex, 16)
        conn = self._imap()
        try:
            conn.select(f'"{folder}"', readonly=True)
            status, data = conn.uid("SEARCH", None, f"X-GM-MSGID {decimal}")
            uids = (data[0] or b"").split()
            if status != "OK" or not uids:
                raise LookupError(f"message {gmail_message_id_hex} not found in {folder}")
            status, parts = conn.uid("FETCH", uids[-1], "(RFC822)")
            raw = parts[0][1]
            return email.message_from_bytes(raw, policy=email.policy.default)
        finally:
            conn.logout()

    def list_recent(self, folder: str = "INBOX", days: int = 7, limit: int = 50) -> list[dict]:
        from datetime import date, timedelta

        conn = self._imap()
        try:
            conn.select(f'"{folder}"', readonly=True)
            since = (date.today() - timedelta(days=days)).strftime("%d-%b-%Y")
            status, data = conn.uid("SEARCH", None, f"SINCE {since}")
            uids = (data[0] or b"").split()[-limit:]
            out = []
            for uid in uids:
                status, parts = conn.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] X-GM-MSGID)")
                header = email.message_from_bytes(parts[0][1], policy=email.policy.default)
                meta = parts[0][0].decode(errors="ignore")
                m = re.search(r"X-GM-MSGID (\d+)", meta)
                out.append({"uid": uid.decode(), "gmail_id": format(int(m.group(1)), "x") if m else None, "from": header.get("From"), "subject": header.get("Subject"), "date": header.get("Date")})
            return out
        finally:
            conn.logout()

    # -- SMTP ------------------------------------------------------------------------------
    def send(self, to: Iterable[str], subject: str, body: str, *, cc: Iterable[str] = (), html: Optional[str] = None, attachments: Iterable[Path] = (), in_reply_to: Optional[str] = None) -> str:
        missing = self.settings.missing()
        if missing:
            raise RuntimeError("mail not configured: " + ", ".join(missing))
        msg = EmailMessage()
        msg["From"] = f"{self.settings.from_name} <{self.settings.from_address or self.settings.user}>"
        msg["To"] = ", ".join(to)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject
        msg["Message-ID"] = email.utils.make_msgid(domain=(self.settings.from_address or self.settings.user).split("@")[-1])
        if in_reply_to:
            msg["In-Reply-To"] = in_reply_to
            msg["References"] = in_reply_to
        msg.set_content(body)
        if html:
            msg.add_alternative(html, subtype="html")
        for path in attachments:
            path = Path(path)
            ctype, _ = mimetypes.guess_type(path.name)
            maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
            msg.add_attachment(path.read_bytes(), maintype=maintype, subtype=subtype, filename=path.name)
        with smtplib.SMTP_SSL(self.settings.smtp_host, self.settings.smtp_port) as smtp:
            smtp.login(self.settings.user, self.settings.app_password)
            smtp.send_message(msg)
        return msg["Message-ID"] or ""
