# Phase 3: Design

Define the option space and the rules of the game: a long list by the pathway's option logic, a screened shortlist, candidate guiding principles, political-directive questions and a predicted reaction matrix, validated in a workshop. Phase 3 ends at AP3.

**When Horus uses this:** `engagement.phase` is `P3` and gate `AP3` is not `passed`.

## Purpose and exit criteria

Agree with the decision makers what a good answer must satisfy before any answer is appraised, so that P4 compares options against criteria the client owns. Gate AP3 (STATE_SCHEMA.md section 7) reports `ready` when: at least two `options` plus a `do_nothing` option are at `short_list` with an `options_screening` analysis; candidate guiding principles exist as `decisions` of kind `guiding_principle` at `proposed`; the `stakeholder_reaction_matrix` covers every priority-1 stakeholder and every shortlisted option; the principles deck is released; and, after the workshop, `guiding_principle`, `political_directive` and `criteria_weights` decisions are `confirmed`. Exit is the AP3 `gate` decision, the `gate_transition` approval, `set_gate AP3 passed`, `set_phase P4`.

## Entry checks

`gates.AP2.status: passed`; the pack's diagnostic analyses and the `baseline` at `reviewed`; `decision_maker_lens` and `internal_politics` at `reviewed`; no `hypotheses` at `untested`; interview evidence of `kind: position` exists for most priority-1 stakeholders (`view evidence_table` filtered by kind); `political_directive` decisions proposed in P2 listed; `settings.research_budget.per_phase.P3` (default four runs) available.

## Step by step

1. **Load the option logic.** Read `Option logic` and `Frameworks` in the pack. Decide the option `kind` the pathway produces and the two axes of the option landscape (for example intensity of intervention against breadth of coverage).
2. **Build the long list.** `create` one `options` record per distinct choice: `code` (A, B, C), `title`, `summary`, `kind` (per pathway), `addresses_objectives` (OBJ ids), `instrument_types` for regulatory kinds, `mechanism {inputs, activities, outputs, outcomes, impacts, key_assumptions → ASM}`, `design_parameters[] {lever, setting, alternatives}`, `target_groups`, `origin` (`horus`, `client`, `stakeholder`, `literature`), `status: long_list`. Always one `kind: do_nothing` option describing business as usual. Eight to twelve long-list options is typical; options proposed by stakeholders in interviews are included with `origin: stakeholder` so they are visibly considered.
3. **Map precedents.** Delegate up to four `researcher` runs by option cluster: the option mechanisms, the question (where has this been tried, with what design, outcome and evaluation), outputs `sources`, `evidence` and a memo, credibility floor B. `update options.precedents[] {jurisdiction, programme, period, outcome, evidence → EVD}`. Precedents without evaluation evidence are marked as such.
4. **Screen to a shortlist.** `create` `analyses` `kind: options_screening` with `content {criteria[] {criterion, weight, source → DEC}, scores[] {option, criterion, score, rationale}, shortlist → OPT[]}`. Criteria come from the brief's objectives and constraints, confirmed directives and feasibility thresholds; weights are provisional until AP3. `update options` to `screened_out` or `short_list` with `screening {criteria, result, rationale, analysis → ANA}`. Keep do-nothing on the shortlist as the comparator. `create` `decisions` `kind: shortlist`, `status: proposed`.
5. **Add variants and packages.** Where a shortlisted option has a design fork that matters politically (phasing, thresholds, voluntary before mandatory), `create` variant `options` (`code: B1`, `B2`, listed in the parent's `variants`) or a `kind: package` with `package_members`.
6. **Draft the guiding principles.** From the brief, the decision-maker lens and the diagnosis, `create` five to seven `decisions` `kind: guiding_principle`, `status: proposed`, `proposed_by: horus`, each a full sentence a minister could say, with `rationale` and `alternatives_considered`. Pre-score every shortlisted option: `update options.principles_alignment[] {principle → DEC, score -2 to +2, rationale}`. A principle every option satisfies equally is decoration; drop it.
7. **Frame the directive questions.** For each political fork the client must settle (fiscal envelope, legislative route, timing against the political calendar, who leads delivery, whom to exempt), `create` an `open_questions` record `kind: political`, `owner → STK (sponsor)`, `priority: P1`, `blocking: AP3`, paired with a `decisions` record `kind: political_directive`, `status: proposed`, worded as the directive would read if confirmed. Carry forward the directives proposed in P2.
8. **Propose criteria weights.** `create` `decisions` `kind: criteria_weights`, `status: proposed`, naming the appraisal dimensions (the impact dimension enumeration in STATE_SCHEMA.md section 4) and the weights the pack's `Appraisal method` expects; `rationale` ties each weight to a principle.
9. **Build the reaction matrix.** `create` `analyses` `kind: stakeholder_reaction_matrix` with `rows → STK` (priority 1 and 2), `columns → OPT` (shortlist and variants) and `DEC` (principles), `cells[] {stakeholder, target, reaction, rationale, confidence, basis → EVD}`, `coalition_notes`. Populate from interview evidence (`search` across evidence and transcripts for each option's terms); `update stakeholders.predicted_reactions` to match and `update options.reactions → ANA`. Check `view reaction_matrix` for empty cells on priority-1 rows and fill them with a targeted interview (the Phase 2 loop) or a `researcher` run on public positions. `update internal_politics.positions_by_option`.
10. **Design the workshop.** `create` `meetings` `kind: workshop`, `conduct_mode: principal_co_led`, `participants` (sponsor, steering, PM, Supervisor, Horus), `purpose`, `objectives`, `decisions_sought[]` listing each principle, each directive question, the shortlist and the weights, `agenda` with minutes per block, `hypotheses_to_test` (the political ones), `open_questions_to_close` (the directive questions), `plan {disclosure_script_id, consent_terms, attribution_rule}`.
11. **Produce the deck and hold the workshop.** `create` `deliverables` `type: principles_deck`, `tier: T1`, `for_meeting → MTG`; ghost deck; `producer` render and QA; fresh `producer` review; `request_approval` action class `tier0_tier1_release`, risk `medium`; `release_version`; pre-read under `client_pm_email`. Hold the workshop per `alignment-point-protocol.md`, capture, gate, `checkpoint`.

## Pathway hooks

`Option logic` in `horus-policy/references/pathways/<id>.md` sets the option kind and the generator: `regulatory` uses the instrument typology (`instrument_types`) and the OECD alternatives to regulation, with variants by stringency and phasing; `strategy` frames strategic choices (ambition, focus, delivery model, sequencing) as mutually exclusive bundles; `institutional_operating_model` uses operating-model archetypes and transition paths; `transformation_delivery` generates delivery interventions against the bottlenecks in the delivery chain; `public_investment_business_case` spans do-minimum to full scope with delivery and procurement models; `programme_service_design` generates service concepts by channel, eligibility and behavioural lever. `Appraisal method` tells you which dimensions the criteria weights must cover, so the weights confirmed at AP3 match the P4 method.

## Client-facing artefact

Option space and guiding principles deck, Tier 1, `DRAFT FOR DISCUSSION`. Section order: (1) executive summary: the choice in front of the client and what today must settle; (2) diagnosis recap in one slide; (3) option landscape: the long list on two axes; (4) screening funnel: criteria, what fell away and why; (5) the shortlist, one slide per option: mechanism, who is affected, precedents, open design parameters; (6) candidate guiding principles, each tested against the shortlist (which options it rules in or out); (7) directive questions, each framed as a choice with consequences, never as a recommendation; (8) proposed appraisal criteria and weights, with the ranking sensitivity to them; (9) predicted reactions as a coalition view, individual positions only where `on_record`; (10) decisions sought; (11) next steps and the appraisal plan. Variants and packages get a slide only if they change the decision.

## Capture after the alignment point

`decisions`: `update` each `guiding_principle`, `political_directive`, `shortlist` and `criteria_weights` to `confirmed` with `made_by → STK[]`, `forum → MTG`, `date`, `rationale`, `implications[] {area, change}`, `affects → OPT`; principles reworded in the room get a new record with `supersedes`; principles the client added arrive first as `client_inputs` `kind: guiding_principle_input` and then as decisions. `options`: `update` status for anything added, merged (`merged`) or removed (`rejected`) with the reason in `screening.rationale`; variants requested become new records. `assumptions` the room settled (a fiscal envelope, a start date) are `created` with `basis: client`, `status: agreed`, `agreed_in → DEC`. `client_inputs` for every comment with disposition; `open_questions` closed with `answered_by → DEC`; `actions` for follow-ups; `evidence` for stated positions. Regenerate the reaction matrix as a new version against the confirmed principles. Then the `gate` decision, `gate_transition` approval (risk `high`), `set_gate AP3 passed`, `set_phase P4`, minutes email.

## Pitfalls

- Shortlisting by Horus's preference and backfilling the criteria. Write the criteria first and show the screening scores; the client will check.
- Dropping do-nothing from the shortlist. Every appraisal method compares against it, and the decision memo must offer it.
- Principles written as objectives ("increase formalisation"). A principle constrains how, not what.
- Directive questions asked as yes or no. Frame the fork with the consequence of each branch so the answer is a decision, not a mood.
- A reaction matrix filled from intuition. Each cell needs `basis → EVD` or a `confidence: low` flag, and empty priority-1 cells are gate failures.
- Letting a workshop confirm weights without arithmetic. Show the ranking sensitivity to the proposed weights before asking for them.
- Showing a stakeholder's predicted reaction by name where the attribution rule was `background` or `not_for_attribution`.

## Checkpoint template

- `done`: long list of N options (OPT ids), shortlist of M plus do-nothing; screening (ANA id); principles proposed (DEC ids); directive questions (OQ and DEC ids); reaction matrix (ANA id, coverage); deck (DEL id, version); workshop held.
- `decided`: principles, directives, shortlist and weights confirmed (DEC ids); options added or removed.
- `learned`: which principle was contested and why; the directive the sponsor would not give; coalition risks.
- `next`: appraisal design and assumptions register; analyst briefs per option; AP3 gate approval (APV id).
- `blockers`: directives still unanswered (OQ ids); reaction-matrix gaps on priority-1 rows.
