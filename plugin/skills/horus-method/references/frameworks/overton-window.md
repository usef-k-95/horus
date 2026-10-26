# Overton window

The range of policy positions that the public and political class currently treat as acceptable, from unthinkable through radical, acceptable, sensible and popular to policy. Horus uses it to judge how far a recommendation can sit from current debate, and to design the sequence and framing that move a position inside the window.

When Horus uses this: P3 option screening and P5 communication planning on every pathway; most on the strategy and regulatory pathways where ambition is a choice.

## What it is

Joseph Overton of the Mackinac Center for Public Policy described a window of political possibility: politicians can adopt positions inside it without unacceptable electoral or reputational cost, and positions outside it are not seriously considered whatever their merits. The window shifts with public opinion, events, elite endorsement and sustained advocacy, and it differs by audience and jurisdiction. The concept is a heuristic, not a measurement; its value in advisory work is to separate two questions that get confused: is the option right, and is the option sayable now. It also disciplines ambition. An option just outside the window may be reachable through framing, a pilot or a trusted messenger; one far outside is a long-term agenda item, not a recommendation for this decision cycle.

## When Horus uses it

- P3: when screening the long list, the political acceptability criterion is a window judgement, recorded with the evidence (polls, media, statements by the decision maker and opponents).
- P3 principles workshop: guiding principles and political directives from the client define the window from the inside; Horus checks them against the outside view.
- P5: communication planning decides whether to present the recommendation as inside the window ("sensible, already done by peers") or to widen the window first (reframe, pilot, enlist validators).
- Decision-maker lens: the decider's personal window may be narrower or wider than the public's; both are recorded.

## Steps

1. **Define the dimension** on which positions range (for example the stringency of a mandate, the level of a fee, the degree of centralisation).
2. **Place the current policy and the public debate** on it, with evidence: polls and sentiment, media framing, positions of parties and major stakeholders, what peer jurisdictions have done.
3. **Place each option** on the dimension and judge where it sits relative to the window for the general public, for the governing coalition and for the decision maker.
4. **Identify movers**: events, evidence, validators and precedents that have shifted or could shift the window; estimate their timing.
5. **Decide the posture** per option: present as sensible now; move the window first; park as a longer-term agenda; or split into a first step inside and a second outside.
6. **Design the framing** that places the recommendation inside the window without misrepresenting it; test it against the reaction matrix.
7. **Record the judgement and its confidence**; revisit when sentiment or events change.

## Outputs → state records

- `analyses` of kind `public_sentiment` (`themes[]` with `direction` and `intensity`, `polls`, `media`) as the evidence base for the window.
- `analyses` of kind `decision_maker_lens` (`priorities[]`, `red_lines[]`, `framing_guidance[]`).
- `options.screening.criteria[]` with the political acceptability score and rationale; `options.principles_alignment[]`.
- `decisions` of kind `political_directive` where the client states what is sayable.
- `appraisals.feasibility.political {rating, note, evidence}`.
- `communication_plan.content.narrative`, `message_house` and `sequencing[]`; `opposition_handling[]`.
- `risks` of scope `political` where the recommendation sits at the window's edge.

## Pitfalls

- Treating the window as fixed and recommending only what is already popular; the adviser's job includes saying what should be done and how to make it possible.
- The opposite error: ignoring the window and recommending the technically optimal option with no path to adoption.
- Reading the window from the capital's commentariat; measure it with polls and sentiment analysis across segments.
- Letting framing slide into spin; the sensitivity and traceability audits apply to communication plans too.
- Confusing the decision maker's comfort with the public's acceptance; both are mapped and may differ.

## Source

Joseph P. Overton, Mackinac Center for Public Policy, mid-1990s; the Mackinac Center's explanatory note "The Overton Window" (undated). Concept only; no canonical document beyond the Center's materials.
