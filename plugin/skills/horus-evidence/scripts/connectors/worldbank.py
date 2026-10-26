"""World Bank Indicators API. Usage: worldbank.py <indicator e.g. NY.GDP.MKTP.CD> <ISO3> [--start 2015 --end 2025]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _http import emit, fail, get, source_record  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("indicator")
    ap.add_argument("country")
    ap.add_argument("--start", type=int, default=2010)
    ap.add_argument("--end", type=int, default=2026)
    a = ap.parse_args()
    url = f"https://api.worldbank.org/v2/country/{a.country}/indicator/{a.indicator}"
    params = {"format": "json", "date": f"{a.start}:{a.end}", "per_page": 200}
    try:
        payload = get(url, params).json()
    except Exception as exc:
        fail(f"World Bank request failed: {exc}")
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        fail(f"no data: {payload}")
    rows = [{"year": r["date"], "value": r["value"], "indicator": r["indicator"]["value"], "country": r["country"]["value"]} for r in payload[1]]
    emit({"rows": rows, "source": source_record(f"{rows[0]['indicator']} for {rows[0]['country']}" if rows else a.indicator, f"{url}?format=json&date={a.start}:{a.end}", "World Bank", "official_statistics", "A", "World Bank World Development Indicators, flagship dataset", query=f"{a.indicator} {a.country} {a.start}-{a.end}", independence_group="world-bank")})


if __name__ == "__main__":
    main()
