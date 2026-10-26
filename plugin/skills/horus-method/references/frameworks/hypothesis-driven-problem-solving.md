# Hypothesis-driven problem solving

The consulting method of stating the likely answer early, decomposing the question into a MECE issue tree, and directing all analysis at proving or disproving the hypotheses. It makes a six-week engagement converge where an open-ended study would not.

When Horus uses this: P1 problem framing on every pathway, and continuously as the discipline behind research questions, workplans and the storyline.

## What it is

The method practised by McKinsey, BCG and Bain and codified in Minto's Pyramid Principle: start with a day-one answer, structure the problem into mutually exclusive and collectively exhaustive (MECE) branches, decide which analyses would move each branch, run only those, and revise the answer as evidence arrives. "Answer-first" is a working posture, not a conclusion; the hypothesis is held loosely and written down so it can be killed. The issue tree is the map of the problem; the hypothesis tree is the same map with the current best answer written on each branch. The workplan is derived from the tree, so every analysis has a reason to exist.

## When Horus uses it

- P1 on every pathway: the Principal turns the reframed problem into an issue tree and a first hypothesis set before the kickoff deck is drafted. The tree becomes the "hypotheses to test" slide.
- P2: research questions, worker briefs and interview question guides are each tied to a hypothesis; the researcher's fan-out is bounded by the tree.
- P3 to P5: the storyline is the hypothesis tree with the supported branches written as action titles. The ghost deck inherits the structure.
- Strategy pathway anchor framework, where the question is open and convergence matters most.

## Steps

1. **Write the governing question** in one sentence from the reframed problem statement. It must have a decidable answer.
2. **State a day-one hypothesis.** The Principal's best guess at the answer, with the two or three conditions that would have to be true.
3. **Build the issue tree.** Decompose the question into sub-questions until each leaf can be settled by one analysis or one interview. Test each level for MECE: no overlaps, no gaps. Prefer trees of three to five branches at each level.
4. **Convert leaves to hypotheses.** Each leaf gets a falsifiable statement, a kind (diagnostic, causal, option_effect, political, stakeholder, implementation), and the evidence that would refute it.
5. **Prioritise.** Mark the branches on which the answer most depends; analyse those first. Skip analyses that would not change the recommendation whatever they found.
6. **Plan the analyses.** Each prioritised hypothesis becomes a research question with a method, data sources and owner; interview questions are tagged to hypotheses.
7. **Run, record, revise.** As evidence lands, set hypothesis status to supported, refuted or revised, with a revision history. Rewrite the day-one answer at each gate.
8. **Convert to storyline.** The supported tree is reordered answer-first and becomes the pyramid of the deck.

## Outputs → state records

- The issue tree: an `analyses` record of kind `issue_tree` (or `problem_framing`), referenced from `approach.problem_framing`.
- Each leaf: a `hypotheses` record with `statement`, `kind`, `parent`, `research_questions`, `status`, `confidence`, `evidence_for`, `evidence_against`, `revision_history[]`.
- The analytical plan: `approach.analytical_plan.research_questions[]` with `hypotheses` links, method and status.
- Interview linkage: `meetings.plan.question_guide[].tests` pointing to hypotheses; `meetings.hypotheses_to_test`.
- Evidence linkage: `evidence.supports` and `evidence.contradicts`.
- Storyline: `deliverables.storyboard_path` for the readout decks.

## Pitfalls

- Confirmation bias: the day-one answer becomes the answer. The guard is to write, for every hypothesis, what evidence would refute it and to assign someone to look for it.
- Trees that are MECE in words but not in analysis: branches that need the same data are not independent.
- Decomposing by organisational unit or by data availability instead of by the logic of the question.
- Too many hypotheses: more than about 15 live hypotheses on a six-week engagement means the tree is too deep.
- Leaving hypotheses `untested` at AP2; the gate requires every hypothesis to have moved.
- Sharing the day-one answer with the client as if it were a finding.

## Source

Barbara Minto, The Pyramid Principle: Logic in Writing and Thinking, 3rd edition, Pearson, 2009; Ethan Rasiel, The McKinsey Way, McGraw-Hill, 1999; Charles Conn and Robert McLean, Bulletproof Problem Solving, Wiley, 2018. Observed practice in public-record McKinsey decks is catalogued in BENCHMARKS.md A3.
