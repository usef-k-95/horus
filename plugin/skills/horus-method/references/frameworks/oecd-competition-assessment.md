# OECD Competition Assessment Toolkit

A checklist and method for finding regulations that unnecessarily restrict competition and for designing less restrictive alternatives that achieve the same objective. Horus uses it for the competition check required in every regulatory appraisal and when a strategy or operating model affects market structure.

When Horus uses this: P3 to screen options for competition restrictions and P4 to complete `appraisals.regulatory.competition_check` on the regulatory pathway; also when a public operator or institutional design affects markets.

## What it is

The OECD Competition Assessment Toolkit has three volumes: Principles (why and how governments assess competition effects), Guidance (the analytical method) and an Operational Manual (how to embed it in rule-making). Its core is a four-part checklist. A regulation is flagged if it limits the number or range of suppliers (exclusive rights, licences or permits as a requirement to operate, limits on some suppliers' ability to provide a good or service, significantly raising costs of entry or exit, geographic barriers); limits the ability of suppliers to compete (controls on prices, advertising or marketing, quality standards that favour some suppliers, significantly raising costs for some suppliers relative to others); reduces the incentive of suppliers to compete (self-regulatory or co-regulatory regimes, requirements to publish information on outputs, prices or costs, exemptions from competition law); or limits the choices and information available to consumers (limiting the ability of consumers to choose a supplier, reducing mobility between suppliers through switching costs, changing information fundamentally). Flagged provisions are analysed in depth and alternatives designed; the assessment is proportionate to the likely harm.

## When Horus uses it

- Regulatory pathway: every shortlisted option is run through the checklist at P3; flagged provisions are analysed in the `ria` appraisal with the toolkit's method and an alternative is designed where possible. The EU and UK standards both expect this check.
- Strategy pathway: sector strategies that propose champions, exclusive rights or standards are screened.
- Institutional pathway: regulator-operator splits, state-owned operators and self-regulatory bodies raise the incentive-to-compete question.
- Programme pathway: eligibility rules and procurement choices that favour incumbent providers.

## Steps

1. **Identify the provisions** of each option that touch suppliers, entry, pricing, information or consumer choice.
2. **Run the checklist** question by question; record a yes, no or unclear with the reason for each.
3. **Define the market** affected for each flagged provision (product and geographic scope, current structure, barriers), using available data and evidence.
4. **Assess the likely effect**: on entry and exit, prices, quality, innovation and consumer choice; quantify where credible, otherwise qualitative with direction and size.
5. **Design alternatives** that achieve the regulatory objective with less restriction (performance standards instead of design standards, notification instead of licensing, time-limited rights, information remedies).
6. **Compare** the original and the alternative on objective achievement and competition effect; recommend.
7. **Record** the finding in the appraisal and the RIA's preferred-option section; propose a review clause where the restriction is retained.

## Outputs → state records

- `appraisals.regulatory.competition_check {applicable, finding, evidence}` and `appraisals.impacts[]` on dimensions `competition`, `consumer_welfare` and `innovation`, with `direction`, `rating` or estimate, and `affected_groups`.
- `options.screening.criteria[]` with the competition flag at P3; alternative designs as `options.variants[]` or new options.
- `evidence` on market structure (`kind: statistic`, `fact`) with graded sources; `analyses` of kind `baseline` for the market description.
- `appraisals.regulatory.review_clause` where a restriction is retained.
- `risks` of scope `legal` where a provision may conflict with competition law or trade obligations (`international_obligations` dimension).

## Pitfalls

- Running the checklist on the policy's intent rather than on its provisions; restrictions hide in licensing conditions and standards.
- Treating any restriction as disqualifying; the test is whether it is necessary and proportionate to the objective.
- No market definition, so effects cannot be judged.
- Ignoring self-regulation and information-sharing provisions, which reduce incentives to compete less visibly than price controls.
- Forgetting consumer switching costs and information effects, the fourth part of the checklist.

## Source

OECD, Competition Assessment Toolkit, Volumes 1 to 3: Principles, Guidance and Operational Manual (OECD, version 3.0, 2016).
