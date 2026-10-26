# WEF agile regulation toolkit

The World Economic Forum's toolkit for regulators facing fast-moving technologies: anticipatory, outcome-focused, experimental (sandboxes, advice, challenges), data-driven, self- and co-regulatory, joined-up and internationally coordinated approaches. Horus uses it to extend the regulatory long list when the subject is a new technology or business model that conventional rules would freeze.

When Horus uses this: P3 option generation on the regulatory pathway for digital, fintech, mobility, health-tech and similar fast-changing domains; P5 for review and sunset design.

## What it is

The 2018 "Agile Governance" white paper argued that policy-making cycles are slower than technology cycles and proposed governance that is adaptive, human-centred, inclusive and sustainable. The 2020 toolkit turns this into practice for regulators, with a chapter per approach, regulator case studies and "issues to consider" at the end of each. Anticipatory regulation uses horizon scanning and scenario work to prepare rules before harm materialises. Outcome-focused regulation sets the result and leaves the method to the regulated. Experimental approaches include regulatory sandboxes (time-limited, supervised exemptions), innovation advice services and challenge prizes. Data-driven regulation uses real-time reporting and supervisory technology. Self- and co-regulation delegates with safeguards. Joined-up regulation coordinates across regulators whose remits a new technology crosses. International cooperation aligns standards and mutual recognition.

## When Horus uses it

- Regulatory pathway when the baseline analysis shows the technology or market changes faster than the legislative cycle, or when the client is a regulator considering a sandbox.
- Strategy pathway for digital economy or innovation strategies, where the regulatory pillar needs an approach, not a rule.
- Institutional pathway when the question is how several regulators should coordinate on a cross-cutting technology (a joined-up or lead-regulator model).
- Complements Hood's typology and the OECD alternatives list; the toolkit's instruments are mostly nodality and authority tools used experimentally.

## Steps

1. **Characterise the pace and uncertainty**: how fast the technology and business models change; what harms are known, suspected and unknown; which regulators' remits are touched.
2. **Check the fit** of each agile approach: anticipatory where harms are foreseeable; outcome-focused where firms can innovate on means; sandbox where the rule's effect is uncertain and supervised testing is feasible; data-driven where real-time data exist; co-regulation where an industry body is credible; joined-up where remits overlap.
3. **Design the instrument** with its safeguards: eligibility and exit for a sandbox; the outcome metric and audit for outcome-focused rules; data standards and access rights for data-driven supervision; the statutory backstop for co-regulation.
4. **Build in learning**: review clauses, sunset dates, evaluation of the sandbox cohort, and the trigger that converts an experiment into a rule.
5. **Check capacity and legality**: whether the regulator can grant exemptions, has the data and skills, and can coordinate with peers; whether international obligations constrain the design.
6. **Appraise like any other option**, with attention to competition effects (sandbox participants can gain an advantage) and to consumer protection during experiments.

## Outputs → state records

- `options` of kind `regulatory_instrument` with `instrument_types[]` (`co_regulation`, `voluntary_or_standard`, `information_or_disclosure`, `regulation` with outcome-based parameters) and `design_parameters[]` for sandbox or review terms.
- `analyses` of kind `scenario_analysis` for anticipatory work; `benchmark` for regulator case studies.
- `appraisals.regulatory {review_clause, enforcement_strategy, competition_check}` and `impacts[]` on dimensions `innovation`, `competition`, `digital_and_data`, `consumer_welfare`.
- `appraisals.monitoring.evaluation {when, method}` for the experiment's evaluation.
- `implementation_plan.content.institutional_arrangements` for joined-up or lead-regulator coordination; `instruments_required[]` for exemption powers.
- `risks` of scope `legal` (vires for exemptions) and `policy_outcome` (consumer harm during trials).

## Pitfalls

- A sandbox with no exit, no evaluation and no path to a rule becomes a permanent exemption for incumbents' favourites.
- Outcome-focused rules without a measurable outcome or an audit capacity are unenforceable.
- Agile language used to delay necessary rules where harms are already evident.
- Ignoring the regulator's legal power to experiment; many need statutory authority first.
- Competition distortion between firms inside and outside the experiment, unaddressed in the appraisal.

## Source

World Economic Forum, Agile Regulation for the Fourth Industrial Revolution: A Toolkit for Regulators, December 2020; World Economic Forum, Agile Governance: Reimagining Policy-making in the Fourth Industrial Revolution, 2018 (both BENCHMARKS.md B10).
