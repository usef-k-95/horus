# Storyline and the ghost deck

How the Principal builds an answer-first storyline and writes the ghost deck that every rendering follows. Covers the pyramid, SCQA openings, MECE, the horizontal and vertical logic tests, and the exact storyboard format with a worked example.

When Horus uses this: before any deliverable is rendered (step 1 of the alignment-point protocol), when restructuring after client feedback, and whenever the logic audit or the partner review questions the argument.

## Answer first: the pyramid

1. **Governing thought.** One sentence that answers the client's question. At AP1 it is the approach, at AP2 the diagnosis, at AP3 the shortlist and principles, at AP4 the preferred option, at AP5 the recommendation. Write it before anything else; if it cannot be written, the work is not ready to be shown.
2. **Key line.** Three to five statements that together make the governing thought true. Inductive key lines give parallel reasons of the same kind (three findings, four benefits). Deductive key lines run situation, complication, therefore. Prefer inductive for decks: each statement stands alone as a slide title.
3. **Supports.** Under each key-line statement sit the slides or paragraphs that prove it, each resting on evidence IDs from the ledger.
4. **Question and answer dialogue.** Every statement raises exactly one question in the reader's mind (why? how? how much?). The level below answers that question and nothing else.
5. **Direction.** Build top-down from the question; verify bottom-up from the evidence. Never render slides first and look for the story afterwards.

## SCQA openings

- **Situation**: what the reader already knows and accepts, taken from `brief.context_summary` and the mandate.
- **Complication**: what changed or is failing, taken from the baseline analysis and the gap it shows.
- **Question**: the question the complication forces, phrased as the decision maker would ask it.
- **Answer**: the governing thought.

Choose the order by audience. Tier 0 is answer-first: the recommendation is the first sentence and the situation and complication are compressed into the issue paragraph. Tier 1 steering decks use the standard order on the executive-summary slide. When the audience disputes that there is a problem (a sceptical diagnostic readout), open with the complication and its evidence before the answer.

## MECE

Every grouping in the storyline (issue tree, option long list, pillars, risk categories, stakeholder groups, audiences) is mutually exclusive and collectively exhaustive.

- Overlap test: could any item sit in two buckets? If yes, redraw the buckets.
- Gap test: ask "what else?" against a standard frame from the pathway pack (an instrument typology, the Five Case Model, the delivery chain) rather than against intuition.
- Shape: two to five items per level, parallel grammar, the same level of abstraction, each label meaningful on its own.
- Do not invent a taxonomy where the pathway pack supplies one.

## Horizontal and vertical logic tests

| Test | Procedure | Pass criterion |
|---|---|---|
| Horizontal (titles only) | Extract every action title in order into a list; read it aloud | The list alone states the governing thought and its key line; each title is a complete sentence making one claim; no title restates another; removing any title breaks the argument; adding none is needed; the executive-summary statements and the titles match word for word |
| Vertical (body proves title) | For each slide, compare title, body and exhibit | Every claim and number in the title is shown in the exhibit or body; the highlighted data point is the title's number; nothing on the slide is unrelated to the title; the title would be false if the exhibit showed different data |
| MECE | At each grouping, apply the overlap and gap tests | No overlaps, no gaps, two to five items, parallel form |

Failing patterns: label titles ("Market overview"); description titles ("This chart shows take-up by size class"); two-claim titles joined by "and"; a body that proves a different claim; a "so what" that introduces a claim the slide does not prove; numbers in the title that differ from the exhibit.

## The ghost deck

The ghost deck is the storyboard the Principal writes before any rendering. `producer` renders only what it contains; the file path is `deliverables.storyboard_path`, and `deliverables.evidence_used` is parsed from its `Evidence:` lines. Documents follow the same format with one block per section and a paragraph budget instead of a body-word budget, so the memo, the deck and the report are one argument with one set of evidence IDs.

Procedure: write the question and governing thought; write the key line; draft every action title; run the horizontal test; assign an archetype to each slide and specify the exhibit and evidence IDs from the ledger, writing `GAP` where evidence is missing and raising a research brief for it; write the "so what" and speaker notes; run the vertical test; reconcile tiers (each Tier 0 paragraph maps to a Tier 1 slide, each Tier 1 slide to a Tier 2 section); register the storyboard path on the deliverable and open a version.

## Storyboard format

Markdown, fixed keys, one block per slide. Header:

```
# Storyboard: <deliverable title>
Deliverable: DEL-nnn | Type: <deliverables.type> | Tier: T0..T3 | Version: n
Audience: STK-nnn (role), ... | Meeting: MTG-nnn (<kind>, <date>) | Language: en
Template: <template id and version> | Confidentiality: client-confidential
Question: <the client's question in one sentence>
Governing thought: <one sentence>
SCQA: S: ... | C: ... | Q: ... | A: ...
Decisions sought: DEC-nnn (proposed) ...
Horizontal logic: 1. <title> 2. <title> ... (all titles, in order)
```

Slide block:

```
## Slide <n>
Title: <full sentence, one claim, at most two lines at the tier's title size>
Archetype: <id from slide-archetypes.md>
Section: <tracker label, for example "Where we are (2 of 5)">
Body: <bullets or table outline within the tier's word limit>
Exhibit:
  Type: <chart or table type, or "none">
  Series: <what is plotted, by what, for which period>
  Units: <unit, currency and price base year where relevant>
  Highlight: <the one series or data point the title rests on>
  Source line: <"Source: <SRC citations>; Horus analysis">
Evidence: EVD-nnnn, EVD-nnnn (EVD ids only; "none" allowed only for cover, road-marker, decisions-sought and next-steps)
Draws on: ANA-nnn, APL-nnn, OPT-x, DEC-nnn, ASM-nnn (as applicable)
So what: <the implication for the decision, at most 25 words>
Notes: <what the presenter says in 30 to 60 seconds; the likely question and its answer>
```

Rules: titles have no terminal full stop; `Evidence:` holds evidence IDs only; a number in the title or body with no evidence ID is a traceability fail; `GAP` in any field blocks rendering; the `Section:` label must match a road-marker entry.

## Worked example (illustrative)

Fictional engagement on an e-invoicing policy for small firms. Every number below is invented for training purposes and must not be reused as data.

```
# Storyboard: Appraisal readout, e-invoicing for micro and small firms
Deliverable: DEL-014 | Type: appraisal_deck | Tier: T1 | Version: 1
Audience: STK-003 (sponsor), STK-004 (deputy minister), STK-006 (tax authority) | Meeting: MTG-012 (steering, 2026-12-09) | Language: en
Template: horus-deck-16x9 v1 | Confidentiality: client-confidential
Question: Which instrument should the ministry adopt to bring micro and small firms into e-invoicing?
Governing thought: A phased mandate paired with free invoicing tools reaches the coverage target at the lowest compliance cost and is the only shortlisted option merchant associations would accept.
SCQA: S: E-invoicing has been mandatory for large firms since 2022 | C: Micro-firm take-up has stalled below one in five | Q: Which instrument closes the gap without a backlash from small merchants? | A: The phased mandate with free tooling (OPT-B2)
Decisions sought: DEC-021 (preferred option), DEC-022 (phasing principle)
Horizontal logic: 1. Four years in, e-invoicing covers large firms almost fully but fewer than one micro-firm in five  2. Among the shortlisted options, the phased mandate with free tooling reaches the target at the lowest compliance cost  3. The steering committee is asked to confirm OPT-B2 as preferred and to agree the phasing principle

## Slide 1
Title: Four years in, e-invoicing covers large firms almost fully but fewer than one micro-firm in five
Archetype: baseline-trend
Section: Where we are (1 of 3)
Body: One line under the chart: "Micro-firms are 91 per cent of registered businesses (illustrative)."
Exhibit:
  Type: column chart, emphasis form
  Series: share of registered firms issuing at least one e-invoice in 2025, by size class (micro, small, medium, large)
  Units: per cent of firms
  Highlight: micro (18 per cent, illustrative); other columns grey
  Source line: Source: national tax authority e-invoicing registry, 2025 extract (SRC-0022); business register 2025 (SRC-0031); Horus analysis. Illustrative figures.
Evidence: EVD-0047, EVD-0052
Draws on: ANA-007
So what: The policy problem is the micro segment; any instrument is judged on reach there.
Notes: Say that large-firm coverage shows the system works; the gap is adoption cost, not technology. Likely question: is the 18 per cent rising? Answer: flat for three years (EVD-0052).

## Slide 2
Title: Among the shortlisted options, the phased mandate with free tooling reaches the target at the lowest compliance cost
Archetype: appraisal-comparison
Section: What the options deliver (2 of 3)
Body: Table, options as columns: do-nothing, OPT-A (incentive only), OPT-B2 (phased mandate plus free tools), OPT-C (single-date mandate); rows: micro-firm coverage in year 3, compliance cost per firm per year, fiscal cost, administrative feasibility, predicted reaction of merchant associations, verdict.
Exhibit:
  Type: comparison table with Harvey balls for qualitative rows and low-to-high ranges for quantified rows
  Series: appraisal results for four options against the same baseline and assumptions register
  Units: per cent of micro-firms; local currency per firm per year, 2026 prices; fiscal cost in millions, 2026 prices
  Highlight: OPT-B2 column
  Source line: Source: Horus appraisal APL-004 to APL-007 (standard cost model, 2026 prices, assumptions ASM-003 to ASM-011). Illustrative figures.
Evidence: EVD-0047, EVD-0063, EVD-0071, EVD-0078
Draws on: APL-004, APL-005, APL-006, APL-007, ANA-014, DEC-011
So what: OPT-B2 is the only option that scores well on reach and acceptability at once.
Notes: Walk the table by row, not by column. Likely question: why not OPT-C, which is cheaper to run? Answer: predicted blocking by merchant associations (ANA-014) and a coverage dip in year 1.

## Slide 3
Title: The steering committee is asked to confirm OPT-B2 as preferred and to agree the phasing principle
Archetype: decisions-sought
Section: Decisions (3 of 3)
Body: 1. Agree that OPT-B2 is the preferred option for the final recommendation. 2. Agree the principle that obligations on micro-firms are phased over 36 months and paired with free tooling. 3. Note the next steps: implementation plan and communication plan for AP5 on 2027-01-20.
Exhibit:
  Type: none
Evidence: none
Draws on: DEC-021, DEC-022, ACT-040
So what: Two decisions today keep the final recommendation on schedule.
Notes: Read each decision aloud and ask for confirmation one at a time; record outcomes on MTG-012.
```

Source: Barbara Minto, The Pyramid Principle: Logic in Writing and Thinking (Minto International; third edition, Pearson, 2009). MECE and the ghost deck are McKinsey working practice with no single canonical document; the deck conventions observed in BENCHMARKS.md A3 are the public evidence for them.
