"""
SARVAVIDYA REWARDS ECOSYSTEM ENGINE
"Learn. Achieve. Earn. Redeem."
Implements the core backend for the gamified learning rewards system:
- Student Coin Wallet (available coins, lifetime earned, lifetime spent, level)
- Daily Learning Rewards & Atomic Earning Rules
- Daily Streak Calendar & Streak Freeze protection
- Student Daily Missions with idempotent claims
- Rewards Marketplace (Reward Store) with atomic purchases & inventory
- Strict Security: atomic transactions, server-side validation, idempotency keys, no negative balances
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple
from database.db import get_db_connection


# Configurable Level Thresholds (Lifetime Earned Coins)
LEVEL_THRESHOLDS = [
    ("Diamond Learner", 700),
    ("Gold Learner", 300),
    ("Silver Learner", 100),
    ("Bronze Learner", 0)
]

# Configurable Reward Values
REWARD_RULES = {
    "DAILY_GOAL": 15,
    "LESSON_COMPLETE": 10,
    "ASSIGNMENT_COMPLETE": 10,
    "QUIZ_CORRECT": 5,
    "ASSESSMENT_PRACTICE": 5,
    "ASSESSMENT_COMPLETE": 20,
    "PERFECT_SCORE_BONUS": 15,
    "STREAK_3_DAY": 10,
    "STREAK_7_DAY": 50,
    "WEEKLY_GOAL": 50,
    "COMPLETED_SUBJECT": 100,
    "WEAK_TOPIC_REVISION": 10,
    "BKT_MASTERY_MILESTONE": 25,
    "ASK_AI_WHY_ENGAGEMENT": 5,
    "TEACHER_RESOURCE_PUBLISH": 25,
    "TEACHER_MILESTONE": 50
}

DEFAULT_STORE_ITEMS = [
    ("avatar_quantum_owl", "Quantum Sage Owl", "avatar", "Exclusive cybernetic owl avatar symbolizing deep algorithmic insight.", 75, "🦉", 0),
    ("avatar_cyber_coder", "Matrix Architect", "avatar", "Neon-infused digital avatar for elite code builders.", 100, "⚡", 0),
    ("avatar_polymath", "Cosmic Polymath", "avatar", "Interdisciplinary scholar crest traversing math, physics, and computing.", 150, "🌌", 0),
    ("frame_gold_laurel", "Imperial Gold Frame", "frame", "Shimmering gold border framing your profile with academic honor.", 80, "👑", 0),
    ("frame_cyber_neon", "Cyber Neon Aura", "frame", "Pulsing violet and cyan glow highlighting your scholar card.", 95, "🔮", 0),
    ("theme_midnight_cyber", "Midnight Cyberpunk Theme", "theme", "Sleek obsidian-navy palette with neon violet highlights.", 120, "🌃", 0),
    ("theme_solar_gold", "Solar Renaissance Theme", "theme", "Warm amber and gold gradient dashboard aesthetics.", 120, "☀️", 0),
    ("theme_emerald_academic", "Emerald Scholar Theme", "theme", "Distinguished deep forest emerald and marble palette.", 120, "🌲", 0),
    ("token_streak_freeze", "Streak Freeze Shield", "powerup", "Protects your active study streak if you miss a study day. Consumable.", 40, "❄️", 1),
    ("badge_iron_will", "Iron Will Century Badge", "badge", "Awarded to relentless learners maintaining consistency.", 60, "🛡️", 0),
    ("badge_bkt_titan", "Latent Mastery Titan", "badge", "Commemorates achieving over 85% mastery across multiple subjects.", 100, "🏆", 0),
    ("bonus_ai_priority", "SARVA AI Ultra Reasoning Pack", "powerup", "Extended contextual multi-turn reasoning on complex mathematical derivations.", 70, "🧠", 0),
]

DEFAULT_DAILY_MISSIONS = [
    ("mission_daily_assessment", "Adaptive Assessment Drill", "Complete at least one adaptive assessment quiz.", 10, 1, "assessment"),
    ("mission_practice_5", "Knowledge Builder", "Practice at least 5 syllabus questions today.", 10, 5, "practice_questions"),
    ("mission_revise_weak", "Targeted Remediator", "Revise an identified cognitive misconception or weak concept.", 10, 1, "revise_weak_topic"),
    ("mission_perfect_score", "Accuracy Maestro", "Answer a question or drill with 100% precision on first try.", 15, 1, "score_improvement"),
    ("mission_ask_ai_why", "Deep Inquiry", "Consult SARVA AI Diagnostic Coach to inspect why an answer works.", 5, 1, "ai_activity"),
]

_REWARDS_SEEDED = False


def _invalidate_session_wallet():
    """Clears in-memory wallet cache on balance changes."""
    try:
        import streamlit as st
        st.session_state.pop("_cached_user_wallet", None)
    except Exception:
        pass


def init_rewards_tables() -> None:
    """Ensures tables are created and seeds default store items and missions."""
    global _REWARDS_SEEDED
    if _REWARDS_SEEDED:
        return
    try:
        from core.avatarverse_data import seed_avatarverse_items
        seed_avatarverse_items()
    except Exception:
        pass

    with get_db_connection() as conn:
        with conn:
            cur = conn.cursor()
            # Ensure system_config table for admin-configurable reward rules
            cur.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Seed store items if empty
            cur.execute("SELECT COUNT(*) FROM reward_store_items")
            if cur.fetchone()[0] == 0:
                for item in DEFAULT_STORE_ITEMS:
                    cur.execute(
                        """INSERT OR IGNORE INTO reward_store_items 
                           (id, name, category, description, coin_price, icon, is_consumable, is_active)
                           VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                        item
                    )

            # Seed daily missions if empty
            cur.execute("SELECT COUNT(*) FROM daily_missions")
            if cur.fetchone()[0] == 0:
                for m in DEFAULT_DAILY_MISSIONS:
                    cur.execute(
                        """INSERT OR IGNORE INTO daily_missions 
                           (mission_code, title, description, reward_coins, target_count, mission_type, is_active)
                           VALUES (?, ?, ?, ?, ?, ?, 1)""",
                        m
                    )
    _REWARDS_SEEDED = True


class RewardsEngine:
    """Central engine for the SARVAVIDYA Rewards Ecosystem."""

    @staticmethod
    def calculate_level(lifetime_earned: int) -> Tuple[str, Optional[str], int, float]:
        """
        Returns (current_level, next_level, threshold_needed, progress_percentage).
        """
        if lifetime_earned >= 700:
            return "Diamond Learner", None, 700, 100.0
        elif lifetime_earned >= 300:
            pct = round(((lifetime_earned - 300) / (700 - 300)) * 100, 1)
            return "Gold Learner", "Diamond Learner", 700, pct
        elif lifetime_earned >= 100:
            pct = round(((lifetime_earned - 100) / (300 - 100)) * 100, 1)
            return "Silver Learner", "Gold Learner", 300, pct
        else:
            pct = round((lifetime_earned / 100) * 100, 1)
            return "Bronze Learner", "Silver Learner", 100, pct

    @classmethod
    def get_reward_rule_value(cls, rule_name: str) -> int:
        """Retrieves configured reward value from system_config or fallback dictionary."""
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT value FROM system_config WHERE key = ?", (f"rule_{rule_name}",))
                r = cur.fetchone()
                if r:
                    return int(r["value"])
        except Exception:
            pass
        return REWARD_RULES.get(rule_name, 25)

    @classmethod
    def set_reward_rule_value(cls, rule_name: str, new_val: int) -> bool:
        """Allows administrator to configure reward values (e.g. teacher milestones)."""
        if new_val < 0:
            return False
        try:
            with get_db_connection() as conn:
                with conn:
                    conn.execute("""
                        INSERT INTO system_config (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
                    """, (f"rule_{rule_name}", str(new_val)))
            REWARD_RULES[rule_name] = new_val
            return True
        except Exception:
            return False

    @classmethod
    def get_or_create_wallet(cls, user_id: int) -> Dict[str, Any]:
        """Fetches student wallet; creates one initialized to 0 coins if not present. Recalculates verified streak."""
        init_rewards_tables()
        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student_wallets WHERE user_id = ?", (user_id,))
                row = cur.fetchone()
                if not row:
                    cur.execute(
                        """INSERT INTO student_wallets 
                           (user_id, available_coins, lifetime_earned_coins, lifetime_spent_coins, current_level, current_streak, longest_streak, streak_freeze_tokens)
                           VALUES (?, 0, 0, 0, 'Bronze Learner', 0, 0, 0)""",
                        (user_id,)
                    )
                    cur.execute("SELECT * FROM student_wallets WHERE user_id = ?", (user_id,))
                    row = cur.fetchone()

                w = dict(row)
                level, next_lvl, thresh, pct = cls.calculate_level(w["lifetime_earned_coins"])
                if w["current_level"] != level:
                    cur.execute("UPDATE student_wallets SET current_level = ? WHERE user_id = ?", (level, user_id))
                    w["current_level"] = level

                w["next_level_name"] = next_lvl
                w["next_level_threshold"] = thresh
                w["level_progress_pct"] = pct

                # Synchronize genuine learning streak from verified database records
                try:
                    from database.db import get_user_learning_dates, calculate_learning_streak
                    act_dates = get_user_learning_dates(user_id)
                    streak_cnt, streak_lbl = calculate_learning_streak(act_dates)
                    if w["current_streak"] != streak_cnt:
                        longest = max(w.get("longest_streak", 0) or 0, streak_cnt)
                        cur.execute("UPDATE student_wallets SET current_streak = ?, longest_streak = ? WHERE user_id = ?", (streak_cnt, longest, user_id))
                        w["current_streak"] = streak_cnt
                        w["longest_streak"] = longest
                    w["streak_label"] = streak_lbl
                except Exception:
                    w["streak_label"] = f"{w.get('current_streak', 0)} Day Streak"

                return w

    @classmethod
    def award_coins(
        cls,
        user_id: int,
        amount: int,
        source_activity: str,
        entity_id: str,
        description: str,
        idempotency_key: Optional[str] = None
    ) -> Tuple[bool, str, int]:
        """
        Atomically awards virtual coins to student wallet with strict idempotency verification.
        Returns: (success, message, new_balance).
        """
        if amount <= 0:
            w = cls.get_or_create_wallet(user_id)
            return False, "Amount must be strictly positive", w["available_coins"]

        idem_key = idempotency_key or f"earn_{user_id}_{source_activity}_{entity_id}"

        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                # 1. Idempotency Check
                cur.execute("SELECT id, balance_after FROM coin_transactions WHERE idempotency_key = ?", (idem_key,))
                existing = cur.fetchone()
                if existing:
                    return False, "Reward already awarded for this activity", existing["balance_after"]

                # 2. Fetch or create wallet
                cur.execute("SELECT available_coins, lifetime_earned_coins FROM student_wallets WHERE user_id = ?", (user_id,))
                row = cur.fetchone()
                if not row:
                    cur.execute(
                        """INSERT INTO student_wallets 
                           (user_id, available_coins, lifetime_earned_coins, lifetime_spent_coins, current_level, current_streak, longest_streak, streak_freeze_tokens)
                           VALUES (?, 0, 0, 0, 'Bronze Learner', 0, 0, 0)""",
                        (user_id,)
                    )
                    curr_bal = 0
                    curr_life = 0
                else:
                    curr_bal = row["available_coins"]
                    curr_life = row["lifetime_earned_coins"]

                new_bal = curr_bal + amount
                new_life = curr_life + amount
                new_level, _, _, _ = cls.calculate_level(new_life)

                # 3. Update wallet
                cur.execute(
                    """UPDATE student_wallets 
                       SET available_coins = ?, lifetime_earned_coins = ?, current_level = ?, updated_at = CURRENT_TIMESTAMP
                       WHERE user_id = ?""",
                    (new_bal, new_life, new_level, user_id)
                )

                # 4. Insert transaction ledger entry
                cur.execute(
                    """INSERT INTO coin_transactions 
                       (user_id, transaction_type, amount, balance_after, source_activity, entity_id, description, idempotency_key)
                       VALUES (?, 'EARN', ?, ?, ?, ?, ?, ?)""",
                    (user_id, amount, new_bal, source_activity, entity_id, description, idem_key)
                )

                _invalidate_session_wallet()
                return True, "Coins awarded successfully", new_bal

    @classmethod
    def record_daily_learning_activity(cls, user_id: int, activity_type: str = "learning_action") -> Dict[str, Any]:
        """
        Updates student's daily streak calendar with server-side validation and streak freeze support.
        Awards automatic milestone bonuses at 3 days (10 coins) and 7 days (30 coins).
        """
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student_wallets WHERE user_id = ?", (user_id,))
                row = cur.fetchone()
                if not row:
                    cls.get_or_create_wallet(user_id)
                    cur.execute("SELECT * FROM student_wallets WHERE user_id = ?", (user_id,))
                    row = cur.fetchone()

                w = dict(row)
                last_active = w["last_active_date"]
                curr_streak = w["current_streak"]
                longest_streak = w["longest_streak"]
                freezes = w["streak_freeze_tokens"]

                streak_status = "already_counted_today"
                milestone_award = None

                if last_active == today:
                    # Already logged today
                    pass
                elif last_active == yesterday:
                    # Consecutive day!
                    curr_streak += 1
                    longest_streak = max(longest_streak, curr_streak)
                    cur.execute(
                        """UPDATE student_wallets 
                           SET current_streak = ?, longest_streak = ?, last_active_date = ?, updated_at = CURRENT_TIMESTAMP
                           WHERE user_id = ?""",
                        (curr_streak, longest_streak, today, user_id)
                    )
                    streak_status = "extended"

                    # Check 3-day and 7-day milestones
                    if curr_streak == 3:
                        milestone_award = (REWARD_RULES["STREAK_3_DAY"], "STREAK_3_DAY", f"streak_3_{today}", "3-Day Learning Streak Bonus! 🔥", f"streak_bonus_{user_id}_3_{today}")
                    elif curr_streak == 7:
                        milestone_award = (REWARD_RULES["STREAK_7_DAY"], "STREAK_7_DAY", f"streak_7_{today}", "7-Day Mastery Streak Milestone! 🏆", f"streak_bonus_{user_id}_7_{today}")
                else:
                    # Missed at least one day
                    if last_active and freezes > 0:
                        # Streak Freeze activated!
                        freezes -= 1
                        curr_streak += 1
                        longest_streak = max(longest_streak, curr_streak)
                        cur.execute(
                            """UPDATE student_wallets 
                               SET current_streak = ?, longest_streak = ?, streak_freeze_tokens = ?, last_active_date = ?, updated_at = CURRENT_TIMESTAMP
                               WHERE user_id = ?""",
                            (curr_streak, longest_streak, freezes, today, user_id)
                        )
                        # Record transaction for freeze used
                        cur.execute(
                            """INSERT INTO coin_transactions 
                               (user_id, transaction_type, amount, balance_after, source_activity, entity_id, description, idempotency_key)
                               VALUES (?, 'FREEZE_USED', 0, ?, 'STREAK_FREEZE', ?, 'Streak Freeze Shield consumed to protect study streak ❄️', ?)""",
                            (user_id, w["available_coins"], today, f"freeze_used_{user_id}_{today}")
                        )
                        streak_status = "freeze_protected"
                    else:
                        # Reset streak to 1
                        curr_streak = 1
                        longest_streak = max(longest_streak, curr_streak)
                        cur.execute(
                            """UPDATE student_wallets 
                               SET current_streak = ?, longest_streak = ?, last_active_date = ?, updated_at = CURRENT_TIMESTAMP
                               WHERE user_id = ?""",
                            (curr_streak, longest_streak, today, user_id)
                        )
                        streak_status = "reset_new_start"

        # Award milestone bonuses outside the lock
        if milestone_award:
            amt, src, eid, desc, ikey = milestone_award
            cls.award_coins(
                user_id=user_id,
                amount=amt,
                source_activity=src,
                entity_id=eid,
                description=desc,
                idempotency_key=ikey
            )

        return {
            "current_streak": curr_streak,
            "longest_streak": longest_streak,
            "last_active_date": today,
            "streak_freeze_tokens": freezes,
            "streak_status": streak_status
        }

    @classmethod
    def update_mission_progress(cls, user_id: int, mission_type: str, increment: int = 1) -> List[Dict[str, Any]]:
        """
        Dynamically tracks progress on daily missions connected to assessments, BKT, and assignments.
        """
        init_rewards_tables()
        today = date.today().isoformat()
        updated_missions = []

        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                # Find missions matching type
                cur.execute("SELECT * FROM daily_missions WHERE mission_type = ? AND is_active = 1", (mission_type,))
                missions = cur.fetchall()

                for m in missions:
                    m_id = m["id"]
                    target = m["target_count"]

                    cur.execute(
                        "SELECT * FROM student_mission_progress WHERE user_id = ? AND mission_id = ? AND date = ?",
                        (user_id, m_id, today)
                    )
                    prog = cur.fetchone()

                    if not prog:
                        new_count = increment
                        is_comp = 1 if new_count >= target else 0
                        cur.execute(
                            """INSERT INTO student_mission_progress 
                               (user_id, mission_id, date, current_count, is_completed, is_claimed)
                               VALUES (?, ?, ?, ?, ?, 0)""",
                            (user_id, m_id, today, new_count, is_comp)
                        )
                    else:
                        if prog["is_completed"]:
                            continue
                        new_count = prog["current_count"] + increment
                        is_comp = 1 if new_count >= target else 0
                        cur.execute(
                            """UPDATE student_mission_progress 
                               SET current_count = ?, is_completed = ?
                               WHERE id = ?""",
                            (new_count, is_comp, prog["id"])
                        )

                    updated_missions.append({
                        "mission_id": m_id,
                        "title": m["title"],
                        "current_count": new_count,
                        "target_count": target,
                        "is_completed": bool(is_comp)
                    })

        return updated_missions

    @classmethod
    def claim_mission_reward(cls, user_id: int, mission_id: int) -> Tuple[bool, str]:
        """
        Idempotently claims reward for a completed daily mission.
        """
        today = date.today().isoformat()
        row_data = None
        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    """SELECT p.*, m.title, m.reward_coins 
                       FROM student_mission_progress p
                       JOIN daily_missions m ON p.mission_id = m.id
                       WHERE p.user_id = ? AND p.mission_id = ? AND p.date = ?""",
                    (user_id, mission_id, today)
                )
                row = cur.fetchone()
                if not row:
                    return False, "Mission not found or not attempted today."
                if not row["is_completed"]:
                    return False, "Mission goal has not been reached yet."
                if row["is_claimed"]:
                    return False, "Reward for this mission has already been claimed today."

                row_data = dict(row)
                # Mark claimed
                cur.execute(
                    "UPDATE student_mission_progress SET is_claimed = 1, claimed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (row["id"],)
                )

        # Award coins outside the lock
        cls.award_coins(
            user_id=user_id,
            amount=row_data["reward_coins"],
            source_activity="DAILY_MISSION",
            entity_id=f"mission_{mission_id}_{today}",
            description=f"Completed Daily Mission: {row_data['title']}",
            idempotency_key=f"claim_mission_{user_id}_{mission_id}_{today}"
        )

        return True, f"Claimed {row_data['reward_coins']} coins successfully!"

    @classmethod
    def redeem_store_item(cls, user_id: int, item_id: str) -> Tuple[bool, str]:
        """
        Executes atomic purchase in Reward Store:
        1. Verifies balance.
        2. Deducts coins atomically.
        3. Adds item to inventory (or increments consumable quantity).
        4. Logs transaction.
        5. Never allows negative balances or duplicate cosmetic purchases.
        """
        init_rewards_tables()
        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                # 1. Fetch Item
                cur.execute("SELECT * FROM reward_store_items WHERE id = ? AND is_active = 1", (item_id,))
                item = cur.fetchone()
                if not item:
                    return False, "Reward item does not exist or is inactive."

                price = item["coin_price"]
                is_consumable = bool(item["is_consumable"])

                # 2. Check Duplicate for non-consumables first
                if not is_consumable:
                    cur.execute("SELECT id FROM student_inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id))
                    if cur.fetchone():
                        return False, "You already own this reward item."

                # 3. Check Wallet balance
                cur.execute("SELECT available_coins, lifetime_spent_coins, streak_freeze_tokens FROM student_wallets WHERE user_id = ?", (user_id,))
                w = cur.fetchone()
                if not w or w["available_coins"] < price:
                    return False, f"Insufficient coins. You have {w['available_coins'] if w else 0} coins, but this item costs {price} coins."

                # 4. Atomic Deduct Coins
                new_bal = w["available_coins"] - price
                new_spent = w["lifetime_spent_coins"] + price
                new_freezes = w["streak_freeze_tokens"] + 1 if item_id == "token_streak_freeze" else w["streak_freeze_tokens"]

                cur.execute(
                    """UPDATE student_wallets 
                       SET available_coins = ?, lifetime_spent_coins = ?, streak_freeze_tokens = ?, updated_at = CURRENT_TIMESTAMP
                       WHERE user_id = ?""",
                    (new_bal, new_spent, new_freezes, user_id)
                )

                # 5. Add to Inventory
                if is_consumable:
                    cur.execute("SELECT id, quantity FROM student_inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id))
                    inv_row = cur.fetchone()
                    if inv_row:
                        cur.execute("UPDATE student_inventory SET quantity = quantity + 1 WHERE id = ?", (inv_row["id"],))
                    else:
                        cur.execute(
                            "INSERT INTO student_inventory (user_id, item_id, quantity, is_equipped) VALUES (?, ?, 1, 0)",
                            (user_id, item_id)
                        )
                else:
                    cur.execute(
                        "INSERT INTO student_inventory (user_id, item_id, quantity, is_equipped) VALUES (?, ?, 1, 0)",
                        (user_id, item_id)
                    )

                # 6. Record Transaction
                idem = f"spend_{user_id}_{item_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                cur.execute(
                    """INSERT INTO coin_transactions 
                       (user_id, transaction_type, amount, balance_after, source_activity, entity_id, description, idempotency_key)
                       VALUES (?, 'SPEND', ?, ?, 'STORE_PURCHASE', ?, ?, ?)""",
                    (user_id, price, new_bal, item_id, f"Redeemed {item['name']} from Reward Store", idem)
                )

                _invalidate_session_wallet()
                return True, f"Successfully redeemed '{item['name']}'! Your new coin balance is {new_bal}."

    @classmethod
    def equip_item(cls, user_id: int, item_id: str) -> Tuple[bool, str]:
        """Sets is_equipped = 1 for item and 0 for other items in same category."""
        with get_db_connection() as conn:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    """SELECT i.id, s.category, s.name 
                       FROM student_inventory i
                       JOIN reward_store_items s ON i.item_id = s.id
                       WHERE i.user_id = ? AND i.item_id = ?""",
                    (user_id, item_id)
                )
                item = cur.fetchone()
                if not item:
                    return False, "Item not found in your inventory."

                cat = item["category"]
                # Unequip others in category
                cur.execute(
                    """UPDATE student_inventory 
                       SET is_equipped = 0
                       WHERE user_id = ? AND item_id IN (SELECT id FROM reward_store_items WHERE category = ?)""",
                    (user_id, cat)
                )
                # Equip target
                cur.execute("UPDATE student_inventory SET is_equipped = 1 WHERE user_id = ? AND item_id = ?", (user_id, item_id))
                return True, f"Equipped {item['name']}!"

    @classmethod
    def get_rewards_dashboard_data(cls, user_id: int) -> Dict[str, Any]:
        """Assembles complete dataset for the Rewards UI page."""
        init_rewards_tables()
        wallet = cls.get_or_create_wallet(user_id)
        today = date.today().isoformat()

        with get_db_connection() as conn:
            cur = conn.cursor()

            # 1. Transactions (recent 15)
            cur.execute(
                """SELECT * FROM coin_transactions 
                   WHERE user_id = ? 
                   ORDER BY created_at DESC LIMIT 15""",
                (user_id,)
            )
            transactions = [dict(r) for r in cur.fetchall()]

            # 2. Daily Missions with Progress
            cur.execute(
                """SELECT m.id, m.mission_code, m.title, m.description, m.reward_coins, m.target_count, m.mission_type,
                          COALESCE(p.current_count, 0) as current_count,
                          COALESCE(p.is_completed, 0) as is_completed,
                          COALESCE(p.is_claimed, 0) as is_claimed
                   FROM daily_missions m
                   LEFT JOIN student_mission_progress p 
                          ON m.id = p.mission_id AND p.user_id = ? AND p.date = ?
                   WHERE m.is_active = 1
                   ORDER BY m.id ASC""",
                (user_id, today)
            )
            missions = [dict(r) for r in cur.fetchall()]

            # 3. Store Items with Owned Status
            cur.execute(
                """SELECT s.*, 
                          CASE WHEN i.id IS NOT NULL THEN 1 ELSE 0 END as is_owned,
                          COALESCE(i.is_equipped, 0) as is_equipped,
                          COALESCE(i.quantity, 0) as owned_quantity
                   FROM reward_store_items s
                   LEFT JOIN student_inventory i ON s.id = i.item_id AND i.user_id = ?
                   WHERE s.is_active = 1
                   ORDER BY s.category ASC, s.coin_price ASC""",
                (user_id,)
            )
            store_items = [dict(r) for r in cur.fetchall()]

            # 4. Inventory
            cur.execute(
                """SELECT i.*, s.name, s.category, s.description, s.icon, s.coin_price 
                   FROM student_inventory i
                   JOIN reward_store_items s ON i.item_id = s.id
                   WHERE i.user_id = ?
                   ORDER BY i.purchased_at DESC""",
                (user_id,)
            )
            inventory = [dict(r) for r in cur.fetchall()]

            # 5. Weekly Streak Days (Last 7 days)
            streak_days = []
            for i in range(6, -1, -1):
                d = (date.today() - timedelta(days=i)).isoformat()
                d_obj = date.today() - timedelta(days=i)
                # Check if there was activity on this date
                cur.execute(
                    """SELECT COUNT(*) FROM assessment_attempts 
                       WHERE user_id = ? AND date(attempted_at) = ?""",
                    (user_id, d)
                )
                has_activity = cur.fetchone()[0] > 0
                streak_days.append({
                    "date": d,
                    "day_name": d_obj.strftime("%a"),
                    "day_num": d_obj.strftime("%d"),
                    "is_today": (d == today),
                    "is_active": has_activity
                })

            return {
                "wallet": wallet,
                "transactions": transactions,
                "missions": missions,
                "store_items": store_items,
                "inventory": inventory,
                "streak_days": streak_days
            }
