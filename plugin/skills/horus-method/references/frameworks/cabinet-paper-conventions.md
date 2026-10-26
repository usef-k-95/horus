# Cabinet-paper and ministerial-submission conventions

The formats governments use to put a decision to a minister, cabinet or head of government: the UK ministerial submission and Cabinet paper, the Australian Cabinet submission, Canada's Memorandum to Cabinet and US presidential decision memoranda. Horus's Tier-0 decision memo follows their common rules: a stand-alone issue statement, recommendations worded as decisions, a date for timing, a short discussion, and implementation, consultation, legal and financial sections.

When Horus uses this: P5 for the decision memo and the five-to-eight-slide brief; P1 to learn the client's own submission format and build the deliverable to it.

## What it is

The formats differ in detail and agree on substance. United Kingdom: the ministerial submission runs title, issue (at most 100 words, stating the financial impact), recommendation ("agree that" or "note that", always including the do-nothing option), timing as a date, and a discussion of at most two pages readable in under five minutes covering impact, financial implications, evidence, risks, communications and handling, parliamentary and legal points, then annexes; Cabinet papers are concise, set out benefits, disadvantages and risks, the decisions required and expenditure implications, and are circulated days ahead with the Treasury consulted first. Australia: the Cabinet Handbook requires the issue and decision sought, fit with strategic priorities, time imperatives, benefits, disadvantages and risks, financial impacts and offsets, wider impacts (gender-responsive budgeting, First Nations), implementation strategy and risks, and legislative implications; recommendations are action-oriented and readable in isolation; states impose page limits (Queensland eight pages, New South Wales under ten) and fixed headings. Canada: the Memorandum to Cabinet separates the ministerial recommendation (problem, proposed solution, financial aspects, communications synopsis; the only place for opinion) from the analysis (options, advantages and disadvantages, financial implications, no opinion), with communications plan and drafting instructions as annexes. United States: decision memoranda flow through the Staff Secretary, are kept to about two pages with attachments, and end in approve and disapprove lines.

## When Horus uses it

- Tier-0 decision memo on every pathway: the structure in ARCHITECTURE.md section 7.5 (title, issue, recommendation with do-nothing, timing, discussion, implementation, decision required, annex pointer) is the synthesis of these conventions; the client's own format overrides where it exists.
- Tier-0 brief: the five-to-eight-slide version follows the same order, with the recommendation worded identically.
- P1: Horus asks for the client's submission template and cabinet rules (page limits, clearance requirements, lead times) and records them as constraints.
- QA: the language and logic audits check the memo against the rules below.

## Steps

1. **Obtain the client's format** and rules: template, page limit, clearance sequence (finance, legal, communications), lead time before the meeting.
2. **Write the issue** in 100 words or fewer, stating the decision needed and the financial impact.
3. **Write the recommendations** as decisions ("agree that…", "note that…", "approve…"), each readable in isolation, including the do-nothing option and what happens if nothing is decided.
4. **State timing** as a date and the reason for it.
5. **Write the discussion** within the page limit: impact, evidence, options considered and why rejected, financial and legal implications, risks, consultation and stakeholder positions, communications and handling.
6. **Add implementation**: owners, timeline, first steps; and the standing sections the client's rules require (gender and inclusion, regional, legislative).
7. **Separate opinion from analysis**: the recommendation carries the judgement; the discussion carries evidence without advocacy.
8. **Close with the decision required** and the annex pointer; keep the full analysis in Tier-1 and Tier-2 deliverables.

## Outputs → state records

- `deliverables` of type `decision_memo` (tier `T0`) with `storyboard_path` in the memo's section order and `evidence_used`; the Tier-0 brief as `executive_deck` or `other` with tier `T0`.
- `decisions` of kind `recommendation` with `statement` worded as the memo's recommendation and `alternatives_considered[]`.
- `brief.constraints[]` for format and clearance rules; `workplan.milestones[]` for circulation deadlines.
- `analyses` of kind `implementation_plan` and `communication_plan` as sources of the implementation and handling sections.
- `approvals` for `tier0_tier1_release` and `decision_maker_email`, which are high-risk action classes.

## Pitfalls

- Arguing in the recommendations; they state decisions, and the discussion persuades.
- Omitting the do-nothing option, which every convention requires.
- "Urgent" instead of a date.
- Exceeding the page limit by moving analysis into the body; annex it and keep the memo readable in five minutes.
- Ignoring clearance: a memo the finance ministry has not seen is returned, not decided.

## Source

UK Cabinet Manual (2011) paragraphs 4.28 to 4.31, Civil Service "Working with Ministers" (2015) and the DWP ministerial submission template (BENCHMARKS.md C1); Australian Cabinet Handbook, 16th edition, 2026, paragraph 97, with Queensland and New South Wales guidelines (BENCHMARKS.md C2); Privy Council Office of Canada, Memorandum to Cabinet guidance (BENCHMARKS.md C3); US Staff Secretary practice and presidential decision memoranda (BENCHMARKS.md C4).
