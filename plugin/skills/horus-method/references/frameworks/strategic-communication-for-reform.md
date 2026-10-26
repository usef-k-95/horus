# Strategic communication for reform (World Bank)

The World Bank's approach to communication as a reform instrument: treat it as a set of management decisions (which stakeholders, what behaviour change, what messages, which channels, how to monitor) taken alongside the policy design, not as publicity after the decision. Horus uses it to build communication plans that change stances and behaviour, and to make the case to clients that communication belongs in the reform plan.

When Horus uses this: P5 communication planning on every pathway; P3 when political directives and guiding principles are being pre-tested with stakeholders.

## What it is

The World Bank's Communication for Governance and Accountability Program and its predecessors argued that governance and economic reforms fail for lack of public support and stakeholder buy-in as often as for technical reasons, and that communication must therefore be strategic: research-based, two-way, targeted at specific behaviours and decisions, and planned from the start. Cabañero-Verzosa and Garcia set out five key decisions a reform team must take: who the stakeholders are and what they think (from research, not assumption); what changes in behaviour or position the reform needs from each; what messages will move them, framed from their interests; which channels and messengers reach them credibly; and how the communication effort will be monitored and adjusted. Odugbemi and Jacobson's edited volume collects the practice of building constituencies for reform under real political conditions: coalition-building, dealing with opposition, using evidence in public argument, and sequencing announcements. The approach is explicitly political-economy aware: communication is how a technically sound reform acquires legitimacy.

## When Horus uses it

- P5 on every pathway: the communication plan deliverable follows the five decisions; its audiences come from the stakeholder register and reaction matrix, its behaviour objectives from the implementation plan's dependencies, and its monitoring from the sentiment analysis.
- P3: pre-testing guiding principles and directives in interviews is communication research; the results update the reaction matrix.
- Regulatory pathway: consultation is two-way communication and must be planned as such under the OECD and EU standards.
- Transformation pathway: compelling communication is one of the five disciplines; the plan covers staff as an audience.
- Decision memo: the "communications and handling" section is the plan's summary for the decision maker.

## Steps

1. **Research**: what each stakeholder group and public segment currently believes, wants and fears, from interviews, polls and sentiment analysis; where the reform's story is being told by others.
2. **Set behaviour and stance objectives** per audience: from resist to conditional, from unaware to compliant, from passive to advocating; tie each to the implementation plan's dependencies.
3. **Craft messages** from the message house, framed in each audience's interests and language, with proofs; decide what is not said.
4. **Choose channels and messengers**: the people and media each audience trusts, from the influence map; the sequence of who hears first.
5. **Plan the sequence**: announcements, consultations, launches aligned to the political calendar and to the implementation milestones; the handling of leaks and opposition.
6. **Prepare the Q&A bank and opposition handling** from the reaction matrix's predicted objections.
7. **Monitor**: indicators of awareness, stance and behaviour; adjust messages and channels; report in stocktakes.

## Outputs → state records

- `analyses` of kind `communication_plan` with `content {narrative, message_house, audiences[] {stakeholder or segment, objective, messages[], channels[], timing, spokesperson, risks}, sequencing[], qa_bank[], opposition_handling[]}`.
- Inputs: `analyses` of kind `stakeholder_reaction_matrix`, `public_sentiment`, `internal_politics`, `decision_maker_lens`; `stakeholders.predicted_reactions[]` and `relationships[]` for messengers.
- `implementation_plan.content.kpis[]` extended with communication indicators; `appraisals.monitoring.indicators[]` where awareness drives take-up.
- `deliverables` of type `communication_plan`; the communications and handling section of `decision_memo`; `communications` records for the outbound messages Horus itself drafts.
- `risks` of scope `reputational` and `political` with mitigations in `opposition_handling[]`.

## Pitfalls

- Communication planned after the decision as announcement logistics; the method exists to prevent this.
- Messages framed in the government's interests rather than the audience's.
- One channel for all audiences; credibility differs by messenger.
- No research on what audiences believe now; the plan then argues with an imagined public.
- Spin: the traceability and sensitivity audits apply to communication plans, and proofs must be validated evidence.

## Source

Cecilia Cabañero-Verzosa and Helen R. Garcia, Building Commitment to Reform through Strategic Communication: The Five Key Decisions, World Bank, 2009; Sina Odugbemi and Thomas Jacobson (eds), Governance Reform under Real-World Conditions: Citizens, Stakeholders, and Voice, World Bank, 2008. World Bank materials are catalogued in BENCHMARKS.md B8.
