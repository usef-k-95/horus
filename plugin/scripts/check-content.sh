#!/bin/sh
# Content checks for plugin skills: conventions (no em-dashes, no URLs in references), index files, SKILL.md front matter.
cd "$(dirname "$0")/.." || exit 1
status=0
echo "== reference files =="
for f in $(find skills -path '*/references/*' -name '*.md' | sort); do
  em=$(grep -c '—' "$f"); url=$(grep -c 'https\?://' "$f"); words=$(wc -w < "$f" | tr -d ' ')
  flag=""
  [ "$em" -gt 0 ] && flag="$flag em-dashes:$em"
  [ "$url" -gt 0 ] && flag="$flag urls:$url"
  [ "$words" -lt 300 ] && flag="$flag short:$words"
  [ -n "$flag" ] && { echo "WARN $f$flag"; status=1; }
done
echo "== indexes =="
for idx in skills/horus-method/references/frameworks/INDEX.md skills/horus-policy/references/pathways/INDEX.md skills/horus-policy/references/pathways/classification.md; do
  [ -f "$idx" ] && echo "ok   $idx" || { echo "MISSING $idx"; status=1; }
done
echo "== SKILL.md front matter =="
for s in skills/*/SKILL.md; do
  head -1 "$s" | grep -q '^---$' && grep -q '^name:' "$s" && grep -q '^description:' "$s" && echo "ok   $s" || { echo "BAD  $s"; status=1; }
done
echo "== description budget (all skills, max 1536 chars) =="
total=0; for s in skills/*/SKILL.md; do n=$(grep '^description:' "$s" | head -1 | wc -c | tr -d ' '); total=$((total + n)); done; echo "total description chars: $total"
[ "$total" -gt 1536 ] && { echo "WARN over budget"; status=1; }
echo "== counts =="; echo "reference files: $(find skills -path '*/references/*' -name '*.md' | wc -l | tr -d ' ')  agents: $(ls agents/*.md | wc -l | tr -d ' ')"
exit $status
