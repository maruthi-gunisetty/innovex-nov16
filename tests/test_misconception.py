"""
Unit Tests for Misconception Detection Engine
Verifies taxonomy lookups, diagnostic reporting, and pattern summarization.
"""

import unittest
from core.misconception import MisconceptionEngine


class TestMisconceptionEngine(unittest.TestCase):

    def test_taxonomy_retrieval(self):
        info = MisconceptionEngine.get_info("OFF_BY_ONE_INDEX")
        self.assertIsNotNone(info)
        self.assertEqual(info["category"], "Data Structures")
        self.assertIn("Off-by-One", info["name"])

        # Invalid code returns None
        self.assertIsNone(MisconceptionEngine.get_info("NON_EXISTENT_CODE"))

    def test_diagnose_attempt(self):
        diag = MisconceptionEngine.diagnose_attempt(
            misconception_code="BASE_CASE_OMISSION",
            question_title="Countdown Recursion",
            concept_name="Recursion"
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["code"], "BASE_CASE_OMISSION")
        self.assertIn("base case", diag["remediation"])
        self.assertTrue(len(diag["remediation"]) > 10)

    def test_summarize_patterns(self):
        sample_attempts = [
            {"misconception_code": "OFF_BY_ONE_INDEX", "is_correct": 0},
            {"misconception_code": "OFF_BY_ONE_INDEX", "is_correct": 0},
            {"misconception_code": "OFF_BY_ONE_INDEX", "is_correct": 0},
            {"misconception_code": "BASE_CASE_OMISSION", "is_correct": 0},
            {"misconception_code": "NONE", "is_correct": 1}
        ]

        summary = MisconceptionEngine.summarize_patterns(sample_attempts)
        self.assertEqual(summary["total_misconceptions_detected"], 4)
        self.assertEqual(summary["unique_patterns_count"], 2)
        # OFF_BY_ONE_INDEX has count 3, so its severity should be High
        top_pattern = summary["patterns"][0]
        self.assertEqual(top_pattern["code"], "OFF_BY_ONE_INDEX")
        self.assertEqual(top_pattern["count"], 3)
        self.assertEqual(top_pattern["severity"], "High")


if __name__ == "__main__":
    unittest.main()
