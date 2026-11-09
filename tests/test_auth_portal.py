"""
Unit Tests for SARVAVIDYA Authentication Portal
Verifies student login, faculty login, validation rules, registration,
and demonstration profile consistency.
"""

import unittest
from core.auth_service import AuthService
from database.db import (
    get_user_by_username, get_user_by_email, create_user
)
from database.seed_data import seed_database


class TestAuthPortal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        seed_database(force=False)

    def test_student_login_success(self):
        user = get_user_by_email("student@123") or get_user_by_username("student@123")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "student")
        self.assertTrue(AuthService.verify_password("student123", user["salt"], user["password_hash"]))

    def test_student_login_invalid_password(self):
        user = get_user_by_email("student@123") or get_user_by_username("student@123")
        self.assertIsNotNone(user)
        self.assertFalse(AuthService.verify_password("wrong_password", user["salt"], user["password_hash"]))

    def test_teacher_login_success(self):
        user = get_user_by_email("teacher@123") or get_user_by_username("teacher@123") or get_user_by_username("dr_bennett")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "teacher")
        self.assertTrue(AuthService.verify_password("teacher123", user["salt"], user["password_hash"]))

    def test_registration_validation(self):
        # Valid data
        valid, err = AuthService.validate_registration("test_user_99", "test99@example.com", "secure123", "secure123", "Test Scholar")
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Mismatched passwords
        valid, err = AuthService.validate_registration("test_user_99", "test99@example.com", "secure123", "different123", "Test Scholar")
        self.assertFalse(valid)
        self.assertIn("match", err.lower())

        # Short password (< 6 chars)
        valid, err = AuthService.validate_registration("test_user_99", "test99@example.com", "123", "123", "Test Scholar")
        self.assertFalse(valid)
        self.assertIn("6 characters", err)

        # Invalid email
        valid, err = AuthService.validate_registration("test_user_99", "invalidemail", "secure123", "secure123", "Test Scholar")
        self.assertFalse(valid)
        self.assertIn("valid email", err)

    def test_registration_flow(self):
        import uuid
        test_uname = f"reg_test_{uuid.uuid4().hex[:6]}"
        test_email = f"{test_uname}@institution.edu"
        pwd = "EnterprisePassword!2026"

        pwd_hash, salt = AuthService.hash_password(pwd)
        uid = create_user(
            username=test_uname,
            email=test_email,
            password_hash=pwd_hash,
            salt=salt,
            full_name="Registered Scholar",
            role="student"
        )
        self.assertIsNotNone(uid)
        self.assertGreater(uid, 0)

        created = get_user_by_username(test_uname)
        self.assertIsNotNone(created)
        self.assertEqual(created["email"], test_email)
        self.assertTrue(AuthService.verify_password(pwd, created["salt"], created["password_hash"]))


if __name__ == "__main__":
    unittest.main()

