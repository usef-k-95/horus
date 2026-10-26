"""Command line for the live-meeting runtime: environment check, mock run, real spike, controls."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer

from .adapters.mock import MockBotAdapter, MockParticipant, MockTTS
from .config import Settings
from .models import ControlKind, Speaker
from .session import MeetingSession
from .spike import SpikeConfig, run_spike

app = typer.Typer(help="Horus live-meeting runtime (build step 0 spike).", no_args_is_help=True)

DEFAULT_PARTICIPANT_LINES = [
    "Yes, that's fine, go ahead.",
    "The biggest obstacle is cost. Most small shops use paper and the accounting software is too expensive for them.",
    "I would start with firms that already file VAT online, they have the systems, then the rest over two or three years.",
    "The tax authority and the banks need to be on board, and the merchant associations will resist if there are penalties early.",
    "Yes, I can send you our member survey from last year. Goodbye.",
]


def _run_dir(base: Path, label: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return base / f"{stamp}-{label}"


@app.command("check-env")
def check_env(env: Optional[Path] = typer.Option(None, help="Path to a .env file (default: nearest .env)")) -> None:
    """Show which provider settings are present (values are masked)."""
    settings = Settings.load(env)
    for key, value in settings.redacted().items():
        typer.echo(f"{key:28} {value}")
    missing = settings.missing_for_real_run()
    if missing:
        typer.echo("\nNot ready for a real run. Missing:")
        for item in missing:
            typer.echo(f"  - {item}")
        raise typer.Exit(code=2)
    typer.echo("\nReady for a real run.")


@app.command("mock-run")
def mock_run(
    turns: int = typer.Option(3, help="Number of exchanges after consent"),
    out: Path = typer.Option(Path("spike-runs"), help="Directory for run folders"),
    fast: bool = typer.Option(False, help="Scale all simulated delays down 50x"),
    decline: bool = typer.Option(False, help="Simulate a participant who declines"),
    never_admit: bool = typer.Option(False, help="Simulate a bot that is never admitted"),
    policy: str = typer.Option("scripted", help="Reply policy: scripted or echo"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Run the whole pipeline against the mock provider and print the latency report."""
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING, format="%(message)s")
    scale = 0.02 if fast else 1.0
    lines = ["No, I would rather not be recorded, sorry."] if decline else DEFAULT_PARTICIPANT_LINES
    participant = MockParticipant(speaker=Speaker(id="p1", name="Test participant"), lines=lines)
    bot = MockBotAdapter(participant, admit_after_s=None if never_admit else 1.2, time_scale=scale)
    tts = MockTTS(time_scale=scale)
    run_dir = _run_dir(out, "mock")
    session = MeetingSession("MTG-MOCK", bot, tts, run_dir, platform="mock", bot_name="Horus AI (recording)", time_scale=scale)
    cfg = SpikeConfig(meeting_id="MTG-MOCK", platform="mock", meeting_url="mock://meeting", turns=turns, grace_s=10, listen_timeout_s=30, consent_timeout_s=30, reply_policy=policy)
    report = asyncio.run(run_spike(cfg, session))
    typer.echo((run_dir / "report.md").read_text())
    typer.echo(f"Run folder: {run_dir}")
    raise typer.Exit(code=0 if report.outcome in {"success", "consent_declined", "not_admitted"} else 1)


@app.command("spike")
def spike(
    url: str = typer.Argument(..., help="Zoom or Google Meet link"),
    platform: str = typer.Option(..., help="zoom or meet"),
    turns: int = typer.Option(3, help="Number of exchanges after consent"),
    out: Path = typer.Option(Path("spike-runs"), help="Directory for run folders"),
    grace_s: float = typer.Option(120.0, help="Seconds to wait for admission"),
    ack: bool = typer.Option(False, help="Play a short acknowledgement before each reply"),
    policy: str = typer.Option("scripted", help="Reply policy: scripted or echo"),
    transcript: Optional[str] = typer.Option(None, help="Transcript preset (MeetStream: deepgram_sentence, meetstream_sentence, assemblyai_sentence, meeting_captions; Recall: recall_low_latency, deepgram_nova3, assemblyai)"),
    separate_streams: bool = typer.Option(False, help="Recall only: per-participant audio streams"),
    env: Optional[Path] = typer.Option(None, help="Path to a .env file"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Send the Horus bot into a real test meeting and measure the audio pipeline."""
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING, format="%(asctime)s %(message)s")
    settings = Settings.load(env)
    missing = settings.missing_for_real_run()
    if missing:
        typer.echo("Cannot run: missing settings:")
        for item in missing:
            typer.echo(f"  - {item}")
        raise typer.Exit(code=2)
    from .adapters.elevenlabs import ElevenLabsTTS
    from .spike import DISCLOSURE_CHAT

    meeting_id = f"MTG-SPIKE-{uuid.uuid4().hex[:6]}"
    run_dir = _run_dir(out, f"{platform}")

    async def main():
        ingress = None
        if settings.provider == "meetstream":
            from .adapters.meetstream import Ingress, MeetStreamBotAdapter

            tts = ElevenLabsTTS(settings.elevenlabs_api_key, settings.elevenlabs_voice_id, model_id=settings.elevenlabs_model_id, output_format=settings.elevenlabs_output_format)
            ingress = Ingress(port=settings.local_port)
            bot = MeetStreamBotAdapter(
                settings.meetstream_api_key,
                ingress,
                settings.public_base_url,
                api_base=settings.meetstream_api_base,
                transcript_preset=transcript or settings.transcript_preset,
                waiting_room_timeout_s=int(min(grace_s, 600)),
                bot_message=DISCLOSURE_CHAT,
                custom_attributes={"meeting_id": meeting_id},
            )
        else:
            from .adapters.recall import RecallBotAdapter

            tts = ElevenLabsTTS(settings.elevenlabs_api_key, settings.elevenlabs_voice_id, model_id=settings.elevenlabs_model_id, output_format="mp3_44100_128")
            placeholder = await tts.synthesize("Hello.")  # Recall's Output Audio needs automatic_audio_output
            bot = RecallBotAdapter(settings.recall_api_key, settings.recall_region, settings.public_ws_url, local_ws_port=settings.local_ws_port, transcript_preset=transcript or "recall_low_latency", separate_streams=separate_streams, waiting_room_timeout_s=int(min(grace_s, 600)), placeholder_clip=placeholder)
        session = MeetingSession(meeting_id, bot, tts, run_dir, platform=platform, bot_name=settings.bot_name)
        cfg = SpikeConfig(meeting_id=meeting_id, platform=platform, meeting_url=url, turns=turns, grace_s=grace_s, reply_policy=policy, use_ack=ack)
        typer.echo(f"Run folder: {run_dir}\nSupervisor controls: horus-meet control {run_dir} whisper|pause|resume|leave [text]")
        try:
            return await run_spike(cfg, session)
        finally:
            if ingress is not None:
                await ingress.stop()

    report = asyncio.run(main())
    typer.echo((run_dir / "report.md").read_text())
    raise typer.Exit(code=0 if report.outcome == "success" else 1)


@app.command("control")
def control(
    run_dir: Path = typer.Argument(..., help="The run folder printed by `spike` or `mock-run`"),
    kind: str = typer.Argument(..., help="whisper, pause, resume, takeover or leave"),
    text: Optional[str] = typer.Argument(None, help="Whisper text"),
) -> None:
    """Send a Supervisor control to a running session (file-drop channel for the spike)."""
    ControlKind(kind)  # validates
    controls_dir = run_dir / "controls"
    controls_dir.mkdir(parents=True, exist_ok=True)
    path = controls_dir / f"{datetime.now().strftime('%H%M%S%f')}-{kind}.json"
    path.write_text(json.dumps({"kind": kind, "text": text, "by": "supervisor"}), encoding="utf-8")
    typer.echo(f"queued {kind} for {run_dir}")


if __name__ == "__main__":
    app()
