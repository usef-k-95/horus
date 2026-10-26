# Programme and service design pathway

Design or redesign a public programme or service for citizens or firms: who is eligible, what they receive, through which channels, with what behavioural design, at what cost per outcome. The method is user and journey research with a service blueprint, service concepts as the option space, and a service concept evaluation on outcomes, take-up, cost per outcome, equity and feasibility with a pilot and evaluation design.

When Horus uses this: as the primary pathway when the object is a service or programme experienced by users (enum value `programme_service_design`); as a secondary pathway when a regulatory, investment or transformation engagement includes a citizen-facing or firm-facing service.

## Classification signals

- The RFP asks to design, redesign, modernise, digitise or evaluate a programme or service: a benefit, a grant, a permit or registration service, a health, education, employment or social service, a one-stop shop.
- Language of eligibility, take-up, enrolment, user journey, channels, front line, case management, cost to serve, service standard, citizen-centric, behavioural barriers, pilot.
- The client is a service-owning ministry or agency, a digital government unit, a social protection or SME programme authority, or a donor-funded programme unit.
- Required deliverables are a programme or service design document, a blueprint, a pilot plan or an operating and cost model.
- Counter-signals: the service is fine and the delivery system is the gap (transformation and delivery); a legal instrument defines the service and must change (regulatory); the funding of a facility is the decision (public investment); the body that runs the service is the question (institutional).

## Diagnostic lens

User and service research. P2 produces, at `reviewed` before AP2:

- `analyses` of kind `user_and_service_research`: user segments by need, capability and channel access; the current journey with steps, time, cost to the user, failure points and drop-off; behavioural barriers at each step (ability, motivation, opportunity); front-line and back-stage processes; cost to serve by channel.
- `analyses` of kind `baseline`: eligible population, current take-up and coverage by segment, outcomes achieved, unit costs and the business-as-usual projection.
- `analyses` of kind `benchmark`: comparable services elsewhere, their design choices and evaluated take-up and outcomes.
- `analyses` of kind `public_sentiment`: how users and the public perceive the service and the institution providing it.
- `analyses` of kind `delivery_chain` for the back-stage view where several bodies deliver.
- Interviews and research: users in each segment including non-users, front-line staff, intermediaries (NGOs, local offices, accountants for firms), data owners, the finance ministry, the data protection authority.

Hypotheses are of kind `diagnostic` (why take-up or outcomes fall short), `causal` (which barrier binds), `option_effect` (what each design change would do) and `implementation` (what the front line can operate).

## Option logic

Options are records of kind `service_concept`, each a complete proposition: eligibility and verification rules; the benefit or service and its level; channels (digital, assisted digital, telephone, face-to-face, intermediaries) with the cost to serve and reach of each; behavioural design at the moments that decide take-up and persistence (defaults, prompts, simplification, timing); redress and exceptions; the operating model behind it, including outcomes-based commissioning where it fits; and the pilot that would test the critical link. Options are generated with the service concept and channel design method, EAST and BASIC, and Hood's resources for the instrument mix. Screening uses expected outcomes and take-up by segment, cost per outcome, equity (who is left out), feasibility for the front line and the data available, and legal and data-protection constraints. The shortlist is two or three service concepts plus the current service improved; variants adjust eligibility thresholds, benefit levels and channel mix.

## Appraisal method

Appraisal kind `service_concept`, `pathway: programme_service_design`.

- Standards applied: the UK Government Service Standard (2019) and the Australian Digital Service Standard as design standards; `OECD-BASIC-2019` for behavioural design and ethics; `UK-Magenta-Book-2020` for pilot and evaluation design; `HMT-Green-Book-2026` for cost-effectiveness and distributional conventions; `OECD-DAC-2019` for evaluation criteria where donors are involved; the EU SME test where firms are the users.
- Methodology: `cea` (cost per outcome) with `mixed` where equity and feasibility are rated; `cba` where outcomes are credibly monetisable; `proportionality_level` usually `standard`.
- Toolkit modules: `cea` for cost per outcome under take-up ranges; `distribution` for coverage and exclusion by segment; `montecarlo` on take-up and unit-cost assumptions; `scenarios` for demand and channel-shift cases; `cba` where used; `report` for the comparison table, blueprint exhibits and incidence charts.
- Method-specific block, required: `service {outcomes[], take_up_estimate, cost_per_outcome, equity_assessment, pilot_design {design, sample, duration, evaluation_method}}`.
- Impact dimensions typically assessed: the outcome dimension (`health_and_safety`, `employment`, `economic_output`, `consumer_welfare`), `fiscal_cost`, `administrative_burden` (on users), `distributional_equity`, `gender_and_inclusion`, `digital_and_data`, `administrative_feasibility`, `sme` where firms are users.
- Common blocks: `baseline`, `impacts[]`, `distributional` (coverage and exclusion by segment), `feasibility`, `sensitivity` on take-up and unit costs, `risks` of scope `policy_outcome` and `implementation`, `monitoring` with indicators placed on the theory of change and the evaluation design.

## Stakeholder emphasis

Users by segment as `public_segment` stakeholders, typically high interest and low power, which is the equity warning; non-users; front-line staff and their representatives; intermediaries and civil-society organisations that reach excluded groups; the data protection authority and identity providers; the finance ministry; the digital government unit; the legislature where eligibility is set in law. Salience analysis is used to ensure dependent stakeholders are heard; the behavioural ethics check applies to how users are nudged.

## Core Tier-2 deliverables and structures

- `service_design_document`: problem and users; outcomes sought; service concept and blueprint; eligibility, channels and behavioural design; operating and cost model; pilot and evaluation plan; scaling path; annexes.
- `service_blueprint`: user actions, front-stage interactions, back-stage processes and supporting systems by step, with the moments that decide take-up, the hand-offs that carry risk, and the channel and cost to serve at each step.
- `pilot_evaluation_plan`: evaluation questions from the theory of change, design, sample and power, duration, data and consent, pre-specified analysis and decision rule, governance, budget and reporting dates aligned to the political calendar; the post-implementation evaluation.
- Cost-to-serve summary: unit costs by channel and segment, fixed and variable costs, the cost per outcome under take-up scenarios; produced within the design document and as an appraisal artefact.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification records the users, the outcomes sought and whether eligibility is set in law.
- AP1: frameworks selected include service concept design, a behavioural toolkit and theory of change; the research plan covers each user segment including non-users; data requests cover take-up, outcomes and unit costs.
- AP2: `user_and_service_research` and `baseline` at `reviewed` with segments, journey, barriers and cost to serve evidenced; benchmark of comparable services exists.
- AP3: shortlisted service concepts each have a theory of change with the critical link identified; guiding principles cover equity, channel policy and the use of behavioural levers; the data-protection constraints are recorded.
- AP4: every shortlisted concept has a `service_concept` appraisal with `cost_per_outcome` under take-up ranges, `equity_assessment` by segment and a `pilot_design`; sensitivity run on take-up and unit costs.
- AP5: `service_design_document`, `service_blueprint` and `pilot_evaluation_plan` released; the operating and cost model names the delivery organisation and channels; the pilot has a decision rule, an owner and a reporting date.

## Frameworks

Framing and diagnosis: `theory-of-change`, `hypothesis-driven-problem-solving`, `delivery-chain-analysis`, `cpi-public-impact-fundamentals`, `pdia-problem-deconstruction`. Stakeholders: `stakeholder-salience`, `mendelow-power-interest`, `net-map-influence`, `political-calendar`. Options: `service-concept-design`, `behavioural-toolkits-basic-east`, `hood-tools-of-government`, `international-benchmarking`, `policy-packaging-and-sequencing`, `investment-option-framing` (where capital is needed). Appraisal: `cost-effectiveness-analysis`, `distributional-and-gender-impact`, `pilot-and-evaluation-design`, `eu-sme-test` (firms as users), `standard-cost-model` (user burden), `scenario-analysis`, `multi-criteria-analysis`. Implementation and communication: `logframe-and-dac-criteria`, `government-outcomes-lab`, `delivery-trajectories`, `raci`, `pyramid-principle`, `scqa`, `message-house`, `strategic-communication-for-reform`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md A5 (CPI Public Impact Fundamentals: legitimacy, policy, action), B13 (Government Outcomes Lab: outcomes-based contracting and value for money), B11 (Harvard Kennedy School policy analysis exercise, document structure), B3 (EU Better Regulation Toolbox: SME test and Standard Cost Model where firms are users), B6 (Green Book: cost-effectiveness and distributional analysis), B8 (World Bank policy note conventions), C1 to C4 (decision memo conventions). The catalogue flags public service design documents (UK Government Digital Service and Australian Digital Transformation Agency service standards and blueprints) as a gap to close before this pack is finalised.

## Typical pitfalls

- Designing for the median user; equity depends on the segments without documents, connectivity or literacy.
- Digital-only channels justified by cost to serve, with no assisted route.
- Take-up assumed at the eligible population; use precedents and show ranges.
- Nudging around a structural barrier; if the benefit is wrong or the form unusable, no message fixes it.
- Blueprints that stop at the front stage; back-stage hand-offs are where services fail.
- A pilot designed to succeed: volunteer sites, no comparison, outcomes chosen afterwards.
- User research skipped because the client knows the users; the service standard requires evidence.

## Proposed schema additions

- `deliverables.type`: a pathway-core value `cost_to_serve_summary`, so the cost model is tracked and QA'd as its own deliverable.
- `analyses.content` shape for kind `user_and_service_research`: `segments[] {name, size, needs, channel_access, evidence}`, `journey[] {step, actor, channel, time, user_cost, failure_rate, evidence}`, `barriers[] {step, type: ability|motivation|opportunity, evidence}`, `cost_to_serve[] {channel, unit_cost, volume, evidence}`.
