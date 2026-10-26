# Implementation planning

How Horus turns a preferred option into a plan that can be executed: delivery chain, sequencing with quick wins, legal and administrative instruments, institutional arrangements and RACI, budget and capacity, KPIs and monitoring, and risks, recorded as an `analyses` record of kind `implementation_plan`.

When Horus uses this: phase P5, after the `preferred_option` decision (AP4), for the recommended option or package; the plan becomes the Tier 2 implementation and communication plan annex, the policy note's short-term and medium-term action table, and the implementation section of the Tier 0 decision memo. Gate AP5 requires it at `final`.

## Principle

A recommendation is only as good as the second-order question it answers: who does what, by when, with what powers and money, and how will we know. Every element below is drawn from records that already exist (the option's `mechanism` and `design_parameters`, the appraisal's `feasibility`, `monitoring` and `risks`, the stakeholder register) and made executable. Nothing in the plan may contradict the appraisal; where delivery realities change the option, the option record is versioned and the appraisal caveated.

## Delivery chain

Draw the chain from the decision maker to the point where the outcome is produced: each link an actor (→ STK) with the action it must take, the hand-off to the next link, and the evidence on its capacity and willingness (interviews, the `delivery_chain` or `institutional_diagnostic` analysis). Mark the weak links: where a body has not done this before, where incentives point the other way, where data does not flow. The chain is `content.delivery_chain[]`; its weak links generate `capacity_needs`, `risks` and the routines in the monitoring section.

## Workstreams and sequencing

Group the actions into workstreams (`content.workstreams[]`: typically legal, institutional, systems and data, operations, finance, communications and stakeholder management, monitoring and evaluation), each with an owner and a lead indicator. Then sequence (`content.sequencing[] {phase, actions[], owners, dates}`) in phases tied to real dates and to the political calendar:

- **Mobilisation and quick wins (first 100 days)**: decisions and appointments that need no new instrument; visible actions that signal direction and buy credibility (a published timetable, a pilot launch, a fee waiver, a help desk); the baseline measurement for every KPI; the legal drafting instruction issued.
- **Enabling phase**: instruments enacted, institutions stood up, systems built, staff recruited and trained, data agreements signed, the first stocktake held.
- **Roll-out**: phased by group, region or function as the option's `design_parameters` specify; assistance before enforcement; the review clause's indicators measured from day one.
- **Steady state and review**: routines continue; the post-implementation review at the date the appraisal set.

Dependencies from the appraisal (`delivery.dependencies`, `operating_model.legal_changes_required`) set the critical path; show it as a Gantt-style chart in the Tier 2 annex and as a one-slide roadmap in the Tier 1 deck. Quick wins are chosen because they are on the path, not beside it.

## Instruments

Every action that needs a legal or administrative act is listed in `content.instruments_required[] {instrument, type, owner}` with `type` from the schema's enumeration: `law` (primary legislation), `decree` (an executive act with the force of law where the system provides for it), `regulation` (secondary legislation under an enabling power), `circular` (an administrative instruction binding the administration, not citizens), `budget` (an appropriation, virement or budget line), `MoU` (an agreement between bodies that binds no one at law but fixes responsibilities). For each: the drafting owner, the approving authority, the normal time from drafting to force in this jurisdiction, the session or cycle it must catch, and the content it must carry (the obligations, thresholds and dates from the option's design parameters). The regulatory pathway's outline of the regulatory instrument is built from this list. Prefer the lightest instrument that is lawful and durable, and say when a circular is a stopgap for a regulation.

## Institutional arrangements and RACI

`content.institutional_arrangements` names the governance: the sponsor or senior responsible owner, the steering or programme board and its cadence, the delivery lead and team, the implementing bodies, the oversight and audit lines, and the routines (a weekly delivery meeting, a monthly stocktake with the minister, a quarterly published report). A RACI table assigns, for each workstream and major action, who is responsible (does the work), accountable (one name, signs it off), consulted (gives input before) and informed (told after); it is reconciled with the RAPID roles in the stakeholder register so that the person who decides in RAPID is the one accountable in RACI. Two accountables, or none, is a defect to fix before release.

## Budget and capacity

`content.budget {capex, opex, source}` carries the implementation cost in nominal cash by year, consistent with the appraisal's `fiscal_cost` row and the directive's envelope, with the funding source named (budget line, reallocation, external finance, fees) and any gap stated. `content.capacity_needs[]` lists the people and skills the chain needs and does not have (number, role, where, by when, how acquired: recruit, second, train, contract) and the systems and data needs with their owners. Where capacity is the binding constraint, the sequencing shows it and the quick wins include the hiring or contracting decision.

## KPIs and monitoring

`content.kpis[] {name, baseline, target, source, frequency}` takes the appraisal's `monitoring.indicators` and makes them operational: a baseline value with its date (measured, not assumed; if unmeasured, measuring it is a 100-day action), a target with a date and trajectory (`scenarios.trajectory`), the data source and its owner, the reporting frequency, and the forum that reviews it. Mix leading indicators (applications, registrations, inspections, staff in post) that move early with the outcome indicators that justify the policy. Specify the dashboard: fields, refresh, audience, and the thresholds that trigger escalation. Set the evaluation: the post-implementation review date, method and evaluator, from the appraisal's `monitoring.evaluation` and, for regulation, `regulatory.review_clause`.

## Risks

Implementation, political, legal, fiscal and reputational risks are `risks` records with `scope`, likelihood and impact 1 to 5, mitigation, contingency, owner, early warning and status, linked to the plan (`content.risks: → RSK[]`). Take the appraisal's risks forward, add the delivery-chain weak links and the dependencies that are uncertain, and give every risk an owner who appears in the RACI; gate AP5 checks that owners exist. The top five appear in the Tier 1 deck with their mitigations; the register is the Tier 2 annex.

## Content shape

The `implementation_plan` analysis holds `workstreams[]`, `sequencing[] {phase, actions[], owners: → STK[], dates}`, `instruments_required[] {instrument, type: law|decree|regulation|circular|budget|MoU, owner}`, `institutional_arrangements`, `budget {capex, opex, source}`, `capacity_needs[]`, `kpis[] {name, baseline, target, source, frequency}`, `delivery_chain[]` and `risks: → RSK[]`, with `inputs` pointing at the option, appraisal, stakeholder and diagnostic records, `findings` for the judgements (the binding constraint, the critical path, the first risk), `limitations` for what the client must still decide, and `method_notes`.

## Pitfalls

Plans without dates, or with dates untied to the legislative and budget calendar; quick wins that are not on the critical path; "the ministry" as owner; instruments listed without the enabling power checked; a budget inconsistent with the appraisal; KPIs with no baseline; routines designed without the minister's time; risks without owners; a plan that quietly redesigns the option.

Source: Barber, Instruction to Deliver (2007) and Barber, Moffit and Kihn, Deliverology 101 (2011) for delivery chains, trajectories and routines; McKinsey Center for Government, "Delivering for citizens" (2018) on the five disciplines of government transformation; HM Treasury, The Green Book (2022), management case and monitoring and evaluation; World Bank policy notes for incoming governments for the short-term and medium-term action table; Australian Government, Cabinet Handbook (16th edition, 2026) on implementation strategy, timelines, responsibilities and risks as standing content of a submission.
