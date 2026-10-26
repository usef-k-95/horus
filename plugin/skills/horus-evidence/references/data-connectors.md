# Data connectors

Horus pulls statistics, literature, media and legal texts programmatically from free public APIs, and every pull becomes a `sources` record carrying the exact query, the retrieval time, the data vintage and a snapshot of the raw response. This file lists the connectors, what each provides, how a pull maps to the ledger, and the pitfalls.

**When Horus uses this:** `researcher` runs for baselines, benchmarks, literature reviews, media volume and legal provisions; the Principal when checking that a number in a deliverable rests on a stated vintage.

## Connectors

| Connector | Provides | How Horus queries it | Ledger mapping |
|---|---|---|---|
| World Bank Indicators API (WDI and sister databases) | Country-year series by indicator code (for example `NY.GDP.MKTP.CD`, `SL.UEM.TOTL.ZS`, `IT.NET.USER.ZS`, `IC.BUS.NREG`); indicator metadata; a `lastupdated` vintage in the response | Country ISO3, indicator code, date range, source id, JSON format, pagination | `dataset`, Tier A, publisher World Bank; `independence_group` the national producer for pass-through series, else `wb-wdi` |
| IMF DataMapper API | World Economic Outlook and Fiscal Monitor indicators by country and year, actuals and projections in one series | Indicator code, country ISO3; the edition read from metadata | `dataset`, Tier A for actuals; projection years become `forecast` evidence; group `imf-weo-<edition>` |
| IMF SDMX data services | IFS, BOP, GFS, CPI and other databases through the SDMX endpoints of the IMF Data portal (the legacy JSON REST service is deprecated; confirm endpoints and dataflow ids at build) | Dataflow, key (frequency, area, indicator), period range | `dataset`, Tier A; group by compiling authority where the series is national |
| OECD SDMX (Data Explorer) | OECD databases as SDMX-JSON or labelled CSV (national accounts, taxation, SME and digital indicators) | Agency, dataflow, version, dimension key, start and end period | `dataset`, Tier A; group `oecd-<dataflow>` |
| ILOSTAT | Labour indicators by country, sex, age and activity, national and ILO modelled, through SDMX and bulk files (for example `UNE_DEAP_SEX_AGE_RT`, `SDG_0831_SEX_ECO_RT`) | Indicator code, country, period, source attribute | `dataset`, Tier A for national-source rows, B for modelled estimates (`ilo-modelled`) |
| OpenAlex | Scholarly works, authors, venues, institutions, topics; DOIs, abstracts, open-access locations, citation counts, a retraction flag, DOAJ membership of venues | Search terms and filters (year, type, venue, topic), polite pool with a contact email | Each cited work becomes a `peer_reviewed` source (A) or `think_tank_report` for working papers (B); the search itself is logged in `method_notes`, not as a source |
| Crossref REST API | Authoritative DOI metadata: title, container, authors, dates, publisher, update notices (corrections, retractions) | DOI lookup; filtered works search; polite pool | DOI validation before any academic source is created; a DOI that does not resolve is not cited |
| Semantic Scholar Graph API | Papers with citations, references, influential-citation counts and machine-generated summaries | Paper search, lookup by DOI, citation graph; API key for workable limits | Navigation and citation chasing; summaries are never evidence; cite the paper by its Crossref-validated DOI |
| GDELT 2.0 DOC API | Full-text search of monitored online news from 2017: article lists, volume time lines (share or raw), tone time lines, source-country and language breakdowns | Query terms and operators (phrase, `sourcelang`, `sourcecountry`, `domain`), mode, start and end datetime, max records | The time-line pull is a `dataset` source (B, volume and tone claims only); each article cited is its own `news` source (C) |
| EUR-Lex | EU legislation, case law and preparatory acts by CELEX number and ELI; consolidated versions; national transposition measures; Cellar SPARQL for metadata | CELEX or ELI, language, consolidation date | `legal_text`, Tier A for Official Journal texts; consolidated texts noted as "for documentation" in `notes` |
| legislation.gov.uk | UK primary and secondary legislation as enacted and as revised, point in time, in XML, HTML and Akoma Ntoso; "changes to legislation" status | Type, year, number, section, version date; `/data.xml` or `/data.akn` suffixes | `legal_text`, Tier A; version date in the title; outstanding unapplied changes flagged in `notes` |
| Federal Register API | US rules, proposed rules, notices and presidential documents with agencies, dates, RIN, docket ids, CFR references, full-text links; public inspection documents | Term, agency, document type, date range; document-number lookup | `legal_text` for rules, `government_document` for notices, Tier A; cite document number and publication date |
| regulations.gov API v4 | US dockets, documents and public comments (API key required) | Docket id, search term, comment-on id; paging by last-modified date beyond the record cap | Dockets and documents as `government_document`; comments only as sentiment signals (E), never counted as opinion |

## How a pull becomes a source record

1. Run the connector script (`scripts/connectors/<connector>.py`); it saves the raw response (JSON, CSV or XML) under `library/incoming/sha256-<prefix>.<ext>` and prints the hash and a source-record skeleton.
2. `create` the `sources` record: `title` naming the dataset, series code and label, geography and period ("World Bank WDI, SL.UEM.TOTL.ZS, unemployment, total, per cent of labour force, modelled ILO estimate, EGY, 2015 to 2025, vintage 2026-09-15"); `type: dataset`; `publisher`; `publication_date` set to the vintage date; `access.query` holding the exact request (endpoint path and every parameter), with `retrieved_at`, `retrieved_by`, `snapshot_path`, `hash`; `tier` and `tier_rationale`; `independence_group`; `interest_declared: none`; `citation` in the data format from ledger-protocol.md.
3. Finalise the snapshot to `library/<SRC-ID>.<ext>`.
4. Create one `evidence` record per data point used, with `value {number, unit, period, geography, as_of: vintage}`; a charted series is one record per point, or one `statistic` per endpoint plus a `finding` for the trend.
5. When a newer vintage is pulled, create the new source and evidence, mark the old source and evidence `superseded` with `notes` pointing forward, and regenerate deliverables from the new ids.

Literature: resolve every DOI through Crossref first; the `peer_reviewed` source carries `doi`, the Crossref-derived citation, `publication_date`, and a snapshot of the open-access PDF or the landing page; OpenAlex abstracts go in `notes` as navigation. GDELT: the query and mode are the source; a tone or volume number is a media claim and the evidence `notes` say so. Legal texts: cite the authentic version (Official Journal, enacted text, Federal Register document) and record which consolidated or revised version was read.

## Pitfalls

- **Rate limits and politeness.** OpenAlex and Crossref expect a contact email and throttle anonymous bursts; Semantic Scholar's unauthenticated limits are low; GDELT blocks rapid-fire queries; OECD limits anonymous use; regulations.gov keys are rate-limited per hour. Cache responses in `library/` and reuse them within a run.
- **Revisions.** National accounts, labour and fiscal series are revised for years; a number pulled in P2 may differ in P5. Record `as_of`, re-pull before the final deliverable, diff against the ledger, update or supersede.
- **Vintage mixing.** One table, one database, one vintage. A national figure beside a WDI figure for another comparator is allowed only with a note in the exhibit source line.
- **Definitions.** ILO modelled versus national; "micro" by headcount versus turnover; national versus ILO unemployment; current versus constant prices, and PPP; calendar versus fiscal years. The definition goes in the statement or `notes`.
- **Projections.** IMF WEO series run past the present; years after the "estimates start after" marker are `forecast` evidence with the edition in `as_of`.
- **Aggregates and breaks.** Regional and income-group aggregates share endpoints with countries; series breaks are flagged in metadata only sometimes; read the footnotes in the raw response.
- **Deprecations.** The IMF legacy REST service is deprecated and OECD.Stat has been replaced by the Data Explorer with new dataflow ids; Doing Business was discontinued in 2021 and Business Ready is not a continuation of it; `pytrends` is unofficial.
- **Licensing and attribution.** World Bank, OECD and ILO data carry Creative Commons attribution licences; GDELT and the legal sources are open; the citation names the producer, not the API.
- **Fabrication guard.** No academic source without a Crossref-resolved DOI or an official URL that was fetched and snapshotted; no statistic without a raw response in `library/`.

## Proposed schema additions

`sources.access.vintage` (date), `access.endpoint` and `access.licence`, so vintage and terms are queryable rather than parsed from the title.

Source: ARCHITECTURE.md §5.8; STATE_SCHEMA.md §C1; the publishers' own API documentation (World Bank, IMF, OECD, ILO, OpenAlex, Crossref, Semantic Scholar, the GDELT Project, the Publications Office of the European Union, The National Archives, the Office of the Federal Register, the eRulemaking Program).
