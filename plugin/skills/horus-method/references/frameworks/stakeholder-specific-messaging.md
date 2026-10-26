# Stakeholder-specific messaging from the reaction matrix

The Horus method for deriving, for each stakeholder or segment, the objective (which reaction to move to), the messages (which pillar of the message house, framed in their interests), the proofs, the messenger, the channel and the timing, directly from the stakeholder reaction matrix. It keeps communication consistent with the analysis and specific to each audience.

When Horus uses this: P5 communication planning on every pathway; P3 to P4 when preparing pre-briefs for gate meetings and interviews that test options.

## What it is

The stakeholder reaction matrix predicts, for every priority stakeholder and every shortlisted option or principle, a reaction from support through conditional and neutral to resist and block, with a rationale, a confidence and the evidence. Stakeholder-specific messaging reads the matrix row by row and asks what would move the stakeholder one step toward support without changing the recommendation: an answer to the concern recorded in their rationale, a proof that addresses it, a messenger they trust, a channel they use, a moment when they can hear it. The method uses the message house for consistency (every audience hears a pillar of the same house), the influence map for messengers and sequencing, salience and veto analysis for priority, and the political calendar for timing. It also decides what is not said to whom, within the rule that nothing said to one audience contradicts what is said to another. The product is the audiences block of the communication plan and the pre-brief notes for gate meetings.

## When Horus uses it

- P5: the communication plan's audiences block is produced from the matrix for every priority-1 and priority-2 stakeholder and each public segment.
- Gate preparation: the attendees' predicted stances drive the pre-reads and the order of the deck's arguments.
- Interviews that test options at P3 to P4: the question guide includes the proofs most relevant to the interviewee's concern, to observe the reaction.
- Opposition handling: for stakeholders predicted to block, the message is paired with a handling plan and a decision on whether to engage, compensate or isolate.

## Steps

1. **Take the reaction matrix** for the recommended option or package and list stakeholders by priority and by predicted reaction.
2. **Set the objective** per stakeholder: the reaction to move to (block to resist, resist to conditional, conditional to support), or to maintain support.
3. **Read the rationale** behind the predicted reaction: the interest, concern or red line it rests on; check the evidence and its date.
4. **Select the pillar** of the message house that addresses the concern and frame it in the stakeholder's terms; choose the two proofs that matter to them; note what is not to be said.
5. **Choose the messenger** from the influence map (who they trust) and the channel (meeting, letter, briefing, public statement, intermediary).
6. **Set timing** against the political calendar and the sequence (allies before opponents, decision maker before the public, Agree roles before the gate).
7. **Write the Q&A** for the predicted objections and the handling plan for blockers.
8. **Record and update** after each contact; a changed reaction updates the matrix and the plan.

## Outputs → state records

- `analyses` of kind `communication_plan` with `content.audiences[] {stakeholder or segment: → STK, objective, messages[], channels[], timing, spokesperson, risks}`, `sequencing[]`, `qa_bank[]`, `opposition_handling[]`.
- Source: `analyses` of kind `stakeholder_reaction_matrix` (`cells[] {stakeholder, target, reaction, rationale, confidence, basis}`, `coalition_notes`) and `stakeholders.predicted_reactions[]`, `interests`, `concerns`, `red_lines`, `relationships[]`.
- Messengers and sequencing from `analyses` of kind `internal_politics` (`influence_paths[]`) and the political calendar.
- Pre-brief notes as `deliverables` of type `memo` linked to the gate `meetings` record; outbound contacts as `communications` with approvals.
- Updated reactions after contact: `stakeholders.predicted_reactions[]` with new `basis` and `last_reviewed`; `meetings.interview_record.reaction_to_options[]`.

## Pitfalls

- Different promises to different audiences; emphasis may differ, substance may not.
- Messaging to the stated position rather than the underlying interest in the rationale.
- Using a messenger the stakeholder does not trust because they are available.
- Treating blockers as persuadable when the red line is real; the honest output is a handling plan and a note to the decision maker.
- Letting the plan go stale; reactions move after every interview and leak.

## Source

Horus method, combining the stakeholder reaction matrix (ARCHITECTURE.md section 9) with the message house and World Bank strategic communication for reform (Cabañero-Verzosa and Garcia, 2009); stakeholder analysis after Mitchell, Agle and Wood (1997) and Mendelow (1981).
