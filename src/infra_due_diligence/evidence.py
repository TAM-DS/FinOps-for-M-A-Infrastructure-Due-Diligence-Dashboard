"""Deterministic evidence extraction for the synthetic diligence case."""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Iterable

ZERO = Decimal("0")
CENT = Decimal("0.01")
PERCENT = Decimal("100")

SUMMARY_INITIATIVES = {
    "Quick Wins Package",
    "Reserved Instance Strategy",
    "Right-Sizing Program",
    "Implement Auto-Scaling",
    "Storage Optimization",
    "Multi-Cloud Consolidation",
    "Network Architecture Redesign",
    "Cost Governance Implementation",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def to_decimal(value: str) -> Decimal:
    return Decimal(value or "0")


def sum_field(rows: Iterable[dict[str, str]], field: str) -> Decimal:
    return sum((to_decimal(row[field]) for row in rows), ZERO)


def group_sum(
    rows: Iterable[dict[str, str]], key: str, value: str
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: ZERO)
    for row in rows:
        totals[row[key]] += to_decimal(row[value])
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def executable_roadmap_rows(
    roadmap_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        row
        for row in roadmap_rows
        if row["Initiative"] not in SUMMARY_INITIATIVES
    ]


def build_evidence(data_dir: Path) -> dict[str, object]:
    target = read_rows(data_dir / "target_cloud_costs.csv")
    optimization = read_rows(data_dir / "optimization_analysis.csv")
    roadmap = read_rows(data_dir / "post_acquisition_roadmap.csv")
    benchmarks = read_rows(data_dir / "industry_benchmarks.csv")

    annual_spend = sum_field(target, "Annual_Cost")
    gross_waste = sum_field(target, "Waste_Amount")
    waste_pct = gross_waste / annual_spend * PERCENT
    residual_run_rate = annual_spend - gross_waste

    actionable_savings = sum_field(optimization, "Savings_Potential")
    quick_win_rows = [row for row in optimization if row["Quick_Win"] == "Yes"]
    quick_win_savings = sum_field(quick_win_rows, "Savings_Potential")
    unbooked_gap = gross_waste - actionable_savings

    executable = executable_roadmap_rows(roadmap)
    roadmap_savings = sum_field(executable, "Annual_Savings")
    implementation_cost = sum_field(executable, "Implementation_Cost")

    return {
        "target": {
            "rows": len(target),
            "annual_spend": annual_spend,
            "gross_waste": gross_waste,
            "waste_pct": waste_pct,
            "residual_run_rate": residual_run_rate,
            "spend_by_provider": group_sum(target, "Cloud_Provider", "Annual_Cost"),
            "waste_by_provider": group_sum(target, "Cloud_Provider", "Waste_Amount"),
            "spend_by_environment": group_sum(target, "Environment", "Annual_Cost"),
            "waste_by_environment": group_sum(target, "Environment", "Waste_Amount"),
            "waste_by_category": group_sum(target, "Category", "Waste_Amount"),
        },
        "optimization": {
            "rows": len(optimization),
            "actionable_savings": actionable_savings,
            "quick_win_savings": quick_win_savings,
            "quick_win_count": len(quick_win_rows),
            "unbooked_gap": unbooked_gap,
            "savings_by_severity": group_sum(
                optimization, "Severity", "Savings_Potential"
            ),
            "savings_by_issue": group_sum(
                optimization, "Issue_Category", "Savings_Potential"
            ),
        },
        "roadmap": {
            "rows": len(roadmap),
            "executable_rows": len(executable),
            "annual_savings": roadmap_savings,
            "implementation_cost": implementation_cost,
        },
        "benchmarks": {
            "rows": len(benchmarks),
            "classification": "synthetic scenario input",
        },
    }


def verify_evidence(evidence: dict[str, object], data_dir: Path) -> None:
    target_rows = read_rows(data_dir / "target_cloud_costs.csv")
    for row in target_rows:
        monthly = to_decimal(row["Monthly_Cost"])
        annual = to_decimal(row["Annual_Cost"])
        waste = to_decimal(row["Waste_Amount"])
        assert annual == monthly * Decimal("12")
        assert ZERO <= waste <= annual

    target = evidence["target"]
    optimization = evidence["optimization"]
    roadmap = evidence["roadmap"]

    assert isinstance(target, dict)
    assert isinstance(optimization, dict)
    assert isinstance(roadmap, dict)

    assert target["rows"] == 38
    assert target["annual_spend"] == Decimal("17040000")
    assert target["gross_waste"] == Decimal("8835600")
    assert target["residual_run_rate"] == Decimal("8204400")

    assert optimization["rows"] == 15
    assert optimization["actionable_savings"] == Decimal("7805800")
    assert optimization["quick_win_savings"] == Decimal("3609600")
    assert optimization["unbooked_gap"] == Decimal("1029800")

    assert roadmap["rows"] == 31
    assert roadmap["executable_rows"] == 23
    assert roadmap["annual_savings"] == optimization["actionable_savings"]
    assert roadmap["implementation_cost"] == Decimal("1066000")
