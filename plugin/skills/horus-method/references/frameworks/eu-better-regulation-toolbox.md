# EU Better Regulation Guidelines and Toolbox

The European Commission's guidelines (SWD(2021) 305) and the accompanying Toolbox set the most detailed public standard for impact-assessment reports: a nine-section structure, mandatory annexes, a 40-page benchmark and a catalogue of analytical tools. Horus uses the report structure as the template for RIA reports and the tools as method references.

When Horus uses this: P4 and P5 on the regulatory pathway (`EU-BR-Toolbox-2025` in `standards_applied`), and for specific tools (SME test, competition, distribution, Standard Cost Model) on other pathways when a regulatory component exists.

## What it is

The Guidelines describe the Commission's policy cycle (planning, impact assessment, adoption, implementation, evaluation) and the "evaluate first" principle. The Toolbox (69 tools in the December 2025 edition) gives operating instructions for each step. The impact-assessment report format (Tool 11) runs: 1 introduction, political and legal context; 2 what is the problem and why is it a problem (problem tree, drivers, evaluation of existing rules); 3 why should the EU act (subsidiarity); 4 what should be achieved (general and specific objectives); 5 what are the options; 6 what are the impacts of the options and who will be affected; 7 how do the options compare; 8 the preferred option, including proportionality; 9 how would impacts be monitored and evaluated. Mandatory annexes: procedural information; stakeholder consultation synopsis report; who is affected and how (summary cost and benefit table); analytical methods; competitiveness check. Conventions: main report of about 40 pages excluding annexes; an executive summary of four to five pages as a separate document; non-technical language; tables and figures titled, sourced and self-explanatory; stakeholder views by group; economic, social and environmental impacts covered, with SME, competitiveness, fundamental rights, climate and digital checks; review by the Regulatory Scrutiny Board.

## When Horus uses it

- Regulatory pathway: the RIA report deliverable follows Tool 11 adapted to the client's jurisdiction (section 3 becomes "why intervene at this level"); the annexes are produced as listed.
- Method references for the appraisal: baselines, cost typology (compliance, administrative, enforcement, indirect), the Standard Cost Model, discount factors, uncertainty, the SME test, the competition tool, income distribution, monitoring indicators.
- Programme and institutional pathways when an EU-style scrutiny body or donor will review the document.
- QA: the producer checks length, separate executive summary, titled and sourced exhibits and views-by-group reporting against these conventions.

## Steps

1. **Evaluate first**: summarise what existing rules achieved and why they fall short, with the evaluation evidence.
2. **Build the problem tree**: problem, drivers, consequences, who is affected; the baseline projection under existing rules.
3. **Justify the level of action**: why this level of government, what others cannot do.
4. **Set objectives**: general, specific and operational, each with an indicator.
5. **Define options**: discarded options with reasons; retained options described to the same depth.
6. **Assess impacts** by option and affected group, using the Toolbox methods; produce the who-is-affected table.
7. **Compare** on effectiveness, efficiency, coherence and proportionality; present a comparison table.
8. **State the preferred option** and its proportionality; run the SME, competitiveness and other checks.
9. **Design monitoring and evaluation**: indicators, data, review timing.
10. **Assemble** the report and annexes; write the separate executive summary; run the internal scrutiny review.

## Outputs → state records

- `appraisals` of kind `ria` with `standards_applied` including `EU-BR-Toolbox-2025`, `methodology`, `impacts[]` by dimension and affected group, `regulatory {sme_test, competition_check, compliance_cost_scm}`, `monitoring`.
- `analyses` of kind `baseline` (evaluate first and problem tree), `options_screening` (discarded options), `option_comparison` (section 7 table).
- Consultation synopsis: `meetings`, `client_inputs` and `evidence` of kind `position` grouped by stakeholder category.
- Who-is-affected table: `appraisals.impacts[].affected_groups` and `distributional`.
- `deliverables` of type `ria_report` with the annexes, and `executive_summary` as a separate deliverable.
- `assumptions` for discount factors and cost parameters, agreed and traced.

## Pitfalls

- Copying the EU subsidiarity section into a national context; rewrite it as the level-of-intervention argument.
- A report over 40 pages because annex material sits in the body.
- Views-by-group reporting that lists who was consulted but not what they said or what changed.
- Impacts assessed only in the economic column; social and environmental dimensions and the digital and climate checks are expected.
- Citing tool numbers from an outdated Toolbox edition; cite the edition used.

## Source

European Commission, Better Regulation Guidelines, SWD(2021) 305, and Better Regulation Toolbox, 2023 edition with the December 2025 update (BENCHMARKS.md B3).
