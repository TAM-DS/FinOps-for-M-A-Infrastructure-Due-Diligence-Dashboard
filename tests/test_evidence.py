from decimal import Decimal
from pathlib import Path
import unittest

from infra_due_diligence.evidence import build_evidence, verify_evidence


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class EvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = build_evidence(DATA_DIR)

    def test_full_evidence_contract(self) -> None:
        verify_evidence(self.evidence, DATA_DIR)

    def test_gross_waste_is_not_actionable_savings(self) -> None:
        target = self.evidence["target"]
        optimization = self.evidence["optimization"]

        self.assertEqual(target["gross_waste"], Decimal("8835600"))
        self.assertEqual(
            optimization["actionable_savings"],
            Decimal("7805800"),
        )
        self.assertEqual(
            optimization["unbooked_gap"],
            Decimal("1029800"),
        )

    def test_provider_waste_reconciles(self) -> None:
        target = self.evidence["target"]
        self.assertEqual(
            sum(target["waste_by_provider"].values(), Decimal("0")),
            target["gross_waste"],
        )

    def test_roadmap_reconciles_to_optimization_backlog(self) -> None:
        roadmap = self.evidence["roadmap"]
        optimization = self.evidence["optimization"]
        self.assertEqual(
            roadmap["annual_savings"],
            optimization["actionable_savings"],
        )


if __name__ == "__main__":
    unittest.main()
