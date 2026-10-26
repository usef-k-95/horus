"""ElevenLabs text-to-speech adapter (REST, non-streaming for the spike)."""

from __future__ import annotations

import time
from typing import Optional

import httpx

from ..audio import TARGET_RATE, duration_seconds, resample_pcm16
from ..models import AudioClip

API_BASE = "https://api.elevenlabs.io"
PCM_FORMATS = {"pcm_16000": 16000, "pcm_22050": 22050, "pcm_24000": 24000, "pcm_44100": 44100, "pcm_48000": 48000}


class TTSError(RuntimeError):
    pass


class ElevenLabsTTS:
    name = "elevenlabs"

    def __init__(
        self,
        api_key: str,
        voice_id: str,
        *,
        model_id: str = "eleven_flash_v2_5",
        output_format: str = "mp3_44100_128",
        client: Optional[httpx.AsyncClient] = None,
        timeout_s: float = 20.0,
    ) -> None:
        self.api_key = api_key
        self.voice_id = voice_id
        self.model_id = model_id
        self.output_format = output_format
        self._client = client or httpx.AsyncClient(timeout=timeout_s)

    async def synthesize(self, text: str) -> AudioClip:
        t0 = time.monotonic()
        url = f"{API_BASE}/v1/text-to-speech/{self.voice_id}"
        response = await self._client.post(
            url,
            params={"output_format": self.output_format},
            headers={"xi-api-key": self.api_key, "accept": "audio/mpeg" if self.output_format.startswith("mp3") else "application/octet-stream"},
            json={"text": text, "model_id": self.model_id},
        )
        if response.status_code >= 400:
            raise TTSError(f"ElevenLabs {response.status_code}: {response.text[:300]}")
        synth_ms = (time.monotonic() - t0) * 1000
        if self.output_format in PCM_FORMATS:
            rate = PCM_FORMATS[self.output_format]
            data = resample_pcm16(response.content, rate, TARGET_RATE)
            return AudioClip(data=data, mime="audio/pcm", sample_rate=TARGET_RATE, duration_s=duration_seconds(data), synth_ms=synth_ms, text=text)
        # MP3: duration is estimated from word count; the provider does not return it.
        words = max(1, len(text.split()))
        return AudioClip(data=response.content, mime="audio/mpeg", duration_s=words / 2.6, synth_ms=synth_ms, text=text)

    async def close(self) -> None:
        await self._client.aclose()
