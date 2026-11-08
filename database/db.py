"""
LearnSphere AI: Database Management and SQLite Operations
Handles thread-safe database connections, parameterized queries,
schema initialization, and state persistence.
"""

import sqlite3
import os
import json
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict, Any, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "learnsphere.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


@contextmanager
def get_db_connection():
    """Yields a SQLite connection with Row factory and foreign keys, safely closing on exit."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    try:
        yield conn
    finally:
        conn.close()


def init_db(force: bool = False) -> None:
    """Initializes tables from schema.sql."""
    if force and os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    with get_db_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


# ==========================================
# USER OPERATIONS
# ==========================================

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username.strip(),))
        row = cur.fetchone()
        return dict(row) if row else None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? COLLATE NOCASE", (email.strip(),))
        row = cur.fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def create_user(
    username: str,
    email: str,
    password_hash: str,
    salt: str,
    full_name: str,
    role: str = "student",
    is_demo: int = 0,
    target_difficulty: str = "adaptive",
    daily_goal: int = 5
) -> int:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, salt, full_name, role, is_demo, target_difficulty, daily_goal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (username.strip(), email.strip(), password_hash, salt, full_name.strip(), role, is_demo, target_difficulty, daily_goal)
        )
        user_id = cur.lastrowid
        conn.commit()

        # Initialize student mastery rows for all concepts if role is student
        if role == "student":
            init_student_mastery(user_id)

        return user_id


def update_user_preferences(user_id: int, target_difficulty: str, daily_goal: int) -> None:
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE users SET target_difficulty = ?, daily_goal = ? WHERE id = ?",
            (target_difficulty, daily_goal, user_id)
        )
        conn.commit()


def update_user_password(user_id: int, password_hash: str, salt: str) -> None:
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (password_hash, salt, user_id)
        )
        conn.commit()


def get_all_students() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE role = 'student' ORDER BY full_name ASC")
        return [dict(r) for r in cur.fetchall()]


# ==========================================
# CONCEPTS & LEARNING CONTENT
# ==========================================

def get_all_concepts() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM concepts ORDER BY order_index ASC")
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["prerequisites"] = json.loads(d["prerequisites"]) if d["prerequisites"] else []
            result.append(d)
        return result


def get_concept_by_id(concept_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM concepts WHERE id = ?", (concept_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["prerequisites"] = json.loads(d["prerequisites"]) if d["prerequisites"] else []
        return d


def get_all_learning_content() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT lc.*, c.name as concept_name, c.code as concept_code
            FROM learning_content lc
            JOIN concepts c ON lc.concept_id = c.id
            ORDER BY lc.order_index ASC
        """)
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["learning_objectives"] = json.loads(d["learning_objectives_json"])
            d["code_examples"] = json.loads(d["code_examples_json"])
            d["common_mistakes"] = json.loads(d["common_mistakes_json"])
            d["practice_exercises"] = json.loads(d["practice_exercises_json"])
            result.append(d)
        return result


def get_learning_content_by_concept(concept_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT lc.*, c.name as concept_name, c.code as concept_code
            FROM learning_content lc
            JOIN concepts c ON lc.concept_id = c.id
            WHERE lc.concept_id = ?
        """, (concept_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["learning_objectives"] = json.loads(d["learning_objectives_json"])
        d["code_examples"] = json.loads(d["code_examples_json"])
        d["common_mistakes"] = json.loads(d["common_mistakes_json"])
        d["practice_exercises"] = json.loads(d["practice_exercises_json"])
        return d


def get_user_lesson_progress(user_id: int) -> Dict[int, bool]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT content_id, is_completed FROM lesson_progress WHERE user_id = ?", (user_id,))
        return {r["content_id"]: bool(r["is_completed"]) for r in cur.fetchall()}


def toggle_lesson_progress(user_id: int, content_id: int, is_completed: bool) -> None:
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        conn.execute("""
            INSERT INTO lesson_progress (user_id, content_id, is_completed, completed_at, last_accessed)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, content_id) DO UPDATE SET
                is_completed = excluded.is_completed,
                completed_at = CASE WHEN excluded.is_completed = 1 THEN excluded.completed_at ELSE NULL END,
                last_accessed = excluded.last_accessed
        """, (user_id, content_id, 1 if is_completed else 0, now if is_completed else None, now))
        conn.commit()


# ==========================================
# QUESTIONS & ASSESSMENTS
# ==========================================

def get_questions_by_concept_and_difficulty(
    concept_id: Optional[int] = None,
    difficulty: Optional[str] = None
) -> List[Dict[str, Any]]:
    query = """
        SELECT q.*, c.name as concept_name, c.code as concept_code
        FROM questions q
        JOIN concepts c ON q.concept_id = c.id
        WHERE 1=1
    """
    params = []
    if concept_id:
        query += " AND q.concept_id = ?"
        params.append(concept_id)
    if difficulty and difficulty != "all":
        query += " AND q.difficulty = ?"
        params.append(difficulty)

    query += " ORDER BY q.id ASC"

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["options"] = json.loads(d["options_json"])
            result.append(d)
        return result


def get_question_by_id(question_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT q.*, c.name as concept_name, c.code as concept_code
            FROM questions q
            JOIN concepts c ON q.concept_id = c.id
            WHERE q.id = ?
        """, (question_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["options"] = json.loads(d["options_json"])
        return d


# ==========================================
# BKT MASTERY & ATTEMPTS
# ==========================================

def init_student_mastery(user_id: int) -> None:
    """Initializes mastery records for a student across all active concepts."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, p_init FROM concepts")
        concepts = cur.fetchall()
        for c in concepts:
            cur.execute("""
                INSERT OR IGNORE INTO student_mastery (user_id, concept_id, mastery_prob, total_attempts, correct_attempts)
                VALUES (?, ?, ?, 0, 0)
            """, (user_id, c["id"], c["p_init"]))
        conn.commit()


def get_student_mastery(user_id: int) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT sm.*, c.name as concept_name, c.code as concept_code, c.description,
                   c.p_transit, c.p_guess, c.p_slip
            FROM student_mastery sm
            JOIN concepts c ON sm.concept_id = c.id
            WHERE sm.user_id = ?
            ORDER BY c.order_index ASC
        """, (user_id,))
        return [dict(r) for r in cur.fetchall()]


def get_student_concept_mastery(user_id: int, concept_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT sm.*, c.name as concept_name, c.code as concept_code,
                   c.p_init, c.p_transit, c.p_guess, c.p_slip
            FROM student_mastery sm
            JOIN concepts c ON sm.concept_id = c.id
            WHERE sm.user_id = ? AND sm.concept_id = ?
        """, (user_id, concept_id))
        row = cur.fetchone()
        return dict(row) if row else None


def update_student_mastery_record(
    user_id: int,
    concept_id: int,
    new_mastery: float,
    is_correct: bool
) -> None:
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        conn.execute("""
            UPDATE student_mastery
            SET mastery_prob = ?,
                total_attempts = total_attempts + 1,
                correct_attempts = correct_attempts + ?,
                last_updated = ?
            WHERE user_id = ? AND concept_id = ?
        """, (new_mastery, 1 if is_correct else 0, now, user_id, concept_id))
        conn.commit()


def record_assessment_attempt(
    user_id: int,
    question_id: int,
    concept_id: int,
    selected_option_index: int,
    is_correct: bool,
    difficulty: str,
    response_time_sec: float,
    misconception_code: Optional[str],
    prior_mastery: float,
    posterior_mastery: float
) -> int:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO assessment_attempts (
                user_id, question_id, concept_id, selected_option_index,
                is_correct, difficulty, response_time_sec, misconception_code,
                prior_mastery, posterior_mastery, attempted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, question_id, concept_id, selected_option_index,
            1 if is_correct else 0, difficulty, response_time_sec, misconception_code,
            prior_mastery, posterior_mastery, datetime.now().isoformat()
        ))
        attempt_id = cur.lastrowid
        conn.commit()
        return attempt_id


def get_user_attempts(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT aa.*, q.title as question_title, q.prompt as question_prompt,
                   c.name as concept_name, c.code as concept_code
            FROM assessment_attempts aa
            JOIN questions q ON aa.question_id = q.id
            JOIN concepts c ON aa.concept_id = c.id
            WHERE aa.user_id = ?
            ORDER BY aa.attempted_at DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(r) for r in cur.fetchall()]


def get_class_overview() -> Dict[str, Any]:
    """Computes aggregate analytics across all registered students."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as total_students FROM users WHERE role = 'student'")
        total_students = cur.fetchone()["total_students"]

        cur.execute("SELECT COUNT(*) as total_attempts, AVG(is_correct) as avg_accuracy FROM assessment_attempts")
        att_row = cur.fetchone()
        total_attempts = att_row["total_attempts"] or 0
        avg_accuracy = float(att_row["avg_accuracy"] or 0.0)

        cur.execute("""
            SELECT c.name as concept_name, c.code as concept_code,
                   AVG(sm.mastery_prob) as avg_mastery,
                   SUM(sm.total_attempts) as total_concept_attempts
            FROM student_mastery sm
            JOIN concepts c ON sm.concept_id = c.id
            GROUP BY c.id
            ORDER BY c.order_index ASC
        """)
        concept_masteries = [dict(r) for r in cur.fetchall()]

        cur.execute("""
            SELECT misconception_code, COUNT(*) as count
            FROM assessment_attempts
            WHERE is_correct = 0 AND misconception_code IS NOT NULL AND misconception_code != 'NONE'
            GROUP BY misconception_code
            ORDER BY count DESC
            LIMIT 6
        """)
        misconceptions = [dict(r) for r in cur.fetchall()]

        return {
            "total_students": total_students,
            "total_attempts": total_attempts,
            "avg_accuracy": avg_accuracy,
            "concept_masteries": concept_masteries,
            "top_misconceptions": misconceptions
        }
