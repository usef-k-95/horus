# Phase 2: Diagnose

Establish the facts, the baseline and the politics: research fan-out, live stakeholder interviews conducted by Horus, the pathway diagnostic, and a readout that gets the findings accepted and previews the solution space. Phase 2 ends at AP2.

**When Horus uses this:** `engagement.phase` is `P2` and gate `AP2` is not `passed`; and for any interview in a later phase, which reuses the loop below.

## Purpose and exit criteria

Replace hypotheses with evidence and give the client a diagnosis they accept before any option is designed. Gate AP2 (STATE_SCHEMA.md section 7) reports `ready` when: every research question is `done` or `dropped` with a reason; the pack's diagnostic `analyses` kinds exist at `reviewed`; at least 70 per cent of priority-1 interviews are `held` with `consent` recorded and `transcript.verified_at` set (threshold configurable); `decision_maker_lens` and `internal_politics` analyses exist; no `hypotheses` record is `untested`; every held interview has its `proposed_updates` confirmed; the diagnostic deck is released; and no P1 `open_questions` record is `open`. Exit is the AP2 `gate` decision from the readout, the `gate_transition` approval, `set_gate AP2 passed`, `set_phase P3`.

## Entry checks

`gates.AP1.status: passed`; `approach` and `workplan` at `approved` with RQs at `planned`; every priority-1 stakeholder has a `client_request_meeting` action at `requested`; `settings.meetings` complete, with the disclosure script for its jurisdiction in `references/live-meetings.md`; the `interview_plan`, `meeting_scheduling` and `stakeholder_email` levels read from `engagement.settings.autonomy`; the P2 research budget (default twelve runs) unspent.

## Step by step

1. **Fan out the research.** For each RQ, set `approach.analytical_plan.research_questions[].status: running` and delegate one `researcher`: the question, the hypotheses it tests (HYP ids), outputs (`sources`, `evidence`, a `research_memo` analysis), credibility floor B, 40 fetches. Four to eight at once. On return, read the memo, `update hypotheses {status, confidence, evidence_for, evidence_against}`, send contradicted figures for a second-source pass, and set the RQ to `done` (`memo → ANA`) or `dropped` with the reason.
2. **Commission the standing analyses and the diagnostic.** One `researcher` each for `public_sentiment` (themes, polls, tone) and `benchmark` (three to five comparators), returned at `draft` and reviewed by the Principal. Then `create` the `analyses` kinds the pack prescribes (see Pathway hooks), each with `inputs`, `method_notes`, `content`, `findings[] {statement, evidence, confidence}`, `limitations`, plus always a `kind: baseline` analysis describing the counterfactual P4 will appraise against; delegate modelled series to an `analyst`.
3. **Interview loop: scheduling.** When the PM's introduction arrives, `create` an outbound `communications` to the stakeholder proposing two or three slots and stating Horus's disclosed AI participation; `request_approval`, action class `meeting_scheduling`, risk `low` (decision 17); send. Read the reply and parse the invite (`horus-mail` for attachments); `update meetings {status: scheduled, scheduled_at, join_url, platform, requested_via → COM}` and `stakeholders.engagement {status: scheduled, meetings → MTG}`. Horus creates no calendar events. On Google Meet confirm who admits Horus; Zoom works only when the client hosts (decision 12). `create` the interview `sources` record (`type: interview`, `tier: A`, `independence_group: <STK id>`) so the interviewer can cite it.
4. **Interview loop: the meeting plan.** `view meeting_plan` assembles the inputs. Write `meetings/<MTG>/plan.md` and `update meetings.plan {path, version, question_guide[] {id, question, priority 1 to 3, purpose, tests → HYP or OQ, follow_up_heuristics}, follow_up_rules, sensitivities, do_not_say, disclosure_script_id, consent_terms, attribution_rule, escalation_rules}`, with `time_budget_min`, `hypotheses_to_test`, `open_questions_to_close`, `participants[].speaker_label`. Twelve to eighteen questions for 45 minutes, priority 1 first.
5. **Interview loop: approval.** `request_approval` with target `{collection: meetings, id, version: plan.version}`, action class `interview_plan`, risk `medium`. Wait for `approved` (`not_required` in shadow); `update meetings.plan.approval → APV`. A later change to the guide needs a new version and a new request (rule 25); the approval expires at the meeting's end.
6. **Interview loop: join, disclose, consent.** At the scheduled time spawn the `interviewer` with the meeting id, participants and profile summaries, and the `plan` block as its brief. It calls `join` (URL, AI-identifying display name, disclosure script id, grace period); the runtime checks rule 21 and writes `bot`. Within the first minute it calls `disclose`, which speaks the script and posts it with `chat`, then `consent`, which records `{ai_participant, recording, transcript, attribution_rule, given_by, given_at}` and lets the meeting move to `in_progress` (rule 22), then `mark consent_given`. If the participant objects: recording off, offer written questions or a human-led call, `leave` politely, `status: aborted`, a follow-up `actions` record. Never argue.
7. **Interview loop: the guide and follow-ups.** The interviewer loops `listen` then `say` (interruptible), working the guide in priority order and tracking coverage. Heuristics: a number gets a source question; a claim an example; a disagreement with a hypothesis a probe; a new name a role question; a document mentioned `mark document_promised`; a request to go off record `mark off_record_start` and `off_record_end`. Whispers, pause, takeover and leave arrive in `listen` and are obeyed at once, each logged with `record_intervention` (rule 27). At three quarters of the budget it warns and wraps: summarise what was heard, confirm attribution and promised documents, state next steps, thank, `leave`. The runtime archives the transcript and writes `consent`, `live` and `transcript`.
8. **Interview loop: capture.** The interviewer reads `transcript` and writes `evidence` per atomic claim (`kind`, `sources → SRC (interview)`, `attribution`, `about → STK`, `supports` or `contradicts → HYP`; nothing off record, rule 23); `meetings.interview_record {topics, reaction_to_options, contradictions, documents_promised → ACT, referrals → STK, follow_ups → ACT, proposed_updates {stakeholder_patch, hypothesis_patches}}`; `open_questions` it could not close; `actions` for each document or introduction promised (`requested_via → MTG`); `meetings/<MTG>/debrief.md` and `meetings.debrief {path, by, what_worked, what_to_change}`. Directives voiced by a client participant go in the debrief; the interviewer writes no `client_inputs` or `decisions`.
9. **Interview loop: integration.** After the `SubagentStop` hook surfaces the debrief, `view interview_debrief`; confirm or amend the proposed updates: `update stakeholders {stance, stance_confidence, stance_basis, concerns, red_lines, predicted_reactions, relationships, engagement.status: engaged, last_reviewed}` and `update hypotheses` with `revision_history`. `create` `client_inputs` (`kind: directive`, `via → MTG`) for client directives and a `proposed` `decisions` `kind: political_directive` for AP3. Verify the transcript and `update meetings.transcript {verified_by, verified_at}` within two days (rule 24); audio then deletes per settings. When a promised document arrives, `import_document` it and set `actions.fulfilled_by → DOC`. Set `meetings.outcomes`.
10. **Interview loop: follow-up email.** `create` outbound `communications` to the stakeholder (`classification: stakeholder`): thanks, what was heard with the attribution rule restated, the documents offered, next steps. Tier 3 content only. `request_approval`, action class `stakeholder_email`, risk `low`; send; `update meetings.follow_up_sent → COM`.
11. **Politics analyses.** Complete `decision_maker_lens` to `reviewed`; `create` `internal_politics {entity → STK, units, positions_by_option (filled in P3), influence_paths, watch_points}`. Neither appears in the deck.
12. **Revisit the classification.** If a `revisit_triggers` entry fires, `create` a new `problem_classification` version and a `decisions` `kind: pathway` with `supersedes`, `append` to `engagement.pathway.revisions`, and raise it at the readout.
13. **Readout.** `create` `meetings` `kind: readout`, `conduct_mode: principal_co_led`, `decisions_sought` (findings accepted; solution space preview accepted; pathway confirmed or revised). `create` `deliverables` `type: diagnostic_deck`, `tier: T1`; ghost deck; `producer` render and QA; fresh `producer` review; `request_approval` `tier0_tier1_release`, risk `medium`; `release_version`; pre-read under `client_pm_email`.

## Pathway hooks

`Diagnostic lens` in `horus-policy/references/pathways/<id>.md` names the analysis kinds the gate checks: `regulatory` needs `baseline` and `diagnostic`; `strategy` needs `strategic_position` and `scenario_analysis`; `institutional_operating_model` needs `institutional_diagnostic`; `transformation_delivery` needs `delivery_chain`; `public_investment_business_case` needs `strategic_case` and `baseline`; `programme_service_design` needs `user_and_service_research`. `Stakeholder emphasis` sets interview priorities and question themes; `Benchmark documents` names the comparators to fetch first.

## Client-facing artefact

Diagnostic readout deck, Tier 1, `DRAFT FOR DISCUSSION`. Section order: (1) executive summary: the diagnosis in three sentences and what it implies; (2) mandate and hypotheses recap; (3) baseline and trends, sourced; (4) diagnostic findings by issue-tree branch, one message per slide; (5) benchmark table and lessons; (6) stakeholder landscape and what we heard, attributed per consent, positions never shown as facts; (7) public sentiment snapshot with caveats; (8) hypotheses supported, refuted and revised; (9) solution space preview, explicitly not yet options; (10) open questions and data still needed; (11) decisions sought; (12) next steps. Annex from `view evidence_table`.

## Capture after the alignment point

`decisions`: `gate` AP2; `pathway` reconfirmation or supersession; `process` decisions on P3 scope. `client_inputs`: feedback on findings (`about → DEL version, section`) with disposition; directives on options that are off the table become `political_directive` proposals for AP3. `open_questions`: challenges to the baseline, with owner and due date. `actions`: data promised, extra interviews. `evidence`: steering members' positions (`kind: position`, attribution per the meeting rule). `update stakeholders` for everyone in the room. Then the `gate_transition` approval (risk `high`), `set_gate AP2 passed`, `set_phase P3`, minutes email.

## Pitfalls

- Improvising outside the approved guide because the conversation is going well. A new question is a new plan version.
- Treating what a stakeholder asserts as a fact. It is Tier A for their position and Tier C for the world until corroborated.
- The decision-maker lens or internal-politics map on a slide. Their implications shape framing; the analyses never leave state.
- RQs closed as `done` on a single source; the two-source rule bites at traceability QA, when fixes are expensive.
- A solution-space slide that reads as a recommendation. The client will anchor on it at AP3.

## Checkpoint template

- `done`: RQs done and dropped (counts, ANA ids); priority-1 interviews held (N of M, MTG ids), transcripts verified; diagnostic analyses at `reviewed` (ANA ids); lens and internal politics (ANA ids); diagnostic deck (DEL id, version); readout held.
- `decided`: AP2 gate (DEC id); pathway confirmed or revised; directives captured as proposed decisions (DEC ids).
- `learned`: hypotheses refuted and why; the findings the client resisted; stakeholders whose stance moved.
- `next`: plans pending approval (APV ids); interviews scheduled (MTG ids, dates); P3 long-list start.
- `blockers`: stakeholders not yet introduced or scheduled; unverified transcripts; P1 questions still open.

## Proposed schema additions

Adopted in STATE_SCHEMA.md 0.3: `meeting_scheduling` is an action class and `decision_brief` is a deliverable type.

`meeting_scheduling` as an action class in STATE_SCHEMA.md section 4 (decision 17 in docs/DECISIONS.md).
