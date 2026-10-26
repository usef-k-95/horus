# Source tiers

Horus grades every source A to E before any claim built on it enters the ledger; the grade decides whether a figure stands alone, needs a second independent source, or counts only as a signal. This file gives the grading rules, twenty worked examples, the independence-group and interest conventions, and how to write `tier_rationale`.

**When Horus uses this:** when the `researcher` or `interviewer` creates a `sources` record, and when the Principal reviews a memo, resolves a contested claim or sets a brief's credibility floor.

## The five tiers

| Tier | What belongs here | May support |
|---|---|---|
| A | Peer-reviewed research; official statistics; primary legal texts (gazettes, statutes, regulations, judgments); flagship datasets of the World Bank, IMF and OECD; parliamentary and court records; own official statements, for what the speaker said or wants | Any claim, alone |
| B | Reports and working papers of international organisations, established think tanks and universities; government policy documents and evaluations; reputable polling with published methodology | Any claim, with a second independent source at B or better |
| C | Quality press and wire agencies; consultancy reports without published methods; machine-coded media indices | Events, quotes, that something was said; never a headline figure |
| D | Trade press; advocacy groups and industry associations for the facts they assert; company materials; encyclopaedic sources | Navigation to primaries; never a figure or a contested claim |
| E | Social media, blogs, forums, anonymous sources | Sentiment signals; a speaker's own words when the account is verifiably theirs |

The `type` sets a ceiling; a source may be graded below it, never above, with one exception (rule 3).

## Decision rules

1. **Find the primary.** What did this document itself observe, measure, decide or say? A source reproducing another's number inherits that number's `independence_group` and cannot outrank the primary. Cite the primary when reachable.
2. **Set the ceiling from the type, then move down** for unpublished methods, a direct stake in the exact question, a preprint or draft, an unexplained discrepancy with the primary, or a translation of unknown fidelity. Age does not change the tier; the evidence `as_of` carries it.
3. **Own statements.** A speech, press release, official post, interview turn or position paper is Tier A for what the speaker said, wants or intends, and only for that; for facts it asserts about the world it takes its type tier (C for an interview or speech, D for a position paper). Until the schema carries a per-use cap (note at the end), a document serving both uses gets two source records in one `independence_group`: an own-statement record at Tier A, tagged `own_statement`, its `tier_rationale` opening "Own statement:", and an assertion record at the type tier; only `position` and `quote` evidence may cite the former.
4. **Client documents** are primary for the client's own affairs: administrative data, registers and legal instruments at Tier A; strategies, presentations and internal analyses at Tier B with `interest_declared: government`; projections become `estimate` or `forecast` evidence, never `fact`; all `client-confidential`.
5. **Audit institutions and regulators** publish at Tier B by type; their statistical annexes are Tier A where they are the designated producer.
6. **Retractions and corrections** move the source to `status: retracted` or `superseded`; the Principal re-grades evidence citing it.
7. **When in doubt, grade lower and say why.** Lower tiers remain useful together under the two-source rule.

## Independence groups

Two sources are not independent when one derives from the other or both derive from the same primary. The two-source rule counts distinct `independence_group` values, so naming must be stable: `list` sources for the same publisher and reuse their group before inventing one.

Naming: `<producer>-<dataset-or-document>[-<year>]` for data and documents (`capmas-economic-census-2025`, `wb-wdi`, `imf-article-iv-egy-2026`); `<wire>-<date>-<slug>` for syndicated news; `stk-<nnn>-own` for a stakeholder's own statements on any channel; `client-<entity>` for client documents; `doi:<doi>` for papers.

Same group: a press report of a ministry figure and the ministry report; a poll and its press coverage; IMF and World Bank GDP figures resting on the same national accounts (group by the national statistical office); a minister's speech, the ministry's press release and the minister's post. Independent: two surveys with separate fieldwork; an administrative register and a household survey; an audit institution's evaluation and an academic one on different data; two interviewees from different organisations asserting the same fact (which still does not validate it).

## Interest declarations

`interest_declared` is the publisher's stake in the question at hand, not its nature in general. `none`: statistical offices, courts, journals, international databases, the press when reporting. `government`: a ministry or agency that is a party to the question (its own programme, budget or mandate), and all client documents. `commercial`: companies, consultancies, paid research, sector-funded trade press. `advocacy`: NGOs, campaigns, unions and industry associations. `party`: parties and their institutes. A declared interest does not move the tier; it limits what the source may support (rule 3) and must appear in `tier_rationale`.

## Twenty worked examples

Format: source; `type`; tier; interest; group, note.

1. CAPMAS (Egypt's statistical office), Economic Census tables; `official_statistics`; A; none; `capmas-economic-census-<year>`, cite table numbers.
2. World Bank, WDI series pulled by API; `dataset`; A; none; `wb-wdi`, or the national producer for pass-through series.
3. ILO, ILOSTAT indicator, national-source rows; `dataset`; A; none; `ilostat`; ILO modelled estimates are B, `ilo-modelled`.
4. IMF, Article IV staff report; `io_report`; B; none; `imf-article-iv-<iso3>-<year>`; data tables inherit the authorities' group.
5. OECD, Economic Survey; `io_report`; B; none; `oecd-<series>-<iso3>-<year>`.
6. Journal article with a Crossref-resolved DOI; `peer_reviewed`; A; none; `doi:<doi>`.
7. NBER or CEPR working paper; `think_tank_report`; B; none; not peer-reviewed.
8. Official Gazette text of a law or decree; `legal_text`; A; none; `gazette-<instrument>`, cite articles; unofficial consolidated texts are B.
9. Court of Justice of the EU or national supreme court judgment; `legal_text`; A; none; `court-<case-ref>`.
10. Hansard or a parliamentary committee report; `parliamentary_record`; A; none; `parl-<chamber>-<date>`; committee conclusions are `finding` evidence.
11. Ministry of Finance budget statement; `government_document`; B; government; `mof-budget-<fy>`; audited outturns from the audit institution are A.
12. UK NAO or US GAO performance audit; `government_document`; B; none; `nao-<slug>`; independent of the audited body.
13. Eurobarometer, Afrobarometer, Arab Barometer or Pew topline; `poll`; B; none; `<pollster>-<wave>`; fieldwork dates and n in `notes`.
14. Financial Times report of a ministerial statement; `news`; C; none; the minister's group for the quote; `ft-<date>-<slug>` for own reporting.
15. One Reuters wire story in three national dailies; `news`; C; none; one group `reuters-<date>-<slug>` for all four.
16. Federation of Egyptian Industries position paper; `advocacy`; D, A as own statement; advocacy; `stk-<nnn>-own`; two records when used for both.
17. McKinsey Global Institute report, partial methodology; `consultancy_report`; C, B if data and method published; commercial; `mgi-<slug>`.
18. Payments company annual report or securities filing; `company`; D; commercial; `company-<name>-<year>`; audited statements are reliable for the firm's own accounts, keep D.
19. A minister's post on a verified official account; `social_media`; A as own statement; government; `stk-<nnn>-own`, the speaker's words only.
20. Wikipedia article; `encyclopaedic`; D; none; navigation only, never cited.

Also: an anonymous blog or forum is E (`web-anon-<date>`), sentiment only; an interview yields a position record at A and an assertion record at C (interview-capture.md).

## Writing `tier_rationale`

One to three sentences, in order: what the source is and who produced it; the rule setting the tier (type ceiling, own statement, downgrade); what it may and may not support; the interest.

- "Official statistics from the national statistical office, published tables with methodology annex. Tier A by type. No interest in the e-invoicing question."
- "Own statement: speech by the Minister of Finance on the ministry's site. Tier A for the minister's position and words only; adoption figures quoted in it are recorded against the tax authority's SRC-0022. Interest: government, the ministry owns the programme."
- "Consultancy report; survey described but sample frame and weighting not published. Downgraded from B to C; context only, no figures. Interest: commercial."

A rationale that only restates the tier fails review.

## Proposed schema additions

`sources.own_statement_of: → STK`, with a server rule that such a source counts as Tier A only for `position` or `quote` evidence whose `about` includes that stakeholder, and as its type tier otherwise; this removes the two-record workaround in rule 3.

Source: ARCHITECTURE.md §8; the NATO Admiralty system (source reliability and information credibility graded separately, as tier and corroboration are here); Verification Handbook (European Journalism Centre, 2014) on locating the primary.
