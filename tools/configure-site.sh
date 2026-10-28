#!/bin/sh
# The website: enter the Cloudflare details once. Typing is hidden for the token; values go only to backend/.env on this Mac.
# Press Enter on a question to keep the value already set.
. "$(dirname "$0")/_common.sh"
[ -f "$ENV_FILE" ] || { cp "$BACKEND/.env.example" "$ENV_FILE"; chmod 600 "$ENV_FILE"; }
current() { grep "^$1=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-; }
ask() { # ask KEY "question" [secret]
  key="$1"; q="$2"; secret="$3"; cur="$(current "$key")"
  if [ -n "$cur" ]; then hint=" (already set, press Enter to keep)"; else hint=""; fi
  printf '%s%s: ' "$q" "$hint"
  if [ "$secret" = "secret" ]; then stty -echo; read -r val; stty echo; printf '\n'; else read -r val; fi
  [ -n "$val" ] && set_env "$key" "$val"
}
[ -t 0 ] || die "this command asks you questions, so it must run in the Terminal panel. Click into the Terminal panel and type the command there."
say "Website configuration (Cloudflare, free plan). Four questions; you can run this again any time."
say "1. Cloudflare API token (dash.cloudflare.com/profile/api-tokens; the permissions are listed in Part F of the guide)"
ask CLOUDFLARE_API_TOKEN "   API token" secret
say "2. The domain (press Enter for horushq.ai)"
ask HORUS_SITE_DOMAIN "   Domain"
[ -n "$(current HORUS_SITE_DOMAIN)" ] || set_env HORUS_SITE_DOMAIN horushq.ai
say "3. The email address that receives new requests (press Enter for your Gmail address)"
ask HORUS_INTAKE_NOTIFY_EMAIL "   Notification address"
[ -n "$(current HORUS_INTAKE_NOTIFY_EMAIL)" ] || set_env HORUS_INTAKE_NOTIFY_EMAIL "$(current HORUS_MAIL_USER)"
say "4. Your Cloudflare Account ID (optional: press Enter and the tool finds it; it is on the dashboard under Workers & Pages, Overview)"
ask CLOUDFLARE_ACCOUNT_ID "   Account ID"
[ -n "$(current HORUS_INTAKE_TOKEN)" ] || set_env HORUS_INTAKE_TOKEN "$(openssl rand -hex 32)"
[ -n "$(current HORUS_INTAKE_AUTOSTART)" ] || set_env HORUS_INTAKE_AUTOSTART 1
[ -n "$(current HORUS_INTAKE_AUTO_ACK)" ] || set_env HORUS_INTAKE_AUTO_ACK 1
[ -n "$(current HORUS_INTAKE_NOTIFY_EMAIL)" ] || warn "no notification address yet: run ~/Horus/configure first (Gmail address), or run this again and type one"
say "Saved to backend/.env. Next: ~/Horus/deploy-site"
