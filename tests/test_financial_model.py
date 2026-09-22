from decimal import Decimal
from pathlib import Path
import unittest

from infra_due_diligence.financial_model import (
    build_financial_scenario,
    five_year_npv,
    staged_year_one_savings,
)


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class FinancialModelTest(unittest.TestCase):
    def test_staged_year_one_savings(self) -> None:
        self.assertEqual(
            staged_year_one_savings(DATA_DIR).quantize(Decimal("0.01")),
            Decimal("5676190.00"),
        )

    def test_five_year_npv(self) -> None:
        self.assertEqual(
            five_year_npv(DATA_DIR).quantize(Decimal("0.01")),
            Decimal("26588114.27"),
        )

    def test_scenario_uses_executable_roadmap_only(self) -> None:
        scenario = build_financial_scenario(DATA_DIR)
        self.assertEqual(
            scenario["implementation_cost"],
            Decimal("1066000"),
        )
        self.assertEqual(
            scenario["steady_state_savings"],
            Decimal("7805800"),
        )


if __name__ == "__main__":
    unittest.main()
