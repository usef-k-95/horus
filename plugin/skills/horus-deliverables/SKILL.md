---
name: horus-deliverables
description: How Horus looks and reads to the McKinsey, BCG and Bain standard: audience tiers, answer-first storyline and ghost deck, slide archetypes, design system, document structures, the five QA audits and the partner review, email and meeting formats.
---

# Horus deliverables standard

One storyline drives every tier. Tier 0 is for the head of government or the deciding minister (a two-page decision memo in the ministerial-submission form and a five-to-eight-slide brief, 18 pt or larger, one decision asked). Tier 1 is for the sponsor and steering committee (an executive deck of 10 to 15 slides and an executive summary under 1,000 words). Tier 2 is for the project manager and technical teams (the full deck and the pathway's core documents). Tier 3 is for external stakeholders, scrubbed of client-confidential and sensitive-personal content.

## Division of labour

- The **Principal** writes the storyboard (`references/storyline-and-ghost-deck.md`): every action title, exhibit, body, evidence ID and "so what". The argument is settled before anything is rendered.
- The **producer** renders with the `pptx` and `docx` skills following `references/design-system.md` and `references/slide-archetypes.md`, runs the five audits (`references/qa-audits.md`) and registers the version. A fresh producer in review mode applies the partner-review rubric.
- The Principal fixes the storyline or orders a re-render, then requests the release approval; `release_version` enforces QA, review and approval.

## Files

- `references/storyline-and-ghost-deck.md`: pyramid, SCQA, MECE, horizontal and vertical logic, the storyboard format with a worked example.
- `references/slide-archetypes.md`: the archetype library with layouts, chart rules and tier text limits.
- `references/document-structures.md`: decision memo, policy note, RIA report, strategy document, operating-model blueprint, business case, delivery plan, service design document, meeting plan, debrief, status note and the phase decks.
- `references/design-system.md`: type scale, grid, palette, chart theme, stamps, trackers, confidentiality marks, Arabic and French readiness.
- `references/qa-audits.md`: the five audits and the review rubric with severities.
- `references/formats-and-templates.md`: interview plan, pre-read, minutes, thank-you and follow-up, weekly status, data-request list, tone rules.
- `references/benchmarks-digest.md`: what the public benchmarks show, as rules.
- `scripts/storyboard_lint.py`: checks a storyboard before rendering (title length, archetype ids, evidence IDs exist in state, sources on every exhibit). Run with `backend/uvw run python plugin/skills/horus-deliverables/scripts/storyboard_lint.py <storyboard.md> --workspace <engagement>`.

## Hard rules

Every number has an evidence ID and a source line. Titles are full sentences of at most two lines that read as a story on their own. One message per slide. Type never below the tier floor. Status stamp on every page: `WORKING DRAFT` until QA passes, `DRAFT FOR DISCUSSION` when released for a meeting, `FINAL` when the client approves. Nothing from `profiles` or from off-record interview spans in any client-facing material.
