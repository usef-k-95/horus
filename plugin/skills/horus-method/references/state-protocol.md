# State protocol

## What to record when

| Moment | Records |
|---|---|
| RFP received | `documents` (kind rfp), `brief` v0, `open_questions` (clarifications), initial `stakeholders`, `analyses` (problem_classification), `engagement.pathway` |
| Approach agreed | `approach` v1, `workplan` v1, `hypotheses`, `decisions` (methodology, workplan), gate AP1 |
| Research returns | `sources`, `evidence` (by the researcher), `analyses` (research_memo), hypotheses status updates (by you) |
| Any email in or out | `communications`; attachments as `documents`; extracted `client_inputs`, `actions`, `open_questions` |
| A meeting planned | `meetings` (plan, participants, scheduling), `actions` (requests), approval |
| A meeting held | runtime blocks on `meetings`; `evidence` with attribution; `interview_record`; `client_inputs` for directives; `decisions` for a forum's decisions; `actions`; debrief |
| An option designed or screened | `options`, `analyses` (options_screening, stakeholder_reaction_matrix) |
| An appraisal done | `appraisals`, `assumptions`, `risks`, `analyses` (option_comparison) |
| A deliverable produced | `deliverables` with versions (producer registers), QA and review, release after approval |
| Any decision by anyone | `decisions` with kind, made_by, forum or channel, rationale, status |
| Anything you cannot answer | `open_questions` with owner, priority, blocking |
| End of session or phase | `checkpoint` (done, decided, learned, next, blockers) |

## Conventions

- IDs are assigned by the server (`STK-001`, `EVD-0042`); never invent them. Refer to records by ID everywhere.
- Workers declare their actor id on every write: `researcher:r-07`, `analyst:a-02`, `producer:p-03`, `interviewer:i-05`; the Principal writes as `principal`. Write scopes are enforced (rule 26).
- Updates merge dictionaries and replace lists; use `append` to add to a list.
- Computed fields (`grade`, `validated`, `independence_count`, `used_in`, `evidence_used`) are set by the server.
- Singletons (`brief`, `approach`, `workplan`) are versioned: raise `version` when you re-propose them; the server snapshots the previous version.
- Confidentiality: default `client-confidential`; profiles are always `sensitive-personal`; mark public facts `public`.

## Never in state

Passwords, API keys, tokens; private personal data about officials (family, health, finances); verbatim off-record interview content; anything a stakeholder asked to be forgotten.

## Checkpoint

`checkpoint(done=[…], decided=[…], learned=[…], next=[…], blockers=[…])`. The next session starts from it. Write it before you stop, and at every phase end.
