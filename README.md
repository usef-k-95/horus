# Horus — AI-native policy advisory (MVP)

Horus is an AI-native policy advisory firm. It executes end-to-end advisory engagements (RFP → classification into an advisory pathway → research → live stakeholder interviews → options → appraisal → recommendation, implementation and communication plans) as a **Claude Code plugin** backed by a **lightweight backend** (engagement state and a live-meeting runtime), under a human Supervisor who approves sensitive actions and can intervene.

## Status

Build in progress (26 October 2026). The backend (`backend/`: engagement state, MeetStream live-meeting runtime, mail, appraisal toolkit) and the plugin (`plugin/`: skills, agents, hooks, MCP launchers) exist and pass their tests; real meetings and mail need the Supervisor's accounts (see `docs/SPIKE-0-live-meetings.md`).

| Document | Contents |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Plugin architecture v0.2: principles, supervision model (Supervisor, autonomy levels, shadow mode), components (Principal, 4 skills, 4 workers including the live `interviewer`, `horus-state` and `horus-meet` servers, hooks), advisory pathways and the common lifecycle, orchestration patterns, deliverable system per pathway, integrations, security and consent, build plan, decisions needed |
| [docs/STATE_SCHEMA.md](docs/STATE_SCHEMA.md) | Project-state schema v0.2: storage model, conventions, 4 singletons, 19 collections (including approvals and appraisals) and an event log with full field definitions, enumerations (pathways, autonomy levels, action classes), relationship map, integrity rules, gate checklists, backend API for both servers, views, concurrency and migration |
| [docs/SPIKE-0-live-meetings.md](docs/SPIKE-0-live-meetings.md) | Live-meeting runbook on MeetStream: what is built, commands, what the Supervisor must set up, verified provider facts |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Decision log and build log |
| [docs/BENCHMARKS.md](docs/BENCHMARKS.md) | Sourced catalogue of the public documents the deliverable standard is benchmarked against: MBB public-sector reports and released decks, OECD, EU, UK and US impact-assessment standards, World Bank, IMF, WEF, HKS and Blavatnik formats, and head-of-government decision-memo conventions |

## Quick start

```bash
cd backend && ./uvw sync --extra dev && ./uvw run pytest
```

Load the plugin in a Claude Code session opened in an engagement folder: `claude --plugin-dir /path/to/Project\ Horus/plugin`. Start an engagement with `/horus:horus-method intake <RFP file>`.

Validate and evaluate the plugin from a logged-in terminal (the desktop app's bundled CLI is not logged in for non-interactive use):

```bash
claude plugin validate ./plugin --strict
```

```bash
claude plugin eval ./plugin --trust-plugin --allow-real-servers --runs 1
```

The eval cases under `evals/` scaffold the fixture engagement (`evals/fixture/`), then test intake and classification, the approval gate on outbound email, and a mock-provider interview.

## Layout

```
plugin/     Claude Code plugin: manifest, skills (horus-method is the /horus:horus-method entry point), agents (researcher, analyst, producer, interviewer), hooks, .mcp.json, launcher scripts
backend/    horus_state (state, rules, approvals, gates, views, MCP server, `horus` console), horus_meet (MeetStream runtime, MCP server, spike), horus_mail (IMAP/SMTP attachments and invites), horus_appraisal (quantitative toolkit)
evals/      plugin eval suite and fixture engagement
docs/       design documents and playbooks
```
