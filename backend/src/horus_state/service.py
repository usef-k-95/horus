"""High-level API over the store: validated create and update, specialised operations that
enforce rules on the way in, approvals and autonomy, gates and phases, checkpoints, validation."""

from __future__ import annotations

import copy
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from . import SCHEMA_VERSION
from .gates import all_checklists, compute_checklist
from .models import COLLECTIONS, PREFIXES, SINGLETONS, model_for
from .models.common import SERVER_FIELDS
from .models.enums import ActionClass, ApprovalStatus, AutonomyLevel, EventOp, Gate, Phase
from .models.records import (
    DEFAULT_AUTONOMY,
    SHADOW_AUTONOMY,
    Approval,
    ApprovalTarget,
    CheckpointBody,
    Client,
    Dates,
    DeliverableVersion,
    Engagement,
    Event,
    PathwayInfo,
    QAResult,
    ReviewResult,
    Team,
)
from .rules import (
    ALLOWED_RELS,
    RuleViolation,
    actor_family,
    check_write_scope,
    collection_of,
    compute_evidence_fields,
    email_action_class,
    iter_refs,
    level_allows_without_approval,
    release_action_class,
    validate_all,
)
from .store import NotFound, Store, StoreError, file_hash, utcnow

COMPUTED_FIELDS = {"evidence": {"grade", "independence_count", "validated", "used_in"}, "assumptions": {"used_in"}, "analyses": {"used_in"}, "deliverables": {"evidence_used"}}
GATE_ORDER = [g.value for g in Gate]
PHASE_ORDER = [p.value for p in Phase if p != Phase.closed]
PHASE_GATE = {"P1": "AP0", "P2": "AP1", "P3": "AP2", "P4": "AP3", "P5": "AP4", "closed": "AP5"}


def deep_merge(base: dict, patch: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _diff(before: dict, after: dict) -> dict:
    changed = {}
    for key in sorted(set(before) | set(after)):
        if key in ("updated_at", "updated_by"):
            continue
        if before.get(key) != after.get(key):
            changed[key] = {"before": _short(before.get(key)), "after": _short(after.get(key))}
    return changed


def _short(value: Any, limit: int = 160) -> Any:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _dump(model) -> dict:
    return model.model_dump(mode="python", by_alias=True)


class Service:
    def __init__(self, workspace: Path | str, actor: str = "principal", session_id: Optional[str] = None) -> None:
        self.store = Store(Path(workspace))
        self.actor = actor
        self.session_id = session_id or os.environ.get("HORUS_SESSION_ID") or uuid.uuid4().hex[:12]

    # =====================================================================================
    # engagement lifecycle
    # =====================================================================================
    def init_engagement(
        self,
        code: str,
        name: str,
        client: dict,
        *,
        pathway_primary: Optional[str] = None,
        supervisors: Iterable[str] = (),
        languages: Iterable[str] = ("en",),
        currency: str = "USD",
        price_base_year: Optional[int] = None,
        received: Optional[str] = None,
        policy_domain: Iterable[str] = (),
    ) -> dict:
        if self.store.initialised:
            raise StoreError(f"an engagement already exists at {self.store.root}")
        self.store.scaffold()
        now = utcnow()
        eng = Engagement(
            id="ENG-001",
            created_at=now,
            updated_at=now,
            created_by=self.actor,
            updated_by=self.actor,
            session_id=self.session_id,
            status="active",
            code=code,
            name=name,
            client=Client(**client),
            policy_domain=list(policy_domain),
            pathway=PathwayInfo(primary=pathway_primary) if pathway_primary else PathwayInfo(),
            languages=list(languages),
            currency=currency,
            price_base_year=price_base_year or now.year,
            team=Team(supervisors=list(supervisors)),
            dates=Dates(received=datetime.fromisoformat(received).date() if received else now.date()),
            schema_version=SCHEMA_VERSION,
        )
        record = _dump(eng)
        self.store.write(record)
        self._event(EventOp.create, "engagement", "ENG-001", f"engagement {code} initialised")
        return self.engagement()

    def engagement(self) -> dict:
        eng = self.store.read("engagement")
        eng["counters"] = self.store.counters()
        return eng

    # =====================================================================================
    # generic reads
    # =====================================================================================
    def get(self, collection: str, record_id: Optional[str] = None, expand: bool = False) -> dict:
        model_for(collection)
        record = self.store.read(collection, None if collection in SINGLETONS else record_id)
        if expand:
            record["_expanded"] = self._expand(record)
        return record

    def _expand(self, record: dict) -> dict:
        out = {}
        for _, ref in iter_refs({k: v for k, v in record.items() if k not in ("id", "links")}):
            if ref in out or ref == record.get("id"):
                continue
            coll = collection_of(ref)
            if coll and self.store.exists(coll, None if coll in SINGLETONS else ref):
                target = self.store.read(coll, None if coll in SINGLETONS else ref)
                label = target.get("title") or target.get("name") or target.get("statement") or target.get("summary") or target.get("question") or ""
                out[ref] = {"collection": coll, "label": _short(label, 100), "status": target.get("status")}
        return out

    def list(self, collection: str, filter: Optional[dict] = None, fields: Optional[list[str]] = None, limit: int = 200, sort: Optional[str] = None) -> list[dict]:
        model_for(collection)
        records = list(self.store.iter_records(collection))
        for key, cond in (filter or {}).items():
            records = [r for r in records if self._match(self._dig(r, key), cond)]
        if sort:
            reverse = sort.startswith("-")
            key = sort.lstrip("-")
            records.sort(key=lambda r: str(self._dig(r, key) or ""), reverse=reverse)
        records = records[:limit]
        if fields:
            keep = set(fields) | {"id", "collection", "status"}
            records = [{k: v for k, v in r.items() if k in keep} for r in records]
        return records

    @staticmethod
    def _dig(record: dict, dotted: str) -> Any:
        node: Any = record
        for part in dotted.split("."):
            if isinstance(node, dict):
                node = node.get(part)
            else:
                return None
        return node

    @staticmethod
    def _match(value: Any, cond: Any) -> bool:
        if isinstance(cond, dict):
            if "in" in cond:
                return value in cond["in"]
            if "since" in cond:
                return value is not None and str(value) >= str(cond["since"])
            if "contains" in cond:
                return cond["contains"] in (value or [])
            if "not" in cond:
                return value != cond["not"]
        return value == cond

    def search(self, query: str, collections: Optional[list[str]] = None, limit: int = 20) -> list[dict]:
        return self.store.search(query, collections, limit)

    # =====================================================================================
    # generic writes
    # =====================================================================================
    def create(self, collection: str, record: dict, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        model_for(collection)
        check_write_scope(actor, collection)
        if collection in SINGLETONS and self.store.exists(collection):
            raise StoreError(f"{collection} already exists; use update")
        if collection == "approvals" and record.get("status") not in (None, "pending", "not_required"):
            raise RuleViolation(25, "approvals are created pending; decide them with decide_approval")
        data = {k: v for k, v in record.items() if k not in SERVER_FIELDS}
        now = utcnow()
        data.update(
            id=self.store.next_id(collection) if collection not in SINGLETONS else f"{PREFIXES[collection]}-001",
            collection=collection,
            created_at=now,
            updated_at=now,
            created_by=actor,
            updated_by=actor,
            session_id=self.session_id,
            schema_version=SCHEMA_VERSION,
        )
        prepared = self._prepare(collection, data, previous=None, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.create, collection, prepared["id"], self._summary(prepared), actor=actor)
        return prepared

    def update(self, collection: str, record_id: Optional[str], patch: dict, reason: Optional[str] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        model_for(collection)
        check_write_scope(actor, collection)
        current = self.store.read(collection, None if collection in SINGLETONS else record_id)
        forbidden = (set(patch) & (SERVER_FIELDS - {"session_id"})) | (set(patch) & COMPUTED_FIELDS.get(collection, set()))
        if forbidden and actor_family(actor) != "system":
            raise RuleViolation(3, f"cannot set server-managed fields {sorted(forbidden)}")
        if collection == "approvals" and current.get("status") != "pending":
            raise RuleViolation(25, "a decided approval is immutable; create a new request")
        if collection == "engagement" and ({"gates", "phase"} & set(patch)) and actor_family(actor) != "system":
            raise RuleViolation(8, "use set_gate and set_phase for gate and phase transitions")
        if collection == "deliverables" and "versions" in patch and actor_family(actor) != "system":
            raise RuleViolation(5, "use register_version and release_version to change versions")
        merged = deep_merge(current, patch)
        merged["updated_at"] = utcnow()
        merged["updated_by"] = actor
        prepared = self._prepare(collection, merged, previous=current, actor=actor)
        if collection in SINGLETONS and prepared.get("version", 0) > current.get("version", 0):
            self.store.snapshot(collection)
        self.store.write(prepared)
        self._event(EventOp.update, collection, prepared["id"], self._summary(prepared), diff=_diff(current, prepared), reason=reason, actor=actor)
        return prepared

    def append(self, collection: str, record_id: str, field_name: str, items: list, actor: Optional[str] = None) -> dict:
        current = self.store.read(collection, record_id)
        existing = list(current.get(field_name) or [])
        for item in items:
            if item not in existing:
                existing.append(item)
        return self.update(collection, record_id, {field_name: existing}, actor=actor)

    def _prepare(self, collection: str, data: dict, previous: Optional[dict], actor: str) -> dict:
        model = model_for(collection).model_validate(data)
        record = _dump(model)
        if collection == "evidence":
            sources = [self.store.read("sources", s) for s in record.get("sources", []) if self.store.exists("sources", s)]
            record.update(compute_evidence_fields(record, sources))
            if record.get("meeting") and not record.get("attribution"):
                raise RuleViolation(23, "interview-sourced evidence needs an attribution rule")
        self._check_refs(record)
        self._check_transitions(collection, previous or {}, record)
        return record

    def _check_refs(self, record: dict) -> None:
        for path, ref in iter_refs({k: v for k, v in record.items() if k != "id"}):
            coll = collection_of(ref)
            if coll is None or ref == record.get("id"):
                continue
            if not self.store.exists(coll, None if coll in SINGLETONS else ref):
                raise RuleViolation(2, f"{path} refers to {ref}, which does not exist")

    def _check_transitions(self, collection: str, before: dict, after: dict) -> None:
        if collection == "communications" and after.get("direction") == "outbound" and after.get("status") == "sent" and before.get("status") != "sent":
            klass = after.get("action_class") or email_action_class(after.get("classification", "client_pm")).value
            if not level_allows_without_approval(self.autonomy_level(klass)):
                approval = after.get("approval") and self.store.exists("approvals", after["approval"]) and self.store.read("approvals", after["approval"])
                if not approval or approval.get("status") != "approved":
                    raise RuleViolation(12, "an outbound communication needs an approved approval before it is sent")
        if collection == "meetings":
            status = after.get("status")
            if status in ("joining", "in_progress") and before.get("status") not in ("joining", "in_progress", "held"):
                plan = after.get("plan") or {}
                if not after.get("conduct_mode") or not (plan.get("disclosure_script") or plan.get("disclosure_script_id")):
                    raise RuleViolation(21, "a meeting cannot be joined without a conduct mode and a plan with a disclosure script")
                if after.get("conduct_mode") != "human" and not level_allows_without_approval(self.autonomy_level(ActionClass.interview_plan.value)):
                    approval = plan.get("approval") and self.store.exists("approvals", plan["approval"]) and self.store.read("approvals", plan["approval"])
                    if not approval or approval.get("status") != "approved":
                        raise RuleViolation(21, "the meeting plan needs an approved approval before joining")
            if status == "in_progress" and before.get("status") != "in_progress":
                consent = after.get("consent") or {}
                if not (consent.get("ai_participant") and consent.get("given_at")):
                    raise RuleViolation(22, "a meeting cannot move to in_progress before consent is recorded")
                if consent.get("recording") is False and after.get("recording"):
                    raise RuleViolation(22, "recording consent was refused but a recording block exists")

    # =====================================================================================
    # links and deletion
    # =====================================================================================
    def link(self, from_id: str, to_id: str, rel: str, actor: Optional[str] = None) -> dict:
        if rel not in ALLOWED_RELS:
            raise RuleViolation(2, f"relation {rel!r} is not allowed; use one of {sorted(ALLOWED_RELS)}")
        coll = collection_of(from_id)
        if coll is None:
            raise RuleViolation(2, f"{from_id} is not a record id")
        current = self.store.read(coll, None if coll in SINGLETONS else from_id)
        links = list(current.get("links") or [])
        entry = {"rel": rel, "to": to_id}
        if entry not in links:
            links.append(entry)
        return self.update(coll, from_id, {"links": links}, actor=actor)

    def delete(self, collection: str, record_id: str, reason: str, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        if not reason:
            raise RuleViolation(18, "a reason is required")
        current = self.store.read(collection, record_id)
        if collection == "profiles":
            if actor_family(actor) not in ("supervisor", "principal", "system"):
                raise RuleViolation(26, "only the Supervisor or Principal may delete a profile")
            self.store.path_for(collection, record_id).unlink()
            self._event(EventOp.delete, collection, record_id, "profile hard-deleted", reason=reason, actor=actor)
            return {"id": record_id, "deleted": True}
        soft_status = {"evidence": "withdrawn", "sources": "superseded", "stakeholders": "inactive", "options": "rejected"}.get(collection, "superseded")
        try:
            return self.update(collection, record_id, {"status": soft_status}, reason=reason, actor=actor)
        except Exception:
            self._event(EventOp.delete, collection, record_id, f"soft delete requested (status {soft_status} not valid for this record)", reason=reason, actor=actor)
            return current

    # =====================================================================================
    # specialised operations
    # =====================================================================================
    def import_document(self, path: str | Path, metadata: dict, destination: str = "inbox", actor: Optional[str] = None) -> dict:
        src = Path(path)
        if not src.exists():
            raise StoreError(f"{src} does not exist")
        doc_id = self.store.next_id("documents")
        folder = self.store.workspace / destination
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / f"{doc_id}__{src.name}"
        shutil.copy2(src, target)
        record = {
            "title": metadata.get("title") or src.stem,
            "kind": metadata.get("kind", "other"),
            "origin": metadata.get("origin", "client"),
            "received_via": metadata.get("received_via"),
            "received_on": metadata.get("received_on") or utcnow().date(),
            "document_date": metadata.get("document_date"),
            "issuer": metadata.get("issuer"),
            "path": str(target.relative_to(self.store.workspace)),
            "hash": file_hash(target),
            "language": metadata.get("language"),
            "summary": metadata.get("summary"),
            "confidentiality": metadata.get("confidentiality", "client-confidential"),
            "status": "active",
        }
        if metadata.get("source"):
            source = self.create("sources", metadata["source"], actor=actor)
            record["source"] = source["id"]
        # the id was already reserved; create() would allocate a second one, so write directly
        actor = actor or self.actor
        check_write_scope(actor, "documents")
        now = utcnow()
        record.update(id=doc_id, collection="documents", created_at=now, updated_at=now, created_by=actor, updated_by=actor, session_id=self.session_id, schema_version=SCHEMA_VERSION)
        prepared = self._prepare("documents", record, previous=None, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.import_, "documents", doc_id, f"imported {src.name} into {destination}/", actor=actor)
        return prepared

    def register_version(self, deliverable_id: str, paths: dict, change_summary: str, qa: dict, review: Optional[dict] = None, based_on_feedback: Iterable[str] = (), actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        check_write_scope(actor, "deliverables")
        current = self.store.read("deliverables", deliverable_id)
        v = int(current.get("current_version", 0)) + 1
        first = next((p for p in paths.values() if p), None)
        file_path = self.store.workspace / first if first else None
        digest = file_hash(file_path) if file_path and file_path.exists() else None
        qa_result = QAResult(**qa)
        version = DeliverableVersion(
            v=v,
            paths=paths,
            hash=digest,
            created_at=utcnow(),
            created_by=actor,
            change_summary=change_summary,
            based_on_feedback=list(based_on_feedback),
            qa=qa_result,
            review=ReviewResult(**(review or {})),
            status="qa_passed" if qa_result.all_pass() else "qa_failed",
        )
        versions = list(current.get("versions") or []) + [_dump(version)]
        merged = deep_merge(current, {"versions": versions, "current_version": v, "status": "in_progress", "updated_at": utcnow(), "updated_by": actor})
        prepared = self._prepare("deliverables", merged, previous=current, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.update, "deliverables", deliverable_id, f"version {v} registered ({version.status})", actor=actor)
        return prepared

    def release_version(self, deliverable_id: str, v: int, sent_in: Optional[str] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        current = self.store.read("deliverables", deliverable_id)
        versions = list(current.get("versions") or [])
        target = next((x for x in versions if x.get("v") == v), None)
        if target is None:
            raise NotFound(f"{deliverable_id} has no version {v}")
        qa = QAResult(**{k: val for k, val in (target.get("qa") or {}).items()})
        if not qa.all_pass():
            raise RuleViolation(5, "QA audits have not all passed")
        if not (target.get("review") or {}).get("resolved"):
            raise RuleViolation(5, "partner review is not resolved")
        klass = release_action_class(current.get("tier", "T2")).value
        if not level_allows_without_approval(self.autonomy_level(klass)):
            approval = self.approval_for("deliverables", deliverable_id, version=v)
            if approval is None:
                raise RuleViolation(5, f"release needs an approved approval (action class {klass})")
            target["approval"] = approval["id"]
        target["status"] = "sent" if sent_in else "supervisor_approved"
        if sent_in:
            target["sent_in"] = sent_in
        merged = deep_merge(current, {"versions": versions, "status": "delivered" if sent_in else current.get("status"), "updated_at": utcnow(), "updated_by": actor})
        prepared = self._prepare("deliverables", merged, previous=current, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.update, "deliverables", deliverable_id, f"version {v} {target['status']}", actor=actor)
        return prepared

    # ---- autonomy and approvals ------------------------------------------------------------
    def autonomy_level(self, action_class: str) -> str:
        levels = ((self.store.read("engagement").get("settings") or {}).get("autonomy") or {}).get("levels") or {}
        return str(levels.get(action_class, DEFAULT_AUTONOMY.get(action_class, AutonomyLevel.approve.value)))

    def set_autonomy(self, profile: Optional[str] = None, levels: Optional[dict] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        if actor_family(actor) not in ("supervisor", "system"):
            raise RuleViolation(26, "only a Supervisor may change autonomy settings")
        current = self.store.read("engagement")
        new_levels = dict(((current.get("settings") or {}).get("autonomy") or {}).get("levels") or DEFAULT_AUTONOMY)
        if profile == "default":
            new_levels = dict(DEFAULT_AUTONOMY)
        elif profile == "shadow":
            new_levels = dict(SHADOW_AUTONOMY)
        if levels:
            new_levels.update({str(k): str(v) for k, v in levels.items()})
            profile = profile or "custom"
        patch = {"settings": {"autonomy": {"profile": profile or (current.get("settings") or {}).get("autonomy", {}).get("profile", "custom"), "levels": new_levels}}}
        return self.update("engagement", None, patch, reason="autonomy change", actor=actor)

    def request_approval(self, target: dict, action_class: str, summary: str, risk_class: Optional[str] = None, expires_at: Optional[datetime] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        level = self.autonomy_level(action_class)
        status = ApprovalStatus.not_required.value if level_allows_without_approval(level) else ApprovalStatus.pending.value
        risk = risk_class or ("high" if action_class in (ActionClass.tier0_tier1_release.value, ActionClass.decision_maker_email.value, ActionClass.gate_transition.value) else "medium")
        record = {
            "target": target,
            "action_class": action_class,
            "risk_class": risk,
            "summary": summary,
            "requested_by": actor,
            "requested_at": utcnow(),
            "autonomy_level_at_request": level,
            "status": status,
            "expires_at": expires_at,
            "note": "human performs this action; Horus prepared it" if level == AutonomyLevel.human.value else None,
        }
        approval = self.create("approvals", record, actor=actor)
        self._event(EventOp.approval, "approvals", approval["id"], f"{status}: {summary}", actor=actor)
        return approval

    def decide_approval(self, approval_id: str, decision: str, note: Optional[str] = None, conditions: Iterable[str] = (), actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        if actor_family(actor) not in ("supervisor", "system"):
            raise RuleViolation(26, "only a Supervisor may decide approvals")
        current = self.store.read("approvals", approval_id)
        if current.get("status") != "pending":
            raise RuleViolation(25, f"approval {approval_id} is already {current.get('status')}")
        if decision not in ("approved", "rejected"):
            raise ValueError("decision must be approved or rejected")
        merged = deep_merge(current, {"status": decision, "decided_by": actor, "decided_at": utcnow(), "note": note, "conditions": list(conditions), "updated_at": utcnow(), "updated_by": actor})
        prepared = self._prepare("approvals", merged, previous=current, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.approval, "approvals", approval_id, f"{decision} by {actor}: {current.get('summary')}", reason=note, actor=actor)
        if decision == "approved":
            self._apply_approval(prepared)
        return prepared

    def _apply_approval(self, approval: dict) -> None:
        target = approval.get("target") or {}
        coll, tid = target.get("collection"), target.get("id")
        if coll == "communications" and self.store.exists(coll, tid):
            current = self.store.read(coll, tid)
            if current.get("status") in ("draft", "pending_approval"):
                self.update(coll, tid, {"status": "approved", "approval": approval["id"]}, actor="system")
        elif coll == "meetings" and self.store.exists(coll, tid):
            current = self.store.read(coll, tid)
            if current.get("plan") is not None:
                self.update(coll, tid, {"plan": {"approval": approval["id"]}}, actor="system")
            if approval.get("action_class") == ActionClass.meeting_scheduling.value:
                self.update(coll, tid, {"scheduling": {"approval": approval["id"]}}, actor="system")

    def approval_for(self, collection: str, record_id: str, version: Optional[int] = None, action_class: Optional[str] = None) -> Optional[dict]:
        now = utcnow()
        best = None
        for a in self.store.iter_records("approvals"):
            t = a.get("target") or {}
            if t.get("collection") != collection or t.get("id") != record_id:
                continue
            if version is not None and t.get("version") not in (None, version):
                continue
            if action_class and a.get("action_class") != action_class:
                continue
            if a.get("status") != "approved":
                continue
            exp = a.get("expires_at")
            if exp:
                exp_dt = exp if isinstance(exp, datetime) else datetime.fromisoformat(str(exp))
                if exp_dt.tzinfo is None:
                    exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                if exp_dt < now:
                    continue
            best = a
        return best

    def pending_approvals(self) -> list[dict]:
        return [a for a in self.store.iter_records("approvals") if a.get("status") == "pending"]

    # ---- gates and phases ----------------------------------------------------------------
    def gate_checklist(self, gate: str) -> dict:
        return compute_checklist(self, gate).as_dict()

    def set_gate(self, gate: str, status: str, decision_id: Optional[str] = None, override_reason: Optional[str] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        if gate not in GATE_ORDER:
            raise ValueError(f"unknown gate {gate}")
        eng = self.store.read("engagement")
        overrides: list[str] = []
        if status == "passed":
            if not decision_id:
                raise RuleViolation(8, "passing a gate needs a confirmed gate decision")
            decision = self.store.read("decisions", decision_id)
            if decision.get("kind") != "gate" or decision.get("status") != "confirmed" or decision.get("gate") != gate:
                raise RuleViolation(8, f"{decision_id} is not a confirmed gate decision for {gate}")
            if gate == "AP1" and not (eng.get("pathway") or {}).get("primary"):
                raise RuleViolation(19, "AP1 cannot pass without a primary pathway")
            if not level_allows_without_approval(self.autonomy_level(ActionClass.gate_transition.value)):
                if self.approval_for("engagement", "ENG-001", action_class=ActionClass.gate_transition.value) is None:
                    raise RuleViolation(8, "gate transition needs an approved approval")
            checklist = compute_checklist(self, gate)
            unsatisfied = [c.description for c in checklist.criteria if not c.satisfied]
            if unsatisfied and not override_reason:
                raise RuleViolation(8, "criteria unsatisfied: " + "; ".join(unsatisfied))
            overrides = unsatisfied
        gates = dict(eng.get("gates") or {})
        gates[gate] = {"status": status, "passed_in": decision_id if status == "passed" else None, "passed_at": utcnow() if status == "passed" else None}
        merged = deep_merge(eng, {"gates": gates, "updated_at": utcnow(), "updated_by": actor})
        prepared = self._prepare("engagement", merged, previous=eng, actor=actor)
        self.store.write(prepared)
        summary = f"gate {gate} → {status}" + (f" with overrides: {'; '.join(overrides)}" if overrides else "")
        self._event(EventOp.gate_change, "engagement", "ENG-001", summary, reason=override_reason, actor=actor)
        return prepared

    def set_phase(self, phase: str, override_reason: Optional[str] = None, actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        eng = self.store.read("engagement")
        required_gate = PHASE_GATE.get(phase)
        if required_gate and (eng.get("gates") or {}).get(required_gate, {}).get("status") != "passed":
            if not override_reason:
                raise RuleViolation(9, f"phase {phase} requires gate {required_gate} to be passed")
        merged = deep_merge(eng, {"phase": phase, "updated_at": utcnow(), "updated_by": actor})
        prepared = self._prepare("engagement", merged, previous=eng, actor=actor)
        self.store.write(prepared)
        self._event(EventOp.phase_change, "engagement", "ENG-001", f"phase {eng.get('phase')} → {phase}", reason=override_reason, actor=actor)
        return prepared

    # ---- checkpoints and interventions -----------------------------------------------------
    def checkpoint(self, done: Iterable[str] = (), decided: Iterable[str] = (), learned: Iterable[str] = (), next: Iterable[str] = (), blockers: Iterable[str] = (), actor: Optional[str] = None) -> dict:
        actor = actor or self.actor
        eng = self.store.read("engagement")
        body = CheckpointBody(done=list(done), decided=list(decided), learned=list(learned), next=list(next), blockers=list(blockers), phase=eng.get("phase"), gates={g: (s or {}).get("status", "not_ready") for g, s in (eng.get("gates") or {}).items()})
        event = self._event(EventOp.checkpoint, None, None, "checkpoint: " + (list(done)[0] if done else "session"), checkpoint=body, actor=actor)
        merged = deep_merge(eng, {"last_checkpoint": event["id"], "updated_at": utcnow(), "updated_by": actor})
        self.store.write(_dump(model_for("engagement").model_validate(merged)))
        return event

    def last_checkpoint(self) -> Optional[dict]:
        last = None
        for ev in self.store.iter_events():
            if ev.get("op") == "checkpoint":
                last = ev
        return last

    def record_intervention(self, meeting_id: str, kind: str, text: Optional[str] = None, by: str = "supervisor") -> dict:
        current = self.store.read("meetings", meeting_id)
        live = current.get("live") or {}
        interventions = list(live.get("supervisor_interventions") or []) + [{"type": kind, "at": utcnow(), "text": text, "by": by}]
        updated = self.update("meetings", meeting_id, {"live": {**live, "supervisor_interventions": interventions}}, actor="meet")
        self._event(EventOp.intervention, "meetings", meeting_id, f"{kind}: {text or ''}".strip(), actor=f"supervisor:{by}" if by != "supervisor" else "supervisor")
        return updated

    # ---- validation, status, export -------------------------------------------------------
    def validate(self, scope: str = "all") -> list[dict]:
        issues = validate_all(self)
        if scope != "all":
            issues = [i for i in issues if i.collection == scope]
        self._event(EventOp.validate, None, None, f"validate {scope}: {len(issues)} issue(s)")
        return [i.as_dict() for i in issues]

    def gates(self) -> dict:
        return all_checklists(self)

    def export(self, include_profiles: bool = False) -> dict:
        out = {"schema_version": SCHEMA_VERSION, "exported_at": utcnow().isoformat(), "collections": {}}
        for coll in COLLECTIONS:
            if coll == "profiles" and not include_profiles:
                continue
            out["collections"][coll] = list(self.store.iter_records(coll))
        out["events"] = sum(1 for _ in self.store.iter_events())
        self._event(EventOp.export, None, None, f"export (profiles {'included' if include_profiles else 'excluded'})")
        return out

    # =====================================================================================
    # events
    # =====================================================================================
    def _event(self, op: EventOp, collection: Optional[str], record_id: Optional[str], summary: str, *, diff: Optional[dict] = None, reason: Optional[str] = None, checkpoint: Optional[CheckpointBody] = None, actor: Optional[str] = None) -> dict:
        event = Event(id=self.store.new_event_id(), ts=utcnow(), actor=actor or self.actor, session_id=self.session_id, op=op, collection=collection, record_id=record_id, summary=summary, diff=diff or None, reason=reason, checkpoint=checkpoint)
        self.store.append_event(event)
        return event.model_dump(mode="json")

    @staticmethod
    def _summary(record: dict) -> str:
        label = record.get("title") or record.get("name") or record.get("statement") or record.get("summary") or record.get("question") or record.get("code") or ""
        return _short(f"{record.get('collection')} {record.get('id')}: {label}", 200)
