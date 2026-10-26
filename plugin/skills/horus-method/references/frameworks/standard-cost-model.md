# Standard Cost Model

An activity-based method for measuring the administrative burden a regulation imposes on businesses and citizens: each information obligation is broken into data requirements and administrative activities, and the cost is price (time multiplied by tariff, plus acquisitions) times quantity (population times frequency). Horus uses it to make compliance costs defensible and comparable across options.

When Horus uses this: P4 on the regulatory pathway for every option that creates, changes or removes information obligations; the toolkit's `scm` module implements it.

## What it is

The Standard Cost Model (SCM) originated in the Netherlands and was codified by the international SCM Network (International SCM Manual, 2005); it underlies the EU's administrative-burden measurements and appears in the Better Regulation Toolbox's cost typology, and the UK's 2005 Administrative Burdens Measurement Exercise. The model distinguishes administrative burdens (costs incurred only because of the regulation) from business-as-usual costs (information the firm would collect anyway) and from substantive compliance costs (changing production, equipment, processes) and enforcement costs borne by government. For each information obligation (a duty to provide information to a public authority or third party) the analyst identifies the data requirements, the administrative activities to meet them (familiarisation, data collection, form filling, submission, record keeping, inspection cooperation), the time per activity for a normally efficient business, the tariff (wage cost plus overhead), external costs (advisers, software), and the quantity (number of entities affected times frequency per year). The product is a standardised annual cost that can be compared across options and tracked after implementation.

## When Horus uses it

- Regulatory pathway: `appraisals.regulatory.compliance_cost_scm` is a required block of the `ria` appraisal; options are compared on administrative burden by firm size, and design changes (digital submission, once-only data, thresholds) are costed.
- Programme pathway: the burden on applicants (eligibility evidence, forms, renewals) is measured the same way; it drives take-up.
- Institutional pathway: when a regulator's reporting requirements are redesigned.
- Monitoring: the SCM baseline becomes the indicator for burden-reduction targets.

## Steps

1. **Map the information obligations** in the baseline and in each option, from the legal text or draft provisions.
2. **Decompose** each into data requirements and administrative activities.
3. **Parameterise**: time per activity (from interviews with a small number of normally efficient firms, expert panels, or comparable measurements elsewhere), tariff by staff category, external costs, population by firm size, frequency.
4. **Separate** business-as-usual costs and substantive compliance costs; record them but do not count them as administrative burden.
5. **Compute** the annual burden per obligation and per option, by firm size; produce low and high cases from the parameter ranges.
6. **Test design changes**: digital by default, pre-filled forms, once-only data sharing, exemptions and thresholds, reduced frequency; recompute.
7. **Present** the burden alongside benefits and the other cost categories; never as the whole cost of the regulation.
8. **Record** parameters as assumptions with sources, and the model as an artefact.

## Outputs → state records

- `appraisals.regulatory.compliance_cost_scm` with the per-option annual burden, by firm size, low and high; `appraisals.impacts[]` on dimensions `administrative_burden`, `business_compliance_cost` and `sme`, with `method: scm` and `quantified: true`.
- `appraisals.methodology: scm` where SCM is the main quantitative method, otherwise `mixed`.
- `assumptions` (`category: cost`, `demographic`) for time per activity, tariffs, population and frequency, with `basis` and ranges.
- `evidence` from firm interviews (`attribution` rule applied) and from comparable measurements.
- `artefacts[]` on the appraisal: the SCM workbook or notebook and CSV, with `inputs_hash`.
- `appraisals.monitoring.indicators[]` for burden tracking; `appraisals.regulatory.sme_test` draws on the by-size results.

## Pitfalls

- Treating administrative burden as the total cost of regulation; substantive compliance costs are usually larger and belong in `business_compliance_cost`.
- Measuring the cost for the least efficient firm; the standard is the normally efficient business, with the range shown.
- Counting business-as-usual information gathering as burden.
- Population figures without a source or a size breakdown; the SME test depends on them.
- Precision theatre: SCM results are estimates with wide ranges; present them so.

## Source

SCM Network, International Standard Cost Model Manual: Measuring and Reducing Administrative Burdens for Businesses, 2005; European Commission, Better Regulation Toolbox, Standard Cost Model tool (BENCHMARKS.md B3).
