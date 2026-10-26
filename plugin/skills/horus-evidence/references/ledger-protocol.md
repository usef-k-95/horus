# Ledger protocol

The ledger is the set of `sources` and `evidence` records that every number, quote and claim in a Horus deliverable traces back to. This file fixes how a claim is cut, written, valued, corroborated, snapshotted and cited, and what the server computes versus what the researcher writes and the Principal confirms.

**When Horus uses this:** on every `create` or `update` to `sources` or `evidence`, by the `researcher`, by the `interviewer` for interview-sourced evidence, and by the Principal.

## One atomic claim per record

A record holds one claim: one subject, one predicate, one value, one period, one geography. Tests: an "and" joining two facts means two records; a number with a breakdown is one record per component plus one for the total; a change between two dates is two `statistic` records plus, where the direction matters, one `finding` naming both IDs in `notes`; a legal provision is one record per article or obligation, not one per law. Before creating, `search` the ledger for the claim; if it exists, `update` it by appending your source to `sources` and raising `corroboration` instead of creating a twin. Duplicates break the two-source rule in both directions.

## Writing the statement

In Horus's words, never a paste, readable alone in a footnote: period and geography inside the sentence; the number exactly as `value` states it; no adjectives or verbs of judgement ("only", "surged"); no causal language unless the source establishes causation, in which case the kind is `finding` and the method is in `notes`. Positions name the holder by title and set `about` to the stakeholder: "The Deputy Minister for Digital Transformation opposes a licensing regime for micro-merchants (stated 12 November 2026)." Forecasts name the forecaster and the edition. "According to" belongs in `sources`, not in the statement.

## Value fields

Required for `statistic`, `estimate` and `forecast`, and for any `fact` with a number.

- `number`: numeric, never a string; the source's precision (round in the deliverable, not the ledger); percentages as 18, not 0.18.
- `unit`: shared vocabulary: `percent`, `percentage_points`, `count`, `persons`, `firms`, `index`, `ratio`, `days`, `hours`, `per_1000`, and money as `<ISO4217>_<thousand|million|billion>` (`EGP_billion`). Never confuse `percent` with `percentage_points`.
- `period`: `2025`, `2025-03`, `2024Q3`, `FY2024/25`, `2020-2025` for a span; fiscal years always marked FY.
- `geography`: ISO 3166 alpha-3 with an optional subnational label after a slash: `EGY`, `EGY/Cairo Governorate`.
- `as_of`: the vintage of the data as published (the "last updated" or "data as at" date), not the retrieval date, which lives in the source's `access.retrieved_at`. Two pulls with different vintages are two records; the older is `superseded`.
- `currency` and `price_base_year`: required for money. Nominal values carry the period's year and `notes: nominal`; real values carry the deflator base year; PPP is stated in the statement.

## Corroboration

The researcher writes `corroboration` and `confidence`; the server computes the rest.

| Status | When | What to do |
|---|---|---|
| `single_source` | One source, or several in one `independence_group` | Default; the memo lists it as a gap if the claim matters |
| `corroborated` | Two or more independent sources agree within their own rounding (estimates: overlapping ranges) | Attach all; note small differences in `notes` |
| `contested` | Independent sources disagree beyond rounding and neither is superseded | One record; statement gives the range; `confidence: low`; both sides in `notes`; the Principal resolves |
| `refuted` | A higher-tier or later source contradicts the claim | Set `status: withdrawn`; `notes` points to the replacing record; never delete |

## The two-source rule as the server computes it

```
usable = [s for s in evidence.sources if s.tier in ("A", "B")]
validated = ( any(s.tier == "A" for s in usable)
              or len({s.independence_group for s in usable}) >= 2 )
            and evidence.corroboration not in ("contested", "refuted")
grade = best tier among all sources
independence_count = distinct independence_group values among all sources
```

Consequences: one Tier-A source validates alone, even at `single_source`; two Tier-B sources in one group do not; A plus C validates through the A; two C sources never validate; `independence_count` can be 2 while `validated` is false (B plus C). Clients never write `grade`, `independence_count` or `validated` (integrity rule 3); `update` rejects them. Unvalidated evidence, or evidence below the engagement `grade_floor` (default B), appears in T0 or T1 material only marked indicative and as a range (rule 6). A retracted or superseded source is removed from `evidence.sources` by the Principal with a reason; the computation is not relied on to ignore it.

## Who writes what

| Researcher or interviewer writes | Principal confirms or writes |
|---|---|
| `sources` with tier, rationale, group, interest, snapshot | Resolution of `contested` records; re-grading after a retraction |
| `evidence`: statement, kind, value, sources, corroboration, confidence, attribution, `research_question`, `about`, proposed `supports` and `contradicts` | `hypotheses` status, `evidence_for` and `evidence_against`; `stakeholders` stance and predictions |
| A second source appended to an existing record | Marking evidence `superseded`; ordering the second-source pass for material single-source claims |
| The research memo as an `analyses` record | Whether a claim is fit for a T0 or T1 exhibit |

## `create` call shapes

Fixture content; values are placeholders, not findings. The server stamps `id`, `created_at`, `updated_at`, `session_id`, `schema_version` and the computed fields.

```json
{"collection": "sources",
 "record": {
  "title": "Economic Census 2025, volume 2: enterprises by size class and governorate",
  "type": "official_statistics",
  "publisher": "Central Agency for Public Mobilization and Statistics (CAPMAS)",
  "publication_date": "2026-02-15",
  "url": "<exact URL fetched>",
  "citation": "CAPMAS (2026). Economic Census 2025, vol. 2, table 4.2. Cairo. Retrieved 2 November 2026.",
  "tier": "A",
  "tier_rationale": "Official statistics from the national statistical office with methodology annex; Tier A by type. No interest in the e-invoicing question.",
  "independence_group": "capmas-economic-census-2025",
  "interest_declared": "none",
  "access": {"retrieved_at": "2026-11-02T09:14:00Z", "retrieved_by": "researcher:r-2026-11-02-03",
             "snapshot_path": "library/incoming/sha256-3f9a1c0e7b2d.pdf", "hash": "sha256:3f9a1c0e7b2d...", "paywalled": false},
  "language": "ar", "geography": "EGY", "status": "active",
  "confidentiality": "public", "phase": "P2", "created_by": "researcher:r-2026-11-02-03",
  "tags": ["RQ-03", "baseline"]}}
```

```json
{"collection": "evidence",
 "record": {
  "statement": "In 2025, 18 per cent of registered micro-enterprises in Egypt issued at least one electronic invoice.",
  "kind": "statistic",
  "value": {"number": 18, "unit": "percent", "period": "2025", "geography": "EGY", "as_of": "2026-03-31"},
  "sources": ["SRC-0022", "SRC-0031"],
  "corroboration": "corroborated",
  "confidence": "high",
  "research_question": "RQ-03",
  "supports": ["HYP-02"],
  "about": ["OPT-B"],
  "status": "active", "confidentiality": "client-confidential", "phase": "P2",
  "created_by": "researcher:r-2026-11-02-03",
  "notes": "SRC-0022 table 4.2, denominator registered micro-enterprises; SRC-0031 p. 17 gives 18.4 on the same base, within rounding."}}
```

Evidence takes the most restrictive confidentiality of its sources; the Principal may open public-source evidence to `public` for T3 material. For a data pull, `access.query` holds the exact request and the title names the series code (data-connectors.md). For an interview, `type: interview`, `access.snapshot_path` is the verified transcript and `confidentiality: client-confidential` (interview-capture.md).

## Snapshots

Integrity rule 16: every web or document source at Tier A to C needs `snapshot_path` and `hash`; take them for D and E too, because posts disappear. Procedure: `scripts/snapshot.py fetch <url>` stores a page as a single-file archive plus extracted text, or a PDF or raw API response as is, under `library/incoming/sha256-<prefix>.<ext>` and prints the SHA-256; `create` the source with that path; once the ID returns, `snapshot.py finalise <hash> SRC-0022` renames the file to `library/SRC-0022.<ext>` and the researcher `update`s `access.snapshot_path` with the reason "snapshot finalised". Paywalled: store the copy accessed if the licence allows, set `paywalled: true`, cite normally. Never snapshot anything behind a login.

## Citation format

`citation` holds the form that may appear in a deliverable footnote; table, page and turn detail goes in the evidence `notes`.

- Document: Publisher (Year). Title, document type and reference. Place. Date. Retrieved date.
- Data: Producer, dataset, series code and label, geography, period, vintage date, retrieved date "via API".
- Legal: jurisdiction, instrument title and number, article, gazette or journal and date.
- Parliamentary: chamber, record, date, column or page.
- Peer-reviewed: authors (year), title, journal, volume(issue), pages, DOI.
- Interview, by attribution. `on_record`: "Interview, Deputy Minister for Digital Transformation, 12 November 2026 (MTG-007)". `background`: "Interview with a senior official of the ministry, November 2026". `not_for_attribution`: "Stakeholder interview, November 2026".

Exhibit source lines read "Source: CAPMAS Economic Census 2025, table 4.2; ETA e-invoicing register, March 2026; Horus analysis." The traceability view resolves each line through evidence IDs.

## Proposed schema additions

`evidence.turn_refs[] {meeting: → MTG, from_turn, to_turn}` for interview evidence, replacing the `notes` convention; a controlled `value.unit` vocabulary in the schema package; `value.nominal: bool`.

Source: STATE_SCHEMA.md §C1, §C2 and integrity rules 3, 4, 6 and 16; ARCHITECTURE.md §8.
