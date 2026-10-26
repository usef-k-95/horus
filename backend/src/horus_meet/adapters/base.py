"""Adapter protocols. A bot adapter joins and leaves the meeting, delivers status and
transcript events, plays audio and posts chat messages. A TTS adapter turns text into audio."""

from __future__ import annotations

from typing import AsyncIterator, Optional, Protocol, Union, runtime_checkable

from ..models import AudioClip, BotStatusEvent, SpeechEvent, Utterance

BotEvent = Union[BotStatusEvent, Utterance, SpeechEvent]


@runtime_checkable
class BotAdapter(Protocol):
    name: str

    async def join(self, meeting_url: str, display_name: str) -> str:
        """Request the bot into the meeting. Returns a provider bot id."""

    def events(self) -> AsyncIterator[BotEvent]:
        """Merged stream of status changes and transcript utterances, until the bot leaves."""

    async def play_audio(self, clip: AudioClip) -> Optional[float]:
        """Play a clip into the meeting. Returns seconds until playback started, when observable."""

    async def stop_audio(self) -> None:
        """Best-effort interruption of the clip being played (barge-in)."""

    async def send_chat(self, text: str) -> None: ...

    async def leave(self) -> None: ...

    async def close(self) -> None: ...


@runtime_checkable
class TTSAdapter(Protocol):
    name: str

    async def synthesize(self, text: str) -> AudioClip: ...
