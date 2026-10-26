# Live meetings playbook

Horus joins Zoom and Google Meet calls through the MeetStream bot as a disclosed AI participant. Stakeholder interviews are conducted by the `interviewer` worker with the `horus-meet` tools; gate meetings are co-led (the Supervisor presents, Horus attends, answers when invited and captures). This file is the conduct protocol; the state fields are in STATE_SCHEMA.md E1.

## Before the meeting: the meeting plan

The Principal writes the plan into `meetings.plan` and the plan document (`meetings/<MTG>/plan.md`):

- objectives (two or three), decisions sought (gate meetings), hypotheses to test (`hypotheses_to_test`) and open questions to close;
- `question_guide`: eight to twelve questions with priority 1 to 3, the hypothesis or question each tests, and two follow-up heuristics each; order by priority so a short meeting still covers what matters;
- `follow_up_rules`: a number gets a source question; a claim gets an example; a disagreement with a hypothesis gets probed; a new name gets a role question; a promised document gets logged;
- `sensitivities` and `do_not_say`: topics to avoid, no commitments on the client's behalf, no opinions on the client's decisions, nothing confidential from other interviews;
- `disclosure_script` (below), `consent_terms`, `attribution_rule` (default background), `time_budget_min`, `escalation_rules`;
- `documents_to_present` for co-led meetings.

Then `request_approval` with target the meeting, action class `interview_plan`. The runtime will not join without an approved plan when the level is `approve`.

Disclosure script (English default; adapt names and jurisdictional requirements, see `settings.meetings.disclosure_jurisdiction`):

> Hello, and thank you for joining. I am Horus, an AI participant working with the project team on behalf of <client>. This conversation is being transcribed so that your views are captured accurately. The transcript is confidential and your comments will be attributed only as we agree. Is it all right with you to proceed on that basis?

Chat version (under 500 characters for Google Meet): "Horus AI participant: this conversation is being transcribed for the project team. The transcript is confidential and comments are attributed only as agreed. You may decline, or ask to go off the record, at any time."

## Conducting an interview (the `interviewer` worker)

1. `join(meeting_id, meeting_url, platform)`. Wait for admission; if `not_admitted`, post nothing, record the fallback and stop.
2. Within the first minute `disclose(meeting_id, script, chat_text)`.
3. `listen` for the answer. Affirmative → `consent(meeting_id, granted=true, given_by=<STK id>, attribution_rule)`. Objection → `consent(granted=false)`, thank, offer written questions or a call with a colleague, `leave`. Unclear → ask once more, plainly.
4. Set the agenda in one sentence and the time budget. Ask the first priority 1 question.
5. Loop: `listen(max_wait_s=45)` → read the turn → decide: follow up (rules above), move on, or close a topic. `say` one or two sentences at a time. Acknowledge before redirecting. Never talk over a participant; when `listen` reports they resumed speaking, stop.
6. Mark moments as they happen with `mark`: `consent_given`, `off_record_start` and `off_record_end` when asked to go off record (nothing in that span becomes evidence), `document_promised` ("I can send you the survey"), `document_shared` (a link in chat or a shared screen), `directive` (an instruction from a client participant, verbatim in the note), `decision`, `referral` (a person to speak to).
7. Watch the budget: at three quarters, say so and move to the two or three must-ask questions left; stop on time.
8. Close: summarise what you heard in three sentences, confirm the attribution rule and the documents promised, state next steps, thank, `leave(closing_text)`.

Controls from `listen`: `whisper` → incorporate the instruction in your next question; `pause` → say "Of course, one moment" and wait for `resume`; `takeover` → stop speaking, keep listening and capturing; `leave` → close politely at once.

Latency manners: a turn can take a few seconds to come back. Do not fill silence with filler; one short acknowledgement at most.

## Co-led gate meetings (the Principal)

`join` with `conduct_mode: principal_co_led` using the approved plan. The Supervisor presents the deck. Horus speaks only when invited ("Horus, what does the evidence say about…") and keeps answers to the analysis, never to the client's decision. Mark every decision as it is made; after the meeting write `decisions` (confirmed, with made_by and forum), `client_inputs`, `open_questions` and `actions`, and draft the minutes email for approval.

## Capturing documents and directives given in a call

- A link posted in chat: `mark(document_shared, note=<link>)`; after the call, fetch it (WebFetch or the Drive connector), `import_document` with `origin: client|stakeholder` and `received_via: <MTG>`, and link it to the meeting.
- A document shown on screen or promised: `mark(document_promised)`; after the call create an `actions` record `client_request_document` owned by the participant with a due date, and mention it in the follow-up email.
- An instruction or directive from a client participant ("Do not model option C", "The minister wants this before the budget"): `mark(directive, note=<verbatim>)`; after the call create a `client_inputs` record of kind `directive` or `instruction` with `content_verbatim`, `from` the stakeholder, `via` the meeting, and a `decisions` record of kind `political_directive` when it binds the analysis, status `proposed` until the Principal confirms it with the PM.

## After the meeting (write-back)

1. The runtime has written `bot`, `disclosure`, `consent`, `live` and `transcript` blocks and set `held_at`.
2. Read the transcript (`transcript` tool or the JSONL file). Create `evidence` records for positions and quotes (kind `position` or `quote`, `attribution` per the rule, `meeting` set, `transcript_turns`), each citing a `sources` record of type `interview` for this meeting.
3. Fill `interview_record`: topics and positions, reactions to options, contradictions with hypotheses, documents promised and shared, directives received, referrals, follow-ups, and `proposed_updates` (stakeholder stance, concerns, red lines, predicted reactions; hypothesis status changes). Set the meeting `status` to `held`.
4. Create `open_questions` and `actions` that arose.
5. Write the debrief memo (`meetings/<MTG>/debrief.md`) and set `debrief.path`.
6. The Principal confirms `proposed_updates` (writes them to the stakeholder and hypotheses, sets `confirmed_at`), regenerates the reaction matrix view before the next gate meeting, and drafts the thank-you and follow-up email for approval (`stakeholder_email`).

## Failure handling

Not admitted within the grace period → `actions` follow-up to the PM, Supervisor notified. Participant objects to the AI or to transcription → stop, offer alternatives, leave, record. Audio or provider failure → `chat` an apology and leave; draft a reschedule email. No-show → record, propose a reschedule. Every failure is an event and an action; none is silent.
