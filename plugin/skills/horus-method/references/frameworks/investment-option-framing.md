# Investment option framing

The Green Book's long-list method for investment: generate options along five dimensions (scope, service solution, delivery, implementation, funding), filter them, and carry a shortlist that always includes business as usual, a do-minimum and a preferred way forward with more and less ambitious variants. Horus uses it so that business cases compare real alternatives, not a single scheme against nothing.

When Horus uses this: P3 option generation on the public investment and business case pathway; P4 to structure the economic case.

## What it is

The options framework filter in Green Book chapter 4 asks, in order: what is the scope of the intervention (how much of the problem to address, for whom); what service solution meets the need (technology, approach); how it is delivered (in-house, outsourced, partnership); how it is implemented (phasing, big-bang, pilot); and how it is funded (public, user charges, private finance). At each dimension options are generated and filtered on the SMART objectives and critical success factors, so the long list narrows systematically. The shortlist for appraisal must include business as usual (the reference case), a do-minimum (the least intervention that meets the critical success factors), the preferred way forward and, where helpful, a more ambitious and a less ambitious variant. The same structure organises the appraisal summary table.

## When Horus uses it

- Public investment pathway anchor option logic: no business case passes the AP3 gate without the five-dimension long list and a shortlist with business as usual and do-minimum.
- Programme pathway when a programme needs funding approval: scope and delivery options for the programme.
- Transformation pathway when delivery interventions require capital (systems, facilities).
- Strategy pathway for the costing of initiatives: scope variants give the order-of-magnitude range.

## Steps

1. **Fix the objectives and critical success factors** from the strategic case: strategic fit, value for money, achievability, supply-side capacity, affordability.
2. **Scope options.** From the narrowest (one region, one group, one service line) to the fullest; include the status quo scope.
3. **Service solution options.** Alternative ways to meet the need, including non-asset solutions (demand management, regulation, digital alternatives) before new build.
4. **Delivery options.** Public delivery, outsourcing, partnership, shared service, concession.
5. **Implementation options.** Phased, pilot first, big-bang; timing relative to dependencies.
6. **Funding options.** Appropriation, user charges, private finance, grant or development finance; note the fiscal rules each triggers.
7. **Filter** at each dimension against the critical success factors; record discarded options with reasons; combine surviving choices into coherent whole options.
8. **Name the shortlist**: business as usual, do-minimum, preferred way forward, plus more and less ambitious variants as needed; confirm with the client at AP3.
9. **Describe each shortlisted option** to the same depth: scope, outputs, costs by year, benefits by stream, risks, delivery route.

## Outputs → state records

- `options` of kind `investment_option` with `design_parameters[]` for the five dimensions, `variants[]` (do-minimum, intermediate, do-maximum), `status` from `long_list` to `short_list`, and a `do_nothing` option describing business as usual.
- `options.screening` with the critical success factors as `criteria[]`; `analyses` of kind `options_screening`.
- `analyses` of kind `strategic_case` and `baseline` referenced by `appraisals.baseline`.
- `assumptions` (`category: cost`, `demographic`, `financial`) for scope and demand parameters.
- `appraisals` of kind `business_case` with `five_case.economic` holding the appraisal summary table path and `summary {npv, bcr}` per option.
- `deliverables` of type `business_case` and `appraisal_summary_table`; the `financing_options_paper` from the funding dimension.

## Pitfalls

- A single scheme compared with doing nothing; the Green Book's shortlist rule exists to prevent this.
- Do-minimum defined as "nothing" rather than the least action that meets the critical success factors.
- Scope creep between options: each option must be described at the same depth and price base.
- Funding chosen before the economic case; the funding dimension affects affordability, not value for money.
- Filtering on affordability too early and losing the option that would have been best value.

## Source

HM Treasury, The Green Book, 2022 edition, chapter 4 (generating options and long-list appraisal) and the Five Case Model guidance; superseded by the Green Book 2026 (BENCHMARKS.md B6).
