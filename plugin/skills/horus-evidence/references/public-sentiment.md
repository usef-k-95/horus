# Public sentiment

Public sentiment is measured by triangulating four signals (polls, media tone and volume, search interest, and coded public discourse) against the stated positions of organised stakeholders, and recorded as a `public_sentiment` analysis in which every topline and illustrative quote is an evidence record. This file names the instruments, sets the coding rules, gives the analysis shape, and lists what Horus never does.

**When Horus uses this:** P2 diagnosis for any question with a public dimension; before the principles workshop (AP3) when options touch citizens or small firms; the communication plan in P5.

## Four signals and one anchor

| Signal | What it measures | Tier | Instruments |
|---|---|---|---|
| Polls | Stated attitudes of a defined population | B (`poll`) | See below |
| Media | How much and in what tone monitored news covers the topic | B for volume and tone claims only (`dataset`); C per article | GDELT 2.0 DOC API; national outlets' archives |
| Search interest | Relative attention over time and across regions | C (`dataset`) | Google Trends, through the unofficial `pytrends` route or a manual export |
| Coded discourse | Themes, direction and intensity in public talk | E (`social_media`); C for op-eds and letters (`news`) | Web search of public posts, comment pages, op-eds, phone-in transcripts, consultation submissions |
| Stakeholder statements (anchor) | Official positions of organised groups | A own statement (`speech_or_statement`, `advocacy`) | Associations, unions, parties, consumer bodies |

No single signal is public opinion. Polls are the only signal that estimates a population; the other three show attention, tone and vocabulary.

## Polls

Reputable producers with published methodology: Pew Research Center; Gallup World Poll; Ipsos, YouGov and Verian (formerly Kantar Public) where sponsor and method are disclosed; the OECD Survey on Drivers of Trust in Public Institutions; the regional barometers (Eurobarometer standard and flash waves, Afrobarometer, Arab Barometer, Latinobarómetro, AmericasBarometer, Asian Barometer); the World Values Survey and the European Social Survey; national statistical offices' opinion modules; national election studies. National pollsters are admitted when they publish method and sit inside a disclosure regime (ICC/ESOMAR code and WAPOR guideline, AAPOR Transparency Initiative, British Polling Council rules), or when two independent polls agree.

Record each poll as a `poll` source (Tier B) with sponsor, fieldwork dates, mode, sample size and design, population, weighting and the verbatim question in `notes`; each topline as `statistic` evidence with `value {number, unit: percent, period: fieldwork dates, geography}` and `about` set to the `public_segment` stakeholder. A poll sponsored by a party to the question carries that interest and stays `single_source` until an independent poll agrees. Trends need the same wording and mode across waves. A poll on a neighbouring question is context, not a topline on ours.

## Media tone and volume

The GDELT 2.0 DOC API returns article lists and time lines of coverage volume (share of all monitored articles, or raw counts) and average tone for a query, filterable by source country, language and domain, from 2017 onward. Use it for when attention rose and fell, which events drove spikes, whether tone moved, and which outlets carry the topic. Record each pull as a `dataset` source with the exact query, and the resulting claims as `statistic` or `finding` evidence about coverage, never about opinion ("online news coverage of e-invoicing in Egypt tripled in the month after the phase announcement" is a media claim). Caveats to carry: GDELT monitors the online news it can reach, with a changing source mix; non-English coverage is machine translated; tone is a dictionary score; syndication inflates counts; press coverage tracks elite debate, not the public. Complement it with the archives of the outlets the client's audiences actually read.

## Search interest

Google Trends gives a normalised 0 to 100 index of relative query share, sampled, with regional comparison. Use it for timing and relative regional attention; never report the index as a level, a count or a share of people. Record query terms, geography, period and category; re-run at the deliverable date because the sample changes. `pytrends` is unofficial and breaks; a manual export is acceptable, snapshotted.

## Coding public discourse

Sample public text found through search. Keep a codebook at `analysis/sentiment/<topic>_codebook.md`: theme labels; direction (favourable, unfavourable, mixed); intensity (1 to 3); the speaker's segment where the text itself shows it (merchant, accountant, consumer, official), never inferred from the person. Code at least fifty items per reported theme; report counts of items, never shares of people. Illustrative quotes become `quote` evidence at Tier E with `quote_text` verbatim, the speaker set to the `public_segment` stakeholder, handles, names and identifying detail removed, and the snapshot kept in `library/` at `client-confidential`. Op-eds by public figures are `position` evidence at the author's own-statement tier.

## Stakeholder statements

Positions of associations, unions, parties, consumer bodies and large firms are `position` evidence (own statement, Tier A for the position) and anchor the segment analysis: a theme that organised groups also voice carries more weight than one found only in comments, and a theme no organised group voices may be a vocal minority or an unrepresented interest; say which.

## Triangulation and confidence

Converging polls, media, search and discourse: `high`. Polls present but older than the main event, other signals converging: `medium`. Media and search only: `low`, and the analysis speaks of attention, not opinion. Discourse alone: `low`, qualitative, no shares. Divergence between polls and discourse is itself a finding (vocal minority, or a poll question that missed the issue).

## The `public_sentiment` analysis

`content`: `topic`; `population` (whose opinion, with the segments covered and not covered); `period`; `themes[] {theme, salience 1-5, direction, intensity, segments[], illustrative: → EVD[]}`; `polls: → EVD[]`; `media {volume_trend, tone}`; `search_interest`; `caveats[]`. Common fields: `inputs`, `method_notes` (codebook path, queries, dates), `findings[]` with confidence, `limitations[]`. Salience is ranked across themes from polls first, then coded-item counts, then media volume. Every theme has at least one illustrative EVD. The "public sentiment snapshot" slide shows polls with fieldwork dates and n, a volume line, and themes with direction; quotes appear only from public figures on the record or anonymised by segment.

## Representativeness caveats

State in `caveats[]`: internet and platform penetration and who is absent (informal firms, rural, older, non-literate); language of search versus languages of the public; urban bias of online news; platform demographics; bot and campaign activity, especially around announcements; event spikes and decay; question wording and order; sponsor effects; mode (mobile, face-to-face) and non-response; social desirability on compliance and tax topics; sample sizes behind sub-group splits; the gap between stated attitude and behaviour.

## Never

Profile or list individual members of the public, critics or commenters; buy or scrape social data behind logins or through paid listening tools that return personal data; infer demographics or affiliations of individuals; treat comments, likes, shares or petition counts as polls; present volume as prevalence; use E-tier material for any fact; quote private individuals identifiably; post, reply, survey or run experiments on platforms (Horus never speaks in public); claim a population view from any signal but a documented poll.

## Proposed schema additions

`sources.poll_metadata {sponsor, fieldwork_from, fieldwork_to, mode, n, population, weighting, margin_of_error}` so poll quality is queryable rather than buried in `notes`.

Source: ARCHITECTURE.md §8; STATE_SCHEMA.md §D1 `public_sentiment`; AAPOR Transparency Initiative and the ICC/ESOMAR International Code with the WAPOR/ESOMAR guideline on opinion polls; GDELT Project documentation of the DOC 2.0 API.
