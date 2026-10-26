# OECD RIA best practice principles and the 2012 Recommendation

The OECD's reference standard for regulatory impact assessment: twelve principles of regulatory policy (2012) and the 2020 best-practice principles for RIA with their eight basic steps. Horus uses them as the method standard for every regulatory appraisal and as the reviewer's checklist for the RIA report.

When Horus uses this: P4 appraisal on the regulatory pathway (every `ria` appraisal records `OECD-RIA-2020` in `standards_applied`), and P2 to P3 for the problem-definition and alternatives steps.

## What it is

The 2012 Recommendation of the Council on Regulatory Policy and Governance sets twelve principles for whole-of-government regulatory policy, including open consultation, oversight institutions, RIA integrated early in policy development (goals, necessity, alternatives, trade-offs), ex post review, risk-based design and multi-level coherence. The 2020 Best Practice Principles for RIA elaborate how to run an RIA system: commitment and buy-in; governance and system design; embedding RIA through capacity and accountability; targeted and appropriate methodology; continuous monitoring, evaluation and improvement. Box 2.2 lists the basic steps of an RIA: consultation and stakeholder engagement; problem definition; objective; description of the regulatory proposal; identification of alternatives; analysis of benefits and costs; identification of the preferred solution; monitoring and evaluation framework. The principles insist on proportionality (a full quantitative cost-benefit analysis is not always required), on an enforcement and compliance strategy in every RIA, on iteration and on communicating results well.

## When Horus uses it

- Regulatory pathway: the eight basic steps are the skeleton of the RIA report and the order of P2 to P5 work; the `ria` appraisal is checked against them before AP4.
- Any pathway that produces a regulatory instrument as part of a package: the regulatory component is appraised to this standard even when the primary pathway is strategy or programme.
- Institutional pathway for regulators: the 2012 principles on oversight bodies and regulatory agencies inform the operating-model options.
- QA: the producer's logic and traceability audits of an RIA report use the eight steps and the proportionality statement as the rubric.

## Steps

1. **Consultation plan**: who is consulted, how, when, and how views will be reported by group; start before the problem definition is final.
2. **Problem definition**: the market, regulatory or institutional failure, its magnitude, who is affected, and why existing rules do not solve it; the baseline projection.
3. **Objective**: what the intervention must achieve, measurable and tied to the problem.
4. **Description of the proposal**: the instrument, its obligations, who it applies to, how it is enforced.
5. **Alternatives**: the non-regulatory and lighter options, each with a theory of change and the reason for carrying or dropping it.
6. **Benefits and costs**: by option, by affected group, quantified and monetised where credible, qualitative where not, with proportionality stated; compliance costs with the Standard Cost Model; competition and SME effects.
7. **Preferred solution**: the comparison and the choice, with the enforcement and compliance strategy, risks and sensitivity.
8. **Monitoring and evaluation framework**: indicators, data sources, a review date and the ex post evaluation method.

## Outputs → state records

- `appraisals` of kind `ria` with `standards_applied` including `OECD-RIA-2020` and the 2012 Recommendation, `proportionality_level`, `baseline`, `impacts[]`, `distributional`, `feasibility`, `sensitivity`, `monitoring`, and the `regulatory {sme_test, competition_check, compliance_cost_scm, enforcement_strategy, review_clause}` block.
- Step 1: `stakeholders.engagement`, `meetings` of kind `interview` and `workshop`, consultation synopsis by group in the RIA annex.
- Steps 2 and 3: `analyses` of kind `baseline` and `diagnostic`; `brief.objectives[]`.
- Steps 4 and 5: `options` with `instrument_types[]` and `mechanism`; `analyses` of kind `options_screening`.
- Step 7: `analyses` of kind `option_comparison`; `decisions` of kind `preferred_option`.
- Step 8: `appraisals.monitoring {indicators[], evaluation}`.
- `deliverables` of type `ria_report` following the structure in ARCHITECTURE.md section 7.5.

## Pitfalls

- Treating RIA as a document written after the decision; the principles require it to inform the decision, which is why Horus starts it at P2.
- Quantifying everything or nothing; proportionality means the depth matches the stakes, and the report says what level was chosen and why.
- Omitting the enforcement and compliance strategy, a recurring OECD finding.
- Consultation reported as "stakeholders were consulted"; views are reported by group with how they changed the proposal.
- No review clause; the monitoring framework is a basic step, not an annex.

## Source

OECD, Regulatory Impact Assessment: Best Practice Principles for Regulatory Policy, 2020 (BENCHMARKS.md B1); OECD, Recommendation of the Council on Regulatory Policy and Governance, OECD/LEGAL/0390, 2012 (BENCHMARKS.md B2).
