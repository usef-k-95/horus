"""Plain outputs: CSV, Markdown tables and simple SVG charts in the Horus chart style
(one highlight colour, direct labels, source line). No third-party dependencies."""

from __future__ import annotations

import csv
import html
from pathlib import Path
from typing import Sequence

PRIMARY = "#1F3A5F"
HIGHLIGHT = "#C8553D"
GREY = "#8A8F98"
TEXT = "#1A1A1A"


def write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def markdown_table(rows: list[dict], columns: Sequence[str] | None = None) -> str:
    if not rows:
        return "(no rows)"
    cols = list(columns or rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(_fmt(r.get(c)) for c in cols) + " |")
    return "\n".join(out)


def _fmt(v) -> str:
    if isinstance(v, float):
        return f"{v:,.2f}"
    return "" if v is None else str(v)


def bar_chart_svg(path: Path, labels: Sequence[str], values: Sequence[float], *, title: str, unit: str = "", source: str = "", highlight: int | None = None, width: int = 720, height: int = 400) -> Path:
    """Horizontal bar chart with direct labels. `highlight` is the index drawn in the highlight colour."""
    path.parent.mkdir(parents=True, exist_ok=True)
    margin_left, margin_top, margin_right = 220, 70, 90
    n = max(1, len(values))
    bar_h = max(16, min(40, (height - margin_top - 60) // n - 10))
    vmax = max([abs(v) for v in values] + [1e-9])
    scale = (width - margin_left - margin_right) / vmax
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Helvetica, Arial, sans-serif">',
             f'<text x="{margin_left}" y="34" font-size="20" font-weight="bold" fill="{TEXT}">{html.escape(title)}</text>']
    for i, (label, value) in enumerate(zip(labels, values)):
        y = margin_top + i * (bar_h + 10)
        w = abs(value) * scale
        colour = HIGHLIGHT if highlight == i else PRIMARY
        parts.append(f'<text x="{margin_left - 10}" y="{y + bar_h / 2 + 5}" font-size="14" text-anchor="end" fill="{TEXT}">{html.escape(str(label))}</text>')
        parts.append(f'<rect x="{margin_left}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{colour}" />')
        parts.append(f'<text x="{margin_left + w + 8:.1f}" y="{y + bar_h / 2 + 5}" font-size="14" fill="{TEXT}">{_fmt(value)}{(" " + unit) if unit else ""}</text>')
    if source:
        parts.append(f'<text x="{margin_left}" y="{height - 16}" font-size="11" fill="{GREY}">Source: {html.escape(source)}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def line_chart_svg(path: Path, series: dict[str, Sequence[float]], *, title: str, x_labels: Sequence[str] | None = None, unit: str = "", source: str = "", highlight: str | None = None, width: int = 720, height: int = 400) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ml, mt, mr, mb = 70, 70, 160, 60
    all_values = [v for s in series.values() for v in s]
    vmin, vmax = min(all_values + [0.0]), max(all_values + [1e-9])
    n = max(2, max(len(s) for s in series.values()))
    x_step = (width - ml - mr) / (n - 1)
    span = (vmax - vmin) or 1.0

    def y_of(v: float) -> float:
        return mt + (height - mt - mb) * (1 - (v - vmin) / span)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Helvetica, Arial, sans-serif">',
             f'<text x="{ml}" y="34" font-size="20" font-weight="bold" fill="{TEXT}">{html.escape(title)}</text>',
             f'<line x1="{ml}" y1="{y_of(vmin):.1f}" x2="{width - mr}" y2="{y_of(vmin):.1f}" stroke="{GREY}" stroke-width="1" />']
    for name, values in series.items():
        colour = HIGHLIGHT if name == highlight else (PRIMARY if highlight is None else GREY)
        points = " ".join(f"{ml + i * x_step:.1f},{y_of(v):.1f}" for i, v in enumerate(values))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="2.5" />')
        last_x = ml + (len(values) - 1) * x_step
        parts.append(f'<text x="{last_x + 8:.1f}" y="{y_of(values[-1]) + 5:.1f}" font-size="13" fill="{colour}">{html.escape(name)} {_fmt(values[-1])}{(" " + unit) if unit else ""}</text>')
    if x_labels:
        for i, lab in enumerate(x_labels[:n]):
            if i % max(1, n // 8) == 0 or i == n - 1:
                parts.append(f'<text x="{ml + i * x_step:.1f}" y="{height - mb + 22}" font-size="12" text-anchor="middle" fill="{GREY}">{html.escape(str(lab))}</text>')
    if source:
        parts.append(f'<text x="{ml}" y="{height - 14}" font-size="11" fill="{GREY}">Source: {html.escape(source)}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    return path
