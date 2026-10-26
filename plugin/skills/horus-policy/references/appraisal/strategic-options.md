# Strategic options appraisal

Multi-criteria analysis of strategic choices against the validated guiding principles, stress-tested against scenarios and costed to an order of magnitude, with the rank robustness that tells a steering committee whether the answer depends on the weights.

When Horus uses this: strategy pathway, phase P4, appraisal kind `strategic_options`; also for the strategic layer of a hybrid (a strategy with a regulatory component appraises the strategic choices here and the instruments with `ria.md`).

## What is being appraised

Strategic choices, not instruments: the level of ambition, where to focus (sectors, regions, segments), how to deliver (state, market, partnership) and sequencing. Options of kind `strategic_choice` or `package` from the short list, each with a `mechanism` and `design_parameters`. The baseline is the current strategy continued (`do_nothing`), described by its projected trajectory on the headline indicators (`scenarios.project`).

## Criteria and weights

Criteria come from two places only: the confirmed guiding principles (decisions of kind `guiding_principle`) and the brief's objectives (OBJ ids). Each criterion is one principle or objective, written so that higher is unambiguously better or flagged `higher_is_better=False` (cost, burden, transition risk). Weights are the confirmed `criteria_weights` decision from AP3 (`guiding-principles.md`); the analyst never sets or adjusts them, and `strategic.criteria_weights` points to that decision.

Tests before scoring: no two criteria measure the same thing (otherwise it is double-weighted); every criterion discriminates between at least two shortlisted options; cost appears once, either as a criterion or in a separate cost-effectiveness read-out, not both; feasibility is scored in `feasibility` and shown beside the attractiveness score rather than folded into it, so the decision maker sees desirability and deliverability separately.

## Scoring

Score each option on each criterion on a 0 to 10 scale with a one-line rationale and evidence IDs; a cell is a claim and follows the evidence rules. Where a criterion has a natural metric (fiscal cost, jobs, emissions), score the metric and let normalisation handle the scale. Scores are recorded in the `option_comparison` analysis `table` and summarised in `appraisals.impacts` with a `rating` from −3 to +3 per dimension.

The analyst runs `mca.mca(raw, criteria)` with `raw` as `{option: {criterion: score}}` and `criteria` as a list of `mca.Criterion(name, weight, higher_is_better)`. `mca.normalise` applies min-max normalisation to 0 to 1 per criterion and flips the direction where lower is better; `mca.weighted_scores` divides by the total weight so the weighted score is also 0 to 1. `MCAResult` carries `scores`, `ranking`, `normalised` and `robustness`.

Min-max normalisation is relative to the short list: adding or removing an option changes every normalised score. Say so in `method_notes` and re-run after any change to the short list.

## Rank robustness

`mca.mca` perturbs every weight by up to plus or minus 20 per cent (`perturbation=0.2`) over 2,000 draws (`robustness_runs`) with a fixed `seed` and reports each option's probability of ranking first. Horus reads it as: 0.8 or above, the ranking is robust to reasonable disagreement about weights; 0.5 to 0.8, sensitive, so name the criteria whose weight flips the ranking; below 0.5, fragile, so present the leading options as a tie and let the principles and the scenario results decide. Record the read-out in `sensitivity.robustness` and show the probability of ranking first beside every score in the appraisal deck. Also report the ranking under equal weights and with each principle's weight set to zero in turn, which is the question steering members actually ask. In the toolkit demo the leading option ranks first in 71 per cent of draws (illustrative): sensitive, not robust.

## Scenario stress tests

Scenarios are the external futures the strategy cannot control: fiscal space, growth, technology, geopolitics, demographic or climate shocks. Build two to four from the P2 `scenario_analysis` (or build it now), each with a name, its drivers and their values, and a probability judgement where one is defensible. For each option and scenario, record the performance: re-score the criteria the scenario moves and re-run `mca.mca`, or rate performance qualitatively (strong, adequate, weak, fails) with a rationale. The result goes to `strategic.scenario_results[] {scenario, performance}`. An option that wins the central case but fails a plausible scenario is a bet; say so and look for the robust alternative or the hedge (a package with an option to switch). Scenario performance is reported beside the ranking, never averaged into it.

Use `scenarios.project(start, growth, years, step_changes)` for quantified drivers and `report.line_chart_svg` to show the headline indicator under each scenario with the option's series highlighted.

## Order-of-magnitude costing

Strategy options are costed to a class, not a budget: for each option, the one-off and recurring cost over the strategy horizon as a range (a minus 30 to plus 50 per cent band around a central figure, or classes such as under 10 million, 10 to 100 million, 100 million to 1 billion), built bottom-up from unit costs × volumes for the main initiatives and cross-checked against precedents in the ledger (`options.precedents`). Every unit cost and volume is an `assumptions` record. Present the fiscal envelope from the `political_directive` decision beside the range. Record in `strategic.order_of_magnitude_cost` with the band, the price base year and the method; discount with `cba.present_value` only when a horizon-weighted comparison is needed, and name the schedule.

## The `strategic` block

`criteria_weights` (→ DEC, the confirmed `criteria_weights` decision), `scenario_results[] {scenario, performance}` (one entry per scenario, performance as the re-scored rank or the qualitative rating with rationale) and `order_of_magnitude_cost` (band, price base year, method, envelope comparison). All three are required by rule 20.

## Common blocks

As for every appraisal: `baseline`; `impacts` by dimension with who bears them (qualitative ratings are normal here; monetise only the fiscal rows); `summary` with `mca_score` and `rank`; `distributional` (which regions, sectors or groups the focus choice favours); `feasibility` (administrative, legal, political, evidence-based; `feasibility-scoring.md`); `risks`; `monitoring` (the strategy's KPIs with baselines and targets); `caveats`; `artefacts` (the scoring table as CSV, the robustness output, charts).

## Pitfalls

Using MCA to avoid a cost-benefit analysis that could credibly be done on part of the option; criteria that restate each other (growth, jobs, investment); scoring without rationale; letting the analyst tune weights; a single ranking with no robustness; treating scenario performance as another criterion to be averaged away; costing to false precision; a short list of one serious option and two straw men, which min-max normalisation rewards.

Source: Department for Communities and Local Government (UK), Multi-criteria analysis: a manual (2009); HM Treasury, The Green Book (2022), on the options framework filter and the limits of weighting and scoring; Bardach and Patashnik, A Practical Guide for Policy Analysis (7th edition, 2023), steps 4 to 6; Schwartz, The Art of the Long View (1991) for scenario planning practice.
