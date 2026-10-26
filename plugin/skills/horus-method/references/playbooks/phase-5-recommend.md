# Phase 5: Recommend

Make the preferred option decidable and deliverable: the recommendation, the implementation and communication plans, the full tiered deliverable set with the pathway's core documents, the final presentation and the handover. Phase 5 ends at AP5 and the close of the engagement.

**When Horus uses this:** `engagement.phase` is `P5` and gate `AP5` is not `passed`, or AP5 is passed and handover actions remain.

## Purpose and exit criteria

Give the ultimate decision maker a decision they can take in five minutes and the client a plan they can execute on Monday. Gate AP5 (STATE_SCHEMA.md section 7) reports `ready` when: the `implementation_plan` and `communication_plan` analyses are `final`; the Tier 0, Tier 1 and the pathway's core Tier 2 `deliverables` are released with the traceability audit passed; every `client_inputs` record has a disposition (rule 15); every `risks` record has an owner; decisions of kind `recommendation` and `deliverable_approval` are `confirmed`; and the handover `actions` are `done`. Exit is the AP5 `gate` decision, the `gate_transition` approval, `set_gate AP5 passed`, then `set_phase closed` and `update engagement.status: closed` once handover is complete.

## Entry checks

`gates.AP4.status: passed`; the `preferred_option` decision `confirmed` and the option at `preferred`; its `appraisals` record promoted from `reviewed` to `final` after the AP4 changes; `option_comparison` at `reviewed`; all `assumptions` used in the final appraisal `agreed` or flagged; `client_inputs` from AP4 dispositioned; the `risks` register populated from the appraisal; the reaction matrix current; `brief.required_deliverables` reviewed so every item will map to a `deliverables` record; `settings.research_budget.per_phase.P5` (default two runs).

## Step by step

1. **Write the recommendation.** `create` `decisions` `kind: recommendation`, `status: proposed`, `proposed_by: horus`: a `statement` worded as the decision the ultimate decision maker accepts or rejects, with the do-nothing alternative named; `rationale` from the comparison; `implications[]`; `affects → OPT, DEL`. Write the master storyline: one answer-first argument every tier will summarise or expand. `update options {status: recommended}` only on confirmation.
2. **Plan implementation and activation.** `create` `analyses` `kind: implementation_plan` with `content {workstreams, sequencing[] {phase, actions, owners → STK, dates}, instruments_required[] {instrument, type, owner}, institutional_arrangements, budget {capex, opex, source}, capacity_needs, kpis[] {name, baseline, target, source, frequency}, delivery_chain, risks → RSK}`, `inputs → APL, ANA, EVD`, `findings`, `limitations`. Delegate one `analyst` for budget phasing and KPI baselines (inputs reference `assumptions` ids) and, if the budget allows, one `researcher` for implementation precedents. `update risks` so every record of scope `implementation`, `political`, `legal` or `fiscal` has `owner → STK`, `mitigation`, `early_warning`, `status`. Status `reviewed`, then `final` after the PM check-in that walks through owners and dates.
3. **Plan communication.** `create` `analyses` `kind: communication_plan` with `content {narrative, message_house {core, pillars, proofs → EVD}, audiences[] {stakeholder → STK, objective, messages, channels, timing, spokesperson, risks}, sequencing, qa_bank[] {question, answer, evidence}, opposition_handling}`, built from `view reaction_matrix` and the interview evidence. Every proof is a validated evidence id. Status `reviewed`, then `final`.
4. **Register the deliverable set.** `create` `deliverables` records, all driven from the master storyline: Tier 0 `decision_memo` and the five-to-eight-slide brief (`type: executive_deck`, `tier: T0`, titled as the brief); Tier 1 `executive_deck` (10 to 15 slides) and `executive_summary` (at most 1,000 words); Tier 2 `final_deck` (30 to 60 slides plus appendix), `implementation_plan`, `communication_plan`, and the pathway core documents named in the pack's `Core Tier-2 deliverables and structures`. Set `maps_to_brief` to the `required_deliverables` id each satisfies, `audience`, `storyboard_path`, `template`. Check that `brief.required_deliverables[].maps_to` is complete.
5. **Produce, top down.** Write the ghost deck for the full deck first; the executive deck and Tier 0 are selections from it; documents are the same argument in prose with the same evidence ids. Delegate one `producer` per deliverable (Tier 2 documents first, then Tier 1, then Tier 0), each with deliverable id, tier, storyboard, evidence ids, template, QA level full. Each `register_version` must show the five audits passing; the sensitivity audit is the one that fails here, because Tier 0 and Tier 1 attract profile-derived phrasing and off-record colour. A fresh `producer` reviews every Tier 0 and Tier 1 file; fix and re-register.
6. **Disposition every client input.** `list_records client_inputs` with `disposition: pending`; `update` each with `disposition`, `disposition_rationale` and `response {what_changed, deliverable_version}`. Rule 15 blocks release otherwise.
7. **Approve and release.** `request_approval` per version: `tier0_tier1_release`, risk `high` for Tier 0 and `medium` for Tier 1; `tier2_release`, risk `low`, for the core documents. `release_version` on each. `create` `decisions` `kind: deliverable_approval`, `status: proposed`, to be confirmed by the client at AP5.
8. **Set up the final presentation.** `create` `meetings` `kind: final_presentation`, `conduct_mode: principal_co_led`, `participants` (sponsor, steering, PM, Supervisor, Horus; the ultimate decision maker if the sponsor invites them), `decisions_sought` (recommendation approved; deliverables accepted; implementation owners confirmed; handover agreed), `agenda`, `prep_pack → DEL[]`, `plan {disclosure_script_id, consent_terms, attribution_rule}`. Pre-read: executive summary and decision memo to the sponsor as `communications` with `classification: client_dm`, approval class `decision_maker_email`, risk `high`; the full set to the PM under `client_pm_email`.
9. **Hold the presentation** per `alignment-point-protocol.md`, co-led case; capture as below.
10. **Hand over.** `create` `actions` `kind: internal_task` for: final versions marked `client_approved`; `export` of state without profiles (`include_profiles: false`) for the client's record; the bibliography, traceability table and assumptions register as annex files; transcript and recording retention check with `validate`; profiles deletion or retention per decision 6 in docs/DECISIONS.md, logged; the closing email. Mark each `done`. Then `set_gate AP5 passed`, `set_phase closed`, `update engagement {status: closed, dates.closed}`, final `checkpoint`.

## Pathway hooks

`Core Tier-2 deliverables and structures` in `horus-policy/references/pathways/<id>.md` names the documents and their section orders: `regulatory` produces `ria_report`, `policy_note` and `regulatory_instrument_outline`; `strategy` produces `strategy_document`, `implementation_roadmap` and `policy_note`; `institutional_operating_model` produces `operating_model_blueprint`, `governance_charter`, `transition_plan` and the inventory of legal changes; `transformation_delivery` produces `delivery_plan`, routines and stocktake design, `dashboard_specification` and a capability plan; `public_investment_business_case` produces `business_case` with `appraisal_summary_table` and `financing_options_paper`; `programme_service_design` produces `service_design_document`, `service_blueprint`, `pilot_evaluation_plan` and a cost-to-serve summary. Section orders are in ARCHITECTURE.md section 7.5 and in `horus-deliverables/references/`. The implementation plan also takes pack-specific content: enforcement strategy and review clause (regulatory); roadmap and KPIs (strategy); transition sequencing (institutional); routines and trajectories (delivery); procurement and approval stages (investment); pilot and scaling path (service).

## Client-facing artefact

Three tiers from one storyline. Tier 0 decision memo, at most two pages in ministerial-submission form: title; issue in 100 words or fewer, stating the financial impact; recommendation worded as the decision, with do-nothing offered; timing as a date; discussion (impact, evidence, options considered and why rejected, financial and legal implications, risks, consultation and stakeholder positions, communications and handling); implementation, owners and timeline; decision required; annex pointer. Tier 0 brief: five to eight slides, no slide over 40 words of body, 18 pt or larger. Tier 1 executive deck: (1) executive summary; (2) mandate and the problem; (3) diagnosis in two slides; (4) options considered and the principles applied; (5) appraisal comparison; (6) the recommendation; (7) implementation roadmap and governance; (8) budget and KPIs; (9) risks and mitigation; (10) communication and handling; (11) decisions sought; (12) next steps. Tier 1 executive summary opens with a one-sentence problem statement. Tier 2 full deck and the pack's core documents carry every back-up exhibit and the traceability table. Stamps move from `DRAFT FOR DISCUSSION` to `FINAL` on client approval.

## Capture after the alignment point

`decisions`: `update recommendation` and `deliverable_approval` to `confirmed` with `made_by → STK[]`, `forum → MTG`, `date`; `update options {status: recommended}`. `client_inputs` for final feedback, each with disposition and a `response` pointing to the final version; a request beyond scope is `declined` with a rationale or becomes an `actions` record for a follow-on proposal. `open_questions` closed or `parked` with a client-side owner. `actions`: handover items, implementation owners' first steps, a review date. `evidence` for positions stated on implementation. `risks` owner confirmations. Register final versions with `status: client_approved`; `communications` for the closing email (`client_pm_email`, or `decision_maker_email` if addressed to the sponsor). Then the `gate` decision, `gate_transition` approval (risk `high`), `set_gate AP5 passed`.

## Pitfalls

- A recommendation the decision maker cannot reject. If the memo cannot be answered "no", it is advocacy, not a submission; keep analysis and recommendation separate.
- Tier 0 written last and squeezed. Write the memo's issue and recommendation paragraphs before the full deck is rendered; they test the storyline.
- Tier 2 documents produced from a different outline than the deck. One storyline, one evidence set; the traceability table catches divergence late and expensively.
- Implementation owners named as institutions. Every sequencing entry needs a `stakeholders` id for a unit or person.
- A communication plan without opposition handling. The reaction matrix says who will resist; the plan must say what is said to them and by whom.
- Releasing with pending client inputs. Rule 15 blocks it; disposition first.
- Forgetting profiles at close. Decision 6 says delete unless the Supervisor retains; the event log must show which.

## Checkpoint template

- `done`: recommendation drafted (DEC id); implementation and communication plans (ANA ids, status); deliverables registered and released (DEL ids, versions, tiers, QA status); client inputs dispositioned (count); final presentation held.
- `decided`: recommendation and deliverable approval (DEC ids, status); scope requests declined or deferred (CIN ids).
- `learned`: what changed in the room; implementation risks the client sees that we did not; what to carry into the next engagement.
- `next`: handover actions (ACT ids) and owners; profiles retention decision; export; close.
- `blockers`: approvals pending (APV ids); deliverables with audit failures; unowned risks.

## Proposed schema additions

Adopted in STATE_SCHEMA.md 0.3: `meeting_scheduling` is an action class and `decision_brief` is a deliverable type.

A `deliverables.type` value `decision_brief` for the Tier 0 slide brief, which currently borrows `executive_deck` with `tier: T0`.
