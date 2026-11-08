"""
Unit Tests for Bayesian Knowledge Tracing (BKT) Engine
Verifies mathematical correctness of Corbett & Anderson formulation.
"""

import unittest
from core.bkt import BayesianKnowledgeTracing


class TestBayesianKnowledgeTracing(unittest.TestCase):

    def setUp(self):
        self.bkt = BayesianKnowledgeTracing(
            p_init=0.20,
            p_transit=0.15,
            p_guess=0.20,
            p_slip=0.10
        )

    def test_predict_correct(self):
        # When p_known = 0, P(C) should equal p_guess
        p_c_zero = self.bkt.predict_correct(0.0)
        self.assertAlmostEqual(p_c_zero, 0.20, places=4)

        # When p_known = 1, P(C) should equal 1 - p_slip
        p_c_one = self.bkt.predict_correct(1.0)
        self.assertAlmostEqual(p_c_one, 0.90, places=4)

    def test_update_correct_increases_mastery(self):
        prior = 0.30
        posterior_obs, next_prior = self.bkt.update(prior, is_correct=True)
        # Posterior after correct response must be strictly greater than prior
        self.assertGreater(posterior_obs, prior)
        self.assertGreater(next_prior, posterior_obs)

    def test_update_incorrect_decreases_mastery(self):
        prior = 0.60
        posterior_obs, next_prior = self.bkt.update(prior, is_correct=False)
        # Posterior given slip must be lower than prior
        self.assertLess(posterior_obs, prior)

    def test_mathematical_exactness(self):
        # Test exact manual calculation
        # p_prior = 0.20, p_slip = 0.10, p_guess = 0.20, p_transit = 0.15
        # numerator = 0.20 * 0.90 = 0.18
        # denominator = 0.18 + 0.80 * 0.20 = 0.18 + 0.16 = 0.34
        # expected_posterior = 0.18 / 0.34 = 0.52941176
        # next_prior = 0.52941176 + (1 - 0.52941176) * 0.15 = 0.52941176 + 0.07058823 = 0.600000
        p_post, n_prior = self.bkt.update(0.20, is_correct=True)
        self.assertAlmostEqual(p_post, 0.18 / 0.34, places=4)
        self.assertAlmostEqual(n_prior, (0.18 / 0.34) + (1.0 - (0.18 / 0.34)) * 0.15, places=4)

    def test_classify_mastery(self):
        novice = self.bkt.classify_mastery(0.25)
        self.assertEqual(novice["tier"], "Novice")

        dev = self.bkt.classify_mastery(0.50)
        self.assertEqual(dev["tier"], "Developing")

        prof = self.bkt.classify_mastery(0.70)
        self.assertEqual(prof["tier"], "Proficient")

        mast = self.bkt.classify_mastery(0.90)
        self.assertEqual(mast["tier"], "Mastered")


if __name__ == "__main__":
    unittest.main()

