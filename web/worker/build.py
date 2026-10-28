#!/usr/bin/env python3
"""Bundle the built site (web/dist) and the worker runtime into web/dist/worker.js.
Run web/build-standalone.sh first; tools/deploy-site.sh does both. Works with the system python3."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEB = HERE.parent
DIST = WEB / "dist"
TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".webmanifest": "application/manifest+json",
}


def collect() -> dict:
    assets = {}
    index = DIST / "index.html"
    if not index.exists():
        sys.exit("web/dist/index.html is missing: run web/build-standalone.sh first")
    for path in sorted(DIST.rglob("*")):
        if not path.is_file() or path.name == "worker.js" or path.name.startswith("."):
            continue
        ctype = TYPES.get(path.suffix.lower())
        if not ctype:
            print(f"  skipped {path.relative_to(DIST)} (binary assets are not embedded)", file=sys.stderr)
            continue
        key = "/" + path.relative_to(DIST).as_posix()
        if key == "/index.html":
            key = "/"
        assets[key] = {"type": ctype, "body": path.read_text(encoding="utf-8")}
    assets.setdefault("/robots.txt", {"type": TYPES[".txt"], "body": "User-agent: *\nAllow: /\n"})
    return assets


def build() -> Path:
    assets = collect()
    digest = hashlib.sha256()
    for key in sorted(assets):
        digest.update(key.encode())
        digest.update(assets[key]["body"].encode("utf-8"))
    runtime = (HERE / "worker-src.js").read_text(encoding="utf-8")
    digest.update(runtime.encode("utf-8"))
    version = digest.hexdigest()[:12]
    # JSON with ASCII escapes is valid JavaScript, including the U+2028/2029 cases plain JSON would leave raw
    for token in ("const ASSETS = __ASSETS__;", 'const VERSION = "__VERSION__";'):
        if runtime.count(token) != 1:
            sys.exit(f"worker-src.js must contain exactly one `{token}` statement")
    code = runtime.replace("const ASSETS = __ASSETS__;", "const ASSETS = " + json.dumps(assets, ensure_ascii=True) + ";", 1)
    code = code.replace('const VERSION = "__VERSION__";', 'const VERSION = "%s";' % version, 1)
    out = DIST / "worker.js"
    out.write_text(code, encoding="utf-8")
    print(f"built {out.relative_to(WEB)} ({len(code.encode('utf-8'))} bytes, {len(assets)} files, version {version})")
    return out


if __name__ == "__main__":
    build()
