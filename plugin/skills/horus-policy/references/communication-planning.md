# Communication planning

How Horus plans the communication of a recommendation: audiences from the stakeholder register, one narrative, a message house whose proof points are validated evidence, channels and sequencing, spokespeople, a Q&A bank, and the handling of opposition and misinformation, recorded as an `analyses` record of kind `communication_plan`.

When Horus uses this: phase P5, alongside the implementation plan, for the recommended option; in lighter form before any gate meeting whose decision will become known outside the room. Gate AP5 requires the plan at `final`. External-facing material is Tier 3 and is scrubbed of client-confidential and sensitive-personal content.

## Principle

Communication is part of the policy, not its wrapping: the reaction matrix predicted who would resist and why, the principles were chosen partly to buy a coalition, and the plan now has to deliver that coalition and hold it through implementation. Everything said must be true to the appraisal and traceable to the ledger; a claim that cannot be traced is not made, however useful.

## Audiences

Start from the stakeholder register and the reaction matrix, not from a generic list. For each priority-1 and priority-2 stakeholder and each public segment that matters (`stakeholders.kind: public_segment`), record in `content.audiences[]`: the stakeholder or segment (→ STK); the communication objective (inform, reassure, convert a `conditional` by meeting its condition, neutralise a `resist`, isolate a `block`, equip a champion); the messages for them, selected and ordered from the message house by what they care about (`interests`, `concerns`, `red_lines`); the channels they trust; the timing relative to the announcement; the spokesperson they will believe; and the risks (leak, misreading, a hostile intermediary). Internal audiences, the administration that must implement, come first in the list and in time; implementers who learn of a policy from the press implement it badly.

## Narrative

One narrative, written answer-first in the decision maker's voice and consistent with the storyline of the deliverables: the situation people already accept, the complication the diagnosis established, the question it forces, and the answer with its reasons. It is `content.narrative`, a few hundred words at most, and every other message is a cut of it. The narrative uses the frames the decision-maker lens recommends (`framing_guidance`) and avoids the frames the sentiment analysis showed to be toxic; it names the problem in human terms and the solution in concrete ones (who will do what, from when), and it says what the policy is not, pre-empting the predictable misreading.

## Message house

`content.message_house {core, pillars[], proofs: → EVD[]}`:

- **Core** (the roof): one sentence any spokesperson can say and the whole policy stands behind.
- **Pillars**: three supporting messages, each answering a different question (why act, why this option, what it means for you), each true for every audience even if emphasised differently.
- **Proofs** (the foundation): the evidence records behind each pillar, each `validated` under the ledger rules or explicitly marked indicative in the message. Numbers carry the unit, period and source the evidence record holds; the Tier 2 traceability table covers the communication plan like any deliverable.

Test the house by reading each pillar against the hostile audiences in the matrix: if a pillar is false for one of them, it is not a pillar but an audience message.

## Channels and sequencing

`content.sequencing[]` orders who hears what, when, relative to the decision and the instrument:

1. Internal alignment: the decision maker's office, the implementing bodies' leadership, the finance ministry; before anything is written down for outside.
2. Pre-briefing of veto players and coalition partners under embargo, with the condition that converted their `conditional` stated explicitly; a surprise is read as a slight.
3. The announcement, by the decision maker, in the channel the lens recommends, with the instrument or timetable attached so the story is action, not intention.
4. Stakeholder briefings by group (industry, labour, civil society, subnational government) within days, with the Q&A bank and the technical annexes.
5. Public and media: proactive explainers through trusted intermediaries and the government's own channels; monitoring begins.
6. Implementation communication: the obligations, dates and help available to those who must comply, repeated through the channels they use and timed to the roll-out phases of the implementation plan.

Channels are chosen per audience from evidence (where that group gets its information, from the sentiment analysis and interviews), not habit. Record for each step the date or trigger, the owner, the material and the approval it needs; any outbound communication Horus itself drafts runs through the autonomy policy and the `communications` log.

## Spokespeople

Match spokesperson to audience by credibility, not seniority: the minister for the public and the legislature; the head of the implementing body for implementers and the regulated; a respected practitioner or association leader for their peers; an independent expert whose evidence the plan cites, where that person has agreed. Note each in `audiences[].spokesperson` and give each a briefing pack of the narrative, their pillars, their proofs and the Q&A bank. A spokesperson who disagrees with a pillar is a risk, not a spokesperson.

## Q&A bank

`content.qa_bank[] {question, answer, evidence: → EVD[]}`: the questions each audience will ask, including the hostile ones, with short answers in the narrative's voice and the evidence behind every number. Sources for the questions: the reaction-matrix rationales, interview objections, the appraisal's caveats and sensitivities (which an informed critic will find), the costs and who bears them, the comparison with what other countries did, and "why not" for every screened-out option a stakeholder favoured. Questions whose honest answer is uncomfortable (a cost, a loser, an uncertainty) are answered as such; a bank with only easy questions fails on day one.

## Opposition and misinformation handling

`content.opposition_handling[]` prepares for what the matrix predicts and for what it cannot. For each stakeholder predicted to `resist` or `block`: their likely arguments and channels, the response (engage privately first; concede what the appraisal supports conceding; correct what is false; never personalise), the spokesperson, and what would change their position, if anything. For misinformation: the claims most likely to circulate (from sentiment themes and past episodes), the pre-emptive explainer that inoculates against each, the correction protocol (lead with the fact, state the myth once with a warning, explain why it is wrong, repeat the fact; do not amplify fringe claims with no reach), the monitoring (media tone and search interest from the `public_sentiment` analysis, refreshed weekly in the first month), the escalation path, and the rule that every correction cites the ledger. Record what will not be answered and why.

## Content shape

The `communication_plan` analysis holds `narrative`, `message_house {core, pillars[], proofs: → EVD[]}`, `audiences[] {stakeholder or segment: → STK, objective, messages[], channels[], timing, spokesperson, risks}`, `sequencing[]`, `qa_bank[] {question, answer, evidence: → EVD[]}` and `opposition_handling[]`, with `inputs` pointing at the reaction matrix, decision-maker lens, public sentiment, option, appraisal and implementation plan, `findings` (the coalition to hold, the message that carries the most risk, the first week's priorities) and `limitations`.

## Pitfalls

Messages that outrun the appraisal; proof points without evidence IDs; a plan that starts with the press release; veto players surprised; one spokesperson for every audience; a Q&A bank with no hostile questions; repeating a false claim in the headline of the correction; treating implementers as a public to be informed rather than the first audience; running the plan after approval without the monitoring that says whether it is working.

Source: Minto, The Pyramid Principle, for the answer-first narrative; World Bank, Communication for Governance and Accountability Program (CommGAP), Governance Reform under Real-World Conditions (2008) on strategic communication for reform; Lewandowsky, Cook and others, The Debunking Handbook 2020; UK ministerial submission conventions on "communications and handling" as standing content; the message-house technique as practised in public affairs.
