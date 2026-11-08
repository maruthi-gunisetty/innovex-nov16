"""
Unit Tests for Sarva Vidya Global Search Service
"""

import unittest
from core.search_service import SearchService


class TestSearchService(unittest.TestCase):

    def test_empty_query(self):
        res = SearchService.search("")
        self.assertEqual(res["total_count"], 0)
        self.assertEqual(len(res["concepts"]), 0)
        self.assertEqual(len(res["lessons"]), 0)

    def test_whitespace_query(self):
        res = SearchService.search("   ")
        self.assertEqual(res["total_count"], 0)

    def test_search_concepts(self):
        # Search for loops
        res = SearchService.search("loop")
        self.assertGreater(res["total_count"], 0)
        concept_names = [c["title"].lower() for c in res["concepts"]]
        self.assertTrue(any("loop" in name for name in concept_names))

    def test_search_lessons(self):
        res = SearchService.search("pointer")
        self.assertGreater(res["total_count"], 0)
        lesson_titles = [l["title"].lower() for l in res["lessons"]]
        self.assertTrue(any("pointer" in t for t in lesson_titles))

    def test_search_assessments(self):
        res = SearchService.search("variable")
        self.assertGreater(res["total_count"], 0)
        self.assertGreater(len(res["assessments"]), 0)

    def test_search_platform_modules(self):
        # Searching for progress
        res_prog = SearchService.search("progress")
        self.assertTrue(any(m["target_page"] == "analytics" for m in res_prog["modules"]))

        # Searching for assignments
        res_assign = SearchService.search("assignment")
        self.assertTrue(any(m["target_page"] == "assessment" for m in res_assign["modules"]))

        # Searching for misconceptions
        res_misc = SearchService.search("misconception")
        self.assertTrue(any(m["target_page"] == "misconceptions" for m in res_misc["modules"]))

    def test_search_courses(self):
        res_math = SearchService.search("math")
        self.assertGreater(len(res_math["courses"]), 0)
        self.assertTrue(any("math" in c["title"].lower() or "math" in c["subject_name"].lower() for c in res_math["courses"]))


if __name__ == "__main__":
    unittest.main()

