#!/bin/sh
# Shared helpers for the Horus tools. Plain language messages; no jargon where avoidable.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$REPO/backend"
ENV_FILE="$BACKEND/.env"
HORUS_HOME="$HOME/Horus"
ENGAGEMENTS="$HORUS_HOME/engagements"
CONFIG_DIR="$HOME/.horus"
mkdir -p "$CONFIG_DIR"
# remember where the backend lives so the installed plugin can find it from any folder
printf 'HORUS_BACKEND_DIR="%s"\n' "$BACKEND" > "$CONFIG_DIR/config"

say()  { printf '\n%s\n' "$*"; }
ok()   { printf '  ✓ %s\n' "$*"; }
warn() { printf '  ! %s\n' "$*"; }
die()  { printf '\n  ✗ %s\n\n' "$*" >&2; exit 1; }

NGROK_CFG="$HOME/Library/Application Support/ngrok/ngrok.yml"
ngrok_has_token() { [ -f "$NGROK_CFG" ] && grep -Eq '^[[:space:]]*authtoken:[[:space:]]*[A-Za-z0-9_.-]+' "$NGROK_CFG"; }

find_claude() {
  if command -v claude >/dev/null 2>&1; then command -v claude; return; fi
  for c in "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  return 1
}

set_env() { # set_env KEY VALUE  (writes or replaces KEY=VALUE in backend/.env)
  key="$1"; value="$2"
  [ -f "$ENV_FILE" ] || cp "$BACKEND/.env.example" "$ENV_FILE"
  if grep -q "^$key=" "$ENV_FILE"; then
    tmp="$ENV_FILE.tmp"; awk -v k="$key" -v v="$value" 'BEGIN{FS=OFS="="} $1==k {print k"="v; next} {print}' "$ENV_FILE" > "$tmp" && mv "$tmp" "$ENV_FILE"
  else
    printf '%s=%s\n' "$key" "$value" >> "$ENV_FILE"
  fi
  chmod 600 "$ENV_FILE"
}
