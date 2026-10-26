# CPI Public Impact Fundamentals

A three-by-three framework from the Centre for Public Impact: legitimacy (public confidence, political commitment, stakeholder engagement), policy (clear objectives, evidence, feasibility) and action (management, measurement, alignment). Horus uses it as a completeness check that a recommendation can actually deliver impact, not just pass appraisal.

When Horus uses this: P1 framing and P5 recommendation on the strategy pathway, and as a diagnostic lens when assessing why a past initiative failed.

## What it is

The Fundamentals were developed by the Centre for Public Impact (a BCG foundation) from more than 300 cases in its Public Impact Observatory. The framework holds that impact requires three things at once: legitimacy (the underlying support for the initiative), sound policy (a well-designed answer to a well-understood problem) and effective action (the capacity to translate policy into results). Each of the nine elements is defined in one sentence and is intended for self-assessment and conversation rather than as a scoring rubric. It is unusual among consulting frameworks in giving political legitimacy equal weight with design and delivery.

## When Horus uses it

- Strategy pathway anchor framework: the nine elements structure the "how we get there" and "resources and governance" sections of a strategy document, and the kickoff deck's methodology slide.
- P2 diagnosis on any pathway: when the brief concerns a policy that already exists and has underperformed, the Fundamentals separate a legitimacy failure from a design failure from a delivery failure, which point to different pathways.
- P4 to P5: as a final check on the preferred option before the recommendation. A design that scores well on policy but has no political commitment and no measurement plan is not ready.
- Communication: the legitimacy elements give the client a vocabulary for why stakeholder engagement is in the workplan.

## Steps

1. **Define the initiative** whose impact is being assessed: the current policy for a diagnostic, the preferred option for a pre-recommendation check.
2. **Assess legitimacy.** Public confidence: what polling, media and sentiment say. Political commitment: whether the decision maker and the people around them will defend it. Stakeholder engagement: whether affected groups were involved and will cooperate.
3. **Assess policy.** Clear objectives: SMART and agreed. Evidence: the baseline and the mechanism are supported at grade floor. Feasibility: legal, administrative and fiscal.
4. **Assess action.** Management: an accountable owner, a delivery chain and routines. Measurement: indicators, baselines and targets with data that exist. Alignment: incentives of the delivery actors point the same way as the objective.
5. **Rate and explain.** Rate each element on a simple scale with a one-paragraph rationale and the evidence behind it. Flag the weakest element as the binding constraint.
6. **Convert to actions.** Each weak element implies a specific move: a consultation, a measurement design, a governance fix, a messaging change.

## Outputs → state records

- Diagnostic use: an `analyses` record of kind `diagnostic` (or `strategic_position` on the strategy pathway) with `content` organised by the nine elements and `findings[]` with evidence links.
- Legitimacy findings: `analyses` of kind `public_sentiment` and `decision_maker_lens`; stakeholder stance fields on `stakeholders`.
- Policy findings: `brief.objectives[].measurable`; `hypotheses` status; `appraisals.feasibility`.
- Action findings: `analyses` of kind `implementation_plan` (`institutional_arrangements`, `kpis[]`, `delivery_chain[]`); `risks` of scope `implementation`.
- Pre-recommendation check: `limitations[]` and `caveats[]` on the final appraisal and option comparison.

## Pitfalls

- Using it as a checklist to be ticked rather than a conversation; CPI explicitly warns against this.
- Scoring legitimacy from the client's own view of itself. Use evidence from outside the client.
- Confusing "evidence" (the element) with volume of research; the test is whether the mechanism is supported.
- Treating alignment as organisational charts; it is about incentives.
- Presenting it as a scientific measure; it is a structured judgement, and the deliverable should say so.

## Source

Centre for Public Impact, The Public Impact Fundamentals, October 2016 (BENCHMARKS.md A5).
