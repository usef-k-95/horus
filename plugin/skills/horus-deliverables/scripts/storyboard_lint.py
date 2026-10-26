"""Lint a Horus storyboard (ghost deck) before rendering.

Checks: one `## Slide N` block per slide with an action title of at most two lines (about 180
characters), an `archetype:` id, at least one `evidence:` ID per exhibit slide, a `source:` line
when an exhibit is present, and that every EVD id exists in the engagement state.

Usage: storyboard_lint.py <storyboard.md> [--workspace <engagement folder>] [--max-title 180]
Exit code 0 when clean, 1 when any error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SLIDE = re.compile(r"^##\s+Slide\s+(\d+)", re.I)
FIELD = re.compile(r"^\s*(title|archetype|section|exhibit|evidence|source(?: line)?|so[ _]what|draws on|body|notes)\s*:\s*(.*)$", re.I)
EVD = re.compile(r"EVD-\d{3,5}")
KNOWN_ARCHETYPES = {
    "executive_summary", "context_and_mandate", "problem_statement", "issue_tree", "baseline_trend", "benchmark_table", "stakeholder_landscape", "public_sentiment", "decision_maker_priorities", "option_landscape", "options_screening_funnel", "guiding_principles", "appraisal_comparison", "cost_benefit_waterfall", "distributional_incidence", "sensitivity_tornado", "delivery_trajectory", "operating_model_comparison", "five_case_summary", "service_blueprint", "risk_matrix", "implementation_roadmap", "governance_raci", "kpi_dashboard", "communication_matrix", "decisions_sought", "next_steps", "section_divider", "text_only",
}


def parse(text: str) -> list[dict]:
    slides: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        m = SLIDE.match(line)
        if m:
            current = {"n": int(m.group(1)), "fields": {}, "lines": []}
            slides.append(current)
            continue
        if current is None:
            continue
        f = FIELD.match(line)
        if f:
            key = f.group(1).lower().replace(" line", "").replace("so what", "so_what")
            current["fields"].setdefault(key, []).append(f.group(2).strip())
        current["lines"].append(line)
    return slides


def state_evidence_ids(workspace: Path | None) -> set[str] | None:
    if workspace is None:
        return None
    folder = workspace / ".horus" / "evidence"
    if not folder.exists():
        return None
    return {p.stem for p in folder.glob("EVD-*.yaml")}


def lint(path: Path, workspace: Path | None, max_title: int) -> list[str]:
    slides = parse(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if not slides:
        return ["no `## Slide N` blocks found"]
    known = state_evidence_ids(workspace)
    for s in slides:
        f = s["fields"]
        title = " ".join(f.get("title", []))
        if not title:
            errors.append(f"slide {s['n']}: missing title")
        elif len(title) > max_title:
            errors.append(f"slide {s['n']}: title too long ({len(title)} chars > {max_title}); action titles are at most two lines")
        elif not title.rstrip().endswith((".", "?", "!")) and len(title.split()) < 6:
            errors.append(f"slide {s['n']}: title is a label, not a full-sentence insight: {title!r}")
        arche = (f.get("archetype") or [""])[0]
        if not arche:
            errors.append(f"slide {s['n']}: missing archetype")
        elif arche not in KNOWN_ARCHETYPES:
            errors.append(f"slide {s['n']}: unknown archetype {arche!r}")
        exhibit_value = (f.get("exhibit") or [""])[0].lower()
        nested_exhibit = any(l.strip().lower().startswith(("type:", "series:")) for l in s["lines"])
        has_exhibit = bool(f.get("exhibit")) and exhibit_value not in ("none", "n/a", "no exhibit") and (exhibit_value != "" or nested_exhibit)
        evidence_text = " ".join(f.get("evidence", []))
        ids = set(EVD.findall(evidence_text))
        if "GAP" in evidence_text:
            errors.append(f"slide {s['n']}: evidence GAP unresolved; raise a research brief before rendering")
        if has_exhibit and not ids:
            errors.append(f"slide {s['n']}: exhibit without evidence IDs")
        if has_exhibit and not f.get("source"):
            errors.append(f"slide {s['n']}: exhibit without a source line")
        if known is not None:
            for ref in sorted(ids - known):
                errors.append(f"slide {s['n']}: evidence {ref} not found in state")
        if not f.get("so_what") and arche not in ("section_divider", "executive_summary", "next_steps", "decisions_sought"):
            errors.append(f"slide {s['n']}: missing so_what")
    titles = [" ".join(s["fields"].get("title", [])) for s in slides]
    if len(set(titles)) != len(titles):
        errors.append("duplicate action titles: the story repeats itself")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--workspace", default=None)
    ap.add_argument("--max-title", type=int, default=180)
    a = ap.parse_args()
    errors = lint(Path(a.storyboard), Path(a.workspace) if a.workspace else None, a.max_title)
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} issue(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
