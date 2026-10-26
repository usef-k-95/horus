# Regulatory pathway

Design, reform or assess a regulation, licensing regime, standard or mandate. The method is regulatory impact assessment to OECD, EU and UK standards, with instrument typologies for the option space and compliance-cost, SME and competition tests in the appraisal.

When Horus uses this: as the primary pathway when a legal or regulatory instrument is the decision at stake (enum value `regulatory`), and as a secondary pathway whenever another pathway's preferred option contains a regulatory component.

## Classification signals

- The RFP names an instrument: a law, decree, regulation, licence, permit regime, standard, code, mandate or ban, to be created, amended, repealed or assessed.
- The client is a regulator, a ministry's legal or regulatory affairs unit, a better-regulation oversight body, or a legislature's committee.
- The brief uses market-failure or risk language (externalities, information asymmetry, consumer harm, safety, systemic risk) or compliance language (obligations, enforcement, inspection, penalties).
- A RIA, impact assessment or regulatory scrutiny step is required by the jurisdiction's rules or by a donor or accession process.
- Formal consultation of regulated parties is expected or legally required.
- Counter-signals: the instrument already exists and is simply unenforced (transformation and delivery); the real question is which body should regulate (institutional and operating model); the brief asks for a sector direction with many instruments (strategy).

## Diagnostic lens

The regulatory baseline. P2 produces, at `reviewed` status before AP2:

- `analyses` of kind `baseline`: the legal stock (acts, secondary rules, standards, international obligations) and how it is applied; the regulated population by size and segment; current compliance and enforcement practice and capacity; the projection of the problem under existing rules.
- `analyses` of kind `diagnostic`: the market failure or risk analysis, its magnitude and who bears it, and why existing rules do not solve it; past attempts and their fate.
- `analyses` of kind `benchmark`: how four to eight comparator jurisdictions regulate the same problem, with instrument, enforcement model and evaluated results.
- `analyses` of kind `public_sentiment`, `internal_politics` and `decision_maker_lens` as on every pathway, with attention to industry positions and the legislature.
- Interviews: regulated firms by size, industry associations, the regulator's inspectors and legal staff, consumer and civil-society groups, parliamentary counsel.

Hypotheses are of kind `diagnostic` (the failure and its cause), `causal` (why enforcement or compliance fails) and `political` (what the legislature and incumbents will accept).

## Option logic

Options are records of kind `regulatory_instrument` with `instrument_types[]` from the schema enumeration, plus one `do_nothing` option described as a projection and, where phasing or compensation is needed, options of kind `package`. The long list is generated with Hood's four resources and the OECD alternatives-to-regulation checklist, extended with behavioural instruments and, for fast-moving sectors, the WEF agile-regulation toolkit. Every long-list option carries a one-paragraph theory of change (`mechanism`) and the legal route it needs (`design_parameters[]`: primary law, decree, regulation, administrative act). Screening at P3 uses effectiveness against the diagnosed failure, enforceability with existing capacity, compliance burden, competition effect, legal route and timing, and political acceptability from the reaction matrix. The shortlist contains at least two options plus do-nothing and must include at least one non-regulatory or lighter-touch alternative, so that the RIA's alternatives section is real. Variants (`A1`, `A2`) capture stringency, thresholds and phasing; packages pair a mandate with transition support.

## Appraisal method

Appraisal kind `ria`, `pathway: regulatory`.

- Standards applied: `OECD-RIA-2020` and the 2012 Recommendation always; `EU-BR-Toolbox-2025` for report structure and tools; the UK Better Regulation Framework 2023 and impact-assessment template for the scorecard presentation; `OMB-A4-2023` as method for baselines and uncertainty; `HMT-Green-Book-2026` for monetisation and discounting conventions. The client's own RIA rules take precedence where they exist and are recorded alongside.
- Proportionality: `proportionality_level` set at P3 from the expected scale of impacts and recorded with the reason; `light` appraisals are qualitative with SCM where information obligations change; `full` appraisals monetise with ranges.
- Methodology: `cba` where benefits are credibly monetisable, `scm` where the main cost is administrative burden, otherwise `mixed`; `mca` as a supplement for unmonetised dimensions.
- Toolkit modules: `scm` for compliance costs by firm size; `cba` for NPV and benefit-cost ratio with the agreed discount schedule; `distribution` for incidence by firm size and household group; `montecarlo` or scenario sensitivity on the parameters with the widest ranges; `mca` for the comparison across dimensions; `report` for the accounting statement, scorecard and charts.
- Method-specific block, required: `regulatory {sme_test {applicable, finding, evidence}, competition_check {applicable, finding, evidence}, compliance_cost_scm, enforcement_strategy, review_clause}`.
- Impact dimensions always assessed: `business_compliance_cost`, `administrative_burden`, `sme`, `competition`, `consumer_welfare`, `fiscal_cost` (enforcement), `legal_and_institutional`, `international_obligations`; others as relevant.
- Common blocks as on every pathway: `baseline`, `impacts[]` by affected group, `distributional`, `feasibility` (administrative, legal, political), `sensitivity`, `risks`, `monitoring` with a review date.

## Stakeholder emphasis

Regulated firms by size class and their associations (positions are evidence of kind `position`; the SME test needs micro and small firms directly); the regulator's enforcement staff (feasibility); consumers and affected publics as `public_segment` stakeholders with high interest and low power; the legislature and its committees as veto players when primary law is needed; the finance ministry for enforcement budgets; courts and legal counsel on vires and procedural fairness; international partners where obligations bind. Consultation is reported by group in the RIA annex, with what changed because of it. The reaction matrix is built against instrument variants, not only against the headline option, because stringency and thresholds decide stances.

## Core Tier-2 deliverables and structures

- `ria_report`: context; what is the problem and why; why intervene at this level; SMART objectives; options with theory of change; impacts and who is affected; comparison; preferred option with proportionality, SME test and competition check; monitoring and evaluation; annexes (procedural information, consultation synopsis by group, who-is-affected table, methods and assumptions, sensitivity, competitiveness). Main report at most 40 pages excluding annexes; separate executive summary.
- `policy_note`: the standard Horus policy note structure, with the RIA as its evidence base.
- `regulatory_instrument_outline`: purpose and legal basis; scope and definitions; obligations by party; thresholds and exemptions; enforcement, sanctions and appeals; transitional provisions; review clause; consequential amendments.
- `implementation_plan` and `communication_plan` annexes: instruments required, enforcement roll-out, guidance and tooling for compliance, consultation and announcement sequence.

## Gate criteria variants

In addition to the common checklists in STATE_SCHEMA.md section 7:

- AP0: the classification analysis records the instrument at stake and the legal route candidates.
- AP1: frameworks selected include at least one instrument typology and one RIA standard; workstreams cover legal baseline, market analysis, compliance cost and consultation.
- AP2: `baseline`, `diagnostic` and `benchmark` analyses at `reviewed`; the regulated population by size is quantified or marked indicative; enforcement capacity assessed; the legal route for intervention identified.
- AP3: shortlist includes at least one non-regulatory or lighter alternative; `proportionality_level` decided and recorded as a `methodology` decision; consultation plan approved.
- AP4: every shortlisted option has a `ria` appraisal with the `regulatory` block complete; SCM run wherever information obligations change; `sme_test` and `competition_check` filled with findings; sensitivity run for quantified appraisals; the same baseline and assumptions register across options.
- AP5: `ria_report` and `regulatory_instrument_outline` released with traceability passed; the monitoring framework names a review date; the consultation synopsis reports views by group.

## Frameworks

Framing and diagnosis: `oecd-ria-principles`, `roamef-and-strategic-case`, `theory-of-change`, `hypothesis-driven-problem-solving`, `political-economy-analysis`. Stakeholders: `mendelow-power-interest`, `stakeholder-salience`, `veto-players-and-coalitions`, `net-map-influence`, `political-calendar`. Options: `hood-tools-of-government`, `oecd-alternatives-to-regulation`, `behavioural-toolkits-basic-east`, `wef-agile-regulation`, `international-benchmarking`, `policy-packaging-and-sequencing`. Appraisal: `eu-better-regulation-toolbox`, `uk-regulatory-scorecard`, `omb-circular-a4`, `green-book-five-case-model`, `standard-cost-model`, `oecd-competition-assessment`, `eu-sme-test`, `distributional-and-gender-impact`, `multi-criteria-analysis`, `scenario-analysis`, `pilot-and-evaluation-design`. Implementation and communication: `raci`, `logframe-and-dac-criteria`, `pyramid-principle`, `scqa`, `message-house`, `strategic-communication-for-reform`, `cabinet-paper-conventions`, `stakeholder-specific-messaging`.

## Benchmark documents

BENCHMARKS.md B1 (OECD RIA best practice principles, 2020), B2 (OECD 2012 Recommendation), B3 (EU Better Regulation Guidelines and Toolbox, report structure and tools), B4 (UK Better Regulation Framework guidance, 2023), B5 (UK impact assessment and options assessment templates), B6 (Green Book, monetisation and discounting), B7 (OMB Circular A-4, 2023, as method with status caveat), B8 (World Bank Global Indicators of Regulatory Governance), B10 (WEF agile regulation toolkit), C1 to C4 (decision memo conventions). The catalogue is strongest on this pathway.

## Typical pitfalls

- Starting from the instrument the client has drafted and writing the RIA around it; the alternatives step is where reviewers look first.
- No enforcement strategy, or one that assumes inspection capacity the baseline shows does not exist.
- Administrative burden presented as the total cost of regulation; substantive compliance costs are usually larger.
- Consultation reported as a list of meetings rather than views by group and what changed.
- Treating UK or EU thresholds as the client's rules; use them to argue proportionality.
- A review clause missing or undated; monitoring and evaluation is a basic step, not an annex.
- Forgetting the legal route: a good instrument that needs primary legislation in a session that has closed is not a recommendation for this cycle.
