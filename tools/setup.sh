#!/bin/sh
# Step 1: prepare this Mac. Installs the small Python tool Horus needs (user level, no password),
# builds the backend, runs its tests, and prepares the folder for engagements.
. "$(dirname "$0")/_common.sh"
say "Horus setup"
if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/Library/Python/3.9/bin/uv" ] && [ ! -x "$HOME/.local/bin/uv" ]; then
  say "Installing the Python package tool (uv)…"
  python3 -m pip install --user --quiet uv || die "could not install uv. Open the Terminal panel and run: python3 -m pip install --user uv"
fi
ok "Python tool present"
say "Building the Horus backend (first time takes a minute)…"
( cd "$BACKEND" && ./uvw sync --extra dev >/dev/null 2>&1 ) || die "backend build failed. Run: cd backend && ./uvw sync --extra dev"
ok "backend built"
say "Running the backend's own checks…"
( cd "$BACKEND" && ./uvw run --no-sync pytest -q 2>&1 | tail -1 )
mkdir -p "$ENGAGEMENTS"
ok "engagement folder ready: $ENGAGEMENTS"
[ -f "$ENV_FILE" ] || { cp "$BACKEND/.env.example" "$ENV_FILE"; chmod 600 "$ENV_FILE"; ok "created the settings file backend/.env (empty keys)"; }
say "Creating the ~/Horus commands…"
for t in "$REPO"/tools/*.sh; do
  n="$(basename "$t" .sh)"
  case "$n" in _common|setup) continue;; esac
  printf '#!/bin/sh\nexec sh "%s" "$@"\n' "$t" > "$HORUS_HOME/$n" && chmod +x "$HORUS_HOME/$n"
done
ok "commands ready in ~/Horus: configure, check, install-ngrok, tunnel, install-plugin, new-engagement, test-meeting, horus"
say "Done. Next: ~/Horus/configure to enter your keys, then ~/Horus/check."
