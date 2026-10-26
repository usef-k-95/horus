"""Turn-taking: assemble partial and final utterances into completed speaker turns."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .models import Speaker, SpeechEvent, Turn, Utterance


@dataclass
class _OpenTurn:
    speaker: Speaker
    finals: list[str] = field(default_factory=list)
    partial: str = ""
    start: float = 0.0
    end: float = 0.0
    last_final_received_at: float = 0.0
    last_activity_at: float = 0.0
    speech_ended_at: Optional[float] = None
    utterances: int = 0

    def text(self, include_partial: bool = False) -> str:
        parts = [part for part in self.finals if part]
        if include_partial and self.partial:
            parts.append(self.partial)
        return " ".join(parts).strip()


class TurnTaker:
    """A turn is complete when its speaker has been silent for `silence_s` after a final
    utterance, when another speaker starts, or, if the provider reports voice activity,
    `silence_s` after the speaker stopped talking even if only partial text has arrived
    (a provisional turn, which lets a reply start before the final transcript lands)."""

    def __init__(self, silence_s: float = 0.8, reconcile_window_s: float = 2.5) -> None:
        self.silence_s = silence_s
        self.reconcile_window_s = reconcile_window_s
        self._open: Optional[_OpenTurn] = None
        self._last_closed: Optional[tuple[str, float, bool]] = None  # speaker id, closed at, provisional
        self.reconciled_finals = 0

    def speech(self, event: SpeechEvent) -> None:
        current = self._open
        if event.speaking:
            if current is None:
                self._open = _OpenTurn(speaker=event.speaker, start=event.at, last_activity_at=event.at)
            elif current.speaker.id == event.speaker.id:
                current.speech_ended_at = None
                current.last_activity_at = event.at
            return
        if current is not None and current.speaker.id == event.speaker.id:
            current.speech_ended_at = event.at

    @property
    def speaking(self) -> Optional[Speaker]:
        return self._open.speaker if self._open else None

    def feed(self, utterance: Utterance) -> list[Turn]:
        completed: list[Turn] = []
        now = utterance.received_at
        current = self._open
        if current is None and utterance.is_final and self._last_closed is not None:
            speaker_id, closed_at, provisional = self._last_closed
            if provisional and speaker_id == utterance.speaker.id and now - closed_at <= self.reconcile_window_s:
                # the final transcript of a turn already closed on voice activity: absorb it
                self.reconciled_finals += 1
                return completed
        if current is not None and current.speaker.id != utterance.speaker.id:
            if current.finals:
                completed.append(self._close(current, now))
            else:
                self._open = None
            current = None
        if current is None:
            current = _OpenTurn(speaker=utterance.speaker, start=utterance.start, last_activity_at=now)
            self._open = current
        current.last_activity_at = now
        current.end = max(current.end, utterance.end)
        if utterance.is_final and current.speech_ended_at is not None and current.speech_ended_at < now:
            pass  # final text arriving after speech ended does not reopen the turn
        if utterance.is_final:
            current.finals.append(utterance.text)
            current.partial = ""
            current.last_final_received_at = now
            current.utterances += 1
        else:
            current.partial = utterance.text
        return completed

    def flush_if_silent(self, now: float) -> Optional[Turn]:
        current = self._open
        if current is None:
            return None
        if current.speech_ended_at is not None and now - current.speech_ended_at >= self.silence_s:
            if current.finals or current.partial:
                return self._close(current, now, provisional=not current.finals or bool(current.partial))
            return None
        if not current.finals:
            return None
        if current.partial:  # the speaker is still mid-sentence
            return None
        if now - current.last_activity_at >= self.silence_s:
            return self._close(current, now)
        return None

    def force_close(self, now: float) -> Optional[Turn]:
        current = self._open
        if current is None or not current.finals:
            self._open = None
            return None
        return self._close(current, now)

    def _close(self, current: _OpenTurn, now: float, provisional: bool = False) -> Turn:
        self._open = None
        self._last_closed = (current.speaker.id, now, provisional)
        return Turn(
            speaker=current.speaker,
            text=current.text(include_partial=provisional),
            start=current.start,
            end=current.end,
            last_final_received_at=current.last_final_received_at or now,
            speech_ended_at=current.speech_ended_at,
            completed_at=now,
            utterances=current.utterances,
            provisional=provisional,
        )
