"""horus_appraisal — quantitative toolkit for policy appraisal: discounting and CBA, Standard Cost
Model, multi-criteria analysis, Monte Carlo and switching values, distributional incidence,
scenarios and delivery trajectories, Five Case Model tables, and plain reports (CSV, Markdown, SVG).
Pure standard library so it runs anywhere the backend runs."""

from . import cba, distribution, fivecase, mca, montecarlo, report, scenarios, scm

__all__ = ["cba", "scm", "mca", "montecarlo", "distribution", "scenarios", "fivecase", "report"]
