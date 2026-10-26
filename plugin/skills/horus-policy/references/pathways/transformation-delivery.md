# Transformation and delivery pathway

Make an existing policy or programme deliver, or set up the capacity to do so (a delivery unit, routines, a performance regime). The method is delivery-chain analysis with performance data, delivery interventions and routines as the option space, and a trajectory-based appraisal of interventions against targets with cost, effort, dependency and risk.

When Horus uses this: as the primary pathway when the policy design is accepted and the gap is between intention and results (enum value `transformation_delivery`); as a secondary pathway on every other pathway for the implementation plan's routines and trajectories.

## Classification signals

- A policy, programme or target already exists and is underperforming: missed targets, slow roll-out, regional variation, backlog, unspent budget, poor citizen outcomes despite spending.
- The RFP asks for implementation support, a delivery plan, a delivery unit, a performance management framework, a stocktake, a turnaround or a "why is it not working" review.
- Performance data exist or can be assembled by period and by unit; the client is a centre of government, a delivery unit, a ministry's programme directorate or an agency head.
- Counter-signals: the design itself is wrong (programme and service design or regulatory); the institution's mandate is the obstacle (institutional and operating model); the brief is to set new direction (strategy); the programme needs funding approval (public investment).

## Diagnostic lens

Delivery-chain analysis with performance data. P2 produces, at `reviewed` before AP2:

- `analyses` of kind `delivery_chain`: actors, links, what flows, lags, link scores (expectation, capacity and incentive, visibility), bottlenecks, with data by region or unit.
- `analyses` of kind `baseline`: the indicator time series with seasonality and trend, the target, the implementation gap decomposed by driver, region or segment.
- `analyses` of kind `diagnostic`: readiness against the five disciplines (leadership, priorities, cadence, communication, capability) and the stocktake and data practices in place; past interventions and their effect.
- `analyses` of kind `benchmark`: how comparable systems closed similar gaps, with evaluated effects and lags.
- `analyses` of kind `internal_politics` and `decision_maker_lens`: whether the principal will chair routines, who owns data, who is blamed today.
- Interviews: front-line units and intermediaries at suspected bottlenecks, data owners, the programme directorate, the finance ministry (funding release), professional bodies and unions.

Hypotheses are of kind `implementation` (where the chain leaks and why), `causal` (which fix would move the indicator) and `political` (what routines the principal will sustain).

## Option logic

Options are records of kind `delivery_intervention`, each attached to the bottleneck it fixes: shortening the chain or clarifying expectations (guidance, standards, templates); changing incentives (performance agreements, funding rules, recognition); adding visibility (data returns, dashboards, league tables used carefully); adding capacity (staff, tooling, training, surge teams); changing routines (stocktakes, delivery reports, priority reviews); and set-up options for a delivery unit or equivalent capacity, which are appraised as operating-model options under the institutional pack. Each option carries a theory of change, an expected contribution to the trajectory with lag and ramp-up, effort and cost, and dependencies. Screening uses contribution to the gap, time to effect, cost and effort, dependency on others, and acceptability to the actors who must perform. The shortlist is a set of interventions whose contributions plausibly sum to the target; packages bundle interventions with the routines that sustain them.

## Appraisal method

Appraisal kind `delivery_intervention`, `pathway: transformation_delivery`.

- Standards applied: Barber's delivery method (Deliverology, 2011; How to Run a Government, 2015) as the method reference; `OECD-DAC-2019` criteria for the evaluation design; `HMT-Green-Book-2026` for cost conventions where interventions need spending; the five disciplines (McKinsey Center for Government, 2018) for the readiness assessment.
- Methodology: `cea` (cost per unit of trajectory gain) with `mixed` where effort and feasibility are rated; `proportionality_level` usually `standard`.
- Toolkit modules: `trajectories` for baseline, target and intervention series; `cea` for cost per unit of gain; `scenarios` for downside and delayed-effect cases; `montecarlo` where contribution ranges are wide; `report` for trajectory charts and the intervention comparison.
- Method-specific block, required: `delivery {trajectory {baseline_series, target_series, intervention_series}, bottlenecks_addressed[], effort, dependencies[]}`.
- Impact dimensions typically assessed: the programme's outcome dimension (for example `health_and_safety`, `economic_output`, `employment`), `fiscal_cost`, `administrative_feasibility`, `political_feasibility`, `distributional_equity` (which regions or groups gain first), `digital_and_data`.
- Common blocks: `baseline` (the time series), `impacts[]`, `distributional`, `feasibility`, `sensitivity` on contribution and lag assumptions, `risks` with `early_warning` tied to trajectory variance, `monitoring` with the stocktake indicators and cadence.

## Stakeholder emphasis

The principal who must chair stocktakes (decision_role `decide`; the feasibility of routines depends on their time); the responsible ministers and programme owners (`agree`, `perform`); front-line units and intermediaries whose behaviour must change (`perform`; interviewed, not only surveyed); data owners; the finance ministry for funding release and incentives; professional bodies and unions where front-line practice changes; citizens as the outcome's beneficiaries. Reaction matrices are built for the delivery actors as much as for the political level, because interventions fail at the link that resists.

## Core Tier-2 deliverables and structures

- `delivery_plan`: aspiration and targets; delivery chain and bottlenecks; interventions; trajectories; routines (stocktakes, dashboards); roles and capability; risks; annexes.
- Routines and stocktake design: cadence, chair, attendees, agenda and format of stocktakes, the delivery report template and rating rules, priority review triggers and the problem-solving protocol; produced as the routines chapter of the delivery plan or as an `implementation_plan` deliverable.
- `dashboard_specification`: indicators with definitions, sources, frequency, lags, owners, trajectories, variance rules and the views for each audience.
- Capability plan: skills, roles and data capacity needed at each link, with sequencing and budget; produced within the delivery plan set.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification records the targets or indicators in scope and the availability of performance data by period and unit.
- AP1: frameworks selected include delivery-chain analysis and trajectories; data requests cover the indicator series; interview priority 1 includes front-line and intermediary actors, not only headquarters.
- AP2: `delivery_chain` and `baseline` at `reviewed` with time series and link scores evidenced by data and interviews; the gap decomposed; readiness assessed.
- AP3: shortlisted interventions each mapped to a bottleneck with a contribution range; routines proposed as part of the option set; guiding principles cover the use of data and consequences.
- AP4: every shortlisted intervention has a `delivery_intervention` appraisal with a trajectory; the intervention series sum to a stated share of the target with a shortfall declared; dependencies and effort recorded.
- AP5: `delivery_plan` and `dashboard_specification` released; routines have a chair, cadence and first date; each KPI has baseline, target, source, frequency and owner; the capability plan is costed.

## Frameworks

Framing and diagnosis: `delivery-chain-analysis`, `hypothesis-driven-problem-solving`, `pdia-problem-deconstruction`, `institutional-diagnostic`, `cpi-public-impact-fundamentals`, `theory-of-change`. Stakeholders: `rapid-decision-rights`, `mendelow-power-interest`, `net-map-influence`, `political-calendar`. Options: `international-benchmarking`, `policy-packaging-and-sequencing`, `behavioural-toolkits-basic-east`, `operating-model-archetypes` (delivery unit set-up). Appraisal: `delivery-trajectories`, `cost-effectiveness-analysis`, `scenario-analysis`, `pilot-and-evaluation-design`, `distributional-and-gender-impact`. Implementation and communication: `deliverology-and-delivery-units`, `five-disciplines-government-transformation`, `logframe-and-dac-criteria`, `raci`, `pyramid-principle`, `scqa`, `message-house`, `strategic-communication-for-reform`, `cabinet-paper-conventions`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md A1 (McKinsey five disciplines of government transformation), A3 (engagement rhythm: one-slide workplan, weekly check-in decks, working-draft stamps), A5 (CPI Fundamentals: action), B13 (Government Outcomes Lab: outcomes and value for money), B6 (Green Book monitoring and evaluation chapter), C1 to C4 (decision memo conventions). The catalogue flags delivery plans and delivery-unit routines (UK Prime Minister's Delivery Unit material, Barber's publications) as a gap to close before this pack is finalised.

## Typical pitfalls

- Diagnosing from headquarters; the leaks are at the front line and in intermediaries.
- Targets without trajectories, and trajectories drawn as straight lines without intervention logic or lags.
- Too many priorities and too many interventions; the method works with a handful of each.
- Routines designed for a principal who will not chair them.
- Dashboards full of indicators nobody owns, with no variance rule that triggers action.
- Treating a design failure as a delivery failure; if the chain is sound and the outcome still fails, revisit the classification at AP2.
- Capability treated as headcount rather than incentives, data and skills at the weak link.

## Proposed schema additions

- `deliverables.type`: pathway-core values `routines_design` and `capability_plan`, so the routines and stocktake design and the capability plan are tracked as deliverables in their own right.
- `analyses.content` shape for kind `delivery_chain`: `outcome {indicator, baseline, target}`, `actors[] → STK`, `links[] {from, to, flows[], instrument, lag, scores {expectation, capacity_incentive, visibility}, evidence}`, `bottlenecks[] {link, finding, evidence}`.
