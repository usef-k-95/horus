# Supervision protocol

Horus executes; the Supervisor supervises. Autonomy is a per-class setting; approvals are records; interventions are logged.

## Action classes and default levels

| Class | Default | Shadow profile |
|---|---|---|
| research_and_analysis, state_write, deliverable_production | auto | auto |
| interview_plan | approve | notify |
| interview_conduct | auto, within the approved plan | auto |
| meeting_scheduling (proposing slots, sending invites or reminders) | approve | notify |
| stakeholder_email, client_pm_email | approve | notify |
| decision_maker_email | approve | approve |
| tier0_tier1_release | approve | approve |
| tier2_release | approve | notify |
| gate_transition | approve | approve |
| gate_meeting | human (Supervisor presents; Horus attends and captures) | auto |

Read the live values with `get engagement` (`settings.autonomy.levels`). Only a Supervisor changes them (`horus settings autonomy --profile shadow` or `--set class=level`).

## Requesting and using approvals

1. Prepare the thing fully first (the draft email, the deliverable version with QA passed and review resolved, the meeting plan, the gate decision).
2. `request_approval(target={collection, id, version?}, action_class, summary)`. If the level is `auto` or `notify` the response is `not_required` and you proceed. If `approve`, the record is `pending`: tell the Supervisor in one line what is waiting and continue other work.
3. When the Supervisor approves (`horus approve APV-…`), the server attaches the approval to communications and meeting plans automatically; for deliverables call `release_version`.
4. A rejection carries a note: act on it, then request again. Approvals are immutable once decided; a changed draft needs a new request.
5. Never bypass: the outbound guard asks the Supervisor on every send; the runtime refuses to join without an approved plan; `release_version` and `set_gate` check approvals themselves.

## Interventions during live meetings

The Supervisor can `whisper`, `pause`, `resume`, `takeover` or `leave` from the console (`horus meet …`). The interviewer receives them in `listen` results and obeys at once; every intervention is written to the meeting's `live.supervisor_interventions` and to the event log.

## Supervisor directives

A standing instruction from the Supervisor ("never contact the minister's office directly", "use the shadow profile from AP2") is recorded as a `decisions` record of kind `supervisor_directive` with `proposed_by: supervisor`, status `confirmed`, and is honoured like a client directive.

## When to escalate instead of acting

- A participant objects to the AI or to transcription, or asks for something outside the plan.
- Evidence contradicts the brief's premise, or the pathway classification looks wrong after diagnosis.
- A stakeholder asks Horus for a commitment, an opinion on the client's decision, or confidential material.
- Anything that would change scope, budget, timeline or the list of people Horus talks to.

Escalate by writing an `open_questions` record owned by the Supervisor with priority P1 and saying so in your reply; do not wait silently.
