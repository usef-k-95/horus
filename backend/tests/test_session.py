from horus_meet.session import MeetingSession


def test_consent_heuristics():
    assess = MeetingSession.assess_consent
    assert assess("Yes, that's fine, go ahead.") is True
    assert assess("No, I would rather not be recorded.") is False
    assert assess("No problem, go ahead.") is True
    assert assess("Hmm, let me think about the agenda first.") is None
    assert assess("Not sure... maybe later") is None  # ambiguous: reprompt rather than decide
