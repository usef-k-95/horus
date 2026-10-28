# Horus website

Static site built on the brand, plus its own small backend. `index.html` is written in the Claude artifact form (no document skeleton); `build-standalone.sh` wraps it into `dist/index.html`; `worker/build.py` embeds `dist/` into a Cloudflare Worker (`worker/worker-src.js`) that serves the site and runs the intake API; `worker/deploy.py` publishes it through Cloudflare's REST API (no Node, no wrangler). The Supervisor runs all of this with `~/Horus/configure-site` and `~/Horus/deploy-site` (docs/GETTING-STARTED.md, Part F).

Positioning (27 October 2026, from the founder's review): Horus is a technology company whose AI runs policy engagements for governments end to end. The site never calls the company "Horus Advisory" or "Policy Advisory", never mentions human supervision, approvals or AI disclosure, names no third-party frameworks, and shows Horus deciding with its decision record. Engagements start from a scope-of-work document, not a question; both forms accept a scope document.

How a request travels:

1. The form posts to `/api/requests` on the same host (multipart, with `scope_file`). The worker validates it, drops bot submissions (hidden `website` field, eight per connection per hour), stores the record and the document in the `horus-intake` KV namespace, and emails the Supervisor through Email Routing (`intake@<domain>`, with the document attached). In the claude.ai artifact preview the same forms store requests in the page's private database instead.
2. The intake watcher on the Supervisor's Mac (`backend/src/horus_intake`, `~/Horus/intake`) polls `/api/intake/pending` with the bearer token from `backend/.env`, creates the engagement folder, downloads the document, acknowledges the request (`/ack`), emails the requester, and starts the Horus Principal unattended. It runs under launchd through the helper app `~/Horus/Horus Intake.app` (built by `~/Horus/intake on` from `tools/intake-launcher.c`), because macOS lets a background job read the Desktop folder, where this repository lives, only through a named application the Supervisor has allowed once.

Hosting: Cloudflare free plan (Workers, KV, Email Routing, custom domain), DNS on Cloudflare (the registrar's nameservers point there). `deploy.py` is idempotent: run it again after the nameservers change or the notification address is verified.

Changing the site: edit `index.html`, `styles.css`, `site.js`, then `~/Horus/deploy-site`. `FORM_ENDPOINT` and `CONTACT` in `site.js` are set for the own-domain deployment. No tracking, no cookies, no third-party scripts; fonts come from Google Fonts.
