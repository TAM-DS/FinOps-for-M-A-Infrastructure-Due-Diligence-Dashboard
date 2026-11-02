"""Contract tests for the read-only executive API and scenario boundaries."""

from decimal import Decimal
import unittest

from fastapi.testclient import TestClient
from api.server import app

CLIENT = TestClient(app)


class DealRoomApiTest(unittest.TestCase):
    def test_baseline_matches_verified_original_model(self):
        response = CLIENT.get("/api/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["evidence"]["annual_spend"], "17040000.00")
        self.assertEqual(data["evidence"]["gross_waste"], "8835600.00")
        self.assertEqual(data["evidence"]["actionable_savings"], "7805800.00")
        self.assertEqual(data["evidence"]["unbooked_gap"], "1029800.00")
        self.assertEqual(data["scenario"]["implementation_cost"], "1066000.00")
        self.assertEqual(data["scenario"]["year_one_savings"], "5676190.00")
        self.assertEqual(data["scenario"]["five_year_npv"], "26588114.27")

    def test_sensitivity_never_changes_source_evidence(self):
        baseline = CLIENT.get("/api/overview").json()
        sensitivity = CLIENT.get(
            "/api/overview",
            params={"capture_pct": 50, "discount_pct": 15, "implementation_overrun_pct": 20},
        ).json()
        self.assertEqual(baseline["evidence"], sensitivity["evidence"])
        self.assertNotEqual(
            baseline["scenario"]["five_year_npv"],
            sensitivity["scenario"]["five_year_npv"],
        )
        self.assertEqual(sensitivity["scenario"]["implementation_cost"], "1279200.00")

    def test_zero_capture_yields_negative_initial_investment(self):
        response = CLIENT.get("/api/overview", params={"capture_pct": 0})
        self.assertEqual(response.status_code, 200)
        scenario = response.json()["scenario"]
        self.assertEqual(scenario["five_year_npv"], "-1066000.00")
        self.assertEqual(scenario["year_one_savings"], "0.00")

    def test_reject_out_of_bound_assumptions(self):
        for params in [
            {"capture_pct": -1},
            {"capture_pct": 101},
            {"discount_pct": 31},
            {"implementation_overrun_pct": 101},
        ]:
            with self.subTest(params=params):
                self.assertEqual(CLIENT.get("/api/overview", params=params).status_code, 422)

    def test_provider_totals_and_exposure_reconcile(self):
        evidence = CLIENT.get("/api/overview").json()["evidence"]
        providers = evidence["provider_mix"]
        annual = sum((Decimal(p["annual_spend"]) for p in providers), Decimal(0))
        waste = sum((Decimal(p["gross_waste"]) for p in providers), Decimal(0))
        for provider in providers:
            self.assertEqual(
                Decimal(provider["annual_spend"]),
                Decimal(provider["gross_waste"]) + Decimal(provider["other_spend"]),
            )
        self.assertEqual(annual, Decimal(evidence["annual_spend"]))
        self.assertEqual(waste, Decimal(evidence["gross_waste"]))


if __name__ == "__main__":
    unittest.main()
