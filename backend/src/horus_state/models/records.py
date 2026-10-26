"""Record models for every collection (STATE_SCHEMA.md §3). Reference fields hold ID strings."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal, Optional

from pydantic import Field, field_validator, model_validator

from .common import Envelope, StrictModel
from .enums import (
    ActionClass,
    ActionKind,
    ActionStatus,
    AnalysisKind,
    AppraisalKind,
    ApprovalStatus,
    Attribution,
    AutonomyLevel,
    Channel,
    ClientInputKind,
    ClientRole,
    Confidence,
    Confidentiality,
    Corroboration,
    DecisionKind,
    DecisionRole,
    DecisionStatus,
    DeliverableStatus,
    DeliverableTier,
    DeliverableVersionStatus,
    Direction,
    EventOp,
    EvidenceKind,
    Gate,
    GateStatus,
    HypothesisStatus,
    ImpactDimension,
    InstrumentType,
    MeetingKind,
    MeetingStatus,
    Methodology,
    OpenQuestionStatus,
    OptionKind,
    OptionStatus,
    Pathway,
    Phase,
    Priority,
    Reaction,
    RelationshipType,
    RiskClass,
    SourceTier,
    SourceType,
    StakeholderCategory,
    StakeholderKind,
    Stance,
    ConductMode,
)

Ref = str

# =====================================================================================
# A. Scope and plan
# =====================================================================================


class Client(StrictModel):
    entity: str
    acronym: Optional[str] = None
    country: str
    level: Literal["national", "subnational", "supranational"] = "national"
    sector: Optional[str] = None


class PathwayRevision(StrictModel):
    date: date
    previous: Pathway
    new: Pathway
    decision: Optional[Ref] = None


class PathwayInfo(StrictModel):
    primary: Optional[Pathway] = None
    secondary: list[Pathway] = Field(default_factory=list)
    rationale: Optional[str] = None
    classified_in: Optional[Ref] = None
    confirmed_in: Optional[Ref] = None
    revisions: list[PathwayRevision] = Field(default_factory=list)


class GateState(StrictModel):
    status: GateStatus = GateStatus.not_ready
    passed_in: Optional[Ref] = None
    passed_at: Optional[datetime] = None


class Dates(StrictModel):
    received: Optional[date] = None
    started: Optional[date] = None
    target_end: Optional[date] = None
    closed: Optional[date] = None


class WorkerModels(StrictModel):
    researcher: str = "sonnet"
    researcher_profiles: str = "opus"
    analyst: str = "opus"
    producer: str = "opus"
    interviewer_live: str = "sonnet"
    interviewer_debrief: str = "opus"


class Team(StrictModel):
    supervisors: list[str] = Field(default_factory=list)
    principal_model: str = "inherit"
    worker_models: WorkerModels = Field(default_factory=WorkerModels)


DEFAULT_AUTONOMY: dict[str, str] = {
    ActionClass.research_and_analysis.value: AutonomyLevel.auto.value,
    ActionClass.state_write.value: AutonomyLevel.auto.value,
    ActionClass.deliverable_production.value: AutonomyLevel.auto.value,
    ActionClass.interview_plan.value: AutonomyLevel.approve.value,
    ActionClass.interview_conduct.value: AutonomyLevel.auto.value,
    ActionClass.stakeholder_email.value: AutonomyLevel.approve.value,
    ActionClass.client_pm_email.value: AutonomyLevel.approve.value,
    ActionClass.decision_maker_email.value: AutonomyLevel.approve.value,
    ActionClass.tier0_tier1_release.value: AutonomyLevel.approve.value,
    ActionClass.tier2_release.value: AutonomyLevel.approve.value,
    ActionClass.gate_transition.value: AutonomyLevel.approve.value,
    ActionClass.gate_meeting.value: AutonomyLevel.human.value,
    ActionClass.meeting_scheduling.value: AutonomyLevel.approve.value,
}
SHADOW_AUTONOMY: dict[str, str] = {
    **DEFAULT_AUTONOMY,
    ActionClass.interview_plan.value: AutonomyLevel.notify.value,
    ActionClass.stakeholder_email.value: AutonomyLevel.notify.value,
    ActionClass.client_pm_email.value: AutonomyLevel.notify.value,
    ActionClass.tier2_release.value: AutonomyLevel.notify.value,
    ActionClass.meeting_scheduling.value: AutonomyLevel.notify.value,
    ActionClass.gate_meeting.value: AutonomyLevel.auto.value,
}


class AutonomySettings(StrictModel):
    profile: Literal["default", "shadow", "custom"] = "default"
    levels: dict[ActionClass, AutonomyLevel] = Field(default_factory=lambda: dict(DEFAULT_AUTONOMY))


class MeetingSettings(StrictModel):
    default_language: str = "en"
    disclosure_jurisdiction: Optional[str] = None
    recording_retention: str = "delete_after_verification"
    off_record_handling: Literal["remove", "flag"] = "remove"
    providers: dict[str, str] = Field(default_factory=lambda: {"bot": "meetstream", "stt": "provider", "tts": "elevenlabs"})
    latency_target_ms: int = 3000
    max_duration_min: int = 90


class EvidenceSettings(StrictModel):
    grade_floor: SourceTier = SourceTier.B
    two_source_rule: bool = True


class ResearchBudget(StrictModel):
    per_phase: dict[str, dict[str, int]] = Field(
        default_factory=lambda: {
            "P0": {"runs": 2, "fetches": 40},
            "P1": {"runs": 4, "fetches": 40},
            "P2": {"runs": 12, "fetches": 40},
            "P3": {"runs": 4, "fetches": 40},
            "P4": {"runs": 6, "fetches": 40},
            "P5": {"runs": 2, "fetches": 40},
        }
    )


class Settings(StrictModel):
    autonomy: AutonomySettings = Field(default_factory=AutonomySettings)
    meetings: MeetingSettings = Field(default_factory=MeetingSettings)
    evidence: EvidenceSettings = Field(default_factory=EvidenceSettings)
    research_budget: ResearchBudget = Field(default_factory=ResearchBudget)
    default_discount_rate: Optional[Ref] = None
    gate_thresholds: dict[str, float] = Field(default_factory=lambda: {"ap2_interviews_held_share": 0.7})


class Workspace(StrictModel):
    inbox: str = "inbox"
    library: str = "library"
    analysis: str = "analysis"
    deliverables: str = "deliverables"
    meetings: str = "meetings"


class Engagement(Envelope):
    collection: Literal["engagement"] = "engagement"
    code: str
    name: str
    client: Client
    policy_domain: list[str] = Field(default_factory=list)
    pathway: PathwayInfo = Field(default_factory=PathwayInfo)
    languages: list[str] = Field(default_factory=lambda: ["en"])
    currency: str = "USD"
    price_base_year: int = 2026
    fiscal_year_start: str = "01-01"
    status: Literal["active", "paused", "closed"] = "active"
    phase: Phase = Phase.P0
    gates: dict[Gate, GateState] = Field(default_factory=lambda: {g: GateState() for g in Gate})
    dates: Dates = Field(default_factory=Dates)
    team: Team = Field(default_factory=Team)
    settings: Settings = Field(default_factory=Settings)
    counters: dict[str, int] = Field(default_factory=dict)
    last_checkpoint: Optional[Ref] = None
    workspace: Workspace = Field(default_factory=Workspace)


class Objective(StrictModel):
    id: str
    statement: str
    measurable: bool = False
    indicator: Optional[str] = None


class RequiredDeliverable(StrictModel):
    id: str
    description: str
    format: Optional[str] = None
    due: Optional[date] = None
    maps_to: Optional[Ref] = None


class Milestone(StrictModel):
    id: Optional[str] = None
    name: str
    date: Optional[date] = None
    kind: Optional[Literal["gate", "deliverable", "meeting", "client_input"]] = None
    status: Optional[str] = None
    linked: Optional[Ref] = None


class Timeline(StrictModel):
    start: Optional[date] = None
    end: Optional[date] = None
    milestones: list[Milestone] = Field(default_factory=list)


class Constraint(StrictModel):
    kind: Literal["budget", "legal", "political", "data", "timing", "other"] = "other"
    statement: str


class ClientRoles(StrictModel):
    pm: Optional[Ref] = None
    sponsor: Optional[Ref] = None
    ultimate_decision_maker: Optional[Ref] = None
    steering: list[Ref] = Field(default_factory=list)


class Clarification(StrictModel):
    question: Ref
    answer: Optional[str] = None
    answered_in: Optional[Ref] = None


class ProblemStatement(StrictModel):
    as_given: str
    as_reframed: Optional[str] = None
    reframing_rationale: Optional[str] = None


class Brief(Envelope):
    collection: Literal["brief"] = "brief"
    version: int = 0
    status: Literal["draft", "clarifying", "confirmed", "amended"] = "draft"
    rfp_documents: list[Ref] = Field(default_factory=list)
    issued_by: Optional[Ref] = None
    received_on: Optional[date] = None
    title: str
    context_summary: str = ""
    problem_statement: ProblemStatement
    objectives: list[Objective] = Field(default_factory=list)
    scope_in: list[str] = Field(default_factory=list)
    scope_out: list[str] = Field(default_factory=list)
    required_deliverables: list[RequiredDeliverable] = Field(default_factory=list)
    timeline: Timeline = Field(default_factory=Timeline)
    constraints: list[Constraint] = Field(default_factory=list)
    evaluation_criteria: list[str] = Field(default_factory=list)
    client_roles: ClientRoles = Field(default_factory=ClientRoles)
    assumptions: list[str] = Field(default_factory=list)
    clarifications: list[Clarification] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    confirmed_in: Optional[Ref] = None


class Framework(StrictModel):
    id: str
    name: str
    source_org: Optional[str] = None
    rationale: Optional[str] = None
    used_in_phases: list[Phase] = Field(default_factory=list)


class Workstream(StrictModel):
    id: str
    name: str
    objective: Optional[str] = None
    key_questions: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)


class ResearchQuestion(StrictModel):
    id: str
    question: str
    hypotheses: list[Ref] = Field(default_factory=list)
    method: Optional[str] = None
    data_sources: list[str] = Field(default_factory=list)
    workstream: Optional[str] = None
    status: Literal["planned", "running", "done", "dropped"] = "planned"
    drop_reason: Optional[str] = None
    memo: Optional[Ref] = None
    runs: list[str] = Field(default_factory=list)


class AnalyticalPlan(StrictModel):
    research_questions: list[ResearchQuestion] = Field(default_factory=list)


class EngagementPlanSummary(StrictModel):
    interview_targets: list[Ref] = Field(default_factory=list)
    workshops: list[str] = Field(default_factory=list)
    cadence: Optional[str] = None


class QualityPlan(StrictModel):
    grade_floor: SourceTier = SourceTier.B
    review_policy: Optional[str] = "fresh-instance partner review before every release"
    traceability_required: bool = True


class Governance(StrictModel):
    steering_members: list[Ref] = Field(default_factory=list)
    pm_cadence: Optional[str] = "weekly"
    decision_forums: list[str] = Field(default_factory=list)


class Approach(Envelope):
    collection: Literal["approach"] = "approach"
    version: int = 0
    status: Literal["draft", "proposed", "approved", "revised"] = "draft"
    problem_framing: Optional[Ref] = None
    methodology_narrative: str = ""
    frameworks: list[Framework] = Field(default_factory=list)
    workstreams: list[Workstream] = Field(default_factory=list)
    analytical_plan: AnalyticalPlan = Field(default_factory=AnalyticalPlan)
    engagement_plan_summary: EngagementPlanSummary = Field(default_factory=EngagementPlanSummary)
    quality_plan: QualityPlan = Field(default_factory=QualityPlan)
    governance: Governance = Field(default_factory=Governance)
    approved_in: Optional[Ref] = None


class PhasePlan(StrictModel):
    id: Phase
    name: str
    start: Optional[date] = None
    end: Optional[date] = None
    gate: Optional[Gate] = None
    status: Literal["planned", "active", "done"] = "planned"


class Activity(StrictModel):
    id: str
    phase: Phase
    workstream: Optional[str] = None
    name: str
    owner: Literal["principal", "supervisor", "client"] = "principal"
    start: Optional[date] = None
    end: Optional[date] = None
    depends_on: list[str] = Field(default_factory=list)
    status: Literal["planned", "in_progress", "done", "blocked", "dropped"] = "planned"
    outputs: list[Ref] = Field(default_factory=list)
    pct_complete: int = Field(default=0, ge=0, le=100)


class GateCriterion(StrictModel):
    rule_id: str
    description: str
    satisfied: Optional[bool] = None
    evidence: Optional[str] = None


class GatePlan(StrictModel):
    id: Gate
    name: str
    criteria: list[GateCriterion] = Field(default_factory=list)
    decisions_required: list[DecisionKind] = Field(default_factory=list)
    status: GateStatus = GateStatus.not_ready
    passed_in: Optional[Ref] = None


class Cadence(StrictModel):
    pm_checkin: Optional[str] = "weekly"
    steering: Optional[str] = "at gates"
    status_note: Optional[str] = "weekly"


class ChangeLogEntry(StrictModel):
    date: date
    change: str
    reason: Optional[str] = None
    approved_in: Optional[Ref] = None


class Workplan(Envelope):
    collection: Literal["workplan"] = "workplan"
    version: int = 0
    status: Literal["draft", "proposed", "approved", "revised"] = "draft"
    phases: list[PhasePlan] = Field(default_factory=list)
    activities: list[Activity] = Field(default_factory=list)
    milestones: list[Milestone] = Field(default_factory=list)
    gates: list[GatePlan] = Field(default_factory=list)
    cadence: Cadence = Field(default_factory=Cadence)
    change_log: list[ChangeLogEntry] = Field(default_factory=list)


# =====================================================================================
# B. People and politics
# =====================================================================================


class PredictedReaction(StrictModel):
    target: Ref
    reaction: Reaction
    rationale: Optional[str] = None
    confidence: Confidence = Confidence.medium
    basis: list[Ref] = Field(default_factory=list)


class Relationship(StrictModel):
    to: Ref
    type: RelationshipType
    strength: Literal["weak", "moderate", "strong"] = "moderate"
    basis: Literal["observed", "assessed"] = "assessed"
    evidence: list[Ref] = Field(default_factory=list)


class EngagementPlan(StrictModel):
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    purpose: Optional[str] = None
    format: Literal["interview", "workshop", "briefing", "consultation", "none"] = "none"
    owner: Optional[str] = None
    status: Literal["not_planned", "requested", "scheduled", "engaged", "declined"] = "not_planned"
    meetings: list[Ref] = Field(default_factory=list)
    next_step: Optional[str] = None


class Contact(StrictModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    assistant: Optional[str] = None
    preferred_channel: Optional[str] = None


class Stakeholder(Envelope):
    collection: Literal["stakeholders"] = "stakeholders"
    name: str
    kind: StakeholderKind = StakeholderKind.person
    organisation: Optional[Ref] = None
    title: Optional[str] = None
    category: StakeholderCategory
    jurisdiction: Optional[str] = None
    is_client: bool = False
    client_role: ClientRole = ClientRole.none
    decision_role: DecisionRole = DecisionRole.none
    influence: Optional[int] = Field(default=None, ge=1, le=5)
    interest: Optional[int] = Field(default=None, ge=1, le=5)
    stance: Stance = Stance.unknown
    stance_confidence: Optional[Confidence] = None
    stance_basis: list[Ref] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    red_lines: list[str] = Field(default_factory=list)
    public_positions: list[Ref] = Field(default_factory=list)
    predicted_reactions: list[PredictedReaction] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    engagement: EngagementPlan = Field(default_factory=EngagementPlan)
    contact: Contact = Field(default_factory=Contact)
    profile: Optional[Ref] = None
    sources: list[Ref] = Field(default_factory=list)
    last_reviewed: Optional[date] = None
    status: Literal["active", "inactive"] = "active"


class Assessment(StrictModel):
    assessment: str
    confidence: Confidence
    basis: list[Ref] = Field(default_factory=list)


class CareerEntry(StrictModel):
    start: Optional[str] = None
    end: Optional[str] = None
    role: str
    organisation: Optional[str] = None
    source: Optional[Ref] = None


class StatedPriority(StrictModel):
    theme: str
    statement: Optional[Ref] = None
    date: Optional[date] = None


class TrackRecordEntry(StrictModel):
    decision: str
    date: Optional[date] = None
    outcome: Optional[str] = None
    source: Optional[Ref] = None


class TopicPosition(StrictModel):
    topic: str
    position: str
    date: Optional[date] = None
    evidence: Optional[Ref] = None


class CalendarEvent(StrictModel):
    event: str
    date: Optional[date] = None
    relevance: Optional[str] = None


class OnlinePresence(StrictModel):
    platform: str
    handle: Optional[str] = None
    url: Optional[str] = None
    official: bool = False


class PublicControversy(StrictModel):
    summary: str
    source: Optional[Ref] = None


class Affiliations(StrictModel):
    party: Optional[str] = None
    declared_positions: list[str] = Field(default_factory=list)
    networks: list[str] = Field(default_factory=list)


class OrgUnit(StrictModel):
    name: str
    head: Optional[Ref] = None
    mandate: Optional[str] = None


class OrgStructure(StrictModel):
    units: list[OrgUnit] = Field(default_factory=list)
    headcount: Optional[int] = None
    budget: Optional[str] = None


class Faction(StrictModel):
    name: str
    members: list[Ref] = Field(default_factory=list)
    position: Optional[str] = None
    confidence: Confidence = Confidence.low
    basis: list[Ref] = Field(default_factory=list)


class ProfileReview(StrictModel):
    personal_data_minimised: bool = False
    defamation_check: bool = False
    reviewed_by: Optional[str] = None
    date: Optional[date] = None


class Profile(Envelope):
    collection: Literal["profiles"] = "profiles"
    confidentiality: Confidentiality = Confidentiality.sensitive_personal
    subject: Ref
    scope: Literal["person", "organisation"] = "person"
    summary: str
    career: list[CareerEntry] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    affiliations: Affiliations = Field(default_factory=Affiliations)
    orientation_assessment: dict[str, Assessment] = Field(default_factory=dict)
    priorities_stated: list[StatedPriority] = Field(default_factory=list)
    track_record: list[TrackRecordEntry] = Field(default_factory=list)
    positions_on_topic: list[TopicPosition] = Field(default_factory=list)
    communication_style: Optional[str] = None
    advisers_and_networks: list[Ref] = Field(default_factory=list)
    political_calendar: list[CalendarEvent] = Field(default_factory=list)
    online_presence: list[OnlinePresence] = Field(default_factory=list)
    controversies_public: list[PublicControversy] = Field(default_factory=list)
    structure: Optional[OrgStructure] = None
    factions_assessed: list[Faction] = Field(default_factory=list)
    implications_for_engagement: list[str] = Field(default_factory=list)
    overall_confidence: Confidence = Confidence.low
    review: ProfileReview = Field(default_factory=ProfileReview)
    sources: list[Ref] = Field(default_factory=list)
    status: Literal["draft", "reviewed", "final", "deleted"] = "draft"

    @field_validator("confidentiality")
    @classmethod
    def _always_sensitive(cls, value):
        if value != Confidentiality.sensitive_personal.value and value != Confidentiality.sensitive_personal:
            raise ValueError("profiles are always sensitive-personal (rule 11)")
        return value


# =====================================================================================
# C. Knowledge
# =====================================================================================


class Access(StrictModel):
    retrieved_at: Optional[datetime] = None
    retrieved_by: Optional[str] = None
    snapshot_path: Optional[str] = None
    hash: Optional[str] = None
    paywalled: bool = False
    query: Optional[str] = None


class Source(Envelope):
    collection: Literal["sources"] = "sources"
    title: str
    type: SourceType
    publisher: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    publication_date: Optional[date] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    isbn: Optional[str] = None
    citation: str
    tier: SourceTier
    tier_rationale: str
    independence_group: str
    interest_declared: Literal["none", "commercial", "advocacy", "government", "party"] = "none"
    access: Access = Field(default_factory=Access)
    language: Optional[str] = None
    geography: Optional[str] = None
    status: Literal["active", "superseded", "retracted", "unreachable"] = "active"


class Value(StrictModel):
    number: Optional[float] = None
    unit: Optional[str] = None
    period: Optional[str] = None
    geography: Optional[str] = None
    as_of: Optional[date] = None
    currency: Optional[str] = None
    price_base_year: Optional[int] = None


class Evidence(Envelope):
    collection: Literal["evidence"] = "evidence"
    statement: str
    kind: EvidenceKind
    value: Optional[Value] = None
    quote_text: Optional[str] = None
    speaker: Optional[Ref] = None
    sources: list[Ref] = Field(min_length=1)
    corroboration: Corroboration = Corroboration.single_source
    independence_count: int = 0
    grade: Optional[SourceTier] = None
    validated: bool = False
    confidence: Confidence = Confidence.medium
    attribution: Optional[Attribution] = None
    meeting: Optional[Ref] = None
    transcript_turns: list[int] = Field(default_factory=list)
    research_question: Optional[str] = None
    supports: list[Ref] = Field(default_factory=list)
    contradicts: list[Ref] = Field(default_factory=list)
    about: list[Ref] = Field(default_factory=list)
    used_in: list[Ref] = Field(default_factory=list)
    status: Literal["active", "superseded", "withdrawn"] = "active"


class Processing(StrictModel):
    status: Literal["received", "extracted", "summarised", "mined"] = "received"
    by: Optional[str] = None
    at: Optional[datetime] = None


class Document(Envelope):
    collection: Literal["documents"] = "documents"
    title: str
    kind: Literal[
        "rfp", "terms_of_reference", "contract", "client_data", "client_report", "legislation", "regulation", "strategy",
        "budget", "statistics", "academic", "report", "news", "transcript", "minutes", "presentation", "calendar_invite", "other",
    ] = "other"
    origin: Literal["client", "public", "stakeholder", "horus"] = "client"
    received_via: Optional[Ref] = None
    received_on: Optional[date] = None
    document_date: Optional[date] = None
    issuer: Optional[str] = None
    path: str
    hash: str
    pages: Optional[int] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    key_points: list[Ref] = Field(default_factory=list)
    source: Optional[Ref] = None
    processing: Processing = Field(default_factory=Processing)
    related: list[Ref] = Field(default_factory=list)
    status: Literal["active", "superseded"] = "active"


class Revision(StrictModel):
    date: date
    previous: str
    new: str
    reason: Optional[str] = None


class Hypothesis(Envelope):
    collection: Literal["hypotheses"] = "hypotheses"
    statement: str
    kind: Literal["diagnostic", "causal", "option_effect", "political", "stakeholder", "implementation"] = "diagnostic"
    parent: Optional[Ref] = None
    research_questions: list[str] = Field(default_factory=list)
    status: HypothesisStatus = HypothesisStatus.untested
    confidence: Confidence = Confidence.low
    evidence_for: list[Ref] = Field(default_factory=list)
    evidence_against: list[Ref] = Field(default_factory=list)
    revision_history: list[Revision] = Field(default_factory=list)
    implications: Optional[str] = None


# =====================================================================================
# D. Analysis
# =====================================================================================


class Finding(StrictModel):
    statement: str
    evidence: list[Ref] = Field(default_factory=list)
    confidence: Confidence = Confidence.medium


class Analysis(Envelope):
    collection: Literal["analyses"] = "analyses"
    kind: AnalysisKind
    title: str
    question: Optional[str] = None
    frameworks: list[str] = Field(default_factory=list)
    inputs: list[Ref] = Field(default_factory=list)
    method_notes: str = ""
    content: dict[str, Any] = Field(default_factory=dict)
    narrative_path: Optional[str] = None
    findings: list[Finding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    version: int = 1
    status: Literal["draft", "reviewed", "final", "superseded"] = "draft"
    used_in: list[Ref] = Field(default_factory=list)


class Mechanism(StrictModel):
    inputs: list[str] = Field(default_factory=list)
    activities: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    impacts: list[str] = Field(default_factory=list)
    key_assumptions: list[Ref] = Field(default_factory=list)


class DesignParameter(StrictModel):
    lever: str
    setting: Optional[str] = None
    alternatives: list[str] = Field(default_factory=list)


class Variant(StrictModel):
    id: str
    description: str


class Precedent(StrictModel):
    jurisdiction: str
    programme: Optional[str] = None
    period: Optional[str] = None
    outcome: Optional[str] = None
    evidence: list[Ref] = Field(default_factory=list)


class ScreeningCriterion(StrictModel):
    criterion: str
    score: Optional[float] = None
    rationale: Optional[str] = None


class Screening(StrictModel):
    criteria: list[ScreeningCriterion] = Field(default_factory=list)
    result: Optional[Literal["pass", "fail", "merge"]] = None
    rationale: Optional[str] = None
    analysis: Optional[Ref] = None


class PrincipleAlignment(StrictModel):
    principle: Ref
    score: int = Field(ge=-2, le=2)
    rationale: Optional[str] = None


class Option(Envelope):
    collection: Literal["options"] = "options"
    code: str
    title: str
    summary: str
    kind: OptionKind
    addresses_objectives: list[str] = Field(default_factory=list)
    instrument_types: list[InstrumentType] = Field(default_factory=list)
    mechanism: Mechanism = Field(default_factory=Mechanism)
    design_parameters: list[DesignParameter] = Field(default_factory=list)
    variants: list[Variant] = Field(default_factory=list)
    target_groups: list[str] = Field(default_factory=list)
    precedents: list[Precedent] = Field(default_factory=list)
    origin: Literal["horus", "client", "stakeholder", "literature"] = "horus"
    status: OptionStatus = OptionStatus.long_list
    screening: Optional[Screening] = None
    principles_alignment: list[PrincipleAlignment] = Field(default_factory=list)
    reactions: Optional[Ref] = None
    appraisal: Optional[Ref] = None
    risks: list[Ref] = Field(default_factory=list)
    package_members: list[Ref] = Field(default_factory=list)


class Estimate(StrictModel):
    central: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    unit: Optional[str] = None
    present_value: bool = False


class Impact(StrictModel):
    dimension: ImpactDimension
    direction: Literal["positive", "negative", "mixed", "neutral"] = "neutral"
    quantified: bool = False
    estimate: Optional[Estimate] = None
    rating: Optional[int] = Field(default=None, ge=-3, le=3)
    affected_groups: list[str] = Field(default_factory=list)
    assumptions: list[Ref] = Field(default_factory=list)
    evidence: list[Ref] = Field(default_factory=list)
    method: Optional[str] = None
    confidence: Confidence = Confidence.medium
    notes: Optional[str] = None


class AppraisalSummary(StrictModel):
    npv: Optional[Estimate] = None
    bcr: Optional[float] = None
    net_benefit: Optional[float] = None
    mca_score: Optional[float] = None
    rank: Optional[int] = None
    verdict: Optional[str] = None


class Distributional(StrictModel):
    groups: list[str] = Field(default_factory=list)
    incidence: list[dict[str, Any]] = Field(default_factory=list)
    equity_note: Optional[str] = None


class FeasibilityItem(StrictModel):
    rating: int = Field(ge=1, le=5)
    note: Optional[str] = None
    evidence: list[Ref] = Field(default_factory=list)


class Feasibility(StrictModel):
    administrative: Optional[FeasibilityItem] = None
    legal: Optional[FeasibilityItem] = None
    political: Optional[FeasibilityItem] = None


class Sensitivity(StrictModel):
    method: Literal["scenarios", "monte_carlo", "switching_values"] = "scenarios"
    parameters: list[Ref] = Field(default_factory=list)
    results_path: Optional[str] = None
    robustness: Optional[str] = None


class Indicator(StrictModel):
    name: str
    baseline: Optional[str] = None
    target: Optional[str] = None
    source: Optional[str] = None
    frequency: Optional[str] = None
    owner: Optional[str] = None


class Monitoring(StrictModel):
    indicators: list[Indicator] = Field(default_factory=list)
    evaluation: dict[str, Any] = Field(default_factory=dict)


class Artefact(StrictModel):
    path: str
    kind: Literal["model", "data", "chart", "notebook", "report"] = "model"
    inputs_hash: Optional[str] = None


class Baseline(StrictModel):
    description: str
    analysis: Optional[Ref] = None


class TimeHorizon(StrictModel):
    start_year: int
    years: int


KIND_BLOCKS = {
    AppraisalKind.ria.value: "regulatory",
    AppraisalKind.strategic_options.value: "strategic",
    AppraisalKind.operating_model.value: "operating_model",
    AppraisalKind.delivery_intervention.value: "delivery",
    AppraisalKind.business_case.value: "five_case",
    AppraisalKind.service_concept.value: "service",
}


class Appraisal(Envelope):
    collection: Literal["appraisals"] = "appraisals"
    options: list[Ref] = Field(min_length=1)
    version: int = 1
    kind: AppraisalKind
    pathway: Pathway
    baseline: Baseline
    standards_applied: list[str] = Field(default_factory=list)
    methodology: Methodology = Methodology.mixed
    proportionality_level: Literal["light", "standard", "full"] = "standard"
    time_horizon: Optional[TimeHorizon] = None
    discount_rate: Optional[Ref] = None
    impacts: list[Impact] = Field(default_factory=list)
    summary: AppraisalSummary = Field(default_factory=AppraisalSummary)
    distributional: Distributional = Field(default_factory=Distributional)
    feasibility: Feasibility = Field(default_factory=Feasibility)
    sensitivity: Optional[Sensitivity] = None
    risks: list[Ref] = Field(default_factory=list)
    monitoring: Monitoring = Field(default_factory=Monitoring)
    regulatory: Optional[dict[str, Any]] = None
    strategic: Optional[dict[str, Any]] = None
    operating_model: Optional[dict[str, Any]] = None
    delivery: Optional[dict[str, Any]] = None
    five_case: Optional[dict[str, Any]] = None
    service: Optional[dict[str, Any]] = None
    artefacts: list[Artefact] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    reviewed_by: Optional[str] = None
    status: Literal["draft", "reviewed", "final", "superseded"] = "draft"

    @model_validator(mode="after")
    def _kind_block_present_when_final(self):
        block = KIND_BLOCKS.get(str(self.kind))
        if self.status in ("reviewed", "final") and block and getattr(self, block) is None:
            raise ValueError(f"appraisal of kind {self.kind} must carry its `{block}` block before review (rule 20)")
        return self


class Assumption(Envelope):
    collection: Literal["assumptions"] = "assumptions"
    name: str
    category: Literal["macro", "demographic", "cost", "behavioural", "policy", "technical", "financial"] = "policy"
    value: float
    unit: str
    low: Optional[float] = None
    high: Optional[float] = None
    distribution: Optional[Literal["point", "uniform", "triangular", "normal", "lognormal"]] = "point"
    basis: Literal["evidence", "expert_judgement", "client", "convention"] = "expert_judgement"
    evidence: list[Ref] = Field(default_factory=list)
    source_note: str = ""
    used_in: list[Ref] = Field(default_factory=list)
    sensitivity_rank: Optional[Literal["high", "medium", "low"]] = None
    owner: str = "principal"
    status: Literal["proposed", "agreed", "superseded"] = "proposed"
    agreed_in: Optional[Ref] = None


class Risk(Envelope):
    collection: Literal["risks"] = "risks"
    scope: Literal["engagement", "policy_outcome", "implementation", "political", "reputational", "legal", "fiscal"] = "engagement"
    description: str
    cause: Optional[str] = None
    consequence: Optional[str] = None
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    mitigation: Optional[str] = None
    contingency: Optional[str] = None
    owner: str = "principal"
    early_warning: Optional[str] = None
    linked: list[Ref] = Field(default_factory=list)
    status: Literal["open", "mitigating", "closed", "materialised"] = "open"
    source: Optional[Ref] = None

    @property
    def score(self) -> int:
        return self.likelihood * self.impact


# =====================================================================================
# E. Engagement loop
# =====================================================================================


class Participant(StrictModel):
    stakeholder: Optional[Ref] = None
    name: Optional[str] = None
    role: Literal["client", "stakeholder", "horus", "supervisor", "observer"] = "stakeholder"
    attended: Optional[bool] = None
    speaker_label: Optional[str] = None
    email: Optional[str] = None


class DecisionSought(StrictModel):
    statement: str
    outcome: Optional[Ref] = None


class QuestionGuideItem(StrictModel):
    id: str
    question: str
    priority: int = Field(default=2, ge=1, le=3)
    purpose: Optional[str] = None
    tests: list[Ref] = Field(default_factory=list)
    follow_up_heuristics: list[str] = Field(default_factory=list)
    asked: bool = False
    answer_summary: Optional[str] = None
    turns: list[int] = Field(default_factory=list)


class MeetingPlan(StrictModel):
    path: Optional[str] = None
    version: int = 1
    objectives: list[str] = Field(default_factory=list)
    question_guide: list[QuestionGuideItem] = Field(default_factory=list)
    follow_up_rules: list[str] = Field(default_factory=list)
    sensitivities: list[str] = Field(default_factory=list)
    do_not_say: list[str] = Field(default_factory=list)
    disclosure_script_id: Optional[str] = None
    disclosure_script: Optional[str] = None
    consent_terms: Optional[str] = None
    attribution_rule: Attribution = Attribution.background
    escalation_rules: list[str] = Field(default_factory=list)
    time_budget_min: Optional[int] = None
    documents_to_present: list[Ref] = Field(default_factory=list)
    approval: Optional[Ref] = None


class AgendaItem(StrictModel):
    item: str
    minutes: Optional[int] = None
    lead: Optional[str] = None
    deliverable: Optional[Ref] = None


class ProposedSlot(StrictModel):
    start: datetime
    end: datetime
    timezone: str = "UTC"
    status: Literal["proposed", "accepted", "declined"] = "proposed"


class Scheduling(StrictModel):
    status: Literal["not_started", "slots_proposed", "awaiting_reply", "confirmed", "rescheduling", "cancelled"] = "not_started"
    proposed_slots: list[ProposedSlot] = Field(default_factory=list)
    selected_slot: Optional[ProposedSlot] = None
    request_sent: Optional[Ref] = None
    reply_received: Optional[Ref] = None
    invite_document: Optional[Ref] = None
    calendar_event_id: Optional[str] = None
    organiser: Literal["horus", "client", "stakeholder"] = "client"
    approval: Optional[Ref] = None


class BotInfo(StrictModel):
    provider: Optional[str] = None
    bot_id: Optional[str] = None
    display_name: Optional[str] = None
    requested_at: Optional[datetime] = None
    joined_at: Optional[datetime] = None
    admitted_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    exit_reason: Optional[str] = None


class Disclosure(StrictModel):
    script_id: Optional[str] = None
    spoken_at: Optional[datetime] = None
    chat_posted_at: Optional[datetime] = None
    text: Optional[str] = None


class Objection(StrictModel):
    at: Optional[datetime] = None
    text: str
    response: Optional[str] = None


class OffRecordSegment(StrictModel):
    start: float
    end: Optional[float] = None


class Consent(StrictModel):
    ai_participant: bool = False
    recording: bool = False
    transcript: bool = False
    attribution_rule: Optional[Attribution] = None
    given_by: Optional[Ref] = None
    given_at: Optional[datetime] = None
    objections: list[Objection] = Field(default_factory=list)
    withdrawn_at: Optional[datetime] = None
    off_record_segments: list[OffRecordSegment] = Field(default_factory=list)


class Intervention(StrictModel):
    type: Literal["whisper", "pause", "resume", "takeover", "leave"]
    at: Optional[datetime] = None
    text: Optional[str] = None
    by: str = "supervisor"


class Mark(StrictModel):
    label: str
    at: float
    note: Optional[str] = None


class Fallback(StrictModel):
    type: str
    at: Optional[datetime] = None
    outcome: Optional[str] = None


class Coverage(StrictModel):
    asked: int = 0
    total: int = 0
    skipped: list[str] = Field(default_factory=list)


class LiveState(StrictModel):
    coverage: Coverage = Field(default_factory=Coverage)
    supervisor_interventions: list[Intervention] = Field(default_factory=list)
    marks: list[Mark] = Field(default_factory=list)
    fallbacks: list[Fallback] = Field(default_factory=list)
    latency: dict[str, float] = Field(default_factory=dict)
    chat_messages: list[dict[str, Any]] = Field(default_factory=list)


class TranscriptInfo(StrictModel):
    path: Optional[str] = None
    language: Optional[str] = None
    diarised: bool = False
    provider: Optional[str] = None
    turns: Optional[int] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    retention_until: Optional[date] = None
    off_record_removed: bool = False


class RecordingInfo(StrictModel):
    path: Optional[str] = None
    retention_until: Optional[date] = None
    deleted_at: Optional[datetime] = None


class StructuredNotes(StrictModel):
    key_points: list[str] = Field(default_factory=list)
    positions: list[Ref] = Field(default_factory=list)
    quotes: list[Ref] = Field(default_factory=list)
    surprises: list[str] = Field(default_factory=list)
    sentiment: Optional[str] = None


class MeetingNotes(StrictModel):
    raw_path: Optional[str] = None
    structured: StructuredNotes = Field(default_factory=StructuredNotes)


class TopicRecord(StrictModel):
    topic: str
    position: str
    evidence: Optional[Ref] = None


class OptionReaction(StrictModel):
    option: Ref
    reaction: Reaction
    evidence: Optional[Ref] = None


class Contradiction(StrictModel):
    hypothesis: Ref
    note: str


class ProposedUpdates(StrictModel):
    stakeholder_patch: dict[str, Any] = Field(default_factory=dict)
    hypothesis_patches: list[dict[str, Any]] = Field(default_factory=list)
    confirmed_by: Optional[str] = None
    confirmed_at: Optional[datetime] = None


class InterviewRecord(StrictModel):
    topics: list[TopicRecord] = Field(default_factory=list)
    reaction_to_options: list[OptionReaction] = Field(default_factory=list)
    contradictions: list[Contradiction] = Field(default_factory=list)
    documents_promised: list[Ref] = Field(default_factory=list)
    documents_shared: list[Ref] = Field(default_factory=list)
    directives_received: list[Ref] = Field(default_factory=list)
    referrals: list[Ref] = Field(default_factory=list)
    follow_ups: list[Ref] = Field(default_factory=list)
    proposed_updates: ProposedUpdates = Field(default_factory=ProposedUpdates)


class Outcomes(StrictModel):
    decisions: list[Ref] = Field(default_factory=list)
    client_inputs: list[Ref] = Field(default_factory=list)
    open_questions: list[Ref] = Field(default_factory=list)
    actions: list[Ref] = Field(default_factory=list)
    evidence: list[Ref] = Field(default_factory=list)


class Debrief(StrictModel):
    path: Optional[str] = None
    by: Optional[str] = None
    what_worked: Optional[str] = None
    what_to_change: Optional[str] = None


class Meeting(Envelope):
    collection: Literal["meetings"] = "meetings"
    kind: MeetingKind
    title: str
    status: MeetingStatus = MeetingStatus.proposed
    conduct_mode: ConductMode = ConductMode.interviewer
    requested_via: Optional[Ref] = None
    join_url: Optional[str] = None
    platform: Optional[Literal["zoom", "meet", "teams", "other"]] = None
    scheduled_at: Optional[datetime] = None
    held_at: Optional[datetime] = None
    duration_min: Optional[int] = None
    time_budget_min: Optional[int] = None
    mode: Optional[Literal["virtual", "in_person", "phone"]] = "virtual"
    location: Optional[str] = None
    participants: list[Participant] = Field(default_factory=list)
    purpose: str
    objectives: list[str] = Field(default_factory=list)
    decisions_sought: list[DecisionSought] = Field(default_factory=list)
    hypotheses_to_test: list[Ref] = Field(default_factory=list)
    open_questions_to_close: list[Ref] = Field(default_factory=list)
    plan: Optional[MeetingPlan] = None
    agenda: list[AgendaItem] = Field(default_factory=list)
    prep_pack: list[Ref] = Field(default_factory=list)
    pre_read_sent: Optional[Ref] = None
    scheduling: Scheduling = Field(default_factory=Scheduling)
    bot: Optional[BotInfo] = None
    disclosure: Optional[Disclosure] = None
    consent: Optional[Consent] = None
    live: Optional[LiveState] = None
    transcript: Optional[TranscriptInfo] = None
    recording: Optional[RecordingInfo] = None
    notes: Optional[MeetingNotes] = None
    interview_record: Optional[InterviewRecord] = None
    outcomes: Outcomes = Field(default_factory=Outcomes)
    debrief: Optional[Debrief] = None
    follow_up_sent: Optional[Ref] = None

    @model_validator(mode="after")
    def _interview_record_when_held(self):
        if self.kind == MeetingKind.interview.value and self.status == MeetingStatus.held.value and self.interview_record is None:
            raise ValueError("a held interview must carry an interview_record")
        return self


class AboutTarget(StrictModel):
    target: Ref
    version: Optional[int] = None
    section: Optional[str] = None


class ClientInputResponse(StrictModel):
    what_changed: Optional[str] = None
    deliverable_version: Optional[Ref] = None
    decision: Optional[Ref] = None
    communicated_in: Optional[Ref] = None


class ClientInput(Envelope):
    collection: Literal["client_inputs"] = "client_inputs"
    kind: ClientInputKind
    from_stakeholder: Ref = Field(alias="from")
    via: Ref
    date: date
    content_verbatim: Optional[str] = None
    paraphrase: str
    about: list[AboutTarget] = Field(default_factory=list)
    sentiment: Literal["positive", "neutral", "negative", "mixed"] = "neutral"
    priority: Priority = Priority.P2
    disposition: Literal["pending", "accepted", "partially_accepted", "declined", "superseded"] = "pending"
    disposition_rationale: Optional[str] = None
    response: ClientInputResponse = Field(default_factory=ClientInputResponse)
    owner: str = "principal"
    status: Literal["open", "addressed", "closed"] = "open"

    model_config = {"extra": "forbid", "use_enum_values": True, "validate_assignment": True, "validate_default": True, "populate_by_name": True}

    @model_validator(mode="after")
    def _disposition_rationale(self):
        if self.disposition != "pending" and not self.disposition_rationale:
            raise ValueError("a disposition other than pending needs a rationale")
        return self


class Implication(StrictModel):
    area: str
    change: str


class Decision(Envelope):
    collection: Literal["decisions"] = "decisions"
    kind: DecisionKind
    statement: str
    proposed_by: Literal["horus", "client", "stakeholder", "supervisor"] = "horus"
    made_by: list[str] = Field(default_factory=list)
    forum: Optional[Ref] = None
    channel: Optional[Ref] = None
    date: date
    rationale: str
    alternatives_considered: list[str] = Field(default_factory=list)
    implications: list[Implication] = Field(default_factory=list)
    affects: list[Ref] = Field(default_factory=list)
    gate: Optional[Gate] = None
    status: DecisionStatus = DecisionStatus.proposed
    supersedes: Optional[Ref] = None
    review_date: Optional[date] = None

    @model_validator(mode="after")
    def _confirmed_needs_forum(self):
        if self.status == DecisionStatus.confirmed.value:
            if not self.made_by or not (self.forum or self.channel):
                raise ValueError("a confirmed decision needs made_by and a forum or channel (rule 7)")
        if self.kind == DecisionKind.gate.value and self.gate is None:
            raise ValueError("a gate decision must name its gate")
        return self


class OpenQuestion(Envelope):
    collection: Literal["open_questions"] = "open_questions"
    question: str
    context: Optional[str] = None
    kind: Literal["clarification", "data", "analytical", "political", "process"] = "clarification"
    raised_by: str
    raised_in: Optional[str] = None
    date: date
    owner: str
    priority: Priority = Priority.P2
    blocking: list[str] = Field(default_factory=list)
    due: Optional[date] = None
    status: OpenQuestionStatus = OpenQuestionStatus.open
    answer: Optional[str] = None
    answered_by: Optional[Ref] = None
    answered_at: Optional[date] = None


class Reminder(StrictModel):
    date: date
    sent_in: Optional[Ref] = None


class Action(Envelope):
    collection: Literal["actions"] = "actions"
    kind: ActionKind
    title: str
    detail: Optional[str] = None
    owner: str
    requested_via: Optional[Ref] = None
    due: Optional[date] = None
    priority: Priority = Priority.P2
    status: ActionStatus = ActionStatus.todo
    fulfilled_by: Optional[Ref] = None
    linked: list[str] = Field(default_factory=list)
    reminders: list[Reminder] = Field(default_factory=list)


class Extracted(StrictModel):
    actions: list[Ref] = Field(default_factory=list)
    client_inputs: list[Ref] = Field(default_factory=list)
    open_questions: list[Ref] = Field(default_factory=list)
    decisions: list[Ref] = Field(default_factory=list)
    evidence: list[Ref] = Field(default_factory=list)
    meetings: list[Ref] = Field(default_factory=list)


class Communication(Envelope):
    collection: Literal["communications"] = "communications"
    channel: Channel = Channel.email
    direction: Direction
    external_ref: Optional[str] = None
    thread_ref: Optional[str] = None
    from_party: str = Field(alias="from")
    to: list[str] = Field(default_factory=list)
    cc: list[str] = Field(default_factory=list)
    date: datetime
    subject: Optional[str] = None
    summary: str
    body_path: Optional[str] = None
    attachments: list[Ref] = Field(default_factory=list)
    classification: Literal["client_pm", "client_dm", "stakeholder", "internal", "vendor", "scheduling"] = "client_pm"
    action_class: Optional[ActionClass] = None
    extracted: Extracted = Field(default_factory=Extracted)
    approval: Optional[Ref] = None
    related: list[Ref] = Field(default_factory=list)
    status: Literal["draft", "pending_approval", "approved", "sent", "received", "triaged", "processed"] = "draft"

    model_config = {"extra": "forbid", "use_enum_values": True, "validate_assignment": True, "validate_default": True, "populate_by_name": True}


class ApprovalTarget(StrictModel):
    collection: str
    id: str
    version: Optional[int] = None


class Approval(Envelope):
    collection: Literal["approvals"] = "approvals"
    target: ApprovalTarget
    action_class: ActionClass
    risk_class: RiskClass = RiskClass.medium
    summary: str
    requested_by: str
    requested_at: datetime
    autonomy_level_at_request: AutonomyLevel
    status: ApprovalStatus = ApprovalStatus.pending
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None
    note: Optional[str] = None
    conditions: list[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None


# =====================================================================================
# F. Outputs
# =====================================================================================


class QAResult(StrictModel):
    visual: Literal["pass", "fail", "n/a"] = "n/a"
    logic: Literal["pass", "fail", "n/a"] = "n/a"
    traceability: Literal["pass", "fail", "n/a"] = "n/a"
    language: Literal["pass", "fail", "n/a"] = "n/a"
    sensitivity: Literal["pass", "fail", "n/a"] = "n/a"
    report_path: Optional[str] = None

    def all_pass(self) -> bool:
        return all(getattr(self, k) in ("pass", "n/a") for k in ("visual", "logic", "traceability", "language", "sensitivity"))


class ReviewResult(StrictModel):
    reviewer_run: Optional[str] = None
    memo_path: Optional[str] = None
    blockers: int = 0
    majors: int = 0
    minors: int = 0
    resolved: bool = False


class DeliverableVersion(StrictModel):
    v: int
    paths: dict[str, str] = Field(default_factory=dict)
    hash: Optional[str] = None
    created_at: datetime
    created_by: str
    change_summary: str = ""
    based_on_feedback: list[Ref] = Field(default_factory=list)
    qa: QAResult = Field(default_factory=QAResult)
    review: ReviewResult = Field(default_factory=ReviewResult)
    approval: Optional[Ref] = None
    sent_in: Optional[Ref] = None
    status: DeliverableVersionStatus = DeliverableVersionStatus.draft


DELIVERABLE_TYPES = Literal[
    "kickoff_deck", "meeting_plan", "interview_debrief", "status_note", "diagnostic_deck", "principles_deck", "appraisal_deck",
    "final_deck", "executive_deck", "decision_brief", "executive_summary", "decision_memo", "policy_note", "implementation_plan", "communication_plan",
    "workplan_document", "minutes", "memo", "email", "ria_report", "regulatory_instrument_outline", "strategy_document",
    "implementation_roadmap", "operating_model_blueprint", "governance_charter", "transition_plan", "delivery_plan",
    "dashboard_specification", "business_case", "appraisal_summary_table", "financing_options_paper", "service_design_document",
    "service_blueprint", "pilot_evaluation_plan", "legal_change_inventory", "routines_design", "capability_plan", "cost_to_serve_summary", "other",
]


class Deliverable(Envelope):
    collection: Literal["deliverables"] = "deliverables"
    type: DELIVERABLE_TYPES
    title: str
    tier: DeliverableTier
    audience: list[Ref] = Field(default_factory=list)
    purpose: str
    for_meeting: Optional[Ref] = None
    maps_to_brief: Optional[str] = None
    storyboard_path: Optional[str] = None
    template: str = "horus-neutral-v1"
    current_version: int = 0
    versions: list[DeliverableVersion] = Field(default_factory=list)
    evidence_used: list[Ref] = Field(default_factory=list)
    feedback: list[Ref] = Field(default_factory=list)
    status: DeliverableStatus = DeliverableStatus.planned


# =====================================================================================
# G. System
# =====================================================================================


class CheckpointBody(StrictModel):
    done: list[str] = Field(default_factory=list)
    decided: list[str] = Field(default_factory=list)
    learned: list[str] = Field(default_factory=list)
    next: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    phase: Optional[Phase] = None
    gates: dict[str, str] = Field(default_factory=dict)


class Event(StrictModel):
    id: str
    ts: datetime
    actor: str
    session_id: str = "unknown"
    op: EventOp
    collection: Optional[str] = None
    record_id: Optional[str] = None
    summary: str
    diff: Optional[dict[str, Any]] = None
    reason: Optional[str] = None
    checkpoint: Optional[CheckpointBody] = None


# =====================================================================================
# Registry
# =====================================================================================

SINGLETONS: dict[str, type[Envelope]] = {
    "engagement": Engagement,
    "brief": Brief,
    "approach": Approach,
    "workplan": Workplan,
}

COLLECTIONS: dict[str, type[Envelope]] = {
    **SINGLETONS,
    "stakeholders": Stakeholder,
    "profiles": Profile,
    "sources": Source,
    "evidence": Evidence,
    "documents": Document,
    "hypotheses": Hypothesis,
    "analyses": Analysis,
    "options": Option,
    "appraisals": Appraisal,
    "assumptions": Assumption,
    "risks": Risk,
    "meetings": Meeting,
    "client_inputs": ClientInput,
    "decisions": Decision,
    "open_questions": OpenQuestion,
    "actions": Action,
    "communications": Communication,
    "approvals": Approval,
    "deliverables": Deliverable,
}

PREFIXES: dict[str, str] = {
    "engagement": "ENG",
    "brief": "BRF",
    "approach": "APR",
    "workplan": "WPL",
    "stakeholders": "STK",
    "profiles": "PRF",
    "sources": "SRC",
    "evidence": "EVD",
    "documents": "DOC",
    "hypotheses": "HYP",
    "analyses": "ANA",
    "options": "OPT",
    "appraisals": "APL",
    "assumptions": "ASM",
    "risks": "RSK",
    "meetings": "MTG",
    "client_inputs": "CIN",
    "decisions": "DEC",
    "open_questions": "OQ",
    "actions": "ACT",
    "communications": "COM",
    "approvals": "APV",
    "deliverables": "DEL",
}
ID_WIDTH: dict[str, int] = {"sources": 4, "evidence": 4}


def model_for(collection: str) -> type[Envelope]:
    try:
        return COLLECTIONS[collection]
    except KeyError as exc:
        raise KeyError(f"unknown collection {collection!r}; known: {', '.join(sorted(COLLECTIONS))}") from exc
