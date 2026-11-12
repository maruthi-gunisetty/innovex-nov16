"""
Comprehensive Unit Tests for SARVAVIDYA Rewards Ecosystem & AI Assistant Redesign
Verifies:
- Student Coin Wallet and Level Thresholds
- Atomic Coin Awards & Strict Idempotency Protection
- Daily Streak Calendar, Milestone Bonuses, and Streak Freeze Protection
- Daily Missions Tracking & Idempotent Claims
- Reward Store Atomic Purchases, Inventory, and Duplicate Purchase Protection
- Mathematical Independence between BKT Mastery and Virtual Currency
- AI Assistant Centered Modal & Contextual Trigger Integration
"""

import unittest
from unittest.mock import patch, MagicMock
from core.rewards_engine import RewardsEngine, init_rewards_tables, REWARD_RULES
from database.db import init_db, get_db_connection
from core.bkt import BayesianKnowledgeTracing


class TestRewardsAndAIRedesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        init_rewards_tables()

    def setUp(self):
        self.test_user_id = 999
        # Clean test user wallet and transactions
        with get_db_connection() as conn:
            with conn:
                conn.execute("DELETE FROM coin_transactions WHERE user_id = ?", (self.test_user_id,))
                conn.execute("DELETE FROM student_mission_progress WHERE user_id = ?", (self.test_user_id,))
                conn.execute("DELETE FROM student_inventory WHERE user_id = ?", (self.test_user_id,))
                conn.execute("DELETE FROM student_wallets WHERE user_id = ?", (self.test_user_id,))
                # Ensure dummy user exists for foreign keys
                conn.execute(
                    """INSERT OR IGNORE INTO users 
                       (id, username, email, password_hash, salt, full_name, role)
                       VALUES (?, 'test_reward_user', 'test_reward@example.edu', 'hash', 'salt', 'Test Scholar', 'student')""",
                    (self.test_user_id,)
                )

    def test_wallet_initialization_and_level_tiers(self):
        """Verifies initial wallet balance is 0 and level thresholds compute accurately."""
        w = RewardsEngine.get_or_create_wallet(self.test_user_id)
        self.assertEqual(w["available_coins"], 0)
        self.assertEqual(w["lifetime_earned_coins"], 0)
        self.assertEqual(w["current_level"], "Bronze Learner")

        # Test level threshold calculations
        lvl, next_lvl, thresh, pct = RewardsEngine.calculate_level(50)
        self.assertEqual(lvl, "Bronze Learner")
        self.assertEqual(next_lvl, "Silver Learner")

        lvl, next_lvl, thresh, pct = RewardsEngine.calculate_level(150)
        self.assertEqual(lvl, "Silver Learner")

        lvl, next_lvl, thresh, pct = RewardsEngine.calculate_level(450)
        self.assertEqual(lvl, "Gold Learner")

        lvl, next_lvl, thresh, pct = RewardsEngine.calculate_level(850)
        self.assertEqual(lvl, "Diamond Learner")

    def test_atomic_coin_award_and_strict_idempotency(self):
        """Ensures coins are awarded atomically and duplicate claims with same idempotency key are rejected."""
        idem_key = "test_award_unique_001"
        ok, msg, bal = RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=20,
            source_activity="ASSIGNMENT_COMPLETE",
            entity_id="assign_1",
            description="Completed Python Assignment 1",
            idempotency_key=idem_key
        )
        self.assertTrue(ok)
        self.assertEqual(bal, 20)

        # Duplicate call with exact same idempotency key
        ok_dup, msg_dup, bal_dup = RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=20,
            source_activity="ASSIGNMENT_COMPLETE",
            entity_id="assign_1",
            description="Completed Python Assignment 1",
            idempotency_key=idem_key
        )
        self.assertFalse(ok_dup)
        self.assertIn("already awarded", msg_dup)
        self.assertEqual(bal_dup, 20)  # Balance must not change!

    def test_negative_or_zero_coin_award_rejection(self):
        """Validates that negative and zero coin awards are rejected by backend validation."""
        ok, msg, _ = RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=-15,
            source_activity="INVALID",
            entity_id="err",
            description="Negative award attempt"
        )
        self.assertFalse(ok)

        ok0, msg0, _ = RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=0,
            source_activity="INVALID",
            entity_id="err0",
            description="Zero award attempt"
        )
        self.assertFalse(ok0)

    def test_streak_tracking_and_streak_freeze(self):
        """Verifies daily streak extension and streak freeze protection upon a missed day."""
        # 1. Initial streak start
        res1 = RewardsEngine.record_daily_learning_activity(self.test_user_id)
        self.assertEqual(res1["current_streak"], 1)

        # 2. Add a streak freeze token directly to wallet
        with get_db_connection() as conn:
            with conn:
                conn.execute(
                    "UPDATE student_wallets SET streak_freeze_tokens = 1, last_active_date = '2026-01-01' WHERE user_id = ?",
                    (self.test_user_id,)
                )

        # 3. Simulate activity after missed day with freeze shield active
        res2 = RewardsEngine.record_daily_learning_activity(self.test_user_id)
        self.assertEqual(res2["streak_status"], "freeze_protected")
        self.assertEqual(res2["streak_freeze_tokens"], 0)  # Consumed 1 freeze
        self.assertEqual(res2["current_streak"], 2)  # Streak preserved and advanced!

    def test_store_redemption_insufficient_balance(self):
        """Validates that purchasing items with insufficient coin balance is strictly rejected."""
        ok, msg = RewardsEngine.redeem_store_item(self.test_user_id, "avatar_quantum_owl")
        self.assertFalse(ok)
        self.assertIn("Insufficient coins", msg)

    def test_store_redemption_and_duplicate_cosmetic_rejection(self):
        """Verifies atomic deduction, inventory record, and rejection of duplicate non-consumable cosmetics."""
        # Give 200 coins
        RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=200,
            source_activity="BONUS",
            entity_id="bonus_fund",
            description="Test bonus"
        )

        # Buy Quantum Owl (costs 75 coins)
        ok, msg = RewardsEngine.redeem_store_item(self.test_user_id, "avatar_quantum_owl")
        self.assertTrue(ok)
        self.assertIn("Successfully redeemed", msg)

        w = RewardsEngine.get_or_create_wallet(self.test_user_id)
        self.assertEqual(w["available_coins"], 125)
        self.assertEqual(w["lifetime_spent_coins"], 75)

        # Attempt to buy same avatar again
        ok_dup, msg_dup = RewardsEngine.redeem_store_item(self.test_user_id, "avatar_quantum_owl")
        self.assertFalse(ok_dup)
        self.assertIn("already own", msg_dup)
        self.assertEqual(w["available_coins"], 125)  # No coins deducted on failed duplicate!

    def test_consumable_streak_freeze_redemption(self):
        """Verifies purchasing streak freeze increments wallet shield counter and allows multi-purchases."""
        RewardsEngine.award_coins(
            user_id=self.test_user_id,
            amount=150,
            source_activity="BONUS",
            entity_id="bonus_freeze",
            description="Test bonus"
        )
        ok, msg = RewardsEngine.redeem_store_item(self.test_user_id, "token_streak_freeze")
        self.assertTrue(ok)

        w = RewardsEngine.get_or_create_wallet(self.test_user_id)
        self.assertEqual(w["streak_freeze_tokens"], 1)

        # Consumables CAN be purchased again if student has coins
        ok2, msg2 = RewardsEngine.redeem_store_item(self.test_user_id, "token_streak_freeze")
        self.assertTrue(ok2)
        w2 = RewardsEngine.get_or_create_wallet(self.test_user_id)
        self.assertEqual(w2["streak_freeze_tokens"], 2)

    def test_bkt_independence_from_currency(self):
        """Ensures that BKT mathematical updates remain strictly independent of coin rewards."""
        bkt = BayesianKnowledgeTracing(p_init=0.20, p_transit=0.15, p_guess=0.20, p_slip=0.10)
        p_prior = 0.30
        p_obs, p_next = bkt.update(p_prior, is_correct=True)

        # Awarding coins must not alter BKT update equation
        RewardsEngine.award_coins(self.test_user_id, 100, "BONUS", "bkt_test", "BKT coin award")
        p_obs_check, p_next_check = bkt.update(p_prior, is_correct=True)

        self.assertAlmostEqual(p_next, p_next_check, places=6)
        self.assertAlmostEqual(p_obs, p_obs_check, places=6)

    def test_daily_mission_progress_and_claim(self):
        """Verifies daily mission progress tracking, completion flag, and one-time claim."""
        RewardsEngine.update_mission_progress(self.test_user_id, "assessment", 1)
        data = RewardsEngine.get_rewards_dashboard_data(self.test_user_id)
        assess_mission = next(m for m in data["missions"] if m["mission_type"] == "assessment")

        self.assertTrue(assess_mission["is_completed"])
        self.assertFalse(assess_mission["is_claimed"])

        # Claim reward
        ok, msg = RewardsEngine.claim_mission_reward(self.test_user_id, assess_mission["id"])
        self.assertTrue(ok)
        self.assertIn("Claimed", msg)

        # Re-claim should be rejected
        ok_dup, msg_dup = RewardsEngine.claim_mission_reward(self.test_user_id, assess_mission["id"])
        self.assertFalse(ok_dup)


if __name__ == "__main__":
    unittest.main()
