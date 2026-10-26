# RACI responsibility assignment

A responsibility assignment matrix listing activities or deliverables against roles and marking each role as Responsible (does the work), Accountable (owns the outcome, exactly one per activity), Consulted (two-way input before) or Informed (told after). Horus uses it to make implementation plans executable and to show the client who does what from day one.

When Horus uses this: P5 on every pathway in the implementation plan and the governance slide; P1 for the engagement's own governance between Horus, the Supervisor and the client.

## What it is

RACI is a project-management convention (the PMBOK Guide's responsibility assignment matrix is the generic form) for allocating roles across the tasks of a plan. Its rules are few and strict: every activity has exactly one Accountable role; Responsible roles actually perform the work and may be several; Consulted roles are asked before the activity is complete, which means they can delay; Informed roles are notified and cannot. Reading the matrix by column exposes overloaded roles and roles with accountability but no authority; reading by row exposes activities with nobody accountable or everybody consulted. RACI is about tasks and deliverables; RAPID is about decisions. Horus keeps both: RAPID for the critical decisions of the operating model, RACI for the activities of the implementation plan.

## When Horus uses it

- P5 implementation plan on every pathway: each sequenced action has an Accountable owner and Responsible performers; the governance and RACI slide archetype presents it.
- Transformation pathway: routines (who prepares the delivery report, who chairs the stocktake, who is consulted) are a RACI.
- Institutional pathway: the transition plan's workstreams (legal drafting, staff transfer, systems migration) and the operating-model blueprint's functions.
- Public investment pathway: the management case's delivery organisation.
- Engagement governance at P1: the approach's governance section is a RACI across client PM, sponsor, steering, Supervisor and Horus for each deliverable and gate.

## Steps

1. **List the activities** from the sequencing block of the implementation plan at a level where ownership is meaningful (ten to thirty rows for a plan).
2. **List the roles** as positions or bodies, not named individuals where possible, matched to stakeholder records.
3. **Assign A** first, one per row; where the client cannot name one, record the gap as a finding.
4. **Assign R**, then C, then I; keep C to the roles whose input is needed, so the plan is not paralysed by consultation.
5. **Read the columns**: overloaded roles, roles with A but no authority or budget, roles absent from every row that should be present.
6. **Validate with the client** at the final readout; convert agreed assignments into actions with owners and due dates for the first ninety days.
7. **Maintain**: the matrix is revised when the structure or the plan changes.

## Outputs → state records

- `analyses` of kind `implementation_plan` with `sequencing[] {phase, actions[], owners: → STK[], dates}`, `institutional_arrangements` (the governance structure) and the RACI table in `narrative_path` or as an artefact.
- `stakeholders` records for each role with `decision_role` and `relationships[]` (`oversees`, `reports_to`).
- `actions` of kind `internal_task` or `client_request_decision` for the first-ninety-days items, with `owner` and `due`.
- `risks.owner` and `appraisals.monitoring.indicators[].owner` aligned with the Accountable roles.
- `approach.governance` for engagement governance at P1.
- `deliverables`: the governance and RACI exhibit in the final deck; `governance_charter` on the institutional pathway.

## Pitfalls

- Several A's per row, or an A with no budget or authority over the R's.
- Everyone Consulted, which is a veto for everyone.
- Named individuals rather than roles, so the matrix dies at the next reshuffle.
- A RACI for the plan but none for the routines that keep it alive.
- Confusing RACI with RAPID and using it to describe who decides.

## Source

Project Management Institute, A Guide to the Project Management Body of Knowledge (PMBOK Guide), responsibility assignment matrix, successive editions; RACI is a widely used convention with no single canonical author.

## Proposed schema additions

- `analyses.content` for kind `implementation_plan`: an optional `raci[] {activity, accountable: → STK, responsible: → STK[], consulted: → STK[], informed: → STK[]}` block, so the matrix is queryable and the sensitivity audit can check roles against stakeholder records rather than reading a Markdown table.
