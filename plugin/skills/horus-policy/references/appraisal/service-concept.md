# Service concept evaluation

How Horus appraises programme and service concepts: the outcomes they are meant to produce, expected take-up, cost per outcome, equity, and the pilot and evaluation design that will test the concept before it scales.

When Horus uses this: programme and service design pathway, phase P4, appraisal kind `service_concept`; also for the citizen-facing component of another pathway's option (a licensing portal, a compliance support service, a benefit redesign).

## What is being appraised

Options of kind `service_concept`: an eligibility rule, a benefit or service offer, delivery channels (digital, assisted digital, face to face, intermediaries), the behavioural design (defaults, reminders, simplification) and the operating model behind them, plus packages and channel variants. Each concept carries a `mechanism` (theory of change) whose outcomes are the thing appraised. The baseline is the current service or its absence, with its take-up, cost to serve and outcomes from the `user_and_service_research` analysis.

## Outcomes

State the outcomes the concept is meant to change at the level the decision maker cares about (employment sustained at six months, children vaccinated, firms compliant), with indicator, baseline value and target. Separate outputs (applications processed) from outcomes (the change in people's lives or firms' behaviour). For each outcome give the evidence that the mechanism produces it: evaluations of comparable programmes in the ledger (`options.precedents`), the behavioural literature, the client's own data. Record in `service.outcomes[]` with indicator, baseline, target and evidence; the same outcomes feed `impacts` (typically `consumer_welfare`, `employment`, `health_and_safety`, `distributional_equity`, `gender_and_inclusion`, `fiscal_cost`) and `monitoring`.

## Take-up

Take-up is the product of a funnel, and each step is an `assumptions` record with a basis: the eligible population (administrative or survey data); the share aware of the offer; the share that applies; the share that completes; the share that persists. Benchmarks come from the baseline service and from precedents with similar eligibility and channel mix. Behavioural barriers found in user research (complexity, stigma, distrust, time cost, digital exclusion) lower the step they act on; design features (automatic enrolment, pre-filled forms, reminders, intermediaries) raise it, with effect sizes from the evidence where it exists and labelled as judgement where it does not. Produce low, central and high take-up and the year-by-year ramp (`scenarios.trajectory` with an `s_curve` shape is the usual pattern) and record in `service.take_up_estimate` with the funnel and the range. Take-up drives both benefits and cost, so it is almost always the first switching value to report.

## Cost per outcome

Build the cost to serve bottom-up: fixed costs (platform, management, premises), variable cost per case by channel (assisted channels cost more per case and reach different people), the cost of the benefit or service itself, and the outreach cost that take-up depends on. Divide total cost by outcomes achieved (not by cases processed) to get cost per outcome and compare it with the baseline and with precedents; `methodology: cea` is the normal read-out, with `cba.present_value` where costs and outcomes fall in different years. Where outcomes can credibly be monetised (fiscal savings, earnings), add an NPV and BCR with `cba.cba`, but do not force it. Record in `service.cost_per_outcome` with unit, range and price base year, and carry the fiscal total to `fiscal_cost`.

## Equity

Who the concept reaches and who it misses. Use `distribution.incidence` with one `distribution.Group(name, population, income_share, cost_per_unit, benefit_per_unit)` per segment (income, gender, region, disability, language, digital access) to show the share of benefits each segment receives against its share of need, and read the `verdict` (progressive, broadly proportional, regressive) as a prompt, not a conclusion. Then answer the design questions: does the eligibility rule exclude a group the objective targets; does the channel mix exclude the digitally excluded or those without identity documents; does the behavioural design rely on a resource (time, literacy, a smartphone) the target group lacks; what assisted route exists. Record in `service.equity_assessment` and in `distributional` with the `equity_note`.

## Pilot and evaluation design

A service concept is a set of hypotheses, and the pilot is how they get tested before the money scales. Design the pilot to inform a named decision (scale, modify, stop) with pre-agreed criteria. `service.pilot_design` holds:

- `design`: the comparison that will identify the effect. A randomised controlled trial where units can be randomised and the ethics permit (individuals, offices, areas); a stepped-wedge roll-out when everyone must eventually receive the service; difference-in-differences or synthetic control against comparable non-pilot areas; A/B tests for channel and message variants. Say what will be compared with what and why that comparison is credible.
- `sample`: how many units, from a power calculation on the primary outcome's expected effect size and variance (both are `assumptions`), and how they are selected so the pilot population resembles the scale population.
- `duration`: long enough for the outcome to show and for take-up to ramp, with interim reads for process problems.
- `evaluation_method`: impact evaluation on the primary outcome, process evaluation (what was delivered, to whom, at what cost, what users experienced) and a value-for-money read-out; who evaluates and how independence is protected; pre-registration of the analysis plan; data access and consent.

Monitoring indicators for the pilot are the same as for scale, with baselines measured before launch; `monitoring.evaluation {when, method}` points to this design.

## Common blocks and the `service` block

As for every appraisal: `baseline`; `impacts`; `summary` (cost per outcome and, where monetised, `npv` and `bcr`; `rank`; `verdict`); `distributional`; `feasibility` (administrative feasibility includes delivery partners' capacity and data-sharing permissions; legal includes eligibility and data-protection rules); `sensitivity` (take-up, unit costs and effect size are the parameters; `montecarlo.tornado` ranks them); `risks`; `monitoring`; `caveats`; `artefacts`. The `service` block holds `outcomes[]`, `take_up_estimate`, `cost_per_outcome`, `equity_assessment` and `pilot_design {design, sample, duration, evaluation_method}`; all are required by rule 20.

## Pitfalls

Take-up assumed at 100 per cent or at the headline figure of a programme with a different channel mix; cost per case reported as cost per outcome; digital-only channels appraised without the cost and reach of the assisted route; equity read from the toolkit verdict without the design questions; a pilot with no comparison group, no decision criteria and a sample too small to detect the effect; evaluation designed after launch so no baseline exists; outcomes measured only for those who completed.

Source: HM Treasury, The Magenta Book: Central Government guidance on evaluation (2020); OECD, Tools and Ethics for Applied Behavioural Insights: The BASIC Toolkit (2019); Behavioural Insights Team, EAST: Four simple ways to apply behavioural insights (2014); UK Government Digital Service, Service Standard; Government Outcomes Lab (Blavatnik School of Government) resources on outcomes-based commissioning.
