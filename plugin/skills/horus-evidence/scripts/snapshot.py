"""Save a web page or PDF into the engagement library so a citation can be reproduced.

Two-step flow (the source ID is only known after `create`):
    snapshot.py fetch <url> [--library library]            → library/incoming/sha256-<prefix>.<ext>, prints hash and access block
    snapshot.py finalise <hash-prefix> <SRC-id> [--library library] → renames to library/<SRC-id>.<ext>, prints the new path
One-step flow when the ID is already known:
    snapshot.py <url> <library dir> --id SRC-0022
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _http import emit, fail, get, now, sha256  # noqa: E402


def _fetch(url: str, library: Path, source_id: str | None) -> dict:
    try:
        response = get(url, accept="*/*", timeout=60)
    except Exception as exc:
        fail(f"fetch failed: {exc}")
    ctype = response.headers.get("content-type", "").split(";")[0].strip()
    ext = ".pdf" if "pdf" in ctype or url.lower().endswith(".pdf") else (".html" if "html" in ctype else ".bin")
    digest = sha256(response.content)
    if source_id:
        target = library / f"{source_id}{ext}"
    else:
        target = library / "incoming" / f"sha256-{digest[7:19]}{ext}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    title = None
    if ext == ".html":
        m = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.I | re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
    return {"url": url, "snapshot_path": str(target), "hash": digest, "hash_prefix": digest[7:19], "content_type": ctype, "bytes": len(response.content), "title": title, "access": {"retrieved_at": now(), "snapshot_path": str(target), "hash": digest, "paywalled": False}}


def _finalise(prefix: str, source_id: str, library: Path) -> dict:
    prefix = prefix.replace("sha256:", "").replace("sha256-", "")[:12]
    matches = list((library / "incoming").glob(f"sha256-{prefix}*"))
    if not matches:
        fail(f"no incoming snapshot with hash prefix {prefix}")
    src = matches[0]
    target = library / f"{source_id}{src.suffix}"
    src.rename(target)
    return {"snapshot_path": str(target), "source_id": source_id, "moved_from": str(src)}


def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] == "fetch":
        ap = argparse.ArgumentParser(prog="snapshot.py fetch")
        ap.add_argument("url")
        ap.add_argument("--library", default="library")
        a = ap.parse_args(argv[1:])
        emit(_fetch(a.url, Path(a.library), None))
        return
    if argv and argv[0] == "finalise":
        ap = argparse.ArgumentParser(prog="snapshot.py finalise")
        ap.add_argument("hash_prefix")
        ap.add_argument("source_id")
        ap.add_argument("--library", default="library")
        a = ap.parse_args(argv[1:])
        emit(_finalise(a.hash_prefix, a.source_id, Path(a.library)))
        return
    ap = argparse.ArgumentParser(prog="snapshot.py")
    ap.add_argument("url")
    ap.add_argument("library")
    ap.add_argument("--id", default=None, help="Source id to use in the file name")
    a = ap.parse_args(argv)
    emit(_fetch(a.url, Path(a.library), a.id))


if __name__ == "__main__":
    main()
