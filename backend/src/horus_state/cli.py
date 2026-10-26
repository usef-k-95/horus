"""`horus` — the Supervisor console and maintenance commands for the engagement state."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import typer

from .models import COLLECTIONS, model_for
from .service import Service
from .views import VIEWS, render

app = typer.Typer(help="Horus engagement state: Supervisor console, views, validation, maintenance.", no_args_is_help=True)


@app.callback()
def _main(workspace: Optional[Path] = typer.Option(None, "--workspace", "-w", help="Engagement folder (default: current directory or $HORUS_WORKSPACE)")) -> None:
    """Horus engagement state console."""
    if workspace is not None:
        os.environ["HORUS_WORKSPACE"] = str(Path(workspace).resolve())
meet_app = typer.Typer(help="Live-meeting controls (forwarded to the horus-meet runtime's control channel).")
settings_app = typer.Typer(help="Engagement settings.")
schema_app = typer.Typer(help="Schema utilities.")
app.add_typer(meet_app, name="meet")
app.add_typer(settings_app, name="settings")
app.add_typer(schema_app, name="schema")

WORKSPACE_OPT = typer.Option(None, "--workspace", "-w", help="Engagement folder (default: current directory or $HORUS_WORKSPACE)")
ACTOR_OPT = typer.Option(None, "--actor", help="Actor id (default: supervisor:<user>)")


def _svc(workspace: Optional[Path], actor: Optional[str] = None) -> Service:
    ws = workspace or Path(os.environ.get("HORUS_WORKSPACE") or os.getcwd())
    actor = actor or f"supervisor:{os.environ.get('USER', 'supervisor')}"
    return Service(ws, actor=actor)


def _echo_json(data) -> None:
    typer.echo(json.dumps(data, default=str, ensure_ascii=False, indent=2))


@app.command()
def init(code: str = typer.Argument(..., help="Engagement code, for example EGY-2026-003-sme-digital"), name: str = typer.Option(..., help="Engagement name"), entity: str = typer.Option(..., help="Client entity"), country: str = typer.Option(..., help="ISO country code"), pathway: Optional[str] = typer.Option(None, help="Primary pathway if already known"), supervisor: list[str] = typer.Option([], help="Supervisor names"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Create a new engagement in the folder."""
    svc = _svc(workspace, actor="principal")
    eng = svc.init_engagement(code, name, {"entity": entity, "country": country}, pathway_primary=pathway, supervisors=supervisor or [os.environ.get("USER", "supervisor")])
    typer.echo(f"initialised {eng['code']} at {svc.store.root}")


@app.command()
def status(format: str = typer.Option("brief", help="brief, context or full"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Where the engagement stands."""
    typer.echo(render(_svc(workspace), "status", {"format": format}))


@app.command()
def view(name: str = typer.Argument(..., help=f"One of: {', '.join(sorted(VIEWS))}"), param: list[str] = typer.Option([], "--param", "-p", help="key=value view parameters"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Render a view."""
    params = dict(p.split("=", 1) for p in param)
    typer.echo(render(_svc(workspace), name, params))


@app.command()
def validate(workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Run the validation rules."""
    issues = _svc(workspace).validate()
    for i in issues:
        typer.echo(f"[{i['severity']}] rule {i['rule']} {i['collection']}/{i['id']}: {i['message']}")
    typer.echo(f"{len(issues)} issue(s)")
    raise typer.Exit(code=1 if any(i["severity"] == "error" for i in issues) else 0)


@app.command()
def approvals(workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Pending approvals."""
    typer.echo(render(_svc(workspace), "approvals_queue", {}))


@app.command()
def approve(approval_id: str, note: Optional[str] = typer.Option(None, "--note"), condition: list[str] = typer.Option([], "--condition"), workspace: Optional[Path] = WORKSPACE_OPT, actor: Optional[str] = ACTOR_OPT) -> None:
    """Approve a pending approval."""
    _echo_json(_svc(workspace, actor).decide_approval(approval_id, "approved", note, condition))


@app.command()
def reject(approval_id: str, note: str = typer.Option(..., "--note"), workspace: Optional[Path] = WORKSPACE_OPT, actor: Optional[str] = ACTOR_OPT) -> None:
    """Reject a pending approval with a reason."""
    _echo_json(_svc(workspace, actor).decide_approval(approval_id, "rejected", note))


@app.command()
def gates(gate: Optional[str] = typer.Argument(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Gate checklists."""
    typer.echo(render(_svc(workspace), "gate_checklist", {"gate": gate} if gate else {}))


@app.command()
def events(follow: bool = typer.Option(False, "--follow", "-f"), last: int = typer.Option(20, help="Show the last N events first"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Event stream (audit log)."""
    svc = _svc(workspace)
    seen = 0
    all_events = list(svc.store.iter_events())
    for ev in all_events[-last:]:
        typer.echo(f"{ev['ts'][:19]} {ev['actor']:<22} {ev['op']:<12} {ev.get('record_id') or '':<10} {ev['summary']}")
    seen = len(all_events)
    while follow:
        time.sleep(1.0)
        all_events = list(svc.store.iter_events())
        for ev in all_events[seen:]:
            typer.echo(f"{ev['ts'][:19]} {ev['actor']:<22} {ev['op']:<12} {ev.get('record_id') or '':<10} {ev['summary']}")
        seen = len(all_events)


@app.command()
def checkpoint(done: list[str] = typer.Option([], "--done"), decided: list[str] = typer.Option([], "--decided"), learned: list[str] = typer.Option([], "--learned"), next: list[str] = typer.Option([], "--next"), blocker: list[str] = typer.Option([], "--blocker"), workspace: Optional[Path] = WORKSPACE_OPT, actor: Optional[str] = ACTOR_OPT) -> None:
    """Write a checkpoint event."""
    _echo_json(_svc(workspace, actor).checkpoint(done, decided, learned, next, blocker))


@app.command()
def export(include_profiles: bool = typer.Option(False), out: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Export the state as JSON."""
    data = _svc(workspace).export(include_profiles)
    if out:
        out.write_text(json.dumps(data, default=str, indent=2), encoding="utf-8")
        typer.echo(f"wrote {out}")
    else:
        _echo_json(data)


@app.command()
def reindex(workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Rebuild the derived index."""
    typer.echo(f"indexed {_svc(workspace).store.reindex()} records")


@app.command("get")
def get_record(collection: str, id: Optional[str] = typer.Argument(None), expand: bool = typer.Option(False), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Print a record."""
    _echo_json(_svc(workspace).get(collection, id, expand))


@app.command("list")
def list_records(collection: str, filter: Optional[str] = typer.Option(None, help="JSON filter"), limit: int = typer.Option(50), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """List records (ids, status and label)."""
    svc = _svc(workspace)
    for r in svc.list(collection, json.loads(filter) if filter else None, limit=limit):
        label = r.get("title") or r.get("name") or r.get("statement") or r.get("summary") or r.get("question") or ""
        typer.echo(f"{r['id']:<10} {str(r.get('status', '')):<16} {label[:90]}")


@settings_app.command("autonomy")
def settings_autonomy(profile: Optional[str] = typer.Option(None, help="default or shadow"), set_: list[str] = typer.Option([], "--set", help="class=level"), workspace: Optional[Path] = WORKSPACE_OPT, actor: Optional[str] = ACTOR_OPT) -> None:
    """Show or change the autonomy profile and levels."""
    svc = _svc(workspace, actor)
    if profile or set_:
        levels = dict(s.split("=", 1) for s in set_)
        svc.set_autonomy(profile, levels or None)
    eng = svc.engagement()
    aut = (eng.get("settings") or {}).get("autonomy") or {}
    typer.echo(f"profile: {aut.get('profile')}")
    for k, v in sorted((aut.get("levels") or {}).items()):
        typer.echo(f"  {k:<28} {v}")


@meet_app.command("whisper")
def meet_whisper(meeting_id: str, text: str, run_dir: Optional[Path] = typer.Option(None, help="Run folder of the live session (defaults to meetings/<id>/live)"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Send a private instruction to the interviewer during a live meeting."""
    _control(workspace, meeting_id, "whisper", text, run_dir)


@meet_app.command("pause")
def meet_pause(meeting_id: str, run_dir: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    _control(workspace, meeting_id, "pause", None, run_dir)


@meet_app.command("resume")
def meet_resume(meeting_id: str, run_dir: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    _control(workspace, meeting_id, "resume", None, run_dir)


@meet_app.command("takeover")
def meet_takeover(meeting_id: str, run_dir: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    _control(workspace, meeting_id, "takeover", None, run_dir)


@meet_app.command("leave")
def meet_leave(meeting_id: str, run_dir: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    _control(workspace, meeting_id, "leave", None, run_dir)


@meet_app.command("watch")
def meet_watch(meeting_id: str, run_dir: Optional[Path] = typer.Option(None), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Tail the live transcript and events of a meeting."""
    svc = _svc(workspace)
    folder = run_dir or (svc.store.workspace / "meetings" / meeting_id / "live")
    events_path = folder / "events.jsonl"
    typer.echo(f"watching {events_path} (Ctrl-C to stop)")
    seen = 0
    while True:
        if events_path.exists():
            lines = events_path.read_text(encoding="utf-8").splitlines()
            for line in lines[seen:]:
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("kind") in ("say", "state", "control", "consent", "barge_in", "speech", "latency", "turn", "error", "chat"):
                    typer.echo(f"{ev.get('t', 0):>8.1f}s {ev.get('kind'):<9} {json.dumps({k: v for k, v in ev.items() if k not in ('t', 'kind')}, ensure_ascii=False)[:160]}")
            seen = len(lines)
        time.sleep(1.0)


def _control(workspace: Optional[Path], meeting_id: str, kind: str, text: Optional[str], run_dir: Optional[Path]) -> None:
    svc = _svc(workspace)
    folder = run_dir or (svc.store.workspace / "meetings" / meeting_id / "live")
    controls = folder / "controls"
    controls.mkdir(parents=True, exist_ok=True)
    path = controls / f"{int(time.time() * 1000)}-{kind}.json"
    path.write_text(json.dumps({"kind": kind, "text": text, "by": os.environ.get("USER", "supervisor")}), encoding="utf-8")
    try:
        svc.record_intervention(meeting_id, kind, text, by=os.environ.get("USER", "supervisor"))
    except Exception as exc:  # the meeting record may not exist in a spike
        typer.echo(f"(not recorded in state: {exc})")
    typer.echo(f"queued {kind} for {meeting_id}")


@schema_app.command("export")
def schema_export(out: Path = typer.Option(Path("schemas"), help="Output folder"), workspace: Optional[Path] = WORKSPACE_OPT) -> None:
    """Write one JSON Schema per collection."""
    out.mkdir(parents=True, exist_ok=True)
    for name, model in COLLECTIONS.items():
        (out / f"{name}.schema.json").write_text(json.dumps(model.model_json_schema(by_alias=True), indent=2), encoding="utf-8")
    typer.echo(f"wrote {len(COLLECTIONS)} schemas to {out}")


if __name__ == "__main__":
    app()
