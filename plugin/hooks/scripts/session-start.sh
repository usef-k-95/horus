#!/bin/sh
# SessionStart: when the working directory is an engagement, inject the resume summary.
WORKSPACE="${CLAUDE_PROJECT_DIR:-$PWD}"
if [ ! -f "$WORKSPACE/.horus/engagement.yaml" ]; then
  echo "Horus plugin loaded. No engagement in this folder. Start one with /horus:horus-method intake <RFP file> (or ask in plain words)."
  exit 0
fi
. "$(dirname "$0")/../../scripts/backend-env.sh" 2>/dev/null || exit 0
echo "# Horus engagement state (resume context)"
HORUS_WORKSPACE="$WORKSPACE" "$BACKEND/uvw" run --no-sync horus status --format context 2>/dev/null || echo "(horus status unavailable: run backend/uvw sync --extra dev)"
echo ""
echo "Operating manual: the horus-method skill. Record everything in state through the horus-state tools; request approvals before anything leaves; checkpoint before you stop."
