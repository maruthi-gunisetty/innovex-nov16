"""
Unit Tests for Scikit-Learn Predictive Learning Risk Engine
Verifies feature extraction, model fitting, and risk inference.
"""

import unittest
from core.ml_predictor import PredictiveLearningEngine


class TestPredictiveLearningEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PredictiveLearningEngine()

    def test_train_model(self):
        metrics = self.engine.train()
        self.assertTrue(self.engine.is_trained)
        self.assertGreater(metrics["sample_count"], 5)
        self.assertGreater(metrics["training_accuracy"], 0.60)
        self.assertIn("prior_mastery", metrics["coefficients"])

    def test_predict_success_probability(self):
        # A student with high mastery on beginner item should have high success probability
        res_high = self.engine.predict_success_probability(
            prior_mastery=0.95,
            difficulty="beginner",
            response_time_sec=12.0,
            concept_order=1,
            historical_accuracy=0.90
        )
        self.assertGreaterEqual(res_high["success_probability"], 0.60)
        self.assertEqual(res_high["risk_tier"], "Low Risk")

        # A student with low mastery on advanced item should have elevated risk
        res_low = self.engine.predict_success_probability(
            prior_mastery=0.10,
            difficulty="advanced",
            response_time_sec=45.0,
            concept_order=6,
            historical_accuracy=0.15
        )
        self.assertLessEqual(res_low["success_probability"], 0.50)
        self.assertIn(res_low["risk_tier"], ["High Risk", "Moderate Risk"])


if __name__ == "__main__":
    unittest.main()
