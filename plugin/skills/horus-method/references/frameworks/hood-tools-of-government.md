# Hood's tools of government (NATO)

Christopher Hood's typology sorts every government instrument by the resource it draws on: Nodality (information and position at the centre of networks), Authority (legal power), Treasure (money) and Organisation (direct capacity). Each resource can be used to detect (gather information) or to effect (change behaviour). Horus uses it to generate a complete long list of instruments before any option is favoured.

When Horus uses this: P3 long-list generation on the regulatory pathway, and as a completeness check on option logic on every pathway.

## What it is

Hood's claim is that governments have only four basic resources and that most policy instruments are combinations of them. Nodality tools: advice, information campaigns, disclosure requirements, labelling, registers; cheap, but weak when the government is not trusted. Authority tools: prohibitions, mandates, licences, standards, certification; strong but costly to enforce and politically visible. Treasure tools: grants, subsidies, tax expenditures, fees, procurement, contracts; flexible but fiscally constrained and prone to capture. Organisation tools: direct provision, public enterprises, inspectorates, armed force; reliable but slow to build and hard to unwind. Hood and Margetts' digital-age revision adds that digital infrastructure changes the cost of nodality tools (data, platforms, defaults) and makes detection far cheaper. The typology is descriptive; the design question is which mix fits the problem, the capacity available and the politics.

## When Horus uses it

- Regulatory pathway anchor framework for option logic: before writing a regulation, the Principal lists the nodality, treasure and organisation alternatives so the RIA's "alternatives considered" section is real and OECD-compliant.
- Strategy pathway: pillars and initiatives are checked for over-reliance on one resource (typically authority or treasure).
- Programme pathway: eligibility rules (authority), payments (treasure), outreach (nodality) and delivery (organisation) are the service's instrument mix.
- Pairs with the OECD alternatives-to-regulation list and behavioural toolkits, which populate the nodality quadrant.

## Steps

1. **State the behaviour or outcome** the policy must change, and whether the government first needs to detect something (information problem) or effect something (behaviour problem).
2. **Generate at least one instrument per resource** for effecting, and one per resource for detecting where information is the constraint. Write them in the schema's instrument types.
3. **Note the resource each instrument consumes**, the capacity it presumes (an inspectorate, a payment system, a trusted communicator) and the legal route it needs.
4. **Combine.** Most feasible options are mixes: a standard (authority) with a transition grant (treasure) and a register (nodality). Build two or three mixes with different centres of gravity.
5. **Screen** against the problem diagnosis: nodality fails where trust is low; authority fails where enforcement capacity is absent; treasure fails under fiscal constraint; organisation fails where the state cannot run things.
6. **Carry the long list** to screening with a one-line theory of change each.

## Outputs → state records

- `options` with `status: long_list`, `kind: regulatory_instrument` (or the pathway's kind), and `instrument_types[]` drawn from the schema enumeration: `regulation`, `economic_incentive`, `tax_or_fee`, `subsidy_or_grant`, `information_or_disclosure`, `direct_provision`, `organisational_or_institutional`, `co_regulation`, `voluntary_or_standard`, `behavioural_nudge`, `procurement`.
- `options.mechanism` (a short theory of change) and `options.design_parameters[]` (the resource mix as levers).
- `analyses` of kind `options_screening` with the resource-fit criteria and `shortlist`.
- `options.package_members[]` for mixes recorded as `kind: package`.
- Enforcement capacity findings carried to `appraisals.regulatory.enforcement_strategy` and `appraisals.feasibility.administrative`.

## Pitfalls

- Starting from the client's favoured instrument and listing the others as straw men; reviewers notice.
- Ignoring detection tools; many regulatory problems are information problems that a register or disclosure rule solves without a mandate.
- Choosing authority tools without an enforcement strategy; OECD RIA principles require one in every RIA.
- Treating the four categories as mutually exclusive options rather than as resources to combine.
- Forgetting that nodality depends on trust; where government credibility is low the quadrant is nearly empty.

## Source

Christopher Hood, The Tools of Government, Macmillan, 1983; Christopher Hood and Helen Margetts, The Tools of Government in the Digital Age, Palgrave Macmillan, 2007.
