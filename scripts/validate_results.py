"""Validate the exported analysis artifacts without third-party dependencies.

Run from the repository root after executing all notebook cells:

    python scripts/validate_results.py
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def read_csv(name: str) -> list[dict[str, str]]:
    path = RESULTS / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing exported file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    expected_files = {
        "summary_statistics.csv",
        "education_summary.csv",
        "topcode_sensitivity.csv",
        "data_quality.csv",
        "environment.txt",
    }
    actual_files = {path.name for path in RESULTS.iterdir() if path.is_file()}
    missing = expected_files - actual_files
    if missing:
        raise AssertionError(f"Missing result files: {sorted(missing)}")

    summary = read_csv("summary_statistics.csv")
    assert len(summary) == 5, "Expected five pooled periods"
    assert abs(float(summary[0]["p10"]) - 9167) < 1
    assert abs(float(summary[-1]["p10"]) - 6738) < 1
    assert round(float(summary[0]["gini"]), 3) == 0.326
    assert round(float(summary[-1]["gini"]), 3) == 0.378

    education = read_csv("education_summary.csv")
    assert len(education) == 5, "Expected five education-summary periods"
    assert round(float(education[0]["BA_premium"]), 2) == 1.34
    assert round(float(education[-1]["BA_premium"]), 2) == 1.82

    quality = read_csv("data_quality.csv")
    assert len(quality) == 31, "Expected one quality row per survey wave"
    assert all(int(row["topcoded_n"]) >= 20 for row in quality)
    assert all(float(row["min_income"]) > 0 for row in quality)

    sensitivity = read_csv("topcode_sensitivity.csv")
    assert len(sensitivity) == 20, "Expected five periods x four scenarios"
    scenarios = {row["scenario"] for row in sensitivity}
    assert scenarios == {
        "trimmed",
        "ceiling_as_recorded",
        "ceiling_x1_5",
        "ceiling_x2",
    }
    shares = [float(row["topcoded_share_pct"]) for row in sensitivity]
    assert all(5 <= share <= 15 for share in shares)
    for scenario in scenarios:
        first = next(row for row in sensitivity if row["period"] == "1972-79" and row["scenario"] == scenario)
        last = next(row for row in sensitivity if row["period"] == "2010s" and row["scenario"] == scenario)
        assert float(last["gini"]) > float(first["gini"]), f"Gini did not rise for {scenario}"

    environment = (RESULTS / "environment.txt").read_text(encoding="utf-8")
    assert "Python: 3.13" in environment
    assert "pandas: 3.0.3" in environment

    figure_names = {path.name for path in FIGURES.glob("*.png")}
    expected_figures = {
        "fig1_income_cdf_1970s_vs_2010s.png",
        "fig2_income_quantiles_by_decade.png",
        "fig3_inequality_by_decade.png",
        "fig4_median_by_education.png",
        "fig5_topcode_sensitivity.png",
    }
    assert expected_figures <= figure_names, "One or more figures are missing"

    print("Result validation passed")
    print(f"- {len(summary)} period summaries, {len(education)} education summaries")
    print(f"- {len(quality)} annual data-quality rows, {len(sensitivity)} scenario rows")
    print(f"- {len(expected_figures)} figures and environment.txt present")


if __name__ == "__main__":
    main()
