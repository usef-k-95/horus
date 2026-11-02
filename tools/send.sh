#!/bin/sh
# Approve and send a pending client email from the engagement state, with no Horus session open.
# Examples: ~/Horus/send COM-004                       preview: who approves what, recipients, subject, thread, attachments, text; nothing is sent
#           ~/Horus/send COM-004 --approve             record your approval, send the email, mark it sent (add --note "…" for a remark)
#           ~/Horus/send COM-004 --send-only           an email you already approved with ~/Horus/horus approve
#           ~/Horus/send COM-004 --reject --reason "…" turn it down; the draft goes back to Horus
# From any folder, put the engagement code first: ~/Horus/send EGY-2026-001 COM-004
. "$(dirname "$0")/_common.sh"
if [ -n "$1" ] && [ -d "$ENGAGEMENTS/$1/.horus" ]; then export HORUS_WORKSPACE="$ENGAGEMENTS/$1"; shift; fi
exec sh "$(dirname "$0")/horus.sh" send "$@"
