# Logical framework and OECD DAC evaluation criteria

The logframe is a four-by-four matrix (goal, outcome, outputs, activities against indicators, means of verification and assumptions) that turns a theory of change into a management and monitoring tool. The OECD DAC criteria (relevance, coherence, effectiveness, efficiency, impact, sustainability) are the standard questions for evaluating a programme. Horus uses both for programme design and for monitoring and evaluation sections across pathways.

When Horus uses this: P5 on the programme and service design pathway (anchor) and the transformation pathway for monitoring design; P2 when evaluating a past programme; whenever a donor or development finance institution will read the deliverable.

## What it is

The logical framework approach originated with USAID around 1970 and became the standard format for development project design in the EU's project cycle management guidelines and most donors' templates. Rows are the results chain: overall objective or impact, specific objective or outcome, outputs, activities (sometimes with inputs). Columns are the objectively verifiable indicators with baselines and targets, the sources and means of verification, and the assumptions or risks that must hold for each level to lead to the next. The DAC criteria, revised in 2019 by the OECD DAC Network on Development Evaluation, ask: relevance (is the intervention doing the right things), coherence (how well does it fit with other interventions and policies), effectiveness (is it achieving its objectives), efficiency (how well are resources used), impact (what difference does it make) and sustainability (will the benefits last). The criteria are applied thoughtfully, not mechanically, and with judgement about which matter for the evaluation at hand.

## When Horus uses it

- Programme and service design pathway: the service design document carries a logframe derived from the theory of change; the pilot and evaluation plan uses DAC criteria for the evaluation questions.
- Transformation pathway: the delivery plan's KPIs and the dashboard specification are the indicator and verification columns of a logframe.
- P2 on any pathway: an ex post review of a past programme is structured by the DAC criteria to explain why it underperformed.
- Donor-facing engagements: logframes and DAC criteria are expected formats; the policy note's monitoring and evaluation section adopts them.
- Regulatory and investment pathways: the monitoring framework and benefits realisation plan borrow the indicator discipline.

## Steps

1. **Start from the theory of change** of the preferred option; collapse it into the four logframe levels.
2. **Write indicators** per level: specific, measurable, with baseline, target and date; prefer existing administrative data.
3. **Specify means of verification**: source, frequency, responsible party, cost of collection.
4. **State assumptions** between levels, drawn from the theory of change's key assumptions, with the evidence grade; convert fatal assumptions into risks with mitigations or redesign.
5. **Check vertical logic** (if activities and assumptions hold, outputs follow, and so on) and horizontal logic (indicators measure the level, verification is feasible).
6. **Design the evaluation** against the DAC criteria: which criteria matter most here, which questions under each, what design answers them, when.
7. **Embed in management**: who reviews the indicators, how often, and what triggers action.

## Outputs → state records

- `options.mechanism` (the theory of change) as the source; `appraisals.monitoring {indicators[] {name, baseline, target, source, frequency, owner}, evaluation {when, method}}`.
- `analyses` of kind `implementation_plan` with `kpis[] {name, baseline, target, source, frequency}`; the full logframe table in `narrative_path` or as an artefact.
- `assumptions` records for the logframe's assumption column, linked from `options.mechanism.key_assumptions`; `risks` where assumptions are fatal.
- `deliverables` of type `service_design_document`, `pilot_evaluation_plan`, `delivery_plan`, `dashboard_specification`; the monitoring and evaluation section of `policy_note` and `ria_report`.
- Ex post use: `analyses` of kind `diagnostic` structured by the DAC criteria with `findings[]`.

## Pitfalls

- Logframes written after the design to satisfy a template, disconnected from the theory of change.
- Indicators that measure activity (workshops held) at the outcome level.
- Assumptions column used for platitudes ("political stability continues") rather than the specific conditions the mechanism needs.
- Applying all six DAC criteria with equal weight regardless of the question; the 2019 revision asks for judgement.
- Means of verification that require data nobody collects and no budget to collect it.

## Source

OECD DAC Network on Development Evaluation, Better Criteria for Better Evaluation: Revised Evaluation Criteria Definitions and Principles for Use, 2019; European Commission, Project Cycle Management Guidelines, 2004 (logical framework approach); origin in USAID's logical framework work around 1970.
