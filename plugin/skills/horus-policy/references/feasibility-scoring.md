# Feasibility scoring

How Horus rates the administrative, legal and political feasibility of each shortlisted option on a 1 to 5 scale with evidence, and how political feasibility is built from the Overton window, veto players, coalition requirements and the political calendar rather than asserted.

When Horus uses this: phase P4, inside every appraisal (`appraisals.feasibility`), and in lighter form at P3 screening; refreshed before each gate meeting as the reaction matrix is regenerated.

## Rules

- Feasibility is scored separately from desirability and shown beside it. An option can be attractive and infeasible; the decision maker, not the score, decides whether to spend political capital.
- Every rating has a `note` and `evidence: → EVD[]`. Interview statements are Tier A evidence of a stakeholder's position and Tier C of any fact asserted; public positions and legal provisions are the other staples. A rating without evidence carries `confidence: low` in the note and a matching `open_questions` record.
- Ratings describe the option as designed, including its phasing and mitigation; a variant can change the rating, and that is often the point of the variant.
- Scores are judgements against rubrics, not measurements; the rubric is the same across options.

## Administrative feasibility

Can the implementing bodies deliver this with the capacity they have or can plausibly acquire?

| Rating | Anchor |
|---|---|
| 5 | Within existing functions, staff, systems and data of a body with a record of delivering comparable things |
| 4 | Minor additions (a unit, a system module, a data-sharing agreement) with a credible owner |
| 3 | New capability or process needed; achievable with a transition period and funding; some dependency on another body |
| 2 | Major new capability across several bodies, or a body with a record of failure on comparable tasks; high coordination burden |
| 1 | No plausible implementer within the horizon; depends on institutions that do not exist |

Evidence: the `institutional_diagnostic` or `delivery_chain` analysis, staffing and budget data, past-attempt evidence, interviews with implementers. The capability gap from `appraisal/operating-model.md` and the dependency list from `appraisal/delivery-intervention.md` feed this rating.

## Legal feasibility

Can this be done lawfully, by which instrument, and how exposed is it?

| Rating | Anchor |
|---|---|
| 5 | Within existing powers; administrative or circular-level action |
| 4 | Secondary legislation or decree under an existing enabling power; no constitutional or treaty issue |
| 3 | Primary legislation needed; no constitutional obstacle; ordinary majority |
| 2 | Primary legislation with constitutional, fundamental-rights, EU-law or treaty questions; litigation likely |
| 1 | Constitutional amendment or treaty change; or clearly unlawful as designed |

Evidence: legal provisions in the ledger, legal opinions, comparable litigation, international obligations (the `international_obligations` dimension). Record the instrument required; the implementation plan's `instruments_required` is built from it.

## Political feasibility

Can this be adopted and sustained, given who decides, who can block, and when? The rating is assembled from four analyses, each recorded, never from the Principal's instinct.

**Overton window.** Place the option on the window of what is currently sayable: unthinkable, radical, acceptable, sensible, popular, policy. Evidence: the `public_sentiment` analysis (polls, media tone, salience), party and manifesto positions, what comparable governments have adopted (the benchmark analysis moves windows), and how the decision maker has framed the issue (`decision_maker_lens.framing_guidance`). An option outside the window is not infeasible; it needs a framing and sequencing strategy, and a lower rating now.

**Veto players.** From the stakeholder register: who holds a `decision_role` of `decide` or `agree`; who controls a procedural choke point (a second chamber, a constitutional court, a coalition partner, a regulator whose approval is required, a union whose agreement a transfer needs); who can delay long enough to kill (a budget committee, a procurement authority). For each, the predicted reaction to this option (`predicted_reactions`, `block` or `resist`) with its basis. One confident `block` from a veto player caps the rating at 2 unless the option has a credible route around it.

**Coalition requirements.** What minimum set of stakeholders must support, or at least not oppose, for adoption and for implementation to hold, and whether the reaction matrix shows it. Count `support` and `conditional` among those who matter (influence 4 to 5), identify the condition that converts each `conditional`, and name the principle or variant that delivers it (`guiding-principles.md`). Record the coalition in the reaction-matrix analysis's `coalition_notes`.

**Political calendar.** Elections, budget cycles, legislative sessions, party congresses, reshuffles, international events, the decision maker's own milestones (`profiles.political_calendar`, `decision_maker_lens.calendar`). Ask whether the option can show visible results inside the window the decision maker needs, whether its legal instrument fits the sessions available, and whether a known event will reopen the question. Timing is a design choice: sequencing and quick wins (`implementation-planning.md`) raise the rating.

| Rating | Anchor |
|---|---|
| 5 | Inside the window; no veto player opposed; coalition in place; fits the calendar with visible results in time |
| 4 | Inside the window; conditional support from veto players with known, affordable conditions; calendar fits |
| 3 | At the edge of the window; at least one veto player resists; coalition achievable with concessions or sequencing; timing tight |
| 2 | Outside the window, or a confident block from a veto player; coalition not visible; would need a different calendar |
| 1 | Blocked by the decision maker's own red line or by a veto player with no route around; or unthinkable in the current climate |

Record the rating in `feasibility.political {rating, note, evidence}`, with the note naming the window placement, the veto players, the coalition gap and the calendar constraint in a sentence each. The same material populates the `political_feasibility` impact row and, for the preferred option, the communication plan's audiences and opposition handling.

## Presenting feasibility

The appraisal deck shows a two-by-two of attractiveness (the appraisal summary) against feasibility (the lowest of the three ratings, or a combination the Principal states), each option a labelled point, with the evidence IDs in the exhibit's source line. Options in the attractive-but-infeasible quadrant get a paragraph on what would make them feasible (a variant, a sequence, a coalition move) rather than a cross; that paragraph is often the recommendation's second phase.

## Pitfalls

Political feasibility inferred from the sponsor's enthusiasm; a single interview standing for a whole constituency; stale stances (`last_reviewed` older than the last significant event); legal feasibility rated without a provision cited; administrative feasibility rated on the ministry's self-assessment; averaging the three ratings into one number; letting feasibility shade the desirability scores; treating the window as fixed when benchmark evidence shows comparable governments have moved it.

Source: Tsebelis, Veto Players: How Political Institutions Work (2002); Kingdon, Agendas, Alternatives, and Public Policies (1984) on policy windows; the Overton window as described by the Mackinac Center for Public Policy; Mendelow's power-interest grid (1991); Mitchell, Agle and Wood on stakeholder salience (1997); Rogers and Blenko, "Who Has the D?" (2006) for RAPID roles.
