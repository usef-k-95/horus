# Message house

A one-page communication architecture: a roof carrying the core message, three or four pillars carrying the supporting messages, and a foundation of proofs (facts, numbers, examples, endorsements) that hold the pillars up. Horus uses it to make the communication plan's narrative consistent across spokespeople, audiences and channels.

When Horus uses this: P5 communication planning on every pathway; the `message_house` block of the communication plan is required.

## What it is

The message house is a widely used device in corporate and political communication for disciplining what an organisation says about a change. The roof is the umbrella message: one sentence that states what is being done and why it is good for the audience that matters most. The pillars are the three or four messages that, taken together, make the roof credible; each addresses a different concern or benefit and can stand alone in a short interview. The foundation holds the evidence for each pillar: statistics with sources, case examples, precedents, independent endorsements and the answers to the hardest questions. Everything a spokesperson says should be traceable to a pillar and a proof; anything that is not either belongs in the house or is not said. The house is built for a specific decision and audience set, and is rebuilt when the recommendation changes. In Horus, it is the bridge between the evidence ledger and public language: every proof is an evidence record, so the communication plan passes the same traceability audit as the analysis.

## When Horus uses it

- P5: the communication plan deliverable opens with the message house; audience-specific messaging is derived from it; the Q&A bank sits in the foundation.
- Decision memo and executive summary: the roof is consistent with the governing thought; the pillars echo the key line, in public language.
- Gate meetings: the Supervisor presents from a house so that answers to questions stay consistent with the analysis.
- Stakeholder-specific messaging: each audience hears the pillar that matters to it, never a different roof.

## Steps

1. **Fix the audience set** and the decision the communication supports.
2. **Write the roof** in one sentence in plain language: the change and the benefit, from the primary audience's point of view, consistent with the recommendation's governing thought.
3. **Choose three or four pillars**: each a complete sentence addressing a distinct concern (why now, who benefits, what it costs and who pays, how it will be delivered fairly); test that they cover the reaction matrix's main objections.
4. **Lay the foundation**: for each pillar, the two or three strongest proofs, each an evidence record with grade and source line; add the precedents and endorsements that are public.
5. **Stress-test** against the reaction matrix and the Q&A bank: which pillar answers each predicted objection; where is there no answer.
6. **Translate** into the working languages and check that the roof survives translation.
7. **Version** the house with the recommendation; retire old pillars explicitly so spokespeople do not mix versions.

## Outputs → state records

- `analyses` of kind `communication_plan` with `content.message_house {core, pillars[], proofs: → EVD[]}`, `narrative`, `qa_bank[] {question, answer, evidence}`, `opposition_handling[]`.
- `evidence` records for every proof, validated under the two-source rule before use in public language.
- `communication_plan.content.audiences[].messages[]` derived from the pillars.
- `deliverables` of type `communication_plan` and the communication matrix exhibit in the final deck.
- `decisions.statement` for `recommendation` as the source of the roof.

## Pitfalls

- A roof that describes the policy rather than its benefit, or that promises what the appraisal does not support.
- Pillars that are the same message three times, or that leave the biggest objection unanswered.
- Proofs without sources, or with numbers the traceability audit cannot resolve; the house inherits the evidence discipline.
- Different houses for different audiences; audiences get different emphasis, not different roofs.
- Building the house before the recommendation is confirmed and then defending the old one.

## Source

Standard communications practice; the message house has no single canonical author or document. Horus applies it under the World Bank's strategic communication for reform (Cabañero-Verzosa and Garcia, 2009) and the evidence conventions of this method.
