"""`horus-intake`: the watcher that turns website requests into engagements. Run through ~/Horus/intake."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from .client import IntakeSettings, SiteClient
from .engage import LOG_FILE, Ledger, kickoff, log, notify_mac, process, pull, summarise_run

app = typer.Typer(help="Horus intake: pull requests from the website, open engagements, acknowledge, kick off.", no_args_is_help=True)


def claude_signed_in(claude_bin: str) -> tuple[bool, str]:
    """`claude auth status` prints JSON (loggedIn, email...) in current versions and text in older ones."""
    try:
        r = subprocess.run([claude_bin, "auth", "status"], capture_output=True, text=True, timeout=30)
    except Exception as exc:  # noqa: BLE001
        return False, f"could not run claude: {exc}"
    out = (r.stdout or "").strip()
    try:
        data = json.loads(out)
        for key in ("loggedIn", "logged_in", "isLoggedIn", "authenticated"):
            if key in data:
                return bool(data[key]), str(data.get("email") or data.get("account") or data.get("authMethod") or "")
    except ValueError:
        pass
    text = (out + " " + (r.stderr or "")).lower()
    return r.returncode == 0 and "not logged in" not in text and "logged out" not in text, out.splitlines()[0][:80] if out else ""


def _settings_and_client() -> tuple[IntakeSettings, SiteClient]:
    settings = IntakeSettings.load()
    missing = settings.missing()
    if missing:
        typer.echo("intake is not configured yet: " + "; ".join(missing))
        raise typer.Exit(code=2)
    return settings, SiteClient(settings.site_url, settings.token)


@app.command()
def check() -> None:
    """What is ready: site, token, claude sign-in, mail, settings."""
    settings = IntakeSettings.load()
    problems = 0
    typer.echo(f"site: {settings.site_url or '(not set yet: run ~/Horus/deploy-site)'}")
    if settings.site_url:
        try:
            h = SiteClient(settings.site_url, settings.token).health()
            typer.echo(f"  reachable, version {h.get('version')}, request store {'on' if h.get('storage') else 'OFF'}, email notifications {'on' if h.get('notifications') else 'off'}")
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  not reachable: {exc}")
            problems += 1
        if settings.token:
            try:
                n = len(SiteClient(settings.site_url, settings.token).pending())
                typer.echo(f"  intake token accepted; {n} request(s) waiting")
            except Exception as exc:  # noqa: BLE001
                typer.echo(f"  intake token rejected or API unavailable: {exc}")
                problems += 1
    else:
        problems += 1
    typer.echo(f"token: {'set' if settings.token else 'missing (run ~/Horus/configure-site)'}")
    typer.echo(f"claude: {settings.claude_bin or 'NOT FOUND (install the Claude app, or set HORUS_CLAUDE_BIN)'}")
    if settings.claude_bin:
        try:
            signed, who = claude_signed_in(settings.claude_bin)
            typer.echo(f"  {'signed in' if signed else 'NOT signed in: run ~/Horus/intake login'}" + (f" ({who})" if who else ""))
            problems += 0 if signed else 1
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  sign-in unknown: {exc}")
    from horus_mail import MailSettings

    mail = MailSettings.load()
    typer.echo(f"acknowledgement emails: {'on' if settings.auto_ack else 'off'}; mail {'configured' if not mail.missing() else 'NOT configured (' + ', '.join(mail.missing()) + ')'}" + (f"; written from {mail.from_address or mail.user}" if mail.user else ""))
    typer.echo(f"automatic kick-off: {'on' if settings.autostart else 'off'} (max {settings.max_turns} turns)")
    typer.echo(f"engagements folder: {settings.engagements_dir}")
    raise typer.Exit(code=1 if problems else 0)


@app.command()
def pending() -> None:
    """Requests waiting at the site."""
    _, client = _settings_and_client()
    rows = client.pending()
    if not rows:
        typer.echo("no requests waiting")
        return
    for r in rows:
        typer.echo(f"{r['id']}  {r.get('received_at', '')[:16]}  {r.get('kind', ''):<10} {r.get('organisation', '')[:40]:<40} {r.get('name', '')[:30]}  {'+file' if r.get('attachment') else ''}")


@app.command("pull")
def pull_cmd(no_kickoff: bool = typer.Option(False, "--no-kickoff", help="Create the engagement without starting Horus"), no_ack: bool = typer.Option(False, "--no-ack", help="Do not email the requester"), quiet: bool = typer.Option(False, "--quiet", help="Print nothing when there is nothing to do")) -> None:
    """One pass: take every new request, open its engagement, acknowledge, kick off."""
    settings, client = _settings_and_client()
    try:
        results = pull(client, settings, do_ack=not no_ack, do_kickoff=not no_kickoff)
    except Exception as exc:  # noqa: BLE001
        log(f"pull failed: {exc}")
        typer.echo(f"pull failed: {exc}")
        raise typer.Exit(code=1)
    new = [r for r in results if "code" in r and not r.get("skipped")]
    if not results and quiet:
        return
    if not results:
        typer.echo("no new requests")
        return
    for r in results:
        if r.get("error"):
            typer.echo(f"{r.get('id')}: failed: {r['error']}")
        elif r.get("skipped"):
            typer.echo(f"{r['id']}: {r['skipped']} ({r.get('code')})")
        else:
            typer.echo(f"{r['id']}: engagement {r['code']} at {r['folder']}" + ("; acknowledged" if r.get("acknowledged") else "") + ("; kick-off started" if r.get("kickoff_log") else ""))
    if new:
        typer.echo(f"{len(new)} engagement(s) opened")


@app.command("kickoff")
def kickoff_cmd(code: str = typer.Argument(..., help="Engagement code under the engagements folder")) -> None:
    """Start (or restart) the unattended kick-off for an engagement opened from the website."""
    settings = IntakeSettings.load()
    folder = settings.engagements_dir / code
    req_file = folder / "inbox" / "request.json"
    if not req_file.exists():
        typer.echo(f"no website request at {req_file}")
        raise typer.Exit(code=2)
    request = json.loads(req_file.read_text(encoding="utf-8"))
    ack = folder / "inbox" / "acknowledgement-sent.md"
    path = kickoff(folder, request, code, ack if ack.exists() else None, settings)
    if not path:
        typer.echo("kick-off not started: the claude command was not found")
        raise typer.Exit(code=1)
    typer.echo(f"kick-off started for {code}; log: {path}")


@app.command(hidden=True)
def finished(code: str, status: str, log_path: Path) -> None:
    """Internal: called by the kick-off wrapper when the claude run ends."""
    s = summarise_run(code, status, log_path)
    summary_path = log_path.with_name(log_path.stem + "-summary.md")
    first_line = (s["result"].strip().splitlines() or ["(no result text)"])[0][:200]
    summary_path.write_text(
        f"# Kick-off run for {code}\n\n- Exit status: {status}\n- Turns: {s['num_turns']}\n- Cost (USD): {s['cost_usd']}\n- Duration (s): {s['duration_s']}\n- Error: {s['is_error']}\n- Log: {log_path}\n\n## Result\n\n{s['result'] or '(none)'}\n",
        encoding="utf-8",
    )
    if s["not_logged_in"]:
        log(f"{code}: kick-off could not run, claude is not signed in. Run ~/Horus/intake login, then ~/Horus/intake kickoff {code}")
        notify_mac("Horus", f"Kick-off for {code} needs a sign-in: run ~/Horus/intake login, then ~/Horus/intake kickoff {code}")
        return
    log(f"{code}: kick-off finished (exit {status}, turns {s['num_turns']}, cost {s['cost_usd']}): {first_line}")
    notify_mac("Horus", f"Kick-off finished for {code}. Open the folder in the Claude app to see what waits for your approval.")


@app.command("test-submit")
def test_submit(to: Optional[str] = typer.Option(None, "--to", help="Email the acknowledgement goes to (default: your own address)"), demo: bool = typer.Option(False, "--demo", help="Send a demo request instead of a scope of work")) -> None:
    """Send a fictional request to your own site, exactly as a client would; then `pull` processes it."""
    settings, client = _settings_and_client()
    email = to or settings.notify_email or settings.mail_user
    if not email:
        typer.echo("give --to EMAIL")
        raise typer.Exit(code=2)
    scope = (
        "Terms of reference: a national strategy for SME e-invoicing adoption.\n\n"
        "The Ministry of Finance seeks advice on how to bring 1.2 million small and medium enterprises onto the national e-invoicing "
        "system within three years without harming their liquidity. The engagement should assess adoption barriers, consult the chambers "
        "of commerce, the tax authority and software vendors, appraise phased mandate options against incentives and support schemes, and "
        "recommend a path with an implementation plan and a communication plan. Deliverables: a decision memo, an executive deck and an options appraisal."
    )
    fields = {"name": "Horus test, Supervisor", "email": email, "organisation": "Horus test", "country": "Egypt", "scope_text": scope, "page": f"{settings.site_url}/"}
    if demo:
        fields["preferred_week"] = "the week after next"
    result = client.submit("demo" if demo else "engagement", fields, file=("test-scope-of-work.md", scope.encode("utf-8"), "text/markdown"))
    if not result.get("ok"):
        typer.echo(f"the site refused the test request (HTTP {result.get('http_status')}): {result.get('error')}")
        raise typer.Exit(code=1)
    typer.echo(f"test request {result.get('id')} received by {settings.site_url}; now run: ~/Horus/intake pull")


if __name__ == "__main__":
    app()
