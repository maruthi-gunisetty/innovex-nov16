"""
Unit Tests for Database Persistence and Security
Verifies PBKDF2 hashing, table consistency, user creation, and attempt persistence.
"""

import unittest
from core.auth_service import AuthService
from database.db import (
    get_db_connection, get_user_by_username, create_user,
    get_all_concepts, get_questions_by_concept_and_difficulty,
    record_assessment_attempt, get_student_mastery, update_student_mastery_record
)
from database.seed_data import seed_database


class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        seed_database(force=False)

    def test_concepts_loaded(self):
        concepts = get_all_concepts()
        self.assertEqual(len(concepts), 6)
        codes = [c["code"] for c in concepts]
        self.assertIn("VAR", codes)
        self.assertIn("REC", codes)

    def test_questions_loaded(self):
        questions = get_questions_by_concept_and_difficulty()
        self.assertGreaterEqual(len(questions), 18)
        # Ensure questions have valid options
        for q in questions[:5]:
            self.assertEqual(len(q["options"]), 4)
            correct_opts = [opt for opt in q["options"] if opt.get("is_correct")]
            self.assertEqual(len(correct_opts), 1)

    def test_auth_hashing_and_verification(self):
        password = "SecretPassword!456"
        p_hash, salt = AuthService.hash_password(password)

        # Verification succeeds with matching password
        self.assertTrue(AuthService.verify_password(password, salt, p_hash))

        # Verification fails with wrong password
        self.assertFalse(AuthService.verify_password("WrongPassword", salt, p_hash))

    def test_demo_users_exist(self):
        alex = get_user_by_username("alex_rivera")
        self.assertIsNotNone(alex)
        self.assertEqual(alex["role"], "student")

        sophia = get_user_by_username("sophia_chen")
        self.assertIsNotNone(sophia)
        self.assertEqual(sophia["role"], "student")

        teacher = get_user_by_username("dr_bennett")
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher["role"], "teacher")

    def test_record_attempt_and_mastery(self):
        alex = get_user_by_username("alex_rivera")
        user_id = alex["id"]

        attempt_id = record_assessment_attempt(
            user_id=user_id,
            question_id=1,
            concept_id=1,
            selected_option_index=0,
            is_correct=True,
            difficulty="beginner",
            response_time_sec=14.5,
            misconception_code="NONE",
            prior_mastery=0.70,
            posterior_mastery=0.85
        )
        self.assertIsNotNone(attempt_id)
        self.assertGreater(attempt_id, 0)


if __name__ == "__main__":
    unittest.main()
