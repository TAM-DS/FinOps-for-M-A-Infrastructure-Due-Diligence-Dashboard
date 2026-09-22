"""Financial scenario modeling for the executable remediation roadmap."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from .evidence import executable_roadmap_rows, read_rows, sum_field, to_decimal

ZERO = Decimal("0")
TWELVE = Decimal("12")


def staged_year_one_savings(data_dir: Path) -> Decimal:
    roadmap = executable_roadmap_rows(
        read_rows(data_dir / "post_acquisition_roadmap.csv")
    )

    total = ZERO
    for row in roadmap:
        annual_savings = to_decimal(row["Annual_Savings"])
        start_month = to_decimal(row["Start_Month"])
        duration = to_decimal(row["Duration_Months"])

        completion_offset = (start_month - Decimal("1")) + duration
        active_months = max(ZERO, TWELVE - completion_offset)
        total += annual_savings * active_months / TWELVE

    return total


def five_year_npv(
    data_dir: Path,
    discount_rate: Decimal = Decimal("0.10"),
) -> Decimal:
    roadmap = executable_roadmap_rows(
        read_rows(data_dir / "post_acquisition_roadmap.csv")
    )
    implementation_cost = sum_field(roadmap, "Implementation_Cost")
    steady_state_savings = sum_field(roadmap, "Annual_Savings")
    year_one = staged_year_one_savings(data_dir)

    cashflows = [year_one] + [steady_state_savings] * 4
    npv = -implementation_cost

    for year, savings in enumerate(cashflows, start=1):
        npv += savings / ((Decimal("1") + discount_rate) ** year)

    return npv


def build_financial_scenario(
    data_dir: Path,
    discount_rate: Decimal = Decimal("0.10"),
) -> dict[str, Decimal]:
    roadmap = executable_roadmap_rows(
        read_rows(data_dir / "post_acquisition_roadmap.csv")
    )
    return {
        "implementation_cost": sum_field(roadmap, "Implementation_Cost"),
        "steady_state_savings": sum_field(roadmap, "Annual_Savings"),
        "year_one_savings": staged_year_one_savings(data_dir),
        "discount_rate": discount_rate,
        "five_year_npv": five_year_npv(data_dir, discount_rate),
    }
