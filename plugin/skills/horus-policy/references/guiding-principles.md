# Guiding principles and political directives

How Horus drafts five to seven candidate principles, prepares the directive questions for the decision makers, pre-tests both against the stakeholder reaction matrix, records what the principles workshop decides, and converts the result into the criteria weights the comparison uses.

When Horus uses this: phase P3, between the diagnostic readout (AP2) and the principles workshop (AP3); revisited when a directive is superseded or the political calendar moves.

## Why principles come before appraisal

An appraisal compares options against criteria. If Horus chooses the criteria and their weights after the numbers are in, the recommendation is Horus's preference wearing a method. Principles fix the criteria and the weights with the decision makers before the options are appraised, so the appraisal is their judgement applied consistently. They also make politics explicit: a red line is a principle with infinite weight, and it is better written down at AP3 than discovered at AP5.

## Drafting candidate principles

Draw on three sources: the brief's objectives and constraints (`brief.objectives`, `brief.constraints`), the decision-maker lens (`decision_maker_lens.priorities`, `red_lines`, `framing_guidance`) and the diagnosis (what the baseline and the diagnostic showed must change, and what previous attempts got wrong). Draft five to seven; fewer leaves gaps, more cannot be weighted meaningfully.

Each candidate is a `decisions` record at `status: proposed` with `kind: guiding_principle`, `proposed_by: horus`, a `statement`, a `rationale` pointing at evidence, and `implications[] {area, change}` saying what the principle does to the option space. A good statement passes four tests:

- **Normative and specific**: it says what good policy here must do or must not do, in the decision maker's words where possible, not "effective" or "sustainable".
- **Discriminating**: it would rank at least two shortlisted options differently; a principle every option satisfies is a value statement, not a criterion.
- **Contestable**: a reasonable stakeholder could disagree with it, which is why it needs a decision.
- **Observable**: an analyst can score an option against it from evidence.

Typical families: who bears the burden (phasing or exemptions for small firms); mandatory versus voluntary; fiscal neutrality or a cost ceiling; speed of effect; reliance on existing institutions versus new ones; alignment with an international standard; distributional protection for a named group; reversibility.

## The directive questions

Directives are the decision maker's constraints that no analysis should overturn. Horus asks them as questions, at the workshop or in a pre-meeting with the sponsor, and records the answers as `decisions` of kind `political_directive`. The standing set:

| Question | What it fixes |
|---|---|
| What is unacceptable whatever the analysis shows? | Red lines; screen-outs |
| What is the fiscal envelope, one-off and recurring, over what period? | The cost criterion and the affordability test |
| Mandatory or voluntary, and for whom? | Instrument family and phasing |
| What must be visible, and by when, against the political calendar? | Timing criterion; quick wins; sequencing |
| Who must be inside the tent before this is announced? | Coalition requirements; consultation sequence |
| Which institution owns this, and which must not? | Institutional home; operating-model constraints |
| How much risk of failure is acceptable, and of what kind? | Risk appetite; pilot versus full roll-out |

Answers are recorded close to verbatim in `statement` with `made_by`, `forum` and `date` (rule 7). A directive that conflicts with the evidence is still recorded, with the conflict in `rationale` and an `open_questions` record if it needs revisiting.

## Pre-testing against the reaction matrix

Before the workshop, the `stakeholder_reaction_matrix` analysis takes the proposed principles as `columns` (→ DEC) beside the shortlisted options, and each priority-1 stakeholder gets a predicted reaction (`support`, `conditional`, `neutral`, `resist`, `block`) with rationale, confidence and the interview evidence behind it. The pre-test asks three things: which principles would a veto player block, and can the statement be re-cut without losing the content; which principle, if adopted, turns a `block` on the leading option into `conditional` (that is the principle that buys the coalition); and where predictions rest on low confidence, so the interviewer can test them in the remaining interviews. The results shape the workshop deck: principles are presented with the reactions they are expected to draw, not as neutral virtues.

## The workshop and what gets recorded

The AP3 deck presents the diagnosis in one slide, the short list and screening, the candidate principles with their implications and predicted reactions, and the directive questions. In the room, Horus captures each decision live. After the workshop the state must hold: every candidate principle `confirmed`, amended (a superseding record with `supersedes`) or `reversed`; every directive question answered as a `political_directive` or parked as an `open_questions` record with an owner; a `shortlist` decision; and a `criteria_weights` decision. Gate AP3 checks exactly this.

## Converting principles into criteria weights

The comparison needs weights that sum to one over criteria that do not overlap. Procedure, run in the workshop or immediately after with the sponsor:

1. List the criteria: one per confirmed principle, plus any brief objective not already covered. Merge overlapping principles into one criterion, or drop one, before weighting.
2. Mark direction: `higher_is_better` true or false for each.
3. Elicit weights by point allocation (100 points across the criteria) or by swing weighting (rank the criteria by how much it matters to move from the worst to the best shortlisted option on each, then scale), from the decision makers present. Record who allocated and the method.
4. Normalise to sum to one. A red line is not weighted: it is a screen, applied before scoring.
5. Record a `decisions` record of kind `criteria_weights` whose `statement` is the weights table, whose `rationale` names the principles each weight derives from, and whose `affects` lists the shortlisted options and the comparison analysis.

The analyst reads this decision into `mca.Criterion(name, weight, higher_is_better)` objects for `mca.mca`, and references it from `options_screening.criteria[].source`, `option_comparison.criteria_weights` and `strategic.criteria_weights`. Rank robustness (`strategic-options.md`) then shows the decision makers how much their weights matter, which is often the moment a weight gets revised; a revision is a superseding `criteria_weights` decision, never an edit.

## Worked example (illustrative)

From the e-invoicing case in `option-design.md`. Candidate principles: P1 "Micro-enterprise compliance costs are phased and paired with free tooling" (from the deputy minister's red line and the regressive incidence finding); P2 "The VAT gap narrows measurably within three years"; P3 "No new licensing regime for small merchants"; P4 "Use the tax authority's existing platform; no new entity"; P5 "Open technical standards; no single certified vendor". Pre-test: merchant associations move from `block` to `conditional` on the mandate once P1 is adopted (interview evidence, medium confidence); software vendors `resist` P5. Workshop: P1 to P4 confirmed; P5 amended to "open standards with a transition for existing vendors". Directives: envelope 40 million one-off (illustrative); mandatory, phased; visible results before the budget speech in 18 months. Weights (100 points, sponsor and deputy minister): fiscal gain 30, SME burden 30 (lower is better), feasibility 20, political fit 20, recorded as `DEC-012`; P3 is a screen, not a weight. The toolkit demo uses exactly these four criteria and weights.

## Pitfalls

Principles written by Horus for Horus (motherhood statements); more than seven; weights set by the analyst "for now" and never revisited; red lines weighted instead of screened; directives taken from a junior official and recorded as the decision maker's; reactions asserted without interview evidence; a workshop that ends without the weights decision, which stalls AP4.

Source: Horus method; HM Treasury, The Green Book (2022), on critical success factors for long-list screening; Department for Communities and Local Government (UK), Multi-criteria analysis: a manual (2009), on swing weighting and weight elicitation; Bardach and Patashnik, A Practical Guide for Policy Analysis (7th edition, 2023), step 4.
