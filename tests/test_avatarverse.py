import unittest
import os
import sys
import uuid

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.avatarverse_data import (
    AVATAR_CATALOG,
    AVATAR_BY_ID,
    seed_avatarverse_items,
    get_user_avatar_state,
)
from database.db import (
    init_db,
    get_db_connection,
    create_user,
    get_user_by_id,
    get_user_equipped_avatar,
    get_cohort_student_summaries,
)
from core.rewards_engine import (
    init_rewards_tables,
    RewardsEngine,
)

class TestAvatarverseEcosystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        init_rewards_tables()
        seed_avatarverse_items()

        # Create dedicated test student and teacher
        cls.student_user_id = create_user(
            username=f"test_student_{uuid.uuid4().hex[:8]}",
            email=f"student_{uuid.uuid4().hex[:8]}@test.edu",
            password_hash="hash",
            salt="salt",
            full_name="Avatar Test Student",
            role="student"
        )
        cls.teacher_user_id = create_user(
            username=f"test_teacher_{uuid.uuid4().hex[:8]}",
            email=f"teacher_{uuid.uuid4().hex[:8]}@test.edu",
            password_hash="hash",
            salt="salt",
            full_name="Avatar Test Teacher",
            role="teacher"
        )

    def test_catalog_exact_ten_avatars(self):
        """Verify exactly 10 avatars exist in the catalog."""
        self.assertEqual(len(AVATAR_CATALOG), 10)
        self.assertEqual(len(AVATAR_BY_ID), 10)

    def test_catalog_levels_and_rarity(self):
        """Verify Levels 1-5 are Epic and 6-10 are Legendary with correct pricing."""
        epic_prices = [800, 850, 900, 950, 1000]
        legendary_prices = [1500, 1600, 1700, 1800, 2000]

        for i in range(1, 6):
            avatar = AVATAR_CATALOG[i - 1]
            self.assertEqual(avatar["level"], i)
            self.assertEqual(avatar["tier"], "Epic")
            self.assertEqual(avatar["coin_price"], epic_prices[i - 1])

        for i in range(6, 11):
            avatar = AVATAR_CATALOG[i - 1]
            self.assertEqual(avatar["level"], i)
            self.assertEqual(avatar["tier"], "Legendary")
            self.assertEqual(avatar["coin_price"], legendary_prices[i - 6])

    def test_avatar_svg_assets_exist(self):
        """Verify all 10 avatar SVG files exist on disk with content."""
        for avatar in AVATAR_CATALOG:
            path = os.path.join(os.path.dirname(__file__), "..", avatar["asset_rel"])
            self.assertTrue(os.path.exists(path), f"File missing: {path}")
            self.assertGreater(os.path.getsize(path), 500, f"File too small: {path}")

    def test_db_seeded_items(self):
        """Verify avatars are seeded in the database reward_store_items table."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, coin_price, category FROM reward_store_items WHERE category = 'avatar'")
            rows = cursor.fetchall()
            row_dict = {r[0]: (r[1], r[2]) for r in rows}

        for avatar in AVATAR_CATALOG:
            self.assertIn(avatar["id"], row_dict)
            name, price = row_dict[avatar["id"]]
            self.assertEqual(name, avatar["name"])
            self.assertEqual(price, avatar["coin_price"])

    def test_purchase_and_equip_flow(self):
        """Verify atomic coin deduction, duplicate prevention, and equipping."""
        user_id = self.student_user_id
        # 1. Initialize wallet
        wallet = RewardsEngine.get_or_create_wallet(user_id)
        start_balance = wallet.get("available_coins", 0)

        # 2. Try purchasing without enough coins (Mystic Scholar costs 800)
        # Note: new student gets 50 welcome coins, so 50 < 800
        success, msg = RewardsEngine.redeem_store_item(user_id, "avatar_1_mystic_scholar")
        self.assertFalse(success)
        self.assertIn("Insufficient coins", msg)

        # 3. Award coins to user
        award_ok, award_msg, new_bal = RewardsEngine.award_coins(
            user_id=user_id,
            amount=1000,
            source_activity="LESSON_COMPLETE",
            entity_id="test_lesson_1",
            description="Test award for avatar purchase",
            idempotency_key=f"test_award_{user_id}_1"
        )
        self.assertTrue(award_ok)

        # 4. Purchase avatar_1_mystic_scholar (costs 800)
        buy_ok, buy_msg = RewardsEngine.redeem_store_item(user_id, "avatar_1_mystic_scholar")
        self.assertTrue(buy_ok)

        # Check balance: was start_balance + 1000 - 800
        wallet_after = RewardsEngine.get_or_create_wallet(user_id)
        self.assertEqual(wallet_after["available_coins"], start_balance + 1000 - 800)

        # 5. Prevent duplicate purchase of already owned avatar
        dup_ok, dup_msg = RewardsEngine.redeem_store_item(user_id, "avatar_1_mystic_scholar")
        self.assertFalse(dup_ok)
        self.assertIn("already own", dup_msg.lower())

        # 6. Verify avatar is in inventory
        state = get_user_avatar_state(user_id)
        owned_ids = [av["id"] for av in state["avatars"] if av["is_owned"]]
        self.assertIn("avatar_1_mystic_scholar", owned_ids)

        # 7. Equip avatar
        equip_ok, equip_msg = RewardsEngine.equip_item(user_id, "avatar_1_mystic_scholar")
        self.assertTrue(equip_ok)

        # 8. Verify get_user_equipped_avatar returns the equipped avatar
        equipped = get_user_equipped_avatar(user_id)
        self.assertIsNotNone(equipped)
        self.assertEqual(equipped["id"], "avatar_1_mystic_scholar")
        self.assertEqual(equipped["name"], "Mystic Scholar")
        self.assertEqual(equipped["level"], 1)

    def test_teacher_wallet_and_access(self):
        """Verify teachers can have wallets and purchase/equip avatars."""
        teacher_id = self.teacher_user_id
        wallet = RewardsEngine.get_or_create_wallet(teacher_id)
        self.assertIsNotNone(wallet)

        # Award teacher milestone coins
        RewardsEngine.award_coins(
            user_id=teacher_id,
            amount=2500,
            source_activity="TEACHER_MILESTONE",
            entity_id="test_faculty_milestone",
            description="Resource publication reward",
            idempotency_key=f"test_teacher_award_{teacher_id}"
        )

        # Purchase Legendary avatar_10_legendary_ace (2000 coins)
        res_buy, buy_msg = RewardsEngine.redeem_store_item(teacher_id, "avatar_10_legendary_ace")
        self.assertTrue(res_buy, buy_msg)

        # Equip
        RewardsEngine.equip_item(teacher_id, "avatar_10_legendary_ace")
        equipped = get_user_equipped_avatar(teacher_id)
        self.assertIsNotNone(equipped)
        self.assertEqual(equipped["id"], "avatar_10_legendary_ace")
        self.assertEqual(equipped["tier"], "Legendary")

    def test_cohort_query_performance(self):
        """Verify batch cohort summary function returns expected structure."""
        summaries = get_cohort_student_summaries("python")
        self.assertIsInstance(summaries, list)
        if len(summaries) > 0:
            student_summary = summaries[0]
            self.assertIn("id", student_summary)
            self.assertIn("avg_mastery", student_summary)
            self.assertIn("accuracy", student_summary)


if __name__ == "__main__":
    unittest.main()
