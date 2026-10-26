#!/bin/sh
# Run the Supervisor console against the current engagement: scripts/horus.sh status
. "$(dirname "$0")/backend-env.sh"
exec HORUS_WORKSPACE="$WORKSPACE" "$BACKEND/uvw" run --no-sync horus "$@"
