# Deliverology and delivery units

Michael Barber's method from the UK Prime Minister's Delivery Unit (2001 to 2005): a small central team, a handful of priorities with targets and trajectories, delivery-chain analysis, routines (stocktakes, delivery reports, priority reviews) and relentless problem-solving. Horus uses it as the anchor method of the transformation and delivery pathway and as the template for delivery-unit set-up.

When Horus uses this: P2 to P5 on the transformation and delivery pathway; P5 on every pathway to design the routines in the implementation plan.

## What it is

Deliverology holds that most policies fail not in design but in the gap between announcement and front-line change, and that a disciplined routine closes it. The elements: a delivery unit of a few dozen people reporting to the head of government or minister, with no operational responsibility and strong analytical capacity; a small number of priorities with measurable targets; a trajectory per target; a delivery chain per priority; routines, meaning monthly or quarterly stocktakes chaired by the principal with the responsible minister and officials, regular delivery reports with a traffic-light assessment of likelihood of delivery, and priority reviews that diagnose problems in depth; problem-solving that treats slippage as a technical problem to be fixed rather than a blame event; and a culture of candour in which the unit tells the principal the truth early. Barber's later work (How to Run a Government, 2015) generalises the approach to any government and adds lessons on the unit's relationship with departments and the finance ministry.

## When Horus uses it

- Transformation and delivery pathway: the diagnosis uses delivery-chain analysis and performance data; options are delivery interventions and routines; the appraisal is trajectory-based; the delivery plan deliverable follows the method's structure (aspiration and targets, delivery chain and bottlenecks, interventions, trajectories, routines, roles and capability, risks).
- Delivery-unit set-up engagements: mandate, size, reporting line, priorities, routines and the relationship with ministries are the design parameters; the institutional pathway's operating-model appraisal applies.
- P5 on every pathway: the implementation plan specifies stocktake cadence, delivery reports and the owner of each KPI.
- Decision-maker lens: whether the principal will chair stocktakes is a feasibility question Horus asks early.

## Steps

1. **Choose the priorities**: few, measurable, owned by the principal; record the target and its baseline.
2. **Build trajectories** per target from baseline, interventions and lags.
3. **Map the delivery chain** per priority and score the links.
4. **Design interventions** per bottleneck, sized by their contribution to the trajectory.
5. **Set the routines**: stocktake cadence, attendees, format (trajectory, actuals, issues, decisions), delivery report template and rating rules, priority review triggers.
6. **Define the unit** (or the equivalent capacity in the client): mandate, reporting line, staffing and skills, data access, relationship with departments.
7. **Run the first cycle** with the client where the engagement allows; adjust routines on evidence.
8. **Build capability** in the departments so that routines survive the unit.

## Outputs → state records

- `analyses` of kind `delivery_chain` and `baseline`; `appraisals` of kind `delivery_intervention` with `delivery {trajectory, bottlenecks_addressed[], effort, dependencies[]}`.
- `options` of kind `delivery_intervention`; for unit set-up, `options` of kind `operating_model` appraised under `appraisals.operating_model`.
- `analyses` of kind `implementation_plan` with `kpis[]`, `institutional_arrangements` (the unit and the routines), `capacity_needs[]`, `sequencing[]`.
- `deliverables` of type `delivery_plan`, `dashboard_specification` and, for routines and stocktake design, `implementation_plan`; the capability plan within the delivery plan.
- `stakeholders.decision_role` for the stocktake chair (`decide`) and the responsible officials (`perform`).
- `risks` of scope `implementation` with `early_warning` tied to trajectory variance.

## Pitfalls

- Too many priorities; the method works with a handful.
- A delivery unit that takes over delivery or becomes a reporting bureaucracy; its job is analysis, routines and candour.
- Stocktakes without the principal; the routine loses its force.
- Traffic lights without trajectories, which turn into negotiation about colours.
- Importing the UK form without the client's political and administrative context; the routines must fit who can chair, who holds data and who controls budgets.

## Source

Michael Barber, Instruction to Deliver, Methuen, 2007; Michael Barber, Andy Moffit and Paul Kihn, Deliverology 101, Corwin, 2011; Michael Barber, How to Run a Government So That Citizens Benefit and Taxpayers Don't Go Crazy, Allen Lane, 2015. BENCHMARKS.md flags UK Prime Minister's Delivery Unit material as a benchmark gap to close.
