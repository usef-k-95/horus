#!/usr/bin/env python3
"""Publish the Horus website and its intake API to Cloudflare (free plan) through the REST API: no Node, no wrangler.

    python3 web/worker/deploy.py            build, publish, then report what is still needed
    python3 web/worker/deploy.py status     report only

Reads backend/.env (CLOUDFLARE_API_TOKEN, optional CLOUDFLARE_ACCOUNT_ID, HORUS_SITE_DOMAIN, HORUS_INTAKE_NOTIFY_EMAIL,
HORUS_INTAKE_TOKEN) and writes HORUS_SITE_URL and CLOUDFLARE_ACCOUNT_ID back. Safe to run repeatedly: every step is
idempotent, and steps that need the domain active or the address verified are retried on the next run.
Normally run through tools/deploy-site.sh. Works with the system python3 (3.9)."""
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ENV_FILE = REPO / "backend" / ".env"
API = "https://api.cloudflare.com/client/v4"
SCRIPT = "horus-site"
KV_TITLE = "horus-intake"
COMPAT_DATE = "2026-01-01"


def say(msg):
    print("\n" + msg)


def ok(msg):
    print("  ✓ " + msg)


def warn(msg):
    print("  ! " + msg)


def fail(msg):
    print("\n  ✗ " + msg + "\n", file=sys.stderr)
    sys.exit(1)


def read_env():
    values = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            values[k.strip()] = v.strip().strip('"').strip("'")
    for k, v in os.environ.items():
        if k.startswith(("CLOUDFLARE_", "HORUS_")) and v:
            values[k] = v
    return values


def set_env(key, value):
    lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []
    out, done = [], False
    for line in lines:
        if line.split("=", 1)[0].strip() == key:
            out.append("%s=%s" % (key, value))
            done = True
        else:
            out.append(line)
    if not done:
        out.append("%s=%s" % (key, value))
    ENV_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    os.chmod(ENV_FILE, 0o600)


class CloudflareError(Exception):
    def __init__(self, status, errors, path):
        self.status, self.errors, self.path = status, errors, path
        detail = "; ".join("%s %s" % (e.get("code"), e.get("message")) for e in errors) if errors else ""
        super().__init__("HTTP %s on %s%s" % (status, path, (": " + detail) if detail else ""))


def first(err):
    return err.errors[0].get("message", str(err)) if getattr(err, "errors", None) else str(err)


class CF:
    def __init__(self, token):
        self.token = token

    def call(self, method, path, body=None, params=None, multipart=None):
        url = API + path + (("?" + urllib.parse.urlencode(params)) if params else "")
        headers = {"Authorization": "Bearer " + self.token, "Accept": "application/json"}
        data = None
        if multipart is not None:
            boundary = "----horus" + uuid.uuid4().hex
            chunks = []
            for name, filename, ctype, content in multipart:
                disp = 'form-data; name="%s"' % name + ('; filename="%s"' % filename if filename else "")
                chunks.append(("--%s\r\nContent-Disposition: %s\r\nContent-Type: %s\r\n\r\n" % (boundary, disp, ctype)).encode() + content + b"\r\n")
            chunks.append(("--%s--\r\n" % boundary).encode())
            data = b"".join(chunks)
            headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
        elif body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload, status = resp.read(), resp.status
        except urllib.error.HTTPError as e:
            payload, status = e.read(), e.code
        except urllib.error.URLError as e:
            raise CloudflareError(0, [{"code": 0, "message": "network error: %s" % e.reason}], path)
        try:
            parsed = json.loads(payload or b"{}")
        except ValueError:
            parsed = {"success": False, "errors": [{"code": status, "message": payload[:300].decode(errors="replace")}]}
        if not parsed.get("success", False):
            raise CloudflareError(status, parsed.get("errors") or [], path)
        return parsed.get("result")

    def get(self, path, **kw):
        return self.call("GET", path, **kw)

    def post(self, path, body=None, **kw):
        return self.call("POST", path, body=body, **kw)

    def put(self, path, body=None, **kw):
        return self.call("PUT", path, body=body, **kw)

    def patch(self, path, body=None, **kw):
        return self.call("PATCH", path, body=body, **kw)

    def delete(self, path, **kw):
        return self.call("DELETE", path, **kw)


# ---- steps -------------------------------------------------------------------------------------
def step_token(cf):
    try:
        r = cf.get("/user/tokens/verify")
    except CloudflareError as e:
        fail("Cloudflare rejected the token (%s). Run ~/Horus/configure-site and paste it again." % first(e))
    if (r or {}).get("status") != "active":
        fail("the Cloudflare token is not active (status %s)" % (r or {}).get("status"))
    ok("Cloudflare token accepted")


def step_account(cf, env):
    acc = env.get("CLOUDFLARE_ACCOUNT_ID")
    if acc:
        return acc
    try:
        accounts = cf.get("/accounts", params={"per_page": 50}) or []
    except CloudflareError as e:
        fail("could not list your Cloudflare accounts with this token (%s). Either give the token 'Account Settings: Read', or run ~/Horus/configure-site and enter the Account ID (Cloudflare dashboard, Workers & Pages, Overview, right-hand column)." % first(e))
    if len(accounts) == 1:
        set_env("CLOUDFLARE_ACCOUNT_ID", accounts[0]["id"])
        ok("account: %s" % accounts[0].get("name"))
        return accounts[0]["id"]
    if not accounts:
        fail("the token sees no Cloudflare account; check 'Account Resources' when creating it")
    fail("the token sees several accounts: " + ", ".join("%s (%s)" % (a.get("name"), a["id"]) for a in accounts) + ". Run ~/Horus/configure-site and enter the one to use.")


def step_zone(cf, account, domain):
    zones = cf.get("/zones", params={"name": domain}) or []
    if zones:
        return zones[0]
    try:
        z = cf.post("/zones", {"name": domain, "account": {"id": account}, "type": "full"})
        ok("added %s to Cloudflare" % domain)
        return z
    except CloudflareError as e:
        fail("could not add %s to Cloudflare (%s). Add it in the dashboard instead: Add a domain, %s, Free plan; then run this again." % (domain, first(e), domain))


def step_zone_settings(cf, zone):
    for name, value in (("always_use_https", "on"), ("min_tls_version", "1.2")):
        try:
            cf.patch("/zones/%s/settings/%s" % (zone["id"], name), {"value": value})
        except CloudflareError as e:
            warn("zone setting %s: %s" % (name, first(e)))
    ok("HTTPS enforced")


def step_kv(cf, account):
    spaces = cf.get("/accounts/%s/storage/kv/namespaces" % account, params={"per_page": 100}) or []
    for s in spaces:
        if s.get("title") == KV_TITLE:
            return s["id"]
    s = cf.post("/accounts/%s/storage/kv/namespaces" % account, {"title": KV_TITLE})
    ok("request store created")
    return s["id"]


def email_status(cf, account, zone, notify_to):
    status = {"routing": False, "verified": False, "rules": []}
    try:
        status["routing"] = bool((cf.get("/zones/%s/email/routing" % zone["id"]) or {}).get("enabled"))
    except CloudflareError:
        pass
    try:
        addrs = cf.get("/accounts/%s/email/routing/addresses" % account, params={"per_page": 50}) or []
        match = next((a for a in addrs if (a.get("email") or "").lower() == notify_to.lower()), None)
        status["verified"] = bool(match and match.get("verified"))
    except CloudflareError:
        pass
    if status["routing"]:
        try:
            rules = cf.get("/zones/%s/email/routing/rules" % zone["id"], params={"per_page": 50}) or []
            status["rules"] = [m["value"] for r in rules for m in r.get("matchers", []) if m.get("type") == "literal"]
        except CloudflareError:
            pass
    return status


def step_email(cf, account, zone, domain, notify_to):
    status = {"routing": False, "verified": False, "rules": []}
    try:
        info = cf.get("/zones/%s/email/routing" % zone["id"]) or {}
        if info.get("enabled"):
            status["routing"] = True
        else:
            try:
                cf.post("/zones/%s/email/routing/enable" % zone["id"])
                status["routing"] = True
                ok("email routing enabled on %s" % domain)
            except CloudflareError as e:
                warn("email routing not enabled yet: %s" % first(e))
    except CloudflareError as e:
        warn("email routing: %s" % first(e))
    try:
        addrs = cf.get("/accounts/%s/email/routing/addresses" % account, params={"per_page": 50}) or []
        match = next((a for a in addrs if (a.get("email") or "").lower() == notify_to.lower()), None)
        if not match:
            match = cf.post("/accounts/%s/email/routing/addresses" % account, {"email": notify_to}) or {}
            ok("verification email sent to %s" % notify_to)
        status["verified"] = bool(match.get("verified"))
        ok("notification address %s: %s" % (notify_to, "verified" if status["verified"] else "waiting for you to click the verification link"))
    except CloudflareError as e:
        warn("notification address: %s" % first(e))
    if status["routing"]:
        try:
            rules = cf.get("/zones/%s/email/routing/rules" % zone["id"], params={"per_page": 50}) or []
            existing = {m["value"] for r in rules for m in r.get("matchers", []) if m.get("type") == "literal"}
            for local in ("intake", "hello"):
                addr = "%s@%s" % (local, domain)
                if addr in existing:
                    continue
                cf.post("/zones/%s/email/routing/rules" % zone["id"], {"name": local, "enabled": True, "matchers": [{"type": "literal", "field": "to", "value": addr}], "actions": [{"type": "forward", "value": [notify_to]}]})
                ok("%s forwards to %s" % (addr, notify_to))
                existing.add(addr)
            status["rules"] = sorted(existing)
        except CloudflareError as e:
            warn("email addresses on the domain: %s (retried on the next run)" % first(e))
    return status


def step_build():
    sys.path.insert(0, str(HERE))
    import build as builder  # noqa: E402

    return builder.build().read_bytes()


def step_upload(cf, account, code, bindings):
    metadata = {"main_module": "worker.js", "compatibility_date": COMPAT_DATE, "bindings": bindings, "observability": {"enabled": True}}
    parts = [("metadata", None, "application/json", json.dumps(metadata).encode()), ("worker.js", "worker.js", "application/javascript+module", code)]
    return cf.put("/accounts/%s/workers/scripts/%s" % (account, SCRIPT), multipart=parts)


def step_workers_dev(cf, account, create=True):
    sub = None
    try:
        sub = (cf.get("/accounts/%s/workers/subdomain" % account) or {}).get("subdomain")
    except CloudflareError:
        sub = None
    if not sub and create:
        try:
            sub = (cf.put("/accounts/%s/workers/subdomain" % account, {"subdomain": "horus-" + secrets.token_hex(3)}) or {}).get("subdomain")
        except CloudflareError as e:
            warn("workers.dev test address: %s" % first(e))
            return None
    if not sub:
        return None
    if create:
        try:
            cf.post("/accounts/%s/workers/scripts/%s/subdomain" % (account, SCRIPT), {"enabled": True, "previews_enabled": False})
        except CloudflareError as e:
            warn("workers.dev test address: %s" % first(e))
            return None
    return "https://%s.%s.workers.dev" % (SCRIPT, sub)


def step_domains(cf, account, zone, domain):
    results = {}
    for host in (domain, "www." + domain):
        body = {"zone_id": zone["id"], "hostname": host, "service": SCRIPT, "environment": "production"}
        try:
            existing = cf.get("/accounts/%s/workers/domains" % account, params={"zone_id": zone["id"], "hostname": host}) or []
            if any(d.get("service") == SCRIPT for d in existing):
                results[host] = "attached"
                continue
            try:
                cf.put("/accounts/%s/workers/domains" % account, body)
            except CloudflareError as e:
                msg = " ".join((err.get("message") or "") for err in e.errors).lower()
                if not any(w in msg for w in ("record", "exist", "conflict", "already")):
                    raise
                for rec in cf.get("/zones/%s/dns_records" % zone["id"], params={"name": host, "per_page": 50}) or []:
                    if rec.get("type") in ("A", "AAAA", "CNAME"):
                        cf.delete("/zones/%s/dns_records/%s" % (zone["id"], rec["id"]))
                cf.put("/accounts/%s/workers/domains" % account, body)
            results[host] = "attached"
            ok("%s points at the site" % host)
        except CloudflareError as e:
            results[host] = "pending"
            warn("%s: %s (retried on the next run)" % (host, first(e)))
    return results


def health(url, timeout=25):
    try:
        req = urllib.request.Request(url + "/api/health", headers={"Accept": "application/json", "User-Agent": "horus-deploy"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}


# ---- main --------------------------------------------------------------------------------------
def main(argv):
    mode = argv[1] if len(argv) > 1 else "deploy"
    if mode not in ("deploy", "status"):
        fail("usage: deploy.py [deploy|status]")
    env = read_env()
    token = env.get("CLOUDFLARE_API_TOKEN")
    if not token:
        fail("no Cloudflare token in backend/.env yet: run ~/Horus/configure-site")
    domain = (env.get("HORUS_SITE_DOMAIN") or "horushq.ai").strip().lower()
    notify_to = env.get("HORUS_INTAKE_NOTIFY_EMAIL") or env.get("HORUS_MAIL_USER")
    if not notify_to:
        fail("no notification address: run ~/Horus/configure-site")
    intake_token = env.get("HORUS_INTAKE_TOKEN")
    if not intake_token:
        intake_token = secrets.token_hex(32)
        set_env("HORUS_INTAKE_TOKEN", intake_token)
    cf = CF(token)

    say("Horus website: " + ("status" if mode == "status" else "publishing to Cloudflare"))
    step_token(cf)
    account = step_account(cf, env)
    zone = step_zone(cf, account, domain)
    active = zone.get("status") == "active"
    ok("%s on Cloudflare: %s" % (domain, zone.get("status")))

    notifications = False
    if mode == "deploy":
        kv_id = step_kv(cf, account)
        email = step_email(cf, account, zone, domain, notify_to)
        say("Uploading the site and the intake API")
        code = step_build()
        bindings = [
            {"type": "kv_namespace", "name": "INTAKE", "namespace_id": kv_id},
            {"type": "plain_text", "name": "SITE_DOMAIN", "text": domain},
            {"type": "plain_text", "name": "NOTIFY_TO", "text": notify_to},
            {"type": "secret_text", "name": "INTAKE_TOKEN", "text": intake_token},
        ]
        if email["routing"] and email["verified"]:
            bindings.append({"type": "send_email", "name": "NOTIFY", "destination_address": notify_to})
        try:
            step_upload(cf, account, code, bindings)
            notifications = any(b["type"] == "send_email" for b in bindings)
        except CloudflareError as e:
            if any(b["type"] == "send_email" for b in bindings):
                warn("upload with email notifications failed (%s); uploading without them" % first(e))
                bindings = [b for b in bindings if b["type"] != "send_email"]
                try:
                    step_upload(cf, account, code, bindings)
                except CloudflareError as e2:
                    fail("upload failed: %s" % e2)
            else:
                fail("upload failed: %s" % e)
        ok("site and intake API uploaded" + (" with email notifications" if notifications else " (email notifications turn on once the address is verified)"))
        test_url = step_workers_dev(cf, account)
        domains = step_domains(cf, account, zone, domain)
        if active:
            step_zone_settings(cf, zone)
    else:
        email = email_status(cf, account, zone, notify_to)
        test_url = step_workers_dev(cf, account, create=False)
        domains = {}
        try:
            for d in cf.get("/accounts/%s/workers/domains" % account, params={"zone_id": zone["id"]}) or []:
                if d.get("service") == SCRIPT:
                    domains[d["hostname"]] = "attached"
        except CloudflareError:
            pass
        h = health(test_url) if test_url else {}
        notifications = bool(h.get("notifications"))

    say("Checks")
    site_url = None
    if test_url:
        h = health(test_url)
        if h.get("ok"):
            ok("test address %s is live (version %s)" % (test_url, h.get("version")))
            site_url = test_url
        else:
            warn("test address %s is not reachable yet (%s)" % (test_url, h.get("error", "")))
    if active:
        if domains.get(domain) == "attached":
            h = health("https://" + domain)
            if h.get("ok"):
                ok("https://%s is live" % domain)
                site_url = "https://" + domain
            else:
                warn("https://%s does not answer yet (%s); certificates can take a few minutes after the domain activates" % (domain, h.get("error", "")))
        else:
            warn("%s is not attached to the site yet; run ~/Horus/deploy-site again" % domain)
    if site_url and mode == "deploy":
        set_env("HORUS_SITE_URL", site_url)
        ok("the intake watcher will use %s" % site_url)
    ok("email notifications to %s: %s" % (notify_to, "on" if notifications else "off"))
    if email.get("rules"):
        ok("addresses on the domain: " + ", ".join(email["rules"]))

    todo = []
    if not active:
        ns = zone.get("name_servers") or []
        todo.append("At GoDaddy, set the nameservers of %s to:\n       %s\n     (godaddy.com, My Products, the domain, DNS, Nameservers, Change Nameservers, 'I'll use my own nameservers', save). Cloudflare activates the domain when it sees the change, usually within an hour." % (domain, "\n       ".join(ns) if ns else "(not assigned yet; run this again in a minute)"))
    if not email.get("verified"):
        todo.append("Open the Cloudflare verification email sent to %s and click its link, so new requests can be emailed to you." % notify_to)
    if todo:
        say("Still needed from you")
        for i, t in enumerate(todo, 1):
            print("  %d. %s" % (i, t))
        print("  Then run ~/Horus/deploy-site again to finish. It is safe to run as often as you like.")
    else:
        say("Nothing more is needed from you." + (" The site is live at https://%s." % domain if site_url == "https://" + domain else ""))


if __name__ == "__main__":
    main(sys.argv)
