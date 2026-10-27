#!/bin/sh
# Step 4 (once): deploy the Horus plugin on this Mac so every Claude Code session can use it.
. "$(dirname "$0")/_common.sh"
CL="$(find_claude)" || die "could not find the Claude Code command. Open the Claude app once, then run this again."
say "Registering the Horus plugin with Claude Code…"
"$CL" plugin marketplace add "$REPO" >/dev/null 2>&1 || "$CL" plugin marketplace update horus-local >/dev/null 2>&1 || true
installed_copy() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["plugins"]["horus@horus-local"][0]["installPath"])' "$HOME/.claude/plugins/installed_plugins.json" 2>/dev/null; }
if "$CL" plugin list 2>/dev/null | grep -q "horus@horus-local"; then
  "$CL" plugin update horus@horus-local 2>&1 | tail -1
  # Claude Code runs a copy of the plugin; if the copy is behind the repository, reinstall to refresh it
  copy="$(installed_copy)"
  if [ -n "$copy" ] && [ -d "$copy" ] && diff -rq -x .DS_Store -x __pycache__ "$copy" "$REPO/plugin" >/dev/null 2>&1; then :; else
    say "Refreshing the installed copy…"
    "$CL" plugin uninstall horus@horus-local >/dev/null 2>&1
    "$CL" plugin install horus@horus-local --scope user 2>&1 | tail -1
  fi
else
  "$CL" plugin install horus@horus-local --scope user 2>&1 | tail -1
fi
copy="$(installed_copy)"
if [ -n "$copy" ] && diff -rq -x .DS_Store -x __pycache__ "$copy" "$REPO/plugin" >/dev/null 2>&1; then ok "installed copy matches the repository"; else warn "the installed copy still differs from the repository"; fi
"$CL" plugin list 2>/dev/null | grep -A3 "horus@horus-local" | sed 's/^/  /'
say "Done. New Claude Code sessions will have Horus. Restart any session that is already open."
