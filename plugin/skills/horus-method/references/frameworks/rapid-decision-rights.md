# RAPID decision rights

Bain's RAPID assigns five roles to each decision: Recommend, Agree, Perform, Input and Decide (the "D"). Horus uses it to find out who really decides on the client side, to design governance in operating-model options, and to diagnose institutions where decisions stall.

When Horus uses this: P0 to P1 to identify the ultimate decision maker on every pathway; P2 to P4 as a design and diagnostic tool on the institutional and operating-model pathway.

## What it is

RAPID, developed by Bain & Company and described by Paul Rogers and Marcia Blenko, is a decision-rights vocabulary. Recommend: gathers input, builds the case, proposes. Agree: must sign off and can veto, but must negotiate with Recommend rather than kill silently; keep this role rare. Perform: executes once decided and should be consulted on feasibility. Input: consulted, with no veto. Decide: one person or body with the single point of accountability who commits the organisation. The method's rule is that every important decision has exactly one D and as few A's as possible, and that the roles are written down. In government the D is often diffuse (cabinet, a committee, a minister advised by a centre) and the A's are many (finance ministry, legal counsel, a regulator), which is why RAPID is diagnostic there.

## When Horus uses it

- P0 intake: the brief must name the ultimate decision maker; RAPID is the question set for finding the D behind the signatory of the RFP. The stakeholder record's `decision_role` field uses RAPID values.
- Alignment points: each decision sought at a gate is checked against who holds the D and which A's must be in the room or pre-briefed.
- Institutional and operating-model pathway anchor framework: the decision-rights map of the current state is part of the institutional diagnostic; target operating models specify RAPID for the critical decisions; the governance charter deliverable is substantially a RAPID table.
- Transformation pathway: delivery chains stall where the D is missing or contested.

## Steps

1. **List the critical decisions.** For the engagement: the gate decisions and the final recommendation. For an institution: the ten to fifteen decisions that most affect its performance (budget allocation, appointments, licensing, enforcement, project approval).
2. **Assign roles on paper.** From law, decrees, delegations and terms of reference: who holds R, A, P, I, D.
3. **Assign roles in practice.** From interviews and observed behaviour: who actually decides, who can quietly veto, who is consulted late. Note gaps between paper and practice.
4. **Diagnose.** Decisions with no D, with several D's, with many A's, or with Perform excluded from Input are the ones that stall or fail in execution.
5. **Design (institutional pathway).** For each option, specify the RAPID table for the critical decisions, with the legal instrument that would make it so.
6. **Apply to the engagement.** Pre-brief every A before a gate meeting; make sure the D is in the room or has delegated; list decisions sought in the meeting record.

## Outputs → state records

- `stakeholders.decision_role` (`recommend`, `agree`, `perform`, `input`, `decide`, `none`) for every person and body, and `brief.client_roles.ultimate_decision_maker`.
- `analyses` record of kind `institutional_diagnostic` (current-state RAPID tables) and of kind `internal_politics` (`influence_paths[]` for where practice differs from paper).
- `meetings.decisions_sought[]` and `decisions.made_by` checked against the D.
- Target-state RAPID tables in `options` of kind `operating_model` (`design_parameters[]`), appraised under `appraisals.operating_model.fit_to_mandate` and `legal_changes_required[]`.
- The governance charter: `deliverables` of type `governance_charter`; the implementation plan's `instruments_required[]` for the legal changes that move a D.

## Pitfalls

- Assuming the signatory of the contract holds the D; often the D sits with a minister, a cabinet committee or a finance ministry.
- Too many A's in a proposed governance design; each veto point is a delay point.
- Leaving Perform out of Input; implementers find out last and comply least.
- Reading RAPID as an organisation chart; it is per decision, and the same body may hold different roles for different decisions.
- Recording in-practice roles for named officials in client-facing documents without sensitivity review.

## Source

Paul Rogers and Marcia Blenko, "Who Has the D? How Clear Decision Roles Enhance Organizational Performance", Harvard Business Review, January 2006; Bain & Company's RAPID decision-rights tool.
