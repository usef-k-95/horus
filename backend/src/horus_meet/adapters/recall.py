"""Recall.ai meeting-bot adapter.

Checked against docs.recall.ai on 25 October 2026 (see docs/SPIKE-0-live-meetings.md §6):
- auth header is the bare API key; all resources are region-local;
- real-time events are pushed by Recall to a public websocket URL we expose (`?token=` auth,
  trailing slash before the query string); bot status changes are NOT delivered there, so the
  adapter polls the Bot resource;
- the bot speaks through Output Audio (short MP3 snippets, base64 at most 1,835,008 chars),
  which requires `automatic_audio_output` to be configured at creation; Output Media (a
  webpage streaming audio) is the lower-latency alternative kept for a later iteration;
- chat messages on Google Meet are capped at 500 characters and go to everyone.
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import secrets
import time
from typing import AsyncIterator, Optional
from urllib.parse import parse_qs, urlparse

import httpx
import websockets

from ..models import AudioClip, BotState, BotStatusEvent, Speaker, SpeechEvent, Utterance
from .base import BotEvent

log = logging.getLogger(__name__)

REGION_HOSTS = {
    "us-east-1": "https://us-east-1.recall.ai",
    "us-west-2": "https://us-west-2.recall.ai",
    "eu-central-1": "https://eu-central-1.recall.ai",
    "ap-northeast-1": "https://ap-northeast-1.recall.ai",
}
PATH_CREATE_BOT = "/api/v1/bot/"
PATH_BOT = "/api/v1/bot/{bot_id}/"
PATH_OUTPUT_AUDIO = "/api/v1/bot/{bot_id}/output_audio/"
PATH_SEND_CHAT = "/api/v1/bot/{bot_id}/send_chat_message/"
PATH_LEAVE = "/api/v1/bot/{bot_id}/leave_call/"

EVENT_TRANSCRIPT_FINAL = "transcript.data"
EVENT_TRANSCRIPT_PARTIAL = "transcript.partial_data"
EVENT_SPEECH_ON = "participant_events.speech_on"
EVENT_SPEECH_OFF = "participant_events.speech_off"
REALTIME_EVENTS = [EVENT_TRANSCRIPT_FINAL, EVENT_TRANSCRIPT_PARTIAL, EVENT_SPEECH_ON, EVENT_SPEECH_OFF]

# Transcript provider presets. Third-party providers need their API key added in the Recall
# dashboard for the region; `recallai_streaming` needs nothing extra.
TRANSCRIPT_PROVIDERS = {
    "recall_low_latency": {"recallai_streaming": {"mode": "prioritize_low_latency", "language_code": "en"}},
    "deepgram_nova3": {
        "deepgram_streaming": {"model": "nova-3", "interim_results": True, "endpointing": 300, "utterance_end_ms": 1000, "smart_format": True}
    },
    "assemblyai": {"assembly_ai_v3_streaming": {}},
}

OUTPUT_AUDIO_B64_LIMIT = 1_835_008
MEET_CHAT_LIMIT = 500

# Bot.status_changes[].code → runtime state
STATUS_MAP = {
    "ready": BotState.requested,
    "joining_call": BotState.joining,
    "in_waiting_room": BotState.waiting_room,
    "in_call_not_recording": BotState.joined,
    "recording_permission_allowed": BotState.joined,
    "recording_permission_denied": BotState.joined,
    "in_call_recording": BotState.joined,
    "call_ended": BotState.left,
    "done": BotState.left,
    "analysis_done": BotState.left,
    "fatal": BotState.aborted,
}


class RecallError(RuntimeError):
    pass


class RecallBotAdapter:
    name = "recall"

    def __init__(
        self,
        api_key: str,
        region: str,
        public_ws_url: str,
        *,
        local_ws_port: int = 8765,
        transcript_preset: str = "recall_low_latency",
        separate_streams: bool = False,
        waiting_room_timeout_s: int = 300,
        placeholder_clip: Optional[AudioClip] = None,
        poll_interval_s: float = 2.0,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        if region not in REGION_HOSTS:
            raise RecallError(f"unknown Recall region {region!r}")
        if transcript_preset not in TRANSCRIPT_PROVIDERS:
            raise RecallError(f"unknown transcript preset {transcript_preset!r}")
        self.base = REGION_HOSTS[region]
        self.api_key = api_key
        self.public_ws_url = public_ws_url.rstrip("/") + "/"
        self.local_ws_port = local_ws_port
        self.transcript_preset = transcript_preset
        self.separate_streams = separate_streams
        self.waiting_room_timeout_s = waiting_room_timeout_s
        self.placeholder_clip = placeholder_clip
        self.poll_interval_s = poll_interval_s
        self._client = client or httpx.AsyncClient(timeout=30.0)
        self._queue: asyncio.Queue[Optional[BotEvent]] = asyncio.Queue()
        self._server = None
        self._poller: Optional[asyncio.Task] = None
        self._last_status: Optional[str] = None
        self._token = secrets.token_urlsafe(24)
        self._t0 = time.monotonic()
        self.bot_id: Optional[str] = None
        self.raw_events_path = None  # set by the session to archive raw provider messages
        self.last_bot_payload: Optional[dict] = None

    def _headers(self) -> dict:
        return {"Authorization": self.api_key, "Content-Type": "application/json"}

    # -- websocket receiver (Recall connects to us) --------------------------------------
    async def _start_ws_server(self) -> None:
        if self._server is not None:
            return
        self._server = await websockets.serve(self._ws_handler, "0.0.0.0", self.local_ws_port)
        log.info("real-time receiver on port %s; public %s", self.local_ws_port, self.public_ws_url)

    def _token_ok(self, websocket) -> bool:
        try:
            path = websocket.request.path  # websockets >= 13
        except AttributeError:  # older versions
            path = getattr(websocket, "path", "")
        token = parse_qs(urlparse(path).query).get("token", [None])[0]
        return token == self._token

    async def _ws_handler(self, websocket) -> None:
        if not self._token_ok(websocket):
            log.warning("rejected real-time connection with a bad or missing token")
            await websocket.close(code=4401, reason="bad token")
            return
        async for raw in websocket:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                log.warning("non-JSON message from provider: %r", raw[:200])
                continue
            self._archive(message)
            event = message.get("event")
            if event in (EVENT_TRANSCRIPT_FINAL, EVENT_TRANSCRIPT_PARTIAL):
                utterance = self._parse_transcript(message, is_final=(event == EVENT_TRANSCRIPT_FINAL))
                if utterance is not None:
                    await self._queue.put(utterance)
            elif event in (EVENT_SPEECH_ON, EVENT_SPEECH_OFF):
                speech = self._parse_speech(message, speaking=(event == EVENT_SPEECH_ON))
                if speech is not None:
                    await self._queue.put(speech)

    def _archive(self, message: dict) -> None:
        if self.raw_events_path is None:
            return
        with open(self.raw_events_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"t": round(time.monotonic() - self._t0, 3), "message": message}) + "\n")

    @staticmethod
    def _speaker(participant: Optional[dict]) -> Speaker:
        participant = participant or {}
        return Speaker(id=str(participant.get("id", "unknown")), name=participant.get("name"), is_bot=False)

    @classmethod
    def _parse_transcript(cls, message: dict, *, is_final: bool) -> Optional[Utterance]:
        try:
            data = message["data"]["data"]
            words = data.get("words") or []
            if not words:
                return None
            text = " ".join((w.get("text") or "") for w in words).strip()
            if not text:
                return None
            first = words[0].get("start_timestamp") or {}
            last = words[-1].get("end_timestamp") or {}
            start = float(first.get("relative") or 0.0)
            end_value = last.get("relative")
            end = float(end_value) if end_value is not None else start
            return Utterance(speaker=cls._speaker(data.get("participant")), text=text, start=start, end=end, is_final=is_final)
        except (KeyError, TypeError, ValueError) as exc:
            log.warning("could not parse transcript event: %s", exc)
            return None

    @classmethod
    def _parse_speech(cls, message: dict, *, speaking: bool) -> Optional[SpeechEvent]:
        try:
            data = message["data"]["data"]
            return SpeechEvent(speaker=cls._speaker(data.get("participant")), speaking=speaking)
        except (KeyError, TypeError) as exc:
            log.warning("could not parse speech event: %s", exc)
            return None

    # -- status polling (status changes are not available on real-time endpoints) -----------
    async def _poll_status(self) -> None:
        assert self.bot_id
        url = self.base + PATH_BOT.format(bot_id=self.bot_id)
        while True:
            try:
                response = await self._client.get(url, headers=self._headers())
                response.raise_for_status()
                payload = response.json()
                self.last_bot_payload = payload
                changes = payload.get("status_changes") or []
                if changes:
                    latest = changes[-1]
                    code = latest.get("code")
                    if code != self._last_status:
                        self._last_status = code
                        state = STATUS_MAP.get(code)
                        detail = str(code) + (f" ({latest.get('sub_code')})" if latest.get("sub_code") else "")
                        if state is not None:
                            await self._queue.put(BotStatusEvent(state=state, detail=detail))
                        if state in (BotState.left, BotState.aborted):
                            await self._queue.put(None)
                            return
            except (httpx.HTTPError, ValueError) as exc:
                log.warning("status poll failed: %s", exc)
            await asyncio.sleep(self.poll_interval_s)

    # -- BotAdapter ------------------------------------------------------------------------
    def _create_body(self, meeting_url: str, display_name: str) -> dict:
        transcript: dict = {"provider": TRANSCRIPT_PROVIDERS[self.transcript_preset]}
        if self.separate_streams:
            transcript["diarization"] = {"use_separate_streams_when_available": True}
        body: dict = {
            "meeting_url": meeting_url,
            "bot_name": display_name,
            "recording_config": {
                "transcript": transcript,
                "realtime_endpoints": [
                    {"type": "websocket", "url": f"{self.public_ws_url}?token={self._token}", "events": REALTIME_EVENTS}
                ],
            },
            "automatic_leave": {"waiting_room_timeout": self.waiting_room_timeout_s},
        }
        if self.placeholder_clip is not None:
            b64 = base64.b64encode(self.placeholder_clip.data).decode("ascii")
            body["automatic_audio_output"] = {"in_call_recording": {"data": {"kind": "mp3", "b64_data": b64}}}
        else:
            log.warning("no placeholder clip: Output Audio requires automatic_audio_output and may be refused")
        return body

    async def join(self, meeting_url: str, display_name: str) -> str:
        await self._start_ws_server()
        body = self._create_body(meeting_url, display_name)
        response = await self._client.post(self.base + PATH_CREATE_BOT, headers=self._headers(), json=body)
        if response.status_code >= 400:
            raise RecallError(f"create bot failed {response.status_code}: {response.text[:400]}")
        self.bot_id = response.json()["id"]
        self._poller = asyncio.create_task(self._poll_status())
        return self.bot_id

    async def events(self) -> AsyncIterator[BotEvent]:
        while True:
            item = await self._queue.get()
            if item is None:
                return
            yield item

    async def play_audio(self, clip: AudioClip) -> Optional[float]:
        assert self.bot_id
        if clip.mime != "audio/mpeg":
            raise RecallError("Output Audio accepts MP3 only")
        b64 = base64.b64encode(clip.data).decode("ascii")
        if len(b64) > OUTPUT_AUDIO_B64_LIMIT:
            raise RecallError(f"clip too large for Output Audio ({len(b64)} > {OUTPUT_AUDIO_B64_LIMIT} base64 chars)")
        response = await self._client.post(
            self.base + PATH_OUTPUT_AUDIO.format(bot_id=self.bot_id), headers=self._headers(), json={"kind": "mp3", "b64_data": b64}
        )
        if response.status_code >= 400:
            raise RecallError(f"output audio failed {response.status_code}: {response.text[:400]}")
        return None  # playback start is not observable through the API; measured as request completion

    async def stop_audio(self) -> None:
        if not self.bot_id:
            return
        response = await self._client.delete(self.base + PATH_OUTPUT_AUDIO.format(bot_id=self.bot_id), headers=self._headers())
        if response.status_code >= 400:
            log.warning("stop audio failed %s: %s", response.status_code, response.text[:200])

    async def send_chat(self, text: str) -> None:
        assert self.bot_id
        if len(text) > MEET_CHAT_LIMIT:
            log.warning("chat message truncated to %s characters (Google Meet limit)", MEET_CHAT_LIMIT)
            text = text[: MEET_CHAT_LIMIT - 1] + "…"
        response = await self._client.post(
            self.base + PATH_SEND_CHAT.format(bot_id=self.bot_id), headers=self._headers(), json={"to": "everyone", "message": text}
        )
        if response.status_code >= 400:
            log.warning("send chat failed %s: %s", response.status_code, response.text[:200])

    async def leave(self) -> None:
        if not self.bot_id:
            return
        response = await self._client.post(self.base + PATH_LEAVE.format(bot_id=self.bot_id), headers=self._headers())
        if response.status_code >= 400:
            log.warning("leave call failed %s: %s", response.status_code, response.text[:200])

    async def close(self) -> None:
        if self._poller:
            self._poller.cancel()
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        await self._client.aclose()
