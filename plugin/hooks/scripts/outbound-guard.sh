#!/bin/sh
# PreToolUse on any send/reply/forward tool: hold for Supervisor confirmation and show which
# communications already carry an approval, so what leaves is always seen.
INPUT="$(cat)"
WORKSPACE="${CLAUDE_PROJECT_DIR:-$PWD}"
APPROVED=""
if [ -f "$WORKSPACE/.horus/engagement.yaml" ]; then
  . "$(dirname "$0")/../../scripts/backend-env.sh" 2>/dev/null
  if [ -n "$BACKEND" ]; then
    APPROVED="$("$BACKEND/uvw" run --no-sync horus --workspace "$WORKSPACE" list communications --filter '{"status":"approved","direction":"outbound"}' 2>/dev/null | head -5 | tr '\n' ';')"
  fi
fi
python3 - "$APPROVED" <<'PY'
import json, sys
approved = sys.argv[1].strip(";")
reason = "Horus outbound guard: a Supervisor confirms every email or message that leaves. "
reason += ("Approved outbound communications in state: " + approved) if approved else "No approved outbound communication is recorded in state; approve one first (horus approve <APV-id>) or confirm here."
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": reason}}))
PY
