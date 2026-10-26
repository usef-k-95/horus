"""MCP server for the engagement state (STATE_SCHEMA.md §8.1). Launched by the plugin's .mcp.json:
    horus-state --workspace <engagement folder>
Mutating tools take an `actor` so workers declare who is writing (rule 26)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

from mcp.server.mcpserver import MCPServer

from .service import Service
from .views import render

mcp = MCPServer("horus-state", instructions="Horus engagement state. Read with status, get, list, search and view; write with create, update, link, import_document, register_version; approvals, gates and phases through their own tools. Pass your actor id on every write.")
_service: Optional[Service] = None


def service() -> Service:
    global _service
    if _service is None:
        workspace = os.environ.get("HORUS_WORKSPACE") or os.getcwd()
        _service = Service(Path(workspace))
    return _service


def _ok(payload: Any) -> str:
    return json.dumps(payload, default=str, ensure_ascii=False, indent=2)


def _err(exc: Exception) -> str:
    return json.dumps({"error": type(exc).__name__, "message": str(exc)})


@mcp.tool()
def status(format: str = "brief") -> str:
    """Resume summary: phase, pathway, gates, pending approvals, P1 questions, due actions, inbox, meetings ahead."""
    try:
        return render(service(), "status", {"format": format})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def get(collection: str, id: Optional[str] = None, expand: bool = False) -> str:
    """Fetch one record (singletons need no id). expand=true adds one-line labels for referenced records."""
    try:
        return _ok(service().get(collection, id, expand))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def list_records(collection: str, filter: Optional[dict] = None, fields: Optional[list[str]] = None, limit: int = 100, sort: Optional[str] = None) -> str:
    """Filtered listing. filter maps dotted field paths to a value or {in: [...]}, {since: iso}, {contains: x}, {not: x}."""
    try:
        return _ok(service().list(collection, filter, fields, limit, sort))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def search(query: str, collections: Optional[list[str]] = None, limit: int = 20) -> str:
    """Full-text search over statements, titles, summaries, questions and notes."""
    try:
        return _ok(service().search(query, collections, limit))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def create(collection: str, record: dict, actor: str = "principal") -> str:
    """Validated create with ID assignment; writes an event. Workers must pass their actor id (for example researcher:r-07)."""
    try:
        return _ok(service().create(collection, record, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def update(collection: str, id: Optional[str], patch: dict, reason: Optional[str] = None, actor: str = "principal") -> str:
    """Validated partial update (dicts merge, lists replace); server-managed and computed fields are rejected."""
    try:
        return _ok(service().update(collection, id, patch, reason=reason, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def append(collection: str, id: str, field: str, items: list, actor: str = "principal") -> str:
    """Append items to a list field without replacing it."""
    try:
        return _ok(service().append(collection, id, field, items, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def link(from_id: str, to_id: str, rel: str, actor: str = "principal") -> str:
    """Add a typed relation between two records."""
    try:
        return _ok(service().link(from_id, to_id, rel, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def import_document(path: str, metadata: dict, destination: str = "inbox", actor: str = "principal") -> str:
    """Copy a file into inbox/ or library/ immutably, hash it and create the document record (and a source when metadata.source is given)."""
    try:
        return _ok(service().import_document(path, metadata, destination, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def register_version(deliverable_id: str, paths: dict, change_summary: str, qa: dict, review: Optional[dict] = None, based_on_feedback: Optional[list[str]] = None, actor: str = "producer") -> str:
    """Add a deliverable version with files, QA audit results and review; status becomes qa_passed or qa_failed."""
    try:
        return _ok(service().register_version(deliverable_id, paths, change_summary, qa, review, based_on_feedback or [], actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def release_version(deliverable_id: str, v: int, sent_in: Optional[str] = None, actor: str = "principal") -> str:
    """Mark a version supervisor_approved (or sent when sent_in names the communication). Enforces QA, review and approval rules."""
    try:
        return _ok(service().release_version(deliverable_id, v, sent_in, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def request_approval(target: dict, action_class: str, summary: str, risk_class: Optional[str] = None, actor: str = "principal") -> str:
    """Create an approval request for a target {collection, id, version?}; returns not_required immediately when the autonomy level allows."""
    try:
        return _ok(service().request_approval(target, action_class, summary, risk_class, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def decide_approval(approval_id: str, decision: str, note: Optional[str] = None, conditions: Optional[list[str]] = None, actor: str = "supervisor") -> str:
    """Approve or reject a pending approval. Supervisor actors only."""
    try:
        return _ok(service().decide_approval(approval_id, decision, note, conditions or [], actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def set_gate(gate: str, status: str, decision_id: Optional[str] = None, override_reason: Optional[str] = None, actor: str = "principal") -> str:
    """Gate transition (not_ready, ready, passed). Passing needs a confirmed gate decision and satisfied criteria, or an override reason."""
    try:
        return _ok(service().set_gate(gate, status, decision_id, override_reason, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def set_phase(phase: str, override_reason: Optional[str] = None, actor: str = "principal") -> str:
    """Phase transition; requires the previous gate to be passed unless an override reason is given."""
    try:
        return _ok(service().set_phase(phase, override_reason, actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def checkpoint(done: list[str], decided: Optional[list[str]] = None, learned: Optional[list[str]] = None, next: Optional[list[str]] = None, blockers: Optional[list[str]] = None, actor: str = "principal") -> str:
    """Write the session narrative that the next session resumes from."""
    try:
        return _ok(service().checkpoint(done, decided or [], learned or [], next or [], blockers or [], actor=actor))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def view(name: str, params: Optional[dict] = None) -> str:
    """Render a named view as Markdown: status, gate_checklist, approvals_queue, pathway_summary, stakeholder_matrix, reaction_matrix, decision_log, question_register, action_tracker, evidence_table, bibliography, traceability, hypothesis_tree, appraisal_comparison, risk_register, status_note, meeting_plan, interview_debrief, timeline."""
    try:
        return render(service(), name, params or {})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def validate(scope: str = "all") -> str:
    """Run the validation rules and return issues by severity."""
    try:
        return _ok(service().validate(scope))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def export(include_profiles: bool = False) -> str:
    """Bundle the state as JSON (profiles excluded unless asked)."""
    try:
        return _ok(service().export(include_profiles))
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def record_intervention(meeting_id: str, kind: str, text: Optional[str] = None, by: str = "supervisor") -> str:
    """Log a Supervisor intervention in a live meeting (whisper, pause, resume, takeover, leave)."""
    try:
        return _ok(service().record_intervention(meeting_id, kind, text, by))
    except Exception as exc:
        return _err(exc)


@mcp.resource("horus://status")
def status_resource() -> str:
    return render(service(), "status", {"format": "context"})


@mcp.resource("horus://gates")
def gates_resource() -> str:
    return render(service(), "gate_checklist", {})


@mcp.resource("horus://approvals")
def approvals_resource() -> str:
    return render(service(), "approvals_queue", {})


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="horus-state")
    parser.add_argument("--workspace", default=os.environ.get("HORUS_WORKSPACE") or os.getcwd())
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse", "streamable-http"])
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).resolve()
    if not (workspace / ".horus" / "engagement.yaml").exists():
        print(f"horus-state: no engagement at {workspace} (run `horus init` first); serving anyway for init through the CLI", file=sys.stderr)
    os.environ["HORUS_WORKSPACE"] = str(workspace)
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
