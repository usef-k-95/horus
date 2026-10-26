"""The whole interview loop against a fake MeetStream: REST answered by an httpx mock transport,
status webhooks and transcript webhooks posted to our ingress, the control websocket opened by the
fake provider and used to capture `sendaudio`, `sendmsg` and `interrupt` commands."""

import asyncio
import json
import socket
import time

import httpx
import pytest
import websockets

from horus_meet.adapters import meetstream as ms
from horus_meet.adapters.meetstream import Ingress, MeetStreamBotAdapter
from horus_meet.audio import TARGET_RATE
from horus_meet.models import AudioClip, BotState
from horus_meet.session import MeetingSession
from horus_meet.spike import SpikeConfig, run_spike

SCALE = 0.05
LINES = [
    "Yes, that's fine, go ahead.",
    "The biggest obstacle is cost; most small shops still use paper.",
    "Start with firms that already file VAT online, then the rest over two years.",
    "The tax authority and the banks must be on board. Goodbye.",
]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class PCMMockTTS:
    name = "pcm-mock-tts"

    async def synthesize(self, text: str) -> AudioClip:
        await asyncio.sleep(0.01)
        words = max(1, len(text.split()))
        data = b"\x00\x10" * int(TARGET_RATE * 0.05 * words)  # 50 ms per word
        return AudioClip(data=data, mime="audio/pcm", sample_rate=TARGET_RATE, duration_s=len(data) / (2 * TARGET_RATE), synth_ms=10, text=text)


class FakeMeetStream:
    def __init__(self, port: int, token: str, lines: list[str]) -> None:
        self.port = port
        self.token = token
        self.lines = list(lines)
        self.status = "Scheduled"
        self.create_body = None
        self.chats: list[dict] = []
        self.ws_commands: list[dict] = []
        self.removed = False
        self._task = None
        self._speak_timer = None
        self._loop = asyncio.get_event_loop()
        self.base = f"http://127.0.0.1:{port}/ms/{token}"

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/bots/create_bot"):
            self.create_body = json.loads(request.content)
            self.status = "Joining"
            self._task = asyncio.ensure_future(self.run())
            return httpx.Response(201, json={"bot_id": "bot-1", "transcript_id": "tr-1", "meeting_url": self.create_body["meeting_link"], "status": "Active"})
        if path.endswith("/status"):
            return httpx.Response(200, json={"bot_id": "bot-1", "status": self.status})
        if path.endswith("/send_message"):
            self.chats.append(json.loads(request.content))
            return httpx.Response(200, json={"status": "accepted", "bot_id": "bot-1"})
        if path.endswith("/remove_bot"):
            self.removed = True
            self.status = "Stopped"
            asyncio.ensure_future(self._post(f"{self.base}/callback", {"event": "bot.stopped", "bot_event": "bot.stopped", "bot_id": "bot-1", "bot_status": "Stopped", "status_code": 200}))
            return httpx.Response(200, json={"bot_id": "bot-1", "status": "stopped"})
        if path.endswith("/stop_status"):
            return httpx.Response(200, json={"bot_id": "bot-1", "status": "stopped"})
        if path.endswith("/get_transcript"):
            return httpx.Response(200, json=[{"speaker": "Test participant", "transcript": " ".join(self.lines)}])
        if path.endswith("/get_chats"):
            return httpx.Response(200, json={"chatMessages": []})
        return httpx.Response(404, json={"error": path})

    async def _post(self, url: str, payload: dict) -> None:
        async with httpx.AsyncClient() as c:
            await c.post(url, json=payload)

    async def run(self) -> None:
        await asyncio.sleep(0.05)
        await self._post(f"{self.base}/callback", {"event": "bot.joining", "bot_event": "bot.joining", "bot_id": "bot-1", "bot_status": "Joining", "status_code": 200})
        await asyncio.sleep(0.05)
        await self._post(f"{self.base}/callback", {"event": "bot.in_waiting_room", "bot_event": "bot.in_waiting_room", "bot_id": "bot-1", "bot_status": "InWaitingRoom", "status_code": 200})
        await asyncio.sleep(0.05)
        async with websockets.connect(f"ws://127.0.0.1:{self.port}/ms/{self.token}/control") as ws:
            await ws.send(json.dumps({"type": "ready", "bot_id": "bot-1"}))
            self.status = "InMeeting"
            await self._post(f"{self.base}/callback", {"event": "bot.inmeeting", "bot_event": "bot.inmeeting", "bot_id": "bot-1", "bot_status": "InMeeting", "status_code": 200})
            try:
                while not self.removed:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=0.2)
                    except asyncio.TimeoutError:
                        continue
                    cmd = json.loads(raw)
                    if cmd.get("command") == "sendaudio":
                        self.ws_commands.append({"command": "sendaudio", "bytes": len(cmd.get("audiochunk", ""))})
                        self._schedule_answer()
                    else:
                        self.ws_commands.append(cmd)
                    await ws.send(json.dumps({"command": cmd.get("command"), "bot_id": "bot-1", "status": "sent"}))
            except websockets.ConnectionClosed:
                pass

    def _schedule_answer(self) -> None:
        if self._speak_timer and not self._speak_timer.done():
            self._speak_timer.cancel()
        self._speak_timer = asyncio.ensure_future(self._answer_after_gap())

    async def _answer_after_gap(self) -> None:
        await asyncio.sleep(0.35)  # no further audio for a while: the bot finished its utterance
        if not self.lines or self.removed:
            return
        line = self.lines.pop(0)
        words = line.split()
        t = time.time()
        payload = {
            "bot_id": "bot-1",
            "speakerName": "Test participant",
            "speakerId": "p1",
            "timestamp": 12.3,
            "utterance": line,
            "transcript": line,
            "words": [{"word": w, "start": 12.3 + i * 0.3, "end": 12.6 + i * 0.3, "confidence": 0.9} for i, w in enumerate(words)],
            "end_of_turn": True,
            "is_final": True,
            "turn_order": 1,
            "end_of_turn_confidence": 0.9,
            "transcription_mode": "sentence",
        }
        await self._post(f"{self.base}/transcript", payload)


@pytest.fixture
def fast_pacing(monkeypatch):
    monkeypatch.setattr(ms, "SEND_INTERVAL", 0.02)


async def test_full_interview_against_fake_meetstream(tmp_path, fast_pacing):
    port = free_port()
    ingress = Ingress(host="127.0.0.1", port=port)
    fake = FakeMeetStream(port, ingress.token, LINES)
    client = httpx.AsyncClient(transport=httpx.MockTransport(fake.handler))
    bot = MeetStreamBotAdapter("ms_test", ingress, f"http://127.0.0.1:{port}", api_base="http://fake/api/v1", bot_message="Horus AI participant: this meeting is transcribed.", client=client, poll_interval_s=0.2)
    session = MeetingSession("MTG-T", bot, PCMMockTTS(), tmp_path / "run", platform="meet", bot_name="Horus AI (recording)", time_scale=SCALE)
    cfg = SpikeConfig(meeting_id="MTG-T", platform="meet", meeting_url="https://meet.google.com/abc-defg-hij", turns=2, grace_s=20, listen_timeout_s=40, consent_timeout_s=40)
    try:
        report = await run_spike(cfg, session)
    finally:
        await ingress.stop()
    assert report.outcome == "success", (report.outcome, report.errors)
    assert len(report.turns) == 2 and report.consent.ai_participant is True
    # create_bot payload shape
    body = fake.create_body
    assert body["video_required"] is False and body["audio_required"] is True
    assert body["live_transcription_required"]["webhook_url"].endswith(f"/ms/{ingress.token}/transcript")
    assert body["socket_connection_url"]["websocket_url"].startswith("ws://") and body["callback_url"].endswith("/callback")
    assert body["recording_config"]["transcript"]["provider"] == {"meetstream_streaming": {}}
    assert body["automatic_leave"]["waiting_room_timeout"] == 60 * 0 + 60 if False else body["automatic_leave"]["waiting_room_timeout"] >= 60
    assert body["bot_message"].startswith("Horus AI")
    # the bot spoke through the control socket and posted the disclosure to chat
    assert sum(1 for c in fake.ws_commands if c.get("command") == "sendaudio") >= 3
    assert fake.chats and "Horus" in fake.chats[0]["message"]
    assert fake.removed is True
    states = [s.state for s in report.states]
    assert BotState.waiting_room in states and BotState.joined in states and BotState.left in states


def test_status_and_event_mapping():
    assert ms.STATUS_MAP["inwaitingroom"] == BotState.waiting_room
    assert ms.STATUS_MAP["notallowed"] == BotState.aborted
    assert ms.BOT_EVENT_MAP["bot.inmeeting"] == BotState.joined
    assert ms.BOT_EVENT_MAP["bot.kicked"] == BotState.left


async def test_play_audio_rejects_non_pcm():
    ingress = Ingress(host="127.0.0.1", port=free_port())
    bot = MeetStreamBotAdapter("ms_test", ingress, "http://127.0.0.1:1", client=httpx.AsyncClient(transport=httpx.MockTransport(lambda r: httpx.Response(404))))
    with pytest.raises(ms.MeetStreamError):
        await bot.play_audio(AudioClip(data=b"abc", mime="audio/mpeg"))
    await bot.close()


@pytest.mark.asyncio
async def test_native_raw_chunks_close_the_turn_on_end_of_turn():
    """MeetStream's own live transcription sends raw chunks: interim ones with is_final false, and a
    turn end that may arrive without is_final. The adapter must still close the utterance and the turn."""
    from horus_meet.adapters.meetstream import Ingress, MeetStreamBotAdapter, TRANSCRIPT_PRESETS
    from horus_meet.models import SpeechEvent, Utterance

    assert TRANSCRIPT_PRESETS["meetstream_native"] == {"meetstream_streaming": {}}
    bot = MeetStreamBotAdapter("ms_test", Ingress(port=free_port()), "https://example.test")
    assert bot.transcript_preset == "meetstream_native"
    base = {"bot_id": "b1", "speakerName": "Alice", "timestamp": "2026-10-26T07:00:00Z", "transcription_mode": "raw", "words": []}
    await bot.on_transcript({**base, "transcript": "Can you walk me", "is_final": False, "end_of_turn": False})
    await bot.on_transcript({**base, "transcript": "through the pilot", "is_final": False, "end_of_turn": True})
    events = []
    while not bot._queue.empty():
        events.append(bot._queue.get_nowait())
    utterances = [e for e in events if isinstance(e, Utterance)]
    assert [u.is_final for u in utterances] == [False, True]
    assert utterances[1].speaker.name == "Alice"
    speech = [e for e in events if isinstance(e, SpeechEvent)]
    assert speech[-1].speaking is False  # the turn closed
    await bot.close()
