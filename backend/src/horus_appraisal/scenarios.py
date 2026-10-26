"""Baseline projections and delivery trajectories."""

from __future__ import annotations


def project(start: float, growth: float, years: int, step_changes: dict[int, float] | None = None) -> list[float]:
    """Compound growth from `start`, with optional additive step changes at given years."""
    series = []
    value = start
    for year in range(years):
        if year > 0:
            value *= 1 + growth
        if step_changes and year in step_changes:
            value += step_changes[year]
        series.append(value)
    return series


def trajectory(baseline: list[float], target: float, target_year: int, shape: str = "linear") -> list[float]:
    """Path from the baseline's first value to the target by target_year (Barber-style trajectory)."""
    start = baseline[0]
    out = []
    for year in range(len(baseline)):
        if year >= target_year:
            out.append(target)
            continue
        frac = year / max(1, target_year)
        if shape == "s_curve":
            frac = frac * frac * (3 - 2 * frac)
        elif shape == "front_loaded":
            frac = frac ** 0.5
        out.append(start + (target - start) * frac)
    return out


def intervention_effect(baseline: list[float], effects: dict[int, float], decay: float = 0.0) -> list[float]:
    """Baseline plus effects that start in given years and persist (optionally decaying each year)."""
    out = list(baseline)
    active: list[float] = []
    for year in range(len(baseline)):
        if year in effects:
            active.append(effects[year])
        total = sum(active)
        out[year] += total
        active = [a * (1 - decay) for a in active]
    return out
