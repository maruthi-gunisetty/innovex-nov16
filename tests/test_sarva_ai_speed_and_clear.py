import unittest
from unittest.mock import patch
from core.ai_service import _call_gemini_api, query_gemini_ai
from components.sarva_ai import _handle_assistant_generation
from database.db import init_db, get_user_by_username
from core.course_manager import get_active_course

class TestSarvaAISpeedAndClearing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_gemini_ai_greeting_conversational_response(self):
        course = get_active_course() or {"id": 1, "name": "Python Fundamentals", "subject_name": "Programming"}
        
        # Test greeting prompt
        response = query_gemini_ai(
            prompt="hiiiiiiii",
            course_name=course["name"],
            concept_name="General Curriculum"
        )
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 5)

    def test_handle_assistant_generation(self):
        import streamlit as st
        if "sarva_ai_modal_history" not in st.session_state:
            st.session_state["sarva_ai_modal_history"] = []

        user = {"id": 1, "username": "student@123", "role": "student"}
        course = get_active_course() or {"id": 1, "name": "Python Fundamentals", "subject_name": "Programming"}

        reply, mode = _handle_assistant_generation(
            text="Explain variables in Python",
            user=user,
            course=course,
            concept=None
        )
        self.assertTrue(len(reply) > 10)
        self.assertIn(mode, ["gemini_live", "curriculum_engine"])
        self.assertTrue(any(m["message"] == reply for m in st.session_state["sarva_ai_modal_history"]))

if __name__ == "__main__":
    unittest.main()
