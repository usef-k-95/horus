# Horus evals

Run from a logged-in terminal at the repository root:

```bash
claude plugin eval ./plugin --trust-plugin --allow-real-servers --runs 1
```

Each case folder holds `prompt.md` (the task, with frontmatter for runs, turns, timeout and `EVAL_*` environment), `case.yaml` (the scaffold script that initialises the fixture engagement in the sandbox workspace) and `graders/` (file_exists, regex, tool_used and llm graders with weights).

| Case | What it checks |
|---|---|
| `intake-classification` | Intake from the fixture RFP produces a brief, stakeholders, open questions, a problem classification and a pathway, and ends with a checkpoint |
| `approval-gate` | An outbound email to the client PM is drafted and an approval requested; nothing is sent |
| `mock-interview` | A stakeholder interview runs end to end against the mock meeting provider and is written back to state |

The fixture (`fixture/`) is synthetic: the Republic of Meridia and its ministry are fictional. Add cases as the build proceeds: research fan-out with the two-source rule, appraisal with the toolkit, deliverable production with the five audits, gate transitions.
