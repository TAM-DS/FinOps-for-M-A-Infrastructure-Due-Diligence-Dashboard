"""CLI report for the synthetic infrastructure due-diligence case."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path

from .evidence import build_evidence, verify_evidence
from .financial_model import build_financial_scenario

CENT = Decimal("0.01")
ONE_DECIMAL = Decimal("0.1")


def money(value: Decimal) -> str:
    return f"{value.quantize(CENT):,.2f}"


def pct(value: Decimal) -> str:
    return f"{value.quantize(ONE_DECIMAL)}"


def serializable(value: object) -> object:
    if isinstance(value, Decimal):
        return str(value.quantize(CENT))
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serializable(item) for item in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    evidence = build_evidence(args.data_dir)
    scenario = build_financial_scenario(args.data_dir)

    if args.verify:
        verify_evidence(evidence, args.data_dir)
        assert scenario["year_one_savings"].quantize(CENT) == Decimal("5676190.00")
        assert scenario["five_year_npv"].quantize(CENT) == Decimal("26588114.27")

    payload = {"evidence": evidence, "financial_scenario": scenario}

    if args.json:
        print(json.dumps(serializable(payload), indent=2, sort_keys=True))
        return

    target = evidence["target"]
    optimization = evidence["optimization"]

    assert isinstance(target, dict)
    assert isinstance(optimization, dict)

    print("Infrastructure Due Diligence Intelligence — synthetic case")
    print(f"Annual cloud run rate:       $ {money(target['annual_spend'])}")
    print(f"Gross waste exposure:       $ {money(target['gross_waste'])}")
    print(f"Waste / annual spend:         {pct(target['waste_pct'])}%")
    print(f"Actionable savings backlog: $ {money(optimization['actionable_savings'])}")
    print(f"Quick-win opportunity:      $ {money(optimization['quick_win_savings'])}")
    print(f"Unbooked waste gap:         $ {money(optimization['unbooked_gap'])}")
    print(f"Implementation cost:        $ {money(scenario['implementation_cost'])}")
    print(f"Staged Year-1 savings:      $ {money(scenario['year_one_savings'])}")
    print(f"5-year NPV @ 10%:           $ {money(scenario['five_year_npv'])}")
    if args.verify:
        print("Verification: PASS")


if __name__ == "__main__":
    main()
