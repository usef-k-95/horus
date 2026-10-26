"""Command line: `python -m horus_appraisal demo <out dir>` runs an illustrative appraisal end to end and
writes CSV, Markdown and SVG outputs, so an analyst can copy the pattern. Figures are illustrative only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from . import cba, distribution, fivecase, mca, montecarlo, report, scenarios, scm


def demo(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    years = 10
    # Illustrative: a phased e-invoicing mandate. All numbers are placeholders for the pattern.
    benefits = [0, 2.0, 6.0, 12.0, 18.0, 22.0, 24.0, 25.0, 25.0, 25.0]
    costs = [8.0, 9.0, 7.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
    result = cba.cba(benefits, costs, "green_book")
    burden = scm.standard_cost_model([
        scm.Obligation("issue e-invoices", population=250_000, frequency_per_year=120, hours_per_action=0.05, tariff_per_hour=4.0),
        scm.Obligation("register with platform", population=250_000, frequency_per_year=1, hours_per_action=2.0, tariff_per_hour=4.0, out_of_pocket_per_action=10.0, one_off=True),
    ])
    criteria = [mca.Criterion("fiscal_gain", 0.3), mca.Criterion("sme_burden", 0.3, higher_is_better=False), mca.Criterion("feasibility", 0.2), mca.Criterion("political_fit", 0.2)]
    raw = {"A phased mandate": {"fiscal_gain": 8, "sme_burden": 5, "feasibility": 7, "political_fit": 7}, "B voluntary incentives": {"fiscal_gain": 4, "sme_burden": 2, "feasibility": 8, "political_fit": 8}, "C immediate mandate": {"fiscal_gain": 9, "sme_burden": 9, "feasibility": 4, "political_fit": 3}}
    ranking = mca.mca(raw, criteria)
    params = [montecarlo.Param("adoption", 0.6, 0.4, 0.8, "triangular"), montecarlo.Param("benefit_per_firm", 100.0, 60.0, 140.0, "normal"), montecarlo.Param("cost_per_firm", 40.0, 30.0, 60.0, "triangular")]

    def model(p):
        return 250_000 * p["adoption"] * (p["benefit_per_firm"] - p["cost_per_firm"]) / 1e6

    sim = montecarlo.simulate(model, params, runs=4000)
    swings = montecarlo.tornado(model, params)
    switching = montecarlo.switching_value(model, params, "benefit_per_firm", 0.0, 200.0)
    inc = distribution.incidence([distribution.Group("micro", 200_000, 0.15, cost_per_unit=50, benefit_per_unit=60), distribution.Group("small", 40_000, 0.35, cost_per_unit=80, benefit_per_unit=140), distribution.Group("medium", 10_000, 0.50, cost_per_unit=120, benefit_per_unit=300)])
    baseline = scenarios.project(18.0, 0.04, years)
    path = scenarios.trajectory(baseline, 85.0, 6, "s_curve")
    table = fivecase.appraisal_summary_table([fivecase.OptionAppraisal("A phased mandate", result, ["trust in the tax system"], ["transition friction"], ["merchant resistance"], "within envelope")])

    report.write_csv(out / "cba_flows.csv", [{"year": i, "benefit": b, "cost": c} for i, (b, c) in enumerate(zip(benefits, costs))])
    report.write_csv(out / "tornado.csv", swings)
    report.write_csv(out / "incidence.csv", inc["rows"])
    report.bar_chart_svg(out / "tornado.svg", [r["param"] for r in swings], [r["swing"] for r in swings], title="What moves the net benefit most (illustrative)", unit="m", source="Horus illustrative model", highlight=0)
    report.line_chart_svg(out / "trajectory.svg", {"baseline": baseline, "with mandate": path}, title="Adoption trajectory (illustrative)", x_labels=[str(2026 + i) for i in range(years)], unit="%", source="Horus illustrative model", highlight="with mandate")
    summary = {"cba": result.as_dict(), "scm": burden.as_dict(), "mca": ranking.as_dict(), "montecarlo": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in sim.items()}, "tornado": swings, "switching_value_benefit_per_firm": switching, "incidence_verdict": inc["verdict"], "appraisal_summary_table": table}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    (out / "summary.md").write_text("# Illustrative appraisal\n\n" + report.markdown_table(table) + "\n\n## Tornado\n\n" + report.markdown_table(swings) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "demo":
        summary = demo(Path(argv[1]))
        print(json.dumps({k: summary[k] for k in ("cba", "mca")}, indent=2))
        return 0
    print("usage: python -m horus_appraisal demo <out dir>")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
