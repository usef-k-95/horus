# Strategy pathway

Set a direction over a horizon for a nation, a sector or an institution: vision, objectives, pillars, initiatives, sequencing and KPIs. The method is situational analysis with benchmarks, trends and scenarios, strategic choices as the option space, and multi-criteria appraisal against validated principles with scenario stress-testing and order-of-magnitude costing.

When Horus uses this: as the primary pathway when the brief asks where to go and how, across several instruments, rather than for one instrument, one funding decision or one institution (enum value `strategy`); frequently with a secondary regulatory, investment or institutional pathway for specific pillars.

## Classification signals

- The RFP asks for a strategy, vision, roadmap, policy direction, national or sectoral plan, or a review of an existing strategy.
- A horizon of five to fifteen years; objectives and targets to be set rather than given; several ministries or agencies involved.
- The client is a planning ministry, a head of government's office, a sector ministry or an agency setting its own direction.
- The required deliverable is a strategy document, a roadmap or a policy note, not a RIA or a business case.
- Evidence expected is trends, benchmarks and scenarios rather than legal analysis, performance data or a demand forecast.
- Counter-signals: a single instrument decision hides behind the strategy language (regulatory); an existing strategy is not being delivered (transformation and delivery); the question is really who should own the agenda (institutional).

## Diagnostic lens

Situational analysis. P2 produces, at `reviewed` before AP2:

- `analyses` of kind `strategic_position`: where the country, sector or institution stands on the dimensions that matter (performance, capabilities, assets, constraints), what has been tried, what the existing strategies say and what they delivered; a review of capability and asset endowments.
- `analyses` of kind `benchmark`: comparators' positions and the strategies they pursued, with evaluated results.
- `analyses` of kind `scenario_analysis`: driving forces, critical uncertainties and three or four scenarios for the horizon.
- `analyses` of kind `baseline`: the business-as-usual projection of the headline indicators.
- `analyses` of kind `public_sentiment`, `decision_maker_lens` and `internal_politics`: what the decision maker wants to be remembered for, what the public will accept, which ministries will resist.
- Interviews: the decision maker's circle, ministries and agencies that would own pillars, business and labour representatives, academics, international partners.

Hypotheses are of kind `diagnostic` (the binding constraints), `causal` (why past strategies underdelivered) and `political` (the ambition the coalition can carry). The CPI Fundamentals and Bardach's steps 1 and 2 are the framing checks.

## Option logic

Options are records of kind `strategic_choice`. The option space is built along four questions: ambition (how far and how fast on the headline objectives); focus (which sectors, segments, regions or problems to prioritise); delivery (which instruments and which institutions carry each pillar); and sequencing (what first, what later, what conditional). Each coherent combination is a strategic option with a vision statement, three to five pillars, the main initiatives per pillar and an order-of-magnitude cost. Options differ in logic, not in wording. Each pillar carries a theory of change; initiatives that are themselves regulatory instruments, investments or institutional changes are flagged for the secondary pathway's method. Screening uses alignment with the candidate guiding principles, fit with scenarios, feasibility and the reaction matrix; the shortlist is two or three strategic options plus the status quo strategy. Packages are used to combine pillars across options.

## Appraisal method

Appraisal kind `strategic_options`, `pathway: strategy`.

- Standards applied: the DCLG multi-criteria analysis manual (2009) for the method; `HMT-Green-Book-2026` for order-of-magnitude costing and the options framework; `OECD-RIA-2020` or `Five-Case-Model` for pillars that are regulatory or investment components, recorded on those components' own appraisals.
- Methodology: `mca` with `mixed` where parts are costed; `proportionality_level` usually `standard`.
- Toolkit modules: `mca` for criteria normalisation, weighted scoring and rank robustness; `scenarios` for performance under each scenario; `cba` for order-of-magnitude cost ranges and, where credible, benefit ranges; `montecarlo` on the costing where ranges are wide; `distribution` where pillars have uneven incidence; `report` for the comparison matrix and scenario charts.
- Method-specific block, required: `strategic {criteria_weights: → DEC, scenario_results[] {scenario, performance}, order_of_magnitude_cost}`.
- Criteria come from the guiding principles confirmed at AP3 and the SMART objectives; weights are a `criteria_weights` decision made by the client; scores carry evidence; robustness analysis reports which rankings survive weight variation.
- Impact dimensions typically rated: `economic_output`, `employment`, `fiscal_cost`, `distributional_equity`, `gender_and_inclusion`, `environment`, `innovation`, `administrative_feasibility`, `political_feasibility`.
- Common blocks as on every pathway, with `monitoring.indicators[]` becoming the strategy's KPIs.

## Stakeholder emphasis

The decision maker's priorities and legacy (decision-maker lens); the ministries and agencies that would own pillars (RAPID: who will Perform and who must Agree); the finance ministry for the fiscal envelope; political parties and the legislature for durability beyond the term (veto players); business, labour and civil society for legitimacy; the public for the Overton window on ambition. Stances are tracked against pillars and initiatives, because support for a vision rarely predicts support for its hard choices. International partners and donors matter where financing or accession anchors the strategy.

## Core Tier-2 deliverables and structures

- `strategy_document`: executive summary; where we are (diagnosis, benchmarks, trends); where we want to be (vision, objectives, targets); how we get there (pillars and initiatives with owners); sequencing and roadmap; resources and governance; KPIs and review cycle; risks; annexes.
- `implementation_roadmap`: initiatives by pillar with owners, dates, dependencies, instruments required, budget envelopes, quick wins and the governance that reviews progress.
- `policy_note`: the standard structure, used where the client needs a shorter, decision-oriented document alongside the strategy.
- `implementation_plan` and `communication_plan` annexes.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification records the horizon, the breadth of instruments and any components that belong to a secondary pathway.
- AP1: frameworks selected include a framing method, a benchmarking protocol and scenario analysis; workstreams map to the candidate pillars.
- AP2: `strategic_position`, `benchmark`, `scenario_analysis` and `baseline` at `reviewed`; the business-as-usual projection of headline indicators exists; candidate objectives drafted.
- AP3: candidate guiding principles cover ambition, focus, delivery and sequencing; strategic options differ in logic; criteria derived from principles and objectives; `criteria_weights` confirmed by the client after the workshop.
- AP4: every shortlisted strategic option has a `strategic_options` appraisal with scenario results and order-of-magnitude cost; robustness analysis reported; secondary-pathway components appraised with their own kind.
- AP5: `strategy_document` and `implementation_roadmap` released; every KPI has baseline, target, source and frequency; owners named for every initiative; a review cycle dated.

## Frameworks

Framing and diagnosis: `bardach-eightfold-path`, `hypothesis-driven-problem-solving`, `cpi-public-impact-fundamentals`, `roamef-and-strategic-case`, `political-economy-analysis`, `theory-of-change`. Stakeholders: `mendelow-power-interest`, `rapid-decision-rights`, `veto-players-and-coalitions`, `overton-window`, `political-calendar`, `net-map-influence`. Options: `international-benchmarking`, `policy-packaging-and-sequencing`, `hood-tools-of-government`, `investment-option-framing`, `operating-model-archetypes`. Appraisal: `multi-criteria-analysis`, `scenario-analysis`, `green-book-five-case-model`, `distributional-and-gender-impact`, `cost-effectiveness-analysis`. Implementation and communication: `five-disciplines-government-transformation`, `deliverology-and-delivery-units`, `raci`, `logframe-and-dac-criteria`, `pyramid-principle`, `scqa`, `message-house`, `strategic-communication-for-reform`, `cabinet-paper-conventions`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md B12 (Bardach's Eightfold Path), B11 (Harvard Kennedy School policy analysis exercise, document structure), A5 (CPI Public Impact Fundamentals), A1 (McKinsey five disciplines, for the implementation chapter), A3 (public-record consulting decks: road markers, action titles, quantified case for change), B8 (World Bank policy notes for incoming governments: short-term versus medium-term action tables), B6 (Green Book options framework and costing), C1 to C4 (decision memo conventions). The catalogue flags national and sector strategy documents as a gap to close before this pack is finalised.

## Typical pitfalls

- A vision with pillars that are ministries' existing programmes relabelled; options must differ in logic.
- Objectives without baselines or targets, so the strategy cannot fail and cannot be reviewed.
- Analyst-set criteria weights; weights are the client's values recorded as a decision.
- Scenarios used as decoration rather than as a stress test that changes the ranking or adds hedges.
- Costing avoided because "this is a strategy"; order-of-magnitude ranges are expected.
- No owner, no instrument and no date for initiatives, which makes the roadmap a wish list.
- Ignoring durability: a strategy that the opposition will reverse needs cross-party anchoring or a shorter horizon.
