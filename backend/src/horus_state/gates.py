"""Gate checklists computed from the records (STATE_SCHEMA.md §7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .models.enums import Gate


@dataclass
class Criterion:
    rule_id: str
    description: str
    satisfied: bool
    evidence: str = ""

    def as_dict(self) -> dict:
        return {"rule_id": self.rule_id, "description": self.description, "satisfied": self.satisfied, "evidence": self.evidence}


@dataclass
class Checklist:
    gate: str
    criteria: list[Criterion] = field(default_factory=list)
    status: str = "not_ready"
    passed_in: str | None = None

    @property
    def ready(self) -> bool:
        return all(c.satisfied for c in self.criteria)

    def as_dict(self) -> dict:
        return {"gate": self.gate, "status": self.status, "ready": self.ready, "passed_in": self.passed_in, "criteria": [c.as_dict() for c in self.criteria]}


def _has_confirmed_decision(decisions: list[dict], kind: str, gate: str | None = None) -> tuple[bool, str]:
    for d in decisions:
        if d.get("kind") == kind and d.get("status") == "confirmed" and (gate is None or d.get("gate") == gate):
            return True, d["id"]
    return False, ""


def _released(deliverables: list[dict], types: set[str]) -> tuple[bool, str]:
    for d in deliverables:
        if d.get("type") in types:
            for v in d.get("versions", []):
                if v.get("status") in ("supervisor_approved", "sent", "client_approved"):
                    return True, f"{d['id']} v{v.get('v')}"
    return False, ""


def compute_checklist(service, gate: str) -> Checklist:
    eng = service.engagement()
    thresholds = (eng.get("settings") or {}).get("gate_thresholds", {})
    pathway = (eng.get("pathway") or {}).get("primary")
    gate_state = (eng.get("gates") or {}).get(gate, {})
    cl = Checklist(gate=gate, status=gate_state.get("status", "not_ready"), passed_in=gate_state.get("passed_in"))

    def load(coll):
        return list(service.store.iter_records(coll))

    decisions = load("decisions")
    stakeholders = load("stakeholders")
    deliverables = load("deliverables")
    meetings = load("meetings")
    oqs = load("open_questions")
    analyses = load("analyses")
    hyps = load("hypotheses")
    options = load("options")
    appraisals = load("appraisals")
    actions = load("actions")
    client_inputs = load("client_inputs")
    risks = load("risks")
    brief = service.store.read("brief") if service.store.exists("brief") else {}
    approach = service.store.read("approach") if service.store.exists("approach") else {}
    workplan = service.store.read("workplan") if service.store.exists("workplan") else {}

    def add(rule_id, description, satisfied, evidence=""):
        cl.criteria.append(Criterion(rule_id, description, bool(satisfied), evidence))

    roles = brief.get("client_roles") or {}
    p1_open = [q for q in oqs if q.get("priority") == "P1" and q.get("status") in ("open", "awaiting_client")]

    if gate == Gate.AP0.value:
        add("ap0.brief", "brief has objectives, scope and required deliverables mapped", bool(brief.get("objectives")) and bool(brief.get("scope_in")) and bool(brief.get("required_deliverables")))
        add("ap0.timeline", "brief has a timeline", bool((brief.get("timeline") or {}).get("end")))
        add("ap0.classification", "problem classification analysis exists", any(a.get("kind") == "problem_classification" for a in analyses))
        add("ap0.pathway", "primary pathway set", bool(pathway), str(pathway or ""))
        add("ap0.roles", "client PM, sponsor and ultimate decision maker exist", all(roles.get(k) for k in ("pm", "sponsor", "ultimate_decision_maker")))
        add("ap0.clarifications", "P1 clarifications answered or parked", not [q for q in p1_open if q.get("kind") == "clarification"])
        ok, ev = _has_confirmed_decision(decisions, "scope"); add("ap0.scope_decision", "scope decision confirmed", ok, ev)
        ok, ev = _has_confirmed_decision(decisions, "pathway"); add("ap0.pathway_decision", "pathway decision confirmed", ok, ev)
    elif gate == Gate.AP1.value:
        add("ap1.brief_confirmed", "brief confirmed", brief.get("status") in ("confirmed", "amended"))
        add("ap1.approach", "approach at version 1 or later, proposed or approved", approach.get("version", 0) >= 1 and approach.get("status") in ("proposed", "approved", "revised"))
        add("ap1.workplan", "workplan at version 1 or later, proposed or approved", workplan.get("version", 0) >= 1 and workplan.get("status") in ("proposed", "approved", "revised"))
        add("ap1.frameworks", "frameworks selected", bool(approach.get("frameworks")))
        ws = approach.get("workstreams") or []
        add("ap1.hypotheses", "at least one hypothesis per workstream", bool(hyps) and len(hyps) >= max(1, len(ws)))
        p1 = [s for s in stakeholders if (s.get("engagement") or {}).get("priority") == 1]
        meeting_requests = [a for a in actions if a.get("kind") == "client_request_meeting"]
        add("ap1.interview_requests", "every priority-1 stakeholder has a meeting request", bool(p1) and len(meeting_requests) >= len(p1), f"{len(meeting_requests)} requests for {len(p1)} priority-1 stakeholders")
        profiles = load("profiles")
        udm = roles.get("ultimate_decision_maker")
        add("ap1.profiles", "profiles started for the ultimate decision maker and the client entity", any(p.get("subject") == udm for p in profiles) if udm else False)
        ok, ev = _released(deliverables, {"kickoff_deck"}); add("ap1.kickoff_deck", "kickoff deck passed QA and approval", ok, ev)
        kick = [m for m in meetings if m.get("kind") == "kickoff"]
        add("ap1.decisions_sought", "kickoff meeting lists decisions sought", any(m.get("decisions_sought") for m in kick))
        ok, ev = _has_confirmed_decision(decisions, "methodology"); add("ap1.methodology", "methodology decision confirmed", ok, ev)
        ok, ev = _has_confirmed_decision(decisions, "workplan"); add("ap1.workplan_decision", "workplan decision confirmed", ok, ev)
    elif gate == Gate.AP2.value:
        rqs = ((approach.get("analytical_plan") or {}).get("research_questions") or [])
        add("ap2.research_done", "all research questions done or dropped", bool(rqs) and all(r.get("status") in ("done", "dropped") for r in rqs))
        add("ap2.diagnostic", "baseline and diagnostic analyses reviewed", any(a.get("kind") == "baseline" and a.get("status") in ("reviewed", "final") for a in analyses) and any(a.get("kind") == "diagnostic" and a.get("status") in ("reviewed", "final") for a in analyses))
        p1_interviews = [m for m in meetings if m.get("kind") == "interview" and any(((s.get("engagement") or {}).get("priority") == 1) and s["id"] in [p.get("stakeholder") for p in m.get("participants", [])] for s in stakeholders)]
        held = [m for m in p1_interviews if m.get("status") == "held" and (m.get("consent") or {}).get("ai_participant") and (m.get("transcript") or {}).get("verified_at")]
        share = thresholds.get("ap2_interviews_held_share", 0.7)
        add("ap2.interviews", f"at least {int(share*100)}% of priority-1 interviews held with consent and verified transcripts", bool(p1_interviews) and len(held) / max(1, len(p1_interviews)) >= share, f"{len(held)}/{len(p1_interviews)}")
        add("ap2.lens", "decision-maker lens and internal-politics analyses exist", any(a.get("kind") == "decision_maker_lens" for a in analyses) and any(a.get("kind") == "internal_politics" for a in analyses))
        add("ap2.hypotheses_tested", "no hypothesis is untested", bool(hyps) and all(h.get("status") != "untested" for h in hyps))
        add("ap2.updates_confirmed", "every held interview has its proposed updates confirmed", all((((m.get("interview_record") or {}).get("proposed_updates") or {}).get("confirmed_at")) for m in meetings if m.get("kind") == "interview" and m.get("status") == "held"))
        ok, ev = _released(deliverables, {"diagnostic_deck"}); add("ap2.deck", "diagnostic deck released", ok, ev)
        add("ap2.p1_questions", "no P1 open question is open", not p1_open)
    elif gate == Gate.AP3.value:
        short = [o for o in options if o.get("status") in ("short_list", "appraised", "preferred", "recommended")]
        add("ap3.shortlist", "short list of at least two options plus do-nothing", len(short) >= 2 and any(o.get("kind") == "do_nothing" for o in options))
        add("ap3.screening", "options screening analysis exists", any(a.get("kind") == "options_screening" for a in analyses))
        add("ap3.principles_proposed", "guiding principles proposed", any(d.get("kind") == "guiding_principle" for d in decisions))
        add("ap3.reaction_matrix", "reaction matrix exists", any(a.get("kind") == "stakeholder_reaction_matrix" for a in analyses))
        ok, ev = _released(deliverables, {"principles_deck"}); add("ap3.deck", "principles deck released", ok, ev)
        ok, ev = _has_confirmed_decision(decisions, "guiding_principle"); add("ap3.principles_confirmed", "guiding principles confirmed", ok, ev)
        ok, ev = _has_confirmed_decision(decisions, "criteria_weights"); add("ap3.weights", "criteria weights confirmed", ok, ev)
    elif gate == Gate.AP4.value:
        short = [o for o in options if o.get("status") in ("short_list", "appraised", "preferred", "recommended")]
        appraised = {ref for a in appraisals if a.get("status") in ("reviewed", "final") for ref in a.get("options", [])}
        add("ap4.appraisals", "every shortlisted option has a reviewed or final appraisal", bool(short) and all(o["id"] in appraised for o in short), f"{len(appraised)} appraised of {len(short)}")
        add("ap4.sensitivity", "sensitivity run for every quantified appraisal", all(a.get("sensitivity") for a in appraisals if any(i.get("quantified") for i in a.get("impacts", []))))
        add("ap4.comparison", "option comparison analysis reviewed", any(a.get("kind") == "option_comparison" and a.get("status") in ("reviewed", "final") for a in analyses))
        ok, ev = _released(deliverables, {"appraisal_deck"}); add("ap4.deck", "appraisal deck released", ok, ev)
        ok, ev = _has_confirmed_decision(decisions, "preferred_option"); add("ap4.preferred", "preferred option decision confirmed", ok, ev)
    elif gate == Gate.AP5.value:
        add("ap5.plans", "implementation and communication plans final", any(a.get("kind") == "implementation_plan" and a.get("status") == "final" for a in analyses) and any(a.get("kind") == "communication_plan" and a.get("status") == "final" for a in analyses))
        ok0, _ = _released(deliverables, {"decision_memo", "decision_brief"}); ok1, _ = _released(deliverables, {"executive_deck", "executive_summary"})
        add("ap5.tier0_tier1", "Tier 0 and Tier 1 deliverables released", ok0 and ok1)
        add("ap5.inputs", "every client input has a disposition", all(c.get("disposition") != "pending" for c in client_inputs))
        add("ap5.risks", "risk register has owners", all(r.get("owner") for r in risks))
        ok, ev = _has_confirmed_decision(decisions, "recommendation"); add("ap5.recommendation", "recommendation decision confirmed", ok, ev)
        add("ap5.handover", "handover actions complete", all(a.get("status") in ("done", "cancelled") for a in actions if "handover" in (a.get("title") or "").lower()))
    return cl


def all_checklists(service) -> dict[str, dict]:
    return {g.value: compute_checklist(service, g.value).as_dict() for g in Gate}
