# Operating-model archetypes

A short set of recurring ways to organise a public function: integrated within a ministry, a semi-autonomous executive agency, an independent regulator, a state-owned or commercial operator, a network or shared-service arrangement, and a regulator-operator split. Horus uses the archetypes to generate operating-model options quickly and to make the choice explicit before designing the detail.

When Horus uses this: P3 option generation on the institutional and operating-model pathway; P2 to classify the current state.

## What it is

Operating-model design in government draws on the agency literature (Pollitt and Talbot; OECD's work on distributed public governance) and on classification practice such as the UK Cabinet Office's public-bodies categories. The archetypes differ on a few design dimensions: distance from ministerial direction (policy, day-to-day, none); legal form (department, statutory body, company); funding (appropriation, fees, commercial revenue); governance (minister, board, independent commission); accountability instruments (performance agreement, licence, shareholder compact); and the separation of policy, regulation and delivery. The main archetypes are the ministerial directorate (policy and delivery inside the ministry), the executive agency (delivery at arm's length under a performance framework), the independent regulator (rule-setting and enforcement insulated from day-to-day politics), the public corporation or operator (commercial delivery under a shareholder and licence regime), the network or shared-service model (functions pooled across bodies with a coordinating centre) and the regulator-operator split (the same function separated into a regulated operator and an independent regulator). Hybrids are common and legitimate.

## When Horus uses it

- Institutional pathway: after the diagnostic classifies root causes as design, capacity or environment, the archetypes give the long list for design problems. Each archetype is a candidate target model; variants adjust the design dimensions.
- Transformation pathway when a delivery unit or agency set-up is in scope.
- Public investment pathway for the commercial case (who operates the asset) and the management case (who delivers the project).
- Regulatory pathway when the instrument requires a new or reformed regulator.

## Steps

1. **Classify the current model** on the design dimensions, with the legal basis for each.
2. **Derive design principles** from the diagnostic and the client's guiding principles: for example independence from political interference, accountability for results, fiscal control, user focus, speed of decision.
3. **Generate the long list**: each archetype that could house the functions, plus the status quo improved. For each, state the design dimensions, the functions in and out, and the decision rights (RAPID) for the critical decisions.
4. **Add transition paths**: for each target model, the sequence from today (legal change, staff transfer, budget separation, system migration) and quick wins achievable without legal change.
5. **Screen** on fit to mandate, legal change required, capability needed, cost delta, transition risk and political feasibility; carry two or three to appraisal.
6. **Benchmark** each shortlisted archetype against two or three peer institutions that use it, noting what made it work or fail there.

## Outputs → state records

- `options` of kind `operating_model` with `design_parameters[] {lever, setting, alternatives}` for the design dimensions, `variants[]`, `mechanism` and `precedents[]`.
- `analyses` of kind `options_screening` and `benchmark`.
- `appraisals` of kind `operating_model` with the `operating_model {fit_to_mandate, capability_gap, transition_risk, legal_changes_required[], cost_delta}` block and `feasibility`.
- Target RAPID tables in `design_parameters[]` and the `governance_charter` deliverable; the `transition_plan` and `operating_model_blueprint` deliverables.
- `implementation_plan.content.instruments_required[]` (law, decree, budget) and `institutional_arrangements`.
- `risks` of scope `implementation` and `legal` for transition.

## Pitfalls

- Choosing an archetype by fashion (agencification, then re-integration) rather than by the diagnosed problem.
- Designing structure before decision rights and funding; the box moves but the behaviour does not.
- Underestimating transition cost and time, especially staff transfers and legal change.
- Independence without accountability, or accountability instruments nobody will operate.
- Presenting one target model with no alternatives; appraisal and scrutiny bodies expect a real comparison.

## Source

Christopher Pollitt and Colin Talbot (eds), Unbundled Government: A Critical Analysis of the Global Trend to Agencies, Quangos and Contractualisation, Routledge, 2004; OECD, Distributed Public Governance: Agencies, Authorities and Other Government Bodies, 2002; UK Cabinet Office, Classification of Public Bodies: Guidance for Departments, 2016.
