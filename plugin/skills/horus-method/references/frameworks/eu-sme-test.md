# EU SME test

The European Commission's method for assessing whether a proposal places a disproportionate burden on small and medium-sized enterprises: consult SME stakeholders, identify the affected businesses, measure the impact on SMEs, and assess alternatives and mitigating measures. Horus uses it for the SME test block of every regulatory appraisal and as a model for small-firm analysis on other pathways.

When Horus uses this: P3 to flag SME exposure of options and P4 to complete `appraisals.regulatory.sme_test` on the regulatory pathway; programme and investment pathways when small firms are the users or suppliers.

## What it is

The SME test is a tool of the Better Regulation Toolbox, applied in every impact assessment where businesses are affected. It has four steps. Consultation of SME stakeholders: SME representatives and firms are consulted specifically, not only through general consultation. Identification of affected businesses: which sectors and which size classes (micro, small, medium, by the EU definition on headcount and turnover or balance sheet) are affected, directly and indirectly, and how many. Measurement of the impact on SMEs: compliance and administrative costs per firm by size class, often as a share of turnover or profit, compared with large firms, plus effects on competitiveness, entry and innovation. Assessment of alternative options and mitigating measures: exemptions for micro-firms, lighter regimes, transition periods, simplified reporting, fee reductions, information and support, with the trade-off against the policy objective stated. The UK small and micro business assessment is the equivalent under the Better Regulation Framework.

## When Horus uses it

- Regulatory pathway: required for the `ria` appraisal and for the RIA report's preferred-option section; the Standard Cost Model supplies the cost-by-size figures.
- Programme pathway: eligibility and application burdens for small firms as beneficiaries or suppliers.
- Public investment pathway: procurement design and market capacity in the commercial case.
- Strategy pathway for SME or industrial strategies, where the test becomes the design lens rather than a check.
- Stakeholder work: SME associations are a standing interview group; their positions are evidence of kind `position`.

## Steps

1. **Define size classes** for the client's jurisdiction and the data available; record the definitions as assumptions.
2. **Identify affected firms**: sectors, size classes, numbers, direct and indirect exposure (as suppliers or customers of regulated firms); source the population from official statistics.
3. **Consult SME stakeholders**: targeted interviews and written input; record positions and the facts asserted for corroboration.
4. **Measure the impact** per firm by size class: administrative burden (SCM), substantive compliance costs, fees, effects on margins and entry; compare with large firms and express as a share of turnover where data allow; show ranges.
5. **Judge proportionality**: whether the burden is disproportionate relative to the policy benefit and to large firms.
6. **Design mitigations**: exemptions and thresholds, lighter regimes, phasing, simplified procedures, support and tooling; assess each for its effect on the objective, on competition between size classes and on enforcement.
7. **Record** the finding, the mitigations adopted and those rejected, with reasons.

## Outputs → state records

- `appraisals.regulatory.sme_test {applicable, finding, evidence}` and `appraisals.impacts[]` on dimension `sme` (and `business_compliance_cost`, `administrative_burden`, `competition`) with `affected_groups` by size class.
- `appraisals.distributional {groups[] (size classes), incidence[], equity_note}`.
- `assumptions` for size-class definitions and populations (`category: demographic`), with sources.
- `options.variants[]` and `design_parameters[]` for exemptions, thresholds and phasing; `options.target_groups[]`.
- `stakeholders` of category `industry_association` and `private_firm` with `engagement` and `predicted_reactions[]`; `evidence` of kind `position` from consultation.
- `decisions` of kind `guiding_principle` or `political_directive` where the client fixes SME treatment.

## Pitfalls

- Consulting associations only; associations represent their members' larger firms better than micro-firms.
- Cost per firm without a denominator; the disproportion shows as a share of turnover or profit.
- Exemptions that create a cliff edge at the threshold, with firms staying small to avoid it; consider phasing and lighter regimes.
- Mitigations that hollow out the policy; state the trade-off.
- Using EU size definitions in a jurisdiction with different ones without saying so.

## Source

European Commission, Better Regulation Toolbox, SME test tool, 2023 edition (BENCHMARKS.md B3); UK small and micro business assessment in the Better Regulation Framework guidance, 2023 (BENCHMARKS.md B4).
