"""Central enumerations (STATE_SCHEMA.md §4)."""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:  # YAML-friendly
        return self.value


class Phase(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    closed = "closed"


class Gate(StrEnum):
    AP0 = "AP0"
    AP1 = "AP1"
    AP2 = "AP2"
    AP3 = "AP3"
    AP4 = "AP4"
    AP5 = "AP5"


class GateStatus(StrEnum):
    not_ready = "not_ready"
    ready = "ready"
    passed = "passed"


class Confidentiality(StrEnum):
    public = "public"
    client_confidential = "client-confidential"
    sensitive_personal = "sensitive-personal"


class Confidence(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Priority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Pathway(StrEnum):
    regulatory = "regulatory"
    strategy = "strategy"
    institutional_operating_model = "institutional_operating_model"
    transformation_delivery = "transformation_delivery"
    public_investment_business_case = "public_investment_business_case"
    programme_service_design = "programme_service_design"


class AutonomyLevel(StrEnum):
    auto = "auto"
    notify = "notify"
    approve = "approve"
    human = "human"


class ActionClass(StrEnum):
    research_and_analysis = "research_and_analysis"
    state_write = "state_write"
    deliverable_production = "deliverable_production"
    interview_plan = "interview_plan"
    interview_conduct = "interview_conduct"
    stakeholder_email = "stakeholder_email"
    client_pm_email = "client_pm_email"
    decision_maker_email = "decision_maker_email"
    tier0_tier1_release = "tier0_tier1_release"
    tier2_release = "tier2_release"
    gate_transition = "gate_transition"
    gate_meeting = "gate_meeting"
    meeting_scheduling = "meeting_scheduling"


class ConductMode(StrEnum):
    interviewer = "interviewer"
    principal_co_led = "principal_co_led"
    human = "human"


class ApprovalStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    expired = "expired"
    not_required = "not_required"


class RiskClass(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class StakeholderKind(StrEnum):
    person = "person"
    organisation = "organisation"
    group = "group"
    public_segment = "public_segment"


class StakeholderCategory(StrEnum):
    client_decision_maker = "client_decision_maker"
    client_pm = "client_pm"
    client_internal = "client_internal"
    government_executive = "government_executive"
    legislature = "legislature"
    regulator = "regulator"
    judiciary = "judiciary"
    subnational_government = "subnational_government"
    state_owned_enterprise = "state_owned_enterprise"
    political_party = "political_party"
    industry_association = "industry_association"
    private_firm = "private_firm"
    labour = "labour"
    civil_society = "civil_society"
    academia_or_think_tank = "academia_or_think_tank"
    media = "media"
    international_organisation = "international_organisation"
    donor_or_dfi = "donor_or_dfi"
    public_segment = "public_segment"


class ClientRole(StrEnum):
    pm = "pm"
    sponsor = "sponsor"
    ultimate_decision_maker = "ultimate_decision_maker"
    steering = "steering"
    working_level = "working_level"
    none = "none"


class DecisionRole(StrEnum):
    recommend = "recommend"
    agree = "agree"
    perform = "perform"
    input = "input"
    decide = "decide"
    none = "none"


class Stance(StrEnum):
    champion = "champion"
    supportive = "supportive"
    neutral = "neutral"
    sceptical = "sceptical"
    opposed = "opposed"
    unknown = "unknown"


class Reaction(StrEnum):
    support = "support"
    conditional = "conditional"
    neutral = "neutral"
    resist = "resist"
    block = "block"


class RelationshipType(StrEnum):
    reports_to = "reports_to"
    oversees = "oversees"
    allied_with = "allied_with"
    rival_of = "rival_of"
    influences = "influences"
    funds = "funds"
    regulates = "regulates"
    member_of = "member_of"
    advises = "advises"


class SourceTier(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class SourceType(StrEnum):
    peer_reviewed = "peer_reviewed"
    official_statistics = "official_statistics"
    legal_text = "legal_text"
    government_document = "government_document"
    io_report = "io_report"
    think_tank_report = "think_tank_report"
    consultancy_report = "consultancy_report"
    poll = "poll"
    dataset = "dataset"
    news = "news"
    trade_press = "trade_press"
    advocacy = "advocacy"
    company = "company"
    encyclopaedic = "encyclopaedic"
    social_media = "social_media"
    speech_or_statement = "speech_or_statement"
    parliamentary_record = "parliamentary_record"
    interview = "interview"
    client_document = "client_document"
    other = "other"


class EvidenceKind(StrEnum):
    fact = "fact"
    statistic = "statistic"
    estimate = "estimate"
    quote = "quote"
    finding = "finding"
    legal_provision = "legal_provision"
    event = "event"
    position = "position"
    forecast = "forecast"


class Corroboration(StrEnum):
    single_source = "single_source"
    corroborated = "corroborated"
    contested = "contested"
    refuted = "refuted"


class Attribution(StrEnum):
    on_record = "on_record"
    background = "background"
    not_for_attribution = "not_for_attribution"


class InstrumentType(StrEnum):
    regulation = "regulation"
    economic_incentive = "economic_incentive"
    tax_or_fee = "tax_or_fee"
    subsidy_or_grant = "subsidy_or_grant"
    information_or_disclosure = "information_or_disclosure"
    direct_provision = "direct_provision"
    organisational_or_institutional = "organisational_or_institutional"
    co_regulation = "co_regulation"
    voluntary_or_standard = "voluntary_or_standard"
    behavioural_nudge = "behavioural_nudge"
    procurement = "procurement"


class OptionKind(StrEnum):
    regulatory_instrument = "regulatory_instrument"
    strategic_choice = "strategic_choice"
    operating_model = "operating_model"
    delivery_intervention = "delivery_intervention"
    investment_option = "investment_option"
    service_concept = "service_concept"
    package = "package"
    do_nothing = "do_nothing"


class OptionStatus(StrEnum):
    long_list = "long_list"
    screened_out = "screened_out"
    short_list = "short_list"
    appraised = "appraised"
    preferred = "preferred"
    recommended = "recommended"
    rejected = "rejected"
    merged = "merged"


class AppraisalKind(StrEnum):
    ria = "ria"
    strategic_options = "strategic_options"
    operating_model = "operating_model"
    delivery_intervention = "delivery_intervention"
    business_case = "business_case"
    service_concept = "service_concept"
    other = "other"


class Methodology(StrEnum):
    cba = "cba"
    cea = "cea"
    mca = "mca"
    scm = "scm"
    qualitative = "qualitative"
    mixed = "mixed"


class ImpactDimension(StrEnum):
    economic_output = "economic_output"
    fiscal_cost = "fiscal_cost"
    fiscal_revenue = "fiscal_revenue"
    business_compliance_cost = "business_compliance_cost"
    administrative_burden = "administrative_burden"
    consumer_welfare = "consumer_welfare"
    competition = "competition"
    sme = "sme"
    employment = "employment"
    distributional_equity = "distributional_equity"
    gender_and_inclusion = "gender_and_inclusion"
    environment = "environment"
    health_and_safety = "health_and_safety"
    legal_and_institutional = "legal_and_institutional"
    administrative_feasibility = "administrative_feasibility"
    political_feasibility = "political_feasibility"
    international_obligations = "international_obligations"
    innovation = "innovation"
    digital_and_data = "digital_and_data"


class MeetingKind(StrEnum):
    kickoff = "kickoff"
    pm_checkin = "pm_checkin"
    steering = "steering"
    interview = "interview"
    workshop = "workshop"
    readout = "readout"
    final_presentation = "final_presentation"
    internal = "internal"


class MeetingStatus(StrEnum):
    proposed = "proposed"
    requested = "requested"
    scheduled = "scheduled"
    joining = "joining"
    in_progress = "in_progress"
    held = "held"
    cancelled = "cancelled"
    no_show = "no_show"
    aborted = "aborted"


class DecisionKind(StrEnum):
    scope = "scope"
    pathway = "pathway"
    methodology = "methodology"
    workplan = "workplan"
    guiding_principle = "guiding_principle"
    political_directive = "political_directive"
    shortlist = "shortlist"
    criteria_weights = "criteria_weights"
    preferred_option = "preferred_option"
    recommendation = "recommendation"
    deliverable_approval = "deliverable_approval"
    gate = "gate"
    autonomy = "autonomy"
    supervisor_directive = "supervisor_directive"
    process = "process"
    other = "other"


class DecisionStatus(StrEnum):
    proposed = "proposed"
    confirmed = "confirmed"
    superseded = "superseded"
    reversed = "reversed"


class ClientInputKind(StrEnum):
    feedback = "feedback"
    directive = "directive"
    guiding_principle_input = "guiding_principle_input"
    approval = "approval"
    rejection = "rejection"
    request = "request"
    document_provided = "document_provided"
    data_provided = "data_provided"
    clarification = "clarification"
    instruction = "instruction"
    preference = "preference"


class ActionKind(StrEnum):
    internal_task = "internal_task"
    client_request_data = "client_request_data"
    client_request_document = "client_request_document"
    client_request_meeting = "client_request_meeting"
    client_request_decision = "client_request_decision"
    stakeholder_outreach = "stakeholder_outreach"
    follow_up = "follow_up"
    approval_needed = "approval_needed"


class ActionStatus(StrEnum):
    todo = "todo"
    requested = "requested"
    in_progress = "in_progress"
    blocked = "blocked"
    done = "done"
    cancelled = "cancelled"


class OpenQuestionStatus(StrEnum):
    open = "open"
    awaiting_client = "awaiting_client"
    answered = "answered"
    parked = "parked"
    closed = "closed"


class DeliverableTier(StrEnum):
    T0 = "T0"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"


class DeliverableVersionStatus(StrEnum):
    draft = "draft"
    qa_failed = "qa_failed"
    qa_passed = "qa_passed"
    in_review = "in_review"
    operator_approved = "supervisor_approved"
    sent = "sent"
    client_approved = "client_approved"
    superseded = "superseded"


class DeliverableStatus(StrEnum):
    planned = "planned"
    in_progress = "in_progress"
    delivered = "delivered"
    accepted = "accepted"
    closed = "closed"


class Channel(StrEnum):
    email = "email"
    message = "message"
    letter = "letter"
    portal = "portal"
    call_note = "call_note"
    meeting_chat = "meeting_chat"


class Direction(StrEnum):
    inbound = "inbound"
    outbound = "outbound"


class AnalysisKind(StrEnum):
    problem_classification = "problem_classification"
    problem_framing = "problem_framing"
    issue_tree = "issue_tree"
    baseline = "baseline"
    diagnostic = "diagnostic"
    strategic_position = "strategic_position"
    institutional_diagnostic = "institutional_diagnostic"
    delivery_chain = "delivery_chain"
    strategic_case = "strategic_case"
    user_and_service_research = "user_and_service_research"
    benchmark = "benchmark"
    scenario_analysis = "scenario_analysis"
    public_sentiment = "public_sentiment"
    internal_politics = "internal_politics"
    decision_maker_lens = "decision_maker_lens"
    stakeholder_reaction_matrix = "stakeholder_reaction_matrix"
    options_screening = "options_screening"
    option_comparison = "option_comparison"
    implementation_plan = "implementation_plan"
    communication_plan = "communication_plan"
    research_memo = "research_memo"
    interview_debrief = "interview_debrief"
    other = "other"


class HypothesisStatus(StrEnum):
    untested = "untested"
    testing = "testing"
    supported = "supported"
    refuted = "refuted"
    revised = "revised"
    dropped = "dropped"


class EventOp(StrEnum):
    create = "create"
    update = "update"
    append = "append"
    link = "link"
    delete = "delete"
    checkpoint = "checkpoint"
    gate_change = "gate_change"
    phase_change = "phase_change"
    approval = "approval"
    intervention = "intervention"
    validate = "validate"
    import_ = "import"
    export = "export"
