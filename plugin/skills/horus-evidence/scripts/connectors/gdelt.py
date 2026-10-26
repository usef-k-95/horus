"""GDELT 2.0 DOC API: media volume and tone over time for a query. Usage: gdelt.py "<query>" [--days 90] [--country EG]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _http import emit, fail, get, source_record  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--country", default=None, help="FIPS country code filter, e.g. EG")
    a = ap.parse_args()
    q = a.query + (f" sourcecountry:{a.country}" if a.country else "")
    base = "https://api.gdeltproject.org/api/v2/doc/doc"
    try:
        volume = get(base, {"query": q, "mode": "timelinevol", "timespan": f"{a.days}d", "format": "json"}).json()
        tone = get(base, {"query": q, "mode": "timelinetone", "timespan": f"{a.days}d", "format": "json"}).json()
    except Exception as exc:
        fail(f"GDELT request failed: {exc}")
    emit({"query": q, "volume": volume, "tone": tone, "source": source_record(f"GDELT media coverage: {a.query}", base, "GDELT Project", "dataset", "C", "GDELT global news monitoring; use for volume and tone signals, not facts", query=q, independence_group="gdelt")})


if __name__ == "__main__":
    main()
