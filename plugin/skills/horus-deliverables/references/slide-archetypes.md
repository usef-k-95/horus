# Slide archetype library

The slide types Horus is allowed to build, each with its purpose, layout, chart rules, text limits and an example action title. `producer` renders only archetypes listed here; a new slide type is a change to this file, not an improvisation in a deck.

When Horus uses this: when the Principal assigns an archetype to every storyboard slide (`Archetype:` key) and when `producer` renders a deck or runs the visual and logic audits against it.

## Shared layout

All archetypes sit on the 16:9 master (338.7 by 190.5 mm) and use the zones below. Coordinates are from the top-left corner; the design system file holds type sizes and colours.

| Zone | Position | Content |
|---|---|---|
| Tracker | x 12.7 to 200 mm, y 6 to 10 mm | Section label in capitals, current section emphasised; "Back-up" on appendix pages |
| Stamp | right-aligned to x 326 mm, y 6 to 10 mm | WORKING DRAFT, DRAFT FOR DISCUSSION or FINAL |
| Title zone | x 12.7 to 326 mm, y 12 to 40 mm | Action title, left-aligned, at most two lines, no terminal full stop |
| Body grid | x 12.7 to 326 mm, y 46 to 160 mm; 12 columns of 22.4 mm with 4 mm gutters | Exhibit, text and panels on the grids below |
| Source line | x 12.7 to 326 mm, y 164 to 176 mm | Numbered footnotes, then "Source:" line; present on every page with an exhibit or a number |
| Footer | y 180 to 186 mm, hairline rule above | Confidentiality marking left, page number right |

Body grids: **12** (one exhibit or table full width); **8+4** (exhibit in columns 1 to 8, implication panel in 9 to 12); **6+6**; **4+4+4**; **3 by 2** (six cards). The implication panel is a hairline box with a bold lead phrase and at most 25 words; it carries the storyboard's "So what".

## Text limits per tier

| Tier | Action title | Body words | Bullets | Tables | Chart labels | Footnotes and source |
|---|---|---|---|---|---|---|
| T0 | 28 to 32 pt, at most 14 words, two lines | 40 | 3, one line each | 4 rows by 3 columns | 18 pt | 12 pt |
| T1 | 24 to 28 pt, at most 20 words, two lines | 80 | 5, at most 12 words each | 7 rows by 6 columns | 12 pt minimum, 14 pt preferred | 10 pt |
| T2 | 24 pt, at most 20 words, two lines | 120 | 7 | 12 rows by 8 columns; 12 pt cells allowed in back-up only | 12 pt | 10 pt |

Direct labels on charts count as chart labels, not body words. Every number on a slide resolves to an evidence ID in the storyboard.

## Content archetypes

Example titles come from the fictional e-invoicing case in storyline-and-ghost-deck.md; their figures are illustrative.

| Id | Purpose | Body grid and exhibit | Chart and content rules | Example action title |
|---|---|---|---|---|
| `executive-summary` | State the governing thought and key line on one page | 12: title is the governing thought; three to five numbered statements with one supporting line each; no exhibit | Each statement reappears word for word as a slide title; numbers footnoted; T0 variant has three statements within 40 words | A phased mandate paired with free tooling closes the micro-firm gap at the lowest compliance cost |
| `context-mandate` | Record what was asked and how Horus reads it | 6+6: mandate as given (`brief.problem_statement.as_given`, objectives OBJ-n) left; reframing, scope in and out right | RFP wording quoted verbatim with its DOC id; no chart | The mandate asks for higher take-up; the underlying problem is the cost of compliance for micro-firms |
| `problem-issue-tree` | Decompose the problem into the questions the work answers | 12: tree drawn left to right, root then three to five branches, leaves tagged with HYP ids and a status glyph | Branches MECE and in parallel grammar; leaves at most eight words; status by glyph and label, never colour alone | Low take-up comes down to three questions: cost, capability and incentive |
| `baseline-trend` | Show the starting point and its trajectory | 8+4: line or column chart left, implication panel right | One highlight series, the rest grey; endpoints directly labelled; column axes start at zero; units and period in the exhibit heading | Take-up has stalled below one micro-firm in five for three years while large firms are near full coverage |
| `benchmark-table` | Compare the country with chosen comparators | 12: comparators as rows (at most six), dimensions as columns (at most five), home country row emphasised | Every cell sourced to an EVD; mismatched years flagged; "why these comparators" footnote; Harvey balls for qualitative cells | Comparable economies that reached broad coverage all phased the mandate by firm size |
| `stakeholder-landscape` | Map who matters by influence, interest and stance | 8+4: two-axis scatter (influence by interest), marker shape by stance, implications right | Organisations and groups, not named individuals, unless a recorded Principal decision allows; at most 12 markers, all labelled; one colour, shape carries stance | Two merchant associations hold the swing position between the tax authority and the software vendors |
| `sentiment-snapshot` | Show public and media sentiment | 4+4+4: poll result; media tone and volume trend; themes with salience | Each panel sourced; representativeness caveat in a footnote; at most five themes | Public debate centres on cost and privacy, not on the principle of digital invoicing |
| `decision-maker-priorities` | Relate the decision maker's stated priorities to the choice | 6+6: stated priorities with dated public quotes left; what each implies for the options right | Public record only; never profile content; quotes carry speaker, date and EVD id | The minister's three stated priorities favour options that show results before the next budget cycle |
| `option-landscape` | Lay out the long list on two axes | 12 or 8+4: two-axis map (for example impact by ease of implementation), options as labelled markers with OPT codes, do-nothing marked | Axes defined in the exhibit heading; at most nine options; one colour, shape by option kind (all-pairs colour cap applies) | Nine instruments span the space from pure incentives to a hard mandate; four are worth appraising |
| `screening-funnel` | Show how the long list became the shortlist | 8+4: stepped bars from long list to shortlist with the criterion applied at each step; dropped options and reasons right | Criteria from the screening analysis or `decisions[kind=criteria_weights]`; every dropped option named with its reason | Screening on legality, cost and reach leaves three options plus do-nothing |
| `principles-directives` | Present guiding principles and directives for validation | 12: numbered principles (at most six), each one sentence plus what it rules in and out | Wording identical to the proposed `decisions[kind=guiding_principle]`; directive questions phrased as decisions sought | Six guiding principles would rule out a single-date mandate and rule in free tooling |
| `appraisal-comparison` | Compare shortlisted options on the criteria | 12: options as columns including do-nothing, criteria as rows (at most eight), verdict row last | Same baseline and assumptions register for every column; quantified cells as low to high with the central value in bold; Harvey balls for qualitative cells; no colour-coded cells; weights shown when MCA | Option B outperforms on reach and cost; Option C wins only if enforcement capacity doubles |
| `cba-waterfall` | Decompose net benefit into its parts | 8+4: waterfall from zero through costs and benefits to net present value, total bar highlighted | Costs down, benefits up, hairline connectors; price base year, discount rate and ASM id in the footnote; range on the total | Compliance savings outweigh tooling costs twice over at the central estimate |
| `distributional-incidence` | Show who gains and who bears costs | 8+4: diverging bars by affected group centred on zero | Diverging palette with neutral midpoint; groups MECE; per-firm or per-household units stated; equity note in the panel | Micro-firms bear most of the transition cost in year one and most of the benefit from year three |
| `sensitivity-tornado` | Show which assumptions move the result | 8+4: tornado of the result range per assumption, widest first, switching values in labels | Assumptions named with ASM ids; central estimate as a vertical rule; six to eight bars | The result is robust to every assumption except take-up, which switches the ranking at 55 per cent |
| `delivery-trajectory` | Show baseline, target and intervention paths over time | 8+4: line chart with baseline in grey, target as a labelled ink line, intervention in the highlight colour | A vertical "today" rule; milestones as markers; target wording matches the agreed target | Without intervention, coverage reaches the target four years late |
| `operating-model-comparison` | Compare operating-model archetypes | 12: archetypes as columns with the current model first, dimensions as rows (mandate fit, cost, capability, transition risk, legal change) | Harvey balls; legal changes counted, not described; source is the operating-model appraisal | An agency model fits the mandate best but needs two legal amendments the network model avoids |
| `five-case-summary` | Summarise a business case in the Five Case Model | 12: five panels (strategic, economic, commercial, financial, management), each with a status and a one-line finding | Economic panel shows the NPV range and BCR and points to the appraisal summary table; the stage (strategic outline, outline, full) named in the heading | The case is strong on strategy and economics and not yet affordable within the current envelope |
| `service-blueprint` | Show the service journey and what supports it | 12: swimlanes (user actions, front stage, back stage, systems) by journey stage | At most seven stages; pain points marked with a glyph and label; no colour-only coding | Three of seven journey steps fail for firms without a smartphone |
| `risk-matrix` | Show the main risks by likelihood and impact | 8+4: five-by-five grid with numbered risks; top risks with owners and mitigations right | Risks carry RSK ids; at most ten plotted; if RAG is used, status colours with glyphs and labels | Two risks, vendor readiness and enforcement capacity, dominate the register |
| `roadmap-delivery-chain` | Sequence actions and show who delivers | 12: bars by workstream over quarters with milestone diamonds, or a delivery-chain diagram | Owners named per row (STK); instruments required marked; at most eight rows | A 24-month roadmap sequences tooling before obligations and enforcement last |
| `governance-raci` | Show decision rights | 12: RACI or RAPID table, roles as columns (at most seven), decisions as rows (at most eight) | One letter per cell; exactly one decider per row; wording matches the governance decision | Decision rights place the tax authority as decider and the SME agency as recommender |
| `kpi-dashboard` | Show the indicators that will track success | 12: 3 by 2 stat tiles or a table with baseline, target, source, frequency and owner | At most six indicators; every indicator has a baseline and a dated target; no colour-only status | Six indicators track reach, cost and compliance from a 2025 baseline |
| `communication-matrix` | Show messages by audience | 12: audiences as rows; objective, message, channel, timing and spokesperson as columns | Audiences MECE; messages at most 15 words; content from the communication-plan analysis | Each of five audiences hears the same core message with a different proof point |
| `decisions-sought` | State the decisions the meeting must take | 12: numbered decisions worded "Agree that" or "Note that", each with approve, amend or reject | Mirrors `meetings.decisions_sought`; at most four; no new information | The steering committee is asked to take three decisions today |
| `next-steps` | Set out what happens next | 12: table of action, owner and date (at most eight rows) | Owners are named roles; dates are dates; rows mirror `actions` records | Three actions in the next two weeks keep the appraisal on schedule |

## Structural archetypes

Not in ARCHITECTURE.md §7.3 but required to assemble a deck.

| Id | Purpose | Rules |
|---|---|---|
| `cover` | Open the deck | Deck title, meeting, client entity, date, stamp and confidentiality marking; no page number, no tracker |
| `road-marker` | Show the agenda and the current position | The full agenda re-shown at the start of every section with the current section emphasised (BENCHMARKS.md A3); section labels match the `Section:` keys |
| `backup` | Carry proof for a Tier 1 or Tier 2 claim | Any content archetype rendered in the appendix: "Back-up" in the tracker, the T2 table limits, the slide it supports named in the footnote |

## Executive-tier variants (Tier 0)

Any archetype rendered for Tier 0 obeys these overrides: title 28 to 32 pt; body at most 40 words; every character other than the source line at 18 pt or larger, the source line at 12 pt or larger; one exhibit with at most five directly labelled data points, or no exhibit; tables at most four rows by three columns; no footnotes beyond the source line; the "so what" is in the title itself. Only these archetypes appear at Tier 0: `executive-summary`, `baseline-trend`, `appraisal-comparison` (at most four options and four criteria), `cba-waterfall` (at most four bars) or `distributional-incidence`, `roadmap-delivery-chain` (at most four rows), `risk-matrix` (top three risks as text), `decisions-sought` and `next-steps`. The five-to-eight-slide brief runs: executive-summary, baseline-trend, appraisal-comparison, cba-waterfall or distributional-incidence, roadmap, decisions-sought, with risks and next steps optional. Every Tier 0 number also appears in the Tier 2 traceability table.

Source: archetype list from ARCHITECTURE.md §7.3; chart rules from the `dataviz` skill; road-marker, action-title, kicker and back-up conventions observed in BENCHMARKS.md A3.
