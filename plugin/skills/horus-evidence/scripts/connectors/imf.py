"""IMF DataMapper API (World Economic Outlook and other datasets). Usage: imf.py <indicator e.g. NGDP_RPCH> <ISO3>"""

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
    a = ap.parse_args()
    url = f"https://www.imf.org/external/datamapper/api/v1/{a.indicator}/{a.country}"
    try:
        payload = get(url).json()
    except Exception as exc:
        fail(f"IMF request failed: {exc}")
    values = ((payload.get("values") or {}).get(a.indicator) or {}).get(a.country) or {}
    rows = [{"year": y, "value": v} for y, v in sorted(values.items())]
    emit({"rows": rows, "source": source_record(f"IMF DataMapper {a.indicator} {a.country}", url, "International Monetary Fund", "official_statistics", "A", "IMF World Economic Outlook database via DataMapper", query=f"{a.indicator} {a.country}", independence_group="imf")})


if __name__ == "__main__":
    main()
