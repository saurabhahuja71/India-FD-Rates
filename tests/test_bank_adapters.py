import importlib
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).parent
GENERIC = (ROOT / "fixtures/generic_rate_page.html").read_bytes()
HDFC = (ROOT / "fixtures/hdfc_rate_page.html").read_bytes()
AXIS = b"<h2>Key Fixed Deposit Interest Rates</h2><table><tr><td>2 years</td><td>7.25%</td><td>6.00%</td><td>7.75%</td><td>6.50%</td></tr></table>"
ADAPTERS = ["idfc_first", "federal", "yes", "indusind", "indian", "equitas", "jana", "esaf", "suryoday", "utkarsh"]

class AdapterFixtures(unittest.TestCase):
    def test_registry_has_required_candidate_breadth(self):
        configs = yaml.safe_load((Path(__file__).parents[1] / "config/banks.yaml").read_text())["banks"]
        enabled = [x for x in configs if x.get("enabled", True)]
        for category, minimum in (("private_sector", 7), ("public_sector", 10), ("small_finance", 7)):
            self.assertGreaterEqual(sum(x["category"] == category for x in enabled), minimum)
    def test_hdfc_selects_retail_maximum(self):
        result = importlib.import_module("banks.hdfc").parse(HDFC)
        self.assertEqual(result["regular_rate"], 6.50)
        self.assertEqual(result["senior_rate"], 7.10)
        self.assertEqual(result["regular_tenure"], "3 Years 1 day to < 4 Years 7 Months")
        self.assertEqual(result["effective_date"], "2026-08-19")

    def test_each_generic_adapter_extracts_and_excludes_bulk(self):
        for name in ADAPTERS:
            with self.subTest(adapter=name):
                result = importlib.import_module(f"banks.{name}").parse(GENERIC)
                self.assertEqual(result["regular_rate"], 7.25)
                self.assertEqual(result["senior_rate"], 7.75)
                self.assertEqual(result["row_count"], 2)

    def test_axis_uses_general_and_senior_columns(self):
        result = importlib.import_module("banks.axis").parse(AXIS)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (7.25, 7.75))

    def test_sbi_uses_current_public_and_senior_columns(self):
        fixture = b'<h2>Retail Domestic term deposits</h2><table><tr><td>2 years</td><td>6.45</td><td>6.40</td><td>6.95</td><td>6.90</td></tr></table>'
        result = importlib.import_module("banks.sbi").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.45, 6.95))

    def test_pnb_selects_public_and_senior_columns(self):
        fixture = b'<h2>Revised Rates For Public</h2><table><tr><th>Sl. No</th><th>Period</th><th>Revised Rates For Public</th><th>Senior Citizens</th><th>Super Senior</th></tr><tr><td>1</td><td>444 Days</td><td>6.60</td><td>7.10</td><td>7.40</td></tr></table>'
        result = importlib.import_module("banks.pnb").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.60, 7.10))

    def test_canara_selects_callable_general_and_senior_columns(self):
        fixture = b'<h2>TERM DEPOSITS Rate of Interest Deposits less than Rs.3 Crore</h2><table><tr><th>Term</th><th>General Public</th><th>Yield</th><th>Senior Citizen</th><th>Yield</th></tr><tr><td>555 Days</td><td>6.60</td><td>6.77</td><td>7.10</td><td>7.29</td></tr></table>'
        result = importlib.import_module("banks.canara").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.60, 7.10))

    def test_bank_of_baroda_selects_domestic_retail_rows(self):
        fixture = b'<p>Domestic Term Deposits below 3.00 Crores (w.e.f 12-06-2026)</p><table><tr><td>bob Golden Goal deposit Scheme (555 Days)</td><td>6.75</td><td>7.25</td></tr></table>'
        result = importlib.import_module("banks.bank_of_baroda").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.75, 7.25))

    def test_union_applies_official_senior_benefit(self):
        fixture = b'<h2>Domestic/ NRO Term Deposit</h2><p>effective from 4th August 2026</p><table><tr><td>555 Days</td><td>6.55</td></tr></table>'
        result = importlib.import_module("banks.union").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.55, 7.05))

    def test_boi_separates_standard_and_green_deposit(self):
        fixture = b'<h2>BANK HAS REVISED RATE OF INTEREST ON DOMESTIC / NRO TERM DEPOSITS (CALLABLE)</h2><table><tr><th>Maturity</th><th>For deposits less than Rs.3 Cr</th></tr><tr><td>3 Years</td><td>6.70</td></tr><tr><td>Above 3 Years to less than 5 Years</td><td>6.25</td></tr></table>'
        result = importlib.import_module("banks.bank_of_india").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.70, 7.45))
        self.assertEqual(result["products"][1]["product_type"], "GREEN_DEPOSIT")

    def test_ujjivan_applies_published_senior_benefit(self):
        fixture = b'<h2>Platina Fixed Deposit</h2><table><tr><td>2 years</td><td>7.55%</td></tr></table>'
        result = importlib.import_module("banks.ujjivan").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (7.55, 8.05))

    def test_au_pairs_regular_and_senior_tables(self):
        fixture = b'<h2>Domestic, NRE Retail Fixed Deposit Interest Rates</h2><table><tr><td>2 years</td><td>7.25%</td></tr></table><h2>Senior Citizen Fixed Deposit Interest Rates</h2><table><tr><td>2 years</td><td>7.75%</td></tr></table>'
        result = importlib.import_module("banks.au_small_finance").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (7.25, 7.75))

    def test_icici_does_not_verify_headline_without_tenure(self):
        with self.assertRaises(ValueError):
            importlib.import_module("banks.icici").parse(b"general citizens up to 6.50%")

    def test_rbl_selects_callable_general_and_senior_columns(self):
        fixture = (Path(__file__).parent / "fixtures/rbl_rate_page.html").read_bytes()
        result = importlib.import_module("banks.rbl").parse(fixture)
        self.assertEqual(result["regular_rate"], 7.20)
        self.assertEqual(result["senior_rate"], 7.70)
        self.assertEqual(result["regular_tenure"], "18 months to 36 months")
        self.assertTrue(result["callable"])
        self.assertNotIn(result["regular_rate"], (8.15, 8.40))
        self.assertNotIn(result["senior_rate"], (8.15, 8.40))
        self.assertIn("General Citizen", result["regular_source_column"])
        self.assertIn("Senior Citizen", result["senior_source_column"])

    def test_iob_selects_revised_retail_not_non_callable_or_bulk(self):
        fixture = (Path(__file__).parent / "fixtures/iob_rate_page.html").read_bytes()
        result = importlib.import_module("banks.indian_overseas").parse(fixture)
        self.assertEqual((result["regular_rate"], result["senior_rate"]), (6.60, 7.10))
        self.assertTrue(result["callable"])
        self.assertNotIn("Non-Callable", result["regular_source_column"])
        self.assertNotIn("Bulk", result["source_table"])

if __name__ == "__main__": unittest.main()
