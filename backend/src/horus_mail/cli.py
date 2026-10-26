"""`horus-mail`: attachments, invites and sending with attachments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from .client import MailClient, MailSettings, parse_ics, save_attachments

app = typer.Typer(help="Horus mail: fetch attachments and invites by Gmail message id, parse .ics, send with attachments.", no_args_is_help=True)


@app.command()
def check() -> None:
    """Show whether mail is configured (values masked)."""
    s = MailSettings.load()
    typer.echo(f"user: {s.user or '(not set)'}  imap: {s.imap_host}  smtp: {s.smtp_host}:{s.smtp_port}")
    missing = s.missing()
    if missing:
        typer.echo("missing: " + ", ".join(missing))
        raise typer.Exit(code=2)
    typer.echo("ready")


@app.command("list")
def list_recent(days: int = typer.Option(7), folder: str = typer.Option("INBOX"), limit: int = typer.Option(30)) -> None:
    """Recent messages with their Gmail ids (hex, as the Gmail connector reports them)."""
    for m in MailClient().list_recent(folder, days, limit):
        typer.echo(f"{m['gmail_id'] or m['uid']:<18} {str(m['date'])[:25]:<26} {str(m['from'])[:30]:<31} {m['subject']}")


@app.command()
def fetch(gmail_id: str = typer.Argument(..., help="Hex Gmail message id from the connector"), out: Path = typer.Option(Path("inbox"), help="Folder for attachments"), include_inline: bool = typer.Option(False)) -> None:
    """Download a message's attachments (and print body text) into the inbox folder."""
    msg = MailClient().fetch_by_gmail_id(gmail_id)
    dest = out / gmail_id
    saved = save_attachments(msg, dest, include_inline)
    body = msg.get_body(preferencelist=("plain", "html"))
    (dest / "message.txt").parent.mkdir(parents=True, exist_ok=True)
    (dest / "message.txt").write_text(f"From: {msg.get('From')}\nTo: {msg.get('To')}\nDate: {msg.get('Date')}\nSubject: {msg.get('Subject')}\n\n{body.get_content() if body else ''}", encoding="utf-8")
    result = {"gmail_id": gmail_id, "subject": msg.get("Subject"), "from": msg.get("From"), "date": msg.get("Date"), "attachments": [str(p) for p in saved], "body": str(dest / "message.txt")}
    for p in saved:
        if p.suffix.lower() == ".ics":
            result.setdefault("invites", []).append(parse_ics(p.read_text(encoding="utf-8", errors="ignore")))
    typer.echo(json.dumps(result, indent=2, default=str))


@app.command("parse-ics")
def parse_ics_cmd(path: Path) -> None:
    """Extract start, end, location, attendees and the meeting link from an .ics file."""
    typer.echo(json.dumps(parse_ics(path.read_text(encoding="utf-8", errors="ignore")), indent=2, default=str))


@app.command()
def send(to: list[str] = typer.Option(..., "--to"), subject: str = typer.Option(..., "--subject"), body_file: Path = typer.Option(..., "--body-file"), attach: list[Path] = typer.Option([], "--attach"), cc: list[str] = typer.Option([], "--cc"), in_reply_to: Optional[str] = typer.Option(None)) -> None:
    """Send an email with attachments over SMTP. Only after the approval recorded in state."""
    message_id = MailClient().send(to, subject, body_file.read_text(encoding="utf-8"), cc=cc, attachments=attach, in_reply_to=in_reply_to)
    typer.echo(json.dumps({"sent": True, "message_id": message_id, "to": to, "attachments": [str(a) for a in attach]}))


if __name__ == "__main__":
    app()
