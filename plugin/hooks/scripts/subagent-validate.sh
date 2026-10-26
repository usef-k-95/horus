#!/bin/sh
# SubagentStop: after a worker finishes, surface integrity issues so the Principal integrates clean state.
WORKSPACE="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$WORKSPACE/.horus/engagement.yaml" ] || exit 0
. "$(dirname "$0")/../../scripts/backend-env.sh" 2>/dev/null || exit 0
ISSUES="$(HORUS_WORKSPACE="$WORKSPACE" "$BACKEND/uvw" run --no-sync horus validate 2>/dev/null | grep -E '^\[(error|warning)\]' | head -8 | tr '\n' ' ')"
python3 - "$ISSUES" <<'PY'
import json, sys
issues = sys.argv[1].strip()
if not issues:
    sys.exit(0)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStop", "additionalContext": "Horus validate after the worker run: " + issues + " Resolve dangling references and unvalidated evidence before using the results."}}))
PY
