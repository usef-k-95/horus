# Institutional and operating-model pathway

Redesign the mandates, governance, organisation and decision rights of an entity or a system of entities. The method is an institutional diagnostic with political-economy analysis, operating-model archetypes as the option space, and an operating-model assessment of fit to mandate, cost, capability, transition risk, legal change and political feasibility.

When Horus uses this: as the primary pathway when the question is who should do what, under which governance, with which powers (enum value `institutional_operating_model`); as a secondary pathway when another pathway's preferred option needs a new or changed institution.

## Classification signals

- The RFP concerns an institution: create, merge, split, reposition or review an agency, authority, ministry unit, regulator, state-owned enterprise or coordination body; or the governance of a system of bodies.
- Language of mandate, functions, overlaps, duplication, decision rights, autonomy, accountability, board, oversight, capability review, functional review.
- A capability or performance review of an entity where the suspected cause is design rather than effort.
- The client is a centre of government, a public service commission, a finance or planning ministry reviewing bodies, or the entity itself.
- Counter-signals: the entity's design is sound and delivery routines are the gap (transformation and delivery); the issue is a rule the entity enforces (regulatory); a programme's service model rather than its home (programme and service design).

## Diagnostic lens

The institutional diagnostic. P2 produces, at `reviewed` before AP2:

- `analyses` of kind `institutional_diagnostic`: mandate and overlaps (functions-by-institution matrix), functions and process baseline with volumes and costs, decision-rights map (RAPID on paper and in practice), capability maturity by function, incentives and accountability, environment; root causes classified as design, capacity or environment.
- `analyses` of kind `internal_politics`: units, positions by option, influence paths and watch points inside the client entity and the bodies affected.
- `analyses` of kind `benchmark`: two to four peer institutions by mandate, governance form, size and performance.
- `analyses` of kind `delivery_chain` where the entity sits on a delivery chain whose performance is the presenting problem.
- `profiles` of the entity (structure, factions assessed) and its leaders, kept at `sensitive-personal`, distilled into `decision_maker_lens`.
- Interviews: the entity's leadership and middle management, its overseers, its clients and counterparts, the finance ministry, unions and staff representatives, former leaders.

Hypotheses are of kind `diagnostic` (root causes), `political` (which mandate shifts the system will accept) and `implementation` (what transition the administration can carry). PDIA deconstruction and the change-space test shape the interview guides.

## Option logic

Options are records of kind `operating_model`. The long list is generated from the operating-model archetypes (ministerial directorate, executive agency, independent regulator, public corporation or operator, network or shared service, regulator-operator split) and from governance options within each (board composition, appointment rules, performance agreements, funding model). Each option specifies the functions in and out, the design dimensions as `design_parameters[]` (distance from ministerial direction, legal form, funding, governance, accountability instruments, separation of policy, regulation and delivery), a RAPID table for the critical decisions, the legal changes required and a transition path with quick wins. The status quo improved is always an option. Screening uses fit to the diagnosed root causes, legal change required, capability needed, cost delta, transition risk and political feasibility. The shortlist is two or three target models plus the status quo improved; variants adjust autonomy, funding or scope; packages pair a target model with a staged transition.

## Appraisal method

Appraisal kind `operating_model`, `pathway: institutional_operating_model`.

- Standards applied: OECD public governance review practice and World Bank institutional assessment practice as method references; the DCLG multi-criteria analysis manual (2009) for scoring; `HMT-Green-Book-2026` for cost delta and transition cost conventions; `IMF-PIMA-2018` where the entity manages public investment.
- Methodology: `mca` with `mixed` where cost deltas are quantified; `proportionality_level` `standard` or `full` for system-wide redesigns.
- Toolkit modules: `mca` for the criteria matrix and rank robustness; `cba` for cost delta and transition costs over the horizon; `scenarios` for transition risk under different political and fiscal conditions; `report` for the operating-model comparison exhibit.
- Method-specific block, required: `operating_model {fit_to_mandate, capability_gap, transition_risk, legal_changes_required[], cost_delta}`.
- Impact dimensions typically rated: `legal_and_institutional`, `administrative_feasibility`, `political_feasibility`, `fiscal_cost`, `economic_output` where the entity's performance affects a sector, `employment` for staff effects, `digital_and_data` for systems.
- Common blocks: `baseline` (status quo projected), `impacts[]`, `distributional` (effects on regions, staff groups, clients), `feasibility` with `legal` detailed by instrument, `sensitivity` on transition assumptions, `risks` of scope `implementation`, `legal` and `political`, `monitoring` with governance indicators.

## Stakeholder emphasis

The entities that gain and lose functions, budgets and staff (interests are structural; stated positions understate them); ministers who lose or gain oversight; the finance ministry (funding model, headcount) and the public service commission (staff transfer rules); unions and staff representatives; the entity's clients and regulated parties; the legislature where a law changes mandates; courts where vires or employment rights are engaged. RAPID is mapped for the decisions that create and govern the entity. Political-economy analysis is central and most of its findings stay in profiles and the internal politics map; deliverables carry implications without naming rivalries.

## Core Tier-2 deliverables and structures

- `operating_model_blueprint`: mandate and purpose; current-state diagnostic; design principles; target model (functions, structure, decision rights, governance, capabilities, systems); options considered and why; transition plan and quick wins; legal and regulatory changes; risks and change management; annexes.
- `governance_charter`: purpose and legal basis; governing body composition, appointment and tenure; decision rights (RAPID table); relationship with the minister and with overseers; performance framework and reporting; funding and financial rules; transparency and review.
- `transition_plan`: sequenced steps (legal, financial, staff, systems, communications) with owners, dates, dependencies, quick wins and the governance of the transition.
- Inventory of legal and regulatory changes: every provision to enact, amend or repeal, with instrument, owner and session; produced as the blueprint's legal chapter and as `implementation_plan.content.instruments_required[]`.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification records the entities in scope and whether primary law governs their mandates.
- AP1: frameworks selected include an institutional diagnostic method, political-economy analysis and RAPID; the client entity profile is started; interview priority 1 covers the entity's leadership and overseers.
- AP2: `institutional_diagnostic`, `internal_politics` and `benchmark` at `reviewed`; root causes classified as design, capacity or environment; decision-rights map on paper and in practice.
- AP3: shortlist includes the status quo improved and at least two archetypes with RAPID tables and legal routes; design principles confirmed as guiding principles.
- AP4: every shortlisted model has an `operating_model` appraisal with `legal_changes_required[]` and `cost_delta`; transition risk assessed under scenarios; staff and client effects in `distributional`.
- AP5: `operating_model_blueprint`, `governance_charter` and `transition_plan` released; the legal inventory names instrument, owner and session for every change; quick wins have owners and dates.

## Frameworks

Framing and diagnosis: `institutional-diagnostic`, `political-economy-analysis`, `pdia-problem-deconstruction`, `delivery-chain-analysis`, `hypothesis-driven-problem-solving`, `cpi-public-impact-fundamentals`. Stakeholders: `rapid-decision-rights`, `mendelow-power-interest`, `net-map-influence`, `veto-players-and-coalitions`, `political-calendar`, `stakeholder-salience`. Options: `operating-model-archetypes`, `international-benchmarking`, `policy-packaging-and-sequencing`, `wef-agile-regulation` (for regulator design). Appraisal: `multi-criteria-analysis`, `green-book-five-case-model`, `scenario-analysis`, `imf-pima`, `distributional-and-gender-impact`. Implementation and communication: `raci`, `deliverology-and-delivery-units`, `five-disciplines-government-transformation`, `pyramid-principle`, `scqa`, `message-house`, `strategic-communication-for-reform`, `cabinet-paper-conventions`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md B8 (World Bank materials), B9 (IMF staff paper and board paper conventions; PIMA where relevant), A1 (five disciplines for the transition plan), A5 (CPI Fundamentals: legitimacy and action), B2 (OECD 2012 Recommendation on oversight bodies and regulatory agencies), C1 to C4 (decision memo conventions). The catalogue flags operating-model and institutional reviews (UK Cabinet Office capability reviews, OECD public governance reviews, World Bank institutional assessments) as gaps to close before this pack is finalised.

## Typical pitfalls

- Reorganising boxes without changing decision rights, funding or incentives; the diagnostic's design-capacity-environment classification exists to stop this.
- One target model presented as inevitable; scrutiny expects real alternatives including the status quo improved.
- Transition cost and time underestimated, especially legal change, staff transfers and systems.
- Independence designed without accountability instruments anyone will operate.
- Sensitive judgements about named leaders leaking into client-facing material; they belong in profiles.
- Benchmarking agencies from different legal traditions without saying what does not transfer.
- Forgetting the finance ministry and the public service commission until the appraisal; they hold Agree roles on every structural change.

## Proposed schema additions

- `deliverables.type`: a pathway-core value `legal_change_inventory`, so the legal inventory can be tracked and QA'd as its own deliverable rather than as a chapter of the blueprint.
- `analyses.content` shape for kind `institutional_diagnostic`: `mandate {functions[], overlaps[], gaps[]}`, `decision_rights[] {decision, paper: RAPID map, practice: RAPID map}`, `capability[] {function, maturity 1 to 5, evidence}`, `incentives[]`, `root_causes[] {statement, class: design|capacity|environment, evidence}`.
