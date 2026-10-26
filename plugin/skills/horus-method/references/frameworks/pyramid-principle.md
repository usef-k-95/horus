# Minto's Pyramid Principle

Barbara Minto's method for structuring written and spoken argument: the governing thought at the top, a key line of three to five supporting points that are MECE, and supporting detail beneath, with every group summarised by the point above it and ordered by a stated logic. Horus uses it as the structure of every storyline, ghost deck and document.

When Horus uses this: every deliverable, from the kickoff deck to the decision memo; the producer's logic audit tests against it.

## What it is

The Pyramid Principle holds that readers understand ideas most easily when they receive the summarising idea first and the supporting ideas after, grouped and ordered. Three rules govern the pyramid. Ideas at any level summarise the ideas grouped below them. Ideas in each group are the same kind of idea. Ideas in each group are ordered logically: deductively (premise, premise, conclusion), chronologically, structurally (parts of a whole) or by degree (most to least important). Vertically the pyramid is a question-and-answer dialogue: each statement raises a question in the reader's mind that the level below answers. The introduction follows the situation-complication-question-answer pattern (SCQA) to bring the reader to the governing thought. In consulting practice the key line becomes the executive summary and the section headers of the deck, and each key-line point is proved by the slides beneath it. The method is also a thinking tool: building the pyramid bottom-up from findings exposes gaps and non sequiturs before writing.

## When Horus uses it

- Ghost deck: the Principal writes the governing thought, the key line and then a full-sentence action title per slide, so the titles read as the argument on their own; the body of each slide proves its title.
- Documents: the policy note, strategy document and RIA report carry the same pyramid in prose; the executive summary is the key line.
- Decision memo: the recommendation is the governing thought; the discussion is the key line.
- Interview debriefs and status notes: the same structure at small scale.
- QA: the logic audit reads titles only and checks that each group is MECE and that each level answers the question above.

## Steps

1. **Write the governing thought** as one sentence that answers the client's question; if it cannot be written, the analysis is not finished.
2. **Draft the key line**: the three to five points that together make the governing thought true; test for MECE and for the same kind of idea.
3. **Choose the ordering logic** for the key line and state it (deductive for a recommendation chain, structural for pillars, degree for priorities).
4. **Build downward**: for each key-line point, the supporting points; repeat until each leaf is a slide or a paragraph with evidence.
5. **Check vertically**: does each level answer the question the level above raises; remove statements that answer no question.
6. **Write the introduction** as SCQA to bring the reader to the governing thought.
7. **Convert to titles**: each node becomes a full-sentence action title; read titles top to bottom as the argument.
8. **Attach evidence IDs** to each leaf for traceability.

## Outputs → state records

- `deliverables.storyboard_path`: the ghost deck or outline with governing thought, key line, action titles, exhibit types, body content, evidence IDs and the "so what" per slide.
- `deliverables.evidence_used` (computed from the storyboard) and the traceability audit result in the version's `qa.traceability`.
- `analyses` with `narrative_path` written as pyramids for research memos and diagnostic syntheses.
- `decisions.statement` worded as the governing thought for `recommendation` and `preferred_option` kinds.
- `meetings.plan` objectives and `decisions_sought[]` as the governing thoughts for a gate meeting.

## Pitfalls

- Key-line points that are topics ("costs", "stakeholders") rather than assertions.
- Groups that are not the same kind of idea (two reasons and one action step).
- Inductive groups with six or more members; regroup.
- Starting from the slides and writing titles afterwards; the pyramid is built before rendering.
- Burying the answer because the client may not like it; the method is answer-first, and the message is handled through framing and sequencing, not by hiding it.

## Source

Barbara Minto, The Pyramid Principle: Logic in Writing and Thinking, 3rd edition, Pearson, 2009 (first edition 1987).
