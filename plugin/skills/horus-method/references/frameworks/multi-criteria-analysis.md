# Multi-criteria analysis

A structured way to compare options against several criteria that cannot all be monetised: define criteria from agreed objectives and principles, score each option on each criterion with evidence, weight the criteria through the decision makers, combine, and test whether the ranking survives changes in weights and scores. Horus uses it as the appraisal method on the strategy pathway and as a complement to cost-benefit analysis elsewhere.

When Horus uses this: P3 to set criteria and weights at the principles workshop, P4 as the appraisal method for `strategic_options` and `operating_model` appraisals and as a supplementary method in RIAs and business cases; the toolkit's `mca` module implements it.

## What it is

Multi-criteria analysis (MCA), in the form codified for UK government by Dodgson, Spackman, Pearman and Phillips, is a family of techniques for ordering options on multiple objectives. The common linear additive model scores each option on each criterion on a common scale, multiplies by criterion weights that express the decision makers' relative valuation of a unit change on each criterion, and sums. The manual's steps are: establish the decision context; identify options; identify criteria and sub-criteria; score options against criteria; weight the criteria; combine; examine the results; conduct sensitivity analysis. The Green Book treats MCA as supplementary to social cost-benefit analysis where effects cannot be valued, and warns that weights and scores are judgements that must be transparent and owned by the decision makers, not by the analyst. The decisive quality of a Horus MCA is that criteria come from validated guiding principles and weights from a recorded client decision.

## When Horus uses it

- Strategy pathway anchor appraisal: strategic choices are compared on criteria derived from the guiding principles, with scenario stress-testing and order-of-magnitude costs as additional criteria or as separate columns.
- Institutional pathway: operating-model options on fit to mandate, capability, cost, transition risk and feasibility.
- Regulatory and investment pathways: to bring unmonetised effects (distributional, legal and institutional, political feasibility) into the comparison alongside NPV.
- Screening at P3: a light MCA with pass or fail criteria narrows the long list.

## Steps

1. **Set the decision** and the options to be compared, including do-nothing.
2. **Derive criteria** from the SMART objectives and the guiding principles agreed as decisions; test the set for completeness, non-redundancy, operational measurability and independence from one another (so no double counting).
3. **Define a scoring scale** per criterion (natural units where possible, otherwise a defined 0 to 100 or 1 to 5 scale with descriptors) and the evidence that supports each score.
4. **Score** each option on each criterion with a rationale and evidence; where a score is uncertain, record a range.
5. **Weight** through the decision makers (swing weighting or a structured workshop), record the weights as a `criteria_weights` decision, and note disagreements.
6. **Combine** by normalising scores and applying weights; produce the ranking.
7. **Test robustness**: vary weights across the range of stakeholder views, vary uncertain scores, check rank reversals; report which pairs of options are robustly ordered and which depend on judgement.
8. **Present** the scored matrix with the evidence behind each cell, the weights, the ranking and the robustness analysis, and say plainly what the method cannot settle.

## Outputs → state records

- `decisions` of kind `guiding_principle` (criteria sources) and `criteria_weights` (weights, made by the client, with `rationale`).
- `analyses` of kind `options_screening` (`criteria[] {criterion, weight, source: → DEC}`, `scores[]`, `shortlist`) at P3 and of kind `option_comparison` (`criteria_weights: → DEC`, `table`, `ranking[]`) at P4.
- `appraisals` with `methodology: mca` or `mixed`, `summary {mca_score, rank, verdict}`, `impacts[]` with qualitative `rating` and evidence; for `strategic_options` the `strategic {criteria_weights, scenario_results[], order_of_magnitude_cost}` block.
- `sensitivity {method: scenarios, parameters, results_path, robustness}` recording weight and score variation.
- `artefacts[]`: the scoring matrix and robustness charts from the toolkit.

## Pitfalls

- Analyst-set weights presented as objective; weights are the client's values and are recorded as a decision.
- Criteria that double count (for example "cost" and "affordability", or "effectiveness" and an objective it measures).
- Scores without evidence or rationale; every cell must trace.
- A single ranking with no robustness analysis; the decision maker needs to know what the ranking depends on.
- Using MCA to avoid monetisation that was feasible; where cost-benefit analysis is credible, it comes first and MCA carries the rest.

## Source

Department for Communities and Local Government, Multi-criteria Analysis: A Manual, 2009 (John Dodgson, Michael Spackman, Alan Pearman and Lawrence Phillips; first published 2000); HM Treasury, The Green Book (BENCHMARKS.md B6).
