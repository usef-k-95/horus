"""Typed records shared by adapters, the session state machine and the spike runner."""

from __future__ import annotations

import statistics
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BotState(str, Enum):
    requested = "requested"
    joining = "joining"
    waiting_room = "waiting_room"
    joined = "joined"
    disclosed = "disclosed"
    consented = "consented"
    interviewing = "interviewing"
    wrapping_up = "wrapping_up"
    left = "left"
    aborted = "aborted"


class Speaker(BaseModel):
    id: str
    name: Optional[str] = None
    is_bot: bool = False


class Utterance(BaseModel):
    """One transcript segment. `start`/`end` are meeting-relative seconds from the provider;
    `received_at` is session-clock seconds when the event reached us."""

    speaker: Speaker
    text: str
    start: float
    end: float
    is_final: bool = True
    confidence: Optional[float] = None
    received_at: float = 0.0


class SpeechEvent(BaseModel):
    """Voice activity from the provider: a participant started or stopped speaking."""

    speaker: Speaker
    speaking: bool
    at: float = 0.0


class Turn(BaseModel):
    """A completed speaker turn. `provisional` is true when it was closed on voice activity
    with partial text before the final transcript arrived."""

    speaker: Speaker
    text: str
    start: float
    end: float
    last_final_received_at: float
    speech_ended_at: Optional[float] = None
    completed_at: float
    utterances: int
    provisional: bool = False


class ControlKind(str, Enum):
    whisper = "whisper"
    pause = "pause"
    resume = "resume"
    takeover = "takeover"
    leave = "leave"


class ControlEvent(BaseModel):
    kind: ControlKind
    text: Optional[str] = None
    at: float = 0.0
    by: str = "supervisor"


class BotStatusEvent(BaseModel):
    state: BotState
    detail: Optional[str] = None
    at: float = 0.0


class AudioClip(BaseModel):
    data: bytes
    mime: str                      # audio/mpeg for MP3, audio/pcm for raw 16-bit little-endian mono
    sample_rate: Optional[int] = None
    duration_s: Optional[float] = None
    synth_ms: float = 0.0
    text: str = ""


class LatencySample(BaseModel):
    """Timing of one reply, all in session-clock seconds unless suffixed `_ms`."""

    turn_text: str
    reply_text: str
    last_final_received_at: float
    speech_ended_at: Optional[float] = None
    turn_completed_at: float
    synth_started_at: float
    synth_done_at: float
    playback_requested_at: float
    playback_started_at: Optional[float] = None

    @property
    def speech_end(self) -> float:
        """Best estimate of when the human stopped talking: voice activity if the provider
        reports it, otherwise the arrival of the last final transcript segment."""
        return self.speech_ended_at if self.speech_ended_at is not None else self.last_final_received_at

    @property
    def turn_detection_ms(self) -> float:
        return (self.turn_completed_at - self.speech_end) * 1000

    @property
    def transcript_lag_ms(self) -> Optional[float]:
        """How long the final transcript trailed the end of speech, when both are known."""
        if self.speech_ended_at is None:
            return None
        return (self.last_final_received_at - self.speech_ended_at) * 1000

    @property
    def synth_ms(self) -> float:
        return (self.synth_done_at - self.synth_started_at) * 1000

    @property
    def playback_start_ms(self) -> float:
        started = self.playback_started_at or self.playback_requested_at
        return (started - self.playback_requested_at) * 1000

    @property
    def pipeline_ms(self) -> float:
        """End of the human's speech to first bot audio, excluding the model."""
        started = self.playback_started_at or self.playback_requested_at
        return (started - self.speech_end) * 1000

    def as_row(self) -> dict:
        return {
            "turn_text": self.turn_text,
            "reply_text": self.reply_text,
            "turn_detection_ms": round(self.turn_detection_ms, 1),
            "transcript_lag_ms": None if self.transcript_lag_ms is None else round(self.transcript_lag_ms, 1),
            "synth_ms": round(self.synth_ms, 1),
            "playback_start_ms": round(self.playback_start_ms, 1),
            "pipeline_ms": round(self.pipeline_ms, 1),
        }


class ConsentRecord(BaseModel):
    ai_participant: bool = False
    recording: bool = False
    given_by: Optional[str] = None
    given_at: Optional[float] = None
    text: Optional[str] = None
    declined: bool = False


class SpikeReport(BaseModel):
    meeting_id: str
    platform: str
    provider: str
    tts_provider: str
    bot_name: str
    started_at: str
    ended_at: Optional[str] = None
    join_requested_at: Optional[float] = None
    admitted_at: Optional[float] = None
    disclosure_at: Optional[float] = None
    consent: ConsentRecord = Field(default_factory=ConsentRecord)
    turns: list[LatencySample] = Field(default_factory=list)
    controls_received: list[ControlEvent] = Field(default_factory=list)
    states: list[BotStatusEvent] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    outcome: str = "incomplete"

    @property
    def admission_s(self) -> Optional[float]:
        if self.join_requested_at is None or self.admitted_at is None:
            return None
        return self.admitted_at - self.join_requested_at

    def summary(self) -> dict:
        pipeline = [t.pipeline_ms for t in self.turns]
        synth = [t.synth_ms for t in self.turns]
        start = [t.playback_start_ms for t in self.turns]

        def pct(values: list[float], q: float) -> Optional[float]:
            if not values:
                return None
            ordered = sorted(values)
            idx = min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))
            return round(ordered[idx], 1)

        return {
            "outcome": self.outcome,
            "platform": self.platform,
            "provider": self.provider,
            "tts_provider": self.tts_provider,
            "admission_s": None if self.admission_s is None else round(self.admission_s, 2),
            "consent": self.consent.model_dump(),
            "turns": len(self.turns),
            "pipeline_ms_median": round(statistics.median(pipeline), 1) if pipeline else None,
            "pipeline_ms_p95": pct(pipeline, 0.95),
            "synth_ms_median": round(statistics.median(synth), 1) if synth else None,
            "playback_start_ms_median": round(statistics.median(start), 1) if start else None,
            "controls_received": len(self.controls_received),
            "errors": self.errors,
        }
