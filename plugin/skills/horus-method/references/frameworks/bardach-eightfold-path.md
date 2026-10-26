# Bardach's Eightfold Path

A general-purpose discipline for policy analysis: define the problem, assemble evidence, construct alternatives, select criteria, project outcomes, confront trade-offs, decide, tell the story. It is the common-sense skeleton underneath every Horus pathway and the structure most clients recognise.

When Horus uses this: as the reference sequence for the whole engagement, and explicitly in P0 to P1 framing on the strategy pathway.

## What it is

Eugene Bardach's Eightfold Path is the standard teaching model for client-oriented policy analysis in public policy schools. Its eight steps are not strictly sequential; Bardach presents them as a loop the analyst runs several times, narrowing each pass. The method's distinctive contributions are the insistence on a problem definition that states a deficit or excess in measurable terms, the "outcomes matrix" that projects every alternative against every criterion, and the final instruction to stop analysing and tell a story a decider can act on.

## When Horus uses it

- P0 and P1 on every pathway as a checklist that the brief, hypotheses and workplan cover all eight moves. Each phase of the Horus Method maps to one or two steps: P0 to P2 cover steps 1 and 2, P3 covers 3 and 4, P4 covers 5 and 6, P5 covers 7 and 8.
- Strategy pathway anchor framework: when the brief sets a direction rather than a specific instrument, the Eightfold Path gives the client-facing methodology narrative in the kickoff deck.
- As a diagnostic when an engagement stalls: the Principal asks which step is incomplete. Most stalls are an unstated problem definition or criteria never agreed with the client.

## Steps

1. **Define the problem.** State it as a deficit or excess with a magnitude, not as a solution in disguise ("too few micro-firms issue e-invoices", not "there is no e-invoicing mandate"). Record both the client's wording and Horus's reframing.
2. **Assemble some evidence.** Collect only what changes a decision: the baseline, the causes, past attempts, what comparable jurisdictions did. Bardach's rule is to think before collecting; the Horus equivalent is research questions linked to hypotheses.
3. **Construct the alternatives.** Start broad, including do-nothing. Use the pathway's option logic to generate the long list; then simplify by combining and dropping.
4. **Select the criteria.** Separate evaluative criteria (efficiency, equity, legality, political acceptability, administrability) from the practical criteria of the client. Criteria are confirmed with the client, not assumed.
5. **Project the outcomes.** Build the outcomes matrix: alternatives in rows, criteria in columns, cells with the projected result and its confidence. Be explicit about the counterfactual and the uncertainty.
6. **Confront the trade-offs.** Where no alternative dominates, make the trade-off visible in commensurable terms, for example how much fiscal cost buys how much coverage.
7. **Stop, focus, narrow, deepen, decide.** Choose the preferred alternative or package; resist analysis beyond what the decision needs.
8. **Tell your story.** Write for the decider: the "New York taxi driver test" asks whether an intelligent outsider can follow the argument in a few minutes.

## Outputs → state records

- Step 1: `brief.problem_statement` (`as_given`, `as_reframed`, `reframing_rationale`) and an `analyses` record of kind `problem_framing`.
- Step 2: `approach.analytical_plan.research_questions[]` linked to `hypotheses`; `evidence` and `sources` as the researcher fills the ledger.
- Step 3: `options` with `status: long_list`, including one of kind `do_nothing`.
- Step 4: `decisions` of kind `guiding_principle` and `criteria_weights`; `analyses` of kind `options_screening` with `content.criteria[]`.
- Steps 5 and 6: `appraisals` (the outcomes matrix is the `impacts[]` block plus `summary`) and an `analyses` record of kind `option_comparison`.
- Step 7: a `decisions` record of kind `preferred_option`, later `recommendation`.
- Step 8: `deliverables` of type `decision_memo`, `executive_summary` and `policy_note`, built from a storyboard.

## Pitfalls

- Defining the problem as the absence of a favoured solution; the reframing step exists to catch this.
- Collecting evidence before deciding what would change the answer.
- Letting criteria stay implicit until the appraisal, then arguing about weights at AP4 instead of agreeing them at AP3.
- Treating the eight steps as a waterfall; expect at least two passes.
- Over-analysing: step 7 is a deliberate instruction to stop.

## Source

Eugene Bardach and Eric M. Patashnik, A Practical Guide for Policy Analysis: The Eightfold Path to More Effective Problem Solving, 7th edition, CQ Press, 2023 (BENCHMARKS.md B12).
