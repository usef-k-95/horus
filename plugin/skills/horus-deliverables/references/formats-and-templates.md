# Formats and templates

Fill-in templates for the interview plan, the pre-read, minutes, thank-you and follow-up, and weekly status emails, and the data-request list, with the tone rules for writing to ministers, project managers and stakeholders. Placeholders are in angle brackets.

When Horus uses this: at steps 1 and 4 of the alignment-point protocol (prepare, communicate), at the weekly PM cadence, and whenever a request for data or documents leaves the engagement.

## Tone rules

| Audience | Rules |
|---|---|
| Ministers and decision makers (action class `decision_maker_email`, default `approve`) | Decision first, in the first sentence. Body at most 150 words; the memo carries the rest. Formal address with the exact title from `stakeholders.title`. No methodology, no jargon, no exclamation marks, no attachments beyond the memo and the brief. Never sent without the approval record; never a WORKING DRAFT. |
| Client project manager (`client_pm_email`, default `approve`) | Collaborative and precise. One subject per email; asks numbered, each with an owner and a date. Dates as dates ("by Thursday 12 November"), never "soon" or "urgent". Confirm what was received and say what changes as a result. Short paragraphs; attachments named. |
| Stakeholders (`stakeholder_email`, default `approve`) | Courteous, neutral, grateful. Horus identifies itself as an AI participant acting for Horus whenever the exchange concerns a meeting it conducts. No client-confidential content, no other stakeholder's views, no commitment on the client's behalf, no opinion on options. Restate the attribution rule agreed. |
| All | Subject line in three parts separated by vertical bars, as in the templates below: engagement short name, purpose, date or meeting. Sentence case. One ask per email where possible. Signed "Horus, for <engagement name>" with the Supervisor named as the accountable contact. Every outbound email becomes a `communications` record with its `classification` and, where the autonomy level requires, an `approval`. |

## Interview plan

```
# Meeting plan: <MTG-nnn> <participant name>, <title>, <organisation>
Status: <draft | pending_approval | approved APV-nnn>   Prepared: <date>   Version: <n>
Kind: interview   Conduct mode: interviewer   Platform: <zoom | meet | teams>   Join link: <attached at triage>
Date and time: <ISO datetime with time zone>   Time budget: <45> minutes   Language: <en>
Participants: <STK-nnn, role stakeholder>; Horus (interviewer); <Supervisor name> (observer, may whisper)
Confidentiality: client-confidential

## Objectives (at most three)
1. <objective>
2. <objective>

## Hypotheses to test and open questions to close
- HYP-<nn>: <statement>
- OQ-<nn>: <question>

## Participant context (internal; never read aloud)
<Three to five lines from the stakeholder record: role, stance and confidence, interests, red lines, prior public statements with EVD ids. Profile content appears only as implications for the conversation.>

## Disclosure and consent
Disclosure script: <script id>. Text: "<I am Horus, an AI participant conducting this interview for <engagement name> on behalf of <client entity>. The conversation is transcribed. May I continue?>"
Consent to confirm: AI participant <yes/no>; recording <yes/no>; transcript <yes/no>; attribution rule proposed: <on_record | background | not_for_attribution>.
If the participant objects: <offer a human-led interview; offer not_for_attribution; thank and end; log the objection>.

## Question guide
| Id | Question | Priority | Purpose | Tests | Follow-up heuristics |
|---|---|---|---|---|---|
| Q1 | <open question> | 1 | <what we learn> | HYP-<nn> | <if X, ask about Y; ask for numbers and their source; ask for documents> |
| Q2 | <question> | 2 | <purpose> | OQ-<nn> | <heuristic> |

## Follow-up rules
- <When a number is given, ask for its source and period.>
- <When a position is stated, ask what would change it.>

## Sensitivities and do-not-say
- Sensitivities: <topics to approach indirectly and why>
- Do not say: <client-confidential items; other stakeholders' views; options not yet public; any opinion on the options>

## Escalation rules
- Objection to the AI participant or to recording: <script>. Distress or anger: <pause, offer to stop>. Confidential information volunteered: <acknowledge, mark off record, do not probe>. Supervisor whisper, pause or leave: <comply immediately>.

## Time plan
Opening and consent <3> min | Block A <15> | Block B <15> | Block C <7> | Close <5>

## Close script
"<Thank you. May I confirm the attribution rule we agreed? You mentioned <document>; may we follow up by email? Our next step is <x>.>"

## After the interview
Debrief within <24> hours; thank-you email per template; documents promised logged as actions; proposed stakeholder and hypothesis updates to the Principal.
```

## Pre-read email (client PM)

```
Subject: <Engagement short name> | Pre-read for <meeting kind> on <date>
To: <PM name>   Cc: <steering members as agreed>

Dear <first name or title>,

Ahead of the <meeting kind> on <day, date, time, time zone>, the pre-read is attached: <deliverable title>, <DEL-nnn vN>, stamped DRAFT FOR DISCUSSION.

The meeting will ask for <number> decisions:
1. <decision, worded as on the decisions-sought slide>
2. <decision>

Readers short of time should start with <slides or pages>, which carry the findings behind each decision.

Could you confirm by <date> that the attendee list is right and that <named person> will attend? <attendee list>

Agenda (<duration> minutes): <item, minutes, lead>; <item, minutes, lead>.

Kind regards,
Horus, for <engagement name>
<Supervisor name>, <role>, accountable contact

Attachments: <file names>
Log: communications {classification: client_pm, related: [MTG-nnn, DEL-nnn]}; sets meetings.pre_read_sent.
```

## Minutes email (client PM, after a gate meeting)

```
Subject: <Engagement short name> | Minutes and decisions, <meeting kind> on <date>
To: <PM name>   Cc: <attendees>

Dear <name>,

Thank you for <today's> <meeting kind>. The decisions and actions as we recorded them:

Decisions
1. Agreed that <decision text>. <DEC-nnn internal>
2. Noted that <text>.

Actions
| # | Action | Owner | Due |
|---|---|---|---|
| 1 | <action> | <name> | <date> |

Open points
- <open question>, <owner>, <date>

Feedback on <deliverable> and how we will address it
- <comment in one line>: <what changes, in which version>

Please tell us by <date> if anything above differs from your record; otherwise we will treat the decisions as confirmed and update the plan. Next: <next meeting or deliverable, date>.

Kind regards,
Horus, for <engagement name>
<Supervisor name>, accountable contact

Log: communications {classification: client_pm, related: [MTG-nnn]}; decisions confirmed with forum MTG-nnn; client_inputs recorded for each comment.
```

## Thank-you and follow-up email (stakeholder, after an interview)

```
Subject: Thank you | <topic> conversation on <date>
To: <stakeholder name>

Dear <title and surname>,

Thank you for your time <today>. Your perspective on <topic> is valuable to the work <for <client entity>, where disclosed under consent>.

As agreed, your comments will be treated as <on the record | background, not attributed to you by name | not for attribution>. If you would like to change this, reply to this message.

You kindly offered to share <document>; receiving it by <date> would help us. <Optional single clarifying question.>

We will <send a summary of the consultation findings on <date> | not trouble you further unless you wish>.

With thanks and best regards,
Horus, AI participant acting for <engagement name>
<Supervisor name>, accountable contact, <email>

Log: communications {classification: stakeholder, related: [MTG-nnn]}; actions for documents promised; sets meetings.follow_up_sent.
```

## Weekly status email (client PM)

```
Subject: <Engagement short name> | Weekly status, week <n> of <total>, <date>
To: <PM name>   Cc: <as agreed>

Dear <name>,

Headline: <one sentence on where we stand against the workplan, for example "On track for the diagnostic readout on <date>; two data requests now block the baseline".>

Done this week
- <A-nn: what was completed>

Next week
- <A-nn: what will happen>

Needed from you
1. <decision or input>, <owner>, by <date> (ACT-nnn)

Risks and issues
- <Amber (word and glyph)>: <risk, impact, mitigation, owner>

Interviews: <held> held, <scheduled> scheduled, <outstanding> outstanding (priority 1: <roles>)
Data requests outstanding: <n>, oldest <d> days (list attached)
Milestones: <next milestone>, <date>, <status>

The one-page status note is attached.

Kind regards,
Horus, for <engagement name>
<Supervisor name>, accountable contact

Log: communications {classification: client_pm, related: [DEL-nnn status_note]}.
```

## Data-request list

```
# Data and document requests: <Engagement short name>, issued <date>, version <n>
Requests are numbered once and never renumbered; status is updated in every weekly note.

| # | ACT id | Item requested | Why we need it | Format and period | Client owner | Requested on | Needed by | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ACT-nnn | <dataset or document> | <RQ-nn or HYP-nn: the question it answers> | <CSV by month, 2021 to 2025 | PDF> | <name or unit> | <date> | <date> | P1 | requested |

Notes to the client: partial or imperfect data is welcome and its limits will be stated; data is held at client-confidential in the engagement workspace and returned or deleted at close; one named owner per request speeds closure.
```

Rules: ask once and bundle; every request names the question it answers; P1 requests block a gate and are escalated in the status email after <n> days; a fulfilled request links to its `documents` record through `actions.fulfilled_by`; the list is attached to a `client_pm` communication and is itself a rendering of `actions[kind=client_request_data, client_request_document]`, not a separate record.

Source: alignment-point protocol in ARCHITECTURE.md §4.3; `meetings.plan`, `actions` and `communications` fields in STATE_SCHEMA.md E1, E5 and E6; disclosure and consent rules in ARCHITECTURE.md §10.
