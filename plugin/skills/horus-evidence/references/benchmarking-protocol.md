# Benchmarking protocol

International benchmarking in Horus is a controlled comparison: four to six jurisdictions chosen against written criteria before any searching, the same dimensions extracted for each from the same kinds of sources, and a `benchmark` analysis in which every cell is an evidence record. This file sets selection, extraction, the anti-cherry-picking rules, the analysis shape and a worked skeleton.

**When Horus uses this:** P2 diagnosis (what others did and what happened), P3 option design (precedents for the long list, `options.precedents`), P4 appraisal (effect sizes and cost evidence by analogy), and the Tier 1 international benchmark table slide.

## Selecting comparators

Write the criteria into the brief first, then search. Four axes, each scored 1 to 3 for closeness to the client:

1. **Income level**: World Bank income classification and GDP per capita band; fiscal capacity.
2. **Governance tradition**: parliamentary or presidential; unitary or federal; administrative tradition (Westminster, Napoleonic, Germanic, post-Soviet, developmental state); administrative capacity where relevant.
3. **Legal family**: common law, civil law of French or German lineage, mixed systems, systems with religious-law components; whether the instrument at stake is primary legislation, decree or agency rule in that system.
4. **Problem scale and shape**: population and firm counts, informality, digital penetration, market concentration, the size of the sector or programme; the stage the comparator was at when it acted.

Then the admissibility filters: the comparator did something comparable within the last fifteen years; an ex post evaluation or at least official outcome data exists; sources are reachable in a language Horus works in. Compose the set: two structural peers (close on axes 1, 3 and 4), one regional peer the decision maker treats as a reference, one frontier case that shows the full design space, and one cautionary case where the reform stalled, was reversed or produced documented side effects. Record the long list of eight to fifteen candidates with scores and the reason for each exclusion; this list is the first defence against the charge of cherry-picking.

## What to extract

The same dimensions for every comparator, fixed before extraction:

- Context: income group, population, governance and legal family, the baseline value of the problem metric when the reform began.
- Instrument and design: legal basis and issuing authority; scope and thresholds; phasing; institutions and mandates; technology or delivery model; obligations on firms or citizens; incentives, support measures and penalties; cost to comply where measured.
- Timeline: announcement, legal adoption, first mandatory date, full coverage, major revisions.
- Results: adoption or compliance rates; outcome metrics; fiscal effects; distributional effects; unintended effects.
- Evaluation: who evaluated (audit institution, ministry, IMF or World Bank, academic), method, verdict.
- Transferability: what differs from the client that would change the result.

Sources by dimension: legal texts and gazettes (A) for design and timeline; official statistics and administrative data (A) for results; evaluations and IO reports (B); quality press (C) only for events. For quantitative dimensions use one database and one vintage across all comparators (data-connectors.md); never place a national figure for one country beside a WDI figure for another in the same row without saying so.

## Avoiding cherry-picking

- Criteria and long list before search; exclusions written down.
- Same dimensions, same period, same source types for all; a missing cell is recorded in `limitations[]`, never filled with a looser source for one comparator.
- At least one comparator whose experience cuts against the emerging recommendation.
- Report the range across comparators, not the best case; a lesson cites cells from at least two comparators or says it rests on one.
- A transferability note for every comparator; a lesson without one is not a lesson.
- Dates on everything; a design copied from a comparator's 2012 regime that was revised in 2019 is a different design.
- The researcher does not rank comparators by how well they support a hypothesis; the Principal reads the whole table.

## The `benchmark` analysis

`content`: `comparators[] {country, why_chosen}` (ISO 3166 alpha-3; `why_chosen` names the axes it is close on and its role in the set); `dimensions[]` (the fixed list as used); `table[] {comparator, dimension, value: → EVD}` (one evidence record per cell, with its own sources, `value` fields and `as_of`); `lessons[]` (each names the cells it rests on and its transferability caveat). Common fields: `inputs` (all SRC and EVD), `method_notes` (criteria, long-list path under `analysis/benchmarks/`, data vintage), `findings[]` with confidence, `limitations[]` (missing cells, definitional differences). The Tier 1 benchmark table renders from `table[]` with one source line per row; cells below the grade floor show as indicative.

## Worked skeleton (fixture: mandatory e-invoicing for small firms)

Criteria: upper-middle or lower-middle income; civil-law or mixed system preferred, one common-law case for contrast; a general e-invoicing mandate phased by firm size within the last fifteen years; official adoption data; a published evaluation preferred. Long list of eleven candidates scored and filed at `analysis/benchmarks/RQ-07_longlist.md` (illustrative). Characterisations below are selection rationales to be verified against Tier A sources during the run, not findings.

| Comparator | Role in the set | `why_chosen` (summary) |
|---|---|---|
| MEX | Structural peer | Upper-middle income, civil law, federal; an early general mandate run by the tax authority through certified private providers; long outcome series; large informal sector |
| TUR | Structural peer | Upper-middle income, civil law, unitary; thresholds phased by turnover; tax-authority platform with private integrators |
| IND | Scale peer | Lower-middle income, common law; threshold phasing inside a national indirect-tax reform; very large micro-firm base |
| ITA | Frontier | High income, civil law; the first EU member with a general business-to-business mandate through a central exchange; substantial evaluation literature |
| KEN | Regional peer and cautionary watch | Lower-middle income, common law, African comparator with a recent extension to small traders; compliance-burden lessons still emerging |

Dimensions: legal basis and authority; scope and size thresholds; phasing calendar; technology model (clearance or post-audit; central platform or certified providers); SME support (free tools, grace periods, penalties); adoption by size class; VAT or revenue effects reported by evaluators; compliance-cost evidence; institutional set-up; transferability to EGY. Every cell is an `EVD-` id or a listed gap. Lessons are written last, from the table, each naming the cells it rests on.

## Proposed schema additions

`benchmark.content.selection_criteria[]`, `candidates_considered[] {country, scores, excluded_because}` and `table[].missing_reason`, so the anti-cherry-picking record lives in the analysis rather than in a side file; `content.data_vintage`.

Source: ARCHITECTURE.md §5.9 (international benchmarking protocol) and §7.3; STATE_SCHEMA.md §D1 `benchmark`; OECD comparative practice in Government at a Glance and its country reviews (compare like with like, state definitional differences, one source per indicator across countries).
