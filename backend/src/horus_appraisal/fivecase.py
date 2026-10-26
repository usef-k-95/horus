"""Five Case Model helpers: optimism-bias uplift and the appraisal summary table (HM Treasury Green Book)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .cba import CBAResult

# Upper-bound optimism-bias uplifts on capital costs by project type, from the HM Treasury Green Book
# supplementary guidance on optimism bias (upper bounds before mitigation; equipment and development is
# 200 per cent). Take the current table and the mitigation adjustments from the live guidance for a real
# appraisal; these constants exist so the pattern is explicit, not to replace the guidance.
OPTIMISM_BIAS_UPPER = {
    "standard_building": 0.24,
    "non_standard_building": 0.51,
    "standard_civil_engineering": 0.44,
    "non_standard_civil_engineering": 0.66,
    "equipment_development": 2.00,
    "outsourcing": 0.41,
}


def apply_optimism_bias(cost: float, uplift: float) -> float:
    return cost * (1 + uplift)


@dataclass
class OptionAppraisal:
    option: str
    cba: CBAResult
    unmonetised_benefits: list[str] = field(default_factory=list)
    unmonetised_costs: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    affordability_note: str = ""


def appraisal_summary_table(options: list[OptionAppraisal]) -> list[dict]:
    rows = []
    for o in options:
        rows.append({
            "option": o.option,
            "pv_costs": round(o.cba.pv_costs, 1),
            "pv_benefits": round(o.cba.pv_benefits, 1),
            "npsv": round(o.cba.npv, 1),
            "bcr": None if o.cba.bcr is None else round(o.cba.bcr, 2),
            "unmonetised_benefits": "; ".join(o.unmonetised_benefits),
            "unmonetised_costs": "; ".join(o.unmonetised_costs),
            "key_risks": "; ".join(o.risks),
            "affordability": o.affordability_note,
        })
    ranked = sorted((r for r in rows if r["npsv"] is not None), key=lambda r: -r["npsv"])
    for i, r in enumerate(ranked, 1):
        r["rank_by_npsv"] = i
    return rows
