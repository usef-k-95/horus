# Stakeholder salience

Mitchell, Agle and Wood's model classifies stakeholders by whether they hold power, legitimacy and urgency, producing seven types from dormant to definitive. Horus uses it to catch stakeholders the power-interest grid under-rates and to decide who must be heard on legitimacy grounds rather than on power.

When Horus uses this: P1 to P2 when the stakeholder list is long, and whenever a stakeholder with a legitimate claim but little power risks being ignored.

## What it is

Salience is the degree to which managers give priority to a stakeholder's claims. Mitchell, Agle and Wood argue it is a function of three attributes. Power: the ability to impose one's will. Legitimacy: a socially accepted and expected claim (legal, contractual, moral). Urgency: the claim is time-sensitive and critical to the stakeholder. One attribute gives a latent stakeholder (dormant with power only, discretionary with legitimacy only, demanding with urgency only). Two give an expectant stakeholder (dominant: power and legitimacy; dangerous: power and urgency; dependent: legitimacy and urgency). All three make a definitive stakeholder whose claim must be addressed. The attributes are variable, socially constructed and not always consciously exercised, which is why stakeholders move between types.

## When Horus uses it

- P1 when the Mendelow grid leaves a cluster of low-power stakeholders with legitimate claims (service users, small firms, regions). Salience says which of them are dependent stakeholders whose claims the decision maker is expected to honour, and who will find a powerful patron.
- P2 to P3: dangerous stakeholders (power and urgency, no legitimacy) are the ones who can derail a gate meeting through the press or a court; they need a handling plan.
- Regulatory and programme pathways especially, where legitimacy of consultation is a formal requirement and where the EU and OECD standards expect stakeholder views reported by group.
- Public-interest framing in the communication plan: legitimacy is the attribute that persuades a decision maker to take a weak group seriously.

## Steps

1. **Start from the stakeholder list** already rated for influence and interest.
2. **Assess legitimacy**: does the stakeholder have a legal right to be consulted, a contractual relationship, a direct exposure to the policy's effects, or a recognised representative role.
3. **Assess urgency**: is the claim time-critical for the stakeholder (an imminent cost, a deadline, a court case, an election) and does the stakeholder treat it as critical.
4. **Classify** each stakeholder into one of the seven types; record the type and the basis.
5. **Set handling rules.** Definitive: involve in design. Dominant: formal engagement and no surprises. Dependent: give voice through consultation, interviews and the equity analysis; consider who could become their patron. Dangerous: handling plan, legal and media readiness. Latent types: monitor and record.
6. **Watch for attribute acquisition.** A dependent group that gains a powerful ally becomes definitive; a dormant stakeholder acquires urgency when a deadline approaches.
7. **Report by group** in consultation summaries, so that legitimacy is visible in the deliverable even where power is absent.

## Outputs → state records

- Classification and basis recorded in the stakeholder analysis (`analyses` with `narrative_path`) and reflected in `stakeholders.engagement.purpose` and `priority`.
- Legitimacy claims as `evidence` of kind `legal_provision` or `position`, linked through `stakeholders.public_positions`.
- Handling rules for dangerous stakeholders: `risks` of scope `political` or `reputational` with `mitigation` and `early_warning`.
- Dependent groups carried into `appraisals.distributional {groups[], incidence[], equity_note}` and into `communication_plan.content.audiences[]`.
- Consultation reporting by group in the RIA report's consultation annex (`deliverables` of type `ria_report`).

## Pitfalls

- Treating legitimacy as popularity. It is about the recognised standing of the claim.
- Dismissing dependent stakeholders because they cannot block today; they are the usual source of later legitimacy failures and judicial review.
- Over-reacting to demanding stakeholders (urgency only) who have neither power nor a legitimate claim.
- Static classification; urgency in particular changes with the political calendar.
- Letting the client's view decide who is legitimate; use the legal framework and the evidence.

## Source

Ronald K. Mitchell, Bradley R. Agle and Donna J. Wood, "Toward a Theory of Stakeholder Identification and Salience: Defining the Principle of Who and What Really Counts", Academy of Management Review, volume 22, number 4, 1997.
