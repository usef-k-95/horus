# IMF Public Investment Management Assessment (PIMA)

The IMF's framework for assessing how well a country plans, allocates and implements public investment: fifteen institutions in three phases, each scored on institutional design and effectiveness. Horus uses it to diagnose the public investment management system around a business case and to design institutional fixes where the pipeline, not the project, is the problem.

When Horus uses this: P2 on the public investment and business case pathway when the client's system for selecting and delivering projects is in question; P2 to P3 on the institutional pathway for public investment management bodies.

## What it is

PIMA, introduced in 2015 and updated in 2018, evaluates fifteen institutions. Planning: fiscal principles or rules; national and sectoral planning; coordination between entities (central and subnational, public corporations); project appraisal; alternative infrastructure financing (public-private partnerships, regulation of infrastructure companies). Allocation: multi-year budgeting; budget comprehensiveness and unity; budgeting for investment; maintenance funding; project selection. Implementation: procurement; availability of funding; portfolio management and oversight; management of project implementation; monitoring of public assets. Each institution is scored on design (the rules on paper) and effectiveness (practice), with cross-cutting assessments of legal framework, information systems and staff capacity. A climate module (C-PIMA, 2021) adds climate-aware planning, coordination, appraisal, budgeting and risk management. The IMF reports results in spider charts and a prioritised action plan. For Horus the framework is a diagnostic grid: a well-appraised project in a system with weak project selection and unreliable funding will still fail.

## When Horus uses it

- Public investment pathway: when the brief concerns a programme of projects, a pipeline, or an asset whose delivery depends on the system (multi-year budgeting, procurement, maintenance funding); the findings inform the management and financial cases and the risk register.
- Institutional pathway: the operating model of a public investment unit, a planning ministry or a PPP unit is diagnosed against the relevant institutions.
- Transformation pathway: delivery of a capital programme where the delivery chain runs through procurement and funding release.
- Benchmarking: published PIMA reports for comparator countries are grade-A sources for institutional comparison.

## Steps

1. **Scope**: which of the fifteen institutions bear on the client's problem; a full PIMA is an IMF mission, and Horus assesses the relevant subset.
2. **Collect the rules**: laws, budget regulations, planning documents, procurement rules, PPP frameworks; record them as legal and government documents.
3. **Collect the practice**: budget execution data, project selection records, procurement statistics, maintenance spending, asset registers; interview finance, planning and sector officials.
4. **Score design and effectiveness** per institution on a simple scale with the evidence and the gap between the two.
5. **Identify the binding constraints** for the client's project or programme: the institutions whose weakness most threatens delivery and value for money.
6. **Design responses**: institutional fixes (a gateway process, multi-year commitments, maintenance budget rules) as options or as conditions in the management case.
7. **Compare** with published PIMA results for comparator countries where available.

## Outputs → state records

- `analyses` of kind `institutional_diagnostic` with `content` organised by the fifteen institutions (design and effectiveness scores, evidence), `findings[]` on binding constraints, `limitations[]` on coverage.
- `documents` of kind `legislation`, `budget`, `regulation`; `evidence` of kind `legal_provision`, `statistic`, `finding`.
- `appraisals.five_case.management` and `financial` summaries citing system risks; `appraisals.feasibility.administrative`; `risks` of scope `fiscal` and `implementation`.
- `options` of kind `operating_model` or `delivery_intervention` for institutional fixes; `implementation_plan.content.instruments_required[]` (budget rules, decrees).
- `analyses` of kind `benchmark` using published PIMA reports as sources (`io_report`).

## Pitfalls

- Presenting a partial assessment as a PIMA; the IMF's is a formal product, and Horus's is a PIMA-informed diagnostic.
- Scoring design without effectiveness; the gap is the finding.
- Ignoring maintenance funding and asset monitoring, which decide whether the investment keeps delivering.
- Treating PPP frameworks as a financing fix when the appraisal and selection institutions are weak.
- Recommending a project in a system that cannot fund it predictably without saying so in the financial case.

## Source

International Monetary Fund, Public Investment Management Assessment: Review and Update, 2018; IMF, Strengthening Infrastructure Governance for Climate-Responsive Public Investment (C-PIMA), 2021. IMF document conventions are catalogued in BENCHMARKS.md B9.
