# Delivery chain analysis

A map of every actor, hand-off and decision between a minister's policy intention and the citizen-facing outcome, used to find where delivery leaks. It is the first move of Barber's delivery method and the diagnostic core of the transformation pathway.

When Horus uses this: P2 diagnosis on the transformation and delivery pathway, and in P5 implementation planning on every pathway.

## What it is

Michael Barber's Prime Minister's Delivery Unit asked of every target: "who has to do what, in what order, for this to happen?" The delivery chain is the answer drawn as a diagram: the centre of government, the department, intermediaries (agencies, regions, local authorities, contractors), front-line units and the citizen or firm. For each link the analysis records what flows (money, instructions, data, services), what the actor's incentive is, how performance is measured, and where the chain is long, weak or broken. The method's power is that it converts an abstract implementation gap into specific, fixable bottlenecks: a funding rule that arrives late, a data return nobody reads, a professional group with no stake in the target.

## When Horus uses it

- Transformation and delivery pathway anchor diagnostic: paired with performance data to explain why a programme underperforms, and as the frame for choosing delivery interventions.
- Programme and service design pathway: the service blueprint's back-stage view is a delivery chain.
- P5 on every pathway: the implementation plan's `delivery_chain[]` field is the output of this analysis for the preferred option, so the client knows who must act.
- Interview planning: each link suggests an interviewee and a hypothesis about where the leak is.

## Steps

1. **Fix the outcome** and its measure: the target or indicator at the end of the chain, with its baseline.
2. **List the actors** from the decision maker to the end user, including those outside government (contractors, professional bodies, households).
3. **Draw the links.** For each hand-off record: what passes (funding, rules, data, people, services), through which instrument (law, circular, contract, grant agreement, IT system), with what lag.
4. **Score each link** on three questions: does the actor know what is expected; does it have the capacity and incentive to do it; can anyone see whether it did. Rate weak, adequate or strong with evidence.
5. **Find the bottlenecks.** Links with the lowest scores or the longest lags; points where many chains converge on one unit; places where the chain has no owner.
6. **Test with data and interviews.** Compare the mapped chain with performance data by region or unit; interview actors at the suspected bottlenecks.
7. **Design interventions per bottleneck.** Shorten the chain, clarify expectations, change the incentive, add data visibility, add capacity. Each intervention names the link it fixes.
8. **Attach routines.** Decide which links will be reviewed in stocktakes and which indicators the dashboard tracks.

## Outputs → state records

- `analyses` record of kind `delivery_chain` with `content` holding actors, links, scores, bottlenecks and lags; `findings[]` with evidence; `limitations[]` where links are unobserved.
- Actors as `stakeholders` with `decision_role` (`perform` for delivery actors) and `relationships[]` of type `oversees`, `funds`, `reports_to`.
- Bottlenecks as `hypotheses` of kind `implementation`, tested in interviews.
- Interventions as `options` of kind `delivery_intervention`; their appraisal records `delivery.bottlenecks_addressed[]` and `delivery.dependencies[]`.
- For the preferred option: `analyses` of kind `implementation_plan` with `delivery_chain[]`, `kpis[]` and `institutional_arrangements`.
- Risks at weak links: `risks` of scope `implementation` with `early_warning`.

## Pitfalls

- Drawing the organisation chart instead of the chain; the chain follows the outcome, and may skip layers or run through bodies outside the client.
- Stopping at the department boundary. Most leaks are at the front line or in intermediaries.
- Treating a weak link as a people problem when it is an incentive or data problem.
- Mapping without data: a chain scored only from headquarters interviews reflects headquarters' view.
- Proposing an intervention for every weak link; prioritise by effect on the trajectory.

## Source

Michael Barber, Instruction to Deliver: Fighting to Transform Britain's Public Services, Methuen, 2007; Michael Barber, Andy Moffit and Paul Kihn, Deliverology 101: A Field Guide for Educational Leaders, Corwin, 2011.
