"""Multi-criteria analysis: normalisation, weighted scores, ranks, and rank robustness under weight perturbation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Criterion:
    name: str
    weight: float
    higher_is_better: bool = True


@dataclass
class MCAResult:
    scores: dict[str, float]
    ranking: list[str]
    normalised: dict[str, dict[str, float]] = field(default_factory=dict)
    robustness: dict[str, float] = field(default_factory=dict)  # probability of ranking first

    def as_dict(self) -> dict:
        return {"scores": {k: round(v, 4) for k, v in self.scores.items()}, "ranking": self.ranking, "robustness": {k: round(v, 3) for k, v in self.robustness.items()}}


def normalise(raw: dict[str, dict[str, float]], criteria: list[Criterion]) -> dict[str, dict[str, float]]:
    """Min-max normalisation to 0..1 per criterion, flipping direction where lower is better."""
    out: dict[str, dict[str, float]] = {o: {} for o in raw}
    for c in criteria:
        values = [raw[o][c.name] for o in raw]
        lo, hi = min(values), max(values)
        for o in raw:
            v = raw[o][c.name]
            n = 0.5 if hi == lo else (v - lo) / (hi - lo)
            out[o][c.name] = n if c.higher_is_better else 1 - n
    return out


def weighted_scores(normalised: dict[str, dict[str, float]], criteria: list[Criterion]) -> dict[str, float]:
    total_w = sum(c.weight for c in criteria) or 1.0
    return {o: sum(normalised[o][c.name] * c.weight for c in criteria) / total_w for o in normalised}


def mca(raw: dict[str, dict[str, float]], criteria: list[Criterion], robustness_runs: int = 2000, perturbation: float = 0.2, seed: int = 7) -> MCAResult:
    norm = normalise(raw, criteria)
    scores = weighted_scores(norm, criteria)
    ranking = sorted(scores, key=lambda o: -scores[o])
    rng = random.Random(seed)
    firsts = {o: 0 for o in raw}
    for _ in range(robustness_runs):
        perturbed = [Criterion(c.name, max(0.0, c.weight * (1 + rng.uniform(-perturbation, perturbation))), c.higher_is_better) for c in criteria]
        s = weighted_scores(norm, perturbed)
        firsts[max(s, key=s.get)] += 1
    return MCAResult(scores, ranking, norm, {o: n / robustness_runs for o, n in firsts.items()})
