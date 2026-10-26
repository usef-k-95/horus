# ROAMEF cycle and the strategic case

The Green Book's policy cycle (Rationale, Objectives, Appraisal, Monitoring, Evaluation, Feedback) and its first product, the strategic case: a statement of the case for change, business as usual and SMART objectives that precedes any option. It is the spine of UK appraisal and the opening of the Five Case Model.

When Horus uses this: P1 to P2 on the public investment and business case pathway, and as the structure of the "rationale and objectives" sections of every RIA and strategy document.

## What it is

ROAMEF is the overarching policy framework in HM Treasury's Green Book. Rationale establishes why government should intervene at all (market failure, equity, legal duty, strategic objective). Objectives state what the intervention must achieve, in SMART form. Appraisal compares options against business as usual. Monitoring and Evaluation follow implementation; Feedback returns lessons to the next cycle. The strategic case, the first of the five cases, packages the first two steps for a decision maker: the strategic context, the case for change (the problem, its cost and consequences of inaction), the business-as-usual counterfactual, and no more than five or six SMART objectives with measurable benefits. Everything later in the appraisal must trace back to these objectives.

## When Horus uses it

- Public investment and business case pathway: the strategic case is the P2 diagnostic output and the first chapter of the business case deliverable. Nothing is appraised before it is agreed.
- Regulatory pathway: the "rationale for intervention" and "SMART objectives" sections of the RIA report follow the same logic (the UK IA template cross-references Green Book chapters).
- Strategy pathway: objectives and the business-as-usual projection give the "where we are" and "where we want to be" chapters a disciplined form.
- Any pathway at AP2: the strategic case is a convenient test of whether the diagnosis is complete enough to design options.

## Steps

1. **Rationale.** Name the market, institutional or equity failure and the legal or policy duty that justifies intervention. Say why this level of government and why now.
2. **Business as usual.** Project what happens if nothing new is done over the appraisal horizon: demand, cost, performance, risks. This is the baseline for every appraisal.
3. **Case for change.** Quantify the gap between business as usual and what the policy context requires; state the cost of inaction and who bears it.
4. **Objectives.** Write up to six SMART objectives (specific, measurable, achievable, relevant, time-bound). Each must have an indicator with a baseline and a target date. Objectives describe outcomes, not solutions.
5. **Constraints and dependencies.** Legal, fiscal, timing, interdependent programmes.
6. **Scope.** What is in and out, and the main stakeholders.
7. **Carry forward.** Objectives become the first appraisal criteria; the business-as-usual projection becomes the appraisal baseline; monitoring indicators are designed from the objectives now, not after the decision.

## Outputs → state records

- `analyses` record of kind `strategic_case` with `content` covering rationale, business as usual, case for change, objectives, constraints and scope; `findings[]` linked to `evidence`.
- `analyses` record of kind `baseline`, referenced by every `appraisals.baseline.analysis`.
- `brief.objectives[]` with `measurable: true` and `indicator`; revisions logged in a `brief` version.
- Business-as-usual parameters as `assumptions` (`category: macro`, `demographic`, `cost`), owned and agreed.
- `appraisals.monitoring.indicators[]` seeded from the objectives.
- For the business case deliverable: `appraisals.five_case.strategic` with `status` and `summary`.

## Pitfalls

- Objectives written as solutions ("build the new hospital") rather than outcomes ("reduce average waiting time to X by year Y").
- A business-as-usual projection that is a flat line; the counterfactual usually deteriorates or improves on its own.
- More than six objectives, which makes appraisal criteria unmanageable.
- Skipping the rationale because the client has already decided to intervene; reviewers and scrutiny bodies read this section first.
- Treating ROAMEF as linear; feedback from evaluation of past attempts belongs in the rationale.

## Source

HM Treasury, The Green Book: Central Government Guidance on Appraisal and Evaluation, 2022 edition, superseded by the Green Book 2026 (BENCHMARKS.md B6); cross-referenced in the UK Impact Assessment template (BENCHMARKS.md B5).
