/* Horus website worker (Cloudflare Workers, free plan).
   Serves the one-page site and runs the intake API:
     POST /api/requests                         the two forms post here (multipart, with the scope document)
     GET  /api/intake/pending                   new requests, for the intake watcher on the Supervisor's Mac (bearer token)
     GET  /api/intake/requests/<id>             one request                                    (bearer token)
     GET  /api/intake/requests/<id>/file        its scope document                             (bearer token)
     POST /api/intake/requests/<id>/ack         mark it taken, with the engagement code        (bearer token)
     GET  /api/health
   Every request is stored in the INTAKE KV namespace and emailed to the Supervisor through the NOTIFY
   send_email binding. build.py embeds the built site (web/dist) as the ASSETS constant below. */
import { EmailMessage } from "cloudflare:email";

const ASSETS = __ASSETS__;
const VERSION = "__VERSION__";

const MAX_FILE = 15 * 1024 * 1024; // KV holds values up to 25 MiB; email attachments stop at 20 MiB
const ATTACH_LIMIT = 20 * 1024 * 1024;
const MAX_TEXT = 60000;
const MAX_FIELD = 300;
const ALLOWED = ["pdf", "doc", "docx", "txt", "md", "rtf", "odt", "pages", "ppt", "pptx", "xls", "xlsx", "csv", "zip"];
const PER_HOUR = 8; // submissions per connection per hour
const FILE_TTL = 90 * 24 * 3600; // the engagement folder keeps the real copy; the store forgets the file after 90 days

const SECURITY = {
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "strict-origin-when-cross-origin",
  "permissions-policy": "camera=(), microphone=(), geolocation=()",
  "content-security-policy": "default-src 'self'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://cloudflareinsights.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    try {
      if (url.pathname === "/api" || url.pathname.startsWith("/api/")) return await api(request, env, url);
      return serve(request, url.pathname);
    } catch (err) {
      console.error((err && err.stack) || err);
      return json({ ok: false, error: "Something went wrong on our side. Please try again in a minute, or email hello@" + domainOf(env) + "." }, 500);
    }
  }
};

/* ---------- the site ---------- */
function serve(request, path) {
  if (request.method !== "GET" && request.method !== "HEAD") return json({ ok: false, error: "Method not allowed." }, 405);
  if (path === "/index.html") path = "/";
  const asset = ASSETS[path];
  if (!asset) return new Response("Not found", { status: 404, headers: withSecurity({ "content-type": "text/plain; charset=utf-8" }) });
  const etag = '"' + VERSION + '"';
  const headers = withSecurity({ "content-type": asset.type, "cache-control": path === "/" ? "no-cache" : "public, max-age=300", etag });
  if (request.headers.get("if-none-match") === etag) return new Response(null, { status: 304, headers });
  return new Response(request.method === "HEAD" ? null : asset.body, { headers });
}

/* ---------- the API ---------- */
async function api(request, env, url) {
  const p = url.pathname;
  if (p === "/api/health") return json({ ok: true, version: VERSION, storage: !!env.INTAKE, notifications: !!env.NOTIFY, domain: domainOf(env) });
  if (p === "/api/requests") {
    if (request.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);
    return receive(request, env);
  }
  if (p.startsWith("/api/intake/")) {
    if (!(await authorised(request, env))) return json({ ok: false, error: "Unauthorised." }, 401);
    return intake(request, env, p.slice("/api/intake/".length));
  }
  return json({ ok: false, error: "Not found." }, 404);
}

async function receive(request, env) {
  if (!env.INTAKE) return json({ ok: false, error: "The request store is not configured yet. Please email hello@" + domainOf(env) + "." }, 503);
  const ct = request.headers.get("content-type") || "";
  if (!ct.includes("multipart/form-data") && !ct.includes("application/x-www-form-urlencoded")) return json({ ok: false, error: "Send the form as multipart/form-data." }, 415);
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const rlKey = "rl:" + ip + ":" + new Date().toISOString().slice(0, 13);
  const count = parseInt((await env.INTAKE.get(rlKey)) || "0", 10);
  if (count >= PER_HOUR) return json({ ok: false, error: "Too many requests from this connection. Please try again in an hour, or email hello@" + domainOf(env) + "." }, 429);

  let form;
  try { form = await request.formData(); } catch (e) { return json({ ok: false, error: "The form could not be read. Please try again." }, 400); }
  const f = (k) => String(form.get(k) == null || typeof form.get(k) !== "string" ? "" : form.get(k)).trim();
  if (f("website")) return json({ ok: true, id: null }); // honeypot field: a bot filled it; pretend it worked
  const kind = f("kind") === "demo" ? "demo" : "engagement";
  const fields = {
    name: f("name").slice(0, MAX_FIELD), email: f("email").slice(0, MAX_FIELD), organisation: f("organisation").slice(0, MAX_FIELD),
    country: f("country").slice(0, MAX_FIELD), preferred_week: f("preferred_week").slice(0, MAX_FIELD), scope_text: f("scope_text").slice(0, MAX_TEXT), page: f("page").slice(0, 500)
  };
  const missing = [];
  if (!fields.name) missing.push("your name");
  if (!fields.organisation) missing.push("the organisation");
  if (kind === "engagement" && !fields.country) missing.push("the country");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email)) missing.push("a valid work email");
  const file = form.get("scope_file");
  const hasFile = !!file && typeof file === "object" && typeof file.arrayBuffer === "function" && file.size > 0;
  if (kind === "engagement" && !hasFile && !fields.scope_text) missing.push("the scope of work, attached or pasted");
  if (missing.length) return json({ ok: false, error: "Please add " + missing.join(", ") + "." }, 400);

  let attachment = null, bytes = null;
  if (hasFile) {
    if (file.size > MAX_FILE) return json({ ok: false, error: "The document is larger than 15 MB. Please attach a smaller file, or submit without it and email it to hello@" + domainOf(env) + "." }, 413);
    const name = safeName(file.name || "scope");
    const ext = (name.split(".").pop() || "").toLowerCase();
    if (!ALLOWED.includes(ext)) return json({ ok: false, error: "That file type is not accepted. Please attach a PDF, Word, text or Pages document." }, 415);
    bytes = new Uint8Array(await file.arrayBuffer());
    attachment = { name, type: file.type || "application/octet-stream", size: bytes.length };
  }

  const id = newId();
  const record = Object.assign({ id, kind, status: "new", received_at: new Date().toISOString(), attachment, cf_country: (request.cf && request.cf.country) || null, notified: false }, fields);
  await env.INTAKE.put(rlKey, String(count + 1), { expirationTtl: 3600 });
  if (bytes) await env.INTAKE.put("file:" + id, bytes, { expirationTtl: FILE_TTL, metadata: attachment });
  await putRecord(env, record);
  if (env.NOTIFY) {
    try { await notify(env, record, bytes); record.notified = true; }
    catch (e) { record.notify_error = String((e && e.message) || e).slice(0, 300); }
    await putRecord(env, record);
  }
  return json({ ok: true, id });
}

async function intake(request, env, rest) {
  if (!env.INTAKE) return json({ ok: false, error: "The request store is not configured." }, 503);
  if (rest === "pending") {
    if (request.method !== "GET") return json({ ok: false, error: "Method not allowed." }, 405);
    const out = [];
    let cursor;
    do {
      const page = await env.INTAKE.list({ prefix: "req:", cursor, limit: 1000 });
      for (const k of page.keys) {
        if (k.metadata && k.metadata.status && k.metadata.status !== "new") continue;
        const r = await env.INTAKE.get(k.name, "json");
        if (r && r.status === "new") out.push(r);
      }
      cursor = page.list_complete ? undefined : page.cursor;
    } while (cursor);
    out.sort((a, b) => (a.received_at < b.received_at ? -1 : 1));
    return json({ ok: true, requests: out });
  }
  const m = rest.match(/^requests\/([A-Z0-9-]+)(\/file|\/ack)?$/);
  if (!m) return json({ ok: false, error: "Not found." }, 404);
  const id = m[1];
  const record = await env.INTAKE.get("req:" + id, "json");
  if (!record) return json({ ok: false, error: "No such request." }, 404);
  if (!m[2]) return json({ ok: true, request: record });
  if (m[2] === "/file") {
    const got = await env.INTAKE.getWithMetadata("file:" + id, "arrayBuffer");
    if (!got || !got.value) return json({ ok: false, error: "No file for this request: none was attached, or it has expired." }, 404);
    const meta = got.metadata || record.attachment || {};
    return new Response(got.value, { headers: withSecurity({ "content-type": meta.type || "application/octet-stream", "content-disposition": 'attachment; filename="' + asciiName(meta.name || id) + '"', "cache-control": "no-store" }) });
  }
  if (request.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);
  let body = {};
  try { body = await request.json(); } catch (e) { body = {}; }
  record.status = ["taken", "ignored", "new"].includes(body.status) ? body.status : "taken";
  record.taken_at = new Date().toISOString();
  if (body.engagement) record.engagement = String(body.engagement).slice(0, 80);
  if (body.note) record.note = String(body.note).slice(0, 500);
  await putRecord(env, record);
  return json({ ok: true, request: record });
}

/* ---------- the notification to the Supervisor ---------- */
async function notify(env, r, bytes) {
  const domain = domainOf(env);
  const to = env.NOTIFY_TO;
  if (!to) throw new Error("NOTIFY_TO is not set");
  const from = "intake@" + domain;
  const what = r.kind === "demo" ? "demo request" : "scope of work";
  const subject = "[Horus intake] " + r.id + " · " + (r.kind === "demo" ? "demo" : "engagement") + " · " + r.organisation;
  const attachable = !!bytes && bytes.length <= ATTACH_LIMIT;
  const lines = [
    "A " + what + " arrived through " + domain + ".", "",
    "Request       " + r.id,
    "Received      " + r.received_at,
    "Kind          " + r.kind,
    "From          " + r.name + " <" + r.email + ">",
    "Organisation  " + r.organisation,
    "Country       " + (r.country || "-"),
    r.kind === "demo" ? "Preferred     " + (r.preferred_week || "-") : null,
    "Document      " + (r.attachment ? r.attachment.name + " (" + human(r.attachment.size) + ")" + (attachable ? ", attached" : ", too large to attach; the watcher downloads it") : "none"),
    "", "Scope as submitted:", "", r.scope_text || "(no text; see the document)", "",
    "If the intake watcher is on (~/Horus/intake status), Horus opens the engagement folder under ~/Horus/engagements and starts the kick-off within two minutes. Otherwise run ~/Horus/intake pull. Replying to this email reaches the requester."
  ].filter((l) => l !== null);
  const boundary = "horus-" + crypto.randomUUID();
  let raw = "From: Horus intake <" + from + ">\r\nTo: " + to + "\r\nReply-To: " + r.email.replace(/[\r\n]/g, "") + "\r\nSubject: " + encodeHeader(subject) +
    "\r\nDate: " + new Date().toUTCString() + "\r\nMessage-ID: <" + r.id.toLowerCase() + "." + Date.now() + "@" + domain + ">\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=\"" + boundary + "\"\r\n\r\n";
  raw += "--" + boundary + "\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" + wrap76(b64(new TextEncoder().encode(lines.join("\r\n")))) + "\r\n";
  if (attachable) {
    const name = asciiName(r.attachment.name);
    raw += "--" + boundary + "\r\nContent-Type: " + r.attachment.type.replace(/[^\w.+\/-]/g, "") + "; name=\"" + name + "\"\r\nContent-Disposition: attachment; filename=\"" + name + "\"\r\nContent-Transfer-Encoding: base64\r\n\r\n" + wrap76(b64(bytes)) + "\r\n";
  }
  raw += "--" + boundary + "--\r\n";
  await env.NOTIFY.send(new EmailMessage(from, to, raw));
}

/* ---------- helpers ---------- */
async function authorised(request, env) {
  const h = request.headers.get("authorization") || "";
  const token = h.startsWith("Bearer ") ? h.slice(7).trim() : "";
  if (!token || !env.INTAKE_TOKEN) return false;
  const enc = new TextEncoder();
  const a = await crypto.subtle.digest("SHA-256", enc.encode(token));
  const b = await crypto.subtle.digest("SHA-256", enc.encode(env.INTAKE_TOKEN));
  return crypto.subtle.timingSafeEqual(a, b);
}
function putRecord(env, r) {
  return env.INTAKE.put("req:" + r.id, JSON.stringify(r), { metadata: { status: r.status, kind: r.kind, received_at: r.received_at, organisation: (r.organisation || "").slice(0, 80) } });
}
function newId() {
  const alphabet = "ABCDEFGHJKMNPQRSTVWXYZ23456789";
  const rnd = crypto.getRandomValues(new Uint8Array(6));
  let s = "";
  for (const n of rnd) s += alphabet[n % alphabet.length];
  return "REQ-" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + "-" + s;
}
function domainOf(env) { return env.SITE_DOMAIN || "horushq.ai"; }
function json(data, status) { return new Response(JSON.stringify(data), { status: status || 200, headers: withSecurity({ "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }) }); }
function withSecurity(h) { return Object.assign({}, SECURITY, h); }
function safeName(name) { name = String(name).split(/[\\/]/).pop().replace(/[\x00-\x1f"]/g, "").trim(); return (name.length > 120 ? name.slice(-120) : name) || "scope"; }
function asciiName(name) { return String(name).replace(/[^\x20-\x7e]/g, "_").replace(/"/g, "_"); }
function human(n) { return n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(0) + " KB" : (n / 1048576).toFixed(1) + " MB"; }
function b64(bytes) { let s = ""; for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000)); return btoa(s); }
function wrap76(s) { return s.replace(/(.{76})/g, "$1\r\n"); }
function encodeHeader(s) { return /^[\x20-\x7e]*$/.test(s) ? s : "=?utf-8?B?" + b64(new TextEncoder().encode(s)) + "?="; }
