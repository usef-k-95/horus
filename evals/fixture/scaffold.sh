#!/bin/sh
# Initialise the fixture engagement in the current folder (used by evals and demos).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
BACKEND="${HORUS_BACKEND_DIR:-$HERE/../../backend}"
"$BACKEND/uvw" run --no-sync horus init MER-2026-017-sme-einvoicing --name "Meridia SME e-invoicing policy" --entity "Ministry of Finance, Republic of Meridia" --country MER --supervisor "$USER" --workspace "$PWD"
mkdir -p "$PWD/inbox"
cp "$HERE/rfp.md" "$PWD/inbox/rfp.md"
cp "$HERE/pm-email-1.md" "$PWD/inbox/pm-email-1.md"
echo "fixture engagement ready in $PWD"
