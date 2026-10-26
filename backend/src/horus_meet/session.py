"""The per-meeting session: state machine, transcript store, controls, latency metrics."""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from .adapters.base import BotAdapter, TTSAdapter
from .models import (
    BotState,
    BotStatusEvent,
    ControlEvent,
    ControlKind,
    LatencySample,
    SpeechEvent,
    SpikeReport,
    Turn,
    Utterance,
)
from .turns import TurnTaker

log = logging.getLogger(__name__)

AFFIRMATIVE = re.compile(r"\b(yes|yeah|yep|sure|okay|ok|fine|of course|go ahead|that's fine|agreed|agree|no problem|absolutely|certainly)\b", re.I)
NEGATIVE = re.compile(r"\b(no|not|don't|do not|decline|stop|without recording|rather not|uncomfortable|refuse)\b", re.I)

_TERMINAL = {BotState.left, BotState.aborted}
_PROGRESS = [
    BotState.requested,
    BotState.joining,
    BotState.waiting_room,
    BotState.joined,
    BotState.disclosed,
    BotState.consented,
    BotState.interviewing,
    BotState.wrapping_up,
]


class ListenResult(BaseModel):
    turns: list[Turn] = Field(default_factory=list)
    controls: list[ControlEvent] = Field(default_factory=list)
    silence: bool = False
    ended: bool = False
    elapsed_s: float = 0.0


class MeetingSession:
    def __init__(
        self,
        meeting_id: str,
        bot: BotAdapter,
        tts: TTSAdapter,
        run_dir: Path,
        *,
        platform: str,
        bot_name: str,
        silence_s: float = 0.8,
        time_scale: float = 1.0,
        tick_s: float = 0.1,
    ) -> None:
        self.meeting_id = meeting_id
        self.bot = bot
        self.tts = tts
        self.run_dir = run_dir
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / "controls").mkdir(exist_ok=True)
        self.scale = time_scale
        self.tick_s = tick_s
        self.state = BotState.requested
        self._t0 = time.monotonic()
        self._turntaker = TurnTaker(silence_s=silence_s * time_scale)
        self._turns: deque[Turn] = deque()
        self._controls: deque[ControlEvent] = deque()
        self._joined = asyncio.Event()
        self._ended = asyncio.Event()
        self._pump: Optional[asyncio.Task] = None
        self.transcript: list[Utterance] = []
        self.speaking_until = 0.0
        self.paused = False
        self.report = SpikeReport(
            meeting_id=meeting_id,
            platform=platform,
            provider=getattr(bot, "name", "unknown"),
            tts_provider=getattr(tts, "name", "unknown"),
            bot_name=bot_name,
            started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        if hasattr(bot, "raw_events_path"):
            bot.raw_events_path = str(self.run_dir / "provider-events.jsonl")

    # -- clock and logging -------------------------------------------------------------
    def clock(self) -> float:
        return time.monotonic() - self._t0

    def _log(self, kind: str, **payload) -> None:
        record = {"t": round(self.clock(), 3), "kind": kind, **payload}
        with open(self.run_dir / "events.jsonl", "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=str) + "\n")

    def _set_state(self, state: BotState, detail: Optional[str] = None) -> None:
        if state in _PROGRESS and self.state in _PROGRESS and _PROGRESS.index(state) < _PROGRESS.index(self.state):
            return  # never regress (for example a late `joined` status after disclosure)
        self.state = state
        event = BotStatusEvent(state=state, detail=detail, at=self.clock())
        self.report.states.append(event)
        self._log("state", state=state.value, detail=detail)

    # -- lifecycle ----------------------------------------------------------------------
    async def start(self, meeting_url: str, grace_s: float) -> bool:
        self.report.join_requested_at = self.clock()
        bot_id = await self.bot.join(meeting_url, self.report.bot_name)
        self._log("join_requested", bot_id=bot_id, meeting_url=meeting_url)
        self._pump = asyncio.create_task(self._pump_events())
        joined = asyncio.create_task(self._joined.wait())
        ended = asyncio.create_task(self._ended.wait())
        done, pending = await asyncio.wait({joined, ended}, timeout=grace_s * self.scale, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        if joined in done:
            self.report.admitted_at = self.clock()
            return True
        if ended in done:
            # the provider gave up before anyone admitted the bot (invalid link, denied, failed): stop waiting now
            self._log("join_failed", state=self.state.value)
            return False
        self._log("not_admitted", grace_s=grace_s)
        return False

    async def _pump_events(self) -> None:
        try:
            async for event in self.bot.events():
                now = self.clock()
                if isinstance(event, BotStatusEvent):
                    self._set_state(event.state, event.detail)
                    if event.state == BotState.joined:
                        self._joined.set()
                    if event.state in _TERMINAL:
                        self._ended.set()
                elif isinstance(event, SpeechEvent):
                    event.at = now
                    if event.speaker.is_bot:
                        continue
                    self._log("speech", speaker=event.speaker.name or event.speaker.id, speaking=event.speaking)
                    self._turntaker.speech(event)
                    if event.speaking and now < self.speaking_until:
                        self._log("barge_in", speaker=event.speaker.name or event.speaker.id, text=None)
                        try:
                            await self.bot.stop_audio()
                            self.speaking_until = now
                        except Exception as exc:
                            self._log("error", where="stop_audio", error=repr(exc))
                elif isinstance(event, Utterance):
                    event.received_at = now
                    if not event.speaker.is_bot and now < self.speaking_until and event.is_final:
                        self._log("barge_in", speaker=event.speaker.name or event.speaker.id, text=event.text)
                    if event.is_final:
                        self.transcript.append(event)
                        with open(self.run_dir / "transcript.jsonl", "a", encoding="utf-8") as handle:
                            handle.write(event.model_dump_json() + "\n")
                    for turn in self._turntaker.feed(event):
                        self._turns.append(turn)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # the pump must never die silently
            self.report.errors.append(f"event pump: {exc!r}")
            self._log("error", where="pump", error=repr(exc))
        finally:
            self._ended.set()

    # -- speaking -----------------------------------------------------------------------
    async def say(self, text: str, *, turn: Optional[Turn] = None) -> Optional[LatencySample]:
        synth_started = self.clock()
        clip = await self.tts.synthesize(text)
        synth_done = self.clock()
        requested = self.clock()
        start_offset = await self.bot.play_audio(clip)
        started = requested + start_offset if start_offset is not None else self.clock()
        duration = clip.duration_s if clip.duration_s is not None else max(1.0, len(text.split()) / 2.6)
        self.speaking_until = started + duration * self.scale
        self._log("say", text=text, synth_ms=round((synth_done - synth_started) * 1000, 1), duration_s=round(duration, 2))
        if turn is None:
            return None
        sample = LatencySample(
            turn_text=turn.text,
            reply_text=text,
            last_final_received_at=turn.last_final_received_at,
            speech_ended_at=turn.speech_ended_at,
            turn_completed_at=turn.completed_at,
            synth_started_at=synth_started,
            synth_done_at=synth_done,
            playback_requested_at=requested,
            playback_started_at=started,
        )
        self.report.turns.append(sample)
        self._log("latency", **sample.as_row())
        return sample

    async def wait_until_quiet(self) -> None:
        remaining = self.speaking_until - self.clock()
        if remaining > 0:
            await asyncio.sleep(remaining)

    async def disclose(self, script: str, chat_text: Optional[str] = None) -> None:
        await self.bot.send_chat(chat_text or script)
        await self.say(script)
        self.report.disclosure_at = self.clock()
        self._set_state(BotState.disclosed, "disclosure delivered by voice and chat")

    # -- listening ----------------------------------------------------------------------
    def _ingest_controls(self) -> None:
        controls_dir = self.run_dir / "controls"
        for path in sorted(controls_dir.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                event = ControlEvent(kind=ControlKind(payload["kind"]), text=payload.get("text"), at=self.clock(), by=payload.get("by", "supervisor"))
                self._controls.append(event)
                self.report.controls_received.append(event)
                self._log("control", control=event.kind.value, text=event.text, by=event.by)
            except (ValueError, KeyError) as exc:
                self._log("error", where="controls", file=path.name, error=repr(exc))
            finally:
                path.unlink(missing_ok=True)

    async def listen(self, max_wait_s: float) -> ListenResult:
        """Wait for a completed turn or a control. The timeout counts from the moment the bot
        has finished speaking, so `max_wait_s` means seconds of silence after our own turn."""
        started = self.clock()
        deadline = max(started, self.speaking_until) + max_wait_s * self.scale
        while True:
            self._ingest_controls()
            flushed = self._turntaker.flush_if_silent(self.clock())
            if flushed is not None:
                self._turns.append(flushed)
            if self._turns or self._controls:
                turns = list(self._turns)
                controls = list(self._controls)
                self._turns.clear()
                self._controls.clear()
                return ListenResult(turns=turns, controls=controls, elapsed_s=self.clock() - started)
            if self._ended.is_set():
                return ListenResult(ended=True, elapsed_s=self.clock() - started)
            if self.clock() >= deadline:
                return ListenResult(silence=True, elapsed_s=self.clock() - started)
            await asyncio.sleep(self.tick_s * self.scale)

    # -- consent --------------------------------------------------------------------------
    @staticmethod
    def assess_consent(text: str) -> Optional[bool]:
        """True = consent, False = declined, None = unclear."""
        negative = bool(NEGATIVE.search(text))
        positive = bool(AFFIRMATIVE.search(text))
        if negative and not positive:
            return False
        if positive and not negative:
            return True
        if positive and negative:
            # "no problem, go ahead" style phrases: treat trailing affirmative as consent
            return True if re.search(r"(go ahead|that's fine|no problem)", text, re.I) else None
        return None

    def record_consent(self, turn: Turn, granted: bool) -> None:
        self.report.consent.ai_participant = granted
        self.report.consent.recording = granted
        self.report.consent.declined = not granted
        self.report.consent.given_by = turn.speaker.name or turn.speaker.id
        self.report.consent.given_at = turn.completed_at
        self.report.consent.text = turn.text
        self._log("consent", granted=granted, by=self.report.consent.given_by, text=turn.text)
        if granted:
            self._set_state(BotState.consented, "consent confirmed")

    # -- leaving --------------------------------------------------------------------------
    async def leave(self, closing_text: Optional[str]) -> None:
        self._set_state(BotState.wrapping_up)
        try:
            if closing_text and self.state not in _TERMINAL:
                await self.say(closing_text)
                await self.wait_until_quiet()
        except Exception as exc:
            self.report.errors.append(f"closing: {exc!r}")
        try:
            await self.bot.leave()
            if self.report.admitted_at is None and getattr(self.bot, "bot_id", "n/a") is None:
                self._ended.set()  # the provider never created a bot (for example create_bot failed): nothing to wait for
            await asyncio.wait_for(self._ended.wait(), timeout=15 * self.scale)
        except asyncio.TimeoutError:
            self.report.errors.append("provider did not confirm the bot left within 15 s")
        except Exception as exc:
            self.report.errors.append(f"leave: {exc!r}")
        if self.state not in _TERMINAL:
            self._set_state(BotState.left)
        if self._pump:
            self._pump.cancel()
        await self.bot.close()
        self.report.ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # -- reporting ------------------------------------------------------------------------
    def write_report(self) -> Path:
        summary = self.report.summary()
        payload = self.report.model_dump(mode="json")
        payload["turn_rows"] = [t.as_row() for t in self.report.turns]
        payload["summary"] = summary
        (self.run_dir / "report.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        lines = [
            f"# Spike report — {self.meeting_id}",
            "",
            f"Outcome: **{summary['outcome']}** · platform {summary['platform']} · bot {summary['provider']} · TTS {summary['tts_provider']}",
            f"Admission: {summary['admission_s']} s · consent: {'given' if self.report.consent.ai_participant else ('declined' if self.report.consent.declined else 'not recorded')}",
            "",
            "| # | turn (human) | reply | detection ms | transcript lag ms | synth ms | playback start ms | pipeline ms |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for i, row in enumerate(payload["turn_rows"], 1):
            lines.append(
                f"| {i} | {row['turn_text'][:60]} | {row['reply_text'][:60]} | {row['turn_detection_ms']} | {row['transcript_lag_ms']} | {row['synth_ms']} | {row['playback_start_ms']} | {row['pipeline_ms']} |"
            )
        lines += [
            "",
            f"Pipeline latency median {summary['pipeline_ms_median']} ms, p95 {summary['pipeline_ms_p95']} ms; synthesis median {summary['synth_ms_median']} ms; playback start median {summary['playback_start_ms_median']} ms.",
            f"Supervisor controls received: {summary['controls_received']}. Errors: {summary['errors'] or 'none'}.",
        ]
        (self.run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return self.run_dir / "report.md"
