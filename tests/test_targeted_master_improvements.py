"""
Unit Tests for SARVAVIDYA Targeted Master Improvements:
- Task 1: Realistic dashboard numbers (Streak, Coins, Tier, Attempts, Accuracy, Daily Goal, Curriculum)
- Task 2: Assessment answer visualization & question validation (TypeError fix, safe skipping)
- Task 3: Admin Portal - Gemini API key management (Masking, Connection Test, Secure Save, Quota Handling)
- Task 4: AvatarVerse 10 Avatars (Epic/Legendary, Prices, Purchase, Equip, Profile Display)
- Task 5: Secure Coin System (Idempotency, Separate Wallets, Admin Configurable Teacher Rules)
"""

import unittest
import os
import json
from datetime import datetime, timedelta
from database.db import (
    get_user_learning_dates, calculate_learning_streak,
    get_user_assessment_stats, get_user_daily_goal_progress,
    get_course_curriculum_progress, get_db_connection, get_user_by_username
)
from core.rewards_engine import RewardsEngine, REWARD_RULES
from core.avatarverse_data import AVATAR_CATALOG, AVATAR_BY_ID, get_user_avatar_state
from core.ai_service import (
    mask_api_key, test_gemini_connection, save_gemini_api_key,
    get_gemini_api_key, get_ai_configuration_status
)
from views.assessment import validate_question


class TestRealisticDashboardNumbers(unittest.TestCase):
    """TASK 1: Realistic Dashboard Telemetry & Verified Calculations."""

    def test_streak_calculation_empty(self):
        streak, label = calculate_learning_streak([])
        self.assertEqual(streak, 0)
        self.assertEqual(label, "0 Day Streak")

    def test_streak_calculation_active_today_only(self):
        today = datetime.now().strftime("%Y-%m-%d")
        streak, label = calculate_learning_streak([today])
        self.assertEqual(streak, 1)
        self.assertEqual(label, "1 Day Streak")

    def test_streak_calculation_consecutive_3_days(self):
        today = datetime.now().date()
        d0 = today.strftime("%Y-%m-%d")
        d1 = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        d2 = (today - timedelta(days=2)).strftime("%Y-%m-%d")
        streak, label = calculate_learning_streak([d0, d1, d2])
        self.assertEqual(streak, 3)
        self.assertEqual(label, "3 Day Streak")

    def test_streak_calculation_inactive_breaks_streak(self):
        today = datetime.now().date()
        # Activity was 5 days ago and 6 days ago -> inactive today & yesterday
        d5 = (today - timedelta(days=5)).strftime("%Y-%m-%d")
        d6 = (today - timedelta(days=6)).strftime("%Y-%m-%d")
        streak, label = calculate_learning_streak([d5, d6])
        self.assertEqual(streak, 0)
        self.assertEqual(label, "0 Day Streak")

    def test_user_assessment_stats(self):
        # Alex Rivera (ID 1)
        stats = get_user_assessment_stats(1)
        self.assertIn("total_attempts", stats)
        self.assertIn("correct_attempts", stats)
        self.assertIn("accuracy", stats)
        self.assertIsInstance(stats["total_attempts"], int)
        self.assertGreaterEqual(stats["accuracy"], 0.0)
        self.assertLessEqual(stats["accuracy"], 100.0)

    def test_daily_goal_progress(self):
        prog = get_user_daily_goal_progress(1)
        self.assertIn("daily_goal", prog)
        self.assertIn("completed_today", prog)
        self.assertIn("progress_pct", prog)
        self.assertGreaterEqual(prog["daily_goal"], 1)

    def test_curriculum_progress(self):
        prog = get_course_curriculum_progress(1, 1)
        self.assertIn("total_lessons", prog)
        self.assertIn("completed_lessons", prog)
        self.assertIn("progress_pct", prog)
        self.assertGreaterEqual(prog["progress_pct"], 0)
        self.assertLessEqual(prog["progress_pct"], 100)


class TestAssessmentValidationAndBugs(unittest.TestCase):
    """TASK 2: Question Validation, TypeError Bug Fix & Safe Exception Handling."""

    def test_valid_question_passes(self):
        q = {
            "id": 101,
            "title": "Variable Assignment",
            "prompt": "What is x after x = 5?",
            "options": [
                {"index": 0, "text": "5", "is_correct": True},
                {"index": 1, "text": "None", "is_correct": False}
            ]
        }
        is_val, err = validate_question(q)
        self.assertTrue(is_val)
        self.assertIsNone(err)

    def test_malformed_question_fails_gracefully(self):
        # Missing title & prompt
        is_val, err = validate_question({"id": 102})
        self.assertFalse(is_val)
        self.assertIn("missing", err.lower())

        # No correct option designated
        q_no_corr = {
            "id": 103,
            "title": "Test",
            "prompt": "Prompt",
            "options": [
                {"index": 0, "text": "A", "is_correct": False},
                {"index": 1, "text": "B", "is_correct": False}
            ]
        }
        is_val, err = validate_question(q_no_corr)
        self.assertFalse(is_val)
        self.assertIn("no designated correct option", err.lower())

    def test_stack_trace_leak_rejected(self):
        q_leaked = {
            "id": 104,
            "title": "Buggy Option",
            "prompt": "Run code",
            "options": [
                {"index": 0, "text": "Traceback (most recent call last):\n  File 'x.py', line 1", "is_correct": True},
                {"index": 1, "text": "Valid option", "is_correct": False}
            ]
        }
        is_val, err = validate_question(q_leaked)
        self.assertFalse(is_val)
        self.assertIn("stack trace", err.lower())

    def test_immutability_question_fixed_in_db(self):
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT options_json FROM questions WHERE id = 2")
            row = cur.fetchone()
            if row:
                opts = json.loads(row["options_json"])
                for o in opts:
                    # Should NOT be raw unformatted error string
                    if o.get("is_correct"):
                        self.assertIn("Raises TypeError", o["text"])


class TestAdminGeminiKeyManagement(unittest.TestCase):
    """TASK 3: Admin Portal Gemini Key Management & Quota Handling."""

    def test_mask_api_key(self):
        self.assertEqual(mask_api_key(None), "Not Configured")
        self.assertEqual(mask_api_key(""), "Not Configured")
        self.assertEqual(mask_api_key("short"), "********")
        masked = mask_api_key("AIzaSyB_1234567890abcdefXYZ98765")
        self.assertTrue(masked.startswith("AIzaSy"))
        self.assertTrue(masked.endswith("8765"))
        self.assertIn("...", masked)

    def test_test_connection_empty_key(self):
        res = test_gemini_connection("")
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 400)
        self.assertTrue(res["is_invalid_key"])

    def test_save_and_retrieve_runtime_key(self):
        prev = get_gemini_api_key()
        test_key = "AIzaSyTestKey_UnitTestCase_9999"
        ok, msg = save_gemini_api_key(test_key)
        self.assertTrue(ok)
        self.assertEqual(get_gemini_api_key(), test_key)

        # Restore previous key
        if prev:
            save_gemini_api_key(prev)

    def test_admin_account_exists(self):
        admin = get_user_by_username("admin@123")
        self.assertIsNotNone(admin)
        self.assertEqual(admin["role"], "admin")


class TestAvatarVerseExact10(unittest.TestCase):
    """TASK 4: AvatarVerse Exactly 10 Avatars with correct tiers & prices."""

    def test_exactly_10_avatars(self):
        self.assertEqual(len(AVATAR_CATALOG), 10)

    def test_epic_and_legendary_distribution(self):
        epic = [a for a in AVATAR_CATALOG if a["tier"] == "Epic"]
        legendary = [a for a in AVATAR_CATALOG if a["tier"] == "Legendary"]
        self.assertEqual(len(epic), 5)
        self.assertEqual(len(legendary), 5)

    def test_avatar_prices_match_spec(self):
        expected_prices = {
            "avatar_1_mystic_scholar": 800,
            "avatar_2_celestial_dreamer": 850,
            "avatar_3_cyber_sage": 900,
            "avatar_4_tech_wizard": 950,
            "avatar_5_quantum_learner": 1000,
            "avatar_6_shadow_knight": 1500,
            "avatar_7_phoenix_aura": 1600,
            "avatar_8_star_guardian": 1700,
            "avatar_9_royal_enigma": 1800,
            "avatar_10_legendary_ace": 2000,
        }
        for av in AVATAR_CATALOG:
            self.assertEqual(av["coin_price"], expected_prices[av["id"]])

    def test_avatar_assets_exist(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for av in AVATAR_CATALOG:
            abs_path = os.path.join(project_root, av["asset_rel"])
            self.assertTrue(os.path.exists(abs_path), f"Missing SVG asset: {av['asset_rel']}")


class TestSecureCoinSystem(unittest.TestCase):
    """TASK 5: Secure Coin System, Idempotency & Separate Wallets."""

    def test_separate_wallets_for_users(self):
        w_student = RewardsEngine.get_or_create_wallet(1)
        w_teacher = RewardsEngine.get_or_create_wallet(4)
        self.assertNotEqual(w_student["user_id"], w_teacher["user_id"])

    def test_idempotent_coin_awards(self):
        uid = 1
        idem = f"unit_test_idem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        ok1, _, bal1 = RewardsEngine.award_coins(uid, 10, "TEST_ACTIVITY", "101", "Test Award", idem)
        self.assertTrue(ok1)

        # Duplicate award with same idempotency key must fail
        ok2, msg2, bal2 = RewardsEngine.award_coins(uid, 10, "TEST_ACTIVITY", "101", "Test Award Duplicate", idem)
        self.assertFalse(ok2)
        self.assertIn("already awarded", msg2.lower())
        self.assertEqual(bal1, bal2)

    def test_admin_configurable_teacher_rewards(self):
        initial_val = RewardsEngine.get_reward_rule_value("TEACHER_RESOURCE_PUBLISH")
        ok = RewardsEngine.set_reward_rule_value("TEACHER_RESOURCE_PUBLISH", 35)
        self.assertTrue(ok)
        self.assertEqual(RewardsEngine.get_reward_rule_value("TEACHER_RESOURCE_PUBLISH"), 35)

        # Restore
        RewardsEngine.set_reward_rule_value("TEACHER_RESOURCE_PUBLISH", initial_val)


if __name__ == "__main__":
    unittest.main()
