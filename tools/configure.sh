#!/bin/sh
# Step 2: enter your keys. Asks for each value; typing is hidden for secrets; nothing is shown back
# or stored anywhere except backend/.env on this Mac. Press Enter to keep an existing value.
. "$(dirname "$0")/_common.sh"
[ -f "$ENV_FILE" ] || { cp "$BACKEND/.env.example" "$ENV_FILE"; chmod 600 "$ENV_FILE"; }
current() { grep "^$1=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-; }
ask() { # ask KEY "question" secret?
  key="$1"; q="$2"; secret="$3"; cur="$(current "$key")"
  if [ -n "$cur" ]; then hint=" (already set, press Enter to keep)"; else hint=""; fi
  printf '%s%s: ' "$q" "$hint"
  if [ "$secret" = "secret" ]; then stty -echo; read -r val; stty echo; printf '\n'; else read -r val; fi
  [ -n "$val" ] && set_env "$key" "$val"
}
[ -t 0 ] || die "this command asks you questions, so it must run in the Terminal panel. Click into the Terminal panel and type the command there."
say "Horus configuration. You will be asked for five values. You can run this again any time."
say "1. MeetStream API key (from app.meetstream.ai, Configure, API Keys; starts with ms_)"
ask MEETSTREAM_API_KEY "   MeetStream API key" secret
say "2. ElevenLabs API key (elevenlabs.io, your profile, API Keys)"
ask ELEVENLABS_API_KEY "   ElevenLabs API key" secret
say "3. ElevenLabs voice ID (elevenlabs.io, Voices, My Voices: pick a voice there or add one from the library first, then copy its ID)"
ask ELEVENLABS_VOICE_ID "   Voice ID"
say "4. Your Gmail address, used only to download attachments and invites and to send with files"
ask HORUS_MAIL_USER "   Gmail address"
say "5. A Google app password for that account (16 letters; never your normal password)"
ask HORUS_MAIL_APP_PASSWORD "   App password" secret
set_env HORUS_MEET_PROVIDER meetstream
set_env ELEVENLABS_OUTPUT_FORMAT pcm_24000
say "Saved to backend/.env. The tunnel address is set automatically by tools/tunnel.sh."
say "Now run tools/check.sh to see what is ready."
