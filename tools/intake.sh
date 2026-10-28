#!/bin/sh
# New requests from the website become engagements automatically. The watcher runs in the background under macOS
# (launchd) and checks the site every two minutes, also after a restart, until you turn it off.
# It runs through the small "Horus Intake" helper application in ~/Horus, because macOS lets a background job read
# the Desktop folder (where this project lives) only after you have allowed a named application to do so, once.
# Usage: ~/Horus/intake on | off | status | pull | pending | kickoff CODE | log | login | test [--demo]
. "$(dirname "$0")/_common.sh"
LABEL="ai.horus.intake"; PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"; TARGET="gui/$(id -u)"; LOG="$CONFIG_DIR/intake.log"
INTERVAL="${HORUS_INTAKE_INTERVAL:-120}"
APP="$HORUS_HOME/Horus Intake.app"; HELPER="$APP/Contents/MacOS/horus-intake"
run() { ( cd "$BACKEND" && ./uvw run --no-sync horus-intake "$@" ); }
stamp() { date '+%Y-%m-%d %H:%M:%S'; }

build_helper() { # compiles and signs ~/Horus/Horus Intake.app; rebuilt only when its source changes, so the permission you gave it stays valid
  src="$REPO/tools/intake-launcher.c"; info="$REPO/tools/intake-launcher.plist"
  want="$(cat "$src" "$info" | shasum -a 256 | cut -c1-16)"
  have="$(cat "$APP/Contents/Resources/build-id" 2>/dev/null)"
  [ -x "$HELPER" ] && [ "$want" = "$have" ] && return 0
  xcode-select -p >/dev/null 2>&1 || die "the Apple command line tools are missing. Run: xcode-select --install   and try again when they are installed"
  rm -rf "$APP"; mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
  cp "$info" "$APP/Contents/Info.plist"; printf 'APPL????' > "$APP/Contents/PkgInfo"
  cc -O2 -Wall -o "$HELPER" "$src" 2>/dev/null || die "could not build the Horus Intake helper (tools/intake-launcher.c)"
  printf '%s' "$want" > "$APP/Contents/Resources/build-id"
  codesign --force --sign - --identifier "$LABEL" "$APP" >/dev/null 2>&1 || die "could not sign the Horus Intake helper"
}
running_pid() { launchctl print "$TARGET/$LABEL" 2>/dev/null | awk '/^[[:space:]]*pid = /{print $3; exit}'; }
since_last_start() { awk '/ intake on$/{buf=""; next} {buf=buf $0 "\n"} END{printf "%s", buf}' "$LOG" 2>/dev/null; }
permission_help() {
  warn "macOS is not letting Horus Intake read the project folder on your Desktop, so the watcher cannot run."
  printf '    Allow it: System Settings > Privacy & Security > Files and Folders > Horus Intake > turn on Desktop Folder.\n'
  printf '    If Horus Intake is not listed there: Privacy & Security > Full Disk Access > + > your home folder > Horus > Horus Intake.app\n'
  printf '    Then run: ~/Horus/intake on\n'
}
report_start() { # after "on": did the loop get going, is macOS still asking, or did it refuse?
  recent="$(since_last_start)"
  if printf '%s' "$recent" | grep -q 'Operation not permitted'; then permission_help
  elif printf '%s' "$recent" | grep -q 'intake watcher started'; then ok "the watcher is running"
  else say "If macOS is asking whether Horus Intake may access files in your Desktop folder, click Allow: that is what lets the watcher read the Horus tools. Check with ~/Horus/intake status"
  fi
}
cmd="$1"; [ $# -gt 0 ] && shift
case "$cmd" in
  on)
    grep -q '^HORUS_INTAKE_TOKEN=.\{1,\}' "$ENV_FILE" 2>/dev/null || die "no intake token yet: run ~/Horus/configure-site, then ~/Horus/deploy-site"
    grep -q '^HORUS_SITE_URL=.\{1,\}' "$ENV_FILE" 2>/dev/null || die "the site is not published yet: run ~/Horus/deploy-site"
    build_helper
    mkdir -p "$HOME/Library/LaunchAgents"
    {
      printf '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0"><dict>\n'
      printf '  <key>Label</key><string>%s</string>\n' "$LABEL"
      printf '  <key>ProgramArguments</key><array><string>%s</string><string>/bin/sh</string><string>%s</string><string>loop</string></array>\n' "$HELPER" "$REPO/tools/intake.sh"
      printf '  <key>EnvironmentVariables</key><dict><key>HORUS_INTAKE_INTERVAL</key><string>%s</string></dict>\n' "$INTERVAL"
      printf '  <key>KeepAlive</key><true/>\n  <key>RunAtLoad</key><true/>\n  <key>ThrottleInterval</key><integer>60</integer>\n  <key>ProcessType</key><string>Background</string>\n'
      printf '  <key>StandardOutPath</key><string>%s</string>\n  <key>StandardErrorPath</key><string>%s</string>\n' "$LOG" "$LOG"
      printf '</dict></plist>\n'
    } > "$PLIST"
    launchctl bootout "$TARGET/$LABEL" >/dev/null 2>&1
    printf '%s intake on\n' "$(stamp)" >> "$LOG"
    launchctl bootstrap "$TARGET" "$PLIST" 2>/dev/null || die "macOS could not start the watcher. Try: launchctl bootstrap $TARGET \"$PLIST\""
    ok "intake watcher on: it checks the site every $INTERVAL seconds, also after a restart. Turn it off with ~/Horus/intake off"
    run check | sed 's/^/  /'
    sleep 3; report_start;;
  off)
    launchctl bootout "$TARGET/$LABEL" >/dev/null 2>&1; rm -f "$PLIST"; ok "intake watcher off";;
  status)
    pid="$(running_pid)"
    if [ -f "$PLIST" ] && [ -n "$pid" ]; then
      if since_last_start | grep -q 'intake watcher started'; then ok "watcher running (checks every $INTERVAL seconds)"
      else warn "watcher started but has not begun checking: if macOS is asking whether Horus Intake may access your Desktop folder, click Allow"; fi
    elif [ -f "$PLIST" ]; then warn "watcher registered but not running; macOS restarts it within a minute"
    else warn "watcher off: turn it on with ~/Horus/intake on"; fi
    since_last_start | tail -n 3 | grep -q 'Operation not permitted' && permission_help
    run check | sed 's/^/  /'
    [ -f "$LOG" ] && { say "Last activity:"; tail -n 8 "$LOG" | sed 's/^/  /'; }
    exit 0;;
  loop) # what the helper application runs in the background
    printf '%s intake watcher started (checks every %s seconds)\n' "$(stamp)" "$INTERVAL"
    while :; do run pull --quiet; sleep "$INTERVAL"; done;;
  pull) run pull "$@";;
  pending) run pending;;
  kickoff) [ -n "$1" ] || die "which engagement? ~/Horus/intake kickoff CODE"; run kickoff "$@";;
  log) [ -f "$LOG" ] || die "nothing logged yet"; tail -n 40 -f "$LOG";;
  login)
    CL="$(find_claude)" || die "the claude command was not found; install or update the Claude app"
    [ -t 0 ] || die "run this in the Terminal panel: it opens a browser window for the sign-in"
    say "Signing in the Claude command-line tool with the same account as the Claude app. A browser window opens; approve there, then come back here."
    "$CL" auth login;;
  test) run test-submit "$@" && { sleep 2; run pull; };;
  *) say "Usage: ~/Horus/intake on | off | status | pull | pending | kickoff CODE | log | login | test [--demo]"; exit 2;;
esac
