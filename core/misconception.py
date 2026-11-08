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

    # Comprehensive Multi-Subject Taxonomy of Misconceptions
    MISCONCEPTION_TAXONOMY: Dict[str, Dict[str, str]] = {
        # --- Python Programming ---
        "OFF_BY_ONE_INDEX": {
            "name": "Off-by-One Indexing Fallacy",
            "category": "Data Structures",
            "subject": "Programming",
            "description": "Confusion between 0-based indexing and cardinal length, or misunderstandings of range(stop) non-inclusivity.",
            "remediation": "Review Python slice boundaries and 0-indexing conventions. Remember range(n) yields values from 0 up to n - 1."
        },
        "TYPE_COERCION_CONFUSION": {
            "name": "String Concatenation vs Arithmetic Coercion",
            "category": "Data Types",
            "subject": "Programming",
            "description": "Assuming input() returns a numeric type or that Python implicitly coerces strings to numbers during addition.",
            "remediation": "Always inspect variable types with type(). In Python, '3' + '4' produces '34', not 7. Explicit int() or float() casting is mandatory."
        },
        "VARIABLE_MUTATION_CONFUSION": {
            "name": "Immutable Assignment Misconception",
            "category": "Variables",
            "subject": "Programming",
            "description": "Believing that variable reassignment or string method calls mutate the original value in-place without assignment.",
            "remediation": "Strings and integers are immutable in Python. Operations like s.upper() return a new string and leave s unchanged."
        },
        "BOOLEAN_SHORT_CIRCUIT": {
            "name": "Compound Condition Evaluation Error",
            "category": "Conditional Logic",
            "subject": "Programming",
            "description": "Writing expressions such as 'if x == 1 or 2' assuming 'or 2' checks if x equals 2, rather than evaluating truthiness of 2.",
            "remediation": "In Python, each operand of 'or' is evaluated separately. '2' evaluates to truthy True. Use 'if x in (1, 2)' or 'if x == 1 or x == 2'."
        },
        "LOOP_TERMINATION_STEP": {
            "name": "Loop Step and Bounds Error",
            "category": "Control Flow",
            "subject": "Programming",
            "description": "Misunderstanding when the termination check happens in while loops or assuming range(start, stop, step) includes stop.",
            "remediation": "Trace loop counter states line-by-line. The loop condition is checked before executing each iteration body."
        },
        "LIST_ALIASING_SHADOWING": {
            "name": "List Reference vs Deep Copy Confusion",
            "category": "Data Structures",
            "subject": "Programming",
            "description": "Assuming assignment b = a creates an independent copy of a list rather than an alias referencing the same memory block.",
            "remediation": "Assignment assigns references. Modifying b modifies a. To create an independent shallow copy, use a.copy() or list(a)."
        },
        "RETURN_VALUE_OMISSION": {
            "name": "Print vs Return Equivalence Fallacy",
            "category": "Functions",
            "subject": "Programming",
            "description": "Treating print() inside a function as producing a return value, causing caller variables to hold None.",
            "remediation": "print() displays text to stdout and returns None. To capture and reuse computation output, use the return statement."
        },
        "SCOPE_LEAKAGE": {
            "name": "Local vs Global Scope Assumption",
            "category": "Functions",
            "subject": "Programming",
            "description": "Assuming inner function variables persist into the caller scope, or attempting to modify a global without declaration.",
            "remediation": "Variables defined inside a function reside in the local namespace and are destroyed upon function exit."
        },
        "BASE_CASE_OMISSION": {
            "name": "Recursive Base Case Omission",
            "category": "Recursion",
            "subject": "Programming",
            "description": "Omitting the base condition or placing the recursive call before the boundary check, causing infinite recursion.",
            "remediation": "Every recursive function must have a verified termination branch (base case) that executes without calling itself."
        },
        "RECURSIVE_ACCUMULATOR_RETURN": {
            "name": "Unreturned Recursive Call",
            "category": "Recursion",
            "subject": "Programming",
            "description": "Invoking a recursive function call without returning its result back up the activation stack.",
            "remediation": "When a recursive function computes a value, every recursive invocation branch must return that result back to its caller."
        },

        # --- C Systems Programming ---
        "C_WILD_POINTER_DEREF": {
            "name": "Uninitialized / Wild Pointer Dereference",
            "category": "Pointers & Memory",
            "subject": "Programming",
            "description": "Dereferencing a pointer that contains garbage address data before assigning a valid memory location, leading to segmentation faults.",
            "remediation": "Always initialize pointers to NULL or a valid address (&variable) before dereferencing with *."
        },
        "C_STRING_NULL_TERMINATOR": {
            "name": "Missing Null Terminator \\0 in Strings",
            "category": "Arrays & Strings",
            "subject": "Programming",
            "description": "Allocating string buffers without accounting for the terminating '\\0' byte, causing buffer over-reads in strlen/printf.",
            "remediation": "In C, a string of N characters requires N+1 bytes of buffer storage to hold the terminating null character '\\0'."
        },
        "C_ARRAY_OUT_OF_BOUNDS": {
            "name": "Array Buffer Index Out-of-Bounds",
            "category": "Arrays & Memory",
            "subject": "Programming",
            "description": "Accessing arr[N] on an array of size N. In C, valid indices are strictly 0 to N - 1, and no bounds checking is performed at runtime.",
            "remediation": "An array of size N has valid indices 0 through N-1. Accessing index N invokes undefined behavior."
        },
        "C_MEMORY_LEAK_NO_FREE": {
            "name": "Heap Memory Leak from Missing free()",
            "category": "Memory Management",
            "subject": "Programming",
            "description": "Allocating heap memory via malloc/calloc without matching free() invocations before pointer reassignment or scope termination.",
            "remediation": "Every malloc(), calloc(), or realloc() must have a corresponding free() call to release heap memory back to the operating system."
        },
        "C_INTEGER_DIVISION_TRUNC": {
            "name": "Integer Division Truncation Confusion",
            "category": "Data Types",
            "subject": "Programming",
            "description": "Expecting 5 / 2 to evaluate to 2.5 in C. When both operands are integers, the fractional portion is strictly truncated towards zero.",
            "remediation": "Cast at least one operand to float/double: (float)5 / 2 or 5.0 / 2 produces 2.5."
        },
        "C_POINTER_INCREMENT_PRECEDENCE": {
            "name": "Pointer Dereference and Post-Increment Precedence",
            "category": "Pointers & Memory",
            "subject": "Programming",
            "description": "Confusing *p++ with (*p)++. Post-increment ++ has higher precedence than unary dereference *.",
            "remediation": "*p++ yields the value pointed to by p, then advances pointer p. (*p)++ increments the integer value stored at address p."
        },
        "C_STRUCT_PADDING_ALIGNMENT": {
            "name": "Structure Byte Padding Misconception",
            "category": "Structures",
            "subject": "Programming",
            "description": "Assuming sizeof(struct) is simply the arithmetic sum of its member sizes, ignoring architecture alignment padding.",
            "remediation": "Compilers insert padding bytes between struct members to align data types with natural CPU word boundaries."
        },

        # --- Mathematics (Calculus & Linear Algebra) ---
        "MATH_POWER_RULE_EXPONENT": {
            "name": "Power Rule Misapplication to Exponential Functions",
            "category": "Differential Calculus",
            "subject": "Mathematics",
            "description": "Applying the power rule d/dx(x^n) = n*x^(n-1) to an exponential function like a^x, mistakenly writing d/dx(2^x) = x*2^(x-1).",
            "remediation": "The power rule applies when the variable is in the BASE (x^n). For exponential functions (a^x), the derivative is ln(a)*a^x."
        },
        "MATH_MATRIX_COMMUTATIVITY": {
            "name": "Matrix Multiplication Commutativity Fallacy",
            "category": "Linear Algebra",
            "subject": "Mathematics",
            "description": "Assuming that AB = BA for matrices as with scalar real numbers. In general, matrix multiplication is non-commutative.",
            "remediation": "Matrix multiplication depends strictly on row-column dimensional pairing. In general, AB != BA even when both are defined."
        },
        "MATH_ZERO_DETERMINANT_INVERT": {
            "name": "Singular Matrix Invertibility Confusion",
            "category": "Linear Algebra",
            "subject": "Mathematics",
            "description": "Believing a square matrix with determinant zero can be inverted, or confusing det(A) = 0 with det(A) != 0.",
            "remediation": "A matrix A is invertible (non-singular) if and only if det(A) != 0. If det(A) = 0, columns are linearly dependent and no inverse exists."
        },
        "MATH_CHAIN_RULE_OMISSION": {
            "name": "Chain Rule Inner Derivative Omission",
            "category": "Differential Calculus",
            "subject": "Mathematics",
            "description": "Differentiating composite functions f(g(x)) by differentiating only the outer function without multiplying by g'(x).",
            "remediation": "By the Chain Rule, d/dx[f(g(x))] = f'(g(x)) * g'(x). Always multiply by the derivative of the inner function."
        },
        "MATH_INTEGRATION_CONSTANT": {
            "name": "Indefinite Integral Constant of Integration Omission",
            "category": "Integral Calculus",
            "subject": "Mathematics",
            "description": "Omitting the arbitrary constant + C when calculating indefinite integrals, failing to represent the complete family of antiderivatives.",
            "remediation": "An indefinite integral represents a family of curves differing by vertical translation. Always append + C."
        },
        "MATH_LIMIT_DIRECT_SUB_ZERO": {
            "name": "Direct Substitution into Indeterminate Forms",
            "category": "Calculus Foundations",
            "subject": "Mathematics",
            "description": "Concluding a limit does not exist or equals 0 simply because direct substitution yields 0/0, without factoring or applying L'Hopital.",
            "remediation": "0/0 is an indeterminate form, NOT undefined. Factor common terms, rationalize, or apply L'Hopital's Rule to resolve the limit."
        },
        "MATH_LINEAR_INDEPENDENCE": {
            "name": "Linear Independence vs Span Confusion",
            "category": "Linear Algebra",
            "subject": "Mathematics",
            "description": "Assuming a set of vectors is linearly independent simply because none of the vectors is the zero vector.",
            "remediation": "Vectors are linearly independent if and only if the only linear combination yielding the zero vector is all zero coefficients: c1*v1 + ... + cn*vn = 0 implies all ci = 0."
        },
        "MATH_DISTRIBUTIVE_SQRT": {
            "name": "Radical Addition Distributive Fallacy",
            "category": "Algebraic Foundations",
            "subject": "Mathematics",
            "description": "Assuming sqrt(a^2 + b^2) = a + b (the freshman's exponent fallacy).",
            "remediation": "Square roots do NOT distribute over addition or subtraction: sqrt(a^2 + b^2) != a + b. Check with numbers: sqrt(9 + 16) = 5, but 3 + 4 = 7."
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
        if not misconception_code:
            return None

        meta = cls.get_info(misconception_code)
        if not meta:
            clean_name = misconception_code.replace("_", " ").title()
            meta = {
                "name": clean_name,
                "category": "Domain Principle",
                "subject": "General",
                "description": f"Cognitive discrepancy identified during {concept_name} evaluation.",
                "remediation": f"Review the foundational theory for {concept_name} and test your understanding with practice exercises."
            }

        return {
            "code": misconception_code,
            "name": meta["name"],
            "category": meta["category"],
            "concept": concept_name,
            "question": question_title,
            "description": meta["description"],
            "remediation": meta["remediation"]
        }
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

