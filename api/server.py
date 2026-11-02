"""Read-only executive diligence API backed by verified synthetic financial evidence.

The endpoint never accepts arbitrary file paths, executes changes, or makes deal decisions.
All currency amounts in JSON are decimal strings, not binary floating-point estimates.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from fastapi import FastAPI, Query

from infra_due_diligence.evidence import build_evidence, verify_evidence
from infra_due_diligence.financial_model import build_financial_scenario

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CENT = Decimal("0.01")
HUNDRED = Decimal("100")
ONE = Decimal("1")

app = FastAPI(
    title="M&A Infrastructure Decision Room",
    description="Read-only local synthetic evidence and scenario modeling; not a live client system.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url=None,
)


def money(amount: Decimal) -> str:
    """Serialize financial data without silently losing precision."""
    return str(amount.quantize(CENT, rounding=ROUND_HALF_UP))


def grouped(rows: dict[str, Decimal], field: str) -> list[dict[str, str]]:
    return [{"name": name, field: money(amount)} for name, amount in rows.items()]


def model_cashflows(
    implementation_cost: Decimal,
    year_one_savings: Decimal,
    steady_state_savings: Decimal,
    capture: Decimal,
    overrun: Decimal,
    discount: Decimal,
) -> dict[str, object]:
    """Recalculate the existing five-year scenario without changing its evidence baseline."""
    investment = implementation_cost * (ONE + overrun)
    benefits = [year_one_savings * capture] + [steady_state_savings * capture] * 4
    npv = -investment
    cashflow_rows = [{"year": 0, "benefit": money(Decimal("0")), "discounted": money(-investment)}]
    for year, benefit in enumerate(benefits, start=1):
        discounted = benefit / ((ONE + discount) ** year)
        npv += discounted
        cashflow_rows.append({
            "year": year,
            "benefit": money(benefit),
            "discounted": money(discounted),
        })
    return {
        "implementation_cost": money(investment),
        "year_one_savings": money(benefits[0]),
        "steady_state_savings": money(steady_state_savings * capture),
        "five_year_npv": money(npv),
        "cashflows": cashflow_rows,
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "scope": "local synthetic evidence"}


@app.get("/api/overview")
def overview(
    capture_pct: int = Query(default=100, ge=0, le=100),
    discount_pct: int = Query(default=10, ge=0, le=30),
    implementation_overrun_pct: int = Query(default=0, ge=0, le=100),
) -> dict[str, object]:
    """Evidence and illustrative sensitivity controls, not an acquisition recommendation."""
    evidence = build_evidence(DATA_DIR)
    verify_evidence(evidence, DATA_DIR)  # Fail closed on changed or inconsistent source data.
    financial = build_financial_scenario(DATA_DIR)
    target = evidence["target"]
    optimization = evidence["optimization"]
    roadmap = evidence["roadmap"]

    capture = Decimal(capture_pct) / HUNDRED
    discount = Decimal(discount_pct) / HUNDRED
    overrun = Decimal(implementation_overrun_pct) / HUNDRED

    modeled = model_cashflows(
        financial["implementation_cost"],
        financial["year_one_savings"],
        financial["steady_state_savings"],
        capture,
        overrun,
        discount,
    )
    providers = []
    for name, annual_spend in target["spend_by_provider"].items():
        gross = target["waste_by_provider"].get(name, Decimal("0"))
        providers.append({
            "name": name,
            "annual_spend": money(annual_spend),
            "gross_waste": money(gross),
            "other_spend": money(annual_spend - gross),
        })

    return {
        "scope": "synthetic demonstration — not production or a valuation opinion",
        "evidence": {
            "annual_spend": money(target["annual_spend"]),
            "gross_waste": money(target["gross_waste"]),
            "waste_pct": str(target["waste_pct"].quantize(Decimal("0.1"))),
            "actionable_savings": money(optimization["actionable_savings"]),
            "quick_win_savings": money(optimization["quick_win_savings"]),
            "unbooked_gap": money(optimization["unbooked_gap"]),
            "provider_mix": providers,
            "waste_by_category": grouped(target["waste_by_category"], "amount"),
            "waste_by_environment": grouped(target["waste_by_environment"], "amount"),
            "savings_by_severity": grouped(optimization["savings_by_severity"], "amount"),
            "roadmap_initiatives": roadmap["executable_rows"],
        },
        "scenario": {
            "capture_pct": capture_pct,
            "discount_pct": discount_pct,
            "implementation_overrun_pct": implementation_overrun_pct,
            **modeled,
        },
        "decision_controls": [
            {
                "severity": "critical",
                "title": "Do not book gross waste as savings",
                "detail": "The gross-waste gap is excluded from the modeled executable backlog.",
            },
            {
                "severity": "warning",
                "title": "Financial results depend on execution",
                "detail": "Benefit capture, schedule, tax effects and overlap require deal-team diligence.",
            },
            {
                "severity": "information",
                "title": "No automatic valuation adjustment",
                "detail": "Purchase-price decisions and investment authorization remain with humans.",
            },
        ],
        "lineage": {
            "source": "Committed synthetic CSVs; recomputed and verified on every request",
            "classification": "Evidence totals and illustrative five-year discounted cash-flow scenario",
            "limitations": "No live billing accounts, production authorization, tax modeling or verified external benchmarks",
        },
    }
