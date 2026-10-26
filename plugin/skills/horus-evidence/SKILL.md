---
name: horus-evidence
description: How Horus knows things: source grading A to E, the two-source rule, the evidence ledger with snapshots, public-record profiling, public sentiment, benchmarking, interview capture and data connectors. Used whenever evidence is gathered or written.
---

# Horus evidence standard

Every claim Horus uses is a record with graded sources. The server computes whether a claim is `validated`: one Tier A source, or two independent sources at Tier B or better, and no contest. Everything below exists to make that true in practice.

## Grading (summary; detail in `references/source-tiers.md`)

A peer-reviewed research, official statistics, primary legal texts, flagship datasets of the World Bank, IMF and OECD, court and parliamentary records, and a person's own official statements for what that person said. B reports by international organisations, established think tanks and universities, government policy documents, reputable polling. C quality press, for events and quotes, never for statistics without a primary. D trade press, advocacy groups, company materials, encyclopaedic sources for navigation. E social media, blogs, anonymous sources: sentiment signals only, or the speaker's own account.

## The ledger (detail in `references/ledger-protocol.md`)

- One atomic claim per `evidence` record; numbers carry unit, period, geography and date; quotes are verbatim with the speaker.
- Every `sources` record has a tier with a rationale, an independence group, an interest declaration and a snapshot (`scripts/snapshot.py`).
- Workers write with their actor id; the Principal confirms hypotheses and corroboration status.
- Anything that might appear in a deliverable needs validation or is marked indicative in the statement.

## Protocols

- Research memo and brief formats: `references/research-memo.md`.
- People and institutions, public record only, inferences labelled: `references/profiling-protocol.md`.
- Public opinion and sentiment: `references/public-sentiment.md`.
- Comparator jurisdictions: `references/benchmarking-protocol.md`.
- From transcript to evidence, attribution rules, documents and directives given in calls: `references/interview-capture.md`.
- Free data and literature APIs and how a pull becomes a source: `references/data-connectors.md`.

## Scripts (run with `backend/uvw run python <script>` so httpx is available)

- `scripts/snapshot.py fetch <url>` saves the page or PDF under `library/incoming/` with its hash and prints the access block; after `create` returns the source ID, `scripts/snapshot.py finalise <hash-prefix> <SRC-id>` renames it to `library/<SRC-id>.<ext>`. One step when the ID is known: `scripts/snapshot.py <url> library --id SRC-0022`.
- `scripts/connectors/worldbank.py <indicator> <ISO3> [--start Y --end Y]`, `imf.py <indicator> <ISO3>`, `oecd.py <dataflow path> [--filter]`, `openalex.py "<query>" [--n 10]`, `crossref.py <doi>`, `gdelt.py "<query>" [--days 30]`. Each prints the data and a ready-to-use `sources` record body with the query and retrieval time.

## Ethics

Public record only. No private life, health, family or finances of officials. No scraping behind logins. No paid social-media data in the MVP. Assessments of orientation or personality are labelled as assessed, with confidence and the public statements they rest on, and live in `profiles` at `sensitive-personal`. Interview statements are evidence of a position until corroborated; off-record spans never become evidence.
