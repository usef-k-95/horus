# Interview capture

A diarised transcript becomes evidence only through this protocol: speaker mapping verified, off-record segments removed, every substantive turn classified as a position or an asserted fact, quotes verbatim with turn references, attribution carried on every record, and stakeholder and hypothesis updates proposed for the Principal to confirm. This is the `interviewer`'s capture and debrief standard and the Principal's integration checklist.

**When Horus uses this:** after every live interview conducted through `horus-meet`; after co-led gate meetings, where the Principal captures; and when a human-led meeting is captured from notes (`conduct_mode: human`).

## Inputs and the first three checks

Inputs: the verified transcript (`meetings.transcript.path`, JSON Lines turns with speaker label, start and end time, text, confidence); the meeting record (`participants[].speaker_label`, `consent`, `plan.question_guide`); the participants' stakeholder records.

1. **Speaker mapping.** Confirm each diarised label maps to one `STK`. Where two participants share a label or confidence is low, mark the turns and lower the confidence of evidence drawn from them.
2. **Consent and attribution.** Read `consent.attribution_rule` and any objections. If the participant changed the rule mid-meeting ("this next part is background"), note the turn range; the stricter rule applies to those turns.
3. **Off-record segments.** `consent.off_record_segments[] {from, to}` and the `off_record_start` and `off_record_end` marks. Nothing inside becomes evidence, not even a paraphrase; the server rejects evidence whose turns fall inside (integrity rule 23). The stored transcript has the segments removed or flagged per `settings.meetings.off_record_handling`.

## Positions versus facts

Each substantive turn carries one or more claims. Ask of each: is this about what the speaker wants, believes, intends, predicts or will do (a **position**), or about the world (an **asserted fact**)? "We will not accept a licence for kiosks" is a position. "Most kiosks have no bank account" is an asserted fact, whoever says it.

Positions become `position` evidence (or `quote` where the exact words matter), cite the interview's **position source** (type `interview`, Tier A, `independence_group: stk-<nnn>-own`, tagged `own_statement`) and are validated by that source alone. Asserted facts become `fact`, `statistic`, `estimate`, `event` or `forecast` evidence, cite the interview's **assertion source** (type `interview`, Tier C, same group), carry `corroboration: single_source`, and take `confidence` from the speaker's proximity to the fact (a tax official on filing counts: medium; an association head on members' costs: low). Material asserted facts are listed in the debrief for a researcher's corroboration pass. Never attach an asserted fact to the position source: it would validate on one interview.

## Quotes and turn references

`quote_text` is verbatim from the verified transcript. Permitted edits: removing fillers; marking elisions with "[...]"; a bracketed word for grammar; nothing else. Translations keep the original in `notes`. Every interview evidence record carries the turn reference in `notes` in the form `MTG-007 t.41-t.43` (turn indices in the transcript file) and `attribution` set to the rule in force for those turns. The source record's `citation` is the attribution-safe form (ledger-protocol.md).

## Attribution rules

| Rule | Internal record | Client-facing use |
|---|---|---|
| `on_record` | Full | Name, title, direct quotes |
| `background` | Full | Substance attributed to a role or organisation class ("a senior ministry official"); no quote that identifies |
| `not_for_attribution` | Full | Substance only, no attribution, no verbatim quotes; folded into findings |
| Off record | Nothing stored as evidence | Nothing |

The internal record is always complete so the Principal can judge weight; the producer's sensitivity audit enforces the external form.

## What updates `stakeholders` and `hypotheses`

The interviewer proposes in `interview_record.proposed_updates`; the Principal confirms by updating the records.

- `stakeholder_patch`: `stance`, `stance_confidence`, `stance_basis` (the position EVD ids), `interests`, `concerns`, `red_lines`, `predicted_reactions[] {target, reaction, rationale, confidence, basis}` for each option discussed, `relationships[]` with `basis: observed` when the participant described a working relationship and `assessed` when inferred, `engagement.status: engaged`, `last_reviewed`.
- `hypothesis_patches[]`: per `HYP`, the EVD ids to add to `evidence_for` or `evidence_against` and whether the status should move. The interviewer sets `supports` and `contradicts` on the evidence it creates; it does not touch `hypotheses`.
- Referrals ("speak to the head of the chambers federation") go in `interview_record.referrals` as existing `STK` ids, or in the debrief as name and role for the Principal to create.

## Promises, documents and instructions

- **Documents promised**: `mark(document_promised)` during the call; afterwards an `actions` record of kind `follow_up` (owner the stakeholder, `requested_via` the MTG, due date as stated, `linked` to the RQ), listed in `interview_record.documents_promised`. When the file arrives the Principal runs `import_document` (a `documents` record with `origin: stakeholder`, `received_via` the MTG or the COM, `kind` by content, plus a `sources` record if the document is public), sets the action's `fulfilled_by` and `status: done`, and mines it into evidence.
- **Documents shared in the call** (a link in chat, a figure read out): the link is logged in `live.marks` and imported by the Principal; a figure read out is an asserted fact at Tier C until the document is in the library.
- **Requests to Horus** ("send us the draft before it goes to the minister"): the interviewer makes no commitment; record an `actions` record of kind `follow_up` with owner `principal`, flagged in the debrief for the Supervisor when it touches confidentiality or scope.
- **Instructions or directives** from a client-side participant (`is_client: true`): the interviewer writes an `open_questions` record if the instruction conflicts with the plan or the brief, and proposes a `client_inputs` record in the debrief (kind `instruction`, `directive` or `preference`, `from`, `via` the MTG, `content_verbatim`, `paraphrase`) for the Principal to create; the interviewer's write scope excludes `client_inputs`, `documents`, `decisions` and `communications`. In a co-led gate meeting the Principal writes `client_inputs` directly and, where the forum decided, a `decisions` record with the meeting as `forum`.
- **Facts about the client's own operations** stated by a client participant are still asserted facts; the corroborating file is requested as `client_request_document`.

## The meeting record after capture

Fill `plan.question_guide[].asked`, `answer_summary` and `turns[]`; `interview_record.topics[] {topic, position, evidence}`, `reaction_to_options[] {option, reaction, evidence}`, `contradictions[] {hypothesis, note}`, `documents_promised`, `referrals`, `follow_ups`, `proposed_updates`; `notes.structured {key_points, positions, quotes, surprises, sentiment}`; `outcomes {open_questions, actions, evidence}`; `debrief {path, by, what_worked, what_to_change}`; `status: held`.

## The debrief memo

Saved at `meetings/<MTG>/debrief.md`, written for a Principal who has not read the transcript:

1. Header: meeting, participants and mapping confidence, duration against budget, consent and attribution rule, interventions received (whispers, pauses, takeover).
2. Coverage: questions asked of total, skipped and why, questions the participant raised.
3. Positions ranked by bearing on the hypotheses, each with EVD ids and attribution.
4. Surprises: anything not in the plan or the profile.
5. Contradictions with hypotheses and with other interviews, by MTG id (one participant's words are never relayed to another).
6. Asserted facts needing corroboration, with suggested sources.
7. Promised documents, follow-ups, referrals, requests to Horus, instructions received.
8. Proposed stakeholder patch and hypothesis patches, as field-level changes.
9. Suggested questions for upcoming interviews.
10. What worked and what to change.
11. IDs written.

## Integration by the Principal

Confirm or amend the patches; create referrals as stakeholders, and the client inputs and documents; refresh the reaction matrix; queue the corroboration pass; draft the thank-you and follow-up `communications` record for approval, naming promised documents and next steps; checkpoint.

## Proposed schema additions

`evidence.meeting: → MTG` and `evidence.transcript_turns[]`, replacing the `notes` convention; `evidence.speaker_confidence` (STATE_SCHEMA.md open question 6); `sources.own_statement_of` as proposed in source-tiers.md, which would collapse the position and assertion records into one.

Source: ARCHITECTURE.md §4.3 step 3, §5.4 and §8; STATE_SCHEMA.md §E1 and integrity rules 22, 23 and 26; attribution conventions as defined in the Reuters Handbook of Journalism and the Chatham House Rule.

Adopted in STATE_SCHEMA.md 0.3: `evidence.transcript_turns` holds turn references and `evidence.meeting` the meeting; the server caps an interview, speech or social-media source at Tier C for any evidence that is not a `position` or `quote`, so one interview `sources` record suffices.
