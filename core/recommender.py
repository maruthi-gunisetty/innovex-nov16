"""
LearnSphere AI: Personalized Recommendation and Learning Path Engine
Uses concept dependency graphs, prerequisite mastery checks, and cognitive
diagnostic data to construct adaptive learning pathways.
"""

from typing import List, Dict, Any, Optional
import json


class RecommenderEngine:
    """
    Constructs personalized learning sequences and adaptive recommendations
    derived from Bayesian Knowledge Tracing scores and concept prerequisites.
    """

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
        "MATH_EIGEN": ["MATH_MATRICES", "MATH_VECTORS"]
    }

    CONCEPT_ORDER: List[str] = ["VAR", "COND", "LOOP", "LIST", "FUNC", "REC"]

    @classmethod
    def get_adaptive_difficulty(cls, mastery_prob: float) -> str:
        """
        Calculates optimal question difficulty to maintain Zone of Proximal Development.
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
        Determines whether the student has met the prerequisite mastery threshold
        for a target concept.
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
    def generate_recommendations(
        cls,
        user_id: int,
        mastery_data: List[Dict[str, Any]],
        recent_attempts: List[Dict[str, Any]],
        lesson_progress: Dict[int, bool]
    ) -> List[Dict[str, Any]]:
        """
        Generates actionable, prioritized learning recommendations dynamically
        across any supported subject and concept sequence.
        """
        mastery_map = {row["concept_code"]: row["mastery_prob"] for row in mastery_data}
        concept_id_map = {row["concept_code"]: row["concept_id"] for row in mastery_data}
        concept_name_map = {row["concept_code"]: row["concept_name"] for row in mastery_data}
        prereqs_map = {row["concept_code"]: row.get("prerequisites", cls.PREREQUISITE_GRAPH.get(row["concept_code"], [])) for row in mastery_data}
        active_concept_order = [row["concept_code"] for row in mastery_data] or cls.CONCEPT_ORDER

        recommendations: List[Dict[str, Any]] = []

        # 1. Inspect recent misconceptions
        misconception_counts: Dict[str, int] = {}
        misconception_concepts: Dict[str, str] = {}
        for att in recent_attempts[:15]:
            code = att.get("misconception_code")
            if code and not att.get("is_correct") and code != "NONE":
                misconception_counts[code] = misconception_counts.get(code, 0) + 1
                misconception_concepts[code] = att.get("concept_code", active_concept_order[0] if active_concept_order else "VAR")

        for m_code, count in misconception_counts.items():
            if count >= 2:
                c_code = misconception_concepts.get(m_code, active_concept_order[0] if active_concept_order else "VAR")
                c_name = concept_name_map.get(c_code, c_code)
                recommendations.append({
                    "concept_id": concept_id_map.get(c_code, 1),
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "type": "misconception_revision",
                    "title": f"Targeted Review: {c_name} Misconceptions",
                    "reason": f"Detected repeating pattern ({m_code}) across {count} recent attempts. Review lesson exercises to correct this mental model.",
                    "priority": 1.5 + (count * 0.2),
                    "recommended_action": "library"
                })

        # 2. Check learning roadmap progression
        first_unlocked_next = None
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            c_name = concept_name_map.get(c_code, c_code)
            c_id = concept_id_map.get(c_code, 1)
            prereq_eval = cls.evaluate_prerequisites(c_code, mastery_map, custom_prereqs=prereqs_map.get(c_code))

            if not prereq_eval["eligible"]:
                # Blocked by prerequisites
                for unmet in prereq_eval["unmet_prerequisites"]:
                    unmet_code = unmet["concept_code"]
                    unmet_name = concept_name_map.get(unmet_code, unmet_code)
                    recommendations.append({
                        "concept_id": concept_id_map.get(unmet_code, 1),
                        "concept_code": unmet_code,
                        "concept_name": unmet_name,
                        "type": "prerequisite_gap",
                        "title": f"Reinforce Foundation: {unmet_name}",
                        "reason": f"Required prerequisite for {c_name}. Current mastery ({unmet['current_mastery']:.0%}) is below benchmark (60%).",
                        "priority": 1.8,
                        "recommended_action": "assessment"
                    })
                break
            else:
                if c_mastery < 0.65:
                    recommendations.append({
                        "concept_id": c_id,
                        "concept_code": c_code,
                        "concept_name": c_name,
                        "type": "practice_drill",
                        "title": f"Adaptive Practice: {c_name}",
                        "reason": f"Current mastery estimate is {c_mastery:.0%}. Complete an adaptive question set to build proficiency.",
                        "priority": 1.4,
                        "recommended_action": "assessment"
                    })
                    break

        # 3. If student has completed foundational steps, recommend next topic
        for c_code in active_concept_order:
            c_mastery = mastery_map.get(c_code, 0.20)
            if c_mastery < 0.80:
                c_name = concept_name_map.get(c_code, c_code)
                c_id = concept_id_map.get(c_code, 1)
                recommendations.append({
                    "concept_id": c_id,
                    "concept_code": c_code,
                    "concept_name": c_name,
                    "type": "next_advancement",
                    "title": f"Next Milestone: {c_name}",
                    "reason": f"All prerequisites satisfied. Proceed to study the core concepts and test your understanding.",
                    "priority": 1.0,
                    "recommended_action": "library"
                })
                break

        # Sort by priority descending
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        return recommendations[:5]

