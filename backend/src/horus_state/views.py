"""Server-rendered views (STATE_SCHEMA.md §9). Each view returns Markdown; `as_json` returns data."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Callable, Optional

from .gates import all_checklists, compute_checklist


def _t(rows: list[list[Any]], header: list[str]) -> str:
    def cell(v: Any) -> str:
        if v is None:
            return ""
        s = str(v).replace("|", "\\|").replace("\n", " ")
        return s if len(s) <= 90 else s[:89] + "…"

    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        lines.append("| " + " | ".join(cell(c) for c in r) + " |")
    if not rows:
        lines.append("| " + " | ".join("—" for _ in header) + " |")
    return "\n".join(lines)


def _label(rec: dict) -> str:
    return rec.get("title") or rec.get("name") or rec.get("statement") or rec.get("summary") or rec.get("question") or rec.get("code") or rec.get("id", "")


def _fmt(d: Any) -> str:
    if isinstance(d, (datetime, date)):
        return d.isoformat()[:16]
    return str(d) if d else ""


# ---- views ------------------------------------------------------------------------------

def status(svc, params: dict) -> str:
    eng = svc.engagement()
    fmt = params.get("format", "brief")
    gates = all_checklists(svc)
    pending = svc.pending_approvals()
    oqs = svc.list("open_questions", {"status": {"in": ["open", "awaiting_client"]}, "priority": "P1"})
    due = [a for a in svc.list("actions", {"status": {"in": ["todo", "requested", "in_progress", "blocked"]}}) if a.get("due")]
    due.sort(key=lambda a: str(a["due"]))
    inbox = svc.list("communications", {"direction": "inbound", "status": "received"})
    upcoming = [m for m in svc.list("meetings", {"status": {"in": ["requested", "scheduled", "proposed"]}}) if m.get("scheduled_at") or m.get("status") in ("requested", "proposed")]
    cp = svc.last_checkpoint()
    lines = [
        f"# {eng.get('name')} ({eng.get('code')})",
        f"Phase **{eng.get('phase')}** · pathway **{(eng.get('pathway') or {}).get('primary') or 'not set'}** · autonomy profile **{((eng.get('settings') or {}).get('autonomy') or {}).get('profile')}**",
        "",
        "Gates: " + " · ".join(f"{g} {d['status']}{' (ready)' if d['ready'] and d['status'] != 'passed' else ''}" for g, d in gates.items()),
        f"Pending approvals: {len(pending)} · P1 open questions: {len(oqs)} · actions with due dates: {len(due)} · untriaged inbound: {len(inbox)} · meetings ahead: {len(upcoming)}",
    ]
    if cp and cp.get("checkpoint"):
        c = cp["checkpoint"]
        lines += ["", f"Last checkpoint {cp['ts'][:16]}:", "- next: " + "; ".join(c.get("next") or []) or "- next: (none)", "- blockers: " + ("; ".join(c.get("blockers") or []) or "none")]
    if fmt in ("context", "full"):
        if pending:
            lines += ["", "Pending approvals:"] + [f"- {a['id']} [{a['risk_class']}] {a['action_class']}: {a['summary']}" for a in pending[:10]]
        if oqs:
            lines += ["", "P1 open questions:"] + [f"- {q['id']} ({q['owner']}): {q['question']}" for q in oqs[:10]]
        if due:
            lines += ["", "Actions due soonest:"] + [f"- {a['id']} {_fmt(a['due'])} {a['owner']}: {a['title']}" for a in due[:10]]
        if upcoming:
            lines += ["", "Meetings ahead:"] + [f"- {m['id']} {m['kind']} {_fmt(m.get('scheduled_at'))} {m['status']}: {m['title']}" for m in upcoming[:10]]
        current_gate = next((g for g, d in gates.items() if d["status"] != "passed"), None)
        if current_gate:
            unmet = [c["description"] for c in gates[current_gate]["criteria"] if not c["satisfied"]]
            lines += ["", f"Next gate {current_gate}; unmet criteria:"] + [f"- {u}" for u in unmet[:12]]
    return "\n".join(lines)


def gate_checklist(svc, params: dict) -> str:
    gate = params.get("gate")
    data = {gate: compute_checklist(svc, gate).as_dict()} if gate else all_checklists(svc)
    out = []
    for g, d in data.items():
        out.append(f"## {g} — {d['status']}{' (ready)' if d['ready'] else ''}")
        out.append(_t([[("✓" if c["satisfied"] else "✗"), c["description"], c["evidence"]] for c in d["criteria"]], ["ok", "criterion", "evidence"]))
    return "\n\n".join(out)


def approvals_queue(svc, params: dict) -> str:
    rows = [[a["id"], a["risk_class"], a["action_class"], f"{a['target'].get('collection')}/{a['target'].get('id')}" + (f" v{a['target'].get('version')}" if a['target'].get("version") else ""), _fmt(a["requested_at"]), a["summary"]] for a in sorted(svc.pending_approvals(), key=lambda a: ({"high": 0, "medium": 1, "low": 2}[a["risk_class"]], str(a["requested_at"])))]
    return "# Approvals queue\n\n" + _t(rows, ["id", "risk", "class", "target", "requested", "summary"])


def pathway_summary(svc, params: dict) -> str:
    eng = svc.engagement()
    p = eng.get("pathway") or {}
    cls = svc.list("analyses", {"kind": "problem_classification"})
    lines = [f"# Pathway: {p.get('primary') or 'not set'}", f"Secondary: {', '.join(p.get('secondary') or []) or 'none'}", f"Rationale: {p.get('rationale') or ''}", f"Classified in: {p.get('classified_in') or ''} · confirmed in: {p.get('confirmed_in') or ''}"]
    for a in cls:
        c = a.get("content") or {}
        lines.append("")
        lines.append(_t([[s.get("question"), s.get("answer")] for s in c.get("signals", [])], ["signal", "answer"]))
        lines.append(_t([[k.get("pathway"), k.get("fit"), k.get("rationale")] for k in c.get("candidates", [])], ["candidate", "fit", "rationale"]))
    return "\n".join(lines)


def stakeholder_matrix(svc, params: dict) -> str:
    rows = []
    for s in sorted(svc.list("stakeholders", {"status": "active"}), key=lambda s: (-(s.get("influence") or 0), s.get("name"))):
        e = s.get("engagement") or {}
        rows.append([s["id"], s["name"], s.get("category"), s.get("influence"), s.get("interest"), s.get("stance"), s.get("decision_role"), e.get("priority"), e.get("status")])
    return "# Stakeholder matrix\n\n" + _t(rows, ["id", "name", "category", "influence", "interest", "stance", "RAPID", "priority", "engagement"])


def reaction_matrix(svc, params: dict) -> str:
    options = svc.list("options", {"status": {"in": ["short_list", "appraised", "preferred", "recommended"]}})
    principles = svc.list("decisions", {"kind": "guiding_principle"})
    targets = [(o["id"], f"{o['code']} {o['title']}") for o in options] + [(d["id"], f"principle {d['id']}") for d in principles]
    header = ["stakeholder"] + [t[1] for t in targets]
    rows = []
    for s in svc.list("stakeholders", {"status": "active"}):
        reactions = {r["target"]: r for r in s.get("predicted_reactions") or []}
        if not any(t[0] in reactions for t in targets):
            continue
        rows.append([s["name"]] + [(f"{reactions[t[0]]['reaction']} ({reactions[t[0]].get('confidence', '')[:1]})" if t[0] in reactions else "") for t in targets])
    return "# Stakeholder reaction matrix\n\n" + _t(rows, header)


def decision_log(svc, params: dict) -> str:
    rows = [[d["id"], _fmt(d["date"]), d["kind"], d["status"], ", ".join(d.get("made_by") or []), d["statement"]] for d in sorted(svc.list("decisions"), key=lambda d: str(d["date"]))]
    return "# Decision log\n\n" + _t(rows, ["id", "date", "kind", "status", "made by", "decision"])


def question_register(svc, params: dict) -> str:
    rows = [[q["id"], q["priority"], q["status"], q["owner"], ", ".join(q.get("blocking") or []), _fmt(q.get("due")), q["question"]] for q in sorted(svc.list("open_questions"), key=lambda q: (q["status"] in ("answered", "closed"), q["priority"]))]
    return "# Open questions\n\n" + _t(rows, ["id", "priority", "status", "owner", "blocks", "due", "question"])


def action_tracker(svc, params: dict) -> str:
    today = date.today()
    rows = []
    for a in sorted(svc.list("actions"), key=lambda a: (a["status"] in ("done", "cancelled"), str(a.get("due") or "9999"))):
        due = a.get("due")
        overdue = bool(due) and a["status"] not in ("done", "cancelled") and (due if isinstance(due, date) else date.fromisoformat(str(due))) < today
        rows.append([a["id"], a["kind"], a["owner"], a["status"] + (" OVERDUE" if overdue else ""), _fmt(due), a["title"]])
    return "# Action tracker\n\n" + _t(rows, ["id", "kind", "owner", "status", "due", "action"])


def evidence_table(svc, params: dict) -> str:
    filt: dict = {}
    if params.get("hypothesis"):
        filt["supports"] = {"contains": params["hypothesis"]}
    if params.get("about"):
        filt["about"] = {"contains": params["about"]}
    if params.get("meeting"):
        filt["meeting"] = params["meeting"]
    rows = []
    for e in svc.list("evidence", filt or None, limit=int(params.get("limit", 200))):
        if params.get("min_tier") and e.get("grade") and e["grade"] > params["min_tier"]:
            continue
        cites = "; ".join(svc.get("sources", s).get("citation", s) for s in e.get("sources", []) if svc.store.exists("sources", s))
        rows.append([e["id"], e["kind"], e.get("grade"), "yes" if e.get("validated") else "no", e["statement"], cites])
    return "# Evidence\n\n" + _t(rows, ["id", "kind", "grade", "validated", "statement", "sources"])


def bibliography(svc, params: dict) -> str:
    rows = [[s["tier"], s["citation"], s.get("url") or s.get("doi") or "", _fmt((s.get("access") or {}).get("retrieved_at"))] for s in sorted(svc.list("sources", {"status": "active"}), key=lambda s: (s["tier"], s["citation"]))]
    return "# Bibliography\n\n" + _t(rows, ["tier", "citation", "link", "retrieved"])


def traceability(svc, params: dict) -> str:
    d = svc.get("deliverables", params["deliverable"])
    rows = []
    for ref in d.get("evidence_used", []):
        if not svc.store.exists("evidence", ref):
            rows.append([ref, "MISSING", "", "", ""])
            continue
        e = svc.get("evidence", ref)
        srcs = [svc.get("sources", s) for s in e.get("sources", []) if svc.store.exists("sources", s)]
        rows.append([ref, e["statement"], "; ".join(f"{s['id']} ({s['tier']})" for s in srcs), "yes" if e.get("validated") else "indicative", e.get("attribution") or ""])
    return f"# Traceability — {d['id']} {d['title']}\n\n" + _t(rows, ["evidence", "claim", "sources", "validated", "attribution"])


def hypothesis_tree(svc, params: dict) -> str:
    hyps = svc.list("hypotheses")
    by_parent: dict[Optional[str], list[dict]] = {}
    for h in hyps:
        by_parent.setdefault(h.get("parent"), []).append(h)

    def walk(parent, depth) -> list[str]:
        out = []
        for h in by_parent.get(parent, []):
            out.append("  " * depth + f"- {h['id']} [{h['status']}, for {len(h.get('evidence_for') or [])}/against {len(h.get('evidence_against') or [])}] {h['statement']}")
            out += walk(h["id"], depth + 1)
        return out

    return "# Hypotheses\n\n" + "\n".join(walk(None, 0) or ["(none)"])


def appraisal_comparison(svc, params: dict) -> str:
    apps = [a for a in svc.list("appraisals") if a.get("status") in ("draft", "reviewed", "final")]
    dims = sorted({i["dimension"] for a in apps for i in a.get("impacts", [])})
    header = ["option", "kind", "method", "NPV (central)", "BCR", "MCA", "rank"] + dims
    rows = []
    for a in apps:
        opts = ", ".join(a.get("options", []))
        s = a.get("summary") or {}
        npv = (s.get("npv") or {}).get("central")
        by_dim = {i["dimension"]: i for i in a.get("impacts", [])}
        cells = []
        for d in dims:
            i = by_dim.get(d)
            if not i:
                cells.append("")
            elif i.get("quantified") and i.get("estimate"):
                est = i["estimate"]
                cells.append(f"{est.get('central')} {est.get('unit') or ''} [{est.get('low')}–{est.get('high')}]")
            else:
                cells.append(f"{i.get('rating')}")
        rows.append([opts, a["kind"], a["methodology"], npv, s.get("bcr"), s.get("mca_score"), s.get("rank")] + cells)
    return "# Appraisal comparison\n\n" + _t(rows, header)


def risk_register(svc, params: dict) -> str:
    rows = [[r["id"], r["scope"], r["likelihood"] * r["impact"], r["status"], r["owner"], r["description"], r.get("mitigation") or ""] for r in sorted(svc.list("risks"), key=lambda r: -(r["likelihood"] * r["impact"]))]
    return "# Risk register\n\n" + _t(rows, ["id", "scope", "score", "status", "owner", "risk", "mitigation"])


def status_note(svc, params: dict) -> str:
    eng = svc.engagement()
    since = params.get("since")
    decisions = svc.list("decisions", {"date": {"since": since}} if since else None)
    confirmed = [d for d in decisions if d["status"] == "confirmed"]
    proposed = [d for d in decisions if d["status"] == "proposed"]
    oqs = svc.list("open_questions", {"status": {"in": ["open", "awaiting_client"]}})
    actions = [a for a in svc.list("actions") if a["status"] in ("requested", "blocked")]
    risks = [r for r in svc.list("risks", {"status": {"in": ["open", "mitigating"]}}) if r["likelihood"] * r["impact"] >= 12]
    held = svc.list("meetings", {"status": "held"})
    lines = [f"# Weekly status — {eng.get('name')}", "", f"Phase {eng.get('phase')}. " + "Gates: " + ", ".join(f"{g} {s.get('status')}" for g, s in (eng.get("gates") or {}).items()), "", "## Progress", f"- Meetings held to date: {len(held)}", "", "## Decisions taken"] + [f"- {d['statement']} ({d['id']})" for d in confirmed] + ["", "## Decisions needed"] + [f"- {d['statement']} ({d['id']})" for d in proposed] + ["", "## Open questions by owner"] + [f"- {q['owner']}: {q['question']} ({q['priority']})" for q in oqs] + ["", "## Requests outstanding"] + [f"- {a['owner']}: {a['title']} (due {_fmt(a.get('due'))})" for a in actions] + ["", "## Risks to flag"] + [f"- {r['description']} (score {r['likelihood'] * r['impact']})" for r in risks] + ["", "## Next week", "- (Principal to complete from the workplan)"]
    return "\n".join(lines)


def meeting_plan(svc, params: dict) -> str:
    m = svc.get("meetings", params["meeting"])
    lines = [f"# Meeting plan — {m['title']} ({m['id']})", f"Kind {m['kind']} · conduct {m['conduct_mode']} · status {m['status']} · scheduled {_fmt(m.get('scheduled_at'))}", "", "## Participants"]
    for p in m.get("participants", []):
        s = svc.get("stakeholders", p["stakeholder"]) if p.get("stakeholder") and svc.store.exists("stakeholders", p["stakeholder"]) else {}
        lines.append(f"- {p.get('name') or s.get('name')} ({p['role']}): stance {s.get('stance', '?')}, influence {s.get('influence', '?')}; concerns: {', '.join(s.get('concerns') or []) or '—'}")
    lines += ["", "## Objectives"] + [f"- {o}" for o in m.get("objectives", [])]
    lines += ["", "## Hypotheses to test"] + [f"- {h}: {svc.get('hypotheses', h)['statement']}" for h in m.get("hypotheses_to_test", []) if svc.store.exists("hypotheses", h)]
    lines += ["", "## Open questions to close"] + [f"- {q}: {svc.get('open_questions', q)['question']}" for q in m.get("open_questions_to_close", []) if svc.store.exists("open_questions", q)]
    plan = m.get("plan") or {}
    lines += ["", "## Question guide"] + [f"{i + 1}. [P{q.get('priority')}] {q['question']}" + (f" — tests {', '.join(q.get('tests') or [])}" if q.get("tests") else "") for i, q in enumerate(plan.get("question_guide", []))]
    lines += ["", "## Disclosure and consent", plan.get("disclosure_script") or "(not set)", f"Attribution rule: {plan.get('attribution_rule')}", "", "## Sensitivities and do-not-say"] + [f"- {x}" for x in (plan.get("sensitivities", []) + plan.get("do_not_say", []))]
    lines += ["", f"Approval: {plan.get('approval') or 'not requested'}"]
    return "\n".join(lines)


def interview_debrief(svc, params: dict) -> str:
    m = svc.get("meetings", params["meeting"])
    rec = m.get("interview_record") or {}
    live = m.get("live") or {}
    lines = [f"# Interview debrief — {m['title']} ({m['id']})", f"Coverage {live.get('coverage', {}).get('asked', 0)}/{live.get('coverage', {}).get('total', 0)} · interventions {len(live.get('supervisor_interventions') or [])} · consent {'given' if (m.get('consent') or {}).get('ai_participant') else 'not recorded'}", "", "## Positions"]
    lines += [f"- {t['topic']}: {t['position']}" + (f" ({t['evidence']})" if t.get("evidence") else "") for t in rec.get("topics", [])]
    lines += ["", "## Reactions to options"] + [f"- {r['option']}: {r['reaction']}" for r in rec.get("reaction_to_options", [])]
    lines += ["", "## Contradictions with hypotheses"] + [f"- {c['hypothesis']}: {c['note']}" for c in rec.get("contradictions", [])]
    lines += ["", "## Documents promised / shared / directives"] + [f"- promised: {x}" for x in rec.get("documents_promised", [])] + [f"- shared: {x}" for x in rec.get("documents_shared", [])] + [f"- directive: {x}" for x in rec.get("directives_received", [])]
    lines += ["", "## Follow-ups"] + [f"- {x}" for x in rec.get("follow_ups", [])]
    pu = rec.get("proposed_updates") or {}
    lines += ["", "## Proposed updates (confirm before they apply)", f"- stakeholder patch: {pu.get('stakeholder_patch') or '{}'}", f"- hypothesis patches: {len(pu.get('hypothesis_patches') or [])}", f"- confirmed: {pu.get('confirmed_at') or 'no'}"]
    return "\n".join(lines)


def timeline(svc, params: dict) -> str:
    wp = svc.store.read("workplan") if svc.store.exists("workplan") else {}
    lines = ["```mermaid", "gantt", "  dateFormat YYYY-MM-DD", "  title Workplan"]
    for ph in wp.get("phases", []):
        lines.append(f"  section {ph['id']} {ph['name']}")
        for a in [a for a in wp.get("activities", []) if a.get("phase") == ph["id"] and a.get("start") and a.get("end")]:
            lines.append(f"  {a['name'][:40]} :{a['id']}, {_fmt(a['start'])[:10]}, {_fmt(a['end'])[:10]}")
    lines.append("```")
    return "\n".join(lines)


VIEWS: dict[str, Callable] = {
    "status": status,
    "gate_checklist": gate_checklist,
    "approvals_queue": approvals_queue,
    "pathway_summary": pathway_summary,
    "stakeholder_matrix": stakeholder_matrix,
    "reaction_matrix": reaction_matrix,
    "decision_log": decision_log,
    "question_register": question_register,
    "action_tracker": action_tracker,
    "evidence_table": evidence_table,
    "bibliography": bibliography,
    "traceability": traceability,
    "hypothesis_tree": hypothesis_tree,
    "appraisal_comparison": appraisal_comparison,
    "risk_register": risk_register,
    "status_note": status_note,
    "meeting_plan": meeting_plan,
    "interview_debrief": interview_debrief,
    "timeline": timeline,
}


def render(svc, name: str, params: Optional[dict] = None) -> str:
    try:
        fn = VIEWS[name]
    except KeyError as exc:
        raise KeyError(f"unknown view {name!r}; available: {', '.join(sorted(VIEWS))}") from exc
    return fn(svc, params or {})
