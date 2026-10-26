#!/bin/sh
# The tunnel: lets MeetStream reach this Mac during meetings. It runs in the background under macOS
# (launchd), so once turned on it stays on, also after a restart, until you turn it off.
# Usage: tools/tunnel.sh         (turn on)      tools/tunnel.sh stop      tools/tunnel.sh status
. "$(dirname "$0")/_common.sh"
NG="$(command -v ngrok || echo "$HOME/.local/bin/ngrok")"
LOG="$CONFIG_DIR/ngrok.log"
LABEL="ai.horus.tunnel"; PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"; TARGET="gui/$(id -u)"
WAIT="${HORUS_TUNNEL_WAIT:-30}"
public_url() { curl -s --max-time 3 http://127.0.0.1:4040/api/tunnels | python3 -c 'import json,sys; d=json.load(sys.stdin); ts=[t["public_url"] for t in d.get("tunnels",[]) if t["public_url"].startswith("https")]; print(ts[0] if ts else "")' 2>/dev/null; }
case "$1" in
  stop)
    launchctl bootout "$TARGET/$LABEL" >/dev/null 2>&1
    rm -f "$PLIST"
    for pid in $(pgrep -f "ngrok http.*8765" 2>/dev/null); do kill "$pid" 2>/dev/null; done
    ok "tunnel turned off"; exit 0;;
  status)
    u="$(public_url)"; [ -n "$u" ] && echo "$u" || echo "no tunnel running"; exit 0;;
esac
[ -x "$NG" ] || die "ngrok is not installed yet. Run ~/Horus/install-ngrok first."
ngrok_has_token || die "ngrok has no authtoken yet. Run ~/Horus/install-ngrok and paste it."
u="$(public_url)"
if [ -n "$u" ]; then
  set_env HORUS_MEET_PUBLIC_URL "$u"; ok "the tunnel is already on at $u"; exit 0
fi
dom="$(grep '^NGROK_DOMAIN=' "$ENV_FILE" 2>/dev/null | cut -d= -f2-)"
mkdir -p "$HOME/Library/LaunchAgents"
{
  printf '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0"><dict>\n'
  printf '  <key>Label</key><string>%s</string>\n' "$LABEL"
  printf '  <key>ProgramArguments</key><array>\n    <string>%s</string><string>http</string>\n' "$NG"
  [ -n "$dom" ] && printf '    <string>--url=%s</string>\n' "$dom"
  printf '    <string>8765</string><string>--log=stdout</string>\n  </array>\n'
  printf '  <key>RunAtLoad</key><true/>\n  <key>KeepAlive</key><true/>\n'
  printf '  <key>StandardOutPath</key><string>%s</string>\n  <key>StandardErrorPath</key><string>%s</string>\n' "$LOG" "$LOG"
  printf '</dict></plist>\n'
} > "$PLIST"
launchctl bootout "$TARGET/$LABEL" >/dev/null 2>&1
launchctl bootstrap "$TARGET" "$PLIST" 2>/dev/null || die "macOS could not start the tunnel service. Look at $LOG, or run: launchctl bootstrap $TARGET \"$PLIST\""
i=0; u=""
while [ -z "$u" ] && [ "$i" -lt "$WAIT" ]; do sleep 1; i=$((i+1)); u="$(public_url)"; done
[ -n "$u" ] || { launchctl bootout "$TARGET/$LABEL" >/dev/null 2>&1; rm -f "$PLIST"; die "the tunnel did not come up within $WAIT seconds. Look at $LOG (a wrong authtoken or a domain that belongs to another account are the usual causes)."; }
set_env HORUS_MEET_PUBLIC_URL "$u"
ok "tunnel on at $u (saved to backend/.env). It stays on in the background, also after a restart. Turn it off with ~/Horus/tunnel stop."
