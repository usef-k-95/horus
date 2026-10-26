"""Parsing of Recall.ai real-time payloads (shapes from docs.recall.ai/docs/real-time-event-payloads)."""

from horus_meet.adapters.recall import RecallBotAdapter


def test_parse_final_transcript_event():
    message = {
        "event": "transcript.data",
        "data": {
            "data": {
                "words": [
                    {"text": "hello", "start_timestamp": {"relative": 12.31}, "end_timestamp": {"relative": 12.80}},
                    {"text": "there", "start_timestamp": {"relative": 12.85}, "end_timestamp": {"relative": 13.10}},
                ],
                "language_code": "en",
                "participant": {"id": 100, "name": "Jane Doe", "is_host": False, "platform": "zoom", "extra_data": {}, "email": None},
            },
            "realtime_endpoint": {"id": "x", "metadata": {}},
            "transcript": {"id": "y", "metadata": {}},
            "recording": {"id": "z", "metadata": {}},
            "bot": {"id": "b", "metadata": {}},
        },
    }
    utt = RecallBotAdapter._parse_transcript(message, is_final=True)
    assert utt.text == "hello there" and utt.is_final
    assert utt.speaker.id == "100" and utt.speaker.name == "Jane Doe"
    assert utt.start == 12.31 and utt.end == 13.10


def test_parse_partial_with_null_end_and_missing_participant():
    message = {"event": "transcript.partial_data", "data": {"data": {"words": [{"text": "um", "start_timestamp": {"relative": 3.0}, "end_timestamp": {"relative": None}}], "participant": None}}}
    utt = RecallBotAdapter._parse_transcript(message, is_final=False)
    assert utt is not None and utt.end == 3.0 and utt.speaker.id == "unknown" and utt.is_final is False


def test_parse_speech_events():
    message = {"event": "participant_events.speech_off", "data": {"data": {"participant": {"id": 7, "name": "Bob"}, "timestamp": {"absolute": "2026-10-25T10:00:00Z", "relative": 40.2}}}}
    ev = RecallBotAdapter._parse_speech(message, speaking=False)
    assert ev.speaker.id == "7" and ev.speaking is False


def test_create_body_shape():
    from horus_meet.models import AudioClip

    adapter = RecallBotAdapter("key", "us-west-2", "wss://example.ngrok.app", placeholder_clip=AudioClip(data=b"abc", mime="audio/mpeg"), waiting_room_timeout_s=300)
    body = adapter._create_body("https://meet.google.com/abc-defg-hij", "Horus AI (recording)")
    assert body["bot_name"] == "Horus AI (recording)"
    endpoint = body["recording_config"]["realtime_endpoints"][0]
    assert endpoint["type"] == "websocket" and endpoint["url"].startswith("wss://example.ngrok.app/?token=")
    assert "transcript.data" in endpoint["events"] and "participant_events.speech_off" in endpoint["events"]
    assert body["recording_config"]["transcript"]["provider"] == {"recallai_streaming": {"mode": "prioritize_low_latency", "language_code": "en"}}
    assert body["automatic_leave"]["waiting_room_timeout"] == 300
    assert body["automatic_audio_output"]["in_call_recording"]["data"]["kind"] == "mp3"
