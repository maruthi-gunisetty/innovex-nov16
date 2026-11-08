"""
LearnSphere AI: Misconception Detection Engine
Analyzes student distractors to diagnose cognitive bugs, pattern repetition,
and domain-specific programming misconceptions.
"""

from typing import Dict, List, Any, Optional


class MisconceptionEngine:
    """
    Catalog and rule-based diagnostic engine for programming misconceptions.
    Maps labeled distractor selections into diagnostic reports and corrective interventions.
    """

    # Comprehensive Taxonomy of Python Programming Misconceptions
    MISCONCEPTION_TAXONOMY: Dict[str, Dict[str, str]] = {
        "OFF_BY_ONE_INDEX": {
            "name": "Off-by-One Indexing Fallacy",
            "category": "Data Structures",
            "description": "Confusion between 0-based indexing and cardinal length, or misunderstandings of range(stop) non-inclusivity.",
            "remediation": "Review Python slice boundaries and 0-indexing conventions. Remember range(n) yields values from 0 up to n - 1."
        },
        "TYPE_COERCION_CONFUSION": {
            "name": "String Concatenation vs Arithmetic Coercion",
            "category": "Data Types",
            "description": "Assuming input() returns a numeric type or that Python implicitly coerces strings to numbers during addition.",
            "remediation": "Always inspect variable types with type(). In Python, '3' + '4' produces '34', not 7. Explicit int() or float() casting is mandatory."
        },
        "VARIABLE_MUTATION_CONFUSION": {
            "name": "Immutable Assignment Misconception",
            "category": "Variables",
            "description": "Believing that variable reassignment or string method calls mutate the original value in-place without assignment.",
            "remediation": "Strings and integers are immutable in Python. Operations like s.upper() return a new string and leave s unchanged."
        },
        "BOOLEAN_SHORT_CIRCUIT": {
            "name": "Compound Condition Evaluation Error",
            "category": "Conditional Logic",
            "description": "Writing expressions such as 'if x == 1 or 2' assuming 'or 2' checks if x equals 2, rather than evaluating truthiness of 2.",
            "remediation": "In Python, each operand of 'or' is evaluated separately. '2' evaluates to truthy True. Use 'if x in (1, 2)' or 'if x == 1 or x == 2'."
        },
        "LOOP_TERMINATION_STEP": {
            "name": "Loop Step and Bounds Error",
            "category": "Control Flow",
            "description": "Misunderstanding when the termination check happens in while loops or assuming range(start, stop, step) includes stop.",
            "remediation": "Trace loop counter states line-by-line. The loop condition is checked before executing each iteration body."
        },
        "LIST_ALIASING_SHADOWING": {
            "name": "List Reference vs Deep Copy Confusion",
            "category": "Data Structures",
            "description": "Assuming assignment b = a creates an independent copy of a list rather than an alias referencing the same memory block.",
            "remediation": "Assignment assigns references. Modifying b modifies a. To create an independent shallow copy, use a.copy() or list(a)."
        },
        "RETURN_VALUE_OMISSION": {
            "name": "Print vs Return Equivalence Fallacy",
            "category": "Functions",
            "description": "Treating print() inside a function as producing a return value, causing caller variables to hold None.",
            "remediation": "print() displays text to stdout and returns None. To capture and reuse computation output, use the return statement."
        },
        "SCOPE_LEAKAGE": {
            "name": "Local vs Global Scope Assumption",
            "category": "Functions",
            "description": "Assuming inner function variables persist into the caller scope, or attempting to modify a global without declaration.",
            "remediation": "Variables defined inside a function reside in the local namespace and are destroyed upon function exit."
        },
        "BASE_CASE_OMISSION": {
            "name": "Recursive Base Case Omission",
            "category": "Recursion",
            "description": "Omitting the base condition or placing the recursive call before the boundary check, causing infinite recursion.",
            "remediation": "Every recursive function must have a verified termination branch (base case) that executes without calling itself."
        },
        "RECURSIVE_ACCUMULATOR_RETURN": {
            "name": "Unreturned Recursive Call",
            "category": "Recursion",
            "description": "Invoking a recursive function call without returning its result back up the activation stack.",
            "remediation": "When a recursive function computes a value, every recursive invocation branch must return that result back to its caller."
        }
    }

    @classmethod
    def get_info(cls, code: Optional[str]) -> Optional[Dict[str, str]]:
        """Retrieves metadata for a specific misconception code."""
        if not code:
            return None
        return cls.MISCONCEPTION_TAXONOMY.get(code)

    @classmethod
    def diagnose_attempt(
        cls,
        misconception_code: Optional[str],
        question_title: str,
        concept_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a structured diagnostic analysis for an incorrect attempt.
        """
        if not misconception_code or misconception_code not in cls.MISCONCEPTION_TAXONOMY:
            return None

        meta = cls.MISCONCEPTION_TAXONOMY[misconception_code]
        return {
            "code": misconception_code,
            "name": meta["name"],
            "category": meta["category"],
            "concept": concept_name,
            "question": question_title,
            "description": meta["description"],
            "remediation": meta["remediation"]
        }

    @classmethod
    def summarize_patterns(cls, attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a sequence of student attempts to detect persistent misconception patterns.
        """
        frequency: Dict[str, int] = {}
        by_category: Dict[str, int] = {}

        for att in attempts:
            code = att.get("misconception_code")
            if code and code in cls.MISCONCEPTION_TAXONOMY:
                frequency[code] = frequency.get(code, 0) + 1
                cat = cls.MISCONCEPTION_TAXONOMY[code]["category"]
                by_category[cat] = by_category.get(cat, 0) + 1

        # Sort by occurrence
        sorted_patterns = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        remedial_targets = []
        for code, count in sorted_patterns:
            meta = cls.MISCONCEPTION_TAXONOMY[code]
            remedial_targets.append({
                "code": code,
                "name": meta["name"],
                "category": meta["category"],
                "count": count,
                "remediation": meta["remediation"],
                "severity": "High" if count >= 3 else ("Moderate" if count >= 2 else "Low")
            })

        return {
            "total_misconceptions_detected": sum(frequency.values()),
            "unique_patterns_count": len(frequency),
            "dominant_category": max(by_category, key=by_category.get) if by_category else "None",
            "patterns": remedial_targets
        }

