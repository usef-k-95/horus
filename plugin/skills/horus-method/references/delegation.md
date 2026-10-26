# Delegation protocol

Workers exist for throughput, context isolation and real-time operation. You keep every judgment call. Each brief is a written contract; each return is a summary plus records in state.

## Brief templates

**researcher** (`Agent` with subagent `researcher`, model Sonnet; Opus for decision-maker and client-entity profiles):
```
Actor id: researcher:r-<n>
Question or subject: <RQ-id and the question, or the stakeholder to profile, or the comparator country>
Hypotheses to test: <HYP ids and statements>
Scope: <geography, period, sectors>; exclusions: <…>
Outputs: <n> evidence records minimum; sources graded; snapshots saved; a research memo at analysis/research/<RQ>.md registered as an analyses record of kind research_memo
Credibility floor: B (A for any figure that will appear in a deliverable)
Budget: <fetches>
Return: at most 500 words: findings ranked, confidence, gaps, follow-ups, IDs written
```

**analyst** (model Opus):
```
Actor id: analyst:a-<n>
Options: <OPT ids>; baseline: <ANA id or description>; pathway: <id>; appraisal kind: <ria|strategic_options|…>
Method and dimensions: <from the pathway pack>; standards: <…>
Assumptions register: <ASM ids>; add proposed assumptions you need with basis
Outputs: appraisals record(s) at status draft, model files under analysis/models/<OPT>/, charts as PNG or SVG with CSV, sensitivity results
Return: results and sensitivities in at most 500 words, with IDs
```

**producer** (model Opus):
```
Actor id: producer:p-<n>
Deliverable: <DEL id>, type, tier; storyboard: <path>; template: horus-neutral-v1
Evidence IDs used: <…>; audience: <…>; language
Run the five audits and register the version with register_version; do not release
Return: file paths, QA results, issues found, at most 300 words
Review mode: only the file path and the rubric; return the critique memo with severities
```

**interviewer** (model Sonnet for the live loop):
```
Actor id: interviewer:i-<n>
Meeting: <MTG id>, join_url, platform; approved plan: yes (<APV id>)
Participants: <STK ids and one-line profiles>; attribution rule
Conduct per horus-method/references/live-meetings.md; capture per horus-evidence/references/interview-capture.md
Return: coverage, positions, surprises, contradictions, documents promised and shared, directives, interventions received, proposed updates; the debrief path
```

## Parallelism

- Research: one researcher per question, stakeholder or comparator; four to eight at once in P2; respect `settings.research_budget`.
- Appraisal: one analyst per option; all against the same baseline and assumptions register.
- Production: one producer per deliverable; review always in a fresh instance.
- Interviews: one at a time.

## Integrating returns

Read the memo, not the raw material. Update hypotheses yourself. Flag contradictions for a second-source pass. Convert gaps into open questions or new research questions. Confirm the interviewer's `proposed_updates` before they apply. Run `validate` after a batch of worker writes (the SubagentStop hook does this too).
