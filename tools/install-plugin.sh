#!/bin/sh
# Step 4 (once): deploy the Horus plugin on this Mac so every Claude Code session can use it.
. "$(dirname "$0")/_common.sh"
CL="$(find_claude)" || die "could not find the Claude Code command. Open the Claude app once, then run this again."
say "Registering the Horus plugin with Claude Code…"
"$CL" plugin marketplace add "$REPO" >/dev/null 2>&1 || "$CL" plugin marketplace update horus-local >/dev/null 2>&1 || true
if "$CL" plugin list 2>/dev/null | grep -q "horus@horus-local"; then
  "$CL" plugin update horus@horus-local 2>&1 | tail -1
else
  "$CL" plugin install horus@horus-local --scope user 2>&1 | tail -1
fi
"$CL" plugin list 2>/dev/null | grep -A3 "horus@horus-local" | sed 's/^/  /'
say "Done. New Claude Code sessions will have Horus. Restart any session that is already open."
