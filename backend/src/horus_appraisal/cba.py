"""Discounting and cost-benefit arithmetic. Rates are real unless stated; flows are per year starting at year 0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

# Social time preference rate schedules (real). Sources: HM Treasury Green Book (3.5% for years 0–30,
# 3.0% for 31–75, 2.5% beyond); US OMB Circular A-4 2023 revision (2.0%); European Commission Better
# Regulation practice (3%). Verify against the current editions before a final appraisal.
SCHEDULES: dict[str, Callable[[int], float]] = {
    "green_book": lambda year: 0.035 if year <= 30 else (0.030 if year <= 75 else 0.025),
    "green_book_health": lambda year: 0.015 if year <= 30 else (0.01286 if year <= 75 else 0.01071),
    "omb_a4_2023": lambda year: 0.02,
    "eu": lambda year: 0.03,
    "omb_2003_3pct": lambda year: 0.03,
    "omb_2003_7pct": lambda year: 0.07,
}


def flat(rate: float) -> Callable[[int], float]:
    return lambda year: rate


def discount_factors(years: int, schedule: str | float | Callable[[int], float] = "green_book") -> list[float]:
    """Cumulative discount factors for years 0..years-1 under a (possibly declining) rate schedule."""
    fn = SCHEDULES[schedule] if isinstance(schedule, str) else (flat(schedule) if isinstance(schedule, (int, float)) else schedule)
    factors = []
    acc = 1.0
    for year in range(years):
        if year > 0:
            acc /= 1.0 + fn(year)
        factors.append(acc)
    return factors


def present_value(flows: Sequence[float], schedule="green_book") -> float:
    factors = discount_factors(len(flows), schedule)
    return sum(f * d for f, d in zip(flows, factors))


@dataclass
class CBAResult:
    pv_benefits: float
    pv_costs: float
    npv: float
    bcr: float | None
    payback_year: int | None
    years: int
    schedule: str

    def as_dict(self) -> dict:
        return {"pv_benefits": round(self.pv_benefits, 2), "pv_costs": round(self.pv_costs, 2), "npv": round(self.npv, 2), "bcr": None if self.bcr is None else round(self.bcr, 3), "payback_year": self.payback_year, "years": self.years, "schedule": self.schedule}


def cba(benefits: Sequence[float], costs: Sequence[float], schedule: str = "green_book") -> CBAResult:
    if len(benefits) != len(costs):
        raise ValueError("benefits and costs must cover the same years")
    pv_b = present_value(benefits, schedule)
    pv_c = present_value(costs, schedule)
    cumulative = 0.0
    payback = None
    factors = discount_factors(len(benefits), schedule)
    for year, (b, c, d) in enumerate(zip(benefits, costs, factors)):
        cumulative += (b - c) * d
        if cumulative >= 0 and payback is None and year > 0:
            payback = year
    return CBAResult(pv_b, pv_c, pv_b - pv_c, (pv_b / pv_c) if pv_c else None, payback, len(benefits), schedule if isinstance(schedule, str) else "custom")


def annuity_factor(rate: float, years: int) -> float:
    if rate == 0:
        return float(years)
    return (1 - (1 + rate) ** (-years)) / rate


def equivalent_annual(pv: float, rate: float, years: int) -> float:
    """Spread a present value evenly over `years` (used for equivalent annual net direct cost to business)."""
    return pv / annuity_factor(rate, years)


def real_from_nominal(nominal: Iterable[float], inflation: float) -> list[float]:
    return [v / ((1 + inflation) ** i) for i, v in enumerate(nominal)]
