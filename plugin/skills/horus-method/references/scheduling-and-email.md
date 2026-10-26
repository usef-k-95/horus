# Scheduling, email and documents

## Identifying the meetings the engagement needs

- Every stakeholder at engagement priority 1 gets an interview; priority 2 a shorter call or written questions; priority 3 a consultation summary.
- Every gate gets its meeting (kickoff, diagnostic readout, principles workshop, appraisal readout, final presentation) and the PM gets a weekly check-in.
- For each, create a `meetings` record (`status: proposed`, participants, purpose, objectives) and an `actions` record of kind `client_request_meeting` owned by the client PM when the PM arranges access, or `stakeholder_outreach` when Horus writes directly.

## Scheduling protocol

1. **Propose.** Draft the scheduling email (see `horus-deliverables/references/formats-and-templates.md`): purpose in two lines, three proposed slots in the stakeholder's time zone, duration, that the call is on Google Meet or Zoom with an AI participant from Horus, and the disclosure in one sentence. Write the slots into `meetings.scheduling.proposed_slots`. Create the outbound `communications` record (`classification: scheduling`, `action_class: meeting_scheduling`) and `request_approval`.
2. **Send** after approval through the Gmail connector (`send_message` or `reply`); set the communication to `sent` and `scheduling.status: awaiting_reply`.
3. **Read replies.** At every inbox triage, search the thread. A reply that picks a slot → `scheduling.selected_slot`, `scheduled_at`, `scheduling.status: confirmed`; an invite with a Meet or Zoom link → `join_url`, `platform`; a counter-proposal → repeat step 1.
4. **Invites and attachments.** Calendar invites arrive as `.ics` attachments. Download with `horus-mail fetch <gmail-message-id> --out inbox/` and parse with `horus-mail parse-ics <file>`; the result gives start, end, location and the meeting link. Import the invite as a `documents` record (`kind: calendar_invite`) linked to the meeting.
5. **Remind.** The day before, draft a short reminder with the disclosure sentence (approval class `meeting_scheduling`).
6. **Join** at the time with the `interviewer` worker (`/horus:horus-method interview MTG-…`).

MeetStream can also auto-join meetings on a connected Google Calendar (the Supervisor connects it once with OAuth credentials in the MeetStream dashboard); Horus cannot create calendar events or Meet links itself, so the client or the stakeholder issues the invite.

## Email: inbound

Read with the Gmail connector: `search_threads` with a Gmail query (client domain, subject keywords, `newer_than:7d`), `get_thread` or `get_message` with `PLAIN_TEXT`. For every relevant message create a `communications` record (`direction: inbound`, `external_ref` the Gmail message id, `classification`, `summary`) and set `status: triaged`. Extract into records: instructions and feedback → `client_inputs` (verbatim where it matters); requests → `actions`; questions → `open_questions`; meeting links or slots → `meetings`; facts worth keeping → `evidence` with a `sources` record of type `client_document`.

Attachments: the connector lists attachment names and ids but does not return their content. Download them with `horus-mail fetch <gmail-message-id> --out inbox/`, then `import_document` each file (`origin: client`, `received_via: <COM id>`), read it (PDF, Word and Excel skills) and record what matters as evidence and client inputs. Set the communication to `processed`.

## Email: outbound

Draft the message in the house style (`formats-and-templates.md`), create the `communications` record (`direction: outbound`, `status: draft`, `action_class` by recipient: `client_pm_email`, `decision_maker_email`, `stakeholder_email`, `meeting_scheduling`), save the body to `inbox/outbound/<COM>.md` as `body_path`, `request_approval`. After approval send with the Gmail connector (attachments as base64 from the deliverable files, or `horus-mail send --attach` when a file is large) and set `status: sent`. Link the communication to the meeting or deliverable it concerns.

## Documents received in any channel

Every file Horus receives, by email, by chat link in a call, or by Drive share, becomes an immutable copy under `inbox/` and a `documents` record with `received_via`. Processing status moves `received → extracted → summarised → mined` as you read it; key points become evidence. Client documents are `client-confidential` unless the client says otherwise.
