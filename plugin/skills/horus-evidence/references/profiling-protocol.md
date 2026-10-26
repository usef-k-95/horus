# Profiling protocol

Horus researches the people and institutions that will decide, shape or resist a recommendation, from the public record only, and stores the result as a `profiles` record at `sensitive-personal` that never reaches the client. This file sets what may be used, what is forbidden, how assessments are labelled, which fields to fill, the defamation and personal-data checks, and how a profile is distilled into analyses.

**When Horus uses this:** profile runs by the `researcher` (Opus-class) for the ultimate decision maker, the sponsor, steering members, priority-1 stakeholders and the client entity, started in P0 and P1 and refreshed before each gate; and by the Principal when writing `decision_maker_lens` and `internal_politics` analyses.

## Why profiles exist

Advice fails when it ignores who decides and what they can accept. A profile answers four questions: what has this person or body publicly committed to, what have they actually done, how do they decide, and what constraints (calendar, coalition, mandate) bind them. Everything else is noise or intrusion.

## Legitimate sources

Public record, in order of value:

- Official biographies and CVs on government, parliamentary and institutional sites; appointment decrees and gazette notices; organisational charts and annual reports of the institution.
- Speeches, statements, press releases and op-eds by the subject or the institution (Tier A own statements for what was said).
- Parliamentary records: questions, debates, committee testimony, votes; court records where the subject acted in an official capacity.
- Decisions taken: laws signed, budgets presented, programmes launched, appointments made, positions reversed, with dates and outcomes.
- Publications: books, articles, academic work, manifestos the subject signed.
- Quality press profiles and interviews (Tier C: quotes and events; corroborate anything that matters).
- Public posts on the subject's own official or verified accounts, read as published; never follower lists, likes, contact graphs or deleted content.
- Statutory registers of interests, only when a declared interest bears directly on the engagement question, recorded as the register states it.

## Forbidden

Private life, family, relationships, religion, ethnicity, health, sexuality, personal finances beyond statutory declarations; home address, personal numbers and emails, identity numbers, dates of birth beyond the year an official biography gives; family members as subjects (a relative who holds a relevant public office is a stakeholder in their own right, on their own record); anything behind a login (LinkedIn, closed groups, subscriber dossiers), leaked or hacked material, people-search and data-broker sites; anonymous allegations and E-tier claims about conduct; inference of motive or character presented as fact; speculation about health or fitness for office; psychological typologies. A public fact that fails the relevance test below is also left out.

## Labelling

Facts are past tense with a source: "Appointed Deputy Minister in March 2024 (SRC-0061)." Assessments are written as assessments and each carries `confidence` and `basis: → EVD[]` (integrity rule 11): "Assessed reform appetite: high on digital administration, cautious on enforcement against small traders (confidence medium; basis EVD-0071, EVD-0074, EVD-0080)." The basis is the subject's own words or actions, never party membership or office alone. Thin basis means `confidence: low` and a short assessment, or no assessment. `summary` is five factual lines with nothing assessed in it.

## Fields to fill

| Field | How |
|---|---|
| `subject`, `scope`, `summary` | Role, institution, tenure, mandate, one line on relevance; nothing assessed |
| `career`, `education` | From official biographies, each row with `source`; omit education when not public or not relevant |
| `affiliations` | Party and declared memberships from the record; `networks[]` only where membership is public |
| `orientation_assessment` | Axes `economic`, `social`, `governance_style`, `reform_appetite`; one or two lines each; `confidence` and `basis` mandatory; omit an axis rather than guess |
| `priorities_stated` | Themes from speeches and programmes, each tied to an EVD and dated |
| `track_record` | Decisions with dates and outcomes as reported, not judged |
| `positions_on_topic` | Statements on the engagement question, dated, with evidence; include reversals |
| `communication_style` | Observed only, with examples: formats preferred, numbers or narrative, public tone |
| `advisers_and_networks` | Public office-holders and formal advisers as `STK` ids; no informal "circles" |
| `political_calendar` | Elections, budget cycles, reshuffle windows, legislative sessions, anniversaries, each with `relevance` |
| `online_presence` | Official channels only, `official` true or false |
| `controversies_public` | Only what passes the defamation check |
| `structure`, `factions_assessed` | Organisations: units, heads and mandates from charts and gazettes; groupings assessed with `confidence` and `basis`, labelled assessed |
| `implications_for_engagement` | Three to seven lines on framing, options and sequencing; the field the Principal works from |
| `overall_confidence`, `review`, `sources` | Set by the researcher; `review` completed by the Principal |

## Defamation and personal-data checks

Run before `create` and again at `review`.

Defamation, for every negative or contested item: is it a court finding, an official inquiry result, or reported by two independent A or B sources; is it phrased as the record phrases it ("was investigated by", "resigned after", never a characterisation); is the subject's public response included; is it relevant to the engagement question. Any "no" removes the item. Opinion is never recorded as fact.

Personal data: purpose limitation (every field serves `implications_for_engagement`); minimisation (would the Supervisor be comfortable if the subject read the record; a line that embarrasses without informing is cut); storage limitation (profiles are deleted at engagement close unless the Supervisor retains them, and hard-deleted on request with a logged event); access (never exported, never in a client-facing file; the producer's sensitivity audit filters `sensitive-personal`). The Principal sets `review.personal_data_minimised` and `review.defamation_check` to true only after checking, with `reviewed_by` and `date`.

## Distilling into analyses

The profile stays internal. What the client sees comes from two analyses at `client-confidential`:

- `decision_maker_lens` (`subject`, `priorities[]`, `red_lines[]`, `decision_style`, `calendar[]`, `framing_guidance[]`, `profile: → PRF`). `priorities` and `red_lines` come only from `priorities_stated` and `positions_on_topic`, phrased as what the decision maker has said publicly and traceable to own-statement evidence; `decision_style` and `calendar` draw on `communication_style`, `track_record` and `political_calendar` without personal detail; `framing_guidance` is advice to Horus and never appears verbatim in a deliverable. The "decision-maker priorities" slide shows stated priorities with dates and sources, nothing assessed.
- `internal_politics` (`entity`, `units[]`, `positions_by_option[] {unit or person, option, position, rationale, confidence}`, `influence_paths[]`, `watch_points[]`). Built from the organisation profile and interview evidence; positions are attributed to units where possible and to persons only with evidence; `factions_assessed` becomes positions by unit, never a named faction; the client-facing stakeholder landscape shows organisations and stance, not individuals' orientations.

Test for every line of either analysis: could it be read aloud to the subject's chief of staff without damage to the engagement. If not, it is profile material and stays there.

## Proposed schema additions

`profiles.subject_access_requests[] {date, request, fulfilled_at, event}` to log deletion or correction requests and their fulfilment.

Source: ARCHITECTURE.md §8, §9 and §10; STATE_SCHEMA.md §B2 and integrity rule 11; DECISIONS.md item 6; OECD Guidelines on the Protection of Privacy and Transborder Flows of Personal Data (2013 revision) and the GDPR principles of purpose limitation, data minimisation and storage limitation.
