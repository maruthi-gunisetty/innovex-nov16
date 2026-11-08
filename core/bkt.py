"""
LearnSphere AI: Bayesian Knowledge Tracing (BKT) Engine
Implements the standard Corbett and Anderson (1995) formulation of BKT
to estimate latent student concept mastery from sequential observations.
"""

from typing import Tuple, Dict, Any


class BayesianKnowledgeTracing:
    """
    Standard Bayesian Knowledge Tracing model for adaptive mastery estimation.

    Parameters:
        p_init (P(L0)): Prior probability of knowing the concept before practice.
        p_transit (P(T)): Probability of acquiring the concept on an opportunity.
        p_guess (P(G)): Probability of guessing correctly without mastery.
        p_slip (P(S)): Probability of slipping (making a mistake despite mastery).
    """

    def __init__(
        self,
        p_init: float = 0.20,
        p_transit: float = 0.15,
        p_guess: float = 0.20,
        p_slip: float = 0.10,
    ):
        self.p_init = min(max(float(p_init), 0.01), 0.99)
        self.p_transit = min(max(float(p_transit), 0.001), 0.50)
        self.p_guess = min(max(float(p_guess), 0.01), 0.40)
        self.p_slip = min(max(float(p_slip), 0.01), 0.30)

    def predict_correct(self, p_known: float) -> float:
        """
        Calculates the expected probability of a correct answer given current mastery:
        P(C) = P(L) * (1 - P(S)) + (1 - P(L)) * P(G)
        """
        p_l = min(max(float(p_known), 0.0), 1.0)
        p_c = p_l * (1.0 - self.p_slip) + (1.0 - p_l) * self.p_guess
        return float(p_c)

    def update(self, p_prior: float, is_correct: bool) -> Tuple[float, float]:
        """
        Updates concept mastery probability based on response correctness.

        Step 1: Compute posterior probability P(L_t | observation).
        Step 2: Account for learning transition to next opportunity P(L_{t+1}).

        Returns:
            Tuple of (posterior_given_obs, next_prior)
        """
        p_prior = min(max(float(p_prior), 0.001), 0.999)

        if is_correct:
            # P(L|C) = [P(L) * (1 - P(S))] / [P(L) * (1 - P(S)) + (1 - P(L)) * P(G)]
            numerator = p_prior * (1.0 - self.p_slip)
            denominator = numerator + (1.0 - p_prior) * self.p_guess
        else:
            # P(L|~C) = [P(L) * P(S)] / [P(L) * P(S) + (1 - P(L)) * (1 - P(G))]
            numerator = p_prior * self.p_slip
            denominator = numerator + (1.0 - p_prior) * (1.0 - self.p_guess)

        if denominator <= 0:
            p_posterior = p_prior
        else:
            p_posterior = numerator / denominator

        # Clamp posterior within valid bounds
        p_posterior = min(max(p_posterior, 0.001), 0.999)

        # Transition step: P(L_{t+1}) = P(L_t|obs) + (1 - P(L_t|obs)) * P(T)
        next_prior = p_posterior + (1.0 - p_posterior) * self.p_transit
        next_prior = min(max(next_prior, 0.001), 0.999)

        return float(p_posterior), float(next_prior)

    def classify_mastery(self, p_mastery: float) -> Dict[str, Any]:
        """
        Classifies probabilistic mastery into actionable educational tiers.
        """
        p = float(p_mastery)
        if p >= 0.85:
            return {
                "tier": "Mastered",
                "badge_class": "badge-success",
                "color": "#16a34a",
                "recommendation": "Ready for advanced synthesis and project challenges."
            }
        elif p >= 0.65:
            return {
                "tier": "Proficient",
                "badge_class": "badge-primary",
                "color": "#2563eb",
                "recommendation": "Consolidate understanding with mixed problem sets."
            }
        elif p >= 0.40:
            return {
                "tier": "Developing",
                "badge_class": "badge-warning",
                "color": "#d97706",
                "recommendation": "Requires targeted practice to eliminate active misconceptions."
            }
        else:
            return {
                "tier": "Novice",
                "badge_class": "badge-danger",
                "color": "#dc2626",
                "recommendation": "Fundamental prerequisite review recommended before continuing."
            }
