import asyncio
import json

import pytest

from horus_meet.adapters.mock import MockBotAdapter, MockParticipant, MockTTS
from horus_meet.cli import DEFAULT_PARTICIPANT_LINES
from horus_meet.models import BotState, Speaker
from horus_meet.session import MeetingSession
from horus_meet.spike import SpikeConfig, run_spike

SCALE = 0.02


def make(tmp_path, lines, *, admit_after_s=1.2, turns=3):
    participant = MockParticipant(speaker=Speaker(id="p1", name="Test participant"), lines=lines)
    bot = MockBotAdapter(participant, admit_after_s=admit_after_s, time_scale=SCALE)
    tts = MockTTS(time_scale=SCALE)
    session = MeetingSession("MTG-T", bot, tts, tmp_path / "run", platform="mock", bot_name="Horus AI (recording)", time_scale=SCALE)
    cfg = SpikeConfig(meeting_id="MTG-T", platform="mock", meeting_url="mock://m", turns=turns, grace_s=10, listen_timeout_s=30, consent_timeout_s=30)
    return bot, session, cfg


async def test_full_success_path(tmp_path):
    bot, session, cfg = make(tmp_path, DEFAULT_PARTICIPANT_LINES, turns=3)
    report = await run_spike(cfg, session)
    assert report.outcome == "success", report.errors
    assert report.consent.ai_participant is True
    assert len(report.turns) == 3
    assert all(t.pipeline_ms > 0 for t in report.turns)
    assert report.admission_s is not None and report.admission_s > 0
    assert bot.chats and "Horus" in bot.chats[0]           # disclosure posted to chat
    assert bot.played[0].text.startswith("Hello")           # disclosure spoken first
    assert bot.left is True
    states = [s.state for s in report.states]
    assert BotState.joined in states and BotState.disclosed in states and BotState.consented in states and BotState.left in states
    data = json.loads((tmp_path / "run" / "report.json").read_text())
    assert data["summary"]["turns"] == 3 and data["summary"]["pipeline_ms_median"] > 0
    assert (tmp_path / "run" / "transcript.jsonl").exists()
    # with voice activity available, turns close on speech end and the final transcript lag is measured
    assert all(t.speech_ended_at is not None for t in report.turns)
    assert all(row["transcript_lag_ms"] is not None for row in data["turn_rows"])
    events = [json.loads(line) for line in (tmp_path / "run" / "events.jsonl").read_text().splitlines()]
    assert any(e["kind"] == "speech" for e in events)


async def test_participant_declines(tmp_path):
    bot, session, cfg = make(tmp_path, ["No, I would rather not be recorded, sorry."])
    report = await run_spike(cfg, session)
    assert report.outcome == "consent_declined"
    assert report.consent.declined is True
    assert report.turns == []
    assert any("stop here" in clip.text for clip in bot.played)


async def test_not_admitted(tmp_path):
    bot, session, cfg = make(tmp_path, DEFAULT_PARTICIPANT_LINES, admit_after_s=None)
    cfg.grace_s = 2
    report = await run_spike(cfg, session)
    assert report.outcome == "not_admitted"
    assert report.admitted_at is None
    assert bot.left is True


async def test_supervisor_leave_control_ends_interview(tmp_path):
    bot, session, cfg = make(tmp_path, DEFAULT_PARTICIPANT_LINES, turns=5)

    async def drop_leave():
        # wait until the first exchange has happened, then drop a leave control
        while len(session.report.turns) < 1:
            await asyncio.sleep(0.01)
        (session.run_dir / "controls" / "001-leave.json").write_text(json.dumps({"kind": "leave", "by": "supervisor"}))

    asyncio.create_task(drop_leave())
    report = await run_spike(cfg, session)
    assert report.outcome == "ended_by_supervisor", (report.outcome, report.errors)
    assert len(report.turns) >= 1
    assert report.controls_received and report.controls_received[0].kind.value == "leave"


async def test_whisper_overrides_next_question(tmp_path):
    bot, session, cfg = make(tmp_path, DEFAULT_PARTICIPANT_LINES, turns=2)

    async def drop_whisper():
        # consent is followed immediately by the opening question; wait for either state
        while session.state not in (BotState.consented, BotState.interviewing):
            await asyncio.sleep(0.01)
        (session.run_dir / "controls" / "001-whisper.json").write_text(json.dumps({"kind": "whisper", "text": "Ask about the 2019 pilot.", "by": "supervisor"}))

    asyncio.create_task(drop_whisper())
    report = await run_spike(cfg, session)
    assert report.outcome == "success", (report.outcome, report.errors)
    assert any(t.reply_text == "Ask about the 2019 pilot." for t in report.turns)
