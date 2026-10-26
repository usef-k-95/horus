# Horus backend

Two packages share this project:

- `horus_meet` — the live-meeting runtime (build step 0 spike onwards): provider adapters for the meeting bot and speech, turn-taking, the per-meeting session state machine, the spike runner and the `horus-meet` command line.
- `horus_state` — the engagement-state server (build step 1; not yet present).

## Setup

```bash
./uvw sync --extra dev
./uvw run pytest
./uvw run horus-meet check-env
./uvw run horus-meet mock-run
```

## Environment notes (macOS)

- This project folder sits under `~/Desktop`, which iCloud Drive syncs on this machine. iCloud deleted files inside `.venv` and replaced a `.venv` symlink with an empty folder during development, so the environment must live outside synced folders. The `./uvw` wrapper runs `uv` with `UV_PROJECT_ENVIRONMENT=~/Library/Caches/horus/backend-venv` and finds `uv` even when it is not on `PATH`. Use it for every command here (`./uvw sync --extra dev`, `./uvw run pytest`, `./uvw run horus-meet …`). Moving the whole repository out of iCloud-synced folders (for example to `~/Horus/`) is the cleaner long-term fix.
- `uv` is pinned to `link-mode = "copy"` in `pyproject.toml`: with the default clone mode the environment's files carried the macOS hidden flag, and Python 3.12 skips hidden `.pth` files, which breaks the editable install.
- `uv` was installed at user level with `python3 -m pip install --user uv`; it lives at `~/Library/Python/3.9/bin/uv`.
- Never run two `uv` commands against the same environment at the same time.

The real spike needs provider credentials in `backend/.env` (see `.env.example`) and test meeting links; the runbook is `docs/SPIKE-0-live-meetings.md`.
