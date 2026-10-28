"""End-to-end tests of the engagement-state service: rules, approvals, gates, views."""

from datetime import date, datetime, timezone

import pytest

from horus_state.rules import RuleViolation
from horus_state.service import Service
from horus_state.views import VIEWS, render


@pytest.fixture
def svc(tmp_path):
    s = Service(tmp_path, actor="principal", session_id="test")
    s.init_engagement("TST-2026-001", "Test engagement", {"entity": "Ministry of Testing", "country": "EGY"}, supervisors=["sup"])
    return s


def sup(svc):
    return Service(svc.store.workspace, actor="supervisor:sup", session_id="test")


def make_people(svc):
    pm = svc.create("stakeholders", {"name": "Client PM", "category": "client_pm", "is_client": True, "client_role": "pm", "decision_role": "input", "contact": {"email": "pm@example.gov"}})
    sponsor = svc.create("stakeholders", {"name": "Sponsor", "category": "client_decision_maker", "is_client": True, "client_role": "sponsor", "decision_role": "agree"})
    udm = svc.create("stakeholders", {"name": "Minister", "category": "client_decision_maker", "is_client": True, "client_role": "ultimate_decision_maker", "decision_role": "decide", "engagement": {"priority": 1, "format": "interview"}})
    return pm, sponsor, udm


def test_init_and_brief(svc):
    eng = svc.engagement()
    assert eng["code"] == "TST-2026-001" and eng["phase"] == "P0" and eng["gates"]["AP0"]["status"] == "not_ready"
    pm, sponsor, udm = make_people(svc)
    brief = svc.create("brief", {"title": "SME e-invoicing", "problem_statement": {"as_given": "Low adoption of e-invoicing among SMEs"}, "objectives": [{"id": "OBJ-1", "statement": "Raise adoption"}], "scope_in": ["SMEs"], "required_deliverables": [{"id": "RD-1", "description": "Policy note"}], "timeline": {"end": "2027-03-31"}, "client_roles": {"pm": pm["id"], "sponsor": sponsor["id"], "ultimate_decision_maker": udm["id"]}})
    assert brief["id"] == "BRF-001" and brief["version"] == 0
    with pytest.raises(Exception):
        svc.create("brief", {"title": "second", "problem_statement": {"as_given": "x"}})  # singleton
    updated = svc.update("brief", None, {"status": "confirmed", "version": 1})
    assert updated["version"] == 1 and (svc.store.root / "history" / "brief.v0.yaml").exists()


def test_evidence_computed_and_refs(svc):
    a = svc.create("sources", {"title": "Official statistics", "type": "official_statistics", "citation": "CAPMAS (2025)", "tier": "A", "tier_rationale": "national statistics office", "independence_group": "capmas"})
    b = svc.create("sources", {"title": "World Bank report", "type": "io_report", "citation": "World Bank (2024)", "tier": "B", "tier_rationale": "IO report", "independence_group": "worldbank", "url": "https://example.org/wb"})
    c = svc.create("sources", {"title": "Press", "type": "news", "citation": "Daily News (2025)", "tier": "C", "tier_rationale": "quality press", "independence_group": "dailynews"})
    e1 = svc.create("evidence", {"statement": "18% of micro-enterprises e-invoiced in 2025", "kind": "statistic", "sources": [a["id"], b["id"]], "corroboration": "corroborated", "confidence": "high"}, actor="researcher:r1")
    assert e1["grade"] == "A" and e1["independence_count"] == 2 and e1["validated"] is True
    e2 = svc.create("evidence", {"statement": "Compliance cost is the main obstacle", "kind": "finding", "sources": [c["id"]], "confidence": "medium"}, actor="researcher:r1")
    assert e2["grade"] == "C" and e2["validated"] is False
    with pytest.raises(RuleViolation) as exc:
        svc.create("evidence", {"statement": "dangling", "kind": "fact", "sources": ["SRC-9999"]})
    assert exc.value.rule == 2
    with pytest.raises(RuleViolation) as exc:
        svc.update("evidence", e2["id"], {"validated": True})
    assert exc.value.rule == 3
    with pytest.raises(RuleViolation) as exc:
        svc.create("decisions", {"kind": "scope", "statement": "x", "date": "2026-10-26", "rationale": "r"}, actor="researcher:r1")
    assert exc.value.rule == 26
    with pytest.raises(RuleViolation) as exc:
        svc.create("evidence", {"statement": "said in interview", "kind": "position", "sources": [c["id"]], "meeting": "MTG-404"})
    assert exc.value.rule in (2, 23)
    issues = svc.validate()
    assert any(i["rule"] == 16 and i["id"] == b["id"] for i in issues)  # tier B web source without snapshot
    # an interview is Tier A for the speaker's position but capped at C for an asserted fact
    stk = svc.create("stakeholders", {"name": "Association head", "category": "industry_association"})
    mtg = svc.create("meetings", {"kind": "interview", "title": "Interview", "purpose": "p", "participants": [{"stakeholder": stk["id"], "role": "stakeholder"}]})
    iv = svc.create("sources", {"title": "Interview with the association head", "type": "interview", "citation": "Interview", "tier": "A", "tier_rationale": "own statement", "independence_group": "interview-1"})
    pos = svc.create("evidence", {"statement": "The association opposes early penalties", "kind": "position", "sources": [iv["id"]], "attribution": "background", "meeting": mtg["id"]})
    fact = svc.create("evidence", {"statement": "Forty per cent of members have no accounting software", "kind": "statistic", "sources": [iv["id"]], "attribution": "background", "meeting": mtg["id"]})
    assert pos["grade"] == "A" and pos["validated"] is True
    assert fact["grade"] == "C" and fact["validated"] is False


def test_approvals_and_outbound(svc):
    pm, _, _ = make_people(svc)
    com = svc.create("communications", {"direction": "outbound", "from": "principal", "to": ["pm@example.gov"], "date": datetime.now(timezone.utc), "subject": "Kickoff", "summary": "Proposed kickoff agenda", "classification": "client_pm"})
    with pytest.raises(RuleViolation) as exc:
        svc.update("communications", com["id"], {"status": "sent"})
    assert exc.value.rule == 12
    apv = svc.request_approval({"collection": "communications", "id": com["id"]}, "client_pm_email", "Send kickoff agenda to the PM")
    assert apv["status"] == "pending" and apv["autonomy_level_at_request"] == "approve"
    with pytest.raises(RuleViolation):
        svc.decide_approval(apv["id"], "approved")  # principal may not decide
    decided = sup(svc).decide_approval(apv["id"], "approved", note="ok")
    assert decided["status"] == "approved"
    com2 = svc.get("communications", com["id"])
    assert com2["status"] == "approved" and com2["approval"] == apv["id"]
    sent = svc.update("communications", com["id"], {"status": "sent"})
    assert sent["status"] == "sent"
    with pytest.raises(RuleViolation) as exc:
        svc.update("approvals", apv["id"], {"note": "changed"})
    assert exc.value.rule == 25
    # shadow mode: PM email becomes notify → not_required
    sup(svc).set_autonomy(profile="shadow")
    apv2 = svc.request_approval({"collection": "communications", "id": com["id"]}, "client_pm_email", "another email")
    assert apv2["status"] == "not_required"
    assert svc.autonomy_level("tier0_tier1_release") == "approve"  # still gated in shadow mode


def test_meeting_transitions(svc):
    pm, _, udm = make_people(svc)
    m = svc.create("meetings", {"kind": "interview", "title": "Interview with the Minister", "purpose": "Test hypotheses", "participants": [{"stakeholder": udm["id"], "role": "stakeholder"}], "join_url": "https://meet.google.com/abc-defg-hij", "platform": "meet", "plan": {"objectives": ["Understand red lines"], "question_guide": [{"id": "Q1", "question": "What matters most?", "priority": 1}]}})
    with pytest.raises(RuleViolation) as exc:
        svc.update("meetings", m["id"], {"status": "joining"})
    assert exc.value.rule == 21  # no disclosure script, no approval
    svc.update("meetings", m["id"], {"plan": {"disclosure_script": "Hello, I am Horus, an AI participant..."}})
    with pytest.raises(RuleViolation) as exc:
        svc.update("meetings", m["id"], {"status": "joining"})
    assert exc.value.rule == 21  # approval missing
    apv = svc.request_approval({"collection": "meetings", "id": m["id"]}, "interview_plan", "Interview plan for the Minister")
    sup(svc).decide_approval(apv["id"], "approved")
    assert svc.get("meetings", m["id"])["plan"]["approval"] == apv["id"]
    joined = svc.update("meetings", m["id"], {"status": "joining"}, actor="meet")
    assert joined["status"] == "joining"
    with pytest.raises(RuleViolation) as exc:
        svc.update("meetings", m["id"], {"status": "in_progress"}, actor="meet")
    assert exc.value.rule == 22
    svc.update("meetings", m["id"], {"consent": {"ai_participant": True, "recording": True, "transcript": True, "given_by": udm["id"], "given_at": datetime.now(timezone.utc), "attribution_rule": "background"}}, actor="meet")
    live = svc.update("meetings", m["id"], {"status": "in_progress"}, actor="meet")
    assert live["status"] == "in_progress"
    with pytest.raises(Exception):
        svc.update("meetings", m["id"], {"status": "held"})  # interview_record required
    held = svc.update("meetings", m["id"], {"status": "held", "held_at": datetime.now(timezone.utc), "interview_record": {"topics": [{"topic": "phasing", "position": "supports a 3-year phase-in"}]}}, actor="interviewer:i1")
    assert held["status"] == "held"
    svc.record_intervention(m["id"], "whisper", "ask about the pilot", by="sup")
    assert svc.get("meetings", m["id"])["live"]["supervisor_interventions"][0]["type"] == "whisper"
    assert "Interview with the Minister" in render(svc, "meeting_plan", {"meeting": m["id"]})
    assert "phasing" in render(svc, "interview_debrief", {"meeting": m["id"]})


def test_deliverable_versions_and_release(svc, tmp_path):
    d = svc.create("deliverables", {"type": "kickoff_deck", "title": "Kickoff deck", "tier": "T1", "purpose": "Align on approach"})
    out = svc.store.workspace / "deliverables" / "DEL-001_v1_kickoff.pptx"
    out.write_bytes(b"fake")
    v1 = svc.register_version(d["id"], {"pptx": "deliverables/DEL-001_v1_kickoff.pptx"}, "first cut", {"visual": "pass", "logic": "pass", "traceability": "pass", "language": "pass", "sensitivity": "pass"}, {"resolved": True}, actor="producer:p1")
    assert v1["current_version"] == 1 and v1["versions"][0]["status"] == "qa_passed" and v1["versions"][0]["hash"].startswith("sha256:")
    with pytest.raises(RuleViolation) as exc:
        svc.release_version(d["id"], 1)
    assert exc.value.rule == 5
    apv = svc.request_approval({"collection": "deliverables", "id": d["id"], "version": 1}, "tier0_tier1_release", "Release kickoff deck v1")
    sup(svc).decide_approval(apv["id"], "approved")
    released = svc.release_version(d["id"], 1)
    assert released["versions"][0]["status"] == "supervisor_approved" and released["versions"][0]["approval"] == apv["id"]
    with pytest.raises(RuleViolation):
        svc.update("deliverables", d["id"], {"versions": []})
    v2 = svc.register_version(d["id"], {"pptx": "deliverables/x.pptx"}, "fails QA", {"visual": "fail", "logic": "pass", "traceability": "pass", "language": "pass", "sensitivity": "pass"}, actor="producer:p1")
    assert v2["versions"][1]["status"] == "qa_failed"


def test_gates_and_phases(svc):
    pm, sponsor, udm = make_people(svc)
    kickoff = svc.create("meetings", {"kind": "kickoff", "title": "Kickoff", "purpose": "Align", "conduct_mode": "principal_co_led", "participants": [{"stakeholder": pm["id"], "role": "client"}]})
    with pytest.raises(RuleViolation) as exc:
        svc.set_gate("AP0", "passed")
    assert exc.value.rule == 8
    dec = svc.create("decisions", {"kind": "gate", "gate": "AP0", "statement": "Brief confirmed", "made_by": [sponsor["id"]], "forum": kickoff["id"], "date": "2026-10-26", "rationale": "Agreed at kickoff", "status": "confirmed"})
    with pytest.raises(RuleViolation) as exc:
        svc.set_gate("AP0", "passed", dec["id"])
    assert exc.value.rule == 8  # needs an approved gate_transition approval
    apv = svc.request_approval({"collection": "engagement", "id": "ENG-001"}, "gate_transition", "Pass AP0")
    sup(svc).decide_approval(apv["id"], "approved")
    with pytest.raises(RuleViolation):
        svc.set_gate("AP0", "passed", dec["id"])  # criteria unsatisfied, no override
    eng = svc.set_gate("AP0", "passed", dec["id"], override_reason="test fixture: criteria waived")
    assert eng["gates"]["AP0"]["status"] == "passed"
    assert svc.set_phase("P1")["phase"] == "P1"
    with pytest.raises(RuleViolation) as exc:
        svc.set_phase("P2")
    assert exc.value.rule == 9
    with pytest.raises(RuleViolation):
        svc.update("engagement", None, {"phase": "P3"})
    ev = svc.checkpoint(["set up fixture"], next=["write brief"], blockers=["none"])
    assert ev["op"] == "checkpoint" and svc.engagement()["last_checkpoint"] == ev["id"]
    text = render(svc, "status", {"format": "context"})
    assert "Last checkpoint" in text and "P1" in text
    checklist = svc.gate_checklist("AP1")
    assert checklist["gate"] == "AP1" and checklist["ready"] is False


def test_all_views_render_and_search(svc):
    pm, sponsor, udm = make_people(svc)
    src = svc.create("sources", {"title": "Doc", "type": "government_document", "citation": "Gov (2025)", "tier": "B", "tier_rationale": "gov", "independence_group": "gov"})
    svc.create("evidence", {"statement": "Compliance cost is the main obstacle for small shops", "kind": "finding", "sources": [src["id"]]})
    svc.create("hypotheses", {"statement": "Cost, not awareness, limits adoption"})
    svc.create("options", {"code": "A", "title": "Phased mandate", "summary": "Mandate e-invoicing over 36 months", "kind": "regulatory_instrument", "status": "short_list"})
    svc.create("risks", {"description": "Merchant backlash", "likelihood": 4, "impact": 4})
    svc.create("open_questions", {"question": "Fiscal envelope?", "raised_by": "principal", "date": "2026-10-26", "owner": pm["id"], "priority": "P1", "blocking": ["AP1"]})
    svc.create("actions", {"kind": "client_request_meeting", "title": "Schedule interview with the Minister", "owner": pm["id"], "due": "2026-11-05"})
    d = svc.create("deliverables", {"type": "policy_note", "title": "Policy note", "tier": "T2", "purpose": "Main document"})
    m = svc.create("meetings", {"kind": "interview", "title": "Interview", "purpose": "p"})
    params = {"traceability": {"deliverable": d["id"]}, "meeting_plan": {"meeting": m["id"]}, "interview_debrief": {"meeting": m["id"]}}
    for name in VIEWS:
        text = render(svc, name, params.get(name, {}))
        assert isinstance(text, str) and text
    assert svc.store.reindex() >= 10
    hits = svc.search("compliance cost")
    assert any(h["collection"] == "evidence" for h in hits)
    exported = svc.export()
    assert "evidence" in exported["collections"] and "profiles" not in exported["collections"]


def test_date_fields_named_date_accept_dates():
    from horus_state.models.records import Milestone, Timeline

    t = Timeline(start="2026-11-01", milestones=[Milestone(name="Kickoff", date="2026-11-10")])
    assert t.milestones[0].date.isoformat() == "2026-11-10"
