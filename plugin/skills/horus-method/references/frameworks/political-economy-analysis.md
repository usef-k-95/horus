# Problem-driven political economy analysis

The World Bank's method for explaining why a sensible reform has not happened: map the institutions, interests, incentives and power behind a specific policy problem, then identify what is feasible and how to widen the space. It turns "political will" from an excuse into an analysable variable.

When Horus uses this: P2 diagnosis on the institutional and operating-model pathway, and on any pathway where past attempts at the same reform failed or stakeholders are polarised.

## What it is

Problem-driven political economy analysis (PEA) starts from a concrete development or policy problem rather than from a general country governance assessment. It asks three layered questions: what are the structural factors (history, geography, economic base) that shape the issue; what are the institutions (formal rules and informal norms) that govern it; and what are the interests and incentives of the actors who can block or carry change. The output is a feasibility map and a set of operational implications: which reform variants have a coalition behind them, what sequencing creates momentum, where to build consensus and where to avoid confrontation.

## When Horus uses it

- Institutional and operating-model pathway anchor framework, because mandates and decision rights are distributional questions between organisations.
- Regulatory pathway when incumbents or a ministry have blocked similar regulation before.
- Public investment pathway when the question is why a project pipeline is captured.
- Feeds the internal politics map, the reaction matrix and the political feasibility rating in every appraisal. Interview planning draws its hypotheses from here.

## Steps

1. **Specify the problem** in the same terms as the brief's reframed problem statement, and list the reforms previously attempted with dates and outcomes.
2. **Map structural factors.** Fiscal position, economic structure, rents at stake, demographic pressures, external anchors (donors, trade agreements, accession processes) and the electoral or appointment cycle.
3. **Map institutions.** The formal rules (constitution, laws, mandates, budget rules) and the informal ones (patronage, clientelism, bureaucratic norms, veto practices). Note where formal and informal diverge; that gap is usually where reform fails.
4. **Map actors, interests and incentives.** For each actor that can block, delay or carry the reform: what it gains or loses, what it has done before, who it answers to. Separate stated positions from underlying interests.
5. **Identify the feasible space.** Which reform variants are acceptable to a sufficient coalition, which require compensating losers, which must wait for a window.
6. **Draw operational implications.** Entry points, sequencing, coalition-building moves, what to communicate to whom, and the warning signs that the analysis is wrong.
7. **Keep it current.** Revisit after every round of interviews and before each gate; stances move.

## Outputs → state records

- The analysis: an `analyses` record of kind `internal_politics` for the client entity and its units (`units[]`, `positions_by_option[]`, `influence_paths[]`, `watch_points[]`), and a companion `analyses` record of kind `diagnostic` or `institutional_diagnostic` for the wider system.
- Actors: `stakeholders` records with `interests`, `concerns`, `red_lines`, `relationships[]` (type `funds`, `regulates`, `allied_with`, `rival_of`) and `predicted_reactions[]`.
- Deep research on key actors: `profiles` (sensitive-personal), with `implications_for_engagement[]` distilled into analyses.
- Hypotheses of kind `political` and `stakeholder`, tested through interviews.
- Feasibility: `appraisals.feasibility.political` and `risks` of scope `political`.
- Sequencing implications: `analyses` of kind `implementation_plan`, `sequencing[]`.

## Pitfalls

- Producing a country governance essay instead of an answer to a specific problem.
- Taking stated positions at face value; interests are inferred from behaviour and resources, then tested in interviews.
- Writing sensitive judgements about named officials into client-facing documents. Judgements stay in `profiles`; deliverables carry implications without attribution.
- Assuming the client is a neutral actor; the client's units have interests too.
- Freezing the analysis at P2. Political feasibility is re-rated at every gate.

## Source

Verena Fritz, Kai Kaiser and Brian Levy, Problem-Driven Governance and Political Economy Analysis: Good Practice Framework, World Bank, 2009; Verena Fritz, Brian Levy and Rachel Ort (eds), Problem-Driven Political Economy Analysis: The World Bank's Experience, World Bank, 2014. World Bank materials catalogued in BENCHMARKS.md B8.
