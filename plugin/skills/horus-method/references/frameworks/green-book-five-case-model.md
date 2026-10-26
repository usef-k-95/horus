# HM Treasury Green Book and the Five Case Model

The UK's central appraisal guidance and its business-case structure: strategic, economic, commercial, financial and management cases developed through strategic outline, outline and full business case stages. Horus uses it as the method for the public investment pathway and as the appraisal standard (social cost-benefit analysis, discounting, optimism bias, sensitivity, distributional analysis) across pathways.

When Horus uses this: P4 appraisal on the public investment and business case pathway (`HMT-Green-Book-2026` and `Five-Case-Model` in `standards_applied`); the economic-appraisal conventions on every pathway that monetises impacts.

## What it is

The Green Book sets how UK public bodies appraise and evaluate proposals. Its core is social cost-benefit analysis against business as usual: all costs and benefits to UK society, valued in real terms at a common price base, discounted at the social time preference rate, with optimism-bias adjustments to cost and benefit estimates, sensitivity and switching-value analysis, and distributional analysis where effects fall unevenly. The 2022 edition's rates: 3.5 per cent real for years 0 to 30, 3.0 per cent for years 31 to 75, 2.5 per cent beyond, and 1.5 per cent for risk to life and health; the Green Book 2026 (February 2026) supersedes it and the build must confirm any change. The Five Case Model structures the business case. Strategic: case for change, business as usual and up to five or six SMART objectives. Economic: options and net social value against business as usual, with the appraisal summary table. Commercial: a credible deal and risk allocation. Financial: affordability within budgets. Management: delivery plans, governance, benefits realisation, evaluation. The stages are strategic outline case, outline business case and full business case, each deepening the same five cases.

## When Horus uses it

- Public investment pathway anchor method: the business case deliverable follows the five cases; Horus normally takes a case to strategic-outline or outline level.
- Regulatory pathway: the UK impact-assessment template cross-references Green Book chapters for monetisation, discounting and distributional analysis.
- Strategy pathway: order-of-magnitude costing and the options framework filter.
- Transformation and programme pathways when delivery interventions or services need funding approval.
- The toolkit's `cba`, `fivecase` and `distribution` modules implement these conventions.

## Steps

1. **Strategic case**: rationale, business as usual, case for change, SMART objectives, scope, constraints, dependencies.
2. **Long list and shortlist** with the options framework filter (scope, solution, delivery, implementation, funding); shortlist with business as usual, do-minimum and preferred way forward.
3. **Economic case**: for each shortlisted option, cost and benefit streams by year in real terms; discount; apply optimism-bias uplifts by project type and stage; compute net present social value and benefit-cost ratio; list unmonetised effects; run sensitivity and switching values; distributional analysis; present the appraisal summary table.
4. **Commercial case**: procurement route, risk allocation, contractual structure, market capacity.
5. **Financial case**: capital and revenue costs by year in nominal terms, funding sources, affordability against budgets and fiscal rules.
6. **Management case**: governance, delivery plan, milestones, change management, benefits realisation plan, risk management, monitoring and evaluation.
7. **Recommendation and next stage**: the preferred option, what the next approval stage must add.

## Outputs → state records

- `appraisals` of kind `business_case` with `standards_applied`, `methodology: cba` (or `cea`), `time_horizon`, `discount_rate` linking an `assumptions` record, `impacts[]` with `present_value: true`, `summary {npv, bcr}`, `sensitivity {method: switching_values}`, `distributional`, and `five_case {strategic, economic, commercial, financial, management}` each with `status` and `summary`, plus `optimism_bias_uplift`.
- `assumptions` for the social time preference rate, price base year, optimism-bias percentages, demand and cost parameters (`basis: convention` or `evidence`).
- `analyses` of kind `strategic_case`, `baseline`, `options_screening`, `option_comparison`.
- `artefacts[]` on the appraisal: model, appraisal summary table, charts, with `inputs_hash`.
- `deliverables` of type `business_case`, `appraisal_summary_table` and `financing_options_paper`.

## Pitfalls

- Confusing the economic case (society, real terms, discounted) with the financial case (budget, nominal, cash).
- Omitting optimism-bias uplifts or applying them after sensitivity rather than before.
- Benefits counted twice (for example land value uplift and the productivity it capitalises).
- Treating unmonetised effects as zero; list them and weigh them in the comparison.
- Using the 2022 discount schedule without checking the 2026 edition; record the edition in `standards_applied`.

## Source

HM Treasury, The Green Book: Central Government Guidance on Appraisal and Evaluation, 2022 edition, and The Green Book 2026, February 2026; HM Treasury, Guide to Developing the Project Business Case (Five Case Model) (BENCHMARKS.md B6).
