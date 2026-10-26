# Document structures

Section-by-section structures for every Horus deliverable type: what each section must contain, its typical length and the state records it draws on. Structures are fixed across engagements; content and pathway emphasis vary.

When Horus uses this: when the Principal outlines a deliverable in the storyboard, when `producer` checks completeness and length ceilings in the logic audit, and when a pathway pack names its core Tier 2 documents.

## Rules common to every document

- One storyline across tiers: memo, executive summary, deck and report share the governing thought and the evidence IDs.
- Numbered paragraphs, exhibits titled as full sentences with a source line, hard length ceilings, stamps and markings from design-system.md.
- Recommendations are worded as decisions and kept apart from the analysis; the analysis carries no opinion (BENCHMARKS.md C3).
- Standing sections that are never dropped: implementation, consultation and stakeholder positions, communications, legal and financial implications, monitoring (BENCHMARKS.md synthesis 8 and 9).
- The `type` named for each structure is the `deliverables.type` value in STATE_SCHEMA.md F1.

## Decision memo (`decision_memo`, T0)

Benchmarks: the UK ministerial submission (C1: DWP template and "Working with Ministers"), the Australian Cabinet Handbook paragraph 97 (C2), Canada's two-part memorandum (C3) and the two-page US presidential memo (C4). Two A4 pages, readable in five minutes, 12 pt, headings are the form fields.

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Title block | Subject as a noun phrase naming the decision; to and from; date; reference; marking (3 lines) | `deliverables.title`, `engagement.client`, `stakeholders[client_role=ultimate_decision_maker]` |
| Issue | The decision needed, why now, and the financial impact in one figure (100 words or fewer) | `brief.problem_statement.as_reframed`, `analyses[kind=baseline]`, `appraisals.summary` |
| Recommendation | Numbered items worded "Agree that" or "Note that", each decidable alone; the do-nothing option named and rejected explicitly; "noting" items kept to a minimum (3 to 5 items, 120 words) | `decisions[kind=recommendation]`, `options[status=recommended]`, `options[kind=do_nothing]` |
| Timing | A date and its reason: cabinet slot, budget cycle, legal deadline or political calendar (2 lines) | `workplan.milestones`, `analyses[kind=decision_maker_lens]` as framing only |
| Discussion | In this order: impact; evidence (at most five numbers, each footnoted); options considered and why rejected; financial and legal implications; risks; consultation and stakeholder positions by group; communications and handling (600 to 800 words) | `appraisals.impacts`, `appraisals.feasibility`, `evidence`, `options.screening`, `risks`, `stakeholders.stance` aggregated by category, `analyses[kind=stakeholder_reaction_matrix]`, `analyses[kind=communication_plan]` |
| Implementation | Owners, first milestones, budget line, instruments required (100 words) | `analyses[kind=implementation_plan]` |
| Decision required | Approve, approve with amendments, reject or discuss, with a signature and date line (4 lines) | `meetings.decisions_sought` |
| Annex pointer | The Tier 1 executive summary and the Tier 2 documents by title and DEL id (1 line) | `deliverables` |

The five-to-eight-slide Tier 0 brief follows the order in slide-archetypes.md and repeats the memo's numbers exactly.

## Executive summary and executive deck (`executive_summary`, `executive_deck`, T1)

Executive summary: stands alone, under 1,000 words; opens with a one-sentence problem statement of at most 25 words (B11); then the answer in one paragraph; three to five numbered findings with footnoted numbers; the recommendation with a table split into short-term (within 12 months) and medium-term (one to three years) actions (B8); decisions and next steps. Executive deck, 10 to 15 slides: cover, executive-summary, road-marker, two to three diagnosis slides, one to two option slides, two to three appraisal slides, recommendation and roadmap, risks, decisions-sought, next-steps. Both draw on the storyboard key line, `decisions`, `analyses[kind=implementation_plan]` and the records behind each archetype.

## Policy note (`policy_note`, T2; at most about 40 pages or 10,000 words)

Benchmarks: the HKS policy analysis exercise (B11) and World Bank policy notes (B8).

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Executive summary | As above, under 1,000 words, printable separately (2 to 3 pages) | storyboard, `decisions` |
| Context and mandate | Mandate as given and reframed; objectives OBJ-n; scope; how the work was done (2 pages) | `brief`, `approach.methodology_narrative` |
| Problem and baseline | Problem definition; baseline and counterfactual with the gap quantified; why intervene; past attempts (4 to 5 pages) | `analyses[kind=baseline, diagnostic, benchmark]`, `hypotheses`, `evidence` |
| Stakeholder landscape and public sentiment | Positions by group with interests and red lines; sentiment themes with caveats (2 to 3 pages) | `stakeholders` by category, `analyses[kind=public_sentiment]`, `meetings.interview_record` under attribution rules |
| Guiding principles | The validated principles and directives, each with what it rules in or out (1 page) | `decisions[kind=guiding_principle, political_directive]` |
| Options | Long list by the pathway's option logic; screening and shortlist with reasons; each shortlisted option with its theory of change (4 to 6 pages) | `options`, `analyses[kind=options_screening]` |
| Appraisal and comparison | Method and proportionality; impacts by dimension and by who bears them; comparison against do-nothing; sensitivity (5 to 7 pages) | `appraisals`, `assumptions`, `analyses[kind=option_comparison]` |
| Recommendation | The recommended option or package; table split short term and medium term with owners (2 pages) | `decisions[kind=recommendation]`, `options[status=recommended]` |
| Implementation and activation plan | Sequencing, instruments, institutions, budget, capacity, delivery chain (3 to 4 pages) | `analyses[kind=implementation_plan]` |
| Communication plan | Narrative, message house, audiences, sequencing, opposition handling (2 pages) | `analyses[kind=communication_plan]` |
| Risks | Register with owners and mitigations (1 to 2 pages) | `risks` |
| Monitoring and evaluation | Indicators with baselines and targets; evaluation timing and method (1 to 2 pages) | `appraisals.monitoring` |
| Annexes | Method and assumptions; evidence and traceability table; consultation synopsis by group; glossary | `assumptions`, `evidence`, `sources`, `meetings` |

## RIA report (`ria_report`, regulatory pathway; main report at most 40 pages excluding annexes)

Benchmarks: OECD basic steps (B1), European Commission Tool 11 (B3), UK framework and template (B4, B5).

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Context | Political and legal context; the mandate; how the assessment was done and its proportionality level (2 pages) | `brief`, `appraisals.proportionality_level`, `appraisals.standards_applied` |
| What is the problem and why | Problem tree, drivers, scale, who is affected; baseline and how it evolves without action; evaluation of existing rules first (4 to 5 pages) | `analyses[kind=baseline, diagnostic]`, `evidence` |
| Why intervene at this level | Legal basis and the case for acting at national, sub-national or supranational level (1 page) | `appraisals.feasibility.legal`, `evidence[kind=legal_provision]` |
| SMART objectives | General and specific objectives, measurable, with target dates (1 page) | `brief.objectives`, `decisions[kind=guiding_principle]` |
| Options with theory of change | Do-nothing plus the shortlisted instruments, each with inputs, activities, outputs, outcomes, impacts and key assumptions; discarded options with reasons (4 to 5 pages) | `options.mechanism`, `options.screening` |
| Impacts and who is affected | Economic, social and environmental impacts by dimension; compliance and administrative costs by the standard cost model; SMEs, competition, distribution (8 to 10 pages) | `appraisals.impacts`, `appraisals.regulatory.compliance_cost_scm`, `appraisals.distributional`, `assumptions` |
| Comparison | Options against the objectives and each other on effectiveness, efficiency and coherence; summary table against do-nothing (3 pages) | `analyses[kind=option_comparison]`, `appraisals.summary` |
| Preferred option | Choice and reasons; proportionality; SME test; competition check; enforcement and compliance strategy; review clause (3 pages) | `appraisals.regulatory`, `decisions[kind=preferred_option]` |
| Monitoring and evaluation | Indicators, data sources, frequency, owner, evaluation date (1 to 2 pages) | `appraisals.monitoring` |
| Annexes | Procedural information; consultation synopsis by stakeholder group; who-is-affected table with summary costs and benefits; methods and assumptions; sensitivity; competitiveness check | `meetings`, `stakeholders`, `appraisals.sensitivity`, `assumptions`, `appraisals.artefacts` |

## Strategy document (`strategy_document`, strategy pathway; 30 to 50 pages)

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Executive summary | Under 1,000 words | storyboard |
| Where we are | Diagnosis, benchmarks, trends and scenarios, capabilities and assets (6 to 8 pages) | `analyses[kind=strategic_position, benchmark, scenario_analysis, diagnostic]` |
| Where we want to be | Vision; objectives; dated, measurable targets (2 to 3 pages) | `brief.objectives`, `decisions[kind=guiding_principle]` |
| How we get there | Pillars and initiatives, each with owner, scope and expected contribution (8 to 10 pages) | `options[kind=strategic_choice]`, `appraisals[kind=strategic_options]` |
| Sequencing and roadmap | Phases, quick wins, dependencies (2 to 3 pages) | `analyses[kind=implementation_plan].sequencing` |
| Resources and governance | Budget envelope, institutional arrangements, decision rights (2 to 3 pages) | `analyses[kind=implementation_plan].budget` and `.institutional_arrangements` |
| KPIs and review cycle | Indicators with baselines and targets; review cadence (2 pages) | `analyses[kind=implementation_plan].kpis` |
| Risks | Register with mitigations (1 to 2 pages) | `risks` |
| Annexes | Methods, scenario assumptions, benchmark detail, evidence table | `assumptions`, `evidence` |

## Operating-model blueprint (`operating_model_blueprint`, institutional pathway; 30 to 50 pages)

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Mandate and purpose | What the entity or system exists to do; legal basis (2 pages) | `brief`, `evidence[kind=legal_provision]` |
| Current-state diagnostic | Mandates and overlaps, functions, decision rights, capability maturity, incentives, political economy (6 to 8 pages) | `analyses[kind=institutional_diagnostic]`; `analyses[kind=internal_politics]` distilled to institutional findings only |
| Design principles | Validated principles for the target model (1 page) | `decisions[kind=guiding_principle]` |
| Target model | Functions, structure, decision rights (RAPID), governance, capabilities, systems (8 to 10 pages) | `options[kind=operating_model, status=recommended]`, `appraisals[kind=operating_model]` |
| Options considered and why | Archetypes compared on fit, cost, capability, transition risk and legal change (3 to 4 pages) | `appraisals.operating_model`, `analyses[kind=option_comparison]` |
| Transition plan and quick wins | Phases, interim arrangements, first 100 days (3 pages) | `analyses[kind=implementation_plan]` |
| Legal and regulatory changes | Inventory of instruments to amend or issue with owner and timing (1 to 2 pages) | `appraisals.operating_model.legal_changes_required`, `analyses[kind=implementation_plan].instruments_required` |
| Risks and change management | Register; communication to staff and stakeholders (2 pages) | `risks`, `analyses[kind=communication_plan]` |
| Annexes | Governance charter draft, decision-rights matrix, evidence table | `deliverables[type=governance_charter]`, `evidence` |

## Business case (`business_case`, public investment pathway; strategic outline or outline level)

Benchmark: HM Treasury Green Book and the Five Case Model (B6).

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Executive summary | Under 1,000 words; the stage named (2 to 3 pages) | storyboard |
| Strategic case | Case for change, business as usual, up to six SMART objectives, fit with policy (4 to 6 pages) | `analyses[kind=strategic_case]`, `brief.objectives` |
| Economic case | Long list to shortlist; social CBA or CEA against business as usual; optimism bias; sensitivity and switching values; distributional analysis; the appraisal summary table (8 to 12 pages) | `appraisals[kind=business_case]`, `appraisals.five_case.economic`, `assumptions`, `deliverables[type=appraisal_summary_table]` |
| Commercial case | Procurement route, risk allocation, contract form (2 to 4 pages) | `appraisals.five_case.commercial`, `deliverables[type=financing_options_paper]` |
| Financial case | Affordability against the budget envelope, funding sources, cash flow (2 to 3 pages) | `appraisals.five_case.financial` |
| Management case | Governance, delivery plan, benefits realisation, risk management, evaluation (3 to 4 pages) | `appraisals.five_case.management`, `analyses[kind=implementation_plan]` |
| Recommendation and next approval stage | The option to carry forward and what the next stage must prove (1 page) | `decisions[kind=recommendation]` |
| Annexes | Appraisal summary table, model documentation, assumptions register, optimism-bias workings | `appraisals.artefacts`, `assumptions` |

## Delivery plan (`delivery_plan`, transformation pathway; 20 to 40 pages)

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Aspiration and targets | The outcome, the dated target, the baseline (2 pages) | `brief.objectives`, `analyses[kind=baseline]` |
| Delivery chain and bottlenecks | Who does what from policy to citizen; where performance is lost (4 to 6 pages) | `analyses[kind=delivery_chain]` |
| Interventions | Delivery interventions appraised on trajectory, effort and dependencies (4 to 6 pages) | `options[kind=delivery_intervention]`, `appraisals[kind=delivery_intervention]` |
| Trajectories | Baseline, target and intervention paths by indicator (2 to 4 pages) | `appraisals.delivery.trajectory` |
| Routines | Stocktakes, dashboards, escalation; the dashboard specification (2 to 3 pages) | `analyses[kind=implementation_plan]`, `deliverables[type=dashboard_specification]` |
| Roles and capability | Owners, delivery unit, capability plan (2 pages) | `analyses[kind=implementation_plan].capacity_needs`, `stakeholders` |
| Risks | Register (1 to 2 pages) | `risks` |
| Annexes | Data definitions, trajectory models | `appraisals.artefacts` |

## Programme or service design document (`service_design_document`, programme pathway; 25 to 40 pages)

| Section | Must contain (typical length) | Draws on |
|---|---|---|
| Problem and users | User groups, journeys, barriers, take-up and cost to serve (4 to 6 pages) | `analyses[kind=user_and_service_research]`, `evidence` |
| Outcomes sought | Outcomes with indicators and targets; theory of change (2 pages) | `brief.objectives`, `options.mechanism` |
| Service concept and blueprint | The concept; blueprint by stage (user, front stage, back stage, systems) (6 to 8 pages) | `options[kind=service_concept]`, `deliverables[type=service_blueprint]` |
| Eligibility, channels and behavioural design | Rules, channels, behavioural levers with evidence (3 to 4 pages) | `options.design_parameters`, `evidence` |
| Operating and cost model | Volumes, staffing, systems, cost per outcome (3 to 4 pages) | `appraisals[kind=service_concept]`, `appraisals.service.cost_per_outcome` |
| Pilot and evaluation plan | Design, sample, duration, evaluation method, decision rule for scaling (2 to 3 pages) | `appraisals.service.pilot_design`, `deliverables[type=pilot_evaluation_plan]` |
| Scaling path | Phases and preconditions (1 to 2 pages) | `analyses[kind=implementation_plan]` |
| Annexes | Research instruments, journey maps, evidence table | `evidence`, `meetings` |

## Phase decks (T1)

- **Kickoff deck** (`kickoff_deck`, 12 to 18 slides, AP1): cover; executive-summary (our understanding and proposed approach); context-mandate; problem-issue-tree with hypotheses; pathway and methodology (6+6 text); roadmap-delivery-chain for the workplan with gates and cadence; governance-raci; stakeholder-landscape by group with interviews requested; data requests as a next-steps table; decisions-sought (approve approach and workplan, authorise interviews and data requests); next-steps. Draws on `brief`, `approach`, `workplan`, `hypotheses`, `stakeholders.engagement`, `actions[kind=client_request_data, client_request_meeting]`.
- **Diagnostic deck** (`diagnostic_deck`, 12 to 20 slides, AP2): cover; executive-summary (the diagnosis); road-marker; baseline-trend; three to five finding slides (baseline-trend, benchmark-table, sentiment-snapshot, stakeholder-landscape by group); hypothesis status on the issue tree; solution-space preview (option-landscape, long list only); decisions-sought (accept findings; confirm or revise the pathway); next-steps. Draws on `analyses[kind=baseline, diagnostic, benchmark, public_sentiment]`, `hypotheses`, `evidence`, `meetings.interview_record` under attribution rules, `options[status=long_list]`. The decision-maker lens and internal politics shape the framing and never appear as slides.
- **Principles deck** (`principles_deck`, 10 to 15 slides, AP3): cover; executive-summary; option-landscape; screening-funnel; one slide per shortlisted option (mechanism, target groups, precedents); principles-directives as proposed; political-directive questions as decisions-sought; reaction summary by stakeholder group; proposed criteria and weights; next-steps. Draws on `options`, `analyses[kind=options_screening, stakeholder_reaction_matrix]`, `decisions[kind=guiding_principle, political_directive, criteria_weights; status=proposed]`.
- **Appraisal deck** (`appraisal_deck`, 12 to 18 slides plus a T2 method annex, AP4): cover; executive-summary; road-marker; baseline restated; appraisal-comparison; cba-waterfall for the leading option or each quantified option; distributional-incidence; sensitivity-tornado; risk-matrix with feasibility; preferred option and why; decisions-sought (preferred option); next-steps. Method annex as back-up: standards applied, proportionality, baseline, assumptions register, impact tables by dimension, model artefacts, caveats. Draws on `appraisals`, `assumptions`, `risks`, `analyses[kind=option_comparison]`, `decisions[kind=criteria_weights]`.

## Internal and recurring documents

- **Meeting plan** (`meeting_plan`, 2 to 4 pages) mirrors `meetings.plan` and §4.3 step 1: header (MTG id, participants and roles, date, platform, conduct mode, time budget, language); objectives (at most three); decisions sought for gate meetings, or hypotheses to test and open questions to close for interviews; question guide (id, question, priority 1 to 3, purpose, tests HYP or OQ, follow-up heuristics); follow-up rules; sensitivities and do-not-say list; disclosure script id and text; consent terms and proposed attribution rule; escalation rules (objection, distress, confidential disclosure, Supervisor whisper or pause); time plan by block; close script; approval record. Template in formats-and-templates.md. Draws on `meetings`, `stakeholders`, `profiles` (internal use only, never quoted), `hypotheses`, `open_questions`, `approvals`.
- **Interview debrief** (`interview_debrief`, 1 to 2 pages): positions by topic with EVD ids; reactions to options; surprises; contradictions with hypotheses and proposed hypothesis patches; proposed stakeholder patch (stance, reactions); documents promised and referrals; suggested follow-ups; question-guide coverage; Supervisor interventions received; what worked and what to change. Draws on `meetings.interview_record`, `meetings.notes.structured`, `meetings.live`, `meetings.debrief`, `evidence` with its `attribution`, `actions`.
- **Weekly status note** (`status_note`, T2 to the client PM, one page): headline sentence on where the engagement stands against the workplan; progress this week (three to five bullets with activity ids); next week; decisions and inputs needed from the client, each with a date; risks and issues with RAG glyphs; interview tracker (held, scheduled, outstanding by priority); data requests outstanding with ages; upcoming milestones. Draws on `workplan.activities` and `.milestones`, `actions` (overdue computed), `open_questions[status=awaiting_client]`, `risks[scope=engagement]`, `meetings`, `deliverables.versions`.

## Proposed schema additions

- `deliverables.type`: add `decision_brief` for the Tier 0 five-to-eight-slide brief, which today can only be recorded as `executive_deck` at `tier: T0` or as `other`.

Source: structures from ARCHITECTURE.md §7.5 and §4.1; ministerial-submission form from BENCHMARKS.md C1 (DWP template and "Working with Ministers"), C2 and C3; executive-summary and policy-note conventions from B11 (HKS) and B8 (World Bank); RIA structure from B1, B3, B4 and B5; business case from B6.
