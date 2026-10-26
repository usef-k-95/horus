# Problem classification

The Principal's decision procedure after intake: twelve questions that separate the six advisory pathways, the record that captures the answer as a `problem_classification` analysis, how to compose a hybrid, and when and how to revisit the choice at AP2.

When Horus uses this: P0, after the RFP and attachments are parsed and the problem statement is reframed, before the AP0 email proposes a pathway; again at AP2 if the diagnosis changes the problem.

## Classification questions

Answer each from the RFP, the attachments and the first clarifications; cite the document or evidence for each answer. A question with no evidence is an open question for the client, not a guess.

1. **Is a specific legal or regulatory instrument the decision at stake** (create, amend, repeal, license, mandate, standard)? Yes points to `regulatory`. If the instrument exists and is unenforced, note the signal for `transformation_delivery`.
2. **Is there a funding or approval decision for a defined programme or asset**, with a gateway, a budget line, a loan or a grant? Yes points to `public_investment_business_case`.
3. **Does a policy or programme already exist and underperform against targets**, with the mandate to make it deliver rather than redesign it? Yes points to `transformation_delivery`.
4. **Is the question who should do what**: mandates, governance, organisation, decision rights of an entity or a system of entities? Yes points to `institutional_operating_model`.
5. **Does the brief ask for direction over a horizon**, across several instruments, with objectives and targets to be set? Yes points to `strategy`.
6. **Is the object a service or programme experienced by citizens or firms**, with eligibility, channels, take-up and user journeys at issue? Yes points to `programme_service_design`.
7. **Who is the client and what do they control?** A regulator or legal unit: `regulatory`. A finance ministry gateway or sponsor seeking approval: `public_investment_business_case`. A centre of government or delivery unit: `transformation_delivery`. A planning ministry or head of government's office: `strategy`. A public service commission or an entity reviewing itself: `institutional_operating_model`. A service-owning agency or digital unit: `programme_service_design`.
8. **What does the required deliverable look like?** RIA report, instrument outline: `regulatory`. Business case, appraisal summary: `public_investment_business_case`. Strategy document, roadmap: `strategy`. Blueprint, governance charter: `institutional_operating_model`. Delivery plan, dashboard: `transformation_delivery`. Service design, blueprint, pilot plan: `programme_service_design`.
9. **What is the legal route and the clock?** A legislative session: `regulatory` or `institutional_operating_model`. A budget cycle: `public_investment_business_case`. A term of office or a published target date: `strategy` or `transformation_delivery`. A launch date for users: `programme_service_design`.
10. **What evidence will decide it?** Legal stock, market analysis and compliance data: `regulatory`. Demand, cost and asset condition: `public_investment_business_case`. Performance time series by unit: `transformation_delivery`. Mandates, decision rights and capability: `institutional_operating_model`. Trends, benchmarks and scenarios: `strategy`. User research, take-up and cost to serve: `programme_service_design`.
11. **Does the client's framing name a solution, and what problem does the reframing reveal?** "We need a regulation" may be a delivery or service problem; "we need a strategy" may be an institutional one. The reframed problem statement, not the RFP's title, drives the answer.
12. **Where would failure most likely come from**: design, capacity, legitimacy or funding? Design of a rule or service points to `regulatory` or `programme_service_design`; capacity and routines to `transformation_delivery`; mandate and legitimacy to `institutional_operating_model`; funding to `public_investment_business_case`; direction and coalition to `strategy`.

## Recording the classification

Create an `analyses` record of kind `problem_classification` with `title`, `question` (the reframed problem statement), `inputs` (the RFP and attachment `documents`, any `evidence`), `method_notes` (this procedure), `frameworks` (the ids consulted), `findings[]`, `limitations[]` and `content`:

- `signals[] {question, answer, evidence: → DOC or EVD}`: one entry per question above, with the document or evidence that supports the answer, or a note that it is unanswered and the `open_questions` id raised.
- `candidates[] {pathway, fit 1 to 5, rationale}`: every pathway scored. Fit 5: the pathway's typical brief, deliverable and evidence all match. Fit 4: most signals match with one counter-signal. Fit 3: a real component of the engagement. Fit 2: a minor component. Fit 1: not relevant. Rationale cites the signals.
- `primary`: the single pathway with the highest fit, which must be 4 or 5. If no pathway reaches 4, do not classify; raise the clarifications and propose a provisional primary in the AP0 email, marked provisional in `rationale`.
- `secondary[]`: pathways with fit 3 or more that are not primary, at most two.
- `hybrid_notes`: which components of the engagement each secondary pathway governs (for example "the licensing pillar of the strategy is appraised as `ria`"), and which gate criteria variants from the secondary pack apply.
- `revisit_triggers[]`: the specific findings at P2 that would change the classification (for example "if enforcement data show the existing rule is adequate but unenforced, move primary to `transformation_delivery`").

Then set `engagement.pathway {primary, secondary[], rationale, classified_in: → this ANA}` and propose a `decisions` record of kind `pathway` with `statement`, `rationale` and `alternatives_considered[]` (the other candidates with fit 3 or more). The AP0 email states the proposed pathway and approach in one paragraph. The decision is `confirmed` at AP0 with the client as `made_by` and the email or meeting as channel or forum; `engagement.pathway.confirmed_in` points to it. The AP0 gate requires the analysis and the confirmed decision.

## Handling hybrids

One primary pathway always governs the engagement: it sets the diagnostic lens, the appraisal `kind` for the main options, the core Tier-2 deliverable set and the gate criteria variants. A secondary pathway contributes modules, not a second engagement:

- Options that belong to the secondary pathway take that pathway's option `kind` and are appraised with that pathway's appraisal `kind`, with `appraisals.pathway` set to the secondary pathway. A strategy whose licensing pillar is a regulatory instrument carries a `ria` appraisal for that option at `proportionality_level: light` or `standard`; a business case whose delivery requires a new agency carries an `operating_model` appraisal for that component.
- The secondary pack's diagnostic analysis kinds are added to the AP2 checklist only for the component in scope, and its Tier-2 deliverables are added only if the brief requires them; otherwise the component is a chapter of the primary deliverable.
- Frameworks from both packs are selected in `approach.frameworks[]` with `rationale` naming the component each serves.
- `hybrid_notes` is the authoritative statement of the split; the workplan's workstreams mirror it.
- Two candidates tied at fit 4 or 5 are resolved by questions 7, 8 and 9 (client, deliverable, clock); if still tied, the Principal proposes the pathway whose core deliverable the client must submit, and records the alternative in `alternatives_considered`.

## Revisiting at AP2

The diagnosis may show a different problem from the one the RFP implied. Before the diagnostic readout the Principal checks the `revisit_triggers[]` against the P2 findings. If a trigger has fired:

1. Create a new version of the `problem_classification` analysis with the updated signals, candidates and rationale, citing the diagnostic evidence; set the old version to `superseded`.
2. Propose a `decisions` record of kind `pathway` that `supersedes` the AP0 decision, with `implications[]` (appraisal kind, deliverables, workplan, frameworks) and `alternatives_considered[]`; list it in the AP2 meeting's `decisions_sought[]`.
3. On confirmation, append to `engagement.pathway.revisions[] {date, from, to, decision}` and update `primary` and `secondary[]`; revise `approach` (frameworks, workstreams) and `workplan` (activities, gate criteria) with `change_log` entries that cite the decision; re-parameterise the gate checklists from the new pack.
4. Communicate the change to the client in the AP2 readout as a finding and a decision sought, never as a surprise in the final deck.

Typical triggers: the rule exists and the failure is enforcement (regulatory to transformation); the programme's design is the cause of underperformance (transformation to programme and service design); the asset is sound and the operator is the problem (investment to institutional); the strategy's one decisive pillar is a single instrument (strategy to regulatory); a client directive narrows or widens scope (any). After AP2, pathway changes are exceptional and require a `scope` decision as well.

## Proposed schema additions

- `engagement.pathway.secondary[]` as objects `{pathway, components[]}` rather than bare enums, so the hybrid split is machine-readable and gate checklists can be parameterised per component.
- `analyses.content.candidates[]` for kind `problem_classification`: an optional `counter_signals[]` field, so the reason a high-fit candidate was not chosen is recorded next to its score.
