"""Shared helpers for the connector scripts."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone

import httpx

UA = "Horus/0.1 (policy research; contact: supervisor)"


def get(url: str, params: dict | None = None, timeout: float = 30.0, accept: str = "application/json") -> httpx.Response:
    with httpx.Client(timeout=timeout, follow_redirects=True, headers={"User-Agent": UA, "Accept": accept}) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def source_record(title: str, url: str, publisher: str, type_: str, tier: str, rationale: str, query: str | None = None, independence_group: str | None = None) -> dict:
    return {
        "title": title,
        "type": type_,
        "publisher": publisher,
        "url": url,
        "citation": f"{publisher}, {title} (retrieved {now()[:10]})",
        "tier": tier,
        "tier_rationale": rationale,
        "independence_group": independence_group or publisher.lower().replace(" ", "-"),
        "interest_declared": "none",
        "access": {"retrieved_at": now(), "retrieved_by": "researcher", "query": query},
    }


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))


def fail(message: str) -> None:
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(1)
