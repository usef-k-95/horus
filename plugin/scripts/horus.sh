#!/bin/sh
# Run the Supervisor console against the current engagement: scripts/horus.sh status
. "$(dirname "$0")/backend-env.sh"
exec "$BACKEND/uvw" run --no-sync horus --workspace "$WORKSPACE" "$@"
