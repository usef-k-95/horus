# Delivery trajectories

A trajectory is the expected path of a performance indicator from its baseline to its target, month by month or quarter by quarter, under the planned interventions, against which actual delivery is tracked. Horus uses trajectories to make targets credible, to size interventions and to give stocktakes something to argue about.

When Horus uses this: P4 appraisal of delivery interventions on the transformation and delivery pathway (`delivery.trajectory` is required), and P5 for every implementation plan's KPIs; the toolkit's `trajectories` module implements it.

## What it is

In Barber's delivery method a target without a trajectory is a wish. The trajectory makes explicit what the indicator would do without intervention (the baseline series, from trend and seasonality), what the target requires by when (the target series), and what each intervention is expected to contribute and when its effect appears (the intervention series). Building it forces questions the target alone hides: which interventions produce the early movement, how long each takes to bite, whether the sum of plausible contributions reaches the target, and what the gap is. In delivery, the trajectory is the reference for routines: stocktakes compare actuals with the trajectory, not with the end target, so slippage is seen early. Trajectories are revised with evidence, and revisions are recorded, not hidden.

## When Horus uses it

- Transformation and delivery pathway anchor appraisal: each delivery intervention option is appraised by its trajectory against the target, its cost and effort, and its dependencies; the delivery plan deliverable carries trajectories per target.
- Programme pathway: take-up trajectories for a new service.
- Regulatory pathway: compliance trajectories (share of firms compliant by period) for phased mandates.
- Strategy pathway: trajectories for the KPIs of the strategy's initiatives, usually at lower resolution.
- Dashboard specification: trajectories define what the dashboard shows.

## Steps

1. **Fix the indicator** precisely (definition, source, frequency, lag) and establish the baseline series from historical data, with seasonality and trend.
2. **Set the target series**: the end target and the intermediate milestones, or a straight or curved path, with the rationale (political commitment, precedent, capacity).
3. **Decompose the gap** by driver, region or segment, so that interventions can be attached to the part of the gap they address.
4. **Estimate each intervention's contribution**: size, lag and ramp-up, from precedents and the delivery-chain analysis; show ranges.
5. **Sum and compare**: the intervention series against the target series; identify the shortfall and when it appears.
6. **Adjust**: add or strengthen interventions, phase the target, or advise that the target is not credible and say what would be.
7. **Attach routines**: which stocktake reviews which trajectory, what variance triggers action, who owns each.
8. **Record and version**: trajectories and the assumptions behind them; update as actuals arrive.

## Outputs → state records

- `appraisals` of kind `delivery_intervention` with `delivery {trajectory {baseline_series, target_series, intervention_series}, bottlenecks_addressed[], effort, dependencies[]}`, `impacts[]`, `summary.verdict` and `sensitivity` on the contribution assumptions.
- `assumptions` for each intervention's contribution, lag and ramp-up (`category: policy` or `behavioural`), with ranges and `basis`.
- `analyses` of kind `baseline` (the historical series) and `delivery_chain` (the drivers).
- `analyses` of kind `implementation_plan` with `kpis[] {name, baseline, target, source, frequency}` and the trajectory artefact referenced from `narrative_path`.
- `deliverables` of type `delivery_plan` and `dashboard_specification`.
- `artefacts[]`: trajectory data (CSV) and charts from the toolkit's `trajectories` and `report` modules.

## Pitfalls

- A straight line from baseline to target with no intervention logic; the trajectory must be built up from contributions.
- Ignoring lags; most interventions take two or more reporting periods to show.
- Baseline series without seasonality, so every seasonal dip looks like slippage.
- Trajectories kept in a spreadsheet nobody owns; they are appraisal artefacts with assumptions in the register.
- Revising the trajectory to match actuals without recording why.

## Source

Michael Barber, Instruction to Deliver, Methuen, 2007; Michael Barber, Andy Moffit and Paul Kihn, Deliverology 101, Corwin, 2011; Michael Barber, How to Run a Government So That Citizens Benefit and Taxpayers Don't Go Crazy, Allen Lane, 2015.
