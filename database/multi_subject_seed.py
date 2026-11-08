"""
LearnSphere AI: Multi-Subject Curriculum Dataset
Comprehensive curriculum, calibrated question banks, and learning modules
for C Systems Programming, Calculus & Linear Algebra, and catalog tracks.
"""

import json

# ==========================================
# 1. SUBJECTS SPECIFICATION
# ==========================================
SUBJECTS = [
    {
        "code": "programming",
        "name": "Programming",
        "category": "Programming",
        "description": "Core syntax, memory architectures, pointer arithmetic, dynamic collections, and algorithmic problem-solving across modern languages.",
        "icon": "code",
        "order_index": 1
    },
    {
        "code": "mathematics",
        "name": "Mathematics",
        "category": "Mathematics",
        "description": "Differential and integral calculus, vector spaces, matrix determinants, eigenvalues, and discrete analytical structures.",
        "icon": "math",
        "order_index": 2
    },
    {
        "code": "engineering",
        "name": "Engineering",
        "category": "Engineering",
        "description": "Boolean minimization, combinational logic gates, sequential state machines, and microcomputer architectures.",
        "icon": "cpu",
        "order_index": 3
    },
    {
        "code": "science",
        "name": "Science",
        "category": "Science",
        "description": "Newtonian mechanics, work-energy principles, rotational dynamics, conservation laws, and physical systems modeling.",
        "icon": "atom",
        "order_index": 4
    },
    {
        "code": "computer_science",
        "name": "Computer Science",
        "category": "Computer Science",
        "description": "Asymptotic analysis, balanced search trees, graph theory traversals, shortest-path algorithms, and dynamic programming.",
        "icon": "layers",
        "order_index": 5
    }
]

# ==========================================
# 2. COURSES SPECIFICATION
# ==========================================
COURSES = [
    {
        "subject_code": "programming",
        "code": "python",
        "name": "Python Fundamentals",
        "description": "Dynamic typing, control flow, list comprehensions, modular functions, and recursive execution in Python.",
        "difficulty_level": "Introductory",
        "order_index": 1
    },
    {
        "subject_code": "programming",
        "code": "c_programming",
        "name": "C Systems Programming",
        "description": "Memory address manipulation, pointer arithmetic, manual heap management with malloc/free, and structure alignment.",
        "difficulty_level": "Intermediate",
        "order_index": 2
    },
    {
        "subject_code": "mathematics",
        "code": "calculus_linear_algebra",
        "name": "Calculus & Linear Algebra",
        "description": "Limits, derivatives, the chain rule, definite integrals, matrix algebra, determinants, and eigenvalue spectra.",
        "difficulty_level": "Intermediate",
        "order_index": 3
    },
    {
        "subject_code": "engineering",
        "code": "digital_electronics",
        "name": "Digital Logic & Microprocessors",
        "description": "Karnaugh maps, multiplexers, latches, flip-flops, registers, and ALU design.",
        "difficulty_level": "Introductory",
        "order_index": 4
    },
    {
        "subject_code": "science",
        "code": "physics_mechanics",
        "name": "Classical Mechanics & Kinematics",
        "description": "Vectors in kinematics, Newton's three laws, momentum conservation, and harmonic oscillation.",
        "difficulty_level": "Introductory",
        "order_index": 5
    },
    {
        "subject_code": "computer_science",
        "code": "dsa",
        "name": "Data Structures & Algorithms",
        "description": "Asymptotic complexity, heaps, binary search trees, BFS/DFS, and dynamic programming memoization.",
        "difficulty_level": "Advanced",
        "order_index": 6
    }
]

# ==========================================
# 3. C SYSTEMS PROGRAMMING CONCEPTS
# ==========================================
C_CONCEPTS = [
    {
        "code": "C_DATA_TYPES",
        "name": "C Data Types & Memory Sizes",
        "description": "Primitive types (int, char, float, double), sizeof operator, signed vs unsigned, and format specifiers.",
        "order_index": 1,
        "p_init": 0.25,
        "p_transit": 0.18,
        "p_guess": 0.20,
        "p_slip": 0.08,
        "prerequisites": json.dumps([])
    },
    {
        "code": "C_CONTROL_FLOW",
        "name": "Control Flow & Switch Branching",
        "description": "If/else branching, switch-case fallthrough, break semantics, and ternary evaluation.",
        "order_index": 2,
        "p_init": 0.22,
        "p_transit": 0.16,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["C_DATA_TYPES"])
    },
    {
        "code": "C_POINTERS",
        "name": "Pointers & Address Arithmetic",
        "description": "Address-of operator (&), dereference operator (*), pointer initialization, and pointer arithmetic.",
        "order_index": 3,
        "p_init": 0.15,
        "p_transit": 0.13,
        "p_guess": 0.20,
        "p_slip": 0.12,
        "prerequisites": json.dumps(["C_DATA_TYPES"])
    },
    {
        "code": "C_ARRAYS_STRINGS",
        "name": "Arrays & Null-Terminated Strings",
        "description": "Array memory continuity, pointer decay, null terminator '\\0', and buffer boundary enforcement.",
        "order_index": 4,
        "p_init": 0.16,
        "p_transit": 0.14,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["C_DATA_TYPES", "C_POINTERS"])
    },
    {
        "code": "C_MEMORY_MGMT",
        "name": "Dynamic Memory (malloc/free)",
        "description": "Heap allocation via malloc/calloc/realloc, heap fragmentation, memory leaks, and free semantics.",
        "order_index": 5,
        "p_init": 0.12,
        "p_transit": 0.12,
        "p_guess": 0.20,
        "p_slip": 0.14,
        "prerequisites": json.dumps(["C_POINTERS"])
    },
    {
        "code": "C_STRUCTS",
        "name": "Structures & Pointer Members (->)",
        "description": "Custom structs, typedefs, member access via dot (.) vs arrow (->), and memory word alignment padding.",
        "order_index": 6,
        "p_init": 0.14,
        "p_transit": 0.12,
        "p_guess": 0.20,
        "p_slip": 0.11,
        "prerequisites": json.dumps(["C_DATA_TYPES", "C_POINTERS"])
    }
]

# ==========================================
# 4. MATHEMATICS CONCEPTS
# ==========================================
MATH_CONCEPTS = [
    {
        "code": "MATH_LIMITS",
        "name": "Limits & Continuity",
        "description": "Intuitive limits, one-sided limits, continuity criteria, and resolving indeterminate forms (0/0).",
        "order_index": 1,
        "p_init": 0.25,
        "p_transit": 0.18,
        "p_guess": 0.20,
        "p_slip": 0.08,
        "prerequisites": json.dumps([])
    },
    {
        "code": "MATH_DERIVATIVES",
        "name": "Differential Calculus & Chain Rule",
        "description": "Instantaneous rate of change, power rule, product rule, quotient rule, and composite chain rule.",
        "order_index": 2,
        "p_init": 0.20,
        "p_transit": 0.16,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["MATH_LIMITS"])
    },
    {
        "code": "MATH_INTEGRALS",
        "name": "Definite & Indefinite Integrals",
        "description": "Antiderivatives, Riemann summation, Fundamental Theorem of Calculus, u-substitution, and constant + C.",
        "order_index": 3,
        "p_init": 0.16,
        "p_transit": 0.14,
        "p_guess": 0.20,
        "p_slip": 0.12,
        "prerequisites": json.dumps(["MATH_DERIVATIVES"])
    },
    {
        "code": "MATH_MATRICES",
        "name": "Matrix Algebra & Invertibility",
        "description": "Matrix operations, non-commutativity (AB != BA), determinants, and non-singular invertibility (det != 0).",
        "order_index": 4,
        "p_init": 0.18,
        "p_transit": 0.15,
        "p_guess": 0.20,
        "p_slip": 0.09,
        "prerequisites": json.dumps([])
    },
    {
        "code": "MATH_VECTORS",
        "name": "Vector Spaces & Orthogonal Projections",
        "description": "Linear combinations, linear independence, basis, span, dot product, and orthogonal projection.",
        "order_index": 5,
        "p_init": 0.15,
        "p_transit": 0.13,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["MATH_MATRICES"])
    },
    {
        "code": "MATH_EIGEN",
        "name": "Eigenvalues & Eigenvectors",
        "description": "Characteristic equation det(A - lambda*I) = 0, eigenspaces, matrix diagonalization, and spectral analysis.",
        "order_index": 6,
        "p_init": 0.10,
        "p_transit": 0.11,
        "p_guess": 0.20,
        "p_slip": 0.13,
        "prerequisites": json.dumps(["MATH_MATRICES", "MATH_VECTORS"])
    }
]

# ==========================================
# 5. C PROGRAMMING QUESTIONS
# ==========================================
C_QUESTIONS = [
    # C_DATA_TYPES (4 questions)
    {
        "concept_code": "C_DATA_TYPES",
        "difficulty": "beginner",
        "title": "Integer Division Truncation in C",
        "prompt": "What is the exact output of the following C code snippet?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    int a = 7;\n    int b = 2;\n    float result = a / b;\n    printf(\"%.2f\\n\", result);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "3.00", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Both a and b are integers, so integer division occurs first yielding integer 3, which is then widened to float 3.00."},
            {"index": 1, "text": "3.50", "is_correct": False, "misconception_code": "C_INTEGER_DIVISION_TRUNC", "misconception_name": "Integer Division Truncation Confusion", "explanation": "Believed that assigning to float converts the division to floating-point before evaluation."},
            {"index": 2, "text": "3", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "%.2f specifies floating point output with two decimal digits, not an integer."},
            {"index": 3, "text": "Compilation Error", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "This is completely valid C syntax."}
        ],
        "explanation": "In C, when both operands of the division operator / are integers, the operation performs integer truncation toward zero (7 / 2 = 3). Assigning the result to a float variable Widens the already-truncated integer 3 to 3.00. To preserve decimals, at least one operand must be cast: (float)a / b."
    },
    {
        "concept_code": "C_DATA_TYPES",
        "difficulty": "intermediate",
        "title": "sizeof Operator Evaluation with Expressions",
        "prompt": "What does this program print upon execution?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    int i = 10;\n    printf(\"%zu \", sizeof(i++));\n    printf(\"%d\\n\", i);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "4 10 (or 2 10 depending on arch, i unchanged)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "sizeof is an unevaluated operand at runtime; i++ is never executed, leaving i as 10."},
            {"index": 1, "text": "4 11", "is_correct": False, "misconception_code": "C_DATA_TYPES_SIZEOF_EVAL", "misconception_name": "sizeof Side-Effect Evaluation Error", "explanation": "Assuming expressions inside sizeof are evaluated at runtime with active side effects."},
            {"index": 2, "text": "10 11", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "sizeof returns byte width, not variable value."},
            {"index": 3, "text": "Undefined Behavior", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "C standard explicitly defines sizeof as unevaluated compile-time construct."}
        ],
        "explanation": "In ISO C, sizeof is a compile-time operator. The expression inside sizeof is NOT evaluated at runtime (except for Variable Length Arrays). Thus i++ does not execute, and i remains 10."
    },
    {
        "concept_code": "C_DATA_TYPES",
        "difficulty": "advanced",
        "title": "Unsigned Integer Underflow Wrap-Around",
        "prompt": "What is printed by the following unsigned comparison loop?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    unsigned int u = 0;\n    u = u - 1;\n    if (u > 0) {\n        printf(\"Wrapped\\n\");\n    } else {\n        printf(\"Negative\\n\");\n    }\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "Wrapped", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Unsigned integers cannot hold negative numbers; 0 - 1 wraps around to UINT_MAX (e.g. 4294967295), which is > 0."},
            {"index": 1, "text": "Negative", "is_correct": False, "misconception_code": "C_UNSIGNED_UNDERFLOW", "misconception_name": "Unsigned Representation Fallacy", "explanation": "Assuming unsigned integers can evaluate to negative values in C."},
            {"index": 2, "text": "Compilation Error: unsigned underflow", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Unsigned wrap-around is defined behavior by the C standard, not a compilation error."},
            {"index": 3, "text": "Segmentation Fault", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Arithmetic does not trigger memory segmentation faults."}
        ],
        "explanation": "According to the C Standard (ISO/IEC 9899), unsigned integer arithmetic is defined to obey modulo 2^N arithmetic. Underflow does not produce a negative number; it wraps around to UINT_MAX."
    },
    {
        "concept_code": "C_DATA_TYPES",
        "difficulty": "intermediate",
        "title": "Character Arithmetic and ASCII Offset",
        "prompt": "What value is stored in the integer variable diff?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    char a = '8';\n    int diff = a - '0';\n    printf(\"%d\\n\", diff);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "8", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The ASCII encoding guarantees that digits '0' through '9' are contiguous; '8' - '0' evaluates to 8."},
            {"index": 1, "text": "56", "is_correct": False, "misconception_code": "C_ASCII_NUMERIC_LITERAL", "misconception_name": "ASCII Literal Confusion", "explanation": "Confusing the character code of '8' (56) with the evaluated subtraction result."},
            {"index": 2, "text": "0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Incorrect subtraction arithmetic."},
            {"index": 3, "text": "Compilation Error: cannot subtract chars", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "In C, chars are integral types and participate in arithmetic via integer promotion."}
        ],
        "explanation": "In C, characters are integer byte values. The standard guarantees that digits '0' through '9' are strictly sequential. Subtracting '0' from any character digit converts the ASCII character to its numerical integer value (56 - 48 = 8)."
    },

    # C_POINTERS (4 questions)
    {
        "concept_code": "C_POINTERS",
        "difficulty": "beginner",
        "title": "Address-Of (&) and Dereference (*) Semantics",
        "prompt": "What does this C code output to stdout?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    int val = 42;\n    int *ptr = &val;\n    *ptr = 100;\n    printf(\"%d %d\\n\", val, *ptr);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "100 100", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "ptr stores the memory address of val; dereferencing *ptr = 100 modifies the integer in that address directly."},
            {"index": 1, "text": "42 100", "is_correct": False, "misconception_code": "C_POINTER_COPY_FALLACY", "misconception_name": "Pointer Direct Value Shadowing", "explanation": "Believing ptr holds a copied value rather than pointing directly to val's memory."},
            {"index": 2, "text": "42 42", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The assignment *ptr = 100 successfully overwrote the memory location."},
            {"index": 3, "text": "Runtime Crash", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "ptr was properly initialized with &val before dereferencing."}
        ],
        "explanation": "A pointer variable holds the memory address of another variable. Modifying *ptr modifies the contents of the memory address assigned to val, updating both."
    },
    {
        "concept_code": "C_POINTERS",
        "difficulty": "intermediate",
        "title": "Uninitialized / Wild Pointer Dereference",
        "prompt": "What is the critical software vulnerability in the following function?",
        "code_snippet": "#include <stdio.h>\n\nvoid compute(void) {\n    int *ptr;\n    *ptr = 250;\n    printf(\"%d\\n\", *ptr);\n}",
        "options": [
            {"index": 0, "text": "Dereference of an uninitialized wild pointer causing undefined behavior or segmentation fault", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "ptr contains random stack garbage and points to an arbitrary or restricted memory address."},
            {"index": 1, "text": "Memory leak because ptr was not freed", "is_correct": False, "misconception_code": "C_MEMORY_LEAK_NO_FREE", "misconception_name": "Confusion Between Stack and Heap", "explanation": "ptr was never allocated with malloc(), so free() does not apply."},
            {"index": 2, "text": "Syntax error: int *ptr requires malloc()", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Pointers can point to stack variables; malloc is not syntactically required."},
            {"index": 3, "text": "The function returns void so *ptr cannot be printed", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Printing inside a void function is completely valid."}
        ],
        "explanation": "Declaring 'int *ptr;' creates a pointer with undefined stack garbage contents. Dereferencing '*ptr = 250;' attempts to write to an arbitrary address in memory, leading to memory corruption or an immediate segmentation fault (SIGSEGV)."
    },
    {
        "concept_code": "C_POINTERS",
        "difficulty": "advanced",
        "title": "Operator Precedence: *p++ vs (*p)++",
        "prompt": "What is printed by this pointer increment sequence?",
        "code_snippet": "#include <stdio.h>\n\nint main(void) {\n    int arr[] = {10, 20, 30};\n    int *p = arr;\n    int val = *p++;\n    printf(\"%d %d\\n\", val, *p);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "10 20", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "*p++ evaluates to *p (10), then increments the pointer p to point to the next element (20)."},
            {"index": 1, "text": "11 11", "is_correct": False, "misconception_code": "C_POINTER_INCREMENT_PRECEDENCE", "misconception_name": "Pointer Increment Precedence Error", "explanation": "Confused *p++ with (*p)++, which would increment the integer value rather than the pointer address."},
            {"index": 2, "text": "11 20", "is_correct": False, "misconception_code": "C_POINTER_INCREMENT_PRECEDENCE", "misconception_name": "Pointer Increment Precedence Error", "explanation": "Post-increment yields the original value before advancing."},
            {"index": 3, "text": "20 20", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "val captures the value before pointer advancement."}
        ],
        "explanation": "Postfix ++ has higher precedence than prefix *. Thus, *p++ is parsed as *(p++). The value of the sub-expression p++ is the original pointer p. Dereferencing yields 10 for val, and p is then incremented to point to arr[1], where *p equals 20."
    },
    {
        "concept_code": "C_POINTERS",
        "difficulty": "intermediate",
        "title": "Pass-by-Reference via Pointers",
        "prompt": "What will be the final value of x in main?",
        "code_snippet": "#include <stdio.h>\n\nvoid increment(int *n) {\n    (*n) += 5;\n}\n\nint main(void) {\n    int x = 15;\n    increment(&x);\n    printf(\"%d\\n\", x);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "20", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "&x passed the memory address of x, allowing increment() to mutate x directly."},
            {"index": 1, "text": "15", "is_correct": False, "misconception_code": "C_PASS_BY_VALUE_FALLACY", "misconception_name": "Pass-by-Value Confusion", "explanation": "Assuming C functions can never modify caller arguments even when passing addresses."},
            {"index": 2, "text": "5", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The operation is += 5, not = 5."},
            {"index": 3, "text": "Compilation Error", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Valid pointer syntax for pass-by-reference simulation in C."}
        ],
        "explanation": "While C is strictly pass-by-value, passing the address '&x' copies the address into pointer parameter n. The expression '(*n) += 5' dereferences the address and modifies the original variable x."
    },

    # C_ARRAYS_STRINGS (4 questions)
    {
        "concept_code": "C_ARRAYS_STRINGS",
        "difficulty": "beginner",
        "title": "Missing Null-Terminator in C String Literals",
        "prompt": "What is the minimum buffer size needed to store the string \"Hello\" safely?",
        "code_snippet": "char str[?] = \"Hello\";",
        "options": [
            {"index": 0, "text": "6 bytes (5 characters + 1 null terminator '\\0')", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "C strings require a terminating '\\0' byte to signal end-of-string to string handling functions."},
            {"index": 1, "text": "5 bytes", "is_correct": False, "misconception_code": "C_STRING_NULL_TERMINATOR", "misconception_name": "Missing Null Terminator in Strings", "explanation": "Forgot that C strings require an explicit '\\0' sentinel byte."},
            {"index": 2, "text": "4 bytes", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "4 bytes would truncate the string and omit the terminator."},
            {"index": 3, "text": "8 bytes", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "8 bytes is more than the minimum required (6)."}
        ],
        "explanation": "In C, strings are null-terminated byte arrays. The string \"Hello\" contains 5 printable characters ('H', 'e', 'l', 'l', 'o') plus the terminating null character '\\0', requiring at least 6 bytes of storage."
    },
    {
        "concept_code": "C_ARRAYS_STRINGS",
        "difficulty": "intermediate",
        "title": "Array Pointer Decay and sizeof",
        "prompt": "What does this function print for sizeof(arr)?",
        "code_snippet": "#include <stdio.h>\n\nvoid print_size(int arr[100]) {\n    printf(\"%zu\\n\", sizeof(arr));\n}\n\nint main(void) {\n    int data[100];\n    print_size(data);\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "Size of a pointer (e.g. 8 bytes on 64-bit systems)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Array arguments in C decay to a pointer (int *arr); sizeof(arr) evaluates the pointer size, not array capacity."},
            {"index": 1, "text": "400 bytes (100 * sizeof(int))", "is_correct": False, "misconception_code": "C_ARRAY_DECAY_FALLACY", "misconception_name": "Array Decay to Pointer Misconception", "explanation": "Assuming function parameter int arr[100] retains its array type rather than decaying to pointer."},
            {"index": 2, "text": "100 bytes", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Confusing array length with byte size."},
            {"index": 3, "text": "Compilation Error", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The syntax is valid C, though arr[100] is treated identically to *arr by the compiler."}
        ],
        "explanation": "In C function parameter lists, array syntax like 'int arr[100]' is syntactic sugar for 'int *arr'. The array decays into a pointer to its first element. Consequently, sizeof(arr) produces the size of the pointer (typically 8 bytes on modern 64-bit architectures), not 400 bytes."
    },
    {
        "concept_code": "C_ARRAYS_STRINGS",
        "difficulty": "advanced",
        "title": "Buffer Overflow via strcpy vs strncpy",
        "prompt": "Why is strcpy(dest, src) considered unsafe in C systems programming?",
        "code_snippet": "#include <string.h>\n\nvoid copy_data(char *src) {\n    char dest[16];\n    strcpy(dest, src); // Potential crash\n}",
        "options": [
            {"index": 0, "text": "strcpy does not check destination buffer boundaries and writes past 16 bytes if src is longer", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Causes stack buffer overflow, memory corruption, and potential arbitrary code execution vulnerabilities."},
            {"index": 1, "text": "strcpy always converts lowercase characters to uppercase", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "strcpy does not modify character case."},
            {"index": 2, "text": "dest must be allocated on the heap with malloc to use strcpy", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Stack buffers can receive copied strings if sized adequately."},
            {"index": 3, "text": "strcpy leaves the string un-terminated without a '\\0'", "is_correct": False, "misconception_code": "C_STRING_NULL_TERMINATOR", "misconception_name": "String Copy Boundary Confusion", "explanation": "strcpy DOES copy the '\\0', but fails to verify if dest has room for it."}
        ],
        "explanation": "strcpy copies bytes from src until it encounters a '\\0' byte. If src exceeds dest's capacity (16 bytes here), it writes beyond buffer boundaries onto the stack frame, overwriting the saved frame pointer and return address."
    },
    {
        "concept_code": "C_ARRAYS_STRINGS",
        "difficulty": "intermediate",
        "title": "Array Indexing via Pointer Arithmetic Equivalence",
        "prompt": "In C, which expression is strictly equivalent to arr[i]?",
        "code_snippet": "int val = arr[i];",
        "options": [
            {"index": 0, "text": "*(arr + i) and *(i + arr) and i[arr]", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Array indexing a[b] is defined by the standard as *((a) + (b)), which is commutative."},
            {"index": 1, "text": "*arr + i", "is_correct": False, "misconception_code": "C_POINTER_INCREMENT_PRECEDENCE", "misconception_name": "Dereference Precedence Confusion", "explanation": "*arr + i dereferences arr[0] and adds i to the integer value, not the pointer address."},
            {"index": 2, "text": "&arr[0] + i", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "This yields the pointer address &arr[i], not the value."},
            {"index": 3, "text": "arr + *i", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "i is an integer index, not a pointer."}
        ],
        "explanation": "In C, the subscript operator is defined as: E1[E2] is identical to (*((E1)+(E2))). Because addition is commutative, *(arr + i) is identical to *(i + arr) and i[arr]."
    },

    # C_MEMORY_MGMT (4 questions)
    {
        "concept_code": "C_MEMORY_MGMT",
        "difficulty": "beginner",
        "title": "Dynamic Allocation with malloc()",
        "prompt": "What does malloc() return if the operating system runs out of heap memory?",
        "code_snippet": "int *ptr = (int *)malloc(1000000000 * sizeof(int));",
        "options": [
            {"index": 0, "text": "NULL pointer (0)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "malloc returns NULL on allocation failure; software must always verify if (ptr == NULL)."},
            {"index": 1, "text": "An empty array of size 0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "malloc returns a pointer, never an array structure."},
            {"index": 2, "text": "Throws a MemoryAllocationException", "is_correct": False, "misconception_code": "C_EXCEPTION_HANDLING_FALLACY", "misconception_name": "Exception Handling Fallacy in C", "explanation": "C has no runtime exception throwing mechanisms like Java or Python."},
            {"index": 3, "text": "Terminates the program automatically with abort()", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "malloc does not terminate programs; it returns NULL to allow error handling."}
        ],
        "explanation": "If malloc cannot allocate the requested memory block, it returns a NULL pointer. In robust C programming, every dynamic allocation must be followed by a NULL-check before dereferencing."
    },
    {
        "concept_code": "C_MEMORY_MGMT",
        "difficulty": "intermediate",
        "title": "Memory Leak Identification",
        "prompt": "Identify the critical flaw in the following function:",
        "code_snippet": "#include <stdlib.h>\n\nvoid process(void) {\n    int *buf = malloc(1024 * sizeof(int));\n    buf[0] = 42;\n    // function completes and returns\n}",
        "options": [
            {"index": 0, "text": "Heap memory leak: buf is allocated on the heap but never released with free()", "is_correct": True, "misconception_code": "C_MEMORY_LEAK_NO_FREE", "misconception_name": "Heap Memory Leak from Missing free()", "explanation": "When process() returns, the pointer buf is destroyed from the stack, but the 4KB heap memory remains reserved forever."},
            {"index": 1, "text": "Segmentation fault at buf[0] = 42", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "buf points to valid allocated heap memory."},
            {"index": 2, "text": "buf is automatically garbage-collected at function exit", "is_correct": False, "misconception_code": "C_GARBAGE_COLLECTION_FALLACY", "misconception_name": "Garbage Collection Assumption in C", "explanation": "C has no automatic garbage collector; manual free() is mandatory."},
            {"index": 3, "text": "Missing cast (int *) before malloc", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "In standard C, void* converts implicitly to any pointer type without casting."}
        ],
        "explanation": "C does not have automatic garbage collection. Memory allocated on the heap with malloc() persists until explicitly freed with free(buf). Losing the pointer reference creates an irrecoverable memory leak."
    },
    {
        "concept_code": "C_MEMORY_MGMT",
        "difficulty": "advanced",
        "title": "Dangling Pointer after free()",
        "prompt": "What dangerous programming error is demonstrated here?",
        "code_snippet": "#include <stdlib.h>\n#include <stdio.h>\n\nint main(void) {\n    int *p = malloc(sizeof(int));\n    *p = 99;\n    free(p);\n    printf(\"%d\\n\", *p); // Line 8\n    return 0;\n}",
        "options": [
            {"index": 0, "text": "Use-After-Free: p is a dangling pointer pointing to deallocated memory", "is_correct": True, "misconception_code": "C_USE_AFTER_FREE", "misconception_name": "Use-After-Free Dereference", "explanation": "free(p) relinquishes ownership to the OS; dereferencing *p invokes undefined behavior."},
            {"index": 1, "text": "Double Free error", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "free() was only called once, not twice."},
            {"index": 2, "text": "Memory leak because p was freed before printing", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Memory was freed, so it is not a leak."},
            {"index": 3, "text": "Compiler Error on Line 8", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Compilers cannot easily detect use-after-free at compile time without static analysis."}
        ],
        "explanation": "Calling free(p) releases the allocated heap memory, but the pointer variable p still contains the old address (a dangling pointer). Dereferencing *p after free() is a Use-After-Free defect (CWE-416) leading to subtle bugs or security exploits. Best practice is to set p = NULL immediately after free(p)."
    },
    {
        "concept_code": "C_MEMORY_MGMT",
        "difficulty": "intermediate",
        "title": "calloc vs malloc Initialization",
        "prompt": "What is the primary difference between malloc(n * sizeof(int)) and calloc(n, sizeof(int))?",
        "code_snippet": "int *a = malloc(10 * sizeof(int));\nint *b = calloc(10, sizeof(int));",
        "options": [
            {"index": 0, "text": "calloc initializes all allocated bytes to zero; malloc leaves memory uninitialized with garbage bytes", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "calloc guarantees zero-initialization; malloc allocates faster without wiping existing memory contents."},
            {"index": 1, "text": "malloc allocates on the heap while calloc allocates on the stack", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Both allocate exclusively from heap memory."},
            {"index": 2, "text": "calloc cannot be freed with free()", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Memory from both calloc and malloc must be released with free()."},
            {"index": 3, "text": "malloc is only for characters while calloc is for integers", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Both allocate raw bytes agnostic to data types."}
        ],
        "explanation": "malloc(size) allocates raw bytes from the heap without clearing them; memory contents remain indeterminate. calloc(num, size) allocates the block and explicitly zeroes out every single byte."
    }
]

# ==========================================
# 6. MATHEMATICS QUESTIONS
# ==========================================
MATH_QUESTIONS = [
    # MATH_LIMITS (4 questions)
    {
        "concept_code": "MATH_LIMITS",
        "difficulty": "beginner",
        "title": "Evaluating Limits of Rational Functions (0/0)",
        "prompt": "Evaluate the limit as x approaches 2 of f(x) = (x^2 - 4) / (x - 2):",
        "code_snippet": "\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}",
        "options": [
            {"index": 0, "text": "4", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Factor (x^2 - 4) as (x - 2)(x + 2). Cancel (x - 2) for x != 2, leaving lim (x + 2) = 4."},
            {"index": 1, "text": "Does Not Exist / Undefined", "is_correct": False, "misconception_code": "MATH_LIMIT_DIRECT_SUB_ZERO", "misconception_name": "Direct Substitution into Indeterminate Forms", "explanation": "Direct substitution gives 0/0, which is indeterminate, not undefined."},
            {"index": 2, "text": "0", "is_correct": False, "misconception_code": "MATH_LIMIT_DIRECT_SUB_ZERO", "misconception_name": "Zero Numerator Assumption", "explanation": "Believing a numerator of 0 forces the limit to 0 without factoring the matching denominator."},
            {"index": 3, "text": "2", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Incorrect algebraic evaluation."}
        ],
        "explanation": "Direct substitution yields 0/0, which is an indeterminate form. By factoring the numerator: (x^2 - 4) = (x - 2)(x + 2). For all x != 2, (x^2 - 4)/(x - 2) = x + 2. Taking the limit as x -> 2 gives 2 + 2 = 4."
    },
    {
        "concept_code": "MATH_LIMITS",
        "difficulty": "intermediate",
        "title": "Trigonometric Limit lim (sin x) / x as x -> 0",
        "prompt": "Evaluate the fundamental trigonometric limit as x approaches 0:",
        "code_snippet": "\\lim_{x \\to 0} \\frac{\\sin(3x)}{x}",
        "options": [
            {"index": 0, "text": "3", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Rewrite as 3 * lim_{x->0} (sin(3x) / (3x)) = 3 * 1 = 3."},
            {"index": 1, "text": "1", "is_correct": False, "misconception_code": "MATH_TRIG_LIMIT_COEFF", "misconception_name": "Trigonometric Coefficient Omission", "explanation": "Ignoring the argument scaling factor 3 in sin(3x)."},
            {"index": 2, "text": "0", "is_correct": False, "misconception_code": "MATH_LIMIT_DIRECT_SUB_ZERO", "misconception_name": "Direct Substitution into Indeterminate Forms", "explanation": "Assuming sin(0)/0 = 0/0 means the limit is 0."},
            {"index": 3, "text": "Undefined", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The limit exists and equals 3."}
        ],
        "explanation": "Since lim_{u -> 0} (sin u / u) = 1, we multiply numerator and denominator by 3: lim_{x -> 0} 3 * (sin(3x) / 3x) = 3 * 1 = 3 (or alternatively via L'Hopital's rule: lim 3 cos(3x) / 1 = 3)."
    },
    {
        "concept_code": "MATH_LIMITS",
        "difficulty": "advanced",
        "title": "Limits at Infinity of Rational Polynomials",
        "prompt": "Determine the horizontal asymptote limit as x approaches positive infinity:",
        "code_snippet": "\\lim_{x \\to \\infty} \\frac{5x^3 - 2x + 7}{2x^3 + 9x^2 - 1}",
        "options": [
            {"index": 0, "text": "5/2 (or 2.5)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Since degrees of numerator and denominator are equal (degree 3), the limit is the ratio of leading coefficients: 5/2."},
            {"index": 1, "text": "Infinity", "is_correct": False, "misconception_code": "MATH_INFINITY_DOMINANCE", "misconception_name": "Infinite Dominance Fallacy", "explanation": "Assuming any polynomial ratio with infinity in numerator goes to infinity."},
            {"index": 2, "text": "0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The degrees are equal, so the limit is non-zero."},
            {"index": 3, "text": "7 / -1 = -7", "is_correct": False, "misconception_code": "MATH_CONSTANT_TERM_CONFUSION", "misconception_name": "Constant Term Dominance Fallacy", "explanation": "Dividing constant terms instead of leading degree terms."}
        ],
        "explanation": "Divide every term in both numerator and denominator by x^3: lim (5 - 2/x^2 + 7/x^3) / (2 + 9/x - 1/x^3). As x -> inf, all terms with x in denominator approach 0, leaving 5/2."
    },
    {
        "concept_code": "MATH_LIMITS",
        "difficulty": "intermediate",
        "title": "Continuous Function Criteria at a Point",
        "prompt": "Which three conditions must ALL hold for a function f(x) to be continuous at x = c?",
        "code_snippet": "f(x) \\text{ is continuous at } x = c",
        "options": [
            {"index": 0, "text": "1) f(c) is defined; 2) lim_{x->c} f(x) exists; 3) lim_{x->c} f(x) = f(c)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Formal Cauchy definition of continuity at a real point c."},
            {"index": 1, "text": "1) f'(c) exists; 2) f''(c) exists", "is_correct": False, "misconception_code": "MATH_DIFFERENTIABILITY_CONTINUITY", "misconception_name": "Confusing Differentiability with Continuity", "explanation": "Differentiability implies continuity, but continuity does not require derivatives to exist (e.g. |x| at 0)."},
            {"index": 2, "text": "f(c) > 0 and lim_{x->c} f(x) > 0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Continuity has no sign requirement; functions can be negative and continuous."},
            {"index": 3, "text": "lim_{x->c+} f(x) = lim_{x->c-} f(x) alone", "is_correct": False, "misconception_code": "MATH_LIMIT_EXISTENCE_ALONE", "misconception_name": "Removable Discontinuity Confusion", "explanation": "Equal one-sided limits prove the limit exists, but f(c) might be undefined or unequal (removable hole)."}
        ],
        "explanation": "By definition, f(x) is continuous at x = c if and only if: 1) f(c) exists (the function is defined at c); 2) lim_{x->c} f(x) exists (left and right limits are equal); 3) lim_{x->c} f(x) = f(c)."
    },

    # MATH_DERIVATIVES (4 questions)
    {
        "concept_code": "MATH_DERIVATIVES",
        "difficulty": "beginner",
        "title": "Power Rule vs Exponential Derivative",
        "prompt": "What is the derivative with respect to x of f(x) = 3^x?",
        "code_snippet": "\\frac{d}{dx} \\left( 3^x \\right)",
        "options": [
            {"index": 0, "text": "3^x * ln(3)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "For an exponential function a^x where a > 0, d/dx(a^x) = a^x * ln(a)."},
            {"index": 1, "text": "x * 3^(x - 1)", "is_correct": False, "misconception_code": "MATH_POWER_RULE_EXPONENT", "misconception_name": "Power Rule Misapplication to Exponential Functions", "explanation": "Applied power rule d/dx(x^n) = n*x^(n-1) to an exponential function where x is in the exponent."},
            {"index": 2, "text": "3^x", "is_correct": False, "misconception_code": "MATH_NATURAL_EXPONENT_CONFUSION", "misconception_name": "e^x Derivative Confusion", "explanation": "Only e^x has derivative e^x (since ln(e) = 1). Base 3 requires multiplication by ln(3)."},
            {"index": 3, "text": "3^(x - 1)", "is_correct": False, "misconception_code": "MATH_POWER_RULE_EXPONENT", "misconception_name": "Power Rule Exponent Error", "explanation": "Decremented the exponent without multiplying by the base or natural log."}
        ],
        "explanation": "The power rule d/dx(x^n) = n*x^(n-1) ONLY applies when the variable x is in the BASE. When x is in the EXPONENT (a^x), the derivative is d/dx(a^x) = a^x * ln(a)."
    },
    {
        "concept_code": "MATH_DERIVATIVES",
        "difficulty": "intermediate",
        "title": "Composite Function Chain Rule",
        "prompt": "Find the derivative with respect to x of f(x) = sin(x^3 + 2x):",
        "code_snippet": "\\frac{d}{dx} \\left[ \\sin(x^3 + 2x) \\right]",
        "options": [
            {"index": 0, "text": "(3x^2 + 2) * cos(x^3 + 2x)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "By Chain Rule: d/dx[f(g(x))] = f'(g(x)) * g'(x), where outer derivative is cos(u) and inner is 3x^2 + 2."},
            {"index": 1, "text": "cos(x^3 + 2x)", "is_correct": False, "misconception_code": "MATH_CHAIN_RULE_OMISSION", "misconception_name": "Chain Rule Inner Derivative Omission", "explanation": "Differentiated the outer sine function but completely omitted multiplying by the inner derivative (3x^2 + 2)."},
            {"index": 2, "text": "(3x^2 + 2) * cos(3x^2 + 2)", "is_correct": False, "misconception_code": "MATH_CHAIN_ARGUMENT_TAMPERING", "misconception_name": "Inner Function Replacement Fallacy", "explanation": "Replaced the argument inside cosine with the derivative instead of preserving g(x)."},
            {"index": 3, "text": "-cos(x^3 + 2x) * (3x^2 + 2)", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The derivative of sin(u) is +cos(u), not -cos(u)."}
        ],
        "explanation": "By the Chain Rule, d/dx[f(g(x))] = f'(g(x)) * g'(x). Here, outer function f(u) = sin(u) with derivative cos(u), and inner function g(x) = x^3 + 2x with derivative 3x^2 + 2. Multiplying gives (3x^2 + 2) * cos(x^3 + 2x)."
    },
    {
        "concept_code": "MATH_DERIVATIVES",
        "difficulty": "advanced",
        "title": "Product Rule Combined with Exponential",
        "prompt": "Compute the derivative of f(x) = x^2 * e^(3x):",
        "code_snippet": "\\frac{d}{dx} \\left[ x^2 e^{3x} \\right]",
        "options": [
            {"index": 0, "text": "e^(3x) * (3x^2 + 2x) or x * e^(3x) * (3x + 2)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Product rule: u'*v + u*v' = 2x * e^(3x) + x^2 * 3e^(3x) = e^(3x)(3x^2 + 2x)."},
            {"index": 1, "text": "2x * 3e^(3x) = 6x * e^(3x)", "is_correct": False, "misconception_code": "MATH_PRODUCT_RULE_FALLACY", "misconception_name": "Product Rule Multiplication Fallacy", "explanation": "Multiplied individual derivatives (u' * v') instead of applying the product rule u'v + uv'."},
            {"index": 2, "text": "2x * e^(3x)", "is_correct": False, "misconception_code": "MATH_CHAIN_RULE_OMISSION", "misconception_name": "Omission of Second Product Term", "explanation": "Differentiated only x^2 while treating e^(3x) as a constant."},
            {"index": 3, "text": "3x^2 * e^(3x)", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Omitted derivative of first factor x^2."}
        ],
        "explanation": "Using the Product Rule d/dx(u*v) = u'*v + u*v': let u = x^2 (so u' = 2x) and v = e^(3x) (so v' = 3e^(3x)). Then f'(x) = 2x*e^(3x) + x^2*3e^(3x) = e^(3x)(3x^2 + 2x)."
    },
    {
        "concept_code": "MATH_DERIVATIVES",
        "difficulty": "intermediate",
        "title": "Implicit Differentiation on a Circle",
        "prompt": "Find dy/dx for the unit circle x^2 + y^2 = 25 at the point (3, 4):",
        "code_snippet": "x^2 + y^2 = 25 \\implies \\frac{dy}{dx} = ?",
        "options": [
            {"index": 0, "text": "-3/4 (or -0.75)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "2x + 2y(dy/dx) = 0 => dy/dx = -x/y = -3/4."},
            {"index": 1, "text": "-4/3", "is_correct": False, "misconception_code": "MATH_SLOPE_RECIPROCAL_INVERSION", "misconception_name": "Reciprocal Slope Inversion Fallacy", "explanation": "Inverted -x/y to -y/x."},
            {"index": 2, "text": "+3/4", "is_correct": False, "misconception_code": "MATH_SIGN_ERROR_ALGEBRAIC", "misconception_name": "Algebraic Sign Error", "explanation": "Lost the negative sign when subtracting 2x to the right-hand side."},
            {"index": 3, "text": "0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Tangent slope is non-zero at (3, 4)."}
        ],
        "explanation": "Differentiate implicitly with respect to x: d/dx(x^2) + d/dx(y^2) = d/dx(25) => 2x + 2y*(dy/dx) = 0. Solving gives dy/dx = -2x / (2y) = -x / y. Evaluating at (3, 4) yields -3/4."
    },

    # MATH_MATRICES (4 questions)
    {
        "concept_code": "MATH_MATRICES",
        "difficulty": "beginner",
        "title": "Matrix Multiplication Commutativity",
        "prompt": "Given two square matrices A and B of order 3x3, which statement is true in general?",
        "code_snippet": "A, B \\in \\mathbb{R}^{3 \\times 3}",
        "options": [
            {"index": 0, "text": "AB != BA in general (matrix multiplication is non-commutative)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Matrix multiplication depends on order; AB and BA yield entirely different matrices in general."},
            {"index": 1, "text": "AB = BA always, exactly like real numbers", "is_correct": False, "misconception_code": "MATH_MATRIX_COMMUTATIVITY", "misconception_name": "Matrix Multiplication Commutativity Fallacy", "explanation": "Assumed scalar arithmetic commutativity extends to matrix linear transformations."},
            {"index": 2, "text": "AB is defined, but BA is undefined", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "For square 3x3 matrices, both AB and BA are always defined, though not equal."},
            {"index": 3, "text": "AB is always the zero matrix", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Product of non-zero matrices is generally non-zero."}
        ],
        "explanation": "Unlike scalar arithmetic, matrix multiplication is non-commutative: in general AB != BA. A simple 2x2 counter-example: A = [[0,1],[0,0]], B = [[0,0],[1,0]]. AB = [[1,0],[0,0]], while BA = [[0,0],[0,1]]."
    },
    {
        "concept_code": "MATH_MATRICES",
        "difficulty": "intermediate",
        "title": "Determinant and Invertibility Condition",
        "prompt": "A square matrix A is invertible (non-singular) if and only if:",
        "code_snippet": "A^{-1} \\text{ exists} \\iff ?",
        "options": [
            {"index": 0, "text": "det(A) != 0", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "A square matrix is invertible if and only if its determinant is non-zero."},
            {"index": 1, "text": "det(A) = 0", "is_correct": False, "misconception_code": "MATH_ZERO_DETERMINANT_INVERT", "misconception_name": "Singular Matrix Invertibility Confusion", "explanation": "Believed det(A) = 0 allows inversion; in fact det(A) = 0 means the matrix is singular (no inverse)."},
            {"index": 2, "text": "trace(A) > 0", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Trace has no direct bearing on invertibility."},
            {"index": 3, "text": "All diagonal entries are non-zero", "is_correct": False, "misconception_code": "MATH_DIAGONAL_INVERT_FALLACY", "misconception_name": "Diagonal Entry Invertibility Fallacy", "explanation": "A matrix can have non-zero diagonals and still have determinant 0 (e.g. [[1,1],[1,1]])."}
        ],
        "explanation": "By the Invertible Matrix Theorem, A^-1 = (1 / det(A)) * adj(A). If det(A) = 0, division by zero occurs, the columns of A are linearly dependent, and A has no inverse (it is singular)."
    },
    {
        "concept_code": "MATH_MATRICES",
        "difficulty": "advanced",
        "title": "2x2 Matrix Determinant Calculation",
        "prompt": "Calculate the determinant of matrix M = [[3, 5], [2, 4]]:",
        "code_snippet": "M = \\begin{pmatrix} 3 & 5 \\\\ 2 & 4 \\end{pmatrix} \\implies \\det(M) = ?",
        "options": [
            {"index": 0, "text": "2", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "det = ad - bc = (3)(4) - (5)(2) = 12 - 10 = 2."},
            {"index": 1, "text": "22", "is_correct": False, "misconception_code": "MATH_DETERMINANT_SIGN_ADDITION", "misconception_name": "Determinant Formula Addition Fallacy", "explanation": "Added the off-diagonal product ad + bc = 12 + 10 = 22 instead of subtracting."},
            {"index": 2, "text": "-2", "is_correct": False, "misconception_code": "MATH_DETERMINANT_DIAGONAL_SWAP", "misconception_name": "Diagonal Order Swap", "explanation": "Subtracted ad from bc: 10 - 12 = -2."},
            {"index": 3, "text": "14", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Arithmetic calculation mistake."}
        ],
        "explanation": "For a 2x2 matrix [[a, b], [c, d]], the determinant is given by ad - bc. Here: (3 * 4) - (5 * 2) = 12 - 10 = 2."
    },
    {
        "concept_code": "MATH_MATRICES",
        "difficulty": "intermediate",
        "title": "Matrix Transpose Properties",
        "prompt": "For any two conformable matrices A and B, what is the transpose of their product (AB)^T?",
        "code_snippet": "(AB)^T = ?",
        "options": [
            {"index": 0, "text": "B^T * A^T (order reverses)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "None", "explanation": "The transpose of a matrix product reverses the order of factors: (AB)^T = B^T A^T."},
            {"index": 1, "text": "A^T * B^T", "is_correct": False, "misconception_code": "MATH_TRANSPOSE_ORDER_RETENTION", "misconception_name": "Transpose Order Retention Fallacy", "explanation": "Failed to reverse the factor order; A^T B^T might not even have compatible dimensions."},
            {"index": 2, "text": "A^T + B^T", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Multiplication does not turn into addition upon transposition."},
            {"index": 3, "text": "-(AB)", "is_correct": False, "misconception_code": "NONE", "misconception_name": "None", "explanation": "Transposition changes rows to columns, not numerical signs."}
        ],
        "explanation": "By linear algebra properties, (AB)^T = B^T * A^T. Notice that if A is m x n and B is n x p, AB is m x p, and (AB)^T is p x m. B^T is p x n and A^T is n x m, so B^T * A^T is valid with dimensions p x m."
    }
]

# ==========================================
# 7. C PROGRAMMING LESSONS
# ==========================================
C_LESSONS = [
    {
        "concept_code": "C_DATA_TYPES",
        "title": "C Primitive Data Types, Memory Representation & Format Specifiers",
        "summary": "Master fundamental C types (int, char, float, double), architecture byte widths, integer division truncation, and printf format specifiers.",
        "reading_time_min": 7,
        "introduction": "Unlike high-level dynamically typed languages, C provides direct mappings to machine hardware words. Variables occupy fixed contiguous memory bytes, and operators execute machine-level instructions with strict typing semantics.",
        "learning_objectives": [
            "Understand byte widths and limits of char, int, float, and double.",
            "Predict and prevent integer division truncation errors.",
            "Use sizeof operator safely without unintended runtime side effects.",
            "Correctly match printf/scanf format specifiers (%d, %c, %f, %zu, %p)."
        ],
        "detailed_explanation": """
### 1. Integer Types and Architecture Byte Widths
In C, the size of data types depends on the compiler and target architecture (e.g. 32-bit vs 64-bit systems):
- `char`: Guaranteed to be 1 byte (typically 8 bits, holding ASCII values -128 to 127 or 0 to 255).
- `short`: At least 16 bits (2 bytes).
- `int`: At least 16 bits, standardly 32 bits (4 bytes) on modern x86/ARM CPUs.
- `long`: 32 bits on 32-bit OS / 64-bit Windows, 64 bits on 64-bit Linux/macOS.
- `long long`: At least 64 bits (8 bytes).

### 2. The Integer Division Trap
When both operands of `/` are integer types, C performs integer division: the fractional part is truncated toward zero:
```c
int a = 7, b = 2;
float x = a / b; // Evaluates to 3.00, NOT 3.50!
```
To obtain floating-point precision, cast at least one operand: `float x = (float)a / b;`.

### 3. sizeof Compile-Time Operator
`sizeof` is a compile-time operator that returns the memory width of an object or type in bytes (`size_t`):
```c
int i = 5;
sizeof(i++); // i++ is NOT evaluated! i remains 5!
```
""",
        "code_examples": [
            {
                "title": "Type Casting and Division Demonstration",
                "code": "#include <stdio.h>\n\nint main(void) {\n    int a = 9, b = 4;\n    float trunc = a / b;\n    float exact = (float)a / b;\n    printf(\"Truncated: %.2f\\n\", trunc);\n    printf(\"Exact: %.2f\\n\", exact);\n    return 0;\n}",
                "output": "Truncated: 2.00\nExact: 2.25",
                "notes": "(float)a / b promotes the division to single-precision IEEE 754 float before division."
            }
        ],
        "common_mistakes": [
            {
                "title": "Integer Division Truncation",
                "wrong_code": "float avg = (score1 + score2) / 2;",
                "correct_code": "float avg = (score1 + score2) / 2.0f;",
                "misconception_code": "C_INTEGER_DIVISION_TRUNC",
                "explanation": "Dividing by integer 2 truncates the sum's half-point before storing into avg. Use 2.0f."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a C expression that calculates the percentage (0 to 100) of correct answers given 'int correct = 17;' and 'int total = 20;'.",
                "hint": "Ensure total is cast to float before dividing, then multiply by 100.0f.",
                "solution": "float pct = ((float)correct / total) * 100.0f;"
            }
        ],
        "order_index": 1
    },
    {
        "concept_code": "C_POINTERS",
        "title": "Pointers, Memory Addresses, and Indirection in C",
        "summary": "Understand pointers as memory address variables, dereferencing (*), address-of (&), pass-by-reference, and pointer arithmetic.",
        "reading_time_min": 9,
        "introduction": "A pointer is a variable whose value is the physical or virtual memory address of another variable. Direct memory access gives C its exceptional efficiency and systems-level control, but requires disciplined address management.",
        "learning_objectives": [
            "Declare, initialize, and dereference pointer variables safely.",
            "Distinguish between a pointer's value (an address) and the target value at that address.",
            "Implement pass-by-reference semantics using pointer arguments in functions.",
            "Understand operator precedence in expressions like *p++ vs (*p)++."
        ],
        "detailed_explanation": """
### 1. Pointer Fundamentals
Every variable in C resides at a unique byte location in memory:
- `&x` (address-of operator): Retrieves the hexadecimal memory address of variable `x`.
- `int *ptr = &x`: Declares `ptr` as a pointer to an `int` and stores `&x`.
- `*ptr` (dereference operator): Accesses or modifies the value stored at that address.

### 2. Wild / Uninitialized Pointers
A pointer declared without an initial value holds random stack garbage:
```c
int *p; // Wild pointer! Points to an unknown memory address!
*p = 50; // Undefined behavior! May overwrite critical memory or trigger SIGSEGV!
```
Always initialize pointers to `NULL` or a valid memory address: `int *p = NULL;`.

### 3. Operator Precedence: *p++ vs (*p)++
- `*p++`: Postfix `++` has higher precedence than `*`. It evaluates to `*p`, and then increments pointer `p` to the next memory address.
- `(*p)++`: Parentheses force dereferencing first; it increments the integer value stored at address `p`.
""",
        "code_examples": [
            {
                "title": "Swapping Two Variables with Pointers",
                "code": "#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}\n\nint main(void) {\n    int x = 10, y = 20;\n    swap(&x, &y);\n    printf(\"x = %d, y = %d\\n\", x, y);\n    return 0;\n}",
                "output": "x = 20, y = 10",
                "notes": "Passing addresses &x and &y allows swap() to directly modify the caller's stack frame variables."
            }
        ],
        "common_mistakes": [
            {
                "title": "Dereferencing Uninitialized Pointer",
                "wrong_code": "int *ptr;\n*ptr = 100;",
                "correct_code": "int val = 0;\nint *ptr = &val;\n*ptr = 100;",
                "misconception_code": "C_WILD_POINTER_DEREF",
                "explanation": "Never dereference a pointer before initializing it with a valid memory address."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a function 'void double_val(int *p)' that doubles the integer value stored at the address pointed to by p.",
                "hint": "Dereference p using *p, and multiply by 2.",
                "solution": "void double_val(int *p) {\n    if (p != NULL) {\n        *p *= 2;\n    }\n}"
            }
        ],
        "order_index": 2
    },
    {
        "concept_code": "C_ARRAYS_STRINGS",
        "title": "C Arrays, Pointer Decay & Null-Terminated Strings",
        "summary": "Master array memory continuity, array-to-pointer decay in function calls, null terminator '\\0', and bounds safety.",
        "reading_time_min": 8,
        "introduction": "In C, arrays are contiguous blocks of memory where elements of the same type are arranged sequentially. Strings are simply character arrays terminating with a null character ('\\0').",
        "learning_objectives": [
            "Explain how arrays decay to pointers in expressions and function arguments.",
            "Understand why C does NOT perform automatic bounds checking.",
            "Safely allocate and manipulate null-terminated string buffers.",
            "Use standard library string functions (strlen, strncpy, snprintf) securely."
        ],
        "detailed_explanation": """
### 1. Array Memory Layout and Pointer Decay
When an array name `arr` is used in most expressions, it automatically decays to a pointer to its first element: `&arr[0]`.
```c
int arr[5] = {10, 20, 30, 40, 50};
// arr[i] is literally defined as *(arr + i)
```
Inside a function signature like `void process(int arr[])`, `arr` is strictly an `int *` pointer.

### 2. The Null Terminator '\\0'
C strings are character arrays where the byte value `0` (ASCII `'\\0'`) indicates the end:
```c
char greeting[6] = "Hello"; // 5 letters + 1 '\\0' = 6 bytes
```
If you forget the null terminator, functions like `strlen()` and `printf(\"%s\")` continue reading through adjacent memory until they encounter a random zero byte.
""",
        "code_examples": [
            {
                "title": "String Traversal with Pointer Arithmetic",
                "code": "#include <stdio.h>\n\nint main(void) {\n    char msg[] = \"LearnSphere\";\n    char *p = msg;\n    int count = 0;\n    while (*p != '\\0') {\n        count++;\n        p++;\n    }\n    printf(\"Length: %d\\n\", count);\n    return 0;\n}",
                "output": "Length: 11",
                "notes": "Iterating until *p == '\\0' is the standard C idiomatic pattern for string inspection."
            }
        ],
        "common_mistakes": [
            {
                "title": "Buffer Too Small for Null Terminator",
                "wrong_code": "char buf[5] = \"Hello\"; // Missing 1 byte for '\\0'!",
                "correct_code": "char buf[6] = \"Hello\"; // Room for 'H','e','l','l','o','\\0'",
                "misconception_code": "C_STRING_NULL_TERMINATOR",
                "explanation": "A string of length N requires N + 1 bytes of buffer allocation to hold '\\0'."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Why does 'sizeof(arr)' inside 'void test(int arr[10])' return 8 on a 64-bit machine instead of 40?",
                "hint": "Remember that array parameters decay to pointers in function signatures.",
                "solution": "In C function parameter lists, 'int arr[10]' decays to a pointer 'int *arr'. sizeof(arr) evaluates the pointer size (8 bytes on 64-bit systems), not the original array."
            }
        ],
        "order_index": 3
    },
    {
        "concept_code": "C_MEMORY_MGMT",
        "title": "Dynamic Heap Memory Management in C (malloc, calloc, free)",
        "summary": "Master heap allocation, memory lifetime, preventing memory leaks, and avoiding Use-After-Free vulnerabilities.",
        "reading_time_min": 9,
        "introduction": "Stack memory is automatically managed but limited in size and scope. The heap allows C programs to allocate arbitrarily large dynamic data structures that outlive the creating function frame.",
        "learning_objectives": [
            "Allocate heap memory using malloc(), calloc(), and realloc().",
            "Verify allocation success by checking for NULL pointers.",
            "Prevent memory leaks by calling free() for every allocated block.",
            "Avoid Dangling Pointers and Use-After-Free security vulnerabilities."
        ],
        "detailed_explanation": """
### 1. Dynamic Allocation Functions
- `malloc(size_t bytes)`: Allocates uninitialized heap memory.
- `calloc(size_t num, size_t size)`: Allocates and clears every byte to `0`.
- `realloc(void *ptr, size_t new_size)`: Resizes an existing heap block.
- `free(void *ptr)`: Returns heap memory back to the operating system.

### 2. Golden Rules of Heap Memory in C
1. Always check for `NULL`: If the OS cannot grant memory, `malloc()` returns `NULL`.
2. Every `malloc()` must have a matching `free()`: Failing to free causes memory leaks.
3. Never dereference a freed pointer: After `free(p);`, `p` is a dangling pointer. Set `p = NULL;` immediately!
""",
        "code_examples": [
            {
                "title": "Safe Heap Allocation and Deallocation",
                "code": "#include <stdio.h>\n#include <stdlib.h>\n\nint main(void) {\n    int n = 5;\n    int *arr = (int *)malloc(n * sizeof(int));\n    if (arr == NULL) {\n        fprintf(stderr, \"Allocation failed!\\n\");\n        return 1;\n    }\n    for (int i = 0; i < n; i++) {\n        arr[i] = (i + 1) * 10;\n    }\n    printf(\"First: %d, Last: %d\\n\", arr[0], arr[n - 1]);\n    free(arr);\n    arr = NULL; // Prevent dangling pointer\n    return 0;\n}",
                "output": "First: 10, Last: 50",
                "notes": "Always verify if (arr == NULL) and set arr = NULL after free(arr)."
            }
        ],
        "common_mistakes": [
            {
                "title": "Use-After-Free Defect",
                "wrong_code": "free(ptr);\nprintf(\"%d\", *ptr); // Dangling pointer!",
                "correct_code": "free(ptr);\nptr = NULL; // Safe defensive pattern",
                "misconception_code": "C_USE_AFTER_FREE",
                "explanation": "Dereferencing a pointer after freeing it accesses deallocated memory and causes crashes or security vulnerabilities."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a snippet that dynamically allocates an array of 50 floats and initializes them all to 0.0.",
                "hint": "Use calloc(50, sizeof(float)).",
                "solution": "float *data = (float *)calloc(50, sizeof(float));\nif (data != NULL) {\n    // Use data...\n    free(data);\n    data = NULL;\n}"
            }
        ],
        "order_index": 4
    }
]

# ==========================================
# 8. MATHEMATICS LESSONS
# ==========================================
MATH_LESSONS = [
    {
        "concept_code": "MATH_LIMITS",
        "title": "Limits, Continuity, and Indeterminate Forms in Calculus",
        "summary": "Master the rigorous definition of limits, one-sided limits, continuity criteria, factoring techniques, and resolving indeterminate forms (0/0).",
        "reading_time_min": 8,
        "introduction": "Calculus begins with the concept of a limit: understanding the behavior of a function as its input approaches a target value, even if the function is not defined at that exact point.",
        "learning_objectives": [
            "Evaluate limits algebraically using factoring and rationalization.",
            "Understand why 0/0 is an indeterminate form, not an undefined result.",
            "Apply the three formal continuity conditions to piecewise functions.",
            "Determine horizontal asymptotes by evaluating limits at infinity."
        ],
        "detailed_explanation": """
### 1. Intuition and Definition of Limits
The notation $\\lim_{x \\to c} f(x) = L$ means that as $x$ gets arbitrarily close to $c$ (from both left and right), $f(x)$ approaches $L$.
Crucially, $f(c)$ does NOT have to equal $L$, and $f(c)$ does not even have to exist!

### 2. Resolving Indeterminate Form 0/0
When evaluating $\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}$, direct substitution yields $\\frac{0}{0}$. This is called an **indeterminate form**: it provides no information about the limit's existence or value.
We resolve it algebraically by factoring:
$$\\frac{x^2 - 4}{x - 2} = \\frac{(x - 2)(x + 2)}{x - 2} = x + 2 \\quad (\\text{for } x \\neq 2)$$
$$\\lim_{x \\to 2} (x + 2) = 4$$

### 3. The Three Conditions for Continuity
A function $f(x)$ is continuous at $x = c$ if and only if:
1. $f(c)$ is defined.
2. $\\lim_{x \\to c} f(x)$ exists (meaning $\\lim_{x \\to c^-} f(x) = \\lim_{x \\to c^+} f(x)$).
3. $\\lim_{x \\to c} f(x) = f(c)$.
""",
        "code_examples": [
            {
                "title": "Factoring to Resolve Indeterminate Form",
                "code": "# SymPy Analytical Verification\nimport sympy as sp\nx = sp.Symbol('x')\nf = (x**2 - 4) / (x - 2)\nlimit_val = sp.limit(f, x, 2)\nprint('Limit as x -> 2:', limit_val)",
                "output": "Limit as x -> 2: 4",
                "notes": "Both analytical factoring and computer algebra confirm the limit is 4."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming 0/0 is Undefined or Zero",
                "wrong_code": "lim (x^2 - 4)/(x - 2) = 0/0 = Undefined",
                "correct_code": "lim (x - 2)(x + 2)/(x - 2) = lim (x + 2) = 4",
                "misconception_code": "MATH_LIMIT_DIRECT_SUB_ZERO",
                "explanation": "0/0 indicates the presence of a common factor that must be canceled before evaluating."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Evaluate the limit as x approaches 3 of (x^2 - 9) / (x - 3).",
                "hint": "Factor the numerator as difference of squares: (x - 3)(x + 3).",
                "solution": "Factor (x - 3)(x + 3) / (x - 3) = x + 3. As x -> 3, limit is 3 + 3 = 6."
            }
        ],
        "order_index": 1
    },
    {
        "concept_code": "MATH_DERIVATIVES",
        "title": "Differential Calculus, Derivative Rules, and the Chain Rule",
        "summary": "Master instantaneous rates of change, the power rule, product rule, quotient rule, and the composite chain rule.",
        "reading_time_min": 9,
        "introduction": "The derivative represents the instantaneous rate of change of a function with respect to its independent variable, geometrically corresponding to the slope of the tangent line to the curve at any given point.",
        "learning_objectives": [
            "Compute derivatives using power, exponential, and trigonometric rules.",
            "Apply the product rule: [u*v]' = u'v + uv'.",
            "Differentiate composite functions f(g(x)) using the Chain Rule.",
            "Distinguish between power functions (x^n) and exponential functions (a^x)."
        ],
        "detailed_explanation": """
### 1. Fundamental Rules of Differentiation
- **Power Rule**: $\\frac{d}{dx}[x^n] = n x^{n-1}$ (for variable in the base).
- **Exponential Rule**: $\\frac{d}{dx}[a^x] = a^x \\ln(a)$ (for constant base $a > 0$). When $a = e$, $\\frac{d}{dx}[e^x] = e^x$.
- **Trigonometric Rules**: $\\frac{d}{dx}[\\sin x] = \\cos x$, $\\frac{d}{dx}[\\cos x] = -\\sin x$.

### 2. The Chain Rule for Composite Functions
When a function is nested inside another, $y = f(g(x))$, the derivative is:
$$\\frac{dy}{dx} = f'(g(x)) \\cdot g'(x)$$
Example: For $y = \\sin(x^3)$:
- Outer function: $f(u) = \\sin(u) \\implies f'(u) = \\cos(u)$
- Inner function: $g(x) = x^3 \\implies g'(x) = 3x^2$
- Derivative: $\\cos(x^3) \\cdot 3x^2 = 3x^2 \\cos(x^3)$

### 3. The Product Rule
$$\\frac{d}{dx}[u(x) v(x)] = u'(x) v(x) + u(x) v'(x)$$
Do NOT simply multiply individual derivatives! $[u v]' \\neq u' v'$.
""",
        "code_examples": [
            {
                "title": "Chain Rule and Product Rule Verification",
                "code": "import sympy as sp\nx = sp.Symbol('x')\nf = sp.sin(x**3)\ndf = sp.diff(f, x)\nprint('Derivative of sin(x^3):', df)",
                "output": "Derivative of sin(x^3): 3*x**2*cos(x**3)",
                "notes": "Notice the inner derivative 3*x^2 multiplied by the outer derivative cos(x^3)."
            }
        ],
        "common_mistakes": [
            {
                "title": "Applying Power Rule to Exponential Functions",
                "wrong_code": "d/dx(2^x) = x * 2^(x-1)",
                "correct_code": "d/dx(2^x) = 2^x * ln(2)",
                "misconception_code": "MATH_POWER_RULE_EXPONENT",
                "explanation": "Power rule only applies when x is the base. For 2^x, x is the exponent, so derivative is 2^x * ln(2)."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Find the derivative of f(x) = (2x + 1)^4.",
                "hint": "Apply the chain rule: outer derivative is 4*(2x+1)^3, inner derivative of (2x+1) is 2.",
                "solution": "f'(x) = 4 * (2x + 1)^3 * 2 = 8 * (2x + 1)^3."
            }
        ],
        "order_index": 2
    },
    {
        "concept_code": "MATH_MATRICES",
        "title": "Matrix Algebra, Determinants, and Invertibility",
        "summary": "Master matrix multiplication, non-commutativity (AB != BA), 2x2 and 3x3 determinants, and the Invertible Matrix Theorem.",
        "reading_time_min": 8,
        "introduction": "Matrices represent linear transformations between vector spaces. Understanding matrix operations, non-commutativity, and determinants forms the core computational engine of modern artificial intelligence and data science.",
        "learning_objectives": [
            "Perform matrix multiplication and verify dimensional compatibility.",
            "Understand why matrix multiplication is non-commutative in general (AB != BA).",
            "Calculate determinants and understand their geometric meaning as volume scaling factors.",
            "Determine matrix invertibility: A is invertible if and only if det(A) != 0."
        ],
        "detailed_explanation": """
### 1. Matrix Multiplication and Non-Commutativity
If $A$ is an $m \\times n$ matrix and $B$ is an $n \\times p$ matrix, their product $C = AB$ is an $m \\times p$ matrix whose entry $c_{ij}$ is the dot product of row $i$ of $A$ and column $j$ of $B$:
$$c_{ij} = \\sum_{k=1}^n a_{ik} b_{kj}$$
**Crucial Property**: In general, $AB \\neq BA$. Matrix multiplication is NOT commutative!

### 2. Determinant of a 2x2 Matrix
For $A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$:
$$\\det(A) = ad - bc$$

### 3. The Invertible Matrix Theorem
A square matrix $A$ has an inverse $A^{-1}$ such that $A A^{-1} = I$ **if and only if** $\\det(A) \\neq 0$.
If $\\det(A) = 0$, the matrix squashes space into a lower dimension, columns are linearly dependent, and no inverse exists (the matrix is singular).
""",
        "code_examples": [
            {
                "title": "Demonstration of Matrix Non-Commutativity",
                "code": "import numpy as np\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[2, 0], [1, 2]])\nAB = np.dot(A, B)\nBA = np.dot(B, A)\nprint('AB:\\n', AB)\nprint('BA:\\n', BA)\nprint('Equal?', np.array_equal(AB, BA))",
                "output": "AB:\n [[ 4  4]\n [10  8]]\nBA:\n [[ 2  4]\n [ 7 10]]\nEqual? False",
                "notes": "AB and BA yield completely different matrices."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming Invertibility when det = 0",
                "wrong_code": "det(A) = 0 implies A is invertible",
                "correct_code": "det(A) != 0 is required for A^-1 to exist",
                "misconception_code": "MATH_ZERO_DETERMINANT_INVERT",
                "explanation": "If det(A) = 0, A is singular and cannot be inverted because division by zero occurs."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Compute the determinant of A = [[4, 2], [1, 3]]. Is A invertible?",
                "hint": "Calculate ad - bc = (4)(3) - (2)(1).",
                "solution": "det(A) = (4)(3) - (2)(1) = 12 - 2 = 10. Since 10 != 0, A is invertible."
            }
        ],
        "order_index": 3
    }
]

