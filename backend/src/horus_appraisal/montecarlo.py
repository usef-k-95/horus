"""Monte Carlo simulation, percentiles, tornado (swing) analysis and switching values."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Param:
    name: str
    central: float
    low: Optional[float] = None
    high: Optional[float] = None
    distribution: str = "point"  # point | uniform | triangular | normal | lognormal

    def sample(self, rng: random.Random) -> float:
        lo = self.central if self.low is None else self.low
        hi = self.central if self.high is None else self.high
        if self.distribution == "point" or lo == hi:
            return self.central
        if self.distribution == "uniform":
            return rng.uniform(lo, hi)
        if self.distribution == "triangular":
            return rng.triangular(lo, hi, self.central)
        if self.distribution == "normal":
            sigma = (hi - lo) / (2 * 1.645)  # treat low/high as a 90% interval
            return rng.gauss(self.central, sigma)
        if self.distribution == "lognormal":
            mu = math.log(max(self.central, 1e-12))
            sigma = (math.log(max(hi, 1e-12)) - math.log(max(lo, 1e-12))) / (2 * 1.645)
            return math.exp(rng.gauss(mu, sigma))
        raise ValueError(f"unknown distribution {self.distribution}")


def percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def simulate(model: Callable[[dict[str, float]], float], params: list[Param], runs: int = 5000, seed: int = 42) -> dict:
    rng = random.Random(seed)
    outcomes = []
    for _ in range(runs):
        outcomes.append(model({p.name: p.sample(rng) for p in params}))
    mean = sum(outcomes) / len(outcomes)
    return {
        "runs": runs,
        "mean": mean,
        "p5": percentile(outcomes, 0.05),
        "p50": percentile(outcomes, 0.50),
        "p95": percentile(outcomes, 0.95),
        "min": min(outcomes),
        "max": max(outcomes),
        "probability_positive": sum(1 for o in outcomes if o > 0) / len(outcomes),
    }


def tornado(model: Callable[[dict[str, float]], float], params: list[Param]) -> list[dict]:
    """Swing of the outcome when each parameter moves to its low and high with the others central."""
    base_inputs = {p.name: p.central for p in params}
    base = model(base_inputs)
    rows = []
    for p in params:
        if p.low is None and p.high is None:
            continue
        low_out = model({**base_inputs, p.name: p.low if p.low is not None else p.central})
        high_out = model({**base_inputs, p.name: p.high if p.high is not None else p.central})
        rows.append({"param": p.name, "base": base, "at_low": low_out, "at_high": high_out, "swing": abs(high_out - low_out)})
    rows.sort(key=lambda r: -r["swing"])
    return rows


def switching_value(model: Callable[[dict[str, float]], float], params: list[Param], name: str, lo: float, hi: float, tol: float = 1e-6, max_iter: int = 200) -> Optional[float]:
    """Value of one parameter at which the outcome crosses zero, by bisection; None if no crossing in [lo, hi]."""
    base_inputs = {p.name: p.central for p in params}

    def f(x: float) -> float:
        return model({**base_inputs, name: x})

    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2
