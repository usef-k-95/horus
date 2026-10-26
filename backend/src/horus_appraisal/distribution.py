"""Distributional incidence: who bears costs and benefits, and a simple progressivity read-out."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Group:
    name: str
    population: float
    income_share: float | None = None   # share of total income (0..1) for progressivity
    cost_per_unit: float = 0.0
    benefit_per_unit: float = 0.0


def incidence(groups: list[Group]) -> dict:
    total_cost = sum(g.population * g.cost_per_unit for g in groups)
    total_benefit = sum(g.population * g.benefit_per_unit for g in groups)
    rows = []
    for g in groups:
        cost = g.population * g.cost_per_unit
        benefit = g.population * g.benefit_per_unit
        rows.append({
            "group": g.name,
            "population": g.population,
            "cost": cost,
            "benefit": benefit,
            "net": benefit - cost,
            "cost_share": (cost / total_cost) if total_cost else 0.0,
            "benefit_share": (benefit / total_benefit) if total_benefit else 0.0,
            "income_share": g.income_share,
            "cost_to_income_ratio": (cost / total_cost) / g.income_share if (total_cost and g.income_share) else None,
        })
    verdict = None
    ratios = [r["cost_to_income_ratio"] for r in rows if r["cost_to_income_ratio"] is not None]
    if ratios and len(ratios) == len(rows):
        ordered = sorted(rows, key=lambda r: r["income_share"] or 0)
        if ordered[0]["cost_to_income_ratio"] > ordered[-1]["cost_to_income_ratio"] * 1.1:
            verdict = "regressive: lower-income groups bear a larger cost share than their income share"
        elif ordered[0]["cost_to_income_ratio"] < ordered[-1]["cost_to_income_ratio"] * 0.9:
            verdict = "progressive"
        else:
            verdict = "broadly proportional"
    return {"total_cost": total_cost, "total_benefit": total_benefit, "rows": rows, "verdict": verdict}
