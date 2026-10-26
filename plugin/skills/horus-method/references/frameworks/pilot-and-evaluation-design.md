# Pilot and evaluation design

How to design a pilot that tests the critical assumptions of an option before full roll-out, and an evaluation plan that will show whether the policy worked: questions, design (randomised, quasi-experimental, theory-based), sample, duration, data, and the decision the results will inform. Horus uses it for programme and service designs and for any option whose mechanism is unproven in the client's context.

When Horus uses this: P4 on the programme and service design pathway (`service.pilot_design` is required) and P5 on every pathway for `appraisals.monitoring.evaluation` and the pilot and evaluation plan deliverable.

## What it is

The UK Magenta Book is the central guidance on evaluation design for government: it distinguishes process evaluation (was it delivered as intended), impact evaluation (what difference did it make, against a counterfactual) and value-for-money evaluation, and it maps designs to questions and feasibility, from randomised controlled trials through difference-in-differences, regression discontinuity, synthetic control and matching, to theory-based approaches when counterfactuals are impossible. The World Bank's Impact Evaluation in Practice is the equivalent reference for development programmes. The Behavioural Insights Team's Test, Learn, Adapt argues for randomised trials in policy wherever feasible. A pilot is an evaluation designed before the decision: it tests the critical link in the theory of change on a sample large enough to detect the effect that would matter, for long enough for the effect to appear, with a pre-specified analysis and a decision rule for scaling, adapting or stopping.

## When Horus uses it

- Programme and service design pathway: the pilot design is part of the service concept appraisal and the pilot and evaluation plan is a core Tier-2 deliverable.
- Regulatory pathway: regulatory sandboxes and phased implementation are pilots and need the same design; the RIA's monitoring and evaluation section needs an evaluation method.
- Transformation pathway: interventions trialled in a few units before roll-out; the trajectory gives the effect size that matters.
- Public investment pathway: the management case's benefits realisation and evaluation plan.
- Every pathway: `appraisals.monitoring.evaluation {when, method}` must be filled with a real design, not "an evaluation will be commissioned".

## Steps

1. **State the evaluation questions** from the theory of change: which links are uncertain and would change the decision if false.
2. **Define outcomes and measures** with data sources, baselines and the minimum effect that would matter for the decision.
3. **Choose the design**: randomised where units can be assigned and ethics allow; otherwise the strongest quasi-experimental design the roll-out permits (staggered roll-out enables difference-in-differences; eligibility thresholds enable regression discontinuity); theory-based process evaluation alongside.
4. **Size the sample and duration**: power to detect the minimum effect; time for the effect to appear and for seasonal cycles.
5. **Specify data collection**: administrative data first, surveys where needed, qualitative work on mechanism; consent and data protection.
6. **Pre-register the analysis and the decision rule**: what result leads to scale, adapt or stop, and who decides.
7. **Cost and govern** the pilot: budget, owner, independence of the evaluator, reporting dates aligned to the political calendar.
8. **Plan the post-implementation evaluation** for the full roll-out with the same logic.

## Outputs → state records

- `appraisals.service.pilot_design {design, sample, duration, evaluation_method}` on the programme pathway; `appraisals.monitoring {indicators[], evaluation {when, method}}` on every pathway.
- `hypotheses` of kind `option_effect` and `implementation` that the pilot tests, with the pre-specified evidence that would refute them.
- `assumptions` (`category: behavioural`, `policy`) whose ranges the pilot is designed to narrow; `sensitivity_rank: high`.
- `deliverables` of type `pilot_evaluation_plan`; the evaluation section of `ria_report`, `business_case` and `delivery_plan`.
- `implementation_plan.content.sequencing[]` with the pilot phase, and `budget` for the evaluation; `decisions` of kind `process` recording the decision rule.
- `risks` of scope `policy_outcome` for a pilot that cannot detect the effect, and `political` for results arriving after a window closes.

## Pitfalls

- Pilots designed to succeed: volunteer sites, no comparison group, outcomes chosen after the fact.
- Too small or too short to detect the effect that matters; power and lag are calculated, not guessed.
- Evaluation specified as a method name without questions, data or a decision rule.
- Ignoring the political calendar; a pilot that reports after the decision is a research project.
- Treating process evaluation as optional; when a pilot fails, the process evaluation says whether design or delivery failed.

## Source

HM Treasury, The Magenta Book: Central Government Guidance on Evaluation, 2020; Paul J. Gertler and others, Impact Evaluation in Practice, 2nd edition, World Bank, 2016; Laura Haynes, Owain Service, Ben Goldacre and David Torgerson, Test, Learn, Adapt: Developing Public Policy with Randomised Controlled Trials, Cabinet Office Behavioural Insights Team, 2012.
