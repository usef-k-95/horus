# Operating-model assessment

How Horus appraises operating-model and governance options for an entity or a system of entities: fit to mandate, capability gap, transition risk, legal changes required and cost delta, scored against the validated principles and the political map.

When Horus uses this: institutional and operating-model pathway, phase P4, appraisal kind `operating_model`; also when another pathway's preferred option needs a new institutional home (a regulator for a new regime, a delivery unit, a programme agency).

## What is being appraised

Options of kind `operating_model`: archetypes (ministry department, executive agency, independent regulator, shared-service or network model, regulator-operator split, corporatised entity, outsourced or partnership model) and their governance variants (board composition, reporting line, decision rights, funding model), plus transition paths (big bang, phased by function, pilot entity). The baseline is the current model with the dysfunctions the `institutional_diagnostic` analysis found, projected forward: overlaps persist, vacancies stay unfilled, the backlog grows at its current rate.

## Method

`methodology` is normally `mixed`: a multi-criteria comparison against the principles for the design dimensions (`strategic-options.md` gives the mechanics with `mca.mca`), a costed delta for the fiscal dimension, and evidence-rated feasibility. Five lenses populate the `operating_model` block.

### Fit to mandate

Decompose the mandate into functions from the legal texts in the ledger (`evidence` of kind `legal_provision`): what the entity must do, may do and must not do, and the decision rights each function implies. For each option, map every function to an owner and a decision right using RAPID (recommend, agree, perform, input, decide) and test: no function without an owner; no decision with two deciders; regulatory and operational roles separated where the mandate or international practice requires it; accountability lines that end at a minister, a board or a legislature. Score fit as the share of mandate functions cleanly owned, with the gaps and overlaps listed. Record in `operating_model.fit_to_mandate` as a short text with the score and the gap list, and in the `legal_and_institutional` impact row.

### Capability gap

For the capabilities the target model needs (leadership and strategy, policy and analysis, regulation or operations, finance and procurement, people, data and digital, legal, communications), rate current maturity 1 to 5 from the diagnostic and interviews, rate the maturity the option requires, and state the gap, the route to close it (recruit, train, transfer, contract, partner) and the time it takes. Capability is the usual reason an elegant archetype fails; where the gap is three levels or more on a core capability, the option needs a transition path that buys that capability first. Record in `operating_model.capability_gap` and reflect it in `feasibility.administrative`.

### Transition risk

Transition risks are what goes wrong between the decision and the steady state: service continuity during the move, staff transfer and terms (unions, civil-service rules), loss of institutional memory, IT and data migration, budget gaps in the transition year, the legal window closing before the entity exists, leadership vacancies, and the political cost of visible disruption. Each is a `risks` record with `scope: implementation` or `political`, scored likelihood × impact, with mitigation and owner; `operating_model.transition_risk` summarises the profile (low, medium, high) and names the top three with their RSK ids. The transition path is a design choice: compare paths as variants when the risk profile differs materially.

### Legal changes required

List every instrument the option needs with its type (constitutional provision, primary law, decree, regulation, charter or statute of the entity, budget line, MoU or service agreement), the change (new, amend, repeal), the owner, the normal time to enact in this jurisdiction, and whether it fits the political calendar's window (`feasibility-scoring.md`). Primary legislation is a different proposition from a decree: say which options can be done under existing powers. Record in `operating_model.legal_changes_required[]`, rate `feasibility.legal` from it, and carry the list into the Tier 2 inventory of legal and regulatory changes.

### Cost delta

Cost against the baseline, not absolute cost: the recurring opex delta (staff, premises, systems, board and oversight costs, duplicated functions removed), the one-off transition cost (severance or transfer, recruitment, IT migration, legal and change support, dual running), and any revenue effect (fees, cost recovery). Use ranges; the main drivers (headcount, pay scales, systems) are `assumptions` records. Discount with `cba.present_value` over the horizon if options differ in timing; otherwise show year by year. Record in `operating_model.cost_delta` with the price base year and in the `fiscal_cost` impact row. Apply an uplift for optimism on transition costs where the client has a record of over-runs, and say what uplift and why.

## Political feasibility and the reaction matrix

Operating-model options redistribute power: a merged agency has a loser, a new regulator takes decisions a ministry used to take. The `internal_politics` analysis and the reaction matrix are therefore inputs to the appraisal, not context. For each option, name who loses decision rights, budget or staff, their predicted reaction (`stakeholders.predicted_reactions`) and whether they can veto or delay. Rate `feasibility.political` with that evidence.

## Common blocks

`baseline`; `impacts` (mainly `legal_and_institutional`, `fiscal_cost`, `administrative_feasibility`, `political_feasibility`, `employment`, `digital_and_data`, with `consumer_welfare` or `economic_output` where service levels change); `summary` with `mca_score` and `rank`; `distributional` (which regions or user groups gain or lose service access); `feasibility`; `sensitivity` (at least the cost delta under low and high headcount and systems assumptions, `montecarlo.tornado` where the model is numeric); `risks`; `monitoring` (decision cycle times, vacancy rates, service indicators, with baselines); `caveats`; `artefacts`.

## The `operating_model` block

`fit_to_mandate` (text with score and gap list), `capability_gap` (table by capability with current, required and route), `transition_risk` (profile and top risks pointing to RSK ids), `legal_changes_required[]` (one entry per instrument), `cost_delta` (recurring, one-off, revenue effect, price base year, range). Rule 20 requires every field; where a field is genuinely not applicable, write "none" with the reason, never leave it empty.

## Pitfalls

Comparing a target model's design with the baseline's dysfunction (both must be projected forward); scoring archetypes in the abstract rather than the specific design (board, funding, reporting line); costing the steady state and forgetting the transition year; a legal list that stops at "a new law is needed"; ignoring who loses; treating independence as free (it has oversight, appointment and accountability costs); copying a foreign archetype without checking the civil-service and budget rules that made it work there.

Source: Rogers and Blenko, "Who Has the D?" (Harvard Business Review, 2006) for RAPID; Andrews, Pritchett and Woolcock, Building State Capability (2017) for problem-driven iterative adaptation; OECD Public Governance Reviews; World Bank institutional and governance assessment practice; UK Cabinet Office, Public Bodies Handbook and classification guidance for arm's-length bodies.
