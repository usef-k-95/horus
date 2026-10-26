# OMB Circular A-4 (2023 revision, as method)

The US Office of Management and Budget's guidance to federal agencies on regulatory analysis: baseline, need for action, range of alternatives, benefits and costs, distributional effects, treatment of uncertainty, discount rates and the accounting statement. Horus cites the November 2023 revision as analytical method, not as current US law, because its legal status changed in 2025.

When Horus uses this: P4 on the regulatory pathway as a second method reference beside the OECD and EU standards (`OMB-A4-2023` in `standards_applied`), particularly for baselines, uncertainty and distributional analysis.

## What it is

Circular A-4 (first issued 2003, revised 9 November 2023) tells agencies how to conduct the regulatory analysis required for significant rules. The 2023 text covers: analytical approaches (benefit-cost and cost-effectiveness); scope; developing an analytic baseline (what the world looks like without the rule, including other rules and trends); identifying the need for federal action (market failure or other justification); alternative regulatory approaches (performance standards, market-based instruments, information, different stringency levels and compliance dates); assessing benefits and costs (willingness to pay, revealed and stated preference, benefit transfer, non-quantified effects); other considerations; transfers; distributional effects (by income, race, geography, with optional weighting); treatment of uncertainty (probabilistic analysis for large rules); discount rates (default real rate of 2.0 per cent, derived from the 30-year Treasury real yield, to be updated every three years; the 2003 text used 3 and 7 per cent); quality and reproducibility; and presentation through an accounting statement that tabulates annualised and present-value benefits and costs with ranges. Secondary reports indicate OMB rescinded the 2023 revision in February 2025 under Executive Order 14192 and that the 2003 text is again served; this is not verified against an OMB primary source.

## When Horus uses it

- Regulatory pathway: baseline construction (A-4's treatment of baselines that include other regulations and trends is the most explicit), the accounting statement as a presentation device, and the uncertainty chapter for choosing between scenarios, Monte Carlo and switching values.
- Any pathway with a monetised appraisal: the discount-rate discussion gives a transparent way to justify the client's rate and show results at alternative rates.
- Distributional analysis: A-4's guidance on reporting by group and on optional weights complements the Green Book annex.
- International clients: A-4 is the reference US practice; useful in benchmarking regulatory systems.

## Steps

1. **Baseline**: project the world without the rule over the analysis period, including trends, other rules and expected compliance with existing rules; state the period and why.
2. **Need**: identify the market failure or other rationale and show existing rules do not address it.
3. **Alternatives**: at least one less stringent and one more stringent alternative, different compliance dates, performance rather than design standards, market-based and informational approaches.
4. **Benefits and costs** for each alternative: incremental to the baseline, by year, with valuation methods stated; non-quantified effects described and their likely size and direction given.
5. **Transfers** separated from benefits and costs.
6. **Distribution**: who gains and who pays, by relevant groups; weights, if used, shown separately from the unweighted results.
7. **Uncertainty**: ranges for key parameters; probabilistic analysis where stakes are large; expected values and distributions reported.
8. **Discounting**: present values at the chosen rate and at alternatives; annualised values.
9. **Accounting statement**: a table of annualised and present-value benefits, costs and transfers with low, central and high estimates, and the non-quantified effects alongside.

## Outputs → state records

- `appraisals` of kind `ria` with `standards_applied` including `OMB-A4-2023` (method), `baseline {description, analysis}`, `impacts[]` with `estimate {central, low, high, present_value}`, `summary {npv {central, low, high}}`, `sensitivity {method: monte_carlo|scenarios|switching_values, parameters, results_path, robustness}`, `distributional`.
- `assumptions` for discount rate (`basis: convention`, `source_note` naming the standard and alternatives), valuation parameters with `low`, `high`, `distribution`.
- `analyses` of kind `baseline` for the counterfactual.
- The accounting statement as an `artefacts[]` entry (kind `report`) produced by the toolkit's `report` module, and the exhibit in the appraisal deck.

## Pitfalls

- Citing A-4 2023 as binding US law; cite it as method and note the status caveat.
- Applying a US discount rate to another country's appraisal without justification; the rate is an `assumptions` record with a stated basis.
- Baselines that assume full compliance with existing rules when the diagnosis shows otherwise.
- Hiding non-quantified effects below the accounting statement; they belong in it.
- Probabilistic analysis with made-up distributions; parameter ranges need a documented basis.

## Source

US Office of Management and Budget, Circular A-4: Regulatory Analysis, 9 November 2023 (archived), with the status caveat in BENCHMARKS.md B7; the 2003 text for comparison.
