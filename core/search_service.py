"""
Sarva Vidya: Global Unified Search Service
Provides multi-index querying across:
1. Concepts and Knowledge Components
2. Learning Content and Lessons
3. Practice Questions and Adaptive Assessments
4. Platform Feature Modules (Progress, BKT Mastery, Misconceptions, Analytics)
5. Courses and Subject Tracks
"""

from typing import Dict, List, Any, Optional
from database.db import get_db_connection


class SearchService:
    """Executes high-performance parameterized search queries across academic and system models."""

    PLATFORM_MODULES = [
        {
            "id": "progress_analytics",
            "title": "Student Progress & Mastery Analytics",
            "subtitle": "BKT latent concept mastery, accuracy distributions, and longitudinal learning telemetry.",
            "category": "Progress & Analytics",
            "target_page": "analytics",
            "badge": "Analytics",
            "action_label": "View Progress",
            "keywords": ["progress", "mastery", "accuracy", "bkt", "latent", "analytics", "stats", "telemetry", "score", "performance", "grade"]
        },
        {
            "id": "adaptive_assessments",
            "title": "Adaptive Assessments & Assignments",
            "subtitle": "IRT-calibrated diagnostic quizzes, adaptive difficulty drills, and mastery evaluations.",
            "category": "Assessments",
            "target_page": "assessment",
            "badge": "Assessments",
            "action_label": "Launch Assessment",
            "keywords": ["assignment", "assignments", "assessment", "assessments", "quiz", "quizzes", "test", "tests", "exam", "drill", "practice", "questions", "homework"]
        },
        {
            "id": "ai_misconceptions",
            "title": "AI Cognitive Intelligence & Misconceptions",
            "subtitle": "Automated mental-bug diagnosis, cognitive distractor analysis, and corrective feedback.",
            "category": "AI Intelligence",
            "target_page": "misconceptions",
            "badge": "AI Core",
            "action_label": "View Intelligence",
            "keywords": ["misconception", "misconceptions", "ai", "intelligence", "bug", "bugs", "error", "errors", "mistake", "cognitive", "diagnostic"]
        },
        {
            "id": "learning_roadmap",
            "title": "Personalized Learning Path & Roadmap",
            "subtitle": "Dynamic prerequisite dependency graph, sequenced curriculum milestones, and pacing recommendations.",
            "category": "Learning Path",
            "target_page": "learning_path",
            "badge": "Roadmap",
            "action_label": "Explore Roadmap",
            "keywords": ["path", "roadmap", "curriculum", "milestone", "prerequisite", "prerequisites", "sequence", "learning path", "journey"]
        },
        {
            "id": "learning_library",
            "title": "Curriculum Library & Code Sandbox",
            "subtitle": "Interactive lessons, multi-language runnable code sandboxes, and concept references.",
            "category": "Library",
            "target_page": "learning_library",
            "badge": "Library",
            "action_label": "Open Library",
            "keywords": ["library", "lesson", "lessons", "content", "sandbox", "code", "notes", "reading", "docs", "curriculum", "study"]
        },
        {
            "id": "account_settings",
            "title": "My Profile & Learning Settings",
            "subtitle": "Daily study goals, target difficulty preferences, credentials, and notification options.",
            "category": "Settings",
            "target_page": "settings",
            "badge": "Profile",
            "action_label": "Open Settings",
            "keywords": ["profile", "settings", "password", "goal", "difficulty", "preferences", "account", "user"]
        },
        {
            "id": "faculty_management",
            "title": "Faculty Intelligence & Cohort Management",
            "subtitle": "Classroom telemetry, at-risk student intervention alerts, and cohort mastery benchmarks.",
            "category": "Faculty",
            "target_page": "teacher_dashboard",
            "badge": "Faculty",
            "action_label": "Open Faculty Portal",
            "keywords": ["students", "faculty", "cohort", "manage", "teacher", "class", "at-risk", "struggling", "excelling"]
        }
    ]

    @classmethod
    def search(cls, query: str, active_course_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes unified search across concepts, lessons, questions, courses, and platform modules.
        Returns a structured dictionary of matched entities and total match count.
        """
        cleaned_query = (query or "").strip().lower()
        if not cleaned_query:
            return {
                "query": "",
                "total_count": 0,
                "concepts": [],
                "lessons": [],
                "assessments": [],
                "modules": [],
                "courses": []
            }

        q_like = f"%{cleaned_query}%"
        results: Dict[str, List[Dict[str, Any]]] = {
            "concepts": [],
            "lessons": [],
            "assessments": [],
            "modules": [],
            "courses": []
        }

        # 1. Match Platform Feature Modules
        for mod in cls.PLATFORM_MODULES:
            # Check title, subtitle, or any keyword
            matched = (
                cleaned_query in mod["title"].lower() or
                cleaned_query in mod["subtitle"].lower() or
                any(kw in cleaned_query or cleaned_query in kw for kw in mod["keywords"])
            )
            if matched:
                results["modules"].append(mod)

        # 2. Match Database Records
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()

                # A. Concepts
                cur.execute("""
                    SELECT c.id, c.code, c.name, c.description, c.course_id,
                           co.name as course_name, s.name as subject_name
                    FROM concepts c
                    LEFT JOIN courses co ON c.course_id = co.id
                    LEFT JOIN subjects s ON c.subject_id = s.id
                    WHERE c.name LIKE ? OR c.code LIKE ? OR c.description LIKE ?
                    ORDER BY (c.name LIKE ?) DESC, c.order_index ASC
                    LIMIT 8
                """, (q_like, q_like, q_like, f"{cleaned_query}%"))
                for row in cur.fetchall():
                    results["concepts"].append({
                        "id": row["id"],
                        "code": row["code"],
                        "title": row["name"],
                        "subtitle": row["description"][:130] + ("..." if len(row["description"]) > 130 else ""),
                        "course_id": row["course_id"],
                        "course_name": row["course_name"] or "Core Curriculum",
                        "subject_name": row["subject_name"] or "General",
                        "category": "Concept",
                        "badge": row["subject_name"] or "Concept",
                        "target_page": "learning_library",
                        "action_label": "Explore Concept"
                    })

                # B. Learning Content / Lessons
                cur.execute("""
                    SELECT lc.id, lc.title, lc.summary, lc.concept_id, lc.reading_time_min,
                           c.name as concept_name, c.code as concept_code, c.course_id,
                           co.name as course_name
                    FROM learning_content lc
                    JOIN concepts c ON lc.concept_id = c.id
                    LEFT JOIN courses co ON c.course_id = co.id
                    WHERE lc.title LIKE ? OR lc.summary LIKE ? OR lc.detailed_explanation LIKE ?
                    LIMIT 8
                """, (q_like, q_like, q_like))
                for row in cur.fetchall():
                    results["lessons"].append({
                        "id": row["id"],
                        "title": row["title"],
                        "subtitle": row["summary"][:130] + ("..." if len(row["summary"]) > 130 else ""),
                        "concept_id": row["concept_id"],
                        "concept_name": row["concept_name"],
                        "concept_code": row["concept_code"],
                        "course_id": row["course_id"],
                        "course_name": row["course_name"] or "General",
                        "reading_time_min": row["reading_time_min"],
                        "category": "Lesson",
                        "badge": f"{row['reading_time_min']} min read",
                        "target_page": "learning_library",
                        "action_label": "Read Lesson"
                    })

                # C. Assessment Questions & Practice
                cur.execute("""
                    SELECT q.id, q.title, q.prompt, q.difficulty, q.concept_id,
                           c.name as concept_name, c.code as concept_code, c.course_id,
                           co.name as course_name
                    FROM questions q
                    JOIN concepts c ON q.concept_id = c.id
                    LEFT JOIN courses co ON c.course_id = co.id
                    WHERE q.title LIKE ? OR q.prompt LIKE ? OR c.name LIKE ?
                    LIMIT 6
                """, (q_like, q_like, q_like))
                for row in cur.fetchall():
                    results["assessments"].append({
                        "id": row["id"],
                        "title": row["title"],
                        "subtitle": row["prompt"][:120] + ("..." if len(row["prompt"]) > 120 else ""),
                        "difficulty": row["difficulty"].capitalize(),
                        "concept_id": row["concept_id"],
                        "concept_name": row["concept_name"],
                        "concept_code": row["concept_code"],
                        "course_id": row["course_id"],
                        "course_name": row["course_name"],
                        "category": "Practice Drill",
                        "badge": row["difficulty"].capitalize(),
                        "target_page": "assessment",
                        "action_label": "Practice Concept"
                    })

                # D. Courses & Subject Tracks
                cur.execute("""
                    SELECT co.id, co.code, co.name, co.description, co.difficulty_level,
                           s.name as subject_name
                    FROM courses co
                    JOIN subjects s ON co.subject_id = s.id
                    WHERE co.name LIKE ? OR co.description LIKE ? OR s.name LIKE ?
                    LIMIT 4
                """, (q_like, q_like, q_like))
                for row in cur.fetchall():
                    results["courses"].append({
                        "id": row["id"],
                        "code": row["code"],
                        "title": row["name"],
                        "subtitle": row["description"][:120] + ("..." if len(row["description"]) > 120 else ""),
                        "subject_name": row["subject_name"],
                        "difficulty_level": row["difficulty_level"],
                        "category": "Course Track",
                        "badge": row["subject_name"],
                        "target_page": "student_dashboard",
                        "action_label": "Switch to Course"
                    })

        except Exception as e:
            print(f"[SearchService] Search error: {e}")

        total_count = (
            len(results["concepts"]) +
            len(results["lessons"]) +
            len(results["assessments"]) +
            len(results["modules"]) +
            len(results["courses"])
        )

        return {
            "query": query,
            "total_count": total_count,
            "concepts": results["concepts"],
            "lessons": results["lessons"],
            "assessments": results["assessments"],
            "modules": results["modules"],
            "courses": results["courses"]
        }

