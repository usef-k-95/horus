# Research brief and memo

A research run starts with a brief the Principal writes and ends with a memo the researcher returns; the ledger records written in between are the product, and the memo is the map to them. This file fixes both formats and shows one worked example of each.

**When Horus uses this:** every `researcher` dispatch (research fan-out in P2, decision-maker and client-entity research in P0 and P1, benchmark and precedent runs in P3 and P4) and every time the Principal integrates a returned memo.

## The brief (Principal to researcher)

One brief answers one research question, profiles one stakeholder or benchmarks one comparator. Fields, in order:

1. **Run header**: run id (`r-<date>-<nn>`), engagement code, phase, research question id (`RQ-nn`) and workstream, date, model class.
2. **Question**: one sentence, answerable, with the unit of answer stated (a share, a list, a timeline, a yes or no with conditions).
3. **What we already hold**: existing `SRC`, `EVD`, `DOC` and `ANA` ids on this question, so the run extends the ledger instead of duplicating it; known contested points.
4. **Hypotheses**: `HYP` ids with statements and, for each, what would support and what would refute it.
5. **Scope**: geography, period, population or unit of analysis, languages, what is out of scope.
6. **Outputs**: the evidence kinds expected (a validated headline statistic, a time series, a list of legal provisions, comparator cells), the `about` targets (`STK` or `OPT`), whether an `analyses` memo record is required (default yes), file locations under `analysis/`.
7. **Credibility floor**: minimum tier for evidence that will be used (engagement default `B`); which claims must be `validated`; source types excluded for this question (for example consultancy estimates of compliance costs); whether D and E are admissible as sentiment signals.
8. **Fetch budget**: WebFetch and connector calls allowed (engagement default 40 per run), wall-clock box, runs allowed. When the budget is spent the run stops and reports gaps; it never pads.
9. **Connectors and starting points**: data connectors to use, institutions to check first, search languages.
10. **Guardrails** restated: public record only; no logged-in scraping; snapshot every source; label inferences; nothing about private individuals.
11. **Return**: memo path and the summary fields below.

## The memo (researcher to Principal)

Saved at `analysis/memos/<run-id>_<RQ>.md`, registered as an `analyses` record of kind `research_memo` (`narrative_path`, `inputs` listing the SRC and EVD ids, `findings[]`, `limitations[]`, `method_notes`, `version: 1`, `status: draft`), and returned as a short summary with the ANA id. Sections:

1. **Header**: run id, question, date, budget used (fetches of allowed, minutes), counts of sources and evidence created or updated.
2. **Answer**: one paragraph, answer first, with the headline EVD id and its `validated` state.
3. **Findings, ranked** by weight for the question. Each line: statement; EVD ids; grade; validated yes or no; confidence; one clause on why it ranks here.
4. **Hypothesis implications**: per HYP, supports, contradicts or no bearing, with EVD ids. The researcher proposes; the Principal changes `hypotheses`.
5. **Contested and single-source items** that matter, with what would settle them.
6. **Gaps**: what was looked for and not found, where and in which languages; whether it is likely a data gap or a search gap.
7. **Follow-ups proposed**: further searches, data requests to the client (draft `actions` of kind `client_request_data`), questions for named stakeholders' interviews, connectors not yet tried.
8. **IDs written**: SRC and EVD lists, ANA id, snapshot paths; anything updated rather than created.
9. **Method notes**: queries run, connectors and endpoints, dates, exclusions applied, anything that fell outside the brief.
10. **Overall confidence** in the answer, with the main reason.

Rules: no number in the memo without an EVD id; no adjective the evidence does not carry; "not found" is a finding; a surprise or a contradiction with the brief goes on the first screen, not the last.

## Worked example: brief

```
Run r-2026-11-02-03 · ENG EGY-2026-003-sme-digital · P2 · RQ-03 · WS-2 Baseline · 2 Nov 2026 · Sonnet-class
Question: What share of registered micro and small enterprises in Egypt issued electronic invoices in 2025,
  and how has that share moved since the tax authority's mandate phases began?
Already held: SRC-0009 (ETA annual report 2024, Tier B); EVD-0012 (mandate phase dates, legal_provision, validated);
  DOC-004 (client data request pending).
Hypotheses: HYP-02 "Adoption among micro-enterprises is below one in four and concentrated in Cairo and Alexandria".
  Supported by an official share under 25 per cent with a governorate split; refuted by a share above 25 per cent
  or an even geography.
Scope: EGY; 2020 to 2025; registered enterprises per the ETA register, size classes per the MSME law; Arabic and
  English; informal firms out of scope here (RQ-05).
Outputs: validated headline statistic for 2025; annual series if published; governorate split; the size-class
  definitions used by ETA and CAPMAS as `fact` records; memo.
Credibility floor: headline figure validated (A, or two independent B); D and E not admissible; consultancy
  reports for context only.
Fetch budget: 40 fetches, 90 minutes, one run.
Start with: ETA publications and press releases; CAPMAS Economic Census; Ministry of Finance budget statement;
  IMF Article IV statistical annex; OpenAlex for evaluations of e-invoicing adoption in middle-income countries.
Return: analysis/memos/r-2026-11-02-03_RQ-03.md and the summary fields.
```

## Worked example: memo

Placeholders throughout; none of these figures is a finding.

```
Run r-2026-11-02-03 · RQ-03 · 2 Nov 2026 · 31 of 40 fetches, 74 min · 6 sources created, 1 updated ·
  9 evidence created, 1 updated
Answer: In 2025 about one in six registered micro-enterprises issued at least one e-invoice (EVD-0047, validated,
  grade A, corroborated by CAPMAS and ETA). The share has risen each year since the first mandate phase
  (EVD-0048 to EVD-0051, single_source, ETA only). A governorate split exists only for 2024 (EVD-0052).
Findings:
 1. Headline share 2025: EVD-0047 · A · validated · high · the only figure on a consistent denominator.
 2. Annual series 2021 to 2025: EVD-0048 to EVD-0051 · B · not validated · medium · ETA is the only publisher.
 3. Cairo and Alexandria hold most issuing micro-firms in 2024: EVD-0052 · B · not validated · medium.
 4. ETA and CAPMAS define "micro" on different thresholds: EVD-0053, EVD-0054 · A · validated · high ·
    affects every comparison in this workstream.
Hypotheses: HYP-02 supported on the share (EVD-0047); supported with lower confidence on geography (EVD-0052,
  one year only).
Contested or single-source: the annual series rests on ETA alone; the IMF Article IV 2026 statistical annex may
  corroborate 2023 (budget ran out before confirming).
Gaps: no published 2025 figure for small (as distinct from micro) enterprises; no sector breakdown; nothing in
  English on the 2026 phase.
Follow-ups: client_request_data to ETA for register extracts by size class and governorate, 2021 to 2025;
  retrieve the Article IV 2026 annex; ask the Deputy Minister (MTG-007) how the ministry reconciles the two
  thresholds.
IDs: SRC-0022, SRC-0031 to SRC-0035 created; SRC-0009 updated (superseded by the 2025 edition);
  EVD-0047 to EVD-0055; ANA-021.
Method: WebSearch in Arabic and English; connectors: openalex (12 works screened, 2 cited), worldbank (not
  relevant to this question); all snapshots finalised.
Confidence: high on the headline, medium on the trend, low on geography.
```

## Integration by the Principal

Read the memo, not the records. Update `hypotheses` (`status`, `evidence_for`, `evidence_against`, `revision_history`); set the research question's `status: done` with `memo: ANA-021` and the run appended to `runs[]`; queue a second-source pass as an internal `action` for material single-source claims; convert follow-ups into `actions` and `open_questions`; carry contradictions into the next checkpoint's `learned[]`.

## Proposed schema additions

A `content` shape for `research_memo`: `{research_question, answer, ranked_findings[] {evidence: → EVD[], rank, why}, hypothesis_implications[] {hypothesis: → HYP, direction, evidence: → EVD[]}, gaps[], follow_ups[], budget {fetches_used, fetches_allowed, minutes}, ids_written {sources[], evidence[]}}`.

Source: ARCHITECTURE.md §5.4 (worker contracts) and §6.2; STATE_SCHEMA.md §A3 (analytical plan) and §D1; DECISIONS.md item 10 (research budget caps).
