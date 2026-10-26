"""Mock adapters: a scripted participant and a fake TTS, so the whole pipeline runs and is
measured without any provider. Timings are scaled by `time_scale` so tests run fast."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import AsyncIterator, Optional

from ..models import AudioClip, BotState, BotStatusEvent, Speaker, SpeechEvent, Utterance
from .base import BotEvent


@dataclass
class MockParticipant:
    speaker: Speaker
    lines: list[str]


class MockBotAdapter:
    """Simulates the meeting-bot provider and one participant.

    Timing model: join → `joining` after 0.2 s, `waiting_room` after 0.6 s, `joined` after
    `admit_after_s` (None means never admitted). After each bot clip finishes playing, the
    participant speaks the next scripted line after `think_s`, delivered as cumulative partial
    utterances every `partial_interval_s`, then a final utterance after `finalisation_delay_s`
    (standing in for speech-to-text finalisation latency). Playback begins `playback_start_s`
    after `play_audio` is called and lasts `clip.duration_s`.
    """

    name = "mock"

    def __init__(
        self,
        participant: MockParticipant,
        *,
        admit_after_s: Optional[float] = 1.2,
        think_s: float = 0.8,
        words_per_s: float = 2.5,
        partial_interval_s: float = 0.4,
        finalisation_delay_s: float = 0.35,
        playback_start_s: float = 0.25,
        time_scale: float = 1.0,
        participant_speaks_first: bool = False,
        emit_speech_events: bool = True,
    ) -> None:
        self.participant = participant
        self.admit_after_s = admit_after_s
        self.think_s = think_s
        self.words_per_s = words_per_s
        self.partial_interval_s = partial_interval_s
        self.finalisation_delay_s = finalisation_delay_s
        self.playback_start_s = playback_start_s
        self.scale = time_scale
        self.participant_speaks_first = participant_speaks_first
        self.emit_speech_events = emit_speech_events
        self.stopped_clips = 0
        self._queue: asyncio.Queue[Optional[BotEvent]] = asyncio.Queue()
        self._tasks: set[asyncio.Task] = set()
        self._t0 = time.monotonic()
        self._line_index = 0
        self._play_generation = 0
        self.played: list[AudioClip] = []
        self.chats: list[str] = []
        self.left = False
        self.bot_id: Optional[str] = None

    # -- helpers -----------------------------------------------------------------------------
    def _now(self) -> float:
        return time.monotonic() - self._t0

    async def _sleep(self, seconds: float) -> None:
        await asyncio.sleep(max(0.0, seconds) * self.scale)

    def _spawn(self, coro) -> None:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _emit_status(self, state: BotState, detail: Optional[str] = None) -> None:
        await self._queue.put(BotStatusEvent(state=state, detail=detail))

    # -- BotAdapter --------------------------------------------------------------------------
    async def join(self, meeting_url: str, display_name: str) -> str:
        self.bot_id = "mock-bot-1"
        self._spawn(self._run_join())
        return self.bot_id

    async def _run_join(self) -> None:
        await self._sleep(0.2)
        await self._emit_status(BotState.joining, "mock: joining call")
        await self._sleep(0.4)
        await self._emit_status(BotState.waiting_room, "mock: in waiting room")
        if self.admit_after_s is None:
            return
        await self._sleep(max(0.0, self.admit_after_s - 0.6))
        await self._emit_status(BotState.joined, "mock: admitted, in call")
        if self.participant_speaks_first:
            self._spawn(self._speak_next_line())

    async def events(self) -> AsyncIterator[BotEvent]:
        while True:
            item = await self._queue.get()
            if item is None:
                return
            yield item

    async def play_audio(self, clip: AudioClip) -> Optional[float]:
        self._play_generation += 1
        generation = self._play_generation
        await self._sleep(self.playback_start_s)
        self.played.append(clip)
        duration = clip.duration_s if clip.duration_s is not None else 1.0
        self._spawn(self._after_playback(generation, duration))
        return self.playback_start_s

    async def _after_playback(self, generation: int, duration: float) -> None:
        await self._sleep(duration)
        if generation != self._play_generation or self.left:
            return  # another clip started meanwhile; the participant waits for the last one
        await self._sleep(self.think_s)
        if generation != self._play_generation or self.left:
            return
        await self._speak_next_line()

    async def _speak_next_line(self) -> None:
        if self._line_index >= len(self.participant.lines):
            return
        line = self.participant.lines[self._line_index]
        self._line_index += 1
        words = line.split()
        start = self._now()
        if self.emit_speech_events:
            await self._queue.put(SpeechEvent(speaker=self.participant.speaker, speaking=True))
        spoken: list[str] = []
        chunk = max(1, round(self.partial_interval_s * self.words_per_s))
        for i in range(0, len(words), chunk):
            spoken.extend(words[i : i + chunk])
            await self._sleep(self.partial_interval_s)
            if self.left:
                return
            await self._queue.put(
                Utterance(
                    speaker=self.participant.speaker,
                    text=" ".join(spoken),
                    start=start,
                    end=self._now(),
                    is_final=False,
                    confidence=0.8,
                )
            )
        if self.emit_speech_events:
            await self._queue.put(SpeechEvent(speaker=self.participant.speaker, speaking=False))
        await self._sleep(self.finalisation_delay_s)
        if self.left:
            return
        await self._queue.put(
            Utterance(
                speaker=self.participant.speaker,
                text=line,
                start=start,
                end=self._now(),
                is_final=True,
                confidence=0.95,
            )
        )

    async def stop_audio(self) -> None:
        self.stopped_clips += 1

    async def send_chat(self, text: str) -> None:
        self.chats.append(text)

    async def leave(self) -> None:
        self.left = True
        await self._emit_status(BotState.left, "mock: bot left the call")
        await self._queue.put(None)

    async def close(self) -> None:
        for task in list(self._tasks):
            task.cancel()
        self._tasks.clear()


class MockTTS:
    name = "mock-tts"

    def __init__(self, *, synth_s: float = 0.45, words_per_s: float = 2.6, time_scale: float = 1.0) -> None:
        self.synth_s = synth_s
        self.words_per_s = words_per_s
        self.scale = time_scale

    async def synthesize(self, text: str) -> AudioClip:
        t0 = time.monotonic()
        await asyncio.sleep(self.synth_s * self.scale)
        words = max(1, len(text.split()))
        return AudioClip(
            data=b"\x00" * (len(text) * 10),
            mime="audio/mpeg",
            duration_s=words / self.words_per_s,
            synth_ms=(time.monotonic() - t0) * 1000,
            text=text,
        )
