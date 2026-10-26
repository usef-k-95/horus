# SCQA

Situation, Complication, Question, Answer: Minto's pattern for the opening of any document or deck, which brings the reader from what they already accept to the question the work answers and the answer itself. Horus uses it for every executive summary, decision memo opening, email and deck introduction.

When Horus uses this: every deliverable and client communication; the first slide after the title and the first paragraph of every executive summary.

## What it is

SCQA is the introductory structure of the Pyramid Principle. Situation: a statement about the subject that the reader already knows and accepts, establishing time, place and context. Complication: what happened or changed to create a problem or an opportunity that makes the situation unstable. Question: the question that the complication raises in the reader's mind. Answer: the governing thought, which the body of the document then supports. The sequence works because it begins from agreement, creates tension, and resolves it with the answer, so the reader knows why they are reading before they read the argument. Variants reorder the elements for effect: answer-first (A, then S, C) for a reader who wants the conclusion immediately; complication-first for urgency; question-first for an expected debate. The benchmark executive summaries converge on this shape: the Harvard Kennedy School policy analysis exercise opens with a 25-word problem statement; UK ministerial submissions open with the issue in 100 words and the recommendation.

## When Horus uses it

- Executive summaries (at most 1,000 words) open with a one-sentence problem statement, which is the complication, and give the answer in the first paragraph.
- Decision memos: the issue section is S and C; the recommendation is A; the discussion answers the questions A raises.
- Decks: the executive summary slide and the context and mandate slide are SCQA; each section opener restates the question that section answers.
- Emails: the pre-read and follow-up emails follow SCQA in three or four sentences.
- Interview openings: the disclosure script leads, then an SCQA statement of why Horus is asking.

## Steps

1. **Write the Situation** in one or two sentences the reader cannot disagree with; use their own framing where possible.
2. **Write the Complication**: the change, gap or deadline that creates the need to decide; quantify it with a sourced number where one exists.
3. **State the Question** as the reader would ask it; check it is the question the governing thought answers.
4. **Give the Answer** as the governing thought, in one sentence, worded as a decision the reader can accept or reject.
5. **Choose the order** for the audience: standard for a readout; answer-first for a decision maker; complication-first for urgency.
6. **Test** by reading it aloud: the reader should know what the document is about, why now, and what Horus recommends within sixty seconds.
7. **Repeat at section level** for long documents.

## Outputs → state records

- `deliverables.storyboard_path`: the SCQA block at the head of the ghost deck and of document outlines.
- `brief.problem_statement.as_reframed` as the source of the Complication; `brief.context_summary` as the Situation.
- `decisions.statement` for `recommendation` as the Answer.
- `communications` of channel `email`: pre-read and follow-up bodies at `body_path` written in SCQA.
- `meetings.plan` openings and `meetings.purpose` for client meetings.

## Pitfalls

- A Situation the reader disputes; start from common ground or the argument is lost in the first sentence.
- A Complication without a number or a date; the tension is abstract.
- A Question the Answer does not answer; the most common structural fault in drafts.
- Hiding the Answer at the end of a long summary to build suspense; decision makers stop reading.
- SCQA that runs to a page; it is a paragraph.

## Source

Barbara Minto, The Pyramid Principle: Logic in Writing and Thinking, 3rd edition, Pearson, 2009; executive summary conventions in the Harvard Kennedy School policy analysis exercise (BENCHMARKS.md B11) and UK ministerial submissions (BENCHMARKS.md C1).
