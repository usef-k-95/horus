"""OpenAlex works search. Usage: openalex.py "<query>" [--n 10] [--from-year 2015]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _http import emit, fail, get, now  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--from-year", type=int, default=None)
    a = ap.parse_args()
    params = {"search": a.query, "per-page": a.n, "sort": "cited_by_count:desc"}
    if a.from_year:
        params["filter"] = f"from_publication_date:{a.from_year}-01-01"
    try:
        payload = get("https://api.openalex.org/works", params).json()
    except Exception as exc:
        fail(f"OpenAlex request failed: {exc}")
    works = []
    for w in payload.get("results", []):
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        works.append({"title": w.get("title"), "year": w.get("publication_year"), "doi": w.get("doi"), "venue": venue, "cited_by": w.get("cited_by_count"), "authors": [x.get("author", {}).get("display_name") for x in w.get("authorships", [])][:5], "open_access_url": (w.get("open_access") or {}).get("oa_url"), "suggested_tier": "A" if venue else "B", "retrieved_at": now()})
    emit({"query": a.query, "count": len(works), "works": works})


if __name__ == "__main__":
    main()
