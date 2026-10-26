"""MeetStream meeting-bot adapter (api.meetstream.ai, checked against the vendor's OpenAPI contract
and the installed `meetstream-ai-meeting-bot-api` plugin documentation on 26 October 2026).

How the pieces connect:
- REST (`Authorization: Token <key>`): create the bot, poll status, send chat, remove the bot, fetch
  the post-call transcript and chats.
- MeetStream pushes to us: live transcript sentences as webhook POSTs, bot status changes as webhook
  POSTs to `callback_url`, and a control websocket (`socket_connection_url`) that MeetStream opens to
  our server. Speaking is done over that websocket with `sendaudio` chunks of PCM16 little-endian
  mono at 48 kHz; `interrupt` clears the queue for barge-in.
- One `Ingress` (Starlette app on one local port behind a public tunnel) serves all three inbound
  channels and routes by bot id; a secret token in the path keeps strangers out.
"""

from __future__ import annotations

import asyncio
import json
import logging
import secrets
import time
import uuid
from typing import AsyncIterator, Optional

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

from ..audio import TARGET_RATE, b64, chunk_pcm16, duration_seconds
from ..models import AudioClip, BotState, BotStatusEvent, Speaker, SpeechEvent, Utterance
from .base import BotEvent

log = logging.getLogger(__name__)

API_BASE = "https://api.meetstream.ai/api/v1"
CHUNK_SECONDS = 0.8
SEND_INTERVAL = 0.75  # pace sendaudio slightly faster than real time so the queue never starves

STATUS_MAP = {  # GET /bots/{id}/status → runtime state (compare lower-case)
    "scheduled": BotState.requested,
    "joining": BotState.joining,
    "inwaitingroom": BotState.waiting_room,
    "inmeeting": BotState.joined,
    "recording": BotState.joined,
    "recordingpermissionallowed": BotState.joined,
    "recordingpermissiondenied": BotState.joined,
    "leaving": BotState.wrapping_up,
    "stopped": BotState.left,
    "kicked": BotState.left,
    "cancelled": BotState.left,
    "mediaprocessing": BotState.left,
    "done": BotState.left,
    "mediaexpired": BotState.left,
    "notallowed": BotState.aborted,
    "denied": BotState.aborted,
    "failed": BotState.aborted,
    "error": BotState.aborted,
}
BOT_EVENT_MAP = {  # callback_url webhook `bot_event`
    "bot.scheduled": BotState.requested,
    "bot.joining": BotState.joining,
    "bot.in_waiting_room": BotState.waiting_room,
    "bot.inmeeting": BotState.joined,
    "bot.recording_permission_allowed": BotState.joined,
    "bot.recording_permission_denied": BotState.joined,
    "bot.recording": BotState.joined,
    "bot.leaving": BotState.wrapping_up,
    "bot.stopped": BotState.left,
    "bot.kicked": BotState.left,
    "bot.denied": BotState.aborted,
    "bot.notallowed": BotState.aborted,
    "bot.failed": BotState.aborted,
}
def _seconds(value, default: float = 0.0) -> float:
    """Seconds from a number, a numeric string or an ISO-8601 timestamp (MeetStream sends ISO strings)."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        pass
    try:
        from datetime import datetime
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return default


TRANSCRIPT_PRESETS = {
    "deepgram_sentence": {"deepgram_streaming": {"model": "nova-2", "transcription_mode": "sentence", "language": "en", "punctuate": True, "smart_format": True, "endpointing": 300, "utterance_end_ms": 1000}},
    # MeetStream's own live transcription: free on every account, no external key; chunks arrive in "raw" mode
    # with is_final/end_of_turn flags and the speaker's meeting name.
    "meetstream_native": {"meetstream_streaming": {}},
    "meetstream_sentence": {"meetstream_streaming": {}},
    "assemblyai_sentence": {"assemblyai_streaming": {"transcription_mode": "sentence"}},
    "meeting_captions": {"meeting_captions": {}},
}


class MeetStreamError(RuntimeError):
    pass


# =========================================================================================
# Ingress: the server MeetStream talks to
# =========================================================================================
class Ingress:
    """Starlette app serving `/ms/<token>/transcript`, `/ms/<token>/callback` and `/ms/<token>/control`.
    Adapters register themselves by bot id; events are routed to them."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765, token: Optional[str] = None) -> None:
        self.host = host
        self.port = port
        self.token = token or secrets.token_urlsafe(18)
        self._adapters: dict[str, "MeetStreamBotAdapter"] = {}
        self._pending: list["MeetStreamBotAdapter"] = []  # adapters that created a bot but have no id yet
        self._server = None
        self._task: Optional[asyncio.Task] = None
        self.app = Starlette(
            routes=[
                Route("/ms/{token}/transcript", self._transcript, methods=["POST"]),
                Route("/ms/{token}/callback", self._callback, methods=["POST"]),
                Route("/ms/{token}/health", self._health, methods=["GET"]),
                WebSocketRoute("/ms/{token}/control", self._control),
            ]
        )

    def paths(self, public_base: str) -> dict:
        base = public_base.rstrip("/")
        ws_base = base.replace("https://", "wss://").replace("http://", "ws://")
        return {
            "transcript": f"{base}/ms/{self.token}/transcript",
            "callback": f"{base}/ms/{self.token}/callback",
            "control": f"{ws_base}/ms/{self.token}/control",
        }

    def register(self, adapter: "MeetStreamBotAdapter") -> None:
        if adapter.bot_id:
            self._adapters[adapter.bot_id] = adapter
        else:
            self._pending.append(adapter)

    def unregister(self, adapter: "MeetStreamBotAdapter") -> None:
        if adapter.bot_id:
            self._adapters.pop(adapter.bot_id, None)
        if adapter in self._pending:
            self._pending.remove(adapter)

    def _route(self, bot_id: Optional[str]) -> Optional["MeetStreamBotAdapter"]:
        if bot_id and bot_id in self._adapters:
            return self._adapters[bot_id]
        if len(self._adapters) == 1:
            return next(iter(self._adapters.values()))
        if self._pending:
            adapter = self._pending.pop(0)
            if bot_id:
                adapter.bot_id = adapter.bot_id or bot_id
                self._adapters[bot_id] = adapter
            return adapter
        return None

    async def start(self) -> None:
        if self._task is not None:
            return
        import socket
        import uvicorn

        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            probe.bind((self.host, self.port))
        except OSError as exc:
            raise MeetStreamError(f"port {self.port} is already in use: another Horus meeting or live test is still running on this Mac. Finish it (say goodbye, or press Control+C in its Terminal tab) and try again.") from exc
        finally:
            probe.close()

        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="warning", lifespan="off")
        self._server = uvicorn.Server(config)
        self._task = asyncio.create_task(self._server.serve())
        for _ in range(50):
            if self._server.started:
                return
            await asyncio.sleep(0.05)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.should_exit = True
        if self._task is not None:
            try:
                await asyncio.wait_for(self._task, timeout=5)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                self._task.cancel()
        self._task = None
        self._server = None

    # -- handlers -------------------------------------------------------------------------
    def _check(self, request_token: str) -> bool:
        return secrets.compare_digest(request_token, self.token)

    async def _health(self, request: Request):
        return JSONResponse({"ok": self._check(request.path_params["token"]), "bots": list(self._adapters)})

    async def _transcript(self, request: Request):
        if not self._check(request.path_params["token"]):
            return JSONResponse({"error": "bad token"}, status_code=401)
        try:
            payload = await request.json()
        except Exception:
            return JSONResponse({"error": "bad json"}, status_code=400)
        adapter = self._route(payload.get("bot_id"))
        if adapter is None:
            return JSONResponse({"error": "unknown bot"}, status_code=404)
        await adapter.on_transcript(payload)
        return JSONResponse({"ok": True})

    async def _callback(self, request: Request):
        if not self._check(request.path_params["token"]):
            return JSONResponse({"error": "bad token"}, status_code=401)
        try:
            payload = await request.json()
        except Exception:
            return JSONResponse({"error": "bad json"}, status_code=400)
        adapter = self._route(payload.get("bot_id"))
        if adapter is None:
            return JSONResponse({"error": "unknown bot"}, status_code=404)
        await adapter.on_callback(payload)
        return JSONResponse({"ok": True})

    async def _control(self, websocket: WebSocket):
        if not self._check(websocket.path_params["token"]):
            await websocket.close(code=4401)
            return
        await websocket.accept()
        adapter: Optional[MeetStreamBotAdapter] = None
        try:
            while True:
                message = await websocket.receive_text()
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    continue
                if adapter is None:
                    adapter = self._route(data.get("bot_id"))
                    if adapter is None:
                        await websocket.close(code=4404)
                        return
                    await adapter.on_control_connected(websocket)
                await adapter.on_control_message(data)
        except WebSocketDisconnect:
            if adapter is not None:
                await adapter.on_control_disconnected()


# =========================================================================================
# Adapter
# =========================================================================================
class MeetStreamBotAdapter:
    name = "meetstream"

    def __init__(
        self,
        api_key: str,
        ingress: Ingress,
        public_base_url: str,
        *,
        api_base: str = API_BASE,
        transcript_preset: str = "meetstream_native",
        waiting_room_timeout_s: int = 300,
        bot_message: Optional[str] = None,
        custom_attributes: Optional[dict] = None,
        poll_interval_s: float = 5.0,
        client: Optional[httpx.AsyncClient] = None,
        retention_hours: int = 24,
    ) -> None:
        if transcript_preset not in TRANSCRIPT_PRESETS:
            raise MeetStreamError(f"unknown transcript preset {transcript_preset!r}")
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.ingress = ingress
        self.public_base_url = public_base_url
        self.transcript_preset = transcript_preset
        self.waiting_room_timeout_s = waiting_room_timeout_s
        self.bot_message = bot_message
        self.custom_attributes = custom_attributes or {}
        self.poll_interval_s = poll_interval_s
        self.retention_hours = retention_hours
        self._client = client or httpx.AsyncClient(timeout=30.0)
        self._queue: asyncio.Queue[Optional[BotEvent]] = asyncio.Queue()
        self._control: Optional[WebSocket] = None
        self._control_ready = asyncio.Event()
        self._sender: Optional[asyncio.Task] = None
        self._poller: Optional[asyncio.Task] = None
        self._last_state: Optional[BotState] = None
        self._terminal = False
        self._t0 = time.monotonic()
        self.bot_id: Optional[str] = None
        self.transcript_id: Optional[str] = None
        self.raw_events_path = None
        self.commands_sent: list[dict] = []
        self.inbound_chat: list[dict] = []

    def _headers(self) -> dict:
        return {"Authorization": f"Token {self.api_key}", "Content-Type": "application/json"}

    def _archive(self, kind: str, payload: dict) -> None:
        if self.raw_events_path is None:
            return
        with open(self.raw_events_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"t": round(time.monotonic() - self._t0, 3), "kind": kind, "payload": payload}, default=str) + "\n")

    # -- create / join ----------------------------------------------------------------------
    def create_body(self, meeting_url: str, display_name: str) -> dict:
        urls = self.ingress.paths(self.public_base_url)
        body: dict = {
            "meeting_link": meeting_url,
            "bot_name": display_name,
            "video_required": False,
            "audio_required": True,
            "callback_url": urls["callback"],
            "live_transcription_required": {"webhook_url": urls["transcript"]},
            "socket_connection_url": {"websocket_url": urls["control"]},
            "recording_config": {
                "transcript": {"provider": TRANSCRIPT_PRESETS[self.transcript_preset]},
                "retention": {"type": "timed", "hours": self.retention_hours},
            },
            "automatic_leave": {
                "waiting_room_timeout": int(min(max(self.waiting_room_timeout_s, 60), 600)),
                "no_one_joined_timeout": 600,
                "everyone_left_timeout": 300,
            },
            "custom_attributes": self.custom_attributes,
        }
        if self.bot_message:
            body["bot_message"] = self.bot_message[:2000]
        return body

    async def join(self, meeting_url: str, display_name: str) -> str:
        await self.ingress.start()
        self.ingress.register(self)
        response = await self._client.post(
            f"{self.api_base}/bots/create_bot", headers={**self._headers(), "Idempotency-Key": uuid.uuid4().hex}, json=self.create_body(meeting_url, display_name)
        )
        if response.status_code not in (200, 201, 507):
            self.ingress.unregister(self)
            raise MeetStreamError(f"create_bot failed {response.status_code}: {response.text[:400]}")
        payload = response.json()
        self.bot_id = payload.get("bot_id")
        self.transcript_id = payload.get("transcript_id")
        self.ingress.unregister(self)
        self.ingress.register(self)
        self._archive("create_bot", payload)
        self._poller = asyncio.create_task(self._poll_status())
        return self.bot_id or ""

    async def _poll_status(self) -> None:
        """Fallback for missed callbacks (they are unsigned and not retried)."""
        while not self._terminal and self.bot_id:
            try:
                response = await self._client.get(f"{self.api_base}/bots/{self.bot_id}/status", headers=self._headers())
                if response.status_code == 200:
                    status = str(response.json().get("status", "")).replace("_", "").replace(" ", "").lower()
                    await self._emit_status(status, source="poll")
            except httpx.HTTPError as exc:
                log.warning("status poll failed: %s", exc)
            await asyncio.sleep(self.poll_interval_s)

    async def _emit_status(self, raw: str, *, source: str, detail: Optional[str] = None, state: Optional[BotState] = None) -> None:
        state = state or STATUS_MAP.get(raw)
        if state is None:
            log.info("unmapped bot status %r (%s)", raw, source)
            return
        if state == self._last_state and state not in (BotState.left, BotState.aborted):
            return
        if self._terminal:
            return
        self._last_state = state
        await self._queue.put(BotStatusEvent(state=state, detail=f"{raw} ({source})" + (f": {detail}" if detail else "")))
        if state in (BotState.left, BotState.aborted):
            self._terminal = True
            await self._queue.put(None)

    # -- inbound from MeetStream ------------------------------------------------------------
    async def on_callback(self, payload: dict) -> None:
        self._archive("callback", payload)
        bot_event = str(payload.get("bot_event") or payload.get("event") or "")
        if bot_event.startswith("participant_events."):
            return
        if bot_event == "bot.done":
            return
        state = BOT_EVENT_MAP.get(bot_event)
        if state is None:
            return
        await self._emit_status(bot_event, source="webhook", detail=payload.get("message") or payload.get("failure_reason"), state=state)

    async def on_transcript(self, payload: dict) -> None:
        self._archive("transcript", payload)
        text = (payload.get("transcript") or payload.get("utterance") or "").strip()
        if not text:
            return
        speaker = Speaker(id=str(payload.get("speakerId") or payload.get("speaker_id") or payload.get("speakerName") or "unknown"), name=payload.get("speakerName") or payload.get("speaker_name"))
        words = payload.get("words") or []
        start = _seconds(words[0].get("start")) if words else _seconds(payload.get("timestamp"))
        end = _seconds(words[-1].get("end"), start) if words else start
        is_final = bool(payload.get("is_final", True))
        end_of_turn = bool(payload.get("end_of_turn", is_final))
        if end_of_turn:
            is_final = True  # a turn end always closes the utterance, whatever the provider's final flag says
        await self._queue.put(SpeechEvent(speaker=speaker, speaking=True))
        await self._queue.put(Utterance(speaker=speaker, text=text, start=start, end=end, is_final=is_final, confidence=payload.get("end_of_turn_confidence")))
        if end_of_turn:
            await self._queue.put(SpeechEvent(speaker=speaker, speaking=False))

    async def on_control_connected(self, websocket: WebSocket) -> None:
        self._control = websocket
        self._control_ready.set()
        log.info("control socket connected for bot %s", self.bot_id)

    async def on_control_message(self, data: dict) -> None:
        self._archive("control", data)
        kind = data.get("type") or data.get("command")
        if kind == "usermsg":
            self.inbound_chat.append(data)
        # acks ({command, bot_id, status}) are archived only

    async def on_control_disconnected(self) -> None:
        self._control = None
        self._control_ready.clear()

    # -- BotAdapter ------------------------------------------------------------------------
    async def events(self) -> AsyncIterator[BotEvent]:
        while True:
            item = await self._queue.get()
            if item is None:
                return
            yield item

    async def _send(self, command: dict) -> None:
        if self._control is None:
            try:
                await asyncio.wait_for(self._control_ready.wait(), timeout=10)
            except asyncio.TimeoutError as exc:
                raise MeetStreamError("control socket not connected; the bot cannot speak yet") from exc
        assert self._control is not None
        command = {**command, "bot_id": self.bot_id}
        self.commands_sent.append(command if command.get("command") != "sendaudio" else {**command, "audiochunk": f"<{len(command.get('audiochunk', ''))} b64 chars>"})
        await self._control.send_text(json.dumps(command))

    async def play_audio(self, clip: AudioClip) -> Optional[float]:
        if clip.mime != "audio/pcm" or clip.sample_rate != TARGET_RATE:
            raise MeetStreamError("MeetStream bridge needs PCM16 mono at 48 kHz (set the TTS output format to PCM)")
        if self._sender and not self._sender.done():
            self._sender.cancel()
        chunks = list(chunk_pcm16(clip.data, TARGET_RATE, CHUNK_SECONDS))

        async def pump():
            for i, chunk in enumerate(chunks):
                await self._send({"command": "sendaudio", "audiochunk": b64(chunk), "sample_rate": TARGET_RATE, "encoding": "pcm16", "channels": 1, "endianness": "little"})
                if i < len(chunks) - 1:
                    await asyncio.sleep(SEND_INTERVAL)

        self._sender = asyncio.create_task(pump())
        await asyncio.sleep(0)  # let the first chunk go out
        return 0.3  # playback start is not observable; the first chunk is typically audible within a few hundred ms

    async def stop_audio(self) -> None:
        if self._sender and not self._sender.done():
            self._sender.cancel()
        try:
            await self._send({"command": "interrupt", "action": "clear_audio_queue"})
        except MeetStreamError:
            pass

    async def send_chat(self, text: str) -> None:
        if not self.bot_id:
            return
        response = await self._client.post(f"{self.api_base}/bots/{self.bot_id}/send_message", headers=self._headers(), json={"message": text[:2000], "metadata": {"message_type": "text"}})
        if response.status_code == 409 and self._control is not None:  # not in meeting yet per REST; try the socket
            await self._send({"command": "sendmsg", "message": text[:2000], "msg": text[:2000]})
        elif response.status_code >= 400:
            log.warning("send_message failed %s: %s", response.status_code, response.text[:200])

    async def leave(self) -> None:
        if not self.bot_id:
            return
        if self._sender and not self._sender.done():
            try:
                await asyncio.wait_for(self._sender, timeout=15)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
        response = await self._client.post(f"{self.api_base}/bots/{self.bot_id}/remove_bot", headers=self._headers())
        if response.status_code >= 400:
            log.warning("remove_bot failed %s: %s", response.status_code, response.text[:200])
        for _ in range(20):
            if self._terminal:
                break
            try:
                status = await self._client.get(f"{self.api_base}/bots/{self.bot_id}/stop_status", headers=self._headers())
                if status.status_code == 200 and str(status.json().get("status", "")).lower() in ("stopped", "force_stopped", "failed", "cancelled"):
                    await self._emit_status("stopped", source="stop_status")
                    break
            except httpx.HTTPError:
                pass
            await asyncio.sleep(1.0)
        if not self._terminal:
            await self._emit_status("stopped", source="assumed")

    async def fetch_post_call(self) -> dict:
        """Transcript and chats after the bot has left (202 while still processing)."""
        out: dict = {"transcript": None, "chats": None}
        if self.transcript_id:
            r = await self._client.get(f"{self.api_base}/transcript/{self.transcript_id}/get_transcript", headers=self._headers())
            out["transcript"] = r.json() if r.status_code == 200 else {"status_code": r.status_code}
        if self.bot_id:
            r = await self._client.get(f"{self.api_base}/bots/{self.bot_id}/get_chats", headers=self._headers())
            out["chats"] = r.json() if r.status_code == 200 else {"status_code": r.status_code}
        return out

    async def close(self) -> None:
        if self._poller:
            self._poller.cancel()
        if self._sender and not self._sender.done():
            self._sender.cancel()
        self.ingress.unregister(self)
        await self._client.aclose()
