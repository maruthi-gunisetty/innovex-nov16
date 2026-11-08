"""
Unit and Integration Tests for LearnSphere AI Multi-Subject Support
Verifies:
1. Retrieval of multiple subjects and courses.
2. Independent question banks and learning content.
3. Bayesian Knowledge Tracing across Python, C, and Mathematics.
4. Cognitive misconception detection for C and Math distractors.
5. Adaptive difficulty and prerequisite recommendations.
6. Dynamic runtime addition of new subjects through the database.
"""

import unittest
from database.db import (
    get_all_subjects, get_subject_by_code, get_all_courses,
    get_course_by_code, get_concepts_by_course, get_all_concepts,
    get_questions_by_concept_and_difficulty, get_all_learning_content,
    get_student_mastery, record_assessment_attempt, get_db_connection
)
from database.seed_data import seed_database
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine
from core.recommender import RecommenderEngine


class TestMultiSubjectPlatform(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        seed_database(force=False)

    def test_subjects_and_courses_exist(self):
        subjects = get_all_subjects()
        self.assertGreaterEqual(len(subjects), 5)
        sub_codes = [s["code"] for s in subjects]
        self.assertIn("programming", sub_codes)
        self.assertIn("mathematics", sub_codes)
        self.assertIn("engineering", sub_codes)
        self.assertIn("science", sub_codes)
        self.assertIn("computer_science", sub_codes)

        courses = get_all_courses()
        self.assertGreaterEqual(len(courses), 6)
        c_codes = [c["code"] for c in courses]
        self.assertIn("python", c_codes)
        self.assertIn("c_programming", c_codes)
        self.assertIn("calculus_linear_algebra", c_codes)

    def test_c_programming_content_isolation(self):
        c_course = get_course_by_code("c_programming")
        self.assertIsNotNone(c_course)

        c_concepts = get_concepts_by_course(c_course["id"])
        self.assertEqual(len(c_concepts), 6)
        c_codes = [c["code"] for c in c_concepts]
        self.assertIn("C_POINTERS", c_codes)
        self.assertIn("C_MEMORY_MGMT", c_codes)

        c_questions = get_questions_by_concept_and_difficulty(course_id=c_course["id"])
        self.assertGreaterEqual(len(c_questions), 12)

        c_lessons = get_all_learning_content(course_id=c_course["id"])
        self.assertGreaterEqual(len(c_lessons), 4)

    def test_mathematics_content_isolation(self):
        math_course = get_course_by_code("calculus_linear_algebra")
        self.assertIsNotNone(math_course)

        math_concepts = get_concepts_by_course(math_course["id"])
        self.assertEqual(len(math_concepts), 6)
        m_codes = [c["code"] for c in math_concepts]
        self.assertIn("MATH_LIMITS", m_codes)
        self.assertIn("MATH_DERIVATIVES", m_codes)
        self.assertIn("MATH_MATRICES", m_codes)

        math_questions = get_questions_by_concept_and_difficulty(course_id=math_course["id"])
        self.assertGreaterEqual(len(math_questions), 12)

    def test_bkt_computation_across_subjects(self):
        bkt = BayesianKnowledgeTracing()

        prior = 0.20
        post_obs_corr, next_prior_corr = bkt.update(prior, is_correct=True)
        self.assertGreater(post_obs_corr, prior)
        self.assertGreater(next_prior_corr, prior)

        post_obs_inc, next_prior_inc = bkt.update(prior, is_correct=False)
        self.assertLess(post_obs_inc, prior)

    def test_misconception_diagnostics_c_and_math(self):
        c_diag = MisconceptionEngine.diagnose_attempt(
            misconception_code="C_WILD_POINTER_DEREF",
            question_title="Pointer Dereference Safety",
            concept_name="C Pointers"
        )
        self.assertIsNotNone(c_diag)
        self.assertEqual(c_diag["code"], "C_WILD_POINTER_DEREF")
        self.assertIn("pointer", c_diag["remediation"].lower())

        math_diag = MisconceptionEngine.diagnose_attempt(
            misconception_code="MATH_POWER_RULE_EXPONENT",
            question_title="Exponential Differentiation",
            concept_name="Derivatives"
        )
        self.assertIsNotNone(math_diag)
        self.assertEqual(math_diag["code"], "MATH_POWER_RULE_EXPONENT")
        self.assertIn("power rule", math_diag["remediation"].lower())

    def test_prerequisite_recommendations_c_and_math(self):
        # C memory allocation requires C pointers
        c_eval_locked = RecommenderEngine.evaluate_prerequisites("C_MEMORY_MGMT", {"C_POINTERS": 0.35})
        self.assertFalse(c_eval_locked["eligible"])

        c_eval_unlocked = RecommenderEngine.evaluate_prerequisites("C_MEMORY_MGMT", {"C_POINTERS": 0.85})
        self.assertTrue(c_eval_unlocked["eligible"])

        # Math integrals require derivatives
        math_eval_locked = RecommenderEngine.evaluate_prerequisites("MATH_INTEGRALS", {"MATH_DERIVATIVES": 0.40})
        self.assertFalse(math_eval_locked["eligible"])

        math_eval_unlocked = RecommenderEngine.evaluate_prerequisites("MATH_INTEGRALS", {"MATH_DERIVATIVES": 0.75})
        self.assertTrue(math_eval_unlocked["eligible"])

    def test_dynamic_new_subject_addition_without_code_changes(self):
        """Verifies Requirement 10: New subjects can be added through the database without rewriting AI engine."""
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO subjects (code, name, category, description, icon, order_index)
                VALUES ('quantum_comp', 'Quantum Computing', 'Science', 'Quantum algorithms and qubits', 'atom', 99)
            """)
            conn.commit()

            cur.execute("SELECT id FROM subjects WHERE code = 'quantum_comp'")
            sub_id = cur.fetchone()[0]

            cur.execute("""
                INSERT OR IGNORE INTO courses (subject_id, code, name, description, difficulty_level, order_index)
                VALUES (?, 'qc_101', 'Intro to Qubits', 'Quantum gates and superposition', 'intermediate', 1)
            """, (sub_id,))
            conn.commit()

            cur.execute("SELECT id FROM courses WHERE code = 'qc_101'")
            c_id = cur.fetchone()[0]

            cur.execute("""
                INSERT OR IGNORE INTO concepts (subject_id, course_id, code, name, description, order_index)
                VALUES (?, ?, 'QC_SUPERPOSITION', 'Quantum Superposition', 'Bloch sphere and state vectors', 1)
            """, (sub_id, c_id))
            conn.commit()

        # Query through standard database methods
        qc_concepts = get_concepts_by_course(c_id)
        self.assertEqual(len(qc_concepts), 1)
        self.assertEqual(qc_concepts[0]["code"], "QC_SUPERPOSITION")

        # Dynamic fallback diagnosis works automatically without code modifications
        diag = MisconceptionEngine.diagnose_attempt(
            misconception_code="QC_STATE_COLLAPSE_CONFUSION",
            question_title="Qubit Measurement",
            concept_name="Quantum Superposition"
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["code"], "QC_STATE_COLLAPSE_CONFUSION")


if __name__ == "__main__":
    unittest.main()
