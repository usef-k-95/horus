#!/bin/sh
# Publish the website and its intake API to Cloudflare (free plan), then report what is still needed from you
# (the nameservers to set at GoDaddy, the verification email to click). Safe to run as often as you like.
# Usage: ~/Horus/deploy-site           ~/Horus/deploy-site status
. "$(dirname "$0")/_common.sh"
grep -q '^CLOUDFLARE_API_TOKEN=.\{1,\}' "$ENV_FILE" 2>/dev/null || die "no Cloudflare token yet: run ~/Horus/configure-site first"
if [ "$1" != "status" ]; then
  sh "$REPO/web/build-standalone.sh" >/dev/null || die "could not build the site (web/build-standalone.sh)"
fi
exec python3 "$REPO/web/worker/deploy.py" "$@"
