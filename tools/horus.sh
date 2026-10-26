#!/bin/sh
# The Supervisor console for the engagement in the current folder (or the one named in HORUS_WORKSPACE).
# Examples: tools/horus.sh status | approvals | approve APV-001 | reject APV-001 --note "…" | meet whisper MTG-003 "ask about X" | meet leave MTG-003
. "$(dirname "$0")/_common.sh"
ws="${HORUS_WORKSPACE:-$PWD}"
if [ -n "$1" ] && [ -d "$ENGAGEMENTS/$1/.horus" ]; then ws="$ENGAGEMENTS/$1"; shift; fi
if [ ! -f "$ws/.horus/engagement.yaml" ]; then
  count=0; only=""
  for d in "$ENGAGEMENTS"/*/; do [ -f "$d/.horus/engagement.yaml" ] && { count=$((count+1)); only="${d%/}"; }; done
  if [ "$count" -eq 1 ]; then ws="$only"; warn "using the only engagement: $(basename "$ws")"
  else die "which engagement? Run this from an engagement folder, or put its code first, e.g. ~/Horus/horus CODE status. Engagements: $(ls "$ENGAGEMENTS" 2>/dev/null | tr '\n' ' ')"; fi
fi
cd "$BACKEND" && HORUS_WORKSPACE="$ws" exec ./uvw run --no-sync horus "$@"
