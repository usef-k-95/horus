"""Crossref DOI lookup: validates a citation and returns a formatted reference. Usage: crossref.py <doi>"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _http import emit, fail, get, source_record  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("doi")
    a = ap.parse_args()
    doi = a.doi.replace("https://doi.org/", "")
    try:
        msg = get(f"https://api.crossref.org/works/{doi}").json().get("message", {})
    except Exception as exc:
        fail(f"Crossref lookup failed (DOI may be invalid): {exc}")
    authors = ", ".join(f"{x.get('family', '')} {x.get('given', '')[:1]}." for x in msg.get("author", [])[:6])
    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
    title = (msg.get("title") or [""])[0]
    venue = (msg.get("container-title") or [""])[0]
    citation = f"{authors} ({year}). {title}. {venue}. https://doi.org/{doi}"
    src = source_record(title, f"https://doi.org/{doi}", venue or msg.get("publisher", ""), "peer_reviewed" if msg.get("type") == "journal-article" else "report", "A" if msg.get("type") == "journal-article" else "B", "DOI-registered publication validated through Crossref", independence_group=(venue or "crossref").lower().replace(" ", "-"))
    src.update({"doi": doi, "citation": citation, "authors": [f"{x.get('given', '')} {x.get('family', '')}".strip() for x in msg.get("author", [])], "publication_date": f"{year}-01-01" if year else None})
    emit({"valid": True, "citation": citation, "source": src})


if __name__ == "__main__":
    main()
