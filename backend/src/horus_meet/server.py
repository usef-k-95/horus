"""MCP server for live meetings (ARCHITECTURE.md §5.5). Launched by the plugin's .mcp.json:
    horus-meet-mcp --workspace <engagement folder>
The interviewer worker drives a meeting with join → disclose → consent → listen/say loop → leave.
Supervisor controls arrive through the run folder's controls channel (`horus meet whisper|pause|leave`)."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

from mcp.server.mcpserver import MCPServer

from .adapters.base import BotAdapter, TTSAdapter
from .bridge import StateBridge
from .config import Settings
from .models import ControlKind
from .session import MeetingSession
from .spike import DISCLOSURE_CHAT

mcp = MCPServer("horus-meet", instructions="Live meetings for Horus. Call join, then disclose, then consent after the participant answers, then loop listen and say, then leave. Honour controls returned by listen (whisper, pause, resume, takeover, leave) immediately.")

_sessions: dict[str, dict[str, Any]] = {}
_ingress = None
_settings: Optional[Settings] = None


def settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings


def workspace() -> Path:
    return Path(os.environ.get("HORUS_WORKSPACE") or os.getcwd())


def _ok(payload: Any) -> str:
    return json.dumps(payload, default=str, ensure_ascii=False)


def _err(exc: Exception) -> str:
    return json.dumps({"error": type(exc).__name__, "message": str(exc)})


def _entry(meeting_id: str) -> dict[str, Any]:
    try:
        return _sessions[meeting_id]
    except KeyError as exc:
        raise KeyError(f"no live session for {meeting_id}; call join first") from exc


async def _build(meeting_id: str, chat_text: Optional[str]) -> tuple[BotAdapter, TTSAdapter, Optional[object]]:
    global _ingress
    cfg = settings()
    provider = os.environ.get("HORUS_MEET_PROVIDER") or os.environ.get("EVAL_HORUS_MEET_PROVIDER") or cfg.provider
    if provider == "mock":
        from .adapters.mock import MockBotAdapter, MockParticipant, MockTTS
        from .models import Speaker

        lines = json.loads(os.environ.get("HORUS_MEET_MOCK_LINES") or "[]") or ["Yes, that's fine.", "Cost is the main obstacle.", "Start with firms already filing online. Goodbye."]
        scale = float(os.environ.get("HORUS_MEET_MOCK_SCALE") or os.environ.get("EVAL_HORUS_MEET_MOCK_SCALE") or "1.0")
        return MockBotAdapter(MockParticipant(Speaker(id="p1", name=os.environ.get("HORUS_MEET_MOCK_NAME", "Participant")), lines), time_scale=scale), MockTTS(time_scale=scale), None
    from .adapters.elevenlabs import ElevenLabsTTS

    if provider == "meetstream":
        from .adapters.meetstream import Ingress, MeetStreamBotAdapter

        missing = cfg.missing_for_real_run()
        if missing:
            raise RuntimeError("not configured: " + ", ".join(missing))
        if _ingress is None:
            _ingress = Ingress(port=cfg.local_port)
        tts = ElevenLabsTTS(cfg.elevenlabs_api_key, cfg.elevenlabs_voice_id, model_id=cfg.elevenlabs_model_id, output_format=cfg.elevenlabs_output_format)
        bot = MeetStreamBotAdapter(cfg.meetstream_api_key, _ingress, cfg.public_base_url, api_base=cfg.meetstream_api_base, transcript_preset=cfg.transcript_preset, bot_message=chat_text or DISCLOSURE_CHAT, custom_attributes={"meeting_id": meeting_id})
        return bot, tts, _ingress
    if provider == "recall":
        from .adapters.recall import RecallBotAdapter

        tts = ElevenLabsTTS(cfg.elevenlabs_api_key, cfg.elevenlabs_voice_id, model_id=cfg.elevenlabs_model_id, output_format="mp3_44100_128")
        placeholder = await tts.synthesize("Hello.")
        bot = RecallBotAdapter(cfg.recall_api_key, cfg.recall_region, cfg.public_ws_url, local_ws_port=cfg.local_ws_port, placeholder_clip=placeholder)
        return bot, tts, None
    raise RuntimeError(f"unknown provider {provider!r}")


@mcp.tool()
async def join(meeting_id: str, meeting_url: str, display_name: Optional[str] = None, platform: str = "meet", grace_s: int = 300, chat_text: Optional[str] = None, conduct_mode: str = "interviewer") -> str:
    """Dispatch the Horus bot into a meeting and wait for admission. Fails before dispatch when the engagement state says the meeting plan is not approved or has no disclosure script."""
    try:
        if meeting_id in _sessions:
            return _ok({"state": _sessions[meeting_id]["session"].state.value, "note": "already joined"})
        bridge = StateBridge(workspace(), meeting_id)
        bridge.check_can_join(conduct_mode)  # raises on rules 21 and 22
        bot, tts, ingress = await _build(meeting_id, chat_text)
        run_dir = workspace() / "meetings" / meeting_id / "live"
        session = MeetingSession(meeting_id, bot, tts, run_dir, platform=platform, bot_name=display_name or settings().bot_name)
        _sessions[meeting_id] = {"session": session, "bot": bot, "bridge": bridge, "ingress": ingress}
        admitted = await session.start(meeting_url, grace_s)
        bridge.on_bot_created(getattr(bot, "name", "unknown"), getattr(bot, "bot_id", "") or "", session.report.bot_name)
        if not admitted:
            await session.leave(None)
            _sessions.pop(meeting_id, None)
            return _ok({"state": "not_admitted", "run_dir": str(run_dir)})
        bridge.on_admitted()
        return _ok({"state": session.state.value, "bot_id": getattr(bot, "bot_id", None), "run_dir": str(run_dir), "admission_s": session.report.admission_s})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def disclose(meeting_id: str, script: str, chat_text: Optional[str] = None, script_id: Optional[str] = None) -> str:
    """Speak the disclosure script and post the short chat version. Do this within the first minute."""
    try:
        e = _entry(meeting_id)
        await e["session"].disclose(script, chat_text or DISCLOSURE_CHAT)
        e["bridge"].on_disclosed(script, script_id)
        return _ok({"state": e["session"].state.value})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def consent(meeting_id: str, granted: bool, given_by: Optional[str] = None, attribution_rule: str = "background", recording: bool = True, text: Optional[str] = None) -> str:
    """Record the participant's consent decision (given_by is a stakeholder id). When granted is false, say goodbye and call leave."""
    try:
        e = _entry(meeting_id)
        s: MeetingSession = e["session"]
        from .models import Speaker, Turn

        turn = Turn(speaker=Speaker(id=given_by or "unknown"), text=text or ("consent given" if granted else "declined"), start=0, end=0, last_final_received_at=s.clock(), completed_at=s.clock(), utterances=1)
        s.record_consent(turn, granted)
        e["bridge"].on_consent(granted, given_by, attribution_rule, recording, text)
        return _ok({"state": s.state.value, "granted": granted})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def listen(meeting_id: str, max_wait_s: float = 45.0) -> str:
    """Wait until the participant finishes a turn or a Supervisor control arrives. Returns turns (text, speaker, provisional), controls and whether the meeting ended."""
    try:
        e = _entry(meeting_id)
        result = await e["session"].listen(max_wait_s)
        for c in result.controls:
            e["bridge"].on_intervention(c.kind.value, c.text, c.by)
        return _ok({"turns": [{"speaker": t.speaker.name or t.speaker.id, "speaker_id": t.speaker.id, "text": t.text, "provisional": t.provisional, "completed_at": round(t.completed_at, 2)} for t in result.turns], "controls": [{"kind": c.kind.value, "text": c.text, "by": c.by} for c in result.controls], "silence": result.silence, "ended": result.ended, "elapsed_s": round(result.elapsed_s, 1), "state": e["session"].state.value})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def say(meeting_id: str, text: str) -> str:
    """Speak to the meeting. Keep it to one or two sentences; participants cannot interrupt long passages gracefully."""
    try:
        e = _entry(meeting_id)
        await e["session"].say(text)
        return _ok({"spoke": text, "speaking_until": round(e["session"].speaking_until, 2)})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def chat(meeting_id: str, text: str) -> str:
    """Post a message in the meeting chat (links, the disclosure text, a summary)."""
    try:
        e = _entry(meeting_id)
        await e["bot"].send_chat(text)
        e["session"]._log("chat", text=text)
        return _ok({"posted": text})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def mark(meeting_id: str, label: str, note: Optional[str] = None) -> str:
    """Timestamp a labelled moment: consent_given, off_record_start, off_record_end, document_promised, document_shared, directive, decision, referral."""
    try:
        e = _entry(meeting_id)
        at = e["session"].clock()
        e["session"]._log("mark", label=label, note=note)
        e["bridge"].on_mark(label, at, note)
        return _ok({"label": label, "at": round(at, 2)})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def status(meeting_id: str) -> str:
    """Current state, elapsed time, turns so far, latency statistics."""
    try:
        e = _entry(meeting_id)
        s: MeetingSession = e["session"]
        return _ok({"state": s.state.value, "elapsed_s": round(s.clock(), 1), "turns_timed": len(s.report.turns), "transcript_utterances": len(s.transcript), "summary": s.report.summary()})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def transcript(meeting_id: str, since: int = 0) -> str:
    """Final transcript utterances captured so far, starting at index `since`."""
    try:
        e = _entry(meeting_id)
        items = e["session"].transcript[since:]
        return _ok({"from": since, "count": len(items), "utterances": [{"i": since + i, "speaker": u.speaker.name or u.speaker.id, "text": u.text, "start": round(u.start, 1), "end": round(u.end, 1)} for i, u in enumerate(items)]})
    except Exception as exc:
        return _err(exc)


@mcp.tool()
async def leave(meeting_id: str, closing_text: Optional[str] = None, exit_reason: str = "completed") -> str:
    """Say the closing text, leave the meeting, archive the transcript and write the meeting facts to state."""
    try:
        e = _sessions.pop(meeting_id, None)
        if e is None:
            return _ok({"state": "not_live"})
        s: MeetingSession = e["session"]
        await s.leave(closing_text)
        summary = s.report.summary()
        coverage = {"asked": len(s.report.turns), "total": len(s.report.turns), "skipped": []}
        latency = {k: v for k, v in summary.items() if k.endswith("_ms_median") or k.endswith("_ms_p95")}
        transcript_path = str((s.run_dir / "transcript.jsonl").relative_to(workspace())) if (s.run_dir / "transcript.jsonl").exists() else None
        e["bridge"].on_left(transcript_path, len(s.transcript), coverage, {k: (v or 0) for k, v in latency.items()}, exit_reason, getattr(e["bot"], "name", "unknown"))
        post = None
        if hasattr(e["bot"], "fetch_post_call"):
            try:
                post = await e["bot"].fetch_post_call()
                (s.run_dir / "post_call.json").write_text(json.dumps(post, default=str, indent=2), encoding="utf-8")
            except Exception as exc:  # post-call data is a bonus, never a blocker
                post = {"error": str(exc)}
        s.write_report()
        return _ok({"state": s.state.value, "outcome": s.report.outcome, "report": str(s.run_dir / "report.md"), "transcript": transcript_path, "post_call": "post_call.json" if post else None})
    except Exception as exc:
        return _err(exc)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="horus-meet-mcp")
    parser.add_argument("--workspace", default=os.environ.get("HORUS_WORKSPACE") or os.getcwd())
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse", "streamable-http"])
    args = parser.parse_args(argv)
    os.environ["HORUS_WORKSPACE"] = str(Path(args.workspace).resolve())
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
