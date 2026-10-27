#!/bin/sh
# Start an engagement. Run it with nothing after it and answer the questions, or give the details:
#   ~/Horus/new-engagement CODE "Engagement name" "Client entity" COUNTRY-CODE [path to the RFP file]
. "$(dirname "$0")/_common.sh"
code="$1"; name="$2"; entity="$3"; country="$4"; rfp="$5"
ask_value() { # ask_value "question" -> the answer typed
  printf '%s: ' "$1" >&2; read -r v; printf '%s' "$v"; }
if [ -z "$code" ]; then
  [ -t 0 ] || die 'run this in the Terminal panel to be asked for the details, or give them: ~/Horus/new-engagement CODE "name" "client" EGY [rfp file]'
  say "New engagement. Answer each question and press Enter."
  code="$(ask_value "1. Short code for the project, letters, digits and dashes (for example the country, the year and a number)")"
  name="$(ask_value "2. Engagement name (what the work is about)")"
  entity="$(ask_value "3. Client entity (the ministry, agency or organisation)")"
  country="$(ask_value "4. Country, as a three-letter code (EGY, SAU, GBR...)")"
  rfp="$(ask_value "5. The RFP or terms of reference: drag the file into this window and press Enter, or just press Enter to add it later")"
fi
code="$(printf '%s' "$code" | tr -d ' ')"
[ -n "$code" ] && [ -n "$name" ] && [ -n "$entity" ] && [ -n "$country" ] || die "all four details are needed: code, name, client entity and country."
printf '%s' "$code" | grep -Eq '^[A-Za-z0-9][A-Za-z0-9._-]*$' || die "the code may only contain letters, digits, dots, dashes and underscores: $code"
country="$(printf '%s' "$country" | tr -d ' ' | tr '[:lower:]' '[:upper:]')"
printf '%s' "$country" | grep -Eq '^[A-Z]{3}$' || die "the country must be a three-letter code such as EGY, SAU or GBR, not: $country"
# a dragged file arrives with quotes or escaped spaces; a typed ~ needs expanding
rfp="$(printf '%s' "$rfp" | sed -e "s/^[\"']//" -e "s/[\"']\$//" -e 's/\\ / /g' -e 's/[[:space:]]*$//')"
case "$rfp" in "~/"*) rfp="$HOME/${rfp#\~/}";; esac
folder="$ENGAGEMENTS/$code"
[ -d "$folder/.horus" ] && die "an engagement with the code $code already exists at $folder"
if [ -t 0 ]; then
  say "About to create this engagement:"
  printf '  code     %s\n  name     %s\n  client   %s\n  country  %s\n  RFP      %s\n' "$code" "$name" "$entity" "$country" "${rfp:-(none yet; drop it into the inbox folder later)}"
  printf '\nCreate it? (y/n): '; read -r yn
  case "$yn" in y|Y|yes|Yes|YES) ;; *) die "nothing was created.";; esac
fi
mkdir -p "$folder"
( cd "$BACKEND" && ./uvw run --no-sync horus init "$code" --name "$name" --entity "$entity" --country "$country" --supervisor "$USER" --workspace "$folder" >/dev/null ) || die "could not initialise the engagement"
ok "engagement $code created"
mkdir -p "$folder/inbox"
if [ -n "$rfp" ]; then
  if [ -f "$rfp" ]; then cp "$rfp" "$folder/inbox/" && ok "RFP copied into the inbox"; else warn "no file found at $rfp; drop the RFP into the inbox folder instead"; fi
fi
( cd "$folder" && git init -q 2>/dev/null && git add -A >/dev/null 2>&1 && git commit -q -m "Engagement $code initialised" >/dev/null 2>&1 ) || true
say "Engagement folder: $folder"
if ! ls -A "$folder/inbox" 2>/dev/null | grep -q .; then
  say "The inbox folder is opening in Finder: drop the RFP and any other client documents into it."
  open "$folder/inbox" 2>/dev/null || true
fi
say "Next: in the Claude app, Code tab, start a new session, choose this folder (home, Horus, engagements, $code), and say: start the Horus intake from the RFP in the inbox."
