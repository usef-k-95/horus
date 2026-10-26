# International benchmarking protocol

A disciplined way to compare the client's situation with other jurisdictions: choose comparators for comparability, fix dimensions and indicators, source every cell, and extract lessons about mechanism and context rather than league-table positions. Horus uses it in diagnosis and option design on every pathway, and as the evidence base for precedents.

When Horus uses this: P2 diagnosis on every pathway (the benchmark analysis is a standard AP2 product), P3 for precedents, and whenever the client asks "what do other countries do".

## What it is

Benchmarking in policy advice has two purposes: to position the client (how far behind or ahead on the baseline indicators) and to learn (what others did, in what conditions, with what results). The protocol keeps them separate. Comparators are chosen on stated criteria: similar income level and administrative capacity, similar legal tradition, the same problem solved recently, aspirational peers the decision maker respects, and a near neighbour the public compares with. Dimensions and indicators are fixed before data collection, from the issue tree. Every cell carries a graded source and a date; definitions are checked for comparability (the same word means different things across statistical systems). Lessons are drawn as mechanism statements ("mandates with a free tool and a 36-month phase-in reached small firms; mandates alone did not") with the context conditions that made them hold, so they can be carried into theories of change and precedents.

## When Horus uses it

- P2 on every pathway: the international benchmark table is a slide archetype and an AP2 expectation; on the strategy pathway it is central to the situational analysis.
- P3: precedents for each option, with outcome evidence; the regulatory pathway's "what other jurisdictions did" is required in RIA practice.
- P4: effect sizes and cost parameters from comparators populate assumptions as ranges.
- Communication: a respected peer's experience is often the most persuasive argument to a decision maker; the decision-maker lens says which peers.

## Steps

1. **Fix the questions** the benchmark must answer from the issue tree; stop if none would change the recommendation.
2. **Select four to eight comparators** on explicit criteria; record why each was chosen and which criterion it fails. Include at least one that tried and failed.
3. **Define dimensions and indicators** with definitions and the preferred source for each (official statistics, OECD and World Bank datasets, legal texts).
4. **Collect and grade.** One source record per dataset or document; one evidence record per cell; retrieval date and snapshot. Mark definitional differences.
5. **Normalise** where needed (per capita, purchasing power, share of GDP) and say so in the method notes.
6. **Analyse mechanism and context**: for each comparator that acted, what instrument, what conditions, what result, what evaluation exists; separate correlation from evaluated effect.
7. **Write lessons** as conditional statements with the confidence and the evidence; list what does not transfer and why.
8. **Carry forward**: precedents to options, parameters to assumptions, the table to the deliverable.

## Outputs → state records

- `analyses` of kind `benchmark` with `comparators[] {country, why_chosen}`, `dimensions[]`, `table[] {comparator, dimension, value: → EVD}`, `lessons[]`, `method_notes`, `limitations[]`.
- `sources` (types `official_statistics`, `io_report`, `legal_text`, `government_document`) and `evidence` (kind `statistic`, `fact`, `legal_provision`, `finding`) for every cell; the two-source rule applies to any figure used in a deliverable.
- `options.precedents[] {jurisdiction, programme, period, outcome, evidence}`.
- `assumptions` with `low` and `high` from the comparator range, `basis: evidence`.
- `hypotheses` supported or refuted by the comparison.
- The international benchmark table exhibit in `deliverables` (diagnostic deck, policy note, strategy document).

## Pitfalls

- Choosing comparators that flatter or frighten; state the criteria and include a failure case.
- League tables without mechanism; a rank tells the client nothing about what to do.
- Mixing definitions (for example SME thresholds, informality, "coverage") across statistical systems without saying so.
- Quoting a comparator's reported result without its evaluation; many programmes report outputs, not outcomes.
- Secondary sources (consultancy summaries, press) as the cell source; go to the primary and grade it.

## Source

Horus evidence protocol (horus-evidence skill); comparator and indicator practice drawn from OECD Government at a Glance methodology and World Bank policy notes for incoming governments (BENCHMARKS.md B8).
