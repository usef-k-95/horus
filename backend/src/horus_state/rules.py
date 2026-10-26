"""Integrity rules (STATE_SCHEMA.md §6): computed fields, write-time checks and validation findings."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator, Optional

from .models import PREFIXES
from .models.enums import ActionClass, AutonomyLevel, SourceTier

ID_PATTERN = re.compile(r"^(" + "|".join(sorted(PREFIXES.values(), key=len, reverse=True)) + r")-[0-9A-Za-z]{1,8}$")
PREFIX_TO_COLLECTION = {v: k for k, v in PREFIXES.items()}
TIER_ORDER = {t.value: i for i, t in enumerate(SourceTier)}  # A=0 … E=4

ALLOWED_RELS = {"supports", "contradicts", "affects", "cites", "about", "derived_from", "prep_for", "feedback_on", "fulfils", "blocks", "related", "attends", "documents", "schedules"}

# rule 26: which collections each actor family may create or update
WRITE_SCOPE: dict[str, set[str]] = {
    "principal": set(PREFIXES),
    "supervisor": set(PREFIXES),
    "system": set(PREFIXES),
    "meet": {"meetings", "documents", "communications"},
    "researcher": {"sources", "evidence", "analyses", "documents"},
    "analyst": {"appraisals", "assumptions", "risks", "analyses"},
    "producer": {"deliverables", "analyses"},
    "interviewer": {"meetings", "evidence", "open_questions", "actions", "documents", "client_inputs", "sources"},
}

RELEASE_CLASS_BY_TIER = {"T0": ActionClass.tier0_tier1_release, "T1": ActionClass.tier0_tier1_release, "T2": ActionClass.tier2_release, "T3": ActionClass.tier2_release}
EMAIL_CLASS_BY_CLASSIFICATION = {
    "client_pm": ActionClass.client_pm_email,
    "client_dm": ActionClass.decision_maker_email,
    "stakeholder": ActionClass.stakeholder_email,
    "scheduling": ActionClass.meeting_scheduling,
    "internal": ActionClass.state_write,
    "vendor": ActionClass.client_pm_email,
}


class RuleViolation(ValueError):
    def __init__(self, rule: int, message: str) -> None:
        super().__init__(f"rule {rule}: {message}")
        self.rule = rule


@dataclass
class Issue:
    rule: int
    severity: str  # error | warning | info
    collection: str
    record_id: str
    message: str

    def as_dict(self) -> dict:
        return {"rule": self.rule, "severity": self.severity, "collection": self.collection, "id": self.record_id, "message": self.message}


def actor_family(actor: str) -> str:
    return actor.split(":", 1)[0]


def check_write_scope(actor: str, collection: str) -> None:
    family = actor_family(actor)
    allowed = WRITE_SCOPE.get(family)
    if allowed is None:
        raise RuleViolation(26, f"unknown actor family {family!r}")
    if collection not in allowed:
        raise RuleViolation(26, f"actor {actor!r} may not write to {collection!r}")


def iter_refs(value: Any, path: str = "") -> Iterator[tuple[str, str]]:
    """Yield (path, id) for every string that looks like a record ID."""
    if isinstance(value, str):
        if ID_PATTERN.match(value):
            yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from iter_refs(v, f"{path}.{k}" if path else str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from iter_refs(v, f"{path}[{i}]")


def collection_of(record_id: str) -> Optional[str]:
    prefix = record_id.split("-", 1)[0]
    return PREFIX_TO_COLLECTION.get(prefix)


POSITION_KINDS = {"position", "quote"}
STATEMENT_SOURCE_TYPES = {"interview", "speech_or_statement", "social_media"}


def compute_evidence_fields(evidence: dict, sources: list[dict]) -> dict:
    """Rules 3 and 4: grade, independence count and validated are computed from the sources.
    A person's own statement (interview, speech, social media) is Tier A evidence of that person's
    position or words, but for an asserted fact it counts no better than Tier C until corroborated."""
    kind = evidence.get("kind")
    effective = []
    for src in sources:
        tier = src.get("tier")
        if not tier:
            continue
        if src.get("type") in STATEMENT_SOURCE_TYPES and kind not in POSITION_KINDS:
            tier = max(tier, "C", key=lambda t: TIER_ORDER.get(t, 9))  # cap at C (worse of the two)
        effective.append({**src, "tier": tier})
    tiers = [s["tier"] for s in effective]
    best = min(tiers, key=lambda t: TIER_ORDER.get(t, 9)) if tiers else None
    groups = {s.get("independence_group") for s in effective if s.get("independence_group")}
    strong_groups = {s.get("independence_group") for s in effective if s.get("independence_group") and TIER_ORDER.get(s["tier"], 9) <= TIER_ORDER["B"]}
    corroboration = evidence.get("corroboration", "single_source")
    validated = corroboration not in ("contested", "refuted") and (best == "A" or len(strong_groups) >= 2)
    return {"grade": best, "independence_count": len(groups), "validated": bool(validated)}


def release_action_class(tier: str) -> ActionClass:
    return RELEASE_CLASS_BY_TIER.get(tier, ActionClass.tier2_release)


def email_action_class(classification: str) -> ActionClass:
    return EMAIL_CLASS_BY_CLASSIFICATION.get(classification, ActionClass.client_pm_email)


def level_allows_without_approval(level: str) -> bool:
    return level in (AutonomyLevel.auto.value, AutonomyLevel.notify.value)


# ---- validation (V rules) ---------------------------------------------------------------

def validate_all(service) -> list[Issue]:
    issues: list[Issue] = []
    now = datetime.now(timezone.utc)
    engagement = service.engagement()
    records: dict[str, list[dict]] = {c: list(service.store.iter_records(c)) for c in PREFIXES}
    index: dict[str, dict] = {}
    for coll, items in records.items():
        for r in items:
            index[r["id"]] = r

    # dangling references (rule 2, as a sweep)
    for coll, items in records.items():
        for r in items:
            for path, ref in iter_refs(r):
                if ref == r.get("id"):
                    continue
                if ref not in index and collection_of(ref) is not None:
                    issues.append(Issue(2, "error", coll, r["id"], f"dangling reference {ref} at {path}"))

    # rule 4 recompute validated
    for ev in records["evidence"]:
        sources = [index[s] for s in ev.get("sources", []) if s in index]
        computed = compute_evidence_fields(ev, sources)
        if computed["validated"] != bool(ev.get("validated")):
            issues.append(Issue(4, "warning", "evidence", ev["id"], "stored validated flag differs from recomputation; reindex or update"))

    # rule 6 evidence used in T0/T1 deliverables must be validated
    for d in records["deliverables"]:
        if d.get("tier") in ("T0", "T1"):
            for ref in d.get("evidence_used", []):
                ev = index.get(ref)
                if ev is None:
                    issues.append(Issue(6, "error", "deliverables", d["id"], f"evidence {ref} referenced but missing"))
                elif not ev.get("validated"):
                    issues.append(Issue(6, "warning", "deliverables", d["id"], f"evidence {ref} used in a {d['tier']} deliverable is not validated; mark indicative"))

    # rule 10 stance basis
    for s in records["stakeholders"]:
        if s.get("stance") not in (None, "unknown") and not s.get("stance_basis") and s.get("stance_confidence") != "low":
            issues.append(Issue(10, "warning", "stakeholders", s["id"], "known stance without stance_basis or low confidence"))

    # rule 13 blocking open questions
    for q in records["open_questions"]:
        if q.get("status") in ("open", "awaiting_client") and q.get("blocking"):
            issues.append(Issue(13, "info", "open_questions", q["id"], f"blocks {', '.join(q['blocking'])}"))

    # rule 14 assumptions used in final appraisals must be agreed
    for a in records["appraisals"]:
        if a.get("status") == "final":
            used = {ref for imp in a.get("impacts", []) for ref in imp.get("assumptions", [])}
            for ref in used:
                asm = index.get(ref)
                if asm and asm.get("status") != "agreed":
                    issues.append(Issue(14, "warning", "appraisals", a["id"], f"assumption {ref} is {asm.get('status')} in a final appraisal"))

    # rule 15 client inputs without disposition before later versions
    for c in records["client_inputs"]:
        if c.get("disposition") == "pending" and c.get("status") == "open":
            issues.append(Issue(15, "info", "client_inputs", c["id"], "pending disposition"))

    # rule 16 snapshots for tiers A–C web sources
    for s in records["sources"]:
        if s.get("tier") in ("A", "B", "C") and s.get("url") and not (s.get("access") or {}).get("snapshot_path"):
            issues.append(Issue(16, "warning", "sources", s["id"], "no snapshot for a Tier A–C web source"))

    # rule 24 transcript verification and retention
    for m in records["meetings"]:
        t = m.get("transcript") or {}
        if t.get("path") and not t.get("verified_at"):
            held = m.get("held_at")
            if held:
                held_dt = held if isinstance(held, datetime) else datetime.fromisoformat(str(held))
                if held_dt.tzinfo is None:
                    held_dt = held_dt.replace(tzinfo=timezone.utc)
                if now - held_dt > timedelta(days=2):
                    issues.append(Issue(24, "warning", "meetings", m["id"], "transcript unverified more than two days after the meeting"))
        rec = m.get("recording") or {}
        if rec.get("path") and rec.get("retention_until") and not rec.get("deleted_at"):
            until = rec["retention_until"]
            until_d = until if hasattr(until, "year") else datetime.fromisoformat(str(until)).date()
            if until_d < now.date():
                issues.append(Issue(24, "error", "meetings", m["id"], "recording retention expired but file not deleted"))

    # rule 19 pathway before AP1
    gates = engagement.get("gates", {})
    if gates.get("AP1", {}).get("status") == "passed" and not (engagement.get("pathway") or {}).get("primary"):
        issues.append(Issue(19, "error", "engagement", engagement["id"], "AP1 passed without a primary pathway"))

    return issues
