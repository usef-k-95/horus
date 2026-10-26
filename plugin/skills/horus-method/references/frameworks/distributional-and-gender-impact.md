# Distributional and gender impact assessment

Methods for showing who gains and who bears the costs of each option, by income, gender, age, region, disability, ethnicity and other relevant groups, and for adjusting the appraisal where effects are uneven. Horus uses them so every appraisal states incidence, not just totals, and so equity is a criterion the decision maker sees.

When Horus uses this: P4 on every pathway (`appraisals.distributional` is a required block); P3 when options are designed with eligibility, thresholds or targeting; the toolkit's `distribution` module implements the incidence analysis.

## What it is

Distributional analysis in the Green Book identifies the groups affected by each option, estimates the incidence of costs and benefits across them, and, where effects on income groups are material, applies distributional weights derived from the diminishing marginal utility of income to produce a weighted net present value alongside the unweighted one. The EU Toolbox includes income-distribution and social-impact tools, and the 2023 OMB Circular A-4 asks for effects by income, race, geography and other groups, with optional weighting shown separately. Gender impact assessment, as in the OECD's 2015 Recommendation on Gender Equality in Public Life, Canada's Gender-based Analysis Plus and Australia's gender-responsive budgeting requirement for Cabinet submissions, asks how a measure affects women and men differently through time use, labour-market position, access to assets and services, and exposure to risk, and extends the lens to intersecting characteristics. The Australian Cabinet Handbook also requires First Nations impacts. The common output is an incidence table, an equity judgement and, where justified, design changes.

## When Horus uses it

- Every appraisal: the `distributional` block and the `distributional_equity` and `gender_and_inclusion` impact dimensions are filled for each shortlisted option.
- Regulatory pathway: who pays compliance costs (firms by size, consumers by income) and who gets the benefit (health, safety, consumer protection).
- Programme pathway: take-up and exclusion by segment is the central equity question.
- Public investment pathway: place-based effects and the Green Book's distributional weighting.
- Communication: the incidence table is the basis for stakeholder-specific messaging and for anticipating opposition from losers.

## Steps

1. **Identify the groups** relevant to this policy: income deciles or quintiles, gender, age, region or urban-rural, disability, ethnicity or indigeneity, firm size; record why each matters here.
2. **Trace incidence**: for each cost and benefit stream, who ultimately bears it after pass-through (for example, compliance costs passed to consumers; payroll costs to workers).
3. **Quantify** incidence by group where data allow (household surveys, administrative data, firm registers), as ranges; qualitative direction and size where not.
4. **Gender and inclusion lens**: how the measure affects time use, employment, income, access, safety and care responsibilities for women and men and for intersecting groups; check data gaps.
5. **Assess equity**: whether the distribution is progressive or regressive, whether any group bears a disproportionate burden, and whether that was intended.
6. **Weight where justified** (Green Book method) and show weighted and unweighted results side by side.
7. **Design responses**: targeting, exemptions, compensation, assisted channels, phasing; cost them and return them to the option design.
8. **Report** the incidence table and the equity note in the appraisal and deliverables.

## Outputs → state records

- `appraisals.distributional {groups[], incidence[], equity_note}` and `impacts[]` on dimensions `distributional_equity` and `gender_and_inclusion` with `affected_groups`, `direction`, `rating` or estimate and `evidence`.
- `assumptions` for pass-through rates and group populations (`basis: evidence`), and for distributional weights (`basis: convention`).
- `evidence` of kind `statistic` from household and firm surveys with graded sources.
- `options.design_parameters[]` and `variants[]` for targeting and mitigation; `options.target_groups[]`.
- `stakeholders` of kind `public_segment` for affected groups, with `interests` and `concerns`; `communication_plan.content.audiences[]`.
- `risks` of scope `political` or `policy_outcome` where a group bears a concentrated loss.

## Pitfalls

- Reporting aggregate net benefit as if distribution did not matter; decision makers and courts ask who pays.
- Incidence stopped at the legal payer; follow pass-through.
- Gender treated as a paragraph rather than analysed through time use, employment and access with data.
- Groups defined by data availability rather than by relevance; where data are missing, say so and plan to collect them.
- Weighted results presented without the unweighted ones.

## Source

HM Treasury, The Green Book, 2022 edition, distributional analysis annex (BENCHMARKS.md B6); US OMB Circular A-4, 2023, distributional effects section (BENCHMARKS.md B7); Australian Cabinet Handbook, 16th edition, paragraph 97 on gender-responsive budgeting and First Nations impacts (BENCHMARKS.md C2); OECD, Recommendation of the Council on Gender Equality in Public Life, 2015; Women and Gender Equality Canada, Gender-based Analysis Plus.
