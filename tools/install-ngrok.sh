#!/bin/sh
# Step 3a (once): install ngrok, the tool that lets MeetStream reach this Mac during a meeting.
# Before running: sign up at ngrok.com, click Download for macOS, let the .zip land in Downloads,
# and copy your authtoken from the ngrok dashboard (Getting Started, Your Authtoken).
. "$(dirname "$0")/_common.sh"
[ -t 0 ] || die "this command asks you questions, so it must run in the Terminal panel. Click into the Terminal panel and type the command there."
mkdir -p "$HOME/.local/bin"
if command -v ngrok >/dev/null 2>&1 || [ -x "$HOME/.local/bin/ngrok" ]; then
  ok "ngrok is already installed"
else
  zip="$(ls -t "$HOME"/Downloads/ngrok*.zip 2>/dev/null | head -1)"
  bin="$HOME/Downloads/ngrok"
  if [ -n "$zip" ]; then unzip -o -q "$zip" -d "$HOME/Downloads" && bin="$HOME/Downloads/ngrok"; fi
  [ -f "$bin" ] || die "ngrok was not found in your Downloads folder. Download it from ngrok.com first, then run this again."
  mv "$bin" "$HOME/.local/bin/ngrok" && chmod +x "$HOME/.local/bin/ngrok"
  xattr -d com.apple.quarantine "$HOME/.local/bin/ngrok" 2>/dev/null || true
  ok "ngrok installed to ~/.local/bin"
fi
NG="$(command -v ngrok || echo "$HOME/.local/bin/ngrok")"
if ngrok_has_token; then ok "an authtoken is already saved"; fi
tries=0
while ! ngrok_has_token && [ $tries -lt 3 ]; do
  printf 'Paste your ngrok authtoken, then press Enter (typing is hidden, so nothing appears): '; stty -echo; read -r token; stty echo; printf '\n'
  if [ -n "$token" ]; then "$NG" config add-authtoken "$token" >/dev/null 2>&1 && ok "authtoken saved" || warn "ngrok did not accept that authtoken; copy it again from dashboard.ngrok.com (Getting Started, Your Authtoken)"
  else warn "nothing was pasted"; fi
  tries=$((tries+1))
done
ngrok_has_token || die "no authtoken saved, so ngrok is not ready. Copy it from dashboard.ngrok.com (Getting Started, Your Authtoken) and run ~/Horus/install-ngrok again."
curdom="$(grep '^NGROK_DOMAIN=' "$ENV_FILE" 2>/dev/null | cut -d= -f2-)"
if [ -n "$curdom" ]; then printf 'Your free static domain (already set to %s; press Enter to keep): ' "$curdom"; else printf 'If you claimed a free static domain in the ngrok dashboard, paste it (or press Enter): '; fi
read -r dom
[ -n "$dom" ] && set_env NGROK_DOMAIN "$dom" && ok "static domain saved"
say "ngrok is ready. Turn the tunnel on with ~/Horus/tunnel; it then stays on in the background."
