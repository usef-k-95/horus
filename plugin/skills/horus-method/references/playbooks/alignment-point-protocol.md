# Alignment-point protocol

Every client or stakeholder touchpoint runs the same four steps: prepare, conduct, capture, communicate. The records are the same each time; what differs is who speaks and what the room is for.

**When Horus uses this:** before and after every `meetings` record of any kind; the phase playbooks point here for their alignment point.

## The common frame

Prepare: a `meetings` record with `purpose`, `objectives`, `decisions_sought`, `hypotheses_to_test`, `open_questions_to_close`, `participants` with `speaker_label`, `agenda`, `prep_pack → DEL[]` for client meetings, a `plan` block (`disclosure_script_id`, `consent_terms`, `attribution_rule`) whenever Horus is in the room, and the approvals the autonomy policy requires. Conduct: Horus is a disclosed participant through `horus-meet` and never speaks outside its plan. Capture, the same day: `decisions` where a forum decided, `client_inputs` for what the client said that should change our work, `open_questions`, `actions`, `evidence` with attribution, stakeholder and hypothesis updates, and `meetings.outcomes` pointing at all of them. Communicate: one outbound `communications` record, approved under its action class, sent, linked through `meetings.follow_up_sent`. A Supervisor instruction given outside a meeting is logged with `record_intervention` and, if standing, as a `decisions` record of kind `supervisor_directive`. A skipped step means the meeting did not happen as far as state is concerned.

## Case A: a stakeholder interview conducted by Horus

**Prepare.** `view meeting_plan` for the MTG. Write `meetings.plan`: objectives; twelve to eighteen questions with `priority`, `purpose`, `tests → HYP or OQ` and `follow_up_heuristics`; `follow_up_rules`; `sensitivities`; `do_not_say` (no commitments, no opinions on the client's choices, nothing from other interviews); the disclosure script for `settings.meetings.disclosure_jurisdiction`; `consent_terms`; `attribution_rule`; `escalation_rules` (objection, requests outside the plan, distress). `create` the interview `sources` record. `request_approval`, action class `interview_plan`, risk `medium`; `update meetings.plan.approval`. Brief the `interviewer` with the plan only: profile summaries, never profiles.

**Conduct.** The interviewer calls `join`, then `disclose` within the first minute (spoken, and posted with `chat`), then `consent` and `mark consent_given`. It states the agenda and time budget aloud, then loops `listen` and `say`: priority-1 questions first, follow-ups by the heuristics, `mark document_promised`, `mark off_record_start` and `off_record_end` as needed, `status` to watch the budget. Whispers and controls arrive in `listen` and are obeyed at once; a takeover puts it in listen-only mode. It warns at three quarters of the budget, closes with a summary, the attribution confirmation, promised documents and next steps, and calls `leave`. The Supervisor watches from the console.

**Capture.** The interviewer writes `evidence` (one claim per record, `sources → SRC (interview)`, `attribution`, `about`, `supports` or `contradicts`, verbatim quotes, nothing off record), `interview_record`, `open_questions`, `actions` for promised documents and referrals, and the debrief. The Principal runs `view interview_debrief`, confirms `proposed_updates` into `stakeholders` and `hypotheses`, raises `client_inputs` for any client directive voiced, verifies the transcript (`verified_by`, `verified_at`), refreshes the reaction matrix if a stance moved, and sets `meetings.outcomes`.

**Communicate.** A thank-you email: thanks, what we heard in four or five lines, the attribution rule as agreed, the documents offered with a date, what happens next. Tier 3 content only. `request_approval`, action class `stakeholder_email`, risk `low`; send; `update meetings.follow_up_sent`.

## Case B: a co-led gate meeting

**Prepare.** The deck is the prep pack: ghost deck by the Principal, render and QA by `producer`, fresh-instance review, `tier0_tier1_release` approval, `release_version`, pre-read under `client_pm_email`. On the `meetings` record: `conduct_mode: principal_co_led`; `decisions_sought` as full sentences the room can accept or reject, each pre-linked to a `proposed` `decisions` record; `agenda` with minutes and a `lead` per item (the Supervisor presents; Horus takes the questions block if invited); `hypotheses_to_test`; the `plan` block. Pull `view decision_log`, `view question_register` and `view reaction_matrix` into the Supervisor's speaker notes; agree beforehand what Horus answers (analysis, evidence) and defers (commitments, scope, fees).

**Conduct.** The Principal joins through `horus-meet`: `join`, `disclose`, `consent` for recording and transcript from the PM or sponsor, `mark consent_given`. The Supervisor presents. Horus listens, answers questions on the analysis when invited (`say`: short, sourced, with ranges), calls `mark decision` with a note each time the room settles a decision sought, `mark document_promised` for client documents, and the off-record marks if asked. If the Supervisor takes over a question, Horus stops. The Supervisor closes; Horus summarises only if asked, and calls `leave` after the client has left.

**Capture.** From `transcript` and the marks: `update` each decision sought to `confirmed` with `made_by`, `forum`, `date`, `rationale`; a reworded decision gets a new record with `supersedes`; `client_inputs` for every comment on the deck with `about {target → DEL version, section}` and a disposition; `open_questions` with owners and `blocking`; `actions` for documents, introductions and re-runs; `evidence` of `kind: position` for what senior participants said, attribution per the plan; `update stakeholders` for everyone in the room with `last_reviewed` today. Then the `gate` decision, the `gate_transition` approval and `set_gate`.

**Communicate.** Minutes to the PM within 24 hours: decisions taken verbatim, decisions still needed, actions by owner and date, open questions, next meeting. `client_pm_email`, risk `medium`; copying decision makers makes it `decision_maker_email`, risk `high`.

## Case C: a PM check-in

**Prepare.** `meetings` `kind: pm_checkin`; `conduct_mode: principal_co_led` when the Supervisor attends, `human` when Horus prepares and captures from notes. Pull `view status_note`, `view action_tracker`, `view question_register` and `view approvals_queue` for items waiting on the client. Six agenda items: progress against the workplan; decisions needed; questions by owner; requests outstanding (data, documents, introductions, who admits Horus to upcoming interviews); risks; next week. No deck.

**Conduct.** Horus joins as a disclosed participant, confirms consent for the transcript, and takes the status items when invited: what was done, what is blocked and by whom, what we need by when. It `mark`s each PM commitment (`decision` or `document_promised`). Scheduling, scope and fees belong to the Supervisor.

**Capture.** `client_inputs` for requests, instructions, preferences and documents promised; `actions` created, or set to `done` with `fulfilled_by`; `open_questions` answered with `answered_by → CIN`; workplan changes the PM agreed as `append` to `workplan.change_log {date, change, reason, approved_in → CIN}`; `decisions` `kind: process` where the PM settled a process matter within scope; `meetings.outcomes`.

**Communicate.** The weekly status note doubles as the minutes: `view status_note`, edit, `create` `communications`, approval under `client_pm_email`, send, link in `meetings.follow_up_sent`.
