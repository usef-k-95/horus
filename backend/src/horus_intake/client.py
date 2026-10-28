"""Settings and the HTTP client for the site's intake API (web/worker/worker-src.js)."""

from __future__ import annotations

import glob
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

BACKEND = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND / ".env"

# What the unattended kick-off session may use. State goes through the horus-state tools; research through
# WebSearch and WebFetch and the evidence scripts (python3). Nothing here can send an email or join a meeting.
DEFAULT_TOOLS = [
    "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "LS", "WebSearch", "WebFetch", "Agent", "Task", "Skill", "TodoWrite",
    "mcp__plugin_horus_horus-state", "mcp__horus-state",
    "Bash(python3:*)", "Bash(git:*)", "Bash(curl:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)", "Bash(wc:*)",
    "Bash(file:*)", "Bash(find:*)", "Bash(grep:*)", "Bash(mkdir:*)", "Bash(cp:*)", "Bash(mv:*)",
]


def find_claude() -> Optional[str]:
    """The claude command: PATH first, then the copy bundled with the Claude desktop app (newest version)."""
    forced = os.getenv("HORUS_CLAUDE_BIN")
    if forced and os.access(forced, os.X_OK):
        return forced
    on_path = shutil.which("claude")
    if on_path:
        return on_path
    pattern = str(Path.home() / "Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude")

    def version_key(path: str):
        m = re.search(r"/claude-code/([^/]+)/", path)
        return tuple(int(p) if p.isdigit() else 0 for p in (m.group(1).split(".") if m else []))

    found = [p for p in glob.glob(pattern) if os.access(p, os.X_OK)]
    return sorted(found, key=version_key)[-1] if found else None


@dataclass
class IntakeSettings:
    site_url: str = ""
    token: str = ""
    autostart: bool = True
    auto_ack: bool = True
    max_turns: int = 150
    allowed_tools: list = field(default_factory=lambda: list(DEFAULT_TOOLS))
    claude_bin: Optional[str] = None
    engagements_dir: Path = field(default_factory=lambda: Path.home() / "Horus" / "engagements")
    notify_email: str = ""
    mail_user: str = ""

    @classmethod
    def load(cls) -> "IntakeSettings":
        load_dotenv(ENV_FILE, override=False)

        def flag(key: str, default: bool) -> bool:
            value = (os.getenv(key) or "").strip().lower()
            return default if not value else value not in ("0", "false", "no", "off")

        tools = (os.getenv("HORUS_INTAKE_ALLOWED_TOOLS") or "").split()
        return cls(
            site_url=(os.getenv("HORUS_SITE_URL") or "").strip().rstrip("/"),
            token=(os.getenv("HORUS_INTAKE_TOKEN") or "").strip(),
            autostart=flag("HORUS_INTAKE_AUTOSTART", True),
            auto_ack=flag("HORUS_INTAKE_AUTO_ACK", True),
            max_turns=int(os.getenv("HORUS_INTAKE_MAX_TURNS") or 150),
            allowed_tools=tools or list(DEFAULT_TOOLS),
            claude_bin=find_claude(),
            engagements_dir=Path(os.getenv("HORUS_ENGAGEMENTS_DIR") or (Path.home() / "Horus" / "engagements")).expanduser(),
            notify_email=(os.getenv("HORUS_INTAKE_NOTIFY_EMAIL") or os.getenv("HORUS_MAIL_USER") or "").strip(),
            mail_user=(os.getenv("HORUS_MAIL_USER") or "").strip(),
        )

    def missing(self) -> list[str]:
        out = []
        if not self.site_url:
            out.append("HORUS_SITE_URL (set by ~/Horus/deploy-site)")
        if not self.token:
            out.append("HORUS_INTAKE_TOKEN (set by ~/Horus/configure-site)")
        return out


class SiteClient:
    """Talks to the deployed site. Unauthenticated: health and submit. Bearer token: pending, get, download, ack."""

    def __init__(self, base_url: str, token: str = "", timeout: float = 60.0) -> None:
        self.base = base_url.rstrip("/")
        self.token = token
        self._http = httpx.Client(timeout=timeout, headers={"Accept": "application/json", "User-Agent": "horus-intake"}, follow_redirects=True)

    def _auth(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def health(self) -> dict:
        r = self._http.get(f"{self.base}/api/health")
        r.raise_for_status()
        return r.json()

    def pending(self) -> list[dict]:
        r = self._http.get(f"{self.base}/api/intake/pending", headers=self._auth())
        r.raise_for_status()
        return r.json().get("requests", [])

    def get(self, request_id: str) -> dict:
        r = self._http.get(f"{self.base}/api/intake/requests/{request_id}", headers=self._auth())
        r.raise_for_status()
        return r.json()["request"]

    def download(self, request_id: str, dest_dir: Path, fallback_name: str = "scope") -> Optional[Path]:
        with self._http.stream("GET", f"{self.base}/api/intake/requests/{request_id}/file", headers=self._auth()) as r:
            if r.status_code == 404:
                return None
            r.raise_for_status()
            name = fallback_name
            m = re.search(r'filename="([^"]+)"', r.headers.get("content-disposition", ""))
            if m:
                name = m.group(1)
            name = re.sub(r"[^A-Za-z0-9._ ()-]+", "_", Path(name).name)[:120] or fallback_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            target = dest_dir / name
            counter = 1
            while target.exists():
                target = dest_dir / f"{Path(name).stem}-{counter}{Path(name).suffix}"
                counter += 1
            with target.open("wb") as fh:
                for chunk in r.iter_bytes():
                    fh.write(chunk)
            return target

    def ack(self, request_id: str, status: str = "taken", engagement: Optional[str] = None, note: Optional[str] = None) -> dict:
        body = {"status": status}
        if engagement:
            body["engagement"] = engagement
        if note:
            body["note"] = note
        r = self._http.post(f"{self.base}/api/intake/requests/{request_id}/ack", headers=self._auth(), json=body)
        r.raise_for_status()
        return r.json()["request"]

    def submit(self, kind: str, fields: dict, file: Optional[tuple] = None) -> dict:
        """Post a request exactly as the website form does. `file` is (name, bytes, content_type)."""
        data = {k: str(v) for k, v in fields.items()}
        data["kind"] = kind
        files = {"scope_file": file} if file else None
        r = self._http.post(f"{self.base}/api/requests", data=data, files=files)
        try:
            payload = r.json()
        except ValueError:
            payload = {"ok": False, "error": r.text[:300]}
        payload["http_status"] = r.status_code
        return payload
