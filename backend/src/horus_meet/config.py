"""Settings for the runtime, read from the environment and an optional .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

RECALL_REGIONS = ("us-east-1", "us-west-2", "eu-central-1", "ap-northeast-1")


def _find_env_file(start: Path) -> Optional[Path]:
    for folder in [start, *start.parents]:
        candidate = folder / ".env"
        if candidate.exists():
            return candidate
    return None


@dataclass
class Settings:
    provider: str = "meetstream"
    meetstream_api_key: Optional[str] = None
    meetstream_api_base: str = "https://api.meetstream.ai/api/v1"
    public_base_url: Optional[str] = None
    local_port: int = 8765
    elevenlabs_output_format: str = "pcm_24000"
    recall_api_key: Optional[str] = None
    recall_region: str = "us-west-2"
    public_ws_url: Optional[str] = None
    local_ws_port: int = 8765
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    elevenlabs_model_id: str = "eleven_flash_v2_5"
    bot_name: str = "Horus AI (recording)"
    env_file: Optional[Path] = field(default=None, repr=False)

    @classmethod
    def load(cls, env_path: Optional[Path] = None) -> "Settings":
        env_file = env_path or _find_env_file(Path.cwd())
        if env_file:
            load_dotenv(env_file, override=False)
        return cls(
            provider=os.getenv("HORUS_MEET_PROVIDER", "meetstream"),
            meetstream_api_key=os.getenv("MEETSTREAM_API_KEY") or None,
            meetstream_api_base=os.getenv("MEETSTREAM_API_URL", "https://api.meetstream.ai/api/v1"),
            public_base_url=os.getenv("HORUS_MEET_PUBLIC_URL") or None,
            local_port=int(os.getenv("HORUS_MEET_LOCAL_PORT", os.getenv("HORUS_MEET_LOCAL_WS_PORT", "8765"))),
            elevenlabs_output_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", "pcm_24000"),
            recall_api_key=os.getenv("RECALL_API_KEY") or None,
            recall_region=os.getenv("RECALL_REGION", "us-west-2"),
            public_ws_url=os.getenv("HORUS_MEET_PUBLIC_WS_URL") or None,
            local_ws_port=int(os.getenv("HORUS_MEET_LOCAL_WS_PORT", "8765")),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY") or None,
            elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID") or None,
            elevenlabs_model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5"),
            bot_name=os.getenv("HORUS_BOT_NAME", "Horus AI (recording)"),
            env_file=env_file,
        )

    def missing_for_real_run(self) -> list[str]:
        missing = []
        if self.provider == "meetstream":
            if not self.meetstream_api_key:
                missing.append("MEETSTREAM_API_KEY")
            if not self.public_base_url:
                missing.append("HORUS_MEET_PUBLIC_URL (public https URL of the tunnel to HORUS_MEET_LOCAL_PORT)")
        elif self.provider == "recall":
            if not self.recall_api_key:
                missing.append("RECALL_API_KEY")
            if self.recall_region not in RECALL_REGIONS:
                missing.append(f"RECALL_REGION (got {self.recall_region!r}; expected one of {', '.join(RECALL_REGIONS)})")
            if not self.public_ws_url:
                missing.append("HORUS_MEET_PUBLIC_WS_URL (tunnel URL for real-time events)")
        else:
            missing.append(f"HORUS_MEET_PROVIDER must be meetstream or recall (got {self.provider!r})")
        if not self.elevenlabs_api_key:
            missing.append("ELEVENLABS_API_KEY")
        if not self.elevenlabs_voice_id:
            missing.append("ELEVENLABS_VOICE_ID")
        return missing

    def redacted(self) -> dict:
        def mask(value: Optional[str]) -> str:
            if not value:
                return "(not set)"
            return value[:3] + "…" + value[-2:] if len(value) > 6 else "set"

        return {
            "env_file": str(self.env_file) if self.env_file else "(none found)",
            "HORUS_MEET_PROVIDER": self.provider,
            "MEETSTREAM_API_KEY": mask(self.meetstream_api_key),
            "HORUS_MEET_PUBLIC_URL": self.public_base_url or "(not set)",
            "HORUS_MEET_LOCAL_PORT": self.local_port,
            "ELEVENLABS_OUTPUT_FORMAT": self.elevenlabs_output_format,
            "RECALL_API_KEY": mask(self.recall_api_key),
            "RECALL_REGION": self.recall_region,
            "HORUS_MEET_PUBLIC_WS_URL": self.public_ws_url or "(not set)",
            "HORUS_MEET_LOCAL_WS_PORT": self.local_ws_port,
            "ELEVENLABS_API_KEY": mask(self.elevenlabs_api_key),
            "ELEVENLABS_VOICE_ID": self.elevenlabs_voice_id or "(not set)",
            "ELEVENLABS_MODEL_ID": self.elevenlabs_model_id,
            "HORUS_BOT_NAME": self.bot_name,
        }
