#!/bin/sh
. "$(dirname "$0")/backend-env.sh"
exec "$BACKEND/uvw" run --no-sync horus-state --workspace "$WORKSPACE"
