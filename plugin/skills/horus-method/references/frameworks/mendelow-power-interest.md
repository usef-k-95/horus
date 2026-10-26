# Mendelow power-interest grid

A two-by-two placing each stakeholder by its power over the decision and its interest in the outcome, which sets the engagement strategy: manage closely, keep satisfied, keep informed, or monitor. It is the first cut of every Horus stakeholder map and the axes of the `influence` and `interest` fields.

When Horus uses this: P1 stakeholder map version 1 on every pathway, refreshed before every gate.

## What it is

Aubrey Mendelow's grid, popularised through Johnson and Scholes' strategy texts, classifies stakeholders on two axes. Power (Horus uses "influence") is the capacity to affect the decision or its implementation, whether formal (a veto, a budget, a signature) or informal (access, expertise, public voice). Interest is how much the stakeholder cares about this particular outcome and will spend attention on it. High power and high interest are key players to be managed closely and engaged in design. High power and low interest must be kept satisfied, because their interest can be activated by opponents. Low power and high interest are kept informed and can be mobilised as allies. Low power and low interest are monitored. The grid is dynamic: stakeholders move as the engagement becomes visible.

## When Horus uses it

- P1: the kickoff deck's stakeholder landscape slide; the engagement plan derives interview priority 1 from the top-right quadrant plus anyone whose power can be activated.
- P2 to P3: refreshed after interviews; movement across quadrants is itself a finding.
- P5: the communication plan sequences audiences by quadrant.
- All pathways. On the institutional pathway power is often formal decision rights; on the regulatory pathway interest is concentrated among regulated firms; on the programme pathway the users have high interest and low power, which is the equity warning.

## Steps

1. **List stakeholders** from the brief, the RFP's distribution list, the legal framework (who signs, who is consulted by law), the delivery chain, the affected groups and the media landscape. Include the client's own units and the ultimate decision maker.
2. **Rate influence 1 to 5** with a one-line basis: formal powers first, then resources, then access and voice. Mark unknowns rather than guessing.
3. **Rate interest 1 to 5**: stake in the outcome, past activity on the issue, public statements.
4. **Plot and assign a quadrant strategy.** Key players: interview, involve in principles, test options with them. Keep satisfied: brief early, avoid surprises, give them a role. Keep informed: consultation, updates, mobilise if supportive. Monitor: watch for movement.
5. **Add stance.** Colour the grid by stance (champion to opposed) so the picture shows where the risk is: high power, opposed, high interest is the red corner.
6. **Set engagement priority and format** per stakeholder and the owner of the relationship.
7. **Refresh** after each interview and before each gate; log movements with the evidence that caused them.

## Outputs → state records

- `stakeholders.influence` and `stakeholders.interest` (1 to 5) with the basis in `method_notes` of the stakeholder analysis; `stakeholders.stance`, `stance_confidence`, `stance_basis`.
- `stakeholders.engagement {priority, purpose, format, owner, status, next_step}`; priority 1 drives the `client_request_meeting` actions the AP1 gate checks.
- The grid as an exhibit: an `analyses` record (kind `other` or as part of `internal_politics` for the client entity) whose `narrative_path` holds the quadrant assignments and the movements since the last version.
- `communication_plan.content.audiences[]` ordered by quadrant in P5.
- `last_reviewed` on each stakeholder, so stale ratings are visible.

## Pitfalls

- Rating power from the organisation chart alone; informal power (a minister's adviser, a columnist, a union) is routinely under-rated.
- Static grids: a stakeholder who is "keep satisfied" in P1 becomes a key player the day the proposal is leaked.
- Confusing interest with support. A highly interested stakeholder may be the strongest opponent.
- Ignoring low-power, high-interest groups because they cannot block; on equity grounds and for legitimacy they are the groups the policy is for.
- Showing the grid with named officials in client-facing material without checking the sensitivity audit; the grid is usually `client-confidential`.

## Source

Aubrey L. Mendelow, "Environmental Scanning: The Impact of the Stakeholder Concept", Proceedings of the Second International Conference on Information Systems, Cambridge, Massachusetts, 1981; popularised in Gerry Johnson and Kevan Scholes, Exploring Corporate Strategy, Prentice Hall, successive editions from 1988.
