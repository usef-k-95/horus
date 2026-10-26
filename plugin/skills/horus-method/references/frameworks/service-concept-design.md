# Service concept and channel design

A method for designing a public service around the user's journey: define the outcome and the users, map the current journey, design the service concept (what the user gets, through which channels, with what eligibility and support), and draw the service blueprint that shows front-stage interactions and back-stage processes. Horus uses it to generate and specify service options on the programme and service design pathway.

When Horus uses this: P2 user research and P3 option generation on the programme and service design pathway; P5 for the service blueprint deliverable.

## What it is

Service blueprinting (Lynn Shostack, 1984) lays out a service as a diagram with the user's actions on top, the visible front-stage actions of staff and systems below the line of interaction, the back-stage actions below the line of visibility, and the supporting processes below the line of internal interaction. Government service standards (the UK Government Service Standard, 14 points, and the Australian Digital Service Standard) add the design practice: understand users and their needs, solve a whole problem, make the service simple to use and accessible, iterate, use data, define what success looks like and measure it. A service concept is the proposition in a paragraph: who is eligible, what they receive, how they access it (channels), what support exists for those who cannot use the default channel, how identity and eligibility are verified, and what happens when something goes wrong. Channel design chooses the mix of digital, assisted digital, telephone, face-to-face and intermediary channels, with the cost to serve and the reach of each.

## When Horus uses it

- Programme and service design pathway anchor option logic: the long list is a set of service concepts differing on eligibility, benefit design, channel mix, intermediaries and behavioural design.
- Regulatory pathway for compliance services (registration, licensing, reporting portals) where the regulated party is the user.
- Transformation pathway when a front-line service is the bottleneck.
- Public investment pathway for the service solution dimension of option framing.

## Steps

1. **Define users and outcomes**: segments (by need, capability, channel access), the outcome sought for each, and the measure.
2. **Research the current journey**: steps, time, cost to the user, failure points, drop-off rates, cost to serve; combine administrative data with interviews and observation. Record evidence grade.
3. **Write the service concept** for each option: eligibility and verification; the benefit or service; channels and assisted routes; intermediaries; redress and exceptions.
4. **Design the channel mix** with the cost to serve and reach of each channel, and the behavioural levers at each step (defaults, prompts, simplification).
5. **Draw the blueprint**: user actions, front-stage, back-stage, support processes; mark the moments that decide take-up and the hand-offs that carry risk.
6. **Estimate take-up and cost per outcome** from precedents and the journey analysis, as ranges.
7. **Design the pilot**: which concept elements to test, with whom, measured how.
8. **Specify the operating and cost model** for the chosen concept.

## Outputs → state records

- `analyses` of kind `user_and_service_research` with the journey, segments, failure points and cost to serve; `findings[]` with evidence.
- `options` of kind `service_concept` with `target_groups[]`, `design_parameters[]` (eligibility, benefit, channel mix, intermediaries, behavioural levers), `mechanism` and `precedents[]`.
- `assumptions` of `category: behavioural` (take-up) and `cost` (cost to serve by channel).
- `appraisals` of kind `service_concept` with `service {outcomes[], take_up_estimate, cost_per_outcome, equity_assessment, pilot_design}` and `distributional`.
- `deliverables` of type `service_design_document`, `service_blueprint` and `pilot_evaluation_plan`; cost-to-serve summary within the design document.
- `implementation_plan.content.delivery_chain[]` from the back-stage view.

## Pitfalls

- Designing for the median user; the segments that fail are those without digital access, documents or literacy, and equity depends on them.
- A digital-only channel strategy justified by cost to serve, without assisted routes.
- Blueprints that stop at the front stage; the back-stage hand-offs are where delivery fails.
- Take-up assumed at 100 per cent of the eligible population; use precedents and show the range.
- Skipping user research because the client "knows the users"; the standard requires evidence.

## Source

G. Lynn Shostack, "Designing Services That Deliver", Harvard Business Review, January to February 1984; UK Government Digital Service, Government Service Standard, 2019; Australian Digital Transformation Agency, Digital Service Standard. Benchmark entries for these are flagged as gaps in BENCHMARKS.md.
