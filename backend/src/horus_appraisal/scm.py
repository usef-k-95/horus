"""Standard Cost Model for administrative burdens and compliance costs (EU and OECD practice):
cost = population × frequency × time × tariff, plus out-of-pocket items, split one-off and recurring."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Obligation:
    name: str
    population: float            # entities that must comply
    frequency_per_year: float    # how often each must act
    hours_per_action: float
    tariff_per_hour: float       # loaded hourly cost of the person doing it
    out_of_pocket_per_action: float = 0.0
    one_off: bool = False
    overhead_rate: float = 0.25  # EU SCM convention adds overhead to wage costs; set 0 to exclude

    def annual_cost(self) -> float:
        labour = self.hours_per_action * self.tariff_per_hour * (1 + self.overhead_rate)
        return self.population * self.frequency_per_year * (labour + self.out_of_pocket_per_action)


@dataclass
class SCMResult:
    one_off: float
    recurring_per_year: float
    by_obligation: dict[str, float] = field(default_factory=dict)

    def present_value(self, years: int, schedule="green_book") -> float:
        from .cba import present_value

        flows = [self.one_off + self.recurring_per_year] + [self.recurring_per_year] * (years - 1)
        return present_value(flows, schedule)

    def as_dict(self) -> dict:
        return {"one_off": round(self.one_off, 2), "recurring_per_year": round(self.recurring_per_year, 2), "by_obligation": {k: round(v, 2) for k, v in self.by_obligation.items()}}


def standard_cost_model(obligations: list[Obligation]) -> SCMResult:
    one_off = 0.0
    recurring = 0.0
    detail = {}
    for ob in obligations:
        cost = ob.annual_cost()
        detail[ob.name] = cost
        if ob.one_off:
            one_off += cost
        else:
            recurring += cost
    return SCMResult(one_off, recurring, detail)
