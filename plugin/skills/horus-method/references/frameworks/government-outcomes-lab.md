# Government Outcomes Lab resources

The Blavatnik School of Government's Government Outcomes Lab (GO Lab) publishes guides, case studies, datasets and a value-for-money toolkit on outcomes-based contracting and impact bonds. Horus uses them when a programme or service option would pay for outcomes rather than inputs, and for value-for-money framing in programme and investment appraisals.

When Horus uses this: P3 option design and P4 appraisal on the programme and service design pathway when outcomes-based commissioning is a candidate delivery model; P5 for the evaluation and payment design.

## What it is

GO Lab is a research and practice centre at the University of Oxford on cross-sector partnerships and outcomes-based approaches. Its resources include "The Basics" guides to outcomes-based contracting and impact bonds (what they are, when they fit, how they are structured); a knowledge bank of case studies and publications; the INDIGO datasets of impact bonds and outcomes contracts worldwide; a toolkit covering the impact bond lifecycle and technical guidance; a value-for-money toolkit developed with CIPFA for assessing outcomes-based contracts; and a glossary. GO Lab does not provide a generic policy-design template; its value to Horus is a disciplined view of when paying for outcomes helps (measurable outcomes, room for provider innovation, a credible counterfactual, manageable measurement cost) and when it does not (outcomes hard to attribute, gaming risk, high transaction costs, thin provider markets), and a body of evidence on what outcomes contracts have achieved.

## When Horus uses it

- Programme and service design pathway: outcomes-based commissioning and impact bonds are service-concept variants on the delivery and funding dimensions; GO Lab's criteria screen them and its case studies supply precedents.
- Public investment pathway: value-for-money framing and the commercial case where a payment-by-results structure is proposed.
- Transformation pathway: outcome-based performance agreements with delivery actors are a lighter form of the same logic.
- Evidence: the INDIGO datasets and case studies are grade-A or B sources for precedents and effect sizes.

## Steps

1. **Test fit**: are outcomes measurable with existing or affordable data; can they be attributed to the provider; is there a credible counterfactual; is there a provider market; are gaming and cream-skimming risks manageable; are transaction costs proportionate.
2. **Define outcomes and payment metrics**: the outcome indicators, the payment triggers, caps and tariffs; the baseline and the verification method.
3. **Structure the contract**: commissioner, provider, investor (for impact bonds), outcome payer; risk allocation; duration; governance.
4. **Assess value for money** with the GO Lab and CIPFA toolkit logic: expected outcomes and savings against the cost of payments, financing and transaction costs; compare with a conventional contract and in-house delivery.
5. **Design evaluation**: independent verification of outcomes; evaluation of impact beyond the paid metrics.
6. **Draw on precedents** from INDIGO and the case studies for design parameters and realised results, with their evidence grade.

## Outputs → state records

- `options` of kind `service_concept` with `design_parameters[]` for delivery model, payment metrics and risk allocation, and `precedents[]` from GO Lab case studies.
- `options.screening.criteria[]` with the fit tests; `analyses` of kind `options_screening`.
- `appraisals` of kind `service_concept` with `service {outcomes[], take_up_estimate, cost_per_outcome, equity_assessment}` and `methodology: cea` or `mixed`; on the investment pathway `appraisals.five_case.commercial` and `economic`.
- `sources` (type `io_report`, `peer_reviewed`, `dataset`) and `evidence` for precedents and effect sizes.
- `appraisals.monitoring {indicators[], evaluation}` with the verification design; `risks` of scope `policy_outcome` for gaming and attribution.
- `deliverables` of type `service_design_document` and `pilot_evaluation_plan`; `financing_options_paper` where investors are involved.

## Pitfalls

- Paying for outcomes that are easy to measure rather than the ones that matter.
- Ignoring transaction and financing costs, which can exceed the efficiency gain.
- Cream-skimming and gaming unaddressed in metric design.
- Assuming a provider market exists; in many jurisdictions it does not.
- Treating impact bonds as a source of money rather than a contracting structure; the outcome payer is still the government.

## Source

Government Outcomes Lab, Blavatnik School of Government, University of Oxford: "The Basics" guides, knowledge bank, INDIGO datasets, and the GO Lab and CIPFA value-for-money toolkit (BENCHMARKS.md B13).
