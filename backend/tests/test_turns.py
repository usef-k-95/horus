from horus_meet.models import Speaker, Utterance
from horus_meet.turns import TurnTaker

A = Speaker(id="a", name="Alice")
B = Speaker(id="b", name="Bob")


def utt(speaker, text, t, final=True):
    return Utterance(speaker=speaker, text=text, start=t, end=t + 1, is_final=final, received_at=t)


def test_partials_do_not_complete_a_turn():
    tt = TurnTaker(silence_s=0.8)
    assert tt.feed(utt(A, "the biggest", 0.0, final=False)) == []
    assert tt.feed(utt(A, "the biggest obstacle", 0.4, final=False)) == []
    assert tt.flush_if_silent(5.0) is None  # partial still open, never flush mid-sentence


def test_silence_after_final_completes_turn():
    tt = TurnTaker(silence_s=0.8)
    tt.feed(utt(A, "the biggest obstacle is cost", 1.0))
    assert tt.flush_if_silent(1.5) is None
    turn = tt.flush_if_silent(1.9)
    assert turn is not None
    assert turn.text == "the biggest obstacle is cost"
    assert turn.speaker.id == "a"
    assert turn.last_final_received_at == 1.0
    assert turn.completed_at == 1.9


def test_multiple_finals_join_into_one_turn():
    tt = TurnTaker(silence_s=0.8)
    tt.feed(utt(A, "first sentence.", 1.0))
    tt.feed(utt(A, "second sentence.", 1.5))
    turn = tt.flush_if_silent(2.4)
    assert turn.text == "first sentence. second sentence."
    assert turn.utterances == 2


def test_speaker_change_closes_previous_turn():
    tt = TurnTaker(silence_s=0.8)
    tt.feed(utt(A, "I think cost", 1.0))
    completed = tt.feed(utt(B, "I disagree", 1.2))
    assert len(completed) == 1 and completed[0].speaker.id == "a"
    assert tt.speaking.id == "b"


def test_force_close_without_finals_returns_none():
    tt = TurnTaker()
    tt.feed(utt(A, "um", 0.0, final=False))
    assert tt.force_close(1.0) is None
    assert tt.speaking is None


def test_speech_off_closes_provisional_turn_and_absorbs_late_final():
    from horus_meet.models import SpeechEvent

    tt = TurnTaker(silence_s=0.8, reconcile_window_s=2.5)
    tt.speech(SpeechEvent(speaker=A, speaking=True, at=1.0))
    tt.feed(utt(A, "the biggest obstacle", 1.5, final=False))
    tt.feed(utt(A, "the biggest obstacle is cost", 2.0, final=False))
    tt.speech(SpeechEvent(speaker=A, speaking=False, at=2.3))
    assert tt.flush_if_silent(2.9) is None            # not yet 0.8 s of silence after speech ended
    turn = tt.flush_if_silent(3.2)
    assert turn is not None and turn.provisional is True
    assert turn.text == "the biggest obstacle is cost"  # partial text used
    assert turn.speech_ended_at == 2.3
    # the provider's final transcript arrives 1.5 s later: absorbed, not a new turn
    assert tt.feed(utt(A, "the biggest obstacle is cost.", 3.8)) == []
    assert tt.flush_if_silent(10.0) is None
    assert tt.reconciled_finals == 1


def test_new_speech_after_provisional_close_is_a_new_turn():
    from horus_meet.models import SpeechEvent

    tt = TurnTaker(silence_s=0.8)
    tt.speech(SpeechEvent(speaker=A, speaking=True, at=1.0))
    tt.feed(utt(A, "first point", 1.5, final=False))
    tt.speech(SpeechEvent(speaker=A, speaking=False, at=1.8))
    assert tt.flush_if_silent(2.7).provisional is True
    tt.speech(SpeechEvent(speaker=A, speaking=True, at=3.0))      # speaker starts a new sentence
    tt.feed(utt(A, "second point", 3.4))
    tt.speech(SpeechEvent(speaker=A, speaking=False, at=3.6))
    second = tt.flush_if_silent(4.5)
    assert second is not None and second.text == "second point"
