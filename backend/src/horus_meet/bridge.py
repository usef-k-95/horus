"""Writes live-meeting facts back into the engagement state (collection `meetings`) as actor `meet`.
Every write is best-effort: a state problem must never break a live conversation, except the
pre-join check, which is the policy gate (rules 21 and 22)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


class StateBridge:
    def __init__(self, workspace: Path, meeting_id: str) -> None:
        from horus_state.service import Service  # local import keeps horus_meet usable without state

        self.meeting_id = meeting_id
        self.svc = Service(workspace, actor="meet")
        self.enabled = self.svc.store.initialised and self.svc.store.exists("meetings", meeting_id)

    def meeting(self) -> dict:
        return self.svc.get("meetings", self.meeting_id)

    def _update(self, patch: dict, reason: Optional[str] = None) -> Optional[dict]:
        if not self.enabled:
            return None
        try:
            return self.svc.update("meetings", self.meeting_id, patch, reason=reason, actor="meet")
        except Exception as exc:
            log.warning("state write failed for %s: %s", self.meeting_id, exc)
            return None

    # -- the gate: raises when the plan is not approved or the disclosure is missing ---------
    def check_can_join(self, conduct_mode: str = "interviewer") -> None:
        if not self.enabled:
            return
        self.svc.update("meetings", self.meeting_id, {"status": "joining", "conduct_mode": conduct_mode}, reason="bot dispatch", actor="meet")

    def on_bot_created(self, provider: str, bot_id: str, display_name: str) -> None:
        self._update({"bot": {"provider": provider, "bot_id": bot_id, "display_name": display_name, "requested_at": _now()}})

    def on_admitted(self) -> None:
        self._update({"bot": {"joined_at": _now(), "admitted_at": _now()}})

    def on_disclosed(self, text: str, script_id: Optional[str] = None) -> None:
        self._update({"disclosure": {"script_id": script_id, "spoken_at": _now(), "chat_posted_at": _now(), "text": text}})

    def on_consent(self, granted: bool, given_by: Optional[str], attribution_rule: str, recording: bool, text: Optional[str]) -> None:
        patch = {"consent": {"ai_participant": granted, "recording": granted and recording, "transcript": granted, "attribution_rule": attribution_rule, "given_by": given_by, "given_at": _now() if granted else None}}
        if not granted:
            patch["consent"]["objections"] = [{"at": _now(), "text": text or "declined", "response": "stopped and offered alternatives"}]
        self._update(patch)
        if granted:
            self._update({"status": "in_progress"})

    def on_mark(self, label: str, at: float, note: Optional[str]) -> None:
        if not self.enabled:
            return
        try:
            live = self.meeting().get("live") or {}
            marks = list(live.get("marks") or []) + [{"label": label, "at": at, "note": note}]
            self._update({"live": {**live, "marks": marks}})
        except Exception as exc:
            log.warning("mark write failed: %s", exc)

    def on_left(self, transcript_path: Optional[str], turns: int, coverage: dict, latency: dict, exit_reason: Optional[str], provider: str, recording_path: Optional[str] = None) -> None:
        patch = {
            "bot": {"left_at": _now(), "exit_reason": exit_reason},
            "transcript": {"path": transcript_path, "diarised": True, "provider": provider, "turns": turns, "off_record_removed": False},
            "live": {"coverage": coverage, "latency": latency},
            "held_at": _now(),
        }
        if recording_path:
            patch["recording"] = {"path": recording_path}
        self._update(patch, reason="bot left the meeting")

    def on_intervention(self, kind: str, text: Optional[str], by: str) -> None:
        if not self.enabled:
            return
        try:
            self.svc.record_intervention(self.meeting_id, kind, text, by=by)
        except Exception as exc:
            log.warning("intervention write failed: %s", exc)
