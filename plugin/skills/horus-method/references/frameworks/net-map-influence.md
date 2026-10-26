# Net-Map influence mapping

A participatory method that draws who is linked to whom (through money, instructions, information, alliances), assigns each actor an influence level, and records each actor's goals. Horus uses it to turn interviews into a network picture that shows paths to the decision maker and clusters that act together.

When Horus uses this: P2 on every pathway once interviews begin, and whenever the question is "who moves whom" rather than "who matters".

## What it is

Net-Map was developed by Eva Schiffer at the International Food Policy Research Institute for governance research in multi-stakeholder settings. In a session the facilitator and participants list the actors, draw links of several defined types between them, build "influence towers" (stacks of pieces indicating perceived influence), and note each actor's goals in relation to the issue. The result is a social network diagram with influence and goals overlaid, plus the discussion that produced it, which is often the most valuable output. Horus adapts it as a desk and interview method: the links come from documents, public records and interview statements; influence and goals come from interviews and profiles. The product complements the Mendelow grid: the grid shows standing, the network shows the channels through which influence travels.

## When Horus uses it

- P2: after the first round of interviews, to consolidate relationship statements into one picture and to identify brokers, isolated actors and coalitions.
- Internal politics map for the client entity: the units and office holders and the paths that reach the ultimate decision maker.
- P3 to P5: to plan the sequence of who is briefed first so that influence travels toward the decision; to find the credible messenger for each audience in the communication plan.
- All pathways; most valuable on the institutional pathway and on regulatory engagements with organised industry interests.

## Steps

1. **Define the question** precisely: "who influences whether the ministry adopts option B by June" produces a different map from "who matters in the sector".
2. **List actors** from the stakeholder register; add any named in interviews.
3. **Draw links by type.** Horus uses the relationship types in the schema: reports_to, oversees, allied_with, rival_of, influences, funds, regulates, member_of, advises. Mark each as observed (from documents or admitted by both parties) or assessed (inferred from one source).
4. **Rate influence** per actor on the question, from interviews and profiles; reconcile with the Mendelow influence rating and record disagreements.
5. **Record goals** per actor in relation to the decision, as stated and as assessed.
6. **Read the network.** Who is central; who brokers between clusters; which paths lead to the decision maker; which clusters share goals (potential coalitions); who is isolated.
7. **Draw implications.** Who to interview next; which allies to activate; which messenger each audience trusts; where an opposition coalition could form.
8. **Update** as interviews add links; version the map before each gate.

## Outputs → state records

- `stakeholders.relationships[] {to, type, strength, basis: observed|assessed, evidence}`; `stakeholders.interests`.
- `analyses` record of kind `internal_politics` with `influence_paths[]`, `units[]`, `watch_points[]`; a wider map as `analyses` of kind `other` with the network exhibit in `narrative_path`.
- Interview-sourced links as `evidence` of kind `position` or `fact`, carrying `attribution` and the speaker, linked from the relationship's `evidence`.
- Coalition findings into `stakeholder_reaction_matrix.content.coalition_notes`.
- Messenger and sequencing choices into `communication_plan.content.audiences[].spokesperson` and `sequencing[]`.
- Next interviews as `actions` of kind `stakeholder_outreach` or `client_request_meeting`.

## Pitfalls

- Drawing links from a single interview as if observed; mark them assessed until corroborated, and never attribute them in client material.
- Confusing formal reporting lines with influence; the network of advice and alliance is usually the one that matters.
- Over-dense maps nobody can read; filter to the actors and link types relevant to the question.
- Treating the map as neutral data; it embeds the interviewees' perceptions, which is why basis and source are recorded.
- Sensitivity: a network map of named officials with rivalries is `sensitive-personal` material in all but anonymised form.

## Source

Eva Schiffer, Net-Map Toolbox: Influence Mapping of Social Networks, International Food Policy Research Institute, 2007; Eva Schiffer and Jennifer Hauck, "Net-Map: Collecting Social Network Data and Facilitating Network Learning through Participatory Influence Network Mapping", Field Methods, volume 22, number 3, 2010.
