#!/bin/sh
# Any time: what is ready and what is missing.
. "$(dirname "$0")/_common.sh"
say "Horus readiness check"
( cd "$BACKEND" && ./uvw run --no-sync horus-meet check-env 2>&1 | sed 's/^/  /' ) ; meet=$?
say "Mail:"; ( cd "$BACKEND" && ./uvw run --no-sync horus-mail check 2>&1 | sed 's/^/  /' )
say "Keys (checked with each vendor; values never shown):"
getv() { grep "^$1=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-; }
MS="$(getv MEETSTREAM_API_KEY)"; EL="$(getv ELEVENLABS_API_KEY)"; VID="$(getv ELEVENLABS_VOICE_ID)"
if [ -n "$MS" ]; then c="$(curl -s -o /dev/null --max-time 20 -w '%{http_code}' -H "Authorization: Token $MS" https://api.meetstream.ai/api/v1/bots)"; [ "$c" = "200" ] && ok "MeetStream key accepted" || warn "MeetStream key rejected (HTTP $c). Check the key on app.meetstream.ai/api-keys and re-enter it with ~/Horus/configure"; else warn "MeetStream key not entered yet"; fi
if [ -n "$EL" ]; then c="$(curl -s -o /dev/null --max-time 20 -w '%{http_code}' -H "xi-api-key: $EL" https://api.elevenlabs.io/v1/user)"; [ "$c" = "200" ] && ok "ElevenLabs key accepted" || warn "ElevenLabs key rejected (HTTP $c). Re-enter it with ~/Horus/configure"
  if [ -n "$VID" ]; then vn="$(curl -s --max-time 20 -H "xi-api-key: $EL" "https://api.elevenlabs.io/v1/voices/$VID" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("name") or "")' 2>/dev/null)"; [ -n "$vn" ] && ok "voice: $vn" || warn "voice ID $VID is not in your ElevenLabs account. Open the voice in the Voice Library and click Add to My Voices, or choose one listed under My Voices, then re-enter its ID with ~/Horus/configure"; else warn "voice ID not entered yet"; fi
else warn "ElevenLabs key not entered yet"; fi
say "ngrok:"; NG="$(command -v ngrok || echo "$HOME/.local/bin/ngrok")"
if [ -x "$NG" ]; then ok "installed"; ngrok_has_token && ok "authtoken saved" || warn "authtoken missing: run ~/Horus/install-ngrok and paste it"; d="$(getv NGROK_DOMAIN)"; [ -n "$d" ] && ok "static domain: $d" || warn "no static domain (optional; the address will change each time)"; else warn "ngrok not installed: run ~/Horus/install-ngrok"; fi
say "Tunnel:"; sh "$(dirname "$0")/tunnel.sh" status | sed 's/^/  /'
say "Website and intake:"; ( cd "$BACKEND" && ./uvw run --no-sync horus-intake check 2>&1 | sed 's/^/  /' )
say "Plugin:"; CL="$(find_claude)" && "$CL" plugin list 2>/dev/null | grep -A3 "horus@" | sed 's/^/  /' || warn "Horus plugin not installed yet (run tools/install-plugin.sh)"
