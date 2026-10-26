# Theory of change

An explicit causal chain from inputs through activities, outputs and outcomes to impact, with the assumptions that must hold at each step. Every Horus option carries one, so that appraisal, monitoring and evaluation test the same logic the recommendation rests on.

When Horus uses this: P3 option design on every pathway (mandatory per option), and P4 to P5 for monitoring and evaluation design.

## What it is

Theory of change originates in evaluation practice (Carol Weiss) and is now required in the UK Magenta Book, the UK impact-assessment template ("description of the proposed intervention and logical change process") and most donor appraisal formats. It states how and why an intervention is expected to work: the resources committed, what will be done, what will be produced, what will change for whom in the short and medium term, and what long-term impact follows. Between each link sit assumptions (about behaviour, capacity, context) and the evidence for them. A logic model is the diagram; the theory of change adds the reasoning and the assumptions. It is distinct from a logframe, which is the management matrix derived from it.

## When Horus uses it

- P3: each option on the long list gets a short theory of change; shortlisted options get a full one, which becomes the option's `mechanism`. Options without a credible mechanism are screened out.
- P4: appraisal quantifies the links (take-up, compliance, behavioural response) and treats the assumptions as sensitivity parameters.
- P5: monitoring indicators are placed on the chain (outputs early, outcomes later); the evaluation plan tests the weakest link.
- Programme and service design pathway anchor framework, paired with the logframe.
- Regulatory pathway: the RIA report's option section requires a theory of change per option.

## Steps

1. **State the impact** sought in the terms of the SMART objectives.
2. **Work backwards.** What outcomes (behaviour or condition changes among target groups) must occur for the impact; what outputs (products, services, rules, payments) must exist for those outcomes; what activities produce them; what inputs they need.
3. **Write the assumptions** at each link: who must act, with what capacity and incentive, under what external conditions. Mark each as evidence-based, expert judgement, client assertion or convention.
4. **Attach evidence.** For each link, the precedent or study that shows the link holding elsewhere, graded; where none exists, say so and treat the link as a hypothesis.
5. **Identify the critical path.** The one or two links whose failure breaks the option. These drive sensitivity analysis and the pilot design.
6. **Draw it.** One page: boxes left to right or bottom to top, assumptions in a parallel row, indicators marked.
7. **Use it in appraisal and monitoring.** Quantify links where data allow; place indicators; design the evaluation around the critical assumptions.

## Outputs → state records

- `options.mechanism` with `inputs`, `activities`, `outputs`, `outcomes`, `impacts` and `key_assumptions` linked to `assumptions` records.
- `assumptions` records (`category: behavioural`, `policy`, `technical`), each with `basis`, `source_note` and ranges for sensitivity.
- `hypotheses` of kind `option_effect` for unevidenced links, with `evidence_for` and `evidence_against`.
- `options.precedents[]` for links supported by other jurisdictions' experience.
- `appraisals.impacts[]` quantified along the chain; `appraisals.sensitivity.parameters` drawn from the key assumptions.
- `appraisals.monitoring.indicators[]` placed on outputs and outcomes; `monitoring.evaluation {when, method}`.
- Programme pathway: `appraisals.service.pilot_design` focused on the critical link.

## Pitfalls

- A chain of activities with no behavioural step; most policy fails because people did not respond as assumed.
- Assumptions left implicit, so the appraisal quantifies outputs and asserts outcomes.
- Confusing outputs (a portal launched) with outcomes (firms registered) and impact (compliance costs down).
- One theory of change for a package of options; each option and each variant needs its own.
- Treating it as a diagram exercise after the option is chosen rather than a design tool before.

## Source

Carol H. Weiss, "Nothing as Practical as Good Theory", in New Approaches to Evaluating Community Initiatives, Aspen Institute, 1995; HM Treasury, The Magenta Book: Central Government Guidance on Evaluation, 2020; the UK Impact Assessment template section 4 (BENCHMARKS.md B5).
