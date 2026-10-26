"""OECD SDMX API. Usage: oecd.py <dataflow path e.g. OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA,1.1> <key e.g. Q..EGY...> [--start 2015]
Returns the raw JSON; shape the series yourself (SDMX-JSON)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _http import emit, fail, get, source_record  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataflow")
    ap.add_argument("key", nargs="?", default="all")
    ap.add_argument("--start", default=None)
    a = ap.parse_args()
    url = f"https://sdmx.oecd.org/public/rest/data/{a.dataflow}/{a.key}"
    params = {"format": "jsondata"}
    if a.start:
        params["startPeriod"] = a.start
    try:
        payload = get(url, params, accept="application/vnd.sdmx.data+json").json()
    except Exception as exc:
        fail(f"OECD request failed: {exc}")
    emit({"data": payload, "source": source_record(f"OECD {a.dataflow} {a.key}", url, "OECD", "official_statistics", "A", "OECD statistical database via SDMX", query=f"{a.dataflow} {a.key}", independence_group="oecd")})


if __name__ == "__main__":
    main()
