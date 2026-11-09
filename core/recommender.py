"""
SARVAVIDYA: AI-Powered Personalized Learning Recommendation Engine
Constructs personalized learning sequences and adaptive recommendations
derived from Bayesian Knowledge Tracing scores, cognitive misconceptions,
and prerequisite dependency graphs.

Implements all 6 pedagogical recommendation categories:
1. Study This Concept
2. Practice These Questions
3. Revise Previous Lessons
4. Attempt Advanced Questions
5. Complete Prerequisite Concepts
6. Continue Your Learning Path
"""

from typing import List, Dict, Any, Optional
import json


class RecommenderEngine:
    """
    Modular Recommendation Engine powering personalized guidance across
    Programming, Mathematics, Engineering, Computer Science, and Science tracks.
    """

    # Recommendation Categories
    CATEGORY_STUDY = "Study This Concept"
    CATEGORY_PRACTICE = "Practice These Questions"
    CATEGORY_REVISE = "Revise Previous Lessons"
    CATEGORY_ADVANCED = "Attempt Advanced Questions"
    CATEGORY_PREREQ = "Complete Prerequisite Concepts"
    CATEGORY_PATH = "Continue Your Learning Path"

    # Comprehensive Cross-Subject Prerequisite Graph
    PREREQUISITE_GRAPH: Dict[str, List[str]] = {
        # Python Fundamentals
        "VAR": [],
        "COND": ["VAR"],
        "LOOP": ["VAR", "COND"],
        "LIST": ["VAR", "LOOP"],
        "FUNC": ["VAR", "COND", "LOOP"],
        "REC": ["FUNC", "COND"],

        # C Systems Programming
        "C_DATA_TYPES": [],
        "C_CONTROL_FLOW": ["C_DATA_TYPES"],
        "C_POINTERS": ["C_DATA_TYPES"],
        "C_ARRAYS_STRINGS": ["C_DATA_TYPES", "C_POINTERS"],
        "C_MEMORY_MGMT": ["C_POINTERS"],
        "C_STRUCTS": ["C_DATA_TYPES", "C_POINTERS"],

        # Mathematics (Calculus & Linear Algebra)
        "MATH_LIMITS": [],
        "MATH_DERIVATIVES": ["MATH_LIMITS"],
        "MATH_INTEGRALS": ["MATH_DERIVATIVES"],
        "MATH_MATRICES": [],
        "MATH_VECTORS": [],
        "MATH_EIGEN": ["MATH_MATRICES", "MATH_VECTORS"],

        # Computer Science (Data Structures & Algorithms)
        "DSA_COMPLEXITY": [],
        "DSA_TREES_HEAPS": ["DSA_COMPLEXITY"],
        "DSA_GRAPHS": ["DSA_TREES_HEAPS"],
        "DSA_DP": ["DSA_COMPLEXITY"],

        # Engineering (Digital Logic)
        "DL_BOOLEAN": [],
        "DL_COMBINATIONAL": ["DL_BOOLEAN"],
        "DL_SEQUENTIAL": ["DL_COMBINATIONAL"],
        "DL_ARCHITECTURE": ["DL_SEQUENTIAL"],

        # Science (Classical Mechanics)
        "PHYS_KINEMATICS": [],
        "PHYS_NEWTON": ["PHYS_KINEMATICS"],
        "PHYS_ENERGY": ["PHYS_NEWTON"],
        "PHYS_MOMENTUM": ["PHYS_NEWTON"],

        # Quantum Computing
        "QC_SUPERPOSITION": [],
        "QC_GATES": ["QC_SUPERPOSITION"],
        "QC_ENTANGLEMENT": ["QC_SUPERPOSITION", "QC_GATES"],
        "QC_MEASUREMENT": ["QC_SUPERPOSITION"]
    }

    @classmethod
    def get_adaptive_difficulty(cls, mastery_prob: float) -> str:
        """
        Determines the optimal difficulty level based on Vygotsky's Zone of Proximal Development.
        """
        if mastery_prob < 0.45:
            return "beginner"
        elif mastery_prob < 0.75:
            return "intermediate"
        else:
            return "advanced"

    @classmethod
    def evaluate_prerequisites(
        cls,
        concept_code: str,
        student_mastery_map: Dict[str, float],
        mastery_threshold: float = 0.60,
        custom_prereqs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Validates whether the student satisfies mastery prerequisites for a concept.
        """
        prereqs = custom_prereqs if custom_prereqs is not None else cls.PREREQUISITE_GRAPH.get(concept_code, [])
        unmet = []

        for p_code in prereqs:
            prob = student_mastery_map.get(p_code, 0.20)
            if prob < mastery_threshold:
                unmet.append({
                    "concept_code": p_code,
                    "current_mastery": prob,
                    "required_mastery": mastery_threshold
                })

        return {
            "eligible": len(unmet) == 0,
            "prerequisites": prereqs,
            "unmet_prerequisites": unmet
        }

    @classmethod
    def analyze_learning_gaps(
        cls,
        mastery_data: List[Dict[str, Any]],
        recent_attempts: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorizes student concept status across 5 cognitive levels:
        - Weak (< 40%)
        - Partially Understood (40% - 60%)
        - Requiring Revision (Repeating misconceptions)
        - Strong / Proficient (60% - 85%)
        - Ready for Advanced Practice (>= 85%)
        """
        weak = []
        partial = []
        strong = []
        advanced_ready = []

        for row in mastery_data:
            prob = row.get("mastery_prob", 0.20)
            if prob < 0.40:
                weak.append(row)
            elif prob < 0.60:
                partial.append(row)
            elif prob < 0.85:
                strong.append(row)
            else:
                advanced_ready.append(row)

        # Misconception analysis
        revision_needed = []
        misc_counts: Dict[str, int] = {}
        for att in recent_attempts[:20]:
            code = att.get("misconception_code")
            if code and not att.get("is_correct") and code != "NONE":
                misc_counts[code] = misc_counts.get(code, 0) + 1

        for row in mastery_data:
            # Check if concept has frequent misconceptions
            c_code = row.get("concept_code")
            if any(k.startswith(c_code) or c_code in k for k, cnt in misc_counts.items() if cnt >= 2):
                revision_needed.append(row)

        return {
            "weak": weak,
            "partial": partial,
            "revision_needed": revision_needed,
            "strong": strong,
            "advanced_ready": advanced_ready
        }

    @classmethod
    def generate_recommendations(
        cls,
        user_id: int,
        mastery_data: List[Dict[str, Any]],
        recent_attempts: List[Dict[str, Any]],
        lesson_progress: Optional[Dict[int, bool]] = None
    ) -> List[Dict[str, Any]]:
        """
        Synthesizes student interaction data into prioritized recommendations
        spanning all 6 pedagogical categories.
        """
        if not mastery_data:
            return []

        mastery_map = {row["concept_code"]: row["mastery_prob"] for row in mastery_data}
        concept_id_map = {row["concept_code"]: row["concept_id"] for row in mastery_data}
        concept_name_map = {row["concept_code"]: row["concept_name"] for row in mastery_data}
        prereqs_map = {row["concept_code"]: row.get("prerequisites", cls.PREREQUISITE_GRAPH.get(row["concept_code"], [])) for row in mastery_data}
        active_concept_order = [row["concept_code"] for row in mastery_data]

        recommendations: List[Dict[str, Any]] = []

        # -------------------------------------------------------------
        # 1. CATEGORY: Complete Prerequisite Concepts (Highest Priority)
        # -------------------------------------------------------------
        for c_code in active_concept_order:
            prereq_eval = cls.evaluate_prerequisites(c_code, mastery_map, custom_prereqs=prereqs_map.get(c_code))
            if not prereq_eval["eligible"]:
                for unmet in prereq_eval["unmet_prerequisites"]:
                    unmet_code = unmet["concept_code"]
                    unmet_name = concept_name_map.get(unmet_code, unmet_code)
                    cid = concept_id_map.get(unmet_code, 1)
                    cur_m = unmet["current_mastery"]
                    recommendations.append({
                        "category": cls.CATEGORY_PREREQ,
                        "type": "prerequisite_gap",
                        "title": f"Complete Prerequisite: {unmet_name}",
                        "concept_id": cid,
                        "concept_code": unmet_code,
                        "concept_name": unmet_name,
                        "current_mastery": cur_m,
                        "suggested_difficulty": "Beginner",
                        "estimated_minutes": 20,
                        "reason": f"Required prerequisite for {concept_name_map.get(c_code, c_code)}. Your current mastery is {cur_m:.0%}, which is below the 60% gating threshold.",
                        "priority": 2.5,
                        "recommended_action": "assessment"
                    })
                break

        # -------------------------------------------------------------
        # 2. CATEGORY: Revise Previous Lessons (Cognitive Misconceptions)
        # -------------------------------------------------------------
        misc_counts: Dict[str, int] = {}
        misc_concepts: Dict[str, str] = {}
        for att in recent_attempts[:20]:
            code = att.get("misconception_code")
            if code and not att.get("is_correct") and code != "NONE":
                misc_counts[code] = misc_counts.get(code, 0) + 1
                misc_concepts[code] = att.get("concept_code", active_concept_order[0])

        for m_code, count in misc_counts.items():
            if count >= 2:
                c_code = misc_concepts.get(m_code, active_concept_order[0])
                c_name = concept_name_map.get(c_code, c_code)
                cid = concept_id_map.get(c_code, 1)
                cur_m = mastery_map.get(c_code, 0.30)
                clean_misc = m_code.replace("_", " ").title()
                recommendations.append({
                    "category": cls.CATEGORY_REVISE,
                    "type": "misconception_revision",
                    "title": f"Revise Lesson: {c_name}",
                    "concept_id": cid,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "current_mastery": cur_m,
                    "suggested_difficulty": "Beginner",
                    "estimated_minutes": 15,
                    "reason": f"Identified repeating cognitive misconception ({clean_misc}) across {count} recent attempts. Review foundational lessons to resolve this error pattern.",
                    "priority": 2.2 + (count * 0.1),
                    "recommended_action": "library"
                })
                break

        # -------------------------------------------------------------
        # 3. CATEGORY: Practice These Questions (Weak / Developing Mastery)
        # -------------------------------------------------------------
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            if 0.25 <= c_mastery < 0.65:
                c_name = concept_name_map.get(c_code, c_code)
                cid = concept_id_map.get(c_code, 1)
                diff = "Intermediate" if c_mastery >= 0.45 else "Beginner"
                recommendations.append({
                    "category": cls.CATEGORY_PRACTICE,
                    "type": "practice_drill",
                    "title": f"Practice Questions: {c_name}",
                    "concept_id": cid,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "current_mastery": c_mastery,
                    "suggested_difficulty": diff,
                    "estimated_minutes": 15,
                    "reason": f"You are currently developing proficiency in {c_name} with {c_mastery:.0%} latent mastery. Solve {diff}-level practice drills to reach target mastery.",
                    "priority": 1.9,
                    "recommended_action": "assessment"
                })
                break

        # -------------------------------------------------------------
        # 4. CATEGORY: Study This Concept (Unstarted / Low Initial Mastery)
        # -------------------------------------------------------------
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            prereq_eval = cls.evaluate_prerequisites(c_code, mastery_map, custom_prereqs=prereqs_map.get(c_code))
            if prereq_eval["eligible"] and c_mastery < 0.35:
                c_name = concept_name_map.get(c_code, c_code)
                cid = concept_id_map.get(c_code, 1)
                recommendations.append({
                    "category": cls.CATEGORY_STUDY,
                    "type": "concept_study",
                    "title": f"Study Concept: {c_name}",
                    "concept_id": cid,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "current_mastery": c_mastery,
                    "suggested_difficulty": "Introductory",
                    "estimated_minutes": 25,
                    "reason": f"All prerequisites are satisfied. Start exploring the core principles, syntax examples, and mental models for {c_name}.",
                    "priority": 1.7,
                    "recommended_action": "library"
                })
                break

        # -------------------------------------------------------------
        # 5. CATEGORY: Attempt Advanced Questions (High Mastery >= 75%)
        # -------------------------------------------------------------
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            if c_mastery >= 0.75:
                c_name = concept_name_map.get(c_code, c_code)
                cid = concept_id_map.get(c_code, 1)
                recommendations.append({
                    "category": cls.CATEGORY_ADVANCED,
                    "type": "advanced_challenge",
                    "title": f"Attempt Advanced Questions: {c_name}",
                    "concept_id": cid,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "current_mastery": c_mastery,
                    "suggested_difficulty": "Advanced",
                    "estimated_minutes": 15,
                    "reason": f"Outstanding mastery demonstrated ({c_mastery:.0%}). Tackle advanced-tier edge cases to solidify your mastery.",
                    "priority": 1.3,
                    "recommended_action": "assessment"
                })
                break

        # -------------------------------------------------------------
        # 6. CATEGORY: Continue Your Learning Path (Roadmap Progression)
        # -------------------------------------------------------------
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            if c_mastery < 0.80:
                c_name = concept_name_map.get(c_code, c_code)
                cid = concept_id_map.get(c_code, 1)
                recommendations.append({
                    "category": cls.CATEGORY_PATH,
                    "type": "learning_path_progress",
                    "title": f"Continue Learning Path: {c_name}",
                    "concept_id": cid,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "current_mastery": c_mastery,
                    "suggested_difficulty": cls.get_adaptive_difficulty(c_mastery).capitalize(),
                    "estimated_minutes": 20,
                    "reason": f"Progress through your active learning milestone. Next target is {c_name} (Current: {c_mastery:.0%}).",
                    "priority": 1.1,
                    "recommended_action": "library"
                })
                break

        # Ensure recommendations are unique by concept and sorted by priority
        seen = set()
        deduped = []
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        for r in recommendations:
            key = (r["category"], r["concept_code"])
            if key not in seen:
                seen.add(key)
                deduped.append(r)

        return deduped[:5]
