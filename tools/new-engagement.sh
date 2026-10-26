#!/bin/sh
# Start an engagement: creates its folder under ~/Horus/engagements and the empty state.
# Usage: tools/new-engagement.sh CODE "Engagement name" "Client entity" COUNTRY-CODE [path to RFP file]
. "$(dirname "$0")/_common.sh"
code="$1"; name="$2"; entity="$3"; country="$4"; rfp="$5"
[ -n "$code" ] && [ -n "$name" ] && [ -n "$entity" ] && [ -n "$country" ] || die 'usage: tools/new-engagement.sh CODE "Engagement name" "Client entity" EGY [rfp.pdf]'
folder="$ENGAGEMENTS/$code"
[ -d "$folder/.horus" ] && die "an engagement already exists at $folder"
mkdir -p "$folder"
( cd "$BACKEND" && ./uvw run --no-sync horus init "$code" --name "$name" --entity "$entity" --country "$country" --supervisor "$USER" --workspace "$folder" ) || die "could not initialise the engagement"
mkdir -p "$folder/inbox"
if [ -n "$rfp" ]; then
  if [ -f "$rfp" ]; then cp "$rfp" "$folder/inbox/" && ok "RFP copied to inbox/"; else warn "RFP file not found at $rfp. Drop it into $folder/inbox later."; fi
fi
( cd "$folder" && git init -q 2>/dev/null && git add -A >/dev/null 2>&1 && git commit -q -m "Engagement $code initialised" >/dev/null 2>&1 ) || true
say "Engagement folder: $folder"
say "Now open this folder as a new session in the Claude app (Code tab, new session, choose this folder) and say: start the Horus intake from the RFP in inbox."
