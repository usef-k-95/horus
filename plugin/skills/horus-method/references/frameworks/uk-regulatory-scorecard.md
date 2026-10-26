# UK Better Regulation Framework and the regulatory scorecard

The UK's 2023 framework for regulating business: options assessment scrutinised by the Regulatory Policy Committee before collective agreement, an impact assessment at the final stage, de minimis thresholds, and a regulatory scorecard that rates the preferred option's impacts on stakeholders and on wider government priorities. Horus uses the scorecard as a compact presentation of a regulatory appraisal and the framework's staging as a model for proportionate scrutiny.

When Horus uses this: P4 and P5 on the regulatory pathway for the presentation of impacts; P1 when designing the scrutiny and approval path with the client.

## What it is

The Better Regulation Framework guidance (2023 reform) sets the stages of UK regulatory policy-making for measures affecting business: initial policy development; pre-implementation, in which an options assessment is prepared and may be scrutinised by the Regulatory Policy Committee (RPC) before collective agreement and consultation, followed by a final impact assessment laid in Parliament; and post-implementation review. Thresholds: measures with an equivalent annual net direct cost to business (EANDCB) within plus or minus £10 million are de minimis and self-certified; measures at plus or minus £100 million, or with a weak options-assessment rating or an exclusion, trigger final-stage RPC scrutiny. The impact-assessment template (2023) runs: summary of proposal; strategic case; SMART objectives; intervention and logical change process; long list and alternatives; shortlisted options; regulatory scorecard for the preferred option; monitoring and evaluation; minimising administrative and compliance costs; declaration; summary analysis and evidence (price and present-value base year, net present social value ranges, business NPV, EANDCB); then the evidence base. The scorecard has two parts: part A rates overall and stakeholder impacts (business, households, public sector, by size and group); part B rates effects on wider government priorities with directional ratings. A small and micro business assessment is required.

## When Horus uses it

- Regulatory pathway: the appraisal deck's comparison slide and the policy note's impact summary adopt the scorecard format, adapted to the client's priorities; the metrics (NPSV range, business NPV, EANDCB equivalent) are produced by the toolkit where monetisation is credible.
- Designing the engagement: the staged scrutiny model (options assessment before consultation, final assessment before adoption) maps onto AP3 and AP4, and Horus proposes an equivalent review step where the client has no scrutiny body.
- Small-firm effects: the small and micro business assessment is the UK analogue of the EU SME test and feeds the `sme_test` block.
- Benchmark for document conventions: numbered paragraphs, Arial 12, Green Book cross-references.

## Steps

1. **Set the proportionality level** from the expected scale of business cost (the UK thresholds are a reference, not the client's rule) and agree the scrutiny path with the client.
2. **Options assessment at AP3**: the long list, shortlist and preliminary impacts, in the template's order, before consultation.
3. **Compute headline metrics** for the preferred option: net present social value with a range, business NPV, equivalent annual net direct cost to business and to households, at a stated price and present-value base year.
4. **Fill scorecard part A**: for each stakeholder group (large business, SMEs, micro and small, households, public sector, consumers) the direction and size of impact, monetised where possible, with the confidence.
5. **Fill scorecard part B**: directional rating against the government's stated priorities (for the client: the guiding principles agreed at AP3).
6. **Small and micro business assessment**: whether they are in scope, the disproportionate burden, and the mitigations (exemptions, phasing, support).
7. **Minimising costs**: the administrative and compliance cost measures taken in the design.
8. **Post-implementation review**: date, method, data.

## Outputs → state records

- `appraisals` of kind `ria` with `standards_applied` including the UK Better Regulation Framework 2023, `summary {npv {central, low, high}, net_benefit}`, `impacts[]` on `business_compliance_cost`, `administrative_burden`, `sme`, `consumer_welfare`, `fiscal_cost`, rated and monetised; `regulatory.sme_test`.
- Scorecard part B: `options.principles_alignment[] {principle: → DEC, score, rationale}`.
- `assumptions` for price base year, present-value base year and appraisal period.
- `appraisals.monitoring.evaluation {when, method}` as the post-implementation review.
- The scorecard exhibit in the appraisal deck and policy note (`deliverables`), and the `ria_report` evidence base structure.

## Pitfalls

- Presenting EANDCB-style metrics without stating the base years and the appraisal period.
- Scorecard ratings without the monetised or qualitative evidence behind each cell.
- Skipping the small and micro business assessment because the measure is "sector-wide".
- Treating UK thresholds as the client's thresholds; use them to argue proportionality, not as rules.
- Options assessment produced after consultation, which the framework exists to prevent.

## Source

Department for Business and Trade, Better Regulation Framework: Guidance, 2023 (BENCHMARKS.md B4); UK Impact Assessment and Options Assessment templates, 2023 (BENCHMARKS.md B5).
