"""
Unit Tests for Recommender Engine and Prerequisite Graph
Verifies prerequisite validation, adaptive difficulty, and personalized recommendations.
"""

import unittest
from core.recommender import RecommenderEngine


class TestRecommenderEngine(unittest.TestCase):

    def test_adaptive_difficulty(self):
        self.assertEqual(RecommenderEngine.get_adaptive_difficulty(0.20), "beginner")
        self.assertEqual(RecommenderEngine.get_adaptive_difficulty(0.40), "beginner")
        self.assertEqual(RecommenderEngine.get_adaptive_difficulty(0.60), "intermediate")
        self.assertEqual(RecommenderEngine.get_adaptive_difficulty(0.80), "advanced")

    def test_evaluate_prerequisites_satisfied(self):
        # COND requires VAR. If VAR >= 0.60, COND should be eligible.
        mastery_map = {"VAR": 0.85, "COND": 0.30}
        eval_result = RecommenderEngine.evaluate_prerequisites("COND", mastery_map)
        self.assertTrue(eval_result["eligible"])
        self.assertEqual(len(eval_result["unmet_prerequisites"]), 0)

    def test_evaluate_prerequisites_unmet(self):
        # REC requires FUNC and COND. If FUNC is 0.30, REC should be blocked.
        mastery_map = {"VAR": 0.90, "COND": 0.80, "LOOP": 0.75, "FUNC": 0.35, "REC": 0.10}
        eval_result = RecommenderEngine.evaluate_prerequisites("REC", mastery_map)
        self.assertFalse(eval_result["eligible"])
        self.assertEqual(len(eval_result["unmet_prerequisites"]), 1)
        self.assertEqual(eval_result["unmet_prerequisites"][0]["concept_code"], "FUNC")

    def test_generate_recommendations(self):
        mastery_data = [
            {"concept_code": "VAR", "concept_id": 1, "concept_name": "Variables", "mastery_prob": 0.40},
            {"concept_code": "COND", "concept_id": 2, "concept_name": "Conditionals", "mastery_prob": 0.20},
            {"concept_code": "LOOP", "concept_id": 3, "concept_name": "Loops", "mastery_prob": 0.20},
            {"concept_code": "LIST", "concept_id": 4, "concept_name": "Lists", "mastery_prob": 0.20},
            {"concept_code": "FUNC", "concept_id": 5, "concept_name": "Functions", "mastery_prob": 0.20},
            {"concept_code": "REC", "concept_id": 6, "concept_name": "Recursion", "mastery_prob": 0.20}
        ]
        recent_attempts = []
        lesson_progress = {}

        recs = RecommenderEngine.generate_recommendations(1, mastery_data, recent_attempts, lesson_progress)
        self.assertGreater(len(recs), 0)
        # Top recommendation should target either prerequisite gap or initial practice
        self.assertIn(recs[0]["type"], ["prerequisite_gap", "practice_drill", "next_advancement"])


if __name__ == "__main__":
    unittest.main()

