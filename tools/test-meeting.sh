#!/bin/sh
# First live test: sends the Horus bot into a Google Meet you host.
# Usage: ~/Horus/test-meeting            (asks you to paste the meeting link)
#        ~/Horus/test-meeting "https://meet.google.com/xxx-xxxx-xxx"
#        ~/Horus/test-meeting --check "link"   (only checks the link, starts nothing)
. "$(dirname "$0")/_common.sh"
check_only=""; [ "$1" = "--check" ] && { check_only=1; shift; }
link="$1"
if [ -z "$link" ]; then
  [ -t 0 ] || die 'run this in the Terminal panel so you can paste the link when asked, or give the link: ~/Horus/test-meeting "https://meet.google.com/..."'
  printf 'Paste the link of the Google Meet you are in (copy it from the address bar), then press Enter: '
  read -r link
  [ -n "$link" ] || die "no link was pasted."
fi
case "$link" in
  *abc-defg-hij*|*kqz-mprt-xyz*|*xxx-xxxx-xxx*|*PASTE-YOUR-LINK-HERE*) die "that is an example link from the guide, not a real meeting. In your Google Meet, copy the link from the address bar (three groups of letters, like meet.google.com/abc-defg-hij but with your own letters) and try again.";;
esac
case "$link" in
  *meet.google.com/*) printf '%s' "$link" | grep -Eq 'meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}' || die "that does not look like a complete Google Meet link: $link";;
  *zoom.us/*|*teams.microsoft.com/*|*teams.live.com/*) ;;
  *) die "that does not look like a Google Meet, Zoom or Teams link: $link";;
esac
[ -n "$check_only" ] && { ok "the link looks valid"; exit 0; }
if pgrep -f 'horus-meet spike' >/dev/null 2>&1; then die "a live test is already running in another Terminal tab. Finish it there (say goodbye, or press Control+C), then run this again."; fi
if lsof -nP -iTCP:8765 -sTCP:LISTEN -t >/dev/null 2>&1; then die "another Horus meeting process is using port 8765. Close the session or Terminal tab that is running a meeting, then run this again."; fi
sh "$(dirname "$0")/tunnel.sh" >/dev/null || die "tunnel not running"
cd "$BACKEND" && ./uvw run --no-sync horus-meet check-env >/dev/null 2>&1 || { ./uvw run --no-sync horus-meet check-env; die "not ready yet; fill the missing values with ~/Horus/configure"; }
say "Sending Horus into the meeting. Admit 'Horus AI (recording)' when it knocks, answer its questions, say goodbye to end."
exec ./uvw run --no-sync horus-meet spike "$link" --platform meet --turns 3
