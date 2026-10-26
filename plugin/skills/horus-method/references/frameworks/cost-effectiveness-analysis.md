# Cost-effectiveness analysis

Comparing options by the cost of achieving a unit of a defined outcome (cost per case resolved, per tonne abated, per job created, per life year gained) when the outcome cannot be or should not be monetised. Horus uses it where cost-benefit analysis is not credible and where options share a single dominant objective.

When Horus uses this: P4 on the programme and service design pathway (cost per outcome is a core measure), on the public investment pathway where benefits are not monetisable, and on the transformation pathway for intervention selection; the toolkit's `cea` module implements it.

## What it is

Cost-effectiveness analysis (CEA) compares options with the same objective by their ratio of cost to effect, with both measured incrementally against the baseline. The Green Book positions it as the appraisal method when benefits cannot be valued in money but can be measured in a common unit, and as a complement to cost-benefit analysis for choosing between ways of delivering a fixed outcome. In health, CEA with quality-adjusted life years and incremental cost-effectiveness ratios is the standard method; in education and social policy, Levin and McEwan's treatment is the reference. The analysis requires a defined effect measure, the incremental cost and incremental effect of each option over the next-best alternative, discounting of costs (and often effects) over time, and sensitivity analysis on the parameters that drive the ratio. It cannot tell the decision maker whether the outcome is worth buying at all; that is a cost-benefit or political judgement, and the report should say so.

## When Horus uses it

- Programme and service design pathway: `appraisals.service.cost_per_outcome` is the central comparison across service concepts; CEA with take-up ranges.
- Transformation pathway: cost per unit of trajectory gain for competing delivery interventions.
- Public investment pathway: when the economic case's benefits are not credibly monetisable (for example, some justice or security outcomes), CEA with a threshold stated.
- Regulatory pathway: cost per unit of risk reduction for alternative stringency levels, alongside the cost-benefit analysis.
- Strategy pathway: ordering initiatives within a pillar by cost per unit of the pillar's KPI.

## Steps

1. **Define the effect measure**: one outcome indicator, with its definition, data source and the period over which it is counted; if several outcomes matter, use cost-benefit analysis or MCA instead.
2. **Specify options and the baseline**, all delivering the same type of outcome.
3. **Estimate incremental costs** by year in real terms (set-up, running, costs to users and third parties where relevant), discounted.
4. **Estimate incremental effects** by year from evidence (trials, precedents, administrative data), with ranges; discount effects if the convention of the field requires it and say so.
5. **Compute ratios**: average cost-effectiveness against baseline and incremental cost-effectiveness between successive options ordered by effect; exclude dominated options.
6. **Sensitivity**: vary effect sizes, take-up, unit costs and discount rate; identify switching values.
7. **Interpret**: present the ratios with a benchmark threshold if one exists in the field, state what the method cannot settle, and carry the unmeasured effects into the comparison narrative.

## Outputs → state records

- `appraisals` with `methodology: cea` (or `mixed`), `impacts[]` quantified on the chosen dimension with `estimate {central, low, high, unit}`, `summary {net_benefit, rank, verdict}` with the cost-effectiveness ratio in `verdict` or `caveats[]`, and `sensitivity {method: switching_values|monte_carlo}`.
- Programme pathway: `appraisals.service {outcomes[], take_up_estimate, cost_per_outcome}`.
- `assumptions` for effect sizes (`category: behavioural` or `policy`), unit costs (`cost`) and discount rate, with ranges and `basis`.
- `evidence` for effect sizes from trials and precedents; `options.precedents[]`.
- `analyses` of kind `option_comparison` with the ratios in `table` and `ranking[]`.
- `artefacts[]`: the CEA model and charts from the toolkit.

## Pitfalls

- Comparing options with different outcomes on one ratio; the method assumes a common effect measure.
- Average ratios where incremental ratios are needed to choose between scaled options.
- Effect sizes from a single study or another context used as point estimates; show ranges and the source grade.
- Omitting costs to users and third parties, which makes government-delivered options look cheaper.
- Presenting a ratio as a verdict without a threshold or a statement of what remains unmeasured.

## Source

HM Treasury, The Green Book, 2022 edition, chapter 5 on shortlist appraisal (BENCHMARKS.md B6); Henry M. Levin and Patrick J. McEwan, Cost-Effectiveness Analysis: Methods and Applications, 2nd edition, Sage, 2001.
