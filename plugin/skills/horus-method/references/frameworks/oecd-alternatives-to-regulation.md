# OECD alternatives to regulation

The OECD's standing requirement that regulators consider non-regulatory and lighter-touch alternatives before adopting command-and-control rules: no action, information and education, economic instruments, performance-based and process-based regulation, co-regulation and self-regulation, voluntary standards, and regulatory sandboxes. Horus uses it as the mandatory checklist behind the "alternatives" step of every RIA.

When Horus uses this: P3 option generation and screening on the regulatory pathway; the RIA's "options" section cannot pass QA without it.

## What it is

Principle 4 of the 2012 OECD Recommendation requires RIA to consider "a range of alternatives to regulation", and Box 2.2 of the 2020 best-practice principles makes "identification of alternatives" basic step 5. The OECD's regulatory policy work since the 1990s has catalogued the alternatives: doing nothing (improving enforcement of existing rules, letting markets adjust); information instruments (disclosure, labelling, campaigns, guidance); economic instruments (taxes, charges, tradable permits, subsidies, deposit-refund); performance-based regulation (outcomes specified, means free) and process-based regulation (management systems required); co-regulation (industry codes backed by law) and self-regulation (industry codes without); voluntary standards and certification; and, more recently, experimental approaches such as sandboxes and sunset clauses. The point is proportionality: the least burdensome instrument that achieves the objective with acceptable risk, chosen on evidence rather than habit.

## When Horus uses it

- Regulatory pathway: every long list contains at least the do-nothing baseline, an information or market-based alternative, a co-regulatory or voluntary alternative and the command-and-control option, each with a theory of change, so that the RIA and the OECD reviewer can see the alternatives were real.
- Screening: alternatives are screened on effectiveness in the specific market failure, enforcement cost, compliance cost, competition effects and timing.
- Strategy and programme pathways: when a strategy or service design assumes a new rule, Horus asks whether a lighter alternative achieves the same outcome.
- Implementation: performance-based and co-regulatory options need monitoring and review clauses, which the appraisal records.

## Steps

1. **Restate the market or behavioural failure** from the diagnosis; the alternative must address that failure, not the symptom.
2. **Run the checklist.** For each alternative category, write whether it could address the failure and what it would look like here. Record a reason for each one dropped.
3. **Check the enforcement and compliance reality.** Alternatives that depend on an inspectorate, a trusted association or a functioning market need evidence those exist.
4. **Draft the long list** with the do-nothing option described as a projection, not a blank.
5. **Screen** with the client's criteria and the OECD proportionality test: achieves the objective; least burden; enforceable; coherent with existing rules; acceptable risk if it underperforms.
6. **Design hybrids and phasing**: co-regulation with a statutory backstop; information first with a mandate trigger if take-up stalls; sunset or review clause.
7. **Document** alternatives considered and rejected with reasons; this is a standing section of the RIA report.

## Outputs → state records

- `options` with `status: long_list` and `instrument_types[]` (`information_or_disclosure`, `economic_incentive`, `tax_or_fee`, `co_regulation`, `voluntary_or_standard`, `regulation`, `behavioural_nudge`, plus `do_nothing` as the option kind), each with `mechanism`.
- `options.screening {criteria[], result, rationale, analysis}` and `status: screened_out` with reasons preserved.
- `analyses` of kind `options_screening` (`criteria[]`, `scores[]`, `shortlist`).
- `appraisals.proportionality_level` and `appraisals.regulatory {enforcement_strategy, review_clause}` for the shortlisted alternatives.
- The RIA report's "alternatives considered" section in `deliverables` of type `ria_report`, traced to the screening analysis.

## Pitfalls

- Alternatives listed to satisfy the form, with no theory of change or evidence; scrutiny bodies reject these.
- Assuming self-regulation works without checking the association's coverage and sanctioning power.
- Treating do-nothing as zero cost; the baseline carries the cost of the unaddressed failure.
- Dropping economic instruments for political reasons without saying so; record the directive as a decision.
- Forgetting coherence with existing rules; stacking a new instrument on an unenforced old one.

## Source

OECD, Regulatory Impact Assessment: Best Practice Principles for Regulatory Policy, 2020, Box 2.2 step 5 (BENCHMARKS.md B1); OECD, Recommendation of the Council on Regulatory Policy and Governance, 2012, principle 4 (BENCHMARKS.md B2); OECD, Regulatory Policies in OECD Countries: From Interventionism to Regulatory Governance, 2002.
