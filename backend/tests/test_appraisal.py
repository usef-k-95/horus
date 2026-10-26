import math

from horus_appraisal import cba, distribution, fivecase, mca, montecarlo, report, scenarios, scm


def test_discount_factors_green_book_declines_after_year_30():
    f = cba.discount_factors(40, "green_book")
    assert f[0] == 1.0 and math.isclose(f[1], 1 / 1.035)
    # year 31 is discounted at 3.0%, so the step between 30 and 31 is smaller than the 3.5% step
    assert (f[30] / f[31]) < (f[29] / f[30])


def test_cba_known_values():
    r = cba.cba([0, 110], [100, 0], schedule=0.10)
    assert math.isclose(r.pv_benefits, 100.0) and math.isclose(r.pv_costs, 100.0) and math.isclose(r.npv, 0.0, abs_tol=1e-9)
    assert math.isclose(r.bcr, 1.0) and r.payback_year == 1
    assert math.isclose(cba.equivalent_annual(100.0, 0.0, 4), 25.0)


def test_scm():
    res = scm.standard_cost_model([scm.Obligation("report", population=100, frequency_per_year=2, hours_per_action=1.0, tariff_per_hour=10.0, overhead_rate=0.0), scm.Obligation("register", population=100, frequency_per_year=1, hours_per_action=1.0, tariff_per_hour=10.0, overhead_rate=0.0, one_off=True)])
    assert res.recurring_per_year == 2000.0 and res.one_off == 1000.0
    assert res.present_value(2, schedule=0.0) == 5000.0


def test_mca_ranking_and_robustness():
    criteria = [mca.Criterion("benefit", 0.5), mca.Criterion("cost", 0.5, higher_is_better=False)]
    raw = {"A": {"benefit": 10, "cost": 1}, "B": {"benefit": 1, "cost": 10}}
    res = mca.mca(raw, criteria, robustness_runs=200)
    assert res.ranking == ["A", "B"] and res.robustness["A"] == 1.0


def test_montecarlo_and_tornado():
    params = [montecarlo.Param("x", 1.0, 0.5, 1.5, "uniform"), montecarlo.Param("y", 2.0)]
    sim = montecarlo.simulate(lambda p: p["x"] * p["y"], params, runs=2000, seed=1)
    assert 1.0 < sim["p5"] < sim["p50"] < sim["p95"] < 3.0 and sim["probability_positive"] == 1.0
    rows = montecarlo.tornado(lambda p: p["x"] * p["y"], params)
    assert rows[0]["param"] == "x" and math.isclose(rows[0]["swing"], 2.0)
    sv = montecarlo.switching_value(lambda p: p["x"] * p["y"] - 1.5, params, "x", 0.0, 3.0)
    assert math.isclose(sv, 0.75, abs_tol=1e-4)


def test_distribution_verdict():
    inc = distribution.incidence([distribution.Group("poor", 100, 0.2, cost_per_unit=5), distribution.Group("rich", 100, 0.8, cost_per_unit=5)])
    assert inc["verdict"].startswith("regressive")


def test_scenarios_and_fivecase_and_report(tmp_path):
    base = scenarios.project(100, 0.1, 3)
    assert [round(v) for v in base] == [100, 110, 121]
    traj = scenarios.trajectory([0] * 5, 100, 4)
    assert traj[0] == 0 and traj[4] == 100 and 0 < traj[2] < 100
    assert fivecase.apply_optimism_bias(100, 0.24) == 124.0
    table = fivecase.appraisal_summary_table([fivecase.OptionAppraisal("A", cba.cba([0, 10], [5, 0], 0.0))])
    assert table[0]["npsv"] == 5.0 and table[0]["rank_by_npsv"] == 1
    p = report.bar_chart_svg(tmp_path / "c.svg", ["a", "b"], [3.0, 1.0], title="t", source="s", highlight=0)
    assert p.exists() and "<svg" in p.read_text()
    assert "| option |" in report.markdown_table(table)
