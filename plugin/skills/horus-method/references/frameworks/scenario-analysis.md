# Scenario analysis

A method for testing options against several plausible futures rather than one forecast: identify the driving forces and critical uncertainties, build three or four internally consistent scenarios, and assess how each option performs in each. Horus uses it to stress-test strategies and to structure uncertainty in appraisals where a single central case would mislead.

When Horus uses this: P2 situational analysis and P4 appraisal on the strategy pathway (anchor); P4 on any pathway as the `scenarios` sensitivity method; the toolkit's `scenarios` module implements the quantitative part.

## What it is

Scenario planning as practised at Shell (Pierre Wack) and codified by Peter Schwartz builds a small set of coherent stories about how the external environment could develop, each driven by a different resolution of the two or three uncertainties that matter most, with predetermined trends common to all. Scenarios are not forecasts and are not assigned probabilities in the classic method; their job is to widen the decision maker's view and to reveal which options are robust (perform acceptably in all scenarios), which are bets (perform well in one) and which hedges or triggers would allow adaptation. In appraisal, scenario analysis is one of the Green Book's and A-4's recognised treatments of uncertainty alongside sensitivity and switching values and Monte Carlo simulation; the Horus schema records it as `sensitivity.method: scenarios` with results per scenario.

## When Horus uses it

- Strategy pathway: scenarios frame the "where we are heading" part of the diagnosis and provide the stress test in the strategic options appraisal (`strategic.scenario_results[]`).
- Regulatory pathway for fast-moving markets: anticipatory regulation (WEF toolkit) starts with scenarios.
- Public investment pathway: demand scenarios for the economic case, with optimism bias applied separately.
- Transformation pathway: trajectory scenarios (baseline, intervention, downside).
- Communication: scenarios are a non-confrontational way to raise a risk the decision maker does not want to hear.

## Steps

1. **Fix the focal question and horizon**: the decision the scenarios must inform and the period over which it plays out.
2. **List driving forces**: economic, demographic, technological, political, environmental, with evidence on their trends.
3. **Separate predetermined elements from critical uncertainties**; rank uncertainties by impact on the decision and by unpredictability.
4. **Choose the scenario logic**: two critical uncertainties as axes (four scenarios) or three distinct narratives; name them neutrally.
5. **Write the scenarios**: a coherent narrative and a parameter set for each (growth, prices, demand, technology adoption, political configuration), with the evidence that makes each plausible.
6. **Assess options** in each scenario on the agreed criteria; identify robust options, bets, and the signposts that would indicate which scenario is unfolding.
7. **Design hedges and triggers**: option elements that preserve flexibility; review points tied to signposts.
8. **Report** a scenario-by-option matrix with the quantitative results from the toolkit and a short narrative per scenario.

## Outputs → state records

- `analyses` of kind `scenario_analysis` with `content` holding driving forces, uncertainties, scenario narratives and parameter sets, signposts; `findings[]` and `limitations[]`.
- `assumptions` with scenario-specific values (`low`, `high`, or a `distribution`) for the parameters that differ across scenarios, `basis` recorded.
- `appraisals.sensitivity {method: scenarios, parameters: → ASM[], results_path, robustness: robust|sensitive_to[]|fragile}` and, for strategic appraisals, `appraisals.strategic.scenario_results[] {scenario, performance}`.
- `options.design_parameters[]` for hedges and triggers; `appraisals.monitoring.indicators[]` for signposts.
- `risks` of scope `policy_outcome` or `fiscal` for downside scenarios, with `early_warning`.
- `artefacts[]`: scenario parameter tables and result charts.

## Pitfalls

- Scenarios that are a central case plus or minus ten per cent; they must differ in logic, not just in magnitude.
- Four scenarios of which one is "the one we believe"; the decision maker then ignores the rest.
- Mixing scenario analysis with optimism bias and Monte Carlo without saying which uncertainty each handles.
- No signposts or triggers, so the scenarios inform nothing after the decision.
- Scenario narratives built on forecasts of a single institution; triangulate drivers across sources.

## Source

Pierre Wack, "Scenarios: Uncharted Waters Ahead", Harvard Business Review, September to October 1985; Peter Schwartz, The Art of the Long View, Doubleday, 1991; HM Treasury, The Green Book, uncertainty and optimism-bias annex (BENCHMARKS.md B6); US OMB Circular A-4, 2023, treatment of uncertainty (BENCHMARKS.md B7).
