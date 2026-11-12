"""
Tests for SARVAVIDYA AI-Powered "Ask AI Why?" Diagnostic Feature
"""

import unittest
from unittest.mock import patch, MagicMock
from core.ai_service import (
    generate_fallback_why_explanation,
    generate_ai_why_explanation,
    generate_ai_why_alternate_example,
    query_ai_why_followup
)
from components.ask_ai_why import render_ask_ai_why_component


class TestAskAIWhyFeature(unittest.TestCase):
    def setUp(self):
        self.sample_question = {
            "id": 101,
            "title": "Type Casting and String Concatenation",
            "prompt": "What is the exact output of: a='20'; b='30'; print(a+b)?",
            "code_snippet": "a = '20'\nb = '30'\nprint(a + b)",
            "difficulty": "beginner",
            "concept_id": 1,
            "concept_code": "PY_TYPES",
            "concept_name": "Data Types & Type Casting",
            "explanation": "Adding two strings performs concatenation, resulting in '2030'."
        }
        self.options = [
            {"index": 0, "text": "50", "is_correct": False, "misconception_code": "TYPE_COERCION_CONFUSION", "explanation": "Believed digits in strings auto-convert to integers."},
            {"index": 1, "text": "2030", "is_correct": True, "misconception_code": "NONE", "explanation": "Correct concatenation."},
            {"index": 2, "text": "TypeError", "is_correct": False, "misconception_code": "TYPE_COERCION_CONFUSION"},
            {"index": 3, "text": "None", "is_correct": False, "misconception_code": "RETURN_VALUE_OMISSION"}
        ]
        self.incorrect_chosen_opt = self.options[0]
        self.correct_chosen_opt = self.options[1]
        self.eval_res = {
            "is_correct": False,
            "chosen_opt": self.incorrect_chosen_opt,
            "prior_mastery": 0.35,
            "posterior_mastery": 0.28,
            "elapsed_time": 4.2,
            "explanation": self.sample_question["explanation"]
        }
        self.active_course = {
            "id": 1,
            "code": "python",
            "name": "Python Fundamentals",
            "subject_name": "Programming"
        }
        self.user = {"id": 1, "username": "student1", "role": "student"}

    def test_fallback_why_explanation_contains_all_seven_sections(self):
        """Verifies that the curriculum fallback generates all 7 structured sections."""
        exp = generate_fallback_why_explanation(
            question_title=self.sample_question["title"],
            question_prompt=self.sample_question["prompt"],
            selected_answer="50",
            correct_answer="2030",
            concept_name=self.sample_question["concept_name"],
            course_name=self.active_course["name"],
            misconception_name="Type Coercion Confusion",
            misconception_explanation="Believed digits in strings auto-convert to integers.",
            base_explanation=self.sample_question["explanation"],
            lesson_summary="Strings use the plus operator for joining characters."
        )

        self.assertIn("1. ❌ Why Your Answer ('50') Was Incorrect", exp)
        self.assertIn("2. ✅ Why '2030' Is The Correct Answer", exp)
        self.assertIn("3. 🧠 The Underlying Misconception", exp)
        self.assertIn("4. 🪜 Step-by-Step Logic", exp)
        self.assertIn("5. 🌍 Real-World Analogy", exp)
        self.assertIn("6. 💻 Core Demonstration", exp)
        self.assertIn("7. 🎯 Quick Practice Check", exp)
        self.assertIn("Type Coercion Confusion", exp)

    def test_generate_ai_why_explanation_offline_fallback(self):
        """Verifies that generate_ai_why_explanation gracefully falls back when API is offline."""
        with patch("core.ai_service._call_gemini_api", return_value=None):
            exp = generate_ai_why_explanation(
                question_title=self.sample_question["title"],
                question_prompt=self.sample_question["prompt"],
                options=self.options,
                selected_answer="50",
                correct_answer="2030",
                subject_name="Programming",
                course_name="Python Fundamentals",
                concept_name="Data Types & Type Casting",
                code_snippet=self.sample_question["code_snippet"],
                misconception_name="Type Coercion Confusion"
            )
            self.assertIsNotNone(exp)
            self.assertIn("50", exp)
            self.assertIn("2030", exp)
            self.assertIn("Type Coercion Confusion", exp)

    def test_generate_ai_why_explanation_live_mock(self):
        """Verifies parsing and return of live model response when available."""
        mock_ai_response = (
            "### 1. ❌ Why Your Answer Was Incorrect\n"
            "You selected '50', which assumes automatic type coercion.\n\n"
            "### 2. ✅ Why '2030' Is The Correct Answer\n"
            "String concatenation links the string characters together directly without arithmetic sum."
        )
        with patch("core.ai_service._call_gemini_api", return_value=mock_ai_response):
            exp = generate_ai_why_explanation(
                question_title=self.sample_question["title"],
                question_prompt=self.sample_question["prompt"],
                options=self.options,
                selected_answer="50",
                correct_answer="2030",
                subject_name="Programming",
                course_name="Python Fundamentals",
                concept_name="Data Types & Type Casting"
            )
            self.assertEqual(exp, mock_ai_response)

    def test_alternate_example_generation(self):
        """Verifies alternate example generation returns actionable pedagogical content."""
        with patch("core.ai_service._call_gemini_api", return_value="Here is an alternative analogy comparing types to labels."):
            alt = generate_ai_why_alternate_example(
                concept_name="Pointers",
                course_name="C Programming",
                question_title="Memory Addresses and Dereferencing"
            )
            self.assertIsNotNone(alt)
            self.assertTrue(len(alt) > 10)

    def test_followup_question_generation(self):
        """Verifies follow-up question returns coherent answer."""
        with patch("core.ai_service._call_gemini_api", return_value="Yes, str() explicitly converts to a string representation."):
            fup = query_ai_why_followup(
                user_query="Can I convert with str()?",
                concept_name="Type Casting",
                course_name="Python Fundamentals",
                question_title="Type Casting and String Concatenation",
                selected_answer="50",
                correct_answer="2030"
            )
            self.assertIsNotNone(fup)
            self.assertTrue(len(fup) > 10)

    def test_render_component_does_nothing_for_correct_answer(self):
        """Ensures 'Ask AI Why?' is strictly NOT displayed for correct answers."""
        import streamlit as st
        with patch.object(st, "button") as mock_btn, patch.object(st, "markdown") as mock_md:
            render_ask_ai_why_component(
                current_q=self.sample_question,
                options=self.options,
                chosen_opt=self.correct_chosen_opt,
                is_correct=True,
                eval_res=self.eval_res,
                active_course=self.active_course,
                user=self.user
            )
            mock_btn.assert_not_called()


if __name__ == "__main__":
    unittest.main()
