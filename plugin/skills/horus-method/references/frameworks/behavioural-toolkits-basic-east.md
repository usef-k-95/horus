# Behavioural toolkits: OECD BASIC and BIT EAST

Two practical frameworks for designing behaviourally informed policy. The Behavioural Insights Team's EAST says make it Easy, Attractive, Social and Timely. The OECD's BASIC gives a project process: Behaviour, Analysis, Strategy, Intervention, Change, with an ethics layer. Horus uses EAST to generate behavioural options and BASIC to run the analysis and testing properly.

When Horus uses this: P2 to P4 on the programme and service design pathway (anchor), and on the regulatory pathway when compliance or take-up depends on behaviour.

## What it is

EAST (2014) distils the UK Behavioural Insights Team's field experience into four design heuristics. Easy: reduce friction, use defaults, simplify messages. Attractive: draw attention, design incentives and lotteries, personalise. Social: show what most people do, use networks and commitments, encourage reciprocity. Timely: prompt at the moment of decision, address immediate costs and benefits, help plan. BASIC (2019) is the OECD's end-to-end process for applying behavioural insights with rigour and ethics. Behaviour: identify and scope the behavioural problem and the target behaviour. Analysis: diagnose the behavioural drivers (attention, belief formation, choice, determination) with evidence. Strategy: generate behaviourally informed strategies from the diagnosis. Intervention: design and test, preferably through randomised trials. Change: scale, monitor and sustain, with ethical review throughout. BASIC replaced and generalised MINDSPACE (2010) as the OECD's reference.

## When Horus uses it

- Programme and service design pathway: eligibility, enrolment, take-up and persistence are behavioural problems; EAST produces the design levers and BASIC the pilot design.
- Regulatory pathway: compliance design (defaults, prompts, simplified forms, disclosure formats) as an instrument type of its own (`behavioural_nudge`) and as a complement to mandates. Behavioural instruments are among the OECD alternatives to regulation.
- Transformation pathway: front-line behaviour of delivery actors (data returns, referral practices) can be addressed with the same tools.
- Communication planning: EAST shapes messages and timing for citizen-facing communication.

## Steps

1. **Behaviour.** Specify the target behaviour precisely: who, does what, when, how often; and the current rate from data.
2. **Analysis.** Map the journey to the behaviour; identify frictions and biases at each step with evidence from data, user research and literature; distinguish ability, motivation and opportunity barriers.
3. **Strategy.** For each barrier generate options with EAST: what makes the behaviour easier, more attractive, more social, better timed. Combine into two or three coherent intervention designs.
4. **Intervention.** Specify the design parameters (default, message, channel, timing, incentive), the comparison group and the outcome measure; prefer a randomised pilot where feasible and ethical, otherwise a strong quasi-experimental design.
5. **Change.** Plan scaling with monitoring of the behaviour over time, decay checks and an ethics review (transparency, autonomy, who benefits).
6. **Record effect sizes** as ranges from precedents until the pilot reports, and mark them indicative.

## Outputs → state records

- `analyses` of kind `user_and_service_research` with the behavioural diagnosis (journey, barriers, drivers) and `findings[]` linked to evidence.
- `options` of kind `service_concept` or `regulatory_instrument` with `instrument_types: [behavioural_nudge, information_or_disclosure]`, `design_parameters[]` (the EAST levers) and `mechanism`.
- `assumptions` of `category: behavioural` for take-up and response rates, with `low` and `high` from precedents and `basis`.
- `options.precedents[]` for trials elsewhere, with evidence.
- `appraisals.service {take_up_estimate, pilot_design {design, sample, duration, evaluation_method}}`; on the regulatory pathway, `appraisals.impacts[]` with dimension `administrative_burden` or `business_compliance_cost`.
- `risks` of scope `policy_outcome` for behavioural assumptions that fail.

## Pitfalls

- Nudging around a structural problem; if the service is unusable or the incentive is wrong, no message fixes it.
- Importing effect sizes from another country as point estimates; context changes them, so use ranges and pilot.
- Ethics as an afterthought; BASIC's ethical checks apply at every stage and the sensitivity audit will ask.
- Testing one message against nothing; test against the current practice and against a simplified-form alternative.
- Treating behavioural instruments as a substitute for enforcement when the problem is deliberate non-compliance.

## Source

Behavioural Insights Team, EAST: Four Simple Ways to Apply Behavioural Insights, 2014; OECD, Tools and Ethics for Applied Behavioural Insights: The BASIC Toolkit, 2019; predecessor Institute for Government and Cabinet Office, MINDSPACE, 2010.
