# Institutional diagnostic

A structured assessment of a public entity or system of entities: mandates and overlaps, functions, decision rights, capability, incentives and accountability, read against what the mandate requires. It tells the Principal whether the problem is the organisation's design, its capacity or its environment before any target model is drawn.

When Horus uses this: P2 on the institutional and operating-model pathway, and as a secondary lens on transformation and delivery engagements.

## What it is

Institutional diagnostics draw on World Bank institutional and governance assessment practice, OECD Public Governance Reviews and the UK Cabinet Office Capability Reviews. The common frame has six layers. Mandate: the legal basis, the functions assigned, and overlaps or gaps with other bodies. Functions and processes: what the entity actually does, with volumes and costs. Governance and decision rights: who decides, agrees, recommends and performs, formally and in practice. Capability: people, systems, data, money, against what the functions need. Incentives and accountability: what the entity and its staff are rewarded and sanctioned for, to whom it reports and how performance is seen. Environment: the political economy and the clients it serves. The diagnostic is comparative where possible, against peer institutions and against the entity's own mandate.

## When Horus uses it

- Institutional and operating-model pathway: the diagnostic is the gate product for AP2 and the "current-state diagnostic" chapter of the operating-model blueprint.
- Transformation and delivery pathway, when delivery-chain analysis points to one institution as the bottleneck.
- Regulatory pathway, for the regulator's capacity to enforce the instrument under design.
- Public investment pathway, for the management case (is the sponsor capable of delivering).

## Steps

1. **Mandate review.** Read the founding law, decrees and strategies; list functions assigned; map overlaps and gaps against other bodies in a functions-by-institution matrix.
2. **Function and process baseline.** For each major function: volumes, cycle times, cost, staffing, outputs. Use administrative data and client documents; mark estimates.
3. **Decision-rights map.** For the ten or so decisions that matter most, record who holds each RAPID role on paper and in practice; note where they differ.
4. **Capability assessment.** People (numbers, skills, vacancies, turnover), systems and data, budget adequacy and predictability, leadership stability. Rate maturity per function on a simple scale with evidence.
5. **Incentives and accountability.** Performance frameworks, reporting lines, budget rules, career incentives, external scrutiny; identify where incentives contradict the mandate.
6. **Environment.** Political economy of the entity: its sponsors, rivals and clients; past reform attempts and why they stalled.
7. **Synthesis.** State the three to five root causes of underperformance, each tied to evidence, and classify them as design, capacity or environment. This classification drives the option logic.
8. **Benchmark.** Compare mandate, size, governance form and performance with two to four peer institutions chosen for comparability.

## Outputs → state records

- `analyses` record of kind `institutional_diagnostic` with `content` across the six layers and `findings[]` classified as design, capacity or environment.
- Functions matrix and peer comparison: `analyses` of kind `benchmark` with `comparators[]`, `dimensions[]`, `table[]`.
- Decision rights: `stakeholders.decision_role` for the units and office holders involved; `analyses` of kind `internal_politics` for the entity.
- Organisation facts: `profiles` with `scope: organisation`, `structure.units[]`, `factions_assessed[]` (sensitive-personal).
- Root causes: `hypotheses` of kind `diagnostic` with evidence links.
- Capability gaps carried to appraisal: `appraisals.operating_model.capability_gap`; legal issues to `operating_model.legal_changes_required[]`.
- Risks of scope `implementation` and `legal`.

## Pitfalls

- Assessing the organisation chart rather than the functions; reorganisations that move boxes without changing decision rights or incentives rarely work.
- Relying on self-assessment interviews from the entity's leadership; triangulate with clients, overseers and data.
- Calling every problem a capacity gap; many are design or incentive problems that more staff will not solve.
- Comparing with institutions from very different legal traditions without saying so.
- Publishing judgements about named leaders; those belong in profiles and stay there.

## Source

World Bank institutional and governance assessment practice (BENCHMARKS.md B8 for World Bank sources); OECD Public Governance Reviews series (OECD, ongoing); UK Cabinet Office, Capability Reviews programme, 2006 to 2012.
