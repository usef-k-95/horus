"""End-to-end dry run: an approved interview plan in the engagement state, the horus-meet server
tools driven as the interviewer would drive them against the mock provider, the state bridge writing
back, and the interviewer's post-call write-back passing the integrity rules."""

import json
import os
from datetime import date

import pytest

from horus_state.service import Service

LINES = ["Yes, that's fine, go ahead.", "Cost is the main obstacle. I can send you our member survey.", "Start with firms already filing online. Goodbye."]


def _json(result):
    return json.loads(result)


@pytest.fixture
def engagement(tmp_path, monkeypatch):
    svc = Service(tmp_path, actor="principal", session_id="dry")
    svc.init_engagement("MER-2026-017", "Meridia SME e-invoicing", {"entity": "Ministry of Finance", "country": "MER"}, supervisors=["sup"])
    stk = svc.create("stakeholders", {"name": "Head of the Merchants Association", "category": "industry_association", "engagement": {"priority": 1, "format": "interview"}})
    meeting = svc.create("meetings", {
        "kind": "interview", "title": "Interview: Merchants Association", "purpose": "Barriers and phasing", "platform": "meet", "join_url": "mock://meeting",
        "participants": [{"stakeholder": stk["id"], "role": "stakeholder", "name": "Head of the Merchants Association"}],
        "plan": {"objectives": ["Understand barriers", "Test phasing"], "question_guide": [{"id": "Q1", "question": "What is the biggest obstacle for your members?", "priority": 1}, {"id": "Q2", "question": "Which firms should come first in a phased mandate?", "priority": 1}], "disclosure_script": "Hello, I am Horus, an AI participant...", "attribution_rule": "background"},
    })
    apv = svc.request_approval({"collection": "meetings", "id": meeting["id"]}, "interview_plan", "Interview plan for the Merchants Association")
    Service(tmp_path, actor="supervisor:sup", session_id="dry").decide_approval(apv["id"], "approved")
    monkeypatch.setenv("HORUS_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("HORUS_MEET_PROVIDER", "mock")
    monkeypatch.setenv("HORUS_MEET_MOCK_SCALE", "0.05")
    monkeypatch.setenv("HORUS_MEET_MOCK_LINES", json.dumps(LINES))
    monkeypatch.setenv("HORUS_MEET_MOCK_NAME", "Head of the Merchants Association")
    return svc, stk, meeting


async def test_interview_dry_run(engagement, tmp_path):
    svc, stk, meeting = engagement
    from horus_meet import server

    server._sessions.clear()
    server._settings = None
    mid = meeting["id"]

    joined = _json(await server.join(mid, "mock://meeting", platform="meet", grace_s=20))
    assert joined.get("state") == "joined", joined
    rec = svc.get("meetings", mid)
    assert rec["status"] == "joining" and rec["bot"]["provider"] == "mock" and rec["bot"]["admitted_at"]

    disclosed = _json(await server.disclose(mid, "Hello, I am Horus, an AI participant working with the project team. This conversation is transcribed. Is that all right?"))
    assert disclosed["state"] == "disclosed"
    assert svc.get("meetings", mid)["disclosure"]["text"].startswith("Hello")

    first = _json(await server.listen(mid, 45))
    assert first["turns"], first
    assert "fine" in first["turns"][-1]["text"].lower()
    consent = _json(await server.consent(mid, True, given_by=stk["id"], attribution_rule="background", text=first["turns"][-1]["text"]))
    assert consent["granted"] is True
    rec = svc.get("meetings", mid)
    assert rec["status"] == "in_progress" and rec["consent"]["ai_participant"] is True and rec["consent"]["given_by"] == stk["id"]

    await server.say(mid, "To start, what is the biggest obstacle for your members?")
    second = _json(await server.listen(mid, 45))
    assert second["turns"] and "obstacle" in second["turns"][-1]["text"].lower()
    marked = _json(await server.mark(mid, "document_promised", "member survey"))
    assert marked["label"] == "document_promised"

    await server.say(mid, "Which firms should come first in a phased mandate?")
    third = _json(await server.listen(mid, 45))
    assert third["turns"] and "goodbye" in third["turns"][-1]["text"].lower()

    left = _json(await server.leave(mid, "Thank you, that was very helpful."))
    assert left["state"] == "left", left
    rec = svc.get("meetings", mid)
    assert rec["bot"]["left_at"] and rec["transcript"]["path"] and rec["held_at"]
    assert any(m["label"] == "document_promised" for m in rec["live"]["marks"])
    assert (tmp_path / rec["transcript"]["path"]).exists()

    # the interviewer's write-back
    iv = Service(tmp_path, actor="interviewer:i1", session_id="dry")
    src = iv.create("sources", {"title": "Interview with the Head of the Merchants Association", "type": "interview", "citation": f"Interview {mid}", "tier": "A", "tier_rationale": "participant's own stated position", "independence_group": f"interview-{mid}"})
    ev = iv.create("evidence", {"statement": "The association sees compliance cost as the main obstacle for its members", "kind": "position", "sources": [src["id"]], "attribution": "background", "meeting": mid, "about": [stk["id"]], "speaker": stk["id"]})
    assert ev["grade"] == "A" and ev["validated"] is True
    act = iv.create("actions", {"kind": "client_request_document", "title": "Member survey promised by the association", "owner": stk["id"], "due": str(date.today())})
    held = iv.update("meetings", mid, {"status": "held", "interview_record": {"topics": [{"topic": "barriers", "position": "cost is the main obstacle", "evidence": ev["id"]}], "documents_promised": [act["id"]], "proposed_updates": {"stakeholder_patch": {"stance": "sceptical", "concerns": ["compliance cost"]}}}, "debrief": {"path": f"meetings/{mid}/debrief.md", "by": "interviewer:i1"}})
    assert held["status"] == "held"
    with pytest.raises(Exception):
        iv.create("communications", {"direction": "outbound", "from": "interviewer", "to": ["x@y"], "date": "2026-10-26T10:00:00Z", "summary": "not allowed"})  # rule 26
    issues = svc.validate()
    assert not [i for i in issues if i["severity"] == "error"], issues
    checklist = svc.gate_checklist("AP2")
    assert any(c["rule_id"] == "ap2.interviews" for c in checklist["criteria"])
