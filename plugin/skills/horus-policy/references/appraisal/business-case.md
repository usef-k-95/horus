# Business case: the Five Case Model

How Horus builds a business case to strategic outline or outline level using HM Treasury's Five Case Model: the strategic, economic, commercial, financial and management cases, the appraisal summary table, optimism bias and affordability.

When Horus uses this: public investment and business case pathway, phase P4 (economic case) and P5 (commercial, financial and management cases to the level the stage requires), appraisal kind `business_case`; also when another pathway's preferred option needs funding approval through a business-case process.

## Stages and what Horus delivers

The **strategic outline case** (SOC) establishes the case for change and the spending objectives, and reduces a long list to a short list with indicative costs; the other cases are in outline. The **outline business case** (OBC) identifies the preferred option through full appraisal of the short list, sets the procurement route and confirms affordability and deliverability. The **full business case** follows procurement and is outside a normal Horus engagement. Horus delivers SOC and OBC; `five_case.<case>.status` records how far each case has been developed and `summary` carries its one-paragraph answer. The Tier 2 document follows the Green Book order: executive summary, strategic, economic (with the appraisal summary table), commercial, financial and management cases, recommendation and next approval stage, annexes.

## Strategic case

The case for change: the strategic context and the policies the investment serves; the business-as-usual position and why it is not acceptable (the `strategic_case` analysis and the baseline); the spending objectives, no more than five or six, SMART and traceable to `brief.objectives`; the scope; the main benefits, risks, constraints and dependencies. The strategic case is the test every later option is screened against: an option that does not meet the spending objectives is not an option. Record a summary and status in `five_case.strategic`.

## Economic case

The core of P4. The long list is generated with the Green Book options framework filter (scope, solution, delivery, implementation, funding) and screened against critical success factors to a short list that always includes business as usual (`do_nothing`) and a do-minimum (`option-design.md`). For each shortlisted option:

- Costs and benefits to society in real terms, excluding transfers (VAT, grants between public bodies) and including non-market values where a defensible method exists; valuation sources are `assumptions` with `basis: evidence`.
- Discounting at the social time preference rate (`cba.cba(benefits, costs, "green_book")`; health effects with `green_book_health`), giving net present social value, benefit-cost ratio and payback year from `CBAResult`.
- Optimism bias applied to costs before discounting (below).
- Unmonetised costs and benefits listed and rated, never dropped.
- Sensitivity: switching values on the main cost and benefit drivers (`montecarlo.switching_value`), scenarios, and Monte Carlo at `full` proportionality (`ria.md` gives the calls).
- Distributional analysis: who gains and who pays, by income group or place, with `distribution.incidence`; the Green Book's distributional weights where the client applies them, recorded as an assumption.

Results are presented in the **appraisal summary table**, one row per option: present value of costs, present value of benefits, net present social value, BCR, unmonetised benefits and costs, key risks, affordability note and rank. The analyst builds it with `fivecase.appraisal_summary_table([fivecase.OptionAppraisal(option, cba_result, unmonetised_benefits, unmonetised_costs, risks, affordability_note)])`, which also adds `rank_by_npsv`, writes it with `report.write_csv` and `report.markdown_table`, and records the path in `five_case.economic` (the schema places the table path there). The preferred option is the one with the highest net present social value unless unmonetised effects, risk or affordability justify otherwise, and the justification is written down.

## Optimism bias

Appraisers systematically underestimate costs and durations and overestimate benefits. The Green Book requires an explicit uplift to cost estimates, starting from the upper-bound percentages in its supplementary guidance by project type (standard and non-standard buildings, standard and non-standard civil engineering, equipment and development, outsourcing) and reducing it as risks are identified, quantified and mitigated and as the estimate matures. `fivecase.OPTIMISM_BIAS_UPPER` holds illustrative upper bounds and `fivecase.apply_optimism_bias(cost, uplift)` applies one; the analyst takes the actual percentage from the current guidance, records it as an `assumptions` record with the mitigation argument, applies it before discounting and writes it to `five_case.optimism_bias_uplift`. Where the client has its own evidence of over-runs on comparable projects, use that evidence and say so. Benefits are not uplifted; where benefit optimism is a concern, shade the benefit range downwards and show the effect in sensitivity.

## Commercial case

Can the preferred option be procured and contracted? Procurement route and strategy, the market's capacity to deliver, risk allocation between the public body and suppliers (a table of risks and who bears them), payment mechanism, contract length and key terms, and the accounting treatment. At SOC this is a short statement of the likely route; at OBC it is a procurement strategy. Record a summary and status in `five_case.commercial`.

## Financial case and affordability

The financial case answers a different question from the economic case: not whether the option is worth it to society but whether the organisation can pay for it. Costs are in nominal cash terms, including VAT and transfers, year by year over the life of the asset or programme, split capital and revenue, set against the agreed budget envelope and funding sources (own budget, central allocation, external finance, user charges), with the funding gap by year shown explicitly and the balance-sheet and income-statement effects noted. `cba.real_from_nominal` converts between the two bases; keep both in the model and label every table with its base. Affordability is confirmed, conditional or not confirmed, and `five_case.financial` says which, with the gap and the proposed treatment. An unaffordable preferred option is presented as such, with the affordable alternative beside it.

## Management case

Can it be delivered? Governance (senior responsible owner, programme board), the programme and project management approach, the plan and milestones, the benefits realisation plan (who owns each benefit, how it is measured, when), risk management arrangements, change and stakeholder management, contract management, and the monitoring and post-implementation evaluation plan (the Green Book expects evaluation to be designed now). Record a summary and status in `five_case.management`; the implementation plan analysis (`implementation-planning.md`) supplies the detail.

## Common blocks and the `five_case` block

Common blocks as for every appraisal: `baseline`, `impacts` by dimension with affected groups, `summary` (`npv` with central, low and high, `bcr`, `rank`, `verdict`), `distributional`, `feasibility`, `sensitivity`, `risks`, `monitoring`, `caveats`, `artefacts` (the model, the appraisal summary table CSV, charts). The `five_case` block holds `strategic`, `economic`, `commercial`, `financial` and `management`, each with `status` and `summary` (the economic case also carries the appraisal summary table path), and `optimism_bias_uplift`.

## Pitfalls

Mixing real and nominal money across cases; counting transfers as social benefits; a do-minimum that is do-nothing with a new name; optimism bias omitted or applied after discounting; benefits no one owns in the management case; an affordability test run on the economic case's numbers; a short list reverse-engineered from the preferred option; evaluation designed after the money is spent.

Proposed schema additions: fix the enumeration for `five_case.<case>.status` (for example `outline`, `developed`, `complete`) so the stage reached is machine-checkable at AP4 and AP5.

Source: HM Treasury, The Green Book (2022; check the 2026 edition for changes to the discount-rate schedule and optimism-bias guidance); HM Treasury, Guide to Developing the Project Business Case and Guide to Developing the Programme Business Case (2018); HM Treasury supplementary guidance on optimism bias; IMF Public Investment Management Assessment framework for the institutional context.
