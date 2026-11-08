"""
LearnSphere AI: Authentication and Security Service
Provides cryptographically secure PBKDF2 password hashing, salt generation,
input sanitization, and role verification.
"""

import hashlib
import os
import re
from typing import Tuple, Optional, Dict, Any


class AuthService:
    """
    Handles user credential hashing, validation, and session verification.
    """

    ITERATIONS = 100_000

    @classmethod
    def hash_password(cls, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hashes a plain password using PBKDF2-HMAC-SHA256 with 100,000 rounds.
        Returns (hex_hash, hex_salt).
        """
        if salt is None:
            salt_bytes = os.urandom(16)
            salt = salt_bytes.hex()
        else:
            salt_bytes = bytes.fromhex(salt)

        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt_bytes,
            iterations=cls.ITERATIONS
        )
        return key.hex(), salt

    @classmethod
    def verify_password(cls, password: str, salt: str, expected_hash: str) -> bool:
        """
        Verifies whether a password matches the recorded hash.
        Uses constant-time comparison to prevent timing attacks.
        """
        test_hash, _ = cls.hash_password(password, salt)
        import hmac
        return hmac.compare_digest(test_hash, expected_hash)

    @classmethod
    def validate_registration(
        cls,
        username: str,
        email: str,
        password: str,
        confirm_password: str,
        full_name: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates form inputs before creating a new user account.
        """
        if not username or len(username.strip()) < 3:
            return False, "Username must be at least 3 characters long."

        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return False, "Username may only contain letters, numbers, underscores, and dashes."

        if not email or "@" not in email or "." not in email:
            return False, "Please enter a valid email address."

        if not full_name or len(full_name.strip()) < 2:
            return False, "Please provide your full name."

        if len(password) < 6:
            return False, "Password must be at least 6 characters long."

        if password != confirm_password:
            return False, "Passwords do not match."

        return True, None
