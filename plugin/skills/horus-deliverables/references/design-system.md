# Horus design system

The neutral visual standard for every Horus deck, document and exhibit: type scale per tier, grid, palette with validated hex values, chart theme, status stamps, trackers, confidentiality markings and Arabic and French readiness. Brand assets, when provided, replace values here without changing the rules (DECISIONS.md item 7).

When Horus uses this: whenever `producer` renders or audits a deliverable, and whenever the Principal specifies an exhibit in a storyboard.

## Principles

The data is the only loud thing on the page. One highlight colour per exhibit; everything else recedes. Every number has a source line. Type is large enough for the back of a ministerial meeting room. Nothing decorative: no icons for their own sake, no stock imagery, no gradients, shadows or 3D.

## Typefaces

- **Latin**: Arial in the MVP. It is on every machine, needs no embedding and matches the government conventions in BENCHMARKS.md B5 (Arial 12) and C2 (Arial 11). Noto Sans is the embedded alternative once templates carry fonts. Regular and bold only; italics only for titles of cited documents in footnotes.
- **Arabic**: Noto Naskh Arabic for body text and tables, Noto Kufi Arabic or Noto Sans Arabic for titles and trackers, each with Noto Sans as the Latin fallback.
- **French**: the Latin faces unchanged; capitals keep their accents.
- **Numerals**: tabular figures in tables and on axes; proportional figures in prose and in stat tiles.

## Type scale per tier (points)

| Element | T0 | T1 | T2 | Documents (A4) |
|---|---|---|---|---|
| Tracker and stamp | 10 caps | 10 caps | 10 caps | 9 caps in the header |
| Action title or heading | 28 to 32 | 24 to 28 | 24 | H1 20, H2 16, H3 14, all bold |
| Exhibit heading (what is plotted, units, period) | 18 | 14 | 12 | 12 bold, written as a full sentence |
| Body text | 18 minimum | 14 minimum | 14 minimum | 12, line spacing 1.15, numbered paragraphs |
| Chart labels and axis text | 18 | 12 minimum, 14 preferred | 12 | 10 |
| Table cells | 18 | 14 | 14 (12 in back-up) | 10 to 12 |
| Footnotes and source line | 12 | 10 | 10 | 9 to 10 |
| Footer | 10 | 10 | 10 | 9 |

Nothing on any slide is set below 10 pt; nothing in a document below 9 pt. The memo (T0 document) is 12 pt throughout with the submission-form headings in bold.

## Grid

Slides: 16:9, 338.7 by 190.5 mm; margins 12.7 mm; 12 columns of 22.4 mm with 4 mm gutters; zones as in slide-archetypes.md (tracker and stamp 6 to 10 mm, title 12 to 40 mm, body 46 to 160 mm, footnotes and source 164 to 176 mm, footer 180 to 186 mm). Objects snap to columns; vertical alignment to a 2 mm baseline grid.

Documents: A4 portrait, 25 mm margins, one text column 160 mm wide, exhibits at full text width, tables with a light grey header row (`#f0efec`) and hairline rules only, paragraphs numbered continuously (1, 2, 3) as in the UK impact-assessment template (B5), headings numbered (1, 1.1), page header with stamp left and confidentiality right, footer with "Page x of y" right.

## Palette

Validated against a white surface with the `dataviz` skill's palette validator (OKLab colour difference under simulated protanopia and deuteranopia, WCAG contrast). Re-run it before changing any value: `python3 -I <dataviz skill>/scripts/validate_palette.py "<hex,...>" --mode light --surface "#ffffff"`.

| Role | Hex | Contrast on white | Use |
|---|---|---|---|
| Ink | `#141414` | 18.4:1 | Titles, body, table text, Harvey balls, target lines |
| Secondary ink | `#4a4946` | 9.0:1 | Exhibit headings, panel text, footnotes |
| Muted ink | `#6b6a66` | 5.4:1 | Trackers, stamps, axis labels, source lines, page numbers |
| Highlight | `#184f95` | 8.1:1 (white on it 8.1:1) | The one highlighted series or cell; section rule; FINAL stamp |
| Context grey | `#8c8a84` | 3.5:1 | De-emphasised series, comparators, baseline bars |
| Light grey | `#c3c2b7` | 1.8:1 | Axis and baseline rules, grey fills that carry a direct label |
| Gridline | `#e1e0d9` | hairline only | Horizontal gridlines when needed |
| Table header fill | `#f0efec` | n/a | Header rows, diverging midpoint |
| Surface | `#ffffff` | n/a | Slides and pages |

**Categorical set** for exhibits where several series carry equal weight, assigned in this fixed order and never cycled: 1 `#184f95` blue, 2 `#d95926` orange, 3 `#199e70` teal, 4 `#6250d6` violet, 5 `#c98500` amber. Validation on white: worst adjacent pair under colour-vision deficiency ΔE 9.4 (deuteranopia), worst normal-vision pair ΔE 26.5, every series at least 3:1 against white. Caps: adjacency forms (stacked or grouped bars, lines) at most five series; all-pairs forms (scatter, two-axis maps, bubbles) at most three series, because slot 4 against slot 1 fails the all-pairs floor. Beyond the cap, fold into "Other" or use small multiples; never add a hue.

**Sequential** (heat maps, choropleths, intensity): one blue ramp `#cde2fb`, `#9ec5f4`, `#6da7ec`, `#3987e5`, `#256abf`, `#184f95`, `#0d366b`, used only for continuous fills where the lightest step means "near zero" and may recede into the page (its contrast on white is 1.3:1, so it never carries a discrete mark). Discrete ordered tiers (funnel stages, maturity levels, Harvey-ball fills) use the validated four-step ramp `#86b6ef`, `#5598e7`, `#256abf`, `#104281`, whose lightest step clears 2:1 on white.

**Diverging** (incidence, agree to disagree, delta to baseline): `#184f95` to `#d03b3b` through the neutral midpoint `#f0efec`, equal steps per arm.

**Status** (risk and delivery RAG only, always with a glyph and a word): good `#0ca30c`, warning `#fab219` (ink text on it 10.0:1; never used as text), serious `#ec835a`, critical `#d03b3b`. Status colours never stand in for a series, and a series never wears a status colour.

## Chart theme rules

1. Direct labelling: label the endpoint, the extreme or the series the title is about; a legend is present for two or more series; a single series needs no legend.
2. One highlight colour per exhibit; context in grey. Where the series are the subject, use the categorical set in order.
3. No 3D, no gradients, no shadows, no dashed gridlines, no dual axes; two measures of different scale become two charts or an index.
4. Marks: bars at most 24 px on screen with a 2 mm surface gap between touching bars; lines 2 pt; markers at least 8 px with a surface ring; gridlines and axes hairline, one step off the surface.
5. Column and bar axes start at zero; line charts may truncate only with a visible axis break noted in the footnote.
6. Every exhibit carries an exhibit heading (what is plotted, units, period), a source line ("Source: <citation>; Horus analysis") and, where computed, the assumption IDs, price base year and discount rate in a footnote.
7. Ranges show as low to high with the central estimate in bold; indicative figures (single-source) are labelled "indicative" in the exhibit, not only in the notes.
8. Harvey balls have five states, drawn in ink, with a legend row; ratings never rely on colour.
9. Text never wears a series colour; identity comes from a swatch or line key beside the text.
10. Illustrative or training exhibits say "Illustrative figures" in the source line.
11. Numbers: thousands separated by commas in English (1,250), one decimal at most in titles, three significant figures at most anywhere; "per cent" in prose and "%" on axes and in tables; currency code with the price base year on first use (EGP, 2026 prices); negative values with a minus sign, not brackets; dates as 9 December 2026 in prose and ISO 8601 in tables.

## Status stamps

Capitals, 10 pt, muted ink, letter-spaced, top-right of every page including the cover and back-up; in documents, the page header. The stamp text follows the version status in `deliverables.versions[].status`:

| Version status | Stamp |
|---|---|
| `draft`, `qa_failed`, `qa_passed`, `in_review` | WORKING DRAFT |
| `supervisor_approved`, `sent` | DRAFT FOR DISCUSSION |
| `client_approved` | FINAL (in highlight blue) |
| `superseded` | File unchanged; superseded in state only |

A deck released for a meeting therefore never says WORKING DRAFT, and nothing says FINAL before a `client_approved` record exists.

## Trackers and page numbers

The tracker names the section and position ("Where we are, 2 of 5") and matches the storyboard `Section:` key and the road-marker agenda. Page numbers sit bottom-right on every page except the cover: "7" on Tier 0 and Tier 1 decks, "7 / 48" on Tier 2 decks, continuous through the back-up. Documents number pages "Page x of y" and paragraphs continuously so a reader can cite "paragraph 23".

## Confidentiality markings

Footer left on every page, header right in documents, cover of every deliverable, driven by the records used and the tier:

| Case | Marking |
|---|---|
| Any record at `client-confidential` used; T0, T1, T2 | CONFIDENTIAL. Prepared for <client entity>. Not for onward distribution without permission. |
| Client applies its own protective-marking scheme | The client's marking as recorded in the engagement settings, in the client's wording |
| T3 external material (scrubbed) | No client marking; "Prepared by Horus for discussion with <stakeholder>" |
| Any record at `sensitive-personal` | Never rendered; the sensitivity audit fails the version |

The distribution list on the cover matches `deliverables.audience`.

## Arabic and French readiness

Arabic (right-to-left): mirror the layout, so the title, tracker and bullets are right-aligned and the page number moves bottom-left; set paragraph direction RTL with Latin acronyms, codes and numbers isolated as left-to-right runs so they do not reorder; keep category axes and tables reading right to left and keep time axes in the direction the client's own publications use, recorded in the engagement settings; choose Eastern or Western Arabic numerals per jurisdiction, once, in the engagement settings; Arabic at the same nominal size reads smaller than Latin, so raise every floor in the type scale by 2 pt for Arabic text and check thumbnails; replace Harvey balls and glyphs with mirrored equivalents only where direction carries meaning (arrows, funnels, roadmaps).

French: budget about a fifth more space for text and allow three-line titles only in back-up; use the decimal comma and a thin non-breaking space as the thousands separator (1 250,5); place a thin non-breaking space before colons, semicolons, question and exclamation marks; use « » quotation marks; sentence case throughout; dates as 9 décembre 2026; keep option codes and evidence IDs unchanged.

Both languages are rendered from the same storyboard: the translation is a version of the same deliverable with the same evidence IDs, and the traceability audit runs on each language version.

Source: type floors and zones from ARCHITECTURE.md §7.4; document conventions from BENCHMARKS.md B5 and C2; chart rules and validation method from the `dataviz` skill.
