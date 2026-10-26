"""Build step 0: the live-meeting spike scenario.

join → disclose → confirm consent → N exchanges (listen, reply) → close → leave → report.
The reply policy is deliberately simple; the spike measures the audio pipeline, not the model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Optional

from .models import ControlKind, SpikeReport, Turn, BotState
from .session import MeetingSession

DEFAULT_DISCLOSURE = (
    "Hello, and thank you for joining. I am Horus, an AI participant working with the project team "
    "on behalf of the client. This conversation is being transcribed so that your views are captured "
    "accurately. The transcript is confidential and your comments will be attributed only as we agree. "
    "Is it all right with you to proceed on that basis?"
)
DISCLOSURE_CHAT = (
    "Horus AI participant: this conversation is being transcribed for the project team. The transcript is "
    "confidential and comments are attributed only as agreed. You may decline, or ask to go off the record, at any time."
)
CONSENT_REPROMPT = "Just to confirm: are you comfortable continuing with the conversation transcribed on that basis?"
DECLINE_TEXT = (
    "Understood, and thank you for telling me. I will stop here and the team will follow up with written "
    "questions or a call with a colleague instead. Thank you for your time."
)
CLOSING_TEXT = (
    "Thank you, that was very helpful. I will share a short summary with the team, and we will follow up "
    "on anything you offered to send. Have a good day."
)
GOODBYE = re.compile(r"\b(goodbye|bye|that's all|we're done|let's stop|end the call)\b", re.I)

SCRIPTED_QUESTIONS = [
    "Thank you. From where you sit, what is the single biggest obstacle to small firms adopting electronic invoicing today?",
    "That is useful. If a mandate were phased over three years, which firms should come first, and why?",
    "Understood. Which organisations would need to be on board for this to work, and who might resist it?",
    "Thank you. Is there any document or data you could share that would help us check these points?",
]


ECHO_OPENING = "To start, could you tell me about your role and how this topic affects the people you represent?"


def echo_policy(turn: Turn, index: int) -> str:
    snippet = turn.text.strip().rstrip(".")
    if len(snippet) > 140:
        snippet = snippet[:137] + "..."
    return f"Thank you. I noted that {snippet}. Could you say a little more about why that matters in practice?"


def scripted_policy(turn: Turn, index: int) -> str:
    """Reply to the participant's answer number `index` (0-based) with the next scripted question."""
    return SCRIPTED_QUESTIONS[(index + 1) % len(SCRIPTED_QUESTIONS)]


POLICIES: dict[str, Callable[[Turn, int], str]] = {"echo": echo_policy, "scripted": scripted_policy}
OPENINGS: dict[str, str] = {"echo": ECHO_OPENING, "scripted": SCRIPTED_QUESTIONS[0]}


@dataclass
class SpikeConfig:
    meeting_id: str
    platform: str
    meeting_url: str
    turns: int = 3
    grace_s: float = 120.0
    listen_timeout_s: float = 60.0
    consent_timeout_s: float = 30.0
    disclosure_script: str = DEFAULT_DISCLOSURE
    disclosure_chat: str = DISCLOSURE_CHAT
    consent_reprompt: str = CONSENT_REPROMPT
    decline_text: str = DECLINE_TEXT
    closing_text: str = CLOSING_TEXT
    reply_policy: str = "scripted"
    use_ack: bool = False
    ack_text: str = "Thank you."
    extra: dict = field(default_factory=dict)


async def _obtain_consent(cfg: SpikeConfig, session: MeetingSession) -> Optional[bool]:
    for attempt in range(2):
        result = await session.listen(cfg.consent_timeout_s)
        if result.ended:
            return None
        if any(c.kind == ControlKind.leave for c in result.controls):
            return None
        if not result.turns:
            if attempt == 0:
                await session.say(cfg.consent_reprompt)
                continue
            return None
        turn = result.turns[-1]
        verdict = session.assess_consent(turn.text)
        if verdict is None and attempt == 0:
            await session.say(cfg.consent_reprompt)
            continue
        if verdict is None:
            return None
        session.record_consent(turn, verdict)
        return verdict
    return None


async def run_spike(cfg: SpikeConfig, session: MeetingSession) -> SpikeReport:
    report = session.report
    policy = POLICIES[cfg.reply_policy]
    try:
        admitted = await session.start(cfg.meeting_url, cfg.grace_s)
        if not admitted:
            if session.state == BotState.aborted:
                last = report.states[-1] if report.states else None
                detail = (last.get("detail") if isinstance(last, dict) else getattr(last, "detail", None)) or "the provider reported a failure"
                report.outcome = "error"
                report.errors.append(f"bot could not join: {detail}")
            else:
                report.outcome = "not_admitted"
                report.errors.append(f"bot was not admitted within {cfg.grace_s:.0f} s")
            await session.leave(None)
            session.write_report()
            return report

        await session.disclose(cfg.disclosure_script, cfg.disclosure_chat)
        consent = await _obtain_consent(cfg, session)
        if consent is False:
            report.outcome = "consent_declined"
            await session.leave(cfg.decline_text)
            session.write_report()
            return report
        if consent is None:
            report.outcome = "consent_unclear"
            await session.leave("I was not able to confirm that you are comfortable proceeding, so I will stop here. Thank you for your time.")
            session.write_report()
            return report

        # An interviewer asks first; the participant's answers are the turns we time replies to.
        session._set_state(session.state.__class__.interviewing, "first question asked")
        await session.say(OPENINGS[cfg.reply_policy])
        exchanges = 0
        pending_whisper: Optional[str] = None
        while exchanges < cfg.turns:
            result = await session.listen(cfg.listen_timeout_s)
            if result.ended:
                report.outcome = "ended_by_platform"
                break
            kinds = {c.kind for c in result.controls}
            if ControlKind.leave in kinds:
                report.outcome = "ended_by_supervisor"
                break
            if ControlKind.pause in kinds and ControlKind.resume not in kinds:
                await session.say("Of course, one moment please.")
                while True:
                    paused = await session.listen(cfg.listen_timeout_s)
                    if paused.ended or any(c.kind in (ControlKind.resume, ControlKind.leave) for c in paused.controls):
                        break
                continue
            whispers = [c.text for c in result.controls if c.kind == ControlKind.whisper and c.text]
            if whispers:
                pending_whisper = whispers[-1]
            if not result.turns:
                if result.silence:
                    report.outcome = "participant_silent"
                    break
                continue
            turn = result.turns[-1]
            if len(result.turns) > 1:
                turn = turn.model_copy(update={"text": " ".join(t.text for t in result.turns)})
            if GOODBYE.search(turn.text):
                report.outcome = "ended_by_participant"
                break
            if cfg.use_ack:
                await session.say(cfg.ack_text)
            reply = pending_whisper or policy(turn, exchanges)
            pending_whisper = None
            await session.say(reply, turn=turn)
            exchanges += 1

        if report.outcome == "incomplete":
            report.outcome = "success" if exchanges > 0 else "no_turns"
        await session.leave(cfg.closing_text)
    except Exception as exc:  # the report must always be written
        report.outcome = "error"
        report.errors.append(repr(exc))
        try:
            await session.leave(None)
        except Exception as inner:
            report.errors.append(f"leave after error: {inner!r}")
    session.write_report()
    return report
