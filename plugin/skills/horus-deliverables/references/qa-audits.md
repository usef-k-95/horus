# QA audits and partner review

The five audits every deliverable version passes before release, written as executable checklists with pass and fail criteria, and the unanchored partner-review rubric with severity levels and what each means for release.

When Horus uses this: `producer` runs the audits on every rendered version and records them in `deliverables.versions[].qa`; a fresh `producer` instance runs the review with only the file and the rubric and writes `deliverables.versions[].review`; the Principal resolves findings before requesting the release approval.

## How audits run

- Inputs: the rendered files (PPTX and PDF, or DOCX and PDF), the storyboard, and the state views for traceability, stakeholders and evidence.
- Run all five in order (visual, logic, traceability, language, sensitivity) even when one fails. Record each as `pass`, `fail` or `n/a` (`n/a` only where an audit cannot apply, for example visual on an email) and write the report to `report_path`, listing every failed item by page or paragraph with the fix.
- Any `fail` sets the version status to `qa_failed`. All `pass` or `n/a` sets `qa_passed`, and the version moves to `in_review`.
- Checks are mechanical wherever possible: thumbnails for visual, text extraction for logic and language, storyboard parsing for traceability, record search for sensitivity. A check that cannot be executed is a fail, not a pass.
- Criteria apply to every page or paragraph; one failing page fails the audit.

## Audit 1: visual

| # | Check | Pass | Fail |
|---|---|---|---|
| V1 | Render a thumbnail of every page at 1280 by 720 and inspect it | Every page renders; no element crosses the page edge or its zone boundary | Any overflow, clipped text or object outside its zone |
| V2 | Overlap | No text box intersects another text box or an exhibit, apart from chart labels placed by design | Any unintended intersection |
| V3 | Orphans and placeholders | No empty placeholder, no "Lorem", "TBD", "XX" or "Click to add"; no title with a single word on its second line; no stray text box | Any found |
| V4 | Type floors | The tier's minimum sizes from design-system.md hold on every page (T0 18 pt body and 12 pt source; T1 and T2 14 pt body, 12 pt labels, 10 pt footnotes) | Any character below the floor |
| V5 | Title | Full sentence, at most two lines, sentence case, no terminal full stop | Any violation |
| V6 | Template compliance | Fonts and colours only from the design system; objects on the grid within 1 mm; exhibit heading, units and source line present on every exhibit | Any off-palette colour, off-template font or missing source line |
| V7 | Stamp, tracker, page number | Present on every page (cover: stamp and marking only); stamp text matches the version status; tracker labels match the road-marker | Any page missing or mismatched |
| V8 | Charts | Direct labels; one highlight colour; legend for two or more series; no 3D, gradients, shadows, dual axes or dashed gridlines; column axes start at zero; ranges shown as low to high | Any violation |
| V9 | Documents | Paragraphs numbered continuously; headings numbered; exhibits numbered and titled as sentences; "Page x of y"; header carries stamp and marking | Any violation |

## Audit 2: logic

| # | Check | Pass | Fail |
|---|---|---|---|
| L1 | Titles-only read-through: extract every action title (for documents, every heading and first sentence) and read in order | The list states the governing thought and key line without the bodies; each title makes one claim; none is a label | Any label title, two-claim title or break in the argument |
| L2 | Governing thought | Appears on the executive-summary slide or in the first paragraph and matches the recommendation in the memo word for word | Different wording across tiers |
| L3 | One message per slide | Body and exhibit support the title and nothing else | Orphan content or a second message |
| L4 | Vertical logic | Every number in the title appears in the exhibit or body; the highlighted data point is the title's number | Any mismatch |
| L5 | MECE | Every grouping has two to five items, no overlaps, no gaps, parallel grammar | Any overlap or gap |
| L6 | Decision structure | Do-nothing present in every comparison; recommendations worded "Agree that" or "Note that"; the decisions-sought slide matches `meetings.decisions_sought` | Missing do-nothing or unmatched decisions |
| L7 | Consistency | The same figures, option codes, names and terms on every slide and across the T0, T1 and T2 versions | Any discrepancy |
| L8 | Length ceilings | T0 memo at most two pages, brief five to eight slides; T1 deck 10 to 15 slides, executive summary under 1,000 words; T2 deck 30 to 60 slides plus back-up; RIA main report and policy note at most 40 pages | Any ceiling exceeded |

## Audit 3: traceability

| # | Check | Pass | Fail |
|---|---|---|---|
| T1 | Enumerate every number, quote and factual claim, excluding page and slide numbers, meeting dates and arithmetic shown on the page | Each maps to an EVD id on the slide's `Evidence:` line, or to an APL or ASM id on its `Draws on:` line | Any unmapped item |
| T2 | Evidence quality | Every cited EVD is `active` and `validated: true`, and its best source meets `engagement.settings.evidence.grade_floor`; single-source figures are labelled "indicative" and shown as ranges; `contested` evidence shows the contest | Any `refuted`, `withdrawn` or `superseded` EVD; any unlabelled single-source figure |
| T3 | Quotes | Verbatim against `quote_text`; attribution per the rule: `on_record` named with title; `background` described by role or group and unnamed; `not_for_attribution` as "interviews indicate" with no identifier | Any misquote or attribution breach |
| T4 | Positions versus facts | Interview statements presented as positions ("the association stated"), never as facts unless corroborated by non-interview sources | Any position presented as fact |
| T5 | Source lines | Every exhibit names its SRC citations and "Horus analysis" where computed; model outputs reference `appraisals.artefacts` | Missing or generic source line ("various sources") |
| T6 | Assumptions | Every model input shown references an ASM id with `status: agreed`, or is labelled a Horus assumption with its range | Unreferenced input |
| T7 | Units | Numbers carry unit, period, currency and price base year as in the EVD `value` object | Any missing unit or base year |
| T8 | Traceability table | Generated for T2 (number, EVD, SRC, grade, slide) and attached as back-up; every T0 and T1 number appears in it | Missing table or missing row |

Tolerance: none. One unresolved item fails the audit.

## Audit 4: language

| # | Check | Pass | Fail |
|---|---|---|---|
| G1 | Register | Senior-executive: active voice, concrete nouns, short sentences; no consultant jargon ("leverage", "synergies", "learnings", "going forward"); no stacked hedges | Any instance in client-facing text |
| G2 | Names and titles | Every person, institution and acronym matches `stakeholders.name`, `stakeholders.title` and `engagement.client`; acronyms defined at first use; T2 carries a glossary | Any error |
| G3 | Numbers | Formats per design-system.md; three significant figures at most; consistent rounding across pages | Any violation |
| G4 | Spelling and terminology | One language variant (British English by default); option names and programme names identical everywhere | Any inconsistency |
| G5 | Sentences and bullets | Titles are sentences; bullets parallel; no bullet over two lines on T0 or T1 | Any violation |
| G6 | Clean file | No comments, tracked changes, hidden slides, internal speaker notes, placeholders or "TBC" | Any found |
| G7 | Decision wording | Recommendations and decisions sought worded as decisions | Any recommendation phrased as a finding |
| G8 | Tier fit | T0 has no methodology and no undefined technical term; T1 shows no raw data tables; T2 carries the method | Any breach |

## Audit 5: sensitivity

| # | Check | Pass | Fail |
|---|---|---|---|
| S1 | Marking | The confidentiality marking matches the tier and the records used, per design-system.md | Wrong or missing marking |
| S2 | Profiles | No content from `profiles` (`sensitive-personal`): search the text for profile field values (career, orientation assessments, controversies, networks); the decision-maker lens appears only as framing | Any match |
| S3 | Internal politics | No named individual's position from `analyses[kind=internal_politics]` in client-facing material; reaction matrices show groups unless a recorded Principal decision names individuals | Any breach |
| S4 | Interview material | No text from `consent.off_record_segments`; `not_for_attribution` and `background` evidence rendered per the rule | Any breach |
| S5 | Personal data | No contact details, no private individuals, nothing beyond what the record requires | Any found |
| S6 | Allegations | No unverified allegation about a named person or firm; "alleged" only with Tier A or B sources and dates | Any found |
| S7 | Audience and distribution | Cover distribution list equals `deliverables.audience`; T3 material contains nothing at `client-confidential` | Any mismatch |
| S8 | Supervision material | No approvals, whispers, interventions or internal notes in client-facing files | Any found |

## Unanchored partner review

A fresh `producer` instance receives only the rendered file and this rubric: no storyboard, no state, no conversation history. It writes a memo (`review.memo_path`) answering the ten questions, lists each finding with a severity, and sets `blockers`, `majors` and `minors`. The Principal fixes or formally accepts every finding; `review.resolved` becomes true only when no blocker remains and every major is fixed or accepted under the release rule below.

| # | Question (who asks it) | Blocker | Major | Minor |
|---|---|---|---|---|
| 1 | What is the answer? Can I state the recommendation in one sentence after the first page? (partner, minister) | No answer on page one, or the answer changes within the document | Answer present but buried or hedged | Answer could be sharper |
| 2 | Do the titles alone tell the story, and does each page prove its title? (partner) | The titles-only read does not make the argument | One or two slides fail vertical logic | Weak wording on a title |
| 3 | What am I asked to decide, by when, and can I accept or reject each item alone? (minister) | No decision, no date, or decisions bundled | Decisions present but not worded as decisions | Reason for the date missing |
| 4 | What happens if I do nothing, and is that compared honestly? (minister, partner) | Do-nothing absent from the comparison | Do-nothing present but not quantified where the options are | Counterfactual thinly described |
| 5 | Would I bet my name on the biggest number? Is every number sourced, with uncertainty where it belongs? (partner) | An unsourced or implausible headline number | Ranges missing on estimates; stale data without a flag | Source line incomplete |
| 6 | Who pays, who gains, and who will be angry? Are their reactions anticipated? (minister) | No distributional view on a policy with losers | Reactions asserted without evidence | Some groups not covered |
| 7 | Can this be implemented: owners, dates, budget, instruments, the first 100 days? (partner, minister) | No implementation section or no owners | Owners named but dates or instruments missing | Sequencing vague |
| 8 | What would the smartest opponent say, and has the document answered it? (partner) | The main counter-argument is unaddressed | Addressed only in back-up | Could be stated more directly |
| 9 | Would any line embarrass the minister if leaked, or expose a stakeholder who spoke in confidence? (minister) | Any sensitive-personal, off-record or defamatory content | Tone that reads as partisan or dismissive of a stakeholder group | Awkward phrasing |
| 10 | Does it look and read like finished senior work: one message per page, no clutter, correct names, within length? (partner) | Wrong names or titles of principals; length ceiling breached | Dense pages, inconsistent terms | Cosmetic defects |

## Severity and release

- **Blocker**: release refused at every tier. Fix, re-run the failing audits and repeat the review.
- **Major**: release refused for T0 and T1. For T2 and internal deliverables the Principal may release with the finding logged on the version and the fix named in the next version's `change_summary`.
- **Minor**: release allowed; logged on the version; fixed in the next version.
- Release then requires all five audits at `pass` or `n/a`, `review.resolved: true`, and the approval record the autonomy policy demands (action classes `tier0_tier1_release` and `tier2_release`; Tier 0 release is `high` risk). Only then may the version move to `supervisor_approved` and `sent`, and the stamp to DRAFT FOR DISCUSSION.

Source: audits and review as defined in ARCHITECTURE.md §7.6; version fields from STATE_SCHEMA.md F1; attribution and evidence rules from ARCHITECTURE.md §8.
