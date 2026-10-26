# Option design

How Horus builds the option space: a long list from the pathway's option logic and from precedents, always with do-nothing, screened to a short list of two to four options plus variants or packages, each carrying a theory of change and explicit design parameters.

When Horus uses this: phase P3, after the diagnostic readout (AP2) and before the principles workshop (AP3), and again whenever a directive or a reaction-matrix finding reopens the option space.

## The long list

Generate wide, then cut. Two sources, both exhausted before any screening:

1. **The pathway's option logic.** Regulatory: the instrument typology (the schema's `instrument_types`: regulation, economic incentive, tax or fee, subsidy or grant, information or disclosure, direct provision, organisational or institutional, co-regulation, voluntary or standard, behavioural nudge, procurement), read through Hood's four resources of government (nodality, authority, treasure, organisation) and the OECD list of alternatives to regulation. Strategy: ambition, focus, delivery model, sequencing. Institutional: operating-model archetypes and governance variants. Delivery: links of the delivery chain and the routines, incentives and capabilities that could change them. Investment: the Green Book options framework filter (scope, solution, delivery, implementation, funding) from do-minimum to full scope. Service: eligibility, offer, channels, behavioural levers, pilots. Walk every cell of the typology and write down what the option would be, including the unpromising ones; the long list is MECE against the typology, not against intuition.
2. **Precedents in the ledger.** What other jurisdictions did about the same problem, with outcomes, from the `benchmark` analysis and `evidence` records; each precedent attaches to an option as `precedents[] {jurisdiction, programme, period, outcome, evidence}`. A precedent without evidence of outcome is a lead for the researcher, not a precedent.

Every entry becomes an `options` record at `status: long_list` with `code`, `title`, `summary`, `kind`, `addresses_objectives` (OBJ ids), `target_groups` and `origin` (`horus`, `client`, `stakeholder`, `literature`). Options proposed by the client or a stakeholder are recorded with that origin and screened like the others; a decision maker's favoured option screened out needs a careful rationale, not silence.

## Do-nothing and do-minimum

`do_nothing` is always on the list and is never screened out: it is the baseline every appraisal measures against (`appraisals.baseline`) and the comparator the decision memo must show. Describe it as a projection, not a snapshot: what happens to the problem, the costs and the stakeholders if current policy continues (the `baseline` analysis, `scenarios.project`). Where the status quo is itself not sustainable (a legal deadline, a funding cliff), add a do-minimum: the smallest action that meets the binding constraint. Keep them distinct; a do-minimum relabelled as do-nothing corrupts every NPV.

## Screening

Screening reduces the long list to a short list of two to four options the appraisal can afford to treat properly. Criteria are few, coarse and recorded:

- Fit to objectives: does the option plausibly move each OBJ id (pass, partial, fail).
- Consistency with the emerging guiding principles and known red lines (the proposed `guiding_principle` and `political_directive` decisions and the decision-maker lens); a red-line breach is a screen-out, not a low score.
- Legal feasibility at the coarse level: possible under existing powers, needs secondary legislation, needs primary legislation or treaty change.
- Fiscal envelope: within, stretches, exceeds the envelope the directive set.
- Evidence of effectiveness: precedents with measured outcomes, theory only, none.
- Time to effect against the political calendar.

Score each option on each criterion on a three-point scale with a one-line rationale and write the `options_screening` analysis: `criteria[] {criterion, weight, source: → DEC}` (weights are coarse and point at the decision that justifies them, or are equal), `scores[] {option: → OPT, criterion, score, rationale}` and `shortlist: → OPT[]`. Each option's `screening {criteria[], result, rationale, analysis}` mirrors its row, and its status moves to `short_list` or `screened_out`. The screening is a Tier 1 slide at AP3; the gate requires at least two options plus do-nothing with this analysis, and the reasons for screening out are kept because stakeholders will ask.

## Variants and packages

Options should differ in kind; variants differ in setting. A **variant** (`variants[] {id, description}`, coded `A1`, `A2`) changes one or two `design_parameters` of the same option: threshold, phasing, exemption, intensity, channel. Variants are how directives are absorbed without reopening the long list (the schema's own example: a phased variant `B2` replaces `B1` after the steering committee asks for phasing). A **package** (`kind: package`, coded `P1`, `package_members: → OPT[]`) combines complementary options whose mechanisms address different parts of the problem, or pairs a hard instrument with the support that makes it acceptable. Packages are appraised as a whole; members' effects are not simply summed where they act on the same group.

## Theory of change and design parameters

Every option carries a `mechanism`: `inputs` (money, powers, people), `activities` (what the state does), `outputs` (what is produced: licences issued, inspections, payments), `outcomes` (what changes in behaviour or condition), `impacts` (the objective-level result) and `key_assumptions: → ASM[]` (the links in the chain that must hold: compliance rates, take-up, elasticities, enforcement capacity). The key assumptions are the appraisal's sensitivity parameters and the implementation plan's early warnings, so write them as `assumptions` records now. `design_parameters[] {lever, setting, alternatives[]}` lists every dial the drafter can turn, its current setting and the alternatives considered; it is what the principles workshop debates and what the variants change.

## Worked example (illustrative)

Problem: low electronic invoicing among micro-enterprises undermines VAT compliance (baseline 18 per cent uptake, `EVD-0047`, illustrative). Long list by instrument type: A information campaign and free software; B mandatory e-invoicing for all VAT-registered firms, phased by size; C immediate mandate; D tax credit for adoption; E platform certification with voluntary uptake; F procurement-led (public buyers accept only e-invoices); do-nothing. Screening: C breaches the deputy minister's red line on micro-firm burden (screened out, rationale recorded); D exceeds the fiscal envelope (screened out); E has no precedent with measured outcomes (merged into B as a design parameter, status `merged`). Short list: A, B, F and do-nothing. Variants: B1 36-month phasing with free tooling; B2 24-month phasing. Package P1: B1 plus A. Mechanism for B1: inputs (platform, tax-authority staff, legal basis); activities (registration, assistance, enforcement after month 24); outputs (invoices issued electronically); outcomes (compliance rate up, record-keeping improved); impacts (VAT gap reduced, formalisation); key assumptions (adoption 60 per cent by year three, ASM-014; benefit per firm, ASM-015; software cost, ASM-016). Design parameters: size threshold; phasing length; exemption for turnover below a floor; penalty start; open standard versus certified platforms.

## Pitfalls

A long list built from what the client already proposed; options that are bundles of everything (unscreenable, unappraisable); do-nothing described as "the problem persists" without a projection; screening with the full appraisal criteria (that is the appraisal, done badly); variants presented as different options to make a short list look longer; a theory of change with no assumption that could fail; design parameters left implicit until drafting, when they become the fight.

Source: Bardach and Patashnik, A Practical Guide for Policy Analysis (7th edition, 2023), steps 3 and 5; Hood, The Tools of Government (1983); OECD, Alternatives to Traditional Regulation, and Regulatory Impact Assessment: Best Practice Principles for Regulatory Policy (2020), step 5; HM Treasury, The Green Book (2022), on the options framework filter and long-list appraisal.
