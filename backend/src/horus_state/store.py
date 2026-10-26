"""File store: one YAML file per record, an append-only JSON Lines event log, ID counters under
a lock, version snapshots for singletons, and a derived SQLite index (STATE_SCHEMA.md §1, §10)."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import shutil
import sqlite3
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterator, Optional

import yaml

from . import SCHEMA_VERSION
from .models import COLLECTIONS, PREFIXES, SINGLETONS
from .models.records import ID_WIDTH, Event

TEXT_FIELDS = ("title", "name", "statement", "summary", "question", "paraphrase", "content_verbatim", "description", "notes", "quote_text", "citation", "purpose")


class StoreError(RuntimeError):
    pass


class NotFound(StoreError):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _yaml_safe(value: Any) -> Any:
    """Convert pydantic output into plain YAML-friendly structures."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _yaml_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_yaml_safe(v) for v in value]
    if isinstance(value, (datetime, date, str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "value"):  # enums
        return value.value
    return str(value)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


class Store:
    def __init__(self, workspace: Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.root = self.workspace / ".horus"

    # -- layout --------------------------------------------------------------------------
    @property
    def initialised(self) -> bool:
        return (self.root / "engagement.yaml").exists()

    def scaffold(self) -> None:
        for name in COLLECTIONS:
            if name not in SINGLETONS:
                (self.root / name).mkdir(parents=True, exist_ok=True)
        (self.root / "history").mkdir(parents=True, exist_ok=True)
        for folder in ("inbox", "library", "analysis", "deliverables", "meetings"):
            (self.workspace / folder).mkdir(parents=True, exist_ok=True)
        (self.root / "schema.lock").write_text(SCHEMA_VERSION + "\n", encoding="utf-8")
        gitignore = self.root / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(".index.sqlite\n.lock\n", encoding="utf-8")
        if not (self.root / "counters.json").exists():
            self._write_json(self.root / "counters.json", {})
        if not (self.root / "events.jsonl").exists():
            (self.root / "events.jsonl").touch()

    def path_for(self, collection: str, record_id: Optional[str] = None) -> Path:
        if collection in SINGLETONS:
            return self.root / f"{collection}.yaml"
        if not record_id:
            raise StoreError(f"{collection} needs a record id")
        return self.root / collection / f"{record_id}.yaml"

    # -- locking -------------------------------------------------------------------------
    @contextmanager
    def lock(self):
        self.root.mkdir(parents=True, exist_ok=True)
        lock_path = self.root / ".lock"
        with open(lock_path, "a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    # -- ids -----------------------------------------------------------------------------
    def next_id(self, collection: str) -> str:
        prefix = PREFIXES[collection]
        if collection in SINGLETONS:
            return f"{prefix}-001"
        width = ID_WIDTH.get(collection, 3)
        with self.lock():
            counters = self._read_json(self.root / "counters.json", {})
            counters[prefix] = int(counters.get(prefix, 0)) + 1
            self._write_json(self.root / "counters.json", counters)
            return f"{prefix}-{counters[prefix]:0{width}d}"

    def counters(self) -> dict[str, int]:
        return self._read_json(self.root / "counters.json", {})

    # -- records -------------------------------------------------------------------------
    def read(self, collection: str, record_id: Optional[str] = None) -> dict:
        path = self.path_for(collection, record_id)
        if not path.exists():
            raise NotFound(f"{collection}/{record_id or collection} not found")
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        return data

    def exists(self, collection: str, record_id: Optional[str] = None) -> bool:
        try:
            return self.path_for(collection, record_id).exists()
        except StoreError:
            return False

    def write(self, record: dict) -> Path:
        collection = record["collection"]
        path = self.path_for(collection, record.get("id"))
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".yaml.tmp")
        with open(tmp, "w", encoding="utf-8") as handle:
            yaml.safe_dump(_yaml_safe(record), handle, sort_keys=False, allow_unicode=True, default_flow_style=False)
        os.replace(tmp, path)
        self.index_record(record)
        return path

    def list_ids(self, collection: str) -> list[str]:
        if collection in SINGLETONS:
            return [collection] if self.path_for(collection).exists() else []
        folder = self.root / collection
        if not folder.exists():
            return []
        return sorted(p.stem for p in folder.glob("*.yaml"))

    def iter_records(self, collection: str) -> Iterator[dict]:
        for record_id in self.list_ids(collection):
            yield self.read(collection, None if collection in SINGLETONS else record_id)

    def snapshot(self, collection: str) -> Optional[Path]:
        """Copy a singleton to history/<collection>.v<N>.yaml."""
        if collection not in SINGLETONS:
            return None
        src = self.path_for(collection)
        if not src.exists():
            return None
        version = (self.read(collection) or {}).get("version", 0)
        dst = self.root / "history" / f"{collection}.v{version}.yaml"
        shutil.copy2(src, dst)
        return dst

    # -- events --------------------------------------------------------------------------
    def append_event(self, event: Event) -> None:
        line = json.dumps(_yaml_safe(event.model_dump(mode="json")), ensure_ascii=False)
        with self.lock():
            with open(self.root / "events.jsonl", "a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def iter_events(self, since: Optional[datetime] = None) -> Iterator[dict]:
        path = self.root / "events.jsonl"
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as handle:
            for raw in handle:
                raw = raw.strip()
                if not raw:
                    continue
                event = json.loads(raw)
                if since is not None and datetime.fromisoformat(event["ts"]) < since:
                    continue
                yield event

    def new_event_id(self) -> str:
        return f"EVT-{int(time.time() * 1000)}-{os.getpid() % 1000:03d}"

    # -- index ---------------------------------------------------------------------------
    @property
    def index_path(self) -> Path:
        return self.root / ".index.sqlite"

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.index_path)
        conn.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, collection TEXT, status TEXT, created_at TEXT, updated_at TEXT, json TEXT)")
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(id UNINDEXED, collection UNINDEXED, text)")
        return conn

    def index_record(self, record: dict) -> None:
        try:
            conn = self._connect()
        except sqlite3.Error:
            return
        with conn:
            rid = record["id"] if record["collection"] not in SINGLETONS else record["collection"]
            text = " ".join(str(record.get(f, "")) for f in TEXT_FIELDS if record.get(f))
            conn.execute("DELETE FROM records WHERE id = ?", (rid,))
            conn.execute("DELETE FROM records_fts WHERE id = ?", (rid,))
            conn.execute(
                "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
                (rid, record["collection"], str(record.get("status", "")), str(record.get("created_at", "")), str(record.get("updated_at", "")), json.dumps(_yaml_safe(record), default=str)),
            )
            conn.execute("INSERT INTO records_fts VALUES (?, ?, ?)", (rid, record["collection"], text))
        conn.close()

    def reindex(self) -> int:
        if self.index_path.exists():
            self.index_path.unlink()
        count = 0
        for collection in COLLECTIONS:
            for record in self.iter_records(collection):
                self.index_record(record)
                count += 1
        return count

    def search(self, query: str, collections: Optional[list[str]] = None, limit: int = 20) -> list[dict]:
        if not self.index_path.exists():
            self.reindex()
        conn = self._connect()
        safe = " ".join(f'"{tok}"' for tok in query.replace('"', " ").split()) if query.strip() else '""'
        sql = "SELECT r.id, r.collection, r.status, snippet(records_fts, 2, '[', ']', '…', 12) FROM records_fts JOIN records r ON r.id = records_fts.id WHERE records_fts MATCH ?"
        params: list[Any] = [safe]
        if collections:
            sql += " AND r.collection IN (%s)" % ",".join("?" for _ in collections)
            params.extend(collections)
        sql += " LIMIT ?"
        params.append(limit)
        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        return [{"id": r[0], "collection": r[1], "status": r[2], "snippet": r[3]} for r in rows]

    # -- helpers -------------------------------------------------------------------------
    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8") or "null") or default

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
