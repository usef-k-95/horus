# Delivery intervention appraisal

How Horus appraises interventions that improve the delivery of an existing policy or programme: trajectories against targets, the bottlenecks each intervention addresses, effort, dependencies and risk, built on the delivery-chain analysis and Barber's method.

When Horus uses this: transformation and delivery pathway, phase P4, appraisal kind `delivery_intervention`; also for the delivery component of another pathway's preferred option (how a regulation or a service actually reaches its target).

## What is being appraised

Options of kind `delivery_intervention`: fixes to the delivery chain (clarifying roles, removing a step, adding capacity at a bottleneck), routines (stocktakes, dashboards, performance dialogues), incentive changes (funding formulas, league tables, consequences), capability building, data and digital fixes, and packages of these. The baseline is the current trajectory of the target indicator if nothing changes, which is rarely flat.

## The delivery chain and the bottlenecks

Start from the `delivery_chain` analysis: the chain of actors from the minister to the front line through which the policy is supposed to produce the outcome, each link with its owner, the hand-off and the evidence on where the chain leaks (stocktake data, performance data, interviews). An intervention is defined by the links it changes. `delivery.bottlenecks_addressed[]` names those links; an intervention that addresses no identified bottleneck is a hope, and the appraisal says so.

## Trajectories

A trajectory is the time path of the target indicator. Horus always draws three, and the chart with the three lines is the central exhibit of the appraisal deck.

1. **Baseline series**: the indicator's recent trend projected forward with `scenarios.project(start, growth, years, step_changes)`, where `growth` is the observed annual rate and `step_changes` captures known future events (a funding cliff, a cohort bulge). The growth rate and any step are `assumptions`.
2. **Target series**: the path from today's value to the target by the target year, with `scenarios.trajectory(baseline, target, target_year, shape)`. Shapes: `linear` when effort is steady; `s_curve` when the intervention needs set-up time and then saturates (most capability and system changes); `front_loaded` when quick wins are available and later gains are harder. The target comes from the brief or the `political_directive` decision; the shape is a claim about how delivery works and needs a rationale. The target series is the yardstick for stocktakes: being below it in year two is the early warning.
3. **Intervention series**: the baseline plus the expected effect of the intervention, with `scenarios.intervention_effect(baseline, effects, decay)`. `effects` is `{year: effect}`, the additive change that starts in that year and persists; `decay` is the fraction of each accumulated effect lost per year (0 for permanent changes, 0.1 to 0.3 for routines that fade without reinforcement). Effect sizes come from precedents in the ledger (`options.precedents`, evidence of kind `estimate` or `finding`) or from the client's own pilots, each an `assumptions` record with `low` and `high`.

Record the three as `delivery.trajectory {baseline_series, target_series, intervention_series}`, one value per year of `time_horizon`, with the unit in the matching impact row. The gap between the intervention series and the target series in the target year is the headline number: it says whether this intervention alone can hit the target or whether a package is needed. Chart with `report.line_chart_svg(path, {"baseline": ..., "target": ..., "with intervention": ...}, title=..., x_labels=years, unit=..., highlight="with intervention")` and write the CSV beside it with `report.write_csv`.

Where several interventions act on the same bottleneck, their effects are not additive; model the package's effect directly and say which interactions were assumed. Where interventions act on different links, additive effects are a reasonable first approximation and the caveat says so.

## Effort

Effort is costed in three currencies: money (one-off and recurring, in ranges, with `assumptions` for unit costs), people (full-time equivalents by role, including the scarce ones such as data analysts or inspectors) and leadership attention (how often the minister or permanent secretary must personally engage; Barber's routines consume this). Record in `delivery.effort` as a short structured text. For money, `methodology: cea` is the natural read-out: cost per unit of indicator moved by the target year, comparable across interventions. Use `cba.present_value` only if interventions differ markedly in timing.

## Dependencies

Each intervention depends on things outside it: a legal change, a data feed, a budget decision, another intervention, a hiring round, a political window. List them in `delivery.dependencies[]` with the owner and the date needed by, and reflect any dependency that is itself uncertain as a `risks` record. The dependency list is the first draft of the implementation plan's sequencing.

## Sensitivity

Run the trajectory under low, central and high effect sizes (and under a slower start) and report the year the target is reached in each; `montecarlo.simulate` over effect size and start year gives the probability of hitting the target by the target year, which is what a delivery unit wants to know; `montecarlo.tornado` ranks what matters. Record method and `robustness` in `sensitivity`.

## Common blocks

`baseline` (the trend analysis); `impacts` (the outcome dimension the indicator measures, `fiscal_cost`, `administrative_feasibility`, `employment` where front-line staffing changes, `digital_and_data`); `summary` (`net_benefit` or cost-effectiveness, `rank`, `verdict`); `distributional` (which regions or user groups the gains concentrate in, since averages hide left-behind places); `feasibility` with evidence; `risks`; `monitoring` (leading indicators that move before the target does, the stocktake cadence, the dashboard fields, owners); `caveats`; `artefacts`.

## The `delivery` block

`trajectory {baseline_series, target_series, intervention_series}`, `bottlenecks_addressed[]` (links of the delivery chain), `effort` (money, people, attention), `dependencies[]` (owner, date). All four are required by rule 20.

## Pitfalls

A flat baseline when the trend is moving; a target with no trajectory shape (and therefore no early-warning points); effect sizes asserted rather than taken from evidence or a pilot; adding the effects of overlapping interventions; omitting leadership attention from effort; measuring activity (training delivered) instead of the outcome; a dashboard specified before the data exists; forgetting that routines decay without consequences.

Proposed schema additions: give `delivery.effort` a fixed shape, `{money {one_off, recurring, unit}, fte[] {role, count}, leadership_attention}`, and `delivery.dependencies[]` the shape `{dependency, owner: → STK, needed_by, risk: → RSK}`.

Source: Barber, Instruction to Deliver (2007) and Barber, Moffit and Kihn, Deliverology 101 (2011) for aspiration, delivery chain, trajectories and routines; McKinsey Center for Government, "Delivering for citizens: How to triple the success rate of government transformations" (2018); OECD DAC evaluation criteria for the monitoring and evaluation framing.
