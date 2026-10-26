---
name: horus-policy
description: How Horus designs, appraises and plans policy across six advisory pathways: problem classification, option design, guiding principles, appraisal methods including regulatory impact assessment with the horus_appraisal toolkit, implementation and communication planning.
---

# Horus policy design and appraisal

The method adapts to the problem. After intake the Principal classifies the problem (`references/pathways/classification.md`) and selects a primary pathway, sometimes with a secondary one. Each pathway pack in `references/pathways/` sets the diagnostic lens, the option logic, the appraisal method, the stakeholder emphasis, the Tier 2 deliverables and the gate variants. Regulatory impact assessment is the regulatory pathway's appraisal method, not the default for everything.

## Option design (`references/option-design.md`)

Build the long list from the pathway's option logic and from precedents in the evidence ledger; always include do-nothing; screen against the brief's objectives and the emerging guiding principles; keep a short list of two to four options plus variants or packages. Every option carries a theory of change (`options.mechanism`) and its design parameters.

## Guiding principles and political directives (`references/guiding-principles.md`)

Draft five to seven candidate principles from the brief, the decision-maker lens and the diagnosis; prepare the directive questions (red lines, fiscal envelope, mandatory versus voluntary, timing against the political calendar); pre-test against the stakeholder reaction matrix; record the validated principles and directives as `decisions` and convert them into criteria weights for the comparison.

## Appraisal (`references/appraisal/`)

One file per kind: `ria.md`, `strategic-options.md`, `operating-model.md`, `delivery-intervention.md`, `business-case.md`, `service-concept.md`. Common to all: a baseline, impacts by dimension and by who bears them, monetisation where credible, distributional effects, feasibility (administrative, legal, political), risks, sensitivity, monitoring indicators, proportionality. The analyst writes the `appraisals` record with the kind's method-specific block.

Toolkit `horus_appraisal` (installed in the backend; run `backend/uvw run python -m horus_appraisal demo <dir>` to see the pattern): `cba` (discounting schedules green_book, omb_a4_2023, eu; NPV, BCR, payback, equivalent annual), `scm` (Standard Cost Model), `mca` (normalised weighted scores with rank robustness), `montecarlo` (distributions, percentiles, tornado, switching values), `distribution` (incidence and progressivity), `scenarios` (projections, trajectories, intervention effects), `fivecase` (optimism bias, appraisal summary table), `report` (CSV, Markdown, SVG charts in the Horus style). Inputs reference `assumptions` IDs; outputs become artefacts on the appraisal record.

## Feasibility and politics (`references/feasibility-scoring.md`)

Overton-window placement, veto players, coalition requirements, timing. Political feasibility is scored with evidence from interviews and the reaction matrix, never asserted.

## Implementation and communication (`references/implementation-planning.md`, `references/communication-planning.md`)

Delivery chain, sequencing and quick wins, instruments and institutions, budget and capacity, KPIs and monitoring, risks; audiences, narrative and message house, proof points from the ledger, channels and sequencing, Q&A and opposition handling. Both become `analyses` records of kind `implementation_plan` and `communication_plan` and the corresponding Tier 2 documents.
