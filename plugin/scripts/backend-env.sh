#!/bin/sh
# Shared resolver for the Horus backend. The plugin is loaded from the repository with
# `claude --plugin-dir ./plugin`, so the backend is the sibling folder unless HORUS_BACKEND_DIR says otherwise.
HERE="$(cd "$(dirname "$0")" && pwd)"
BACKEND="${HORUS_BACKEND_DIR:-$(cd "$HERE/../../backend" 2>/dev/null && pwd)}"
if [ ! -x "$BACKEND/uvw" ]; then
  echo "horus: backend not found at $BACKEND (set HORUS_BACKEND_DIR)" >&2
  exit 1
fi
WORKSPACE="${HORUS_WORKSPACE:-${CLAUDE_PROJECT_DIR:-$PWD}}"
export BACKEND WORKSPACE
