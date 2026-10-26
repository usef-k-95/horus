"""PCM helpers: resampling and chunking for the MeetStream bridge (PCM16 little-endian mono, 48 kHz)."""

from __future__ import annotations

import array
import base64
from typing import Iterator

TARGET_RATE = 48000


def resample_pcm16(data: bytes, src_rate: int, dst_rate: int = TARGET_RATE) -> bytes:
    """Linear-interpolation resampling of 16-bit little-endian mono PCM. Good enough for speech."""
    if src_rate == dst_rate or not data:
        return data
    samples = array.array("h")
    samples.frombytes(data[: len(data) - (len(data) % 2)])
    n_in = len(samples)
    if n_in < 2:
        return data
    n_out = int(n_in * dst_rate / src_rate)
    out = array.array("h", bytes(2 * n_out))
    ratio = (n_in - 1) / max(1, n_out - 1)
    for i in range(n_out):
        pos = i * ratio
        idx = int(pos)
        frac = pos - idx
        a = samples[idx]
        b = samples[idx + 1] if idx + 1 < n_in else a
        out[i] = int(a + (b - a) * frac)
    return out.tobytes()


def duration_seconds(data: bytes, rate: int = TARGET_RATE, channels: int = 1) -> float:
    return len(data) / (2.0 * rate * channels)


def chunk_pcm16(data: bytes, rate: int = TARGET_RATE, seconds: float = 0.8) -> Iterator[bytes]:
    """Yield chunks of about `seconds` each, aligned to whole samples."""
    step = max(2, int(rate * seconds) * 2)
    for start in range(0, len(data), step):
        yield data[start : start + step]


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")
