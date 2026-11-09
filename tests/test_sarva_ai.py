"""
Unit Tests for SARVA AI Assistant & Recommendation Persistence
Verifies curriculum fallback, non-BKT alteration, chat history, and recommendation tracking.
"""

import unittest
from database.db import (
    save_chat_message, get_chat_history, clear_chat_history,
    save_recommendations, get_student_recommendations, mark_recommendation_followed
)
from components.sarva_ai import _get_curriculum_response


class TestSarvaAIAndRecommendations(unittest.TestCase):

    def test_curriculum_response_explanation(self):
        user = {"id": 1, "username": "student@123", "role": "student"}
        course = {"id": 1, "name": "Python Fundamentals", "code": "python"}
        concept = {"id": 1, "name": "Variables & Data Types", "code": "VAR"}

        reply = _get_curriculum_response("Explain this concept in simple terms", user, course, concept)
        self.assertIn("Variables & Data Types", reply)
        self.assertIn("Python Fundamentals", reply)

    def test_curriculum_response_code_example(self):
        user = {"id": 1, "username": "student@123", "role": "student"}
        course = {"id": 1, "name": "Python Fundamentals", "code": "python"}
        concept = {"id": 1, "name": "Variables & Data Types", "code": "VAR"}

        reply = _get_curriculum_response("Show me a code snippet example", user, course, concept)
        self.assertTrue("```" in reply or "Python" in reply)

    def test_chat_persistence(self):
        # Use existing seeded user to satisfy foreign key constraint
        from database.db import get_user_by_username
        demo_user = get_user_by_username("student@123")
        self.assertIsNotNone(demo_user)
        user_id = demo_user["id"]
        course_id = 1
        clear_chat_history(user_id, course_id)

        save_chat_message(user_id, course_id, 1, "user", "Hello SARVA AI")
        save_chat_message(user_id, course_id, 1, "assistant", "Hello scholar!", mode="curriculum_engine")

        history = get_chat_history(user_id, course_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["message"], "Hello SARVA AI")
        self.assertEqual(history[1]["message"], "Hello scholar!")

        clear_chat_history(user_id, course_id)
        cleared = get_chat_history(user_id, course_id)
        self.assertEqual(len(cleared), 0)

    def test_recommendation_persistence(self):
        # Use existing seeded user to satisfy foreign key constraint
        from database.db import get_user_by_username
        demo_user = get_user_by_username("student@123")
        self.assertIsNotNone(demo_user)
        user_id = demo_user["id"]
        course_id = 1
        mock_recs = [
            {
                "concept_id": 1,
                "category": "Study This Concept",
                "title": "Study Variables",
                "reason": "Mastery is low",
                "priority": 0.95,
                "suggested_difficulty": "beginner",
                "estimated_minutes": 15,
                "type": "study"
            }
        ]
        save_recommendations(user_id, course_id, mock_recs)
        saved = get_student_recommendations(user_id, course_id)
        self.assertGreaterEqual(len(saved), 1)
        self.assertEqual(saved[0]["title"], "Study Variables")
        self.assertEqual(saved[0]["category"], "Study This Concept")

        # Mark followed
        rec_id = saved[0]["id"]
        mark_recommendation_followed(rec_id)
        after_followed = get_student_recommendations(user_id, course_id)
        # Should now be empty because is_completed = 1
        self.assertEqual(len(after_followed), 0)


if __name__ == "__main__":
    unittest.main()
