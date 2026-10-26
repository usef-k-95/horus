# Political calendar mapping

A dated map of the events that open or close windows for a decision: elections, cabinet reshuffles, budget cycles, legislative sessions, court dates, international summits, anniversaries and the decision maker's own commitments. Horus uses it to time gates, sequence recommendations and avoid landing a proposal in a week when nobody can decide.

When Horus uses this: P1 workplanning on every pathway, refreshed at every gate; P5 sequencing of the implementation and communication plans.

## What it is

Kingdon's agenda-setting work established that policy change happens when problems, solutions and politics align in a window that opens briefly and predictably around scheduled events or unpredictably around crises. The political calendar operationalises the predictable half. It lists, for the engagement horizon and the implementation horizon, every scheduled event that changes who can decide, what they will attend to, and what can be said in public: the fiscal calendar (budget circular, submission deadlines, parliamentary vote), the legislative calendar (sessions, committee slots, recess), the electoral and appointment calendar (elections at every level, term limits, expected reshuffles, retirements), the judicial calendar (pending cases), the international calendar (summits, reviews by the IMF, OECD or EU, donor missions, treaty deadlines) and the symbolic calendar (anniversaries, national days, party conferences). Each event is tagged by its effect: window opens, window closes, attention diverted, veto players change.

## When Horus uses it

- P1: gate dates in the workplan are set against the calendar so the final recommendation lands when the decision maker can act and the budget cycle can fund it.
- P2: the decision-maker lens records the decider's personal calendar (speeches, trips, commitments made) from the profile.
- P3 to P4: options are screened for whether their legal route fits the available legislative windows; phasing is designed around them.
- P5: the implementation plan's sequencing and the communication plan's timing follow the calendar; the decision memo states timing as a date, as ministerial-submission conventions require.
- Transformation pathway: trajectories are anchored to reporting and election dates by which results must be visible.

## Steps

1. **Set the horizons**: the engagement (to AP5) and the implementation period (usually to the next election or beyond).
2. **Collect scheduled events** from official sources: fiscal calendar, legislative schedule, electoral commission, court lists, international organisations' mission schedules, party calendars. Record the source for each date.
3. **Add the decision maker's calendar** from the profile: speeches, travel, commitments, personal deadlines (an end of term, a candidacy).
4. **Tag each event** with its effect on the decision and the actors it changes.
5. **Identify windows**: periods when the D is available, the budget can be adjusted, parliament can legislate and attention is not consumed by something larger.
6. **Align the workplan**: gate dates inside windows; pre-reads before recess; avoid election periods for public consultation unless required.
7. **Design sequencing**: which decision must be taken by which date for which instrument; what can be done by decree before an election and what must wait.
8. **Maintain**: dates move; the calendar is reviewed at every PM check-in.

## Outputs → state records

- `profiles.political_calendar[] {event, date, relevance}` for the decision maker and the client entity; `analyses` of kind `decision_maker_lens` with `calendar[]`.
- The engagement-level calendar as an `analyses` record of kind `other` with the dated table in `narrative_path`, and `workplan.milestones[]` and `workplan.gates[]` dated against it.
- `brief.constraints[]` of kind `timing` where the calendar fixes a hard date.
- `options.design_parameters[]` for phasing choices driven by windows; `appraisals.feasibility.political.note`.
- `implementation_plan.content.sequencing[] {phase, actions, owners, dates}` and `instruments_required[]` with the session or budget cycle each needs.
- `communication_plan.content.sequencing[]` and `audiences[].timing`.
- `risks` of scope `political` for window-closing events, with `early_warning` dates.

## Pitfalls

- Listing elections only; budget and legislative calendars decide more recommendations than elections do.
- Planning the final readout for a date the decision maker is abroad or parliament is in recess.
- Ignoring the implementation horizon; a recommendation that needs three legislative sessions must say so.
- Dates without sources; the calendar is evidence and is cited like any other.
- Treating the calendar as destiny; crises open unscheduled windows, and the plan should say what Horus would advise if one opens.

## Source

John W. Kingdon, Agendas, Alternatives, and Public Policies, Little, Brown, 1984 (policy windows); Horus practice drawing on World Bank problem-driven political economy analysis (Fritz, Levy and Ort, 2014) and ministerial-submission conventions on timing (BENCHMARKS.md C1).
