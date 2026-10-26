# Regulatory impact assessment

The Horus RIA method: the OECD basic steps, the Commission's impact-assessment report structure and the UK template folded into one appraisal of kind `ria`, proportionate to the stakes, with Standard Cost Model compliance costs and sensitivity run by the analyst with `horus_appraisal`.

When Horus uses this: regulatory pathway, phase P4, for every shortlisted option against the same baseline and assumptions register; also for the regulatory component of a hybrid engagement.

## The eight steps and where they land

The OECD basic steps (Best Practice Principles, 2020, box 2.2) are the spine: consultation; problem definition; objectives; description of the proposal; alternatives; analysis of benefits and costs; preferred solution; monitoring and evaluation. The first five precede the analyst brief, and the appraisal must still point to them: the reaction matrix and interview `evidence`, the `baseline` and `diagnostic` analyses, `brief.objectives`, the `options` records with `mechanism` and `design_parameters`, and the `options_screening` analysis with `do_nothing`. Steps six to eight are the appraisal itself: `impacts`, `summary`, `distributional` and `sensitivity`; `option_comparison` and the `preferred_option` decision; `monitoring` and `regulatory.review_clause`. The OECD also expects an enforcement and compliance strategy in every RIA, hence `regulatory.enforcement_strategy`.

## Report structure

The Tier 2 RIA report (at most 40 pages before annexes) follows the Commission's order: context; the problem and why it is a problem; why intervene at this level; SMART objectives; options with theory of change; impacts and who is affected; comparison; preferred option with proportionality, SME test and competition check; monitoring and evaluation; annexes (procedural information, consultation synopsis by group, who-is-affected table, methods and assumptions, sensitivity, competitiveness). From the UK template Horus adds the price-base and present-value base year up front, net present social value as a range, the equivalent annual net direct cost to business (EANDCB), a directional scorecard for the preferred option and a section on minimising compliance costs. A client jurisdiction's own form is the outer skeleton; record the mapping in `method_notes`.

## Proportionality

`proportionality_level` is set in the analyst brief and justified in `caveats`. Horus defaults, overridable with a reason:

- `light`: direct costs clearly below the jurisdiction's de minimis threshold (UK: plus or minus £10 million EANDCB), no SME, competition or distributional concern, low salience. Content: problem, objectives, options, impacts rated −3 to +3 per dimension, order-of-magnitude costs, feasibility, monitoring; `methodology: qualitative`.
- `standard`: measurable compliance costs, identifiable affected groups, moderate salience. Adds Standard Cost Model costs, monetised direct costs and credibly monetisable benefits, scenario sensitivity, SME test, competition check, distributional table.
- `full`: above the scrutiny threshold (UK: plus or minus £100 million), a novel instrument, contested evidence, high salience or litigation risk. Adds full social cost-benefit analysis with NPV range and BCR, Monte Carlo and switching values, incidence by group with a progressivity read-out, consultation synopsis, competitiveness check.

Proportionality cuts analysis, never steps: even a light RIA states the baseline, the alternatives and the enforcement strategy.

## Impact dimensions and who bears them

Every impact row names a `dimension` from the schema's enumeration, a direction, affected groups, method and evidence. The enumeration covers the economic, fiscal, social, environmental and institutional impacts the three standards require, including `competition`, `sme`, `distributional_equity`, `gender_and_inclusion` and `international_obligations`. The who-is-affected annex is generated from `impacts[].affected_groups` and `distributional.incidence`: businesses by size class, citizens by income group, the administration, third parties. Transfers (fees, fines, taxes) net to zero in the social NPV; show them in the fiscal rows, never as a social benefit.

## SME test and competition check

**SME test** (Commission Toolbox; UK small and micro business assessment). Four steps: identify affected businesses by size class; consult SME representatives (interview or consultation evidence); measure the impact, normally compliance cost per firm and as a share of turnover, from the Standard Cost Model by size class; assess mitigation (micro-enterprise exemptions, thresholds, phased or simplified obligations, free tooling, longer transition). The UK presumption is that small and micro businesses are exempted unless the department justifies otherwise. Record `regulatory.sme_test {applicable, finding, evidence}`; `applicable: false` needs a reason.

**Competition check** (OECD Competition Assessment Toolkit; Commission competition tool). Four questions: does the option limit the number or range of suppliers; limit their ability to compete; reduce their incentive to compete; limit the choices and information available to consumers. Any yes triggers a look at market structure, entry barriers and less restrictive alternatives. Record `regulatory.competition_check {applicable, finding, evidence}`.

## Compliance costs with the Standard Cost Model

Direct compliance costs split into administrative burdens (information obligations), substantive compliance costs and charges (fees and levies). The Standard Cost Model prices each obligation as population × frequency × time × tariff plus out-of-pocket items, one-off or recurring, with the EU convention of a 25 per cent overhead on wage costs; costs firms would incur anyway are excluded and noted. The analyst builds one `scm.Obligation(name, population, frequency_per_year, hours_per_action, tariff_per_hour, out_of_pocket_per_action, one_off, overhead_rate)` per obligation and calls `scm.standard_cost_model(obligations)`; the `SCMResult` gives `one_off`, `recurring_per_year` and `by_obligation`, and `SCMResult.present_value(years, schedule)` discounts the stream. Run it by size class so the SME test and the incidence table share the numbers. Population, time and tariff are `assumptions` records; the result lands in `regulatory.compliance_cost_scm` and in the `business_compliance_cost` and `administrative_burden` rows.

## Discounting by jurisdiction

The rate is one `assumptions` record (basis `convention`) referenced from `appraisals.discount_rate`, never a literal in a model. `cba.SCHEDULES` holds the conventions: `green_book` (HM Treasury social time preference rate, 3.5 per cent real for years 0 to 30, 3.0 for 31 to 75, 2.5 beyond; the default where the jurisdiction has none; verify against the 2026 edition); `green_book_health` (1.5 per cent declining, for risk to life and health); `omb_a4_2023` (2.0 per cent real; analytical method, not current US law, the 2023 revision being reported rescinded); `eu` (3 per cent real per the Toolbox's discount-rate tool; verify the current edition); `omb_2003_3pct` and `omb_2003_7pct` for the 2003 US text. `cba.flat(rate)` serves a jurisdiction with its own published rate. `cba.cba(benefits, costs, schedule)` returns `pv_benefits`, `pv_costs`, `npv`, `bcr` and `payback_year`; `cba.equivalent_annual(pv, rate, years)` gives the EANDCB.

## Sensitivity

Required for every quantified appraisal (gate AP4). Three methods, cumulative with proportionality: **scenarios**, low, central and high cases built with `scenarios.project(start, growth, years, step_changes)` on the drivers, reporting the NPV in each; **switching values**, `montecarlo.switching_value(model, params, name, lo, hi)`, which finds by bisection the value of one parameter at which the NPV crosses zero; **Monte Carlo**, one `montecarlo.Param(name, central, low, high, distribution)` per uncertain assumption (low and high are read as a 90 per cent interval), `montecarlo.simulate(model, params, runs)` for mean, p5, p50, p95 and `probability_positive`, and `montecarlo.tornado(model, params)` for the swing ranking charted with `report.bar_chart_svg`. Classify `sensitivity.robustness` as `robust` (NPV positive in every scenario, p5 above zero, no switching value in range), `sensitive_to` the parameters whose switching value lies in range, or `fragile` (the sign flips in the pessimistic scenario or `probability_positive` is below 0.6). These thresholds are Horus conventions.

## The `regulatory` block

`sme_test` and `competition_check` as above; `compliance_cost_scm`, the `SCMResult.as_dict()` output by size class with present value and artefact path; `enforcement_strategy`, who enforces with what powers and resources, the compliance model (information, assistance, inspection, sanctions), the expected compliance rate with its evidence, the enforcer's cost as `fiscal_cost`; `review_clause`, when the regulation is reviewed (UK convention: a post-implementation review within five years of commencement), by whom, against which `monitoring` indicators, and the sunset or revision trigger.

## Worked skeleton (illustrative figures)

Central values come from `python -m horus_appraisal demo`; the NPV range is a placeholder. Nothing here is evidence about any jurisdiction.

```yaml
kind: ria
pathway: regulatory
options: [OPT-B]
baseline: {description: "Voluntary e-invoicing continues; 18% micro-enterprise uptake", analysis: ANA-006}
standards_applied: [OECD-RIA-2020, EU-BR-Toolbox-2025, UK-IA-template-2023]
methodology: cba
proportionality_level: full
time_horizon: {start_year: 2027, years: 10}
discount_rate: ASM-001   # green_book
summary: {npv: {central: 82.1, low: 31.0, high: 118.0}, bcr: 2.75, verdict: "Positive in every scenario"}   # million PV
regulatory:
  sme_test: {applicable: true, finding: "Regressive: micro-enterprises bear 69% of cost against a 15% income share; phase over 36 months with free tooling", evidence: [EVD-0047]}
  competition_check: {applicable: true, finding: "Certification could raise vendor entry barriers; open standard recommended", evidence: []}
  compliance_cost_scm: {one_off: 5.0, recurring_per_year: 7.5, unit: million, artefact: analysis/models/OPT-B/scm.csv}
  enforcement_strategy: "Tax authority; assistance-first for 24 months, then penalties; compliance assumption 60% (ASM-014)"
  review_clause: "Post-implementation review at year 3 against adoption and compliance-cost indicators"
sensitivity: {method: monte_carlo, parameters: [ASM-014, ASM-015, ASM-016], results_path: analysis/models/OPT-B/mc.json, robustness: robust}   # demo: p5 2.5, p95 15.2, P(positive) 0.99; switching value 40 against a 60 to 140 range
```

## Pitfalls

Transfers counted as benefits; a nominal rate on real flows; asymmetric optimism between the preferred option and the baseline; an SME test that never measures cost per firm; weak benefits monetised to inflate the BCR; no enforcement strategy.

Proposed schema additions: a fixed shape for `regulatory.compliance_cost_scm`, `{by_size_class[] {size_class, one_off, recurring_per_year}, present_value, artefact}`.

Source: OECD, Regulatory Impact Assessment: Best Practice Principles for Regulatory Policy (2020); European Commission, Better Regulation Guidelines SWD(2021) 305 and Toolbox (2023 edition); UK Better Regulation Framework guidance and impact assessment template (2023); HM Treasury, The Green Book (2022; the 2026 edition supersedes it); US OMB Circular A-4 (2023 revision, as method); OECD Competition Assessment Toolkit; EU Standard Cost Model manual.
