# Policy packaging and sequencing

The design step that turns a preferred option into a package that can be adopted: combining complementary instruments, pairing losers' compensation with winners' gains, phasing obligations, and ordering decisions and instruments against capacity and the political calendar. Horus uses it between appraisal and recommendation on every pathway.

When Horus uses this: P3 to design package options, P4 to appraise them as options in their own right, P5 to write the implementation plan's sequencing.

## What it is

Single instruments rarely survive contact with politics or implementation. Packaging combines instruments so that the whole is adoptable: a mandate with a transition grant and free tooling; a tariff cut with retraining; an agency merger with ring-fenced budgets for the losing ministry; a reform with a visible early benefit for the public. Sequencing orders the elements in time so that each step builds capacity, legitimacy and coalition for the next, and so that reversible or low-regret steps precede irreversible ones. The political-economy literature on reform (Williamson on the political economy of adjustment, Rodrik on sequencing and complementarities, the World Bank's problem-driven analysis) and Bardach's instruction to "confront the trade-offs" and then "narrow and decide" are the intellectual sources; the operational form is a package option with its own theory of change, appraised against its components.

## When Horus uses it

- Every pathway at P3, once shortlisted options and the reaction matrix exist: packages are generated where a single option faces a blocking reaction that compensation or phasing could convert.
- Regulatory pathway: phasing by firm size, grace periods, free compliance tools, sunset and review clauses.
- Institutional pathway: transition paths with quick wins before legal change.
- Transformation pathway: the order of interventions along the delivery chain and the trajectory.
- Public investment and programme pathways: phased scope and pilots before full roll-out.
- P5: the sequencing block of the implementation plan and the timing in the decision memo.

## Steps

1. **Start from the reaction matrix**: for each shortlisted option, who resists or blocks and why; what each needs to move to conditional support.
2. **Generate complements**: instruments that address the blocker's concern without destroying the option's effect (compensation, phasing, exemptions with conditions, capacity support, information).
3. **Compose packages** as options in their own right with members, a theory of change and the trade-off made explicit (what effect is given up for what feasibility).
4. **Sequence**: order elements by dependency (legal before administrative), by capacity (build before mandate), by legitimacy (visible benefit before cost), by reversibility (pilots and reviewable steps first) and by the political calendar (windows and veto-player changes).
5. **Appraise the package** against its best single component on the same baseline and assumptions; quantify the cost of the compensation elements.
6. **Pre-test** the package against the reaction matrix and, where possible, in interviews with the pivotal actors.
7. **Write the sequence** as dated steps with instruments, owners and the decision each requires.

## Outputs → state records

- `options` of kind `package` with `package_members[]`, `mechanism`, `design_parameters[]` (phasing, exemptions, compensation) and `status`.
- `analyses` of kind `stakeholder_reaction_matrix` updated with the package as a column; `stakeholders.predicted_reactions[]` targeting the package.
- `appraisals` for the package (same `kind` as the pathway) with `impacts[]` including `fiscal_cost` of compensation and `distributional` effects; `summary.verdict`.
- `decisions` of kind `political_directive` where the client fixes a packaging constraint, and `preferred_option` when the package is chosen.
- `analyses` of kind `implementation_plan` with `sequencing[] {phase, actions, owners, dates}` and `instruments_required[]`.
- `risks` of scope `political` and `implementation` for sequence dependencies.

## Pitfalls

- Compensation that costs more than the reform yields; appraise the package, not the headline option.
- Phasing so long that the benefit never arrives inside anyone's term; set the first visible result early.
- Sequencing by administrative convenience rather than by coalition logic.
- Packages that bundle unrelated measures to buy votes; scrutiny bodies and the public see through omnibus bundles.
- Recording the package informally; it must be an option record so the appraisal and traceability hold.

## Source

Eugene Bardach and Eric M. Patashnik, A Practical Guide for Policy Analysis, 7th edition, 2023, steps 6 and 7 (BENCHMARKS.md B12); John Williamson (ed.), The Political Economy of Policy Reform, Institute for International Economics, 1994; Dani Rodrik, One Economics, Many Recipes, Princeton University Press, 2007.
