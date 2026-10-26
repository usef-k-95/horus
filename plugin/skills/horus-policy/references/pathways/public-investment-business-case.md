# Public investment and business case pathway

Secure funding approval for a programme or asset. The method is the Green Book's strategic case and options framework, investment options from do-minimum to full scope, and the Five Case Model business case with social cost-benefit or cost-effectiveness analysis, optimism bias, sensitivity and affordability.

When Horus uses this: as the primary pathway when the decision is whether and how to fund a defined programme or asset through a treasury or board gateway (enum value `public_investment_business_case`); as a secondary pathway when a strategy, service design or delivery plan contains a capital component that needs approval.

## Classification signals

- The RFP concerns a programme, project or asset (infrastructure, systems, facilities, a multi-year programme) that needs an approval decision and a budget line, loan or grant.
- Language of business case, feasibility study, appraisal, value for money, affordability, financing, procurement, public-private partnership, gateway review, development finance.
- The client is a sponsor ministry or agency preparing a submission, a finance or planning ministry's gateway, a project unit, or a lender's counterpart.
- The required deliverable is a business case, an appraisal summary, a financing or procurement options paper, or inputs to a lender's project appraisal.
- Counter-signals: the pipeline or the investment system is the problem (institutional and operating model with IMF PIMA); the asset exists and underdelivers (transformation and delivery); the question is the service design the asset would host (programme and service design).

## Diagnostic lens

The strategic case. P2 produces, at `reviewed` before AP2:

- `analyses` of kind `strategic_case`: rationale for intervention, strategic fit, the case for change with the cost of inaction, business as usual, up to six SMART objectives, constraints and dependencies, scope.
- `analyses` of kind `baseline`: the business-as-usual projection of demand, need, cost and performance over the appraisal horizon; the reference case for every option.
- Demand and need analysis within the strategic case: current and projected demand by segment, capacity and condition of existing assets, service standards.
- The affordability envelope: the sponsor's and the finance ministry's budget constraints, fiscal rules and co-financing prospects, recorded as `assumptions` of category `financial`.
- `analyses` of kind `institutional_diagnostic` (PIMA-informed) where delivery depends on the public investment management system; `benchmark` for comparable projects' costs, benefits and outturns.
- Interviews: the sponsor, the finance ministry's appraisal and budget staff, the procurement authority, potential lenders or development partners, operators and users, affected communities.

Hypotheses are of kind `diagnostic` (the need and its scale), `option_effect` (benefit streams and their drivers), `implementation` (delivery and procurement capacity) and `political` (what the finance ministry and the legislature will fund).

## Option logic

Options are records of kind `investment_option`, generated with the Green Book options framework filter along five dimensions: scope (how much of the need to address, for whom), service solution (including non-asset solutions such as demand management, regulation or digital alternatives), delivery (in-house, outsourced, partnership, concession), implementation (phasing, pilot, big-bang) and funding (appropriation, user charges, private finance, grant or loan). Options are filtered at each dimension against the SMART objectives and critical success factors (strategic fit, value for money, achievability, supply-side capacity, affordability), with discarded options recorded. The shortlist always contains business as usual (as `do_nothing`), a do-minimum, the preferred way forward and, where useful, more and less ambitious variants. Each shortlisted option is described to the same depth: scope, outputs, costs by year, benefit streams, risks, delivery route, funding.

## Appraisal method

Appraisal kind `business_case`, `pathway: public_investment_business_case`.

- Standards applied: `HMT-Green-Book-2026` (and the 2022 edition where the build has not yet confirmed changes) and `Five-Case-Model`; `OMB-A4-2023` as method for the discount-rate justification and the accounting statement; `IMF-PIMA-2018` for institutional context; the client's or lender's appraisal manual where one applies, recorded alongside.
- Methodology: `cba` as the default for the economic case; `cea` where benefits cannot be credibly monetised; `proportionality_level` tied to the business-case stage (`standard` for strategic outline, `full` for outline).
- Toolkit modules: `cba` for discounting, NPV, benefit-cost ratio and payback over the agreed horizon; `fivecase` for the appraisal summary table, optimism-bias uplifts and affordability; `montecarlo` for probabilistic ranges and tornado charts on cost and demand; `distribution` for incidence by place and group with Green Book weights where justified; `scenarios` for demand scenarios; `cea` where used; `report` for the summary table and charts.
- Method-specific block, required: `five_case {strategic, economic (appraisal summary table path), commercial, financial (affordability), management}` each with `status` and `summary`, plus `optimism_bias_uplift`.
- Impact dimensions typically monetised or rated: `economic_output`, `fiscal_cost`, `fiscal_revenue`, `consumer_welfare`, `employment`, `environment`, `health_and_safety`, `distributional_equity`, `administrative_feasibility`.
- Common blocks: `baseline`, `impacts[]` with `present_value: true`, `summary {npv {central, low, high}, bcr}`, `distributional`, `feasibility`, `sensitivity {method: switching_values|monte_carlo}`, `risks` of scope `fiscal` and `implementation`, `monitoring` with benefits realisation indicators; `discount_rate` and `optimism_bias_uplift` as agreed `assumptions`.

## Stakeholder emphasis

The finance ministry's appraisal and budget functions (Agree or Decide on affordability; their manual is the binding standard); the sponsor and its minister; the procurement authority and the market of potential suppliers (commercial case); lenders and development finance institutions with their own appraisal requirements; operators who will run the asset; users and affected communities, including those displaced or disadvantaged (distributional); subnational governments where the asset sits; the legislature for multi-year commitments. The decision-maker lens tracks the budget calendar closely: a business case that misses the submission date waits a year.

## Core Tier-2 deliverables and structures

- `business_case` to strategic-outline or outline level: executive summary; strategic case; economic case with the appraisal summary table; commercial case; financial case; management case; recommendation and next approval stage; annexes (assumptions register, methods, sensitivity, optimism bias, distributional analysis, consultation).
- `appraisal_summary_table`: options in columns; monetised costs and benefits by stream in present value, NPV and BCR with ranges; unmonetised effects with direction and size; risks; affordability; the preferred option marked.
- `financing_options_paper`: funding sources and their conditions, procurement and delivery models, risk allocation, fiscal treatment and implications for fiscal rules, a recommended route and its approvals.
- `implementation_plan` and `communication_plan` annexes aligned to the management case.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification records the approval authority, the gateway stage sought and the submission date.
- AP1: frameworks selected include the strategic case, investment option framing and the Five Case Model; the finance ministry's appraisal staff are priority-1 interviewees; data requests cover demand, cost and asset condition.
- AP2: `strategic_case` and `baseline` at `reviewed` with business as usual projected and SMART objectives drafted; affordability envelope recorded as agreed assumptions.
- AP3: shortlist contains business as usual, a do-minimum and a preferred way forward, each described to the same depth; critical success factors confirmed as guiding principles; discount rate, price base year and optimism-bias approach agreed as `assumptions` with `status: agreed`.
- AP4: every shortlisted option has a `business_case` appraisal with NPV and BCR ranges (or cost-effectiveness ratios), optimism bias applied, switching values reported, affordability tested against the envelope; the economic case ranks options on the same baseline and assumptions register.
- AP5: `business_case`, `appraisal_summary_table` and `financing_options_paper` released; the management case names the delivery organisation, governance and benefits realisation plan; the next approval stage and its date are stated.

## Frameworks

Framing and diagnosis: `roamef-and-strategic-case`, `hypothesis-driven-problem-solving`, `institutional-diagnostic`, `theory-of-change`, `political-economy-analysis`. Stakeholders: `rapid-decision-rights`, `mendelow-power-interest`, `veto-players-and-coalitions`, `political-calendar`. Options: `investment-option-framing`, `international-benchmarking`, `operating-model-archetypes` (delivery models), `service-concept-design` (service solution dimension), `policy-packaging-and-sequencing`. Appraisal: `green-book-five-case-model`, `omb-circular-a4`, `cost-effectiveness-analysis`, `distributional-and-gender-impact`, `scenario-analysis`, `multi-criteria-analysis`, `pilot-and-evaluation-design`. Implementation and communication: `imf-pima`, `government-outcomes-lab`, `raci`, `logframe-and-dac-criteria`, `five-disciplines-government-transformation`, `pyramid-principle`, `scqa`, `cabinet-paper-conventions`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md B6 (HM Treasury Green Book 2022 and 2026; Five Case Model; discount schedule and optimism bias), B9 (IMF staff paper and board paper structures; PIMA), B7 (OMB Circular A-4 as method for discounting and uncertainty), B8 (World Bank project and policy document conventions), B13 (Government Outcomes Lab value-for-money toolkit), C1 to C4 (decision memo conventions, including financial impact in the issue statement). The catalogue flags published UK outline business cases as a gap to close before this pack is finalised, and requires the Green Book 2026 to be checked for discount-rate changes.

## Typical pitfalls

- A single scheme against doing nothing; the shortlist rule exists to prevent it.
- Economic and financial cases confused: society, real terms and discounting versus budget, nominal terms and cash.
- Optimism bias omitted or applied after sensitivity; benefits double counted across streams.
- Do-minimum defined as nothing rather than the least action meeting the critical success factors.
- Funding route chosen before value for money is established; private finance treated as free money.
- A management case that names no delivery organisation, or a project in a system that cannot release funding predictably, without saying so.
- Missing the budget calendar; timing is a date in the decision memo.
