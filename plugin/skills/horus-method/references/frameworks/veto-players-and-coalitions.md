# Veto players and coalition analysis

Tsebelis's veto-player theory identifies the individual and collective actors whose agreement is required to change the status quo, and predicts that more veto players with more divergent preferences means less policy change. Horus pairs it with coalition analysis to work out which reform variant can assemble the agreements it needs.

When Horus uses this: P2 to P3 on every pathway when the preferred direction needs legislative, constitutional or multi-institution agreement; always on the institutional pathway.

## What it is

A veto player is an actor whose consent is necessary for a change in policy. Institutional veto players are set by the constitution and laws (a second chamber, a president with a veto, a constitutional court, a federal upper house); partisan veto players are the parties in a coalition government or the factions whose votes are needed. Policy stability rises with the number of veto players, the ideological distance between them and the internal cohesion of collective veto players. The practical consequence for a policy adviser is that the feasible set of options is the intersection of what each veto player will accept (the "winset" of the status quo). Coalition analysis adds the positive side: which actors, including non-veto players such as business associations, unions, regions or donors, can be assembled behind a variant so that veto players prefer it to the status quo. Sabatier's advocacy coalition framework is the reference for coalitions that persist across issues.

## When Horus uses it

- Regulatory pathway: whether the instrument needs primary legislation (parliamentary veto players) or can be done by decree or regulation (executive only). This often decides the instrument choice.
- Institutional pathway: mandates changed by law need the same veto players as any reform; moving a function between ministries meets ministerial veto players even without legislation.
- Public investment pathway: budget approvals and finance-ministry agreement are veto points.
- Strategy pathway: a strategy that outlives the government needs cross-party acceptance or will be reversed.
- Feeds the political feasibility rating of each appraisal and the sequencing in the implementation plan.

## Steps

1. **List the legal route** for each shortlisted option: constitution, primary law, secondary regulation, administrative decision, budget line. From the route, list the institutional veto players.
2. **List partisan veto players**: parties and factions whose votes are needed at each stage, with the dates on which their composition could change.
3. **Add de facto veto players**: actors who can block in practice (a court through review, a union through strike, a regulator through non-enforcement, a funder through conditions). Record the basis.
4. **Estimate each veto player's acceptable range** on the design parameters that matter (phasing, exemptions, who pays), from public positions, past votes and interviews.
5. **Compute the feasible set**: which variants fall inside every veto player's acceptable range; which require compensation or packaging to bring one player inside.
6. **Build the coalition**: for each feasible variant, who supports it actively, who can be recruited, what each needs. Identify the pivotal actor whose position tips the outcome.
7. **Sequence**: which agreements to secure first, and which windows (budget cycle, legislative session, election) constrain timing.
8. **Record the reading** in the reaction matrix and update after each interview.

## Outputs → state records

- `stakeholders` records for every veto player with `decision_role` (`agree` or `decide`), `red_lines[]`, `predicted_reactions[] {target, reaction (support to block), rationale, confidence, basis}`.
- `analyses` record of kind `stakeholder_reaction_matrix` with `coalition_notes`, and of kind `internal_politics` where the veto sits inside the client entity.
- Legal route per option in `options.design_parameters[]` and `appraisals.feasibility.legal` and `political`; `appraisals.operating_model.legal_changes_required[]` on the institutional pathway.
- `hypotheses` of kind `political` about acceptable ranges, tested in interviews.
- `implementation_plan.content.instruments_required[]` (law, decree, regulation, circular, budget, MoU) and `sequencing[]`.
- `risks` of scope `political` and `legal` for blocking scenarios, with `early_warning`.

## Pitfalls

- Counting formal veto players only; de facto veto through non-implementation is the common failure mode in weaker administrations.
- Treating a collective veto player as a unit; parties and ministries have factions whose cohesion varies.
- Inferring acceptable ranges from public rhetoric; test them in interviews and from past behaviour.
- Designing to the lowest common denominator and calling it feasible; say what was given up and why.
- Ignoring time: the set of veto players changes at elections and appointments, which the political calendar framework tracks.

## Source

George Tsebelis, Veto Players: How Political Institutions Work, Princeton University Press, 2002; Paul A. Sabatier and Hank C. Jenkins-Smith (eds), Policy Change and Learning: An Advocacy Coalition Approach, Westview Press, 1993.
