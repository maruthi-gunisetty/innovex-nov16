"""
LearnSphere AI: Comprehensive Seed Dataset
Populates the database with:
- 6 Python curriculum concepts with BKT parameters and prerequisite graph
- 6 rich learning modules with code examples, common errors, and exercises
- 26 carefully calibrated assessment questions with labeled misconception distractors
- 3 demonstration user accounts (2 students with distinct cognitive histories, 1 teacher)
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Ensure parent directory is in Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.auth_service import AuthService
from database.db import (
    get_db_connection, init_db, create_user,
    record_assessment_attempt, update_student_mastery_record
)
from database.multi_subject_seed import (
    SUBJECTS, COURSES, C_CONCEPTS, C_LESSONS, C_QUESTIONS,
    MATH_CONCEPTS, MATH_LESSONS, MATH_QUESTIONS
)

CONCEPTS = [
    {
        "code": "VAR",
        "name": "Variables and Data Types",
        "description": "Declaration, dynamic typing, primitive numeric types, strings, immutability, and type casting.",
        "order_index": 1,
        "p_init": 0.25,
        "p_transit": 0.18,
        "p_guess": 0.20,
        "p_slip": 0.08,
        "prerequisites": json.dumps([])
    },
    {
        "code": "COND",
        "name": "Conditional Statements",
        "description": "Boolean expressions, truthiness, if/elif/else branching, and logical operators.",
        "order_index": 2,
        "p_init": 0.20,
        "p_transit": 0.16,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["VAR"])
    },
    {
        "code": "LOOP",
        "name": "Loops and Iteration",
        "description": "For loops, while loops, range generation, loop invariants, break, continue, and termination.",
        "order_index": 3,
        "p_init": 0.18,
        "p_transit": 0.14,
        "p_guess": 0.20,
        "p_slip": 0.12,
        "prerequisites": json.dumps(["VAR", "COND"])
    },
    {
        "code": "LIST",
        "name": "Lists and Arrays",
        "description": "Sequences, 0-based indexing, slicing, mutability, shallow vs deep copying, and comprehension.",
        "order_index": 4,
        "p_init": 0.15,
        "p_transit": 0.13,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["VAR", "LOOP"])
    },
    {
        "code": "FUNC",
        "name": "Functions and Modular Design",
        "description": "Function definitions, parameters, return semantics, local versus global scope, and call frames.",
        "order_index": 5,
        "p_init": 0.15,
        "p_transit": 0.12,
        "p_guess": 0.20,
        "p_slip": 0.10,
        "prerequisites": json.dumps(["VAR", "COND", "LOOP"])
    },
    {
        "code": "REC",
        "name": "Recursion and Stack Execution",
        "description": "Self-referential functions, base case verification, call stack traversal, and recurrence relations.",
        "order_index": 6,
        "p_init": 0.10,
        "p_transit": 0.10,
        "p_guess": 0.20,
        "p_slip": 0.14,
        "prerequisites": json.dumps(["FUNC", "COND"])
    }
]

LESSONS = [
    {
        "concept_code": "VAR",
        "title": "Mastering Variables, Dynamic Typing, and Immutability",
        "summary": "Deep dive into variable assignment, fundamental data types, string operations, and explicit type conversion.",
        "reading_time_min": 7,
        "introduction": "In Python, variables do not store values directly in fixed memory boxes; rather, they serve as symbolic references pointing to dynamically allocated objects in heap memory. Understanding dynamic typing and immutability prevents subtle runtime errors.",
        "learning_objectives": [
            "Distinguish between references and values in Python memory.",
            "Recognize immutable primitive types (int, float, str, bool, tuple).",
            "Perform safe type conversions without accidental string concatenation."
        ],
        "detailed_explanation": """### Variable Binding vs Mutation
When executing `x = 10`, Python allocates an integer object `10` and binds the identifier `x` to that memory address. If you subsequently write `x = x + 1`, Python does not modify `10` in place. Instead, it creates a new integer object `11` and rebinds `x`.

### String Immutability
Strings are strictly immutable. Calling a method like `.replace()` or `.upper()` returns a newly constructed string object. If you do not assign this returned object, the modification is discarded:
```python
message = "learnsphere"
message.upper()  # Does NOT change message
print(message)   # Output: learnsphere

message = message.upper()  # Correct: Rebinds identifier
print(message)   # Output: LEARNSPHERE
```

### Type Coercion Rules
Python does not automatically coerce strings to numbers during addition. The expression `"10" + 5` produces a `TypeError`, while `"10" + str(5)` evaluates to `"105"`. To perform arithmetic on text input, use explicit casting via `int()` or `float()`.""",
        "code_examples": [
            {
                "title": "Dynamic Typing and Identity",
                "code": "score = 95\nprint(type(score), id(score))\n\nscore = 'Grade A'\nprint(type(score), id(score))",
                "output": "<class 'int'> 140723450912\n<class 'str'> 219830129480",
                "notes": "Notice how the object identity (memory address) changes when the type and value change."
            },
            {
                "title": "Explicit Type Casting",
                "code": "user_input = '42'\nmultiplier = 2\ntotal = int(user_input) * multiplier\nprint('Total:', total)",
                "output": "Total: 84",
                "notes": "int() safely parses numeric characters into an integer representation."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming input() returns a numeric type",
                "wrong_code": "age = input('Enter age: ')\nif age > 18:\n    print('Adult')",
                "correct_code": "age = int(input('Enter age: '))\nif age > 18:\n    print('Adult')",
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "explanation": "input() always yields a string. Comparing a string to an integer raises a TypeError in Python 3."
            },
            {
                "title": "Expecting String Methods to Mutate in Place",
                "wrong_code": "text = 'hello'\ntext.capitalize()\nprint(text)",
                "correct_code": "text = 'hello'\ntext = text.capitalize()\nprint(text)",
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "explanation": "Because strings are immutable, methods return a new string rather than modifying the original in-place."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Given num_str = '15', write a statement to add 5 to it as a number and print the result 20.",
                "hint": "Convert num_str using int() before addition.",
                "solution": "num_str = '15'\nresult = int(num_str) + 5\nprint(result)"
            }
        ],
        "order_index": 1
    },
    {
        "concept_code": "COND",
        "title": "Conditional Statements and Boolean Evaluation",
        "summary": "Master multi-way branching, short-circuit evaluation, truthiness rules, and logical operators.",
        "reading_time_min": 8,
        "introduction": "Conditional statements allow programs to make deterministic decisions based on logical predicates. A common pitfall among learners is confusing logical operators with natural human language phrasing.",
        "learning_objectives": [
            "Construct robust multi-way branching using if, elif, and else.",
            "Understand truthiness: which values evaluate to False in Python.",
            "Avoid common short-circuit and chained comparison logical fallacies."
        ],
        "detailed_explanation": """### Truth Value Testing (Truthiness)
In Python, any object can be tested for truth value. The following objects evaluate to `False`:
- Constants: `None`, `False`
- Numeric zeros: `0`, `0.0`, `0j`
- Empty sequences: `""`, `()`, `[]`, `{}`, `set()`

All other objects evaluate to `True`.

### Common Boolean Expression Pitfall
In natural English, one might say: "If x is 1 or 2". A student might write:
```python
if x == 1 or 2:  # BUG
    print("Match")
```
Python evaluates this as `(x == 1) or (2)`. Because non-zero integer `2` is always truthy, this condition always evaluates to `True`, regardless of `x`!

The correct implementation is:
```python
if x == 1 or x == 2:  # Explicit comparison
    print("Match")

if x in (1, 2):        # Idiomatic Python membership test
    print("Match")
```""",
        "code_examples": [
            {
                "title": "Multi-Way Branching",
                "code": "score = 82\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelif score >= 70:\n    grade = 'C'\nelse:\n    grade = 'F'\nprint('Grade:', grade)",
                "output": "Grade: B",
                "notes": "Branches are evaluated sequentially from top to bottom; the first true condition executes."
            }
        ],
        "common_mistakes": [
            {
                "title": "Chaining 'or' with Bare Literals",
                "wrong_code": "status = 'pending'\nif status == 'approved' or 'active':\n    print('Proceed')",
                "correct_code": "status = 'pending'\nif status in ('approved', 'active'):\n    print('Proceed')",
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "explanation": "Evaluating 'active' as a standalone condition always yields True because non-empty strings are truthy."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a condition checking if variable 'val' is strictly between 10 and 20 (inclusive) using chained comparison.",
                "hint": "Python supports chained comparisons: a <= b <= c.",
                "solution": "if 10 <= val <= 20:\n    print('In range')"
            }
        ],
        "order_index": 2
    },
    {
        "concept_code": "LOOP",
        "title": "Loops, Iteration Bounds, and Control Flow",
        "summary": "Understand for-in loops, while loops, range parameters, loop termination criteria, and loop invariants.",
        "reading_time_min": 9,
        "introduction": "Repetition is the bedrock of computational algorithms. Ensuring correct loop termination and understanding range half-open intervals prevents endless execution and off-by-one errors.",
        "learning_objectives": [
            "Use range(start, stop, step) with half-open intervals [start, stop).",
            "Maintain while loop state variables to avoid infinite loops.",
            "Apply break and continue statements judiciously."
        ],
        "detailed_explanation": """### The Half-Open Range Protocol
Python's built-in `range(start, stop, step)` function generates numbers up to, but not including, `stop`.
- `range(5)` yields `0, 1, 2, 3, 4` (5 elements, terminating before 5).
- `range(1, 5)` yields `1, 2, 3, 4`.
- `range(10, 0, -2)` yields `10, 8, 6, 4, 2`.

### While Loop State Invariants
A `while` loop checks its condition prior to executing each iteration. If the state variables affecting the condition are not monotonically advancing toward the termination boundary, an infinite loop occurs:
```python
i = 0
while i < 5:
    print(i)
    i += 1  # State advancement ensures eventual termination
```""",
        "code_examples": [
            {
                "title": "Accumulation Pattern in a Loop",
                "code": "total = 0\nfor n in range(1, 6):\n    total += n\nprint('Sum of 1..5 is', total)",
                "output": "Sum of 1..5 is 15",
                "notes": "n takes values 1, 2, 3, 4, 5. The upper limit 6 is excluded."
            }
        ],
        "common_mistakes": [
            {
                "title": "Off-by-One in Range Upper Bound",
                "wrong_code": "# Trying to print numbers 1 through 10\nfor i in range(1, 10):\n    print(i)",
                "correct_code": "for i in range(1, 11):\n    print(i)",
                "misconception_code": "OFF_BY_ONE_INDEX",
                "explanation": "range(1, 10) stops at 9. To include 10, the stop parameter must be 11."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a loop that calculates the product of numbers 1 through 4.",
                "hint": "Initialize product to 1 and iterate range(1, 5).",
                "solution": "product = 1\nfor i in range(1, 5):\n    product *= i\nprint(product)  # 24"
            }
        ],
        "order_index": 3
    },
    {
        "concept_code": "LIST",
        "title": "Lists, Sequences, Indexing, and Mutability",
        "summary": "Master sequence slicing, 0-based indexing, list references, mutation, and list comprehensions.",
        "reading_time_min": 10,
        "introduction": "Lists are mutable, ordered sequences that store heterogeneous items. Because lists are mutable, passing or assigning list references requires careful consideration of aliasing versus copying.",
        "learning_objectives": [
            "Access elements using positive and negative 0-based indices.",
            "Apply slice notation: list[start:stop:step].",
            "Differentiate between reference assignment (aliasing) and shallow copying."
        ],
        "detailed_explanation": """### Zero-Based Indexing and Slicing
In a list of length $N$, valid positive indices range from $0$ to $N - 1$. Negative index `-1` accesses the final element.
Slice syntax `items[start:stop]` extracts a sublist beginning at `start` and ending at `stop - 1`.

### Reference Aliasing vs Copying
When you assign `b = a`, where `a` is a list, variable `b` does not receive a distinct copy; both identifiers point to the same list object in memory:
```python
a = [1, 2, 3]
b = a        # Aliasing!
b.append(4)
print(a)     # [1, 2, 3, 4] (a is affected)

# To create an independent shallow copy:
c = a.copy() # or list(a) or a[:]
c.append(5)
print(a)     # [1, 2, 3, 4] (a remains intact)
```""",
        "code_examples": [
            {
                "title": "List Slicing and Negative Indices",
                "code": "fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry']\nprint('Last fruit:', fruits[-1])\nprint('Middle three:', fruits[1:4])",
                "output": "Last fruit: elderberry\nMiddle three: ['banana', 'cherry', 'date']",
                "notes": "fruits[1:4] extracts indices 1, 2, and 3."
            }
        ],
        "common_mistakes": [
            {
                "title": "Accidental List Aliasing Mutation",
                "wrong_code": "original = [10, 20, 30]\nbackup = original\nbackup[0] = 99\nprint(original[0])  # prints 99",
                "correct_code": "original = [10, 20, 30]\nbackup = original.copy()\nbackup[0] = 99\nprint(original[0])  # prints 10",
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "explanation": "Assignment copies the object reference, not the underlying array data. Use .copy() to preserve the original."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Given items = [10, 20, 30, 40, 50], obtain the sublist containing [30, 40].",
                "hint": "Index of 30 is 2. The slice stop must be 4.",
                "solution": "sub = items[2:4]\nprint(sub)"
            }
        ],
        "order_index": 4
    },
    {
        "concept_code": "FUNC",
        "title": "Functions, Scope Boundaries, and Return Semantics",
        "summary": "Design modular code with def, positional and keyword arguments, local vs global scope, and return values.",
        "reading_time_min": 10,
        "introduction": "Functions encapsulate algorithms into reusable modular units. Understanding the distinction between side effects (such as printing) and value returns is essential for functional composition.",
        "learning_objectives": [
            "Define parameterized functions using def and return.",
            "Understand that functions without an explicit return evaluate to None.",
            "Differentiate local variables from enclosing and global namespaces."
        ],
        "detailed_explanation": """### Return Semantics vs Printing
The `print()` function writes characters to standard output; it returns `None`. The `return` statement immediately terminates function execution and yields a value back to the caller frame.

```python
def add_print(a, b):
    print(a + b)  # Side effect only

result = add_print(3, 4)
print(result)  # Prints None!

def add_return(a, b):
    return a + b  # Returns computed value

result = add_return(3, 4)
print(result)  # Prints 7
```

### Variable Scoping (LEGB Rule)
Python resolves names using the LEGB hierarchy:
1. **L**ocal: Defined inside the current function.
2. **E**nclosing: Defined in nested enclosing functions.
3. **G**lobal: Defined at module top level.
4. **B**uilt-in: Pre-loaded Python identifiers (e.g., `len`, `range`).""",
        "code_examples": [
            {
                "title": "Functional Composition",
                "code": "def square(n):\n    return n * n\n\ndef sum_of_squares(x, y):\n    return square(x) + square(y)\n\nprint('Result:', sum_of_squares(3, 4))",
                "output": "Result: 25",
                "notes": "The output of square() flows cleanly into arithmetic addition."
            }
        ],
        "common_mistakes": [
            {
                "title": "Using print instead of return",
                "wrong_code": "def multiply(x, y):\n    print(x * y)\n\ntotal = multiply(4, 5) * 2  # TypeError: unsupported operand type for *: 'NoneType' and 'int'",
                "correct_code": "def multiply(x, y):\n    return x * y\n\ntotal = multiply(4, 5) * 2  # 40",
                "misconception_code": "RETURN_VALUE_OMISSION",
                "explanation": "Omitting the return statement causes the function to implicitly return None."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a function is_even(n) that returns True if n is divisible by 2, and False otherwise.",
                "hint": "Use the modulo operator: n % 2 == 0.",
                "solution": "def is_even(n):\n    return n % 2 == 0"
            }
        ],
        "order_index": 5
    },
    {
        "concept_code": "REC",
        "title": "Recursion, Base Conditions, and Call Stack Frames",
        "summary": "Master divide-and-conquer problem solving, recursive leap of faith, base case boundaries, and stack mechanics.",
        "reading_time_min": 11,
        "introduction": "Recursion occurs when a function solves a problem by calling smaller instances of itself. Every recursive procedure requires two components: a well-defined base case and a progress step reducing the problem size.",
        "learning_objectives": [
            "Identify the base case that halts recursive descent.",
            "Formulate the recursive relation that reduces the problem size.",
            "Trace activation frames on the execution call stack."
        ],
        "detailed_explanation": """### Anatomy of a Recursive Function
A robust recursive function adheres to two mandatory invariants:
1. **Base Case**: A trivial condition resolved directly without further recursion.
2. **Recursive Step**: Calling the function with an argument closer to the base case.

```python
def factorial(n):
    # 1. Base Case: Halts descent
    if n <= 1:
        return 1
    # 2. Recursive Step: n * subproblem of size (n - 1)
    return n * factorial(n - 1)
```

### The Call Stack
Each recursive invocation pushes a new stack frame containing local variables and the return address. When the base case is reached, frames unwind in Last-In-First-Out (LIFO) order. If the base case is missing or unreachable, Python raises a `RecursionError: maximum recursion depth exceeded`.""",
        "code_examples": [
            {
                "title": "Recursive Countdown with Base Case",
                "code": "def countdown(n):\n    if n <= 0:\n        print('Liftoff')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
                "output": "3\n2\n1\nLiftoff",
                "notes": "Each call decrements n until n <= 0 triggers return."
            }
        ],
        "common_mistakes": [
            {
                "title": "Omitting the Base Case",
                "wrong_code": "def bad_rec(n):\n    return n + bad_rec(n - 1)  # Never stops! RecursionError",
                "correct_code": "def good_rec(n):\n    if n <= 0:\n        return 0\n    return n + good_rec(n - 1)",
                "misconception_code": "BASE_CASE_OMISSION",
                "explanation": "Without a base case check, recursive calls continue indefinitely until stack memory is exhausted."
            },
            {
                "title": "Failing to Return the Recursive Call Result",
                "wrong_code": "def sum_list(nums):\n    if not nums:\n        return 0\n    sum_list(nums[1:])  # Result discarded! Caller receives None",
                "correct_code": "def sum_list(nums):\n    if not nums:\n        return 0\n    return nums[0] + sum_list(nums[1:])",
                "misconception_code": "RECURSIVE_ACCUMULATOR_RETURN",
                "explanation": "If the recursive call is not returned or accumulated, the calling frame loses the subproblem result."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Write a recursive function power(base, exp) that computes base raised to exp (assume exp >= 0).",
                "hint": "Base case: exp == 0 returns 1. Recursive step: base * power(base, exp - 1).",
                "solution": "def power(base, exp):\n    if exp == 0:\n        return 1\n    return base * power(base, exp - 1)"
            }
        ],
        "order_index": 6
    }
]

QUESTIONS = [
    # ------------------ Concept 1: VAR ------------------
    {
        "concept_code": "VAR",
        "difficulty": "beginner",
        "title": "Type Casting and String Concatenation",
        "prompt": "What is the exact output of the following Python snippet?",
        "code_snippet": "a = '20'\nb = '30'\nresult = a + b\nprint(result)",
        "options": [
            {
                "index": 0,
                "text": "2030",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Both variables are strings. The '+' operator performs string concatenation, resulting in '2030'."
            },
            {
                "index": 1,
                "text": "50",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Implicit Coercion Fallacy",
                "explanation": "Python does not automatically convert string numerals into numbers during addition. Explicit int() casting is required."
            },
            {
                "index": 2,
                "text": "TypeError: unsupported operand",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Invalid Operator Assumption",
                "explanation": "The '+' operator is valid between two strings; it performs concatenation."
            },
            {
                "index": 3,
                "text": "None",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Assignment Misunderstanding",
                "explanation": "The expression evaluates directly to a string object."
            }
        ],
        "explanation": "In Python, string concatenation produces '2030'. To perform numeric addition, use int(a) + int(b)."
    },
    {
        "concept_code": "VAR",
        "difficulty": "intermediate",
        "title": "String Slicing Immutability",
        "prompt": "What does this code print?",
        "code_snippet": "tag = 'python'\ntag[0] = 'P'\nprint(tag)",
        "options": [
            {
                "index": 0,
                "text": "TypeError: 'str' object does not support item assignment",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Strings in Python are immutable; direct item assignment is prohibited."
            },
            {
                "index": 1,
                "text": "Python",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "Item Mutation Fallacy",
                "explanation": "You cannot alter characters in place in a Python string."
            },
            {
                "index": 2,
                "text": "python",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "Silent Mutation Discard Assumption",
                "explanation": "Python raises a TypeError rather than silently ignoring invalid item assignment."
            },
            {
                "index": 3,
                "text": "P",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "Truncation Fallacy",
                "explanation": "Assignment never truncates an existing string."
            }
        ],
        "explanation": "String objects in Python are immutable. Any attempt to modify a character in-place raises a TypeError."
    },
    {
        "concept_code": "VAR",
        "difficulty": "intermediate",
        "title": "String Method In-Place Immutability",
        "prompt": "Consider the following code. What value is printed for word?",
        "code_snippet": "word = 'learnsphere'\nword.replace('learn', 'innov')\nprint(word)",
        "options": [
            {
                "index": 0,
                "text": "learnsphere",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Strings in Python are immutable. replace() returns a new string and does not modify the original word."
            },
            {
                "index": 1,
                "text": "innovsphere",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "In-Place String Mutation Fallacy",
                "explanation": "Strings cannot be mutated in place. Because word was not reassigned (word = word.replace(...)), word remains unchanged."
            },
            {
                "index": 2,
                "text": "None",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Method Return Misconception",
                "explanation": "word retains its original string reference."
            },
            {
                "index": 3,
                "text": "Error: replace requires assignment",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "Syntax Rule Confusion",
                "explanation": "The method call is valid syntax, but its return value was simply discarded."
            }
        ],
        "explanation": "Because strings are immutable, methods return a new string. You must reassign: word = word.replace(...)."
    },
    {
        "concept_code": "VAR",
        "difficulty": "advanced",
        "title": "Integer Division and Floating Point Dynamics",
        "prompt": "What is the data type and value produced by the following expression?",
        "code_snippet": "val = 9 // 2 + 7 / 2\nprint(type(val), val)",
        "options": [
            {
                "index": 0,
                "text": "<class 'float'> 7.5",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "9 // 2 yields int 4. 7 / 2 yields float 3.5. Adding int and float coerces the result to float 7.5."
            },
            {
                "index": 1,
                "text": "<class 'int'> 7",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Truncating Division Coercion Fallacy",
                "explanation": "Single slash '/' in Python 3 always produces a float. Adding a float to an int results in a float."
            },
            {
                "index": 2,
                "text": "<class 'int'> 8",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Rounding Assumption",
                "explanation": "Python does not round 7.5 to 8 unless explicit round() is called."
            },
            {
                "index": 3,
                "text": "<class 'float'> 8.0",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Floor Division Bound Error",
                "explanation": "9 // 2 is 4 (not 4.5). 4 + 3.5 is 7.5."
            }
        ],
        "explanation": "9 // 2 is 4 (int), and 7 / 2 is 3.5 (float). 4 + 3.5 = 7.5 (float)."
    },

    # ------------------ Concept 2: COND ------------------
    {
        "concept_code": "COND",
        "difficulty": "beginner",
        "title": "Compound Logical Condition with 'or'",
        "prompt": "What is printed by this conditional statement?",
        "code_snippet": "x = 5\nif x == 1 or 2:\n    print('Match')\nelse:\n    print('No match')",
        "options": [
            {
                "index": 0,
                "text": "Match",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "The condition evaluates as (x == 1) or (2). Since bool(2) is True, the overall condition is always True."
            },
            {
                "index": 1,
                "text": "No match",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Compound Disjunction Fallacy",
                "explanation": "You assumed 'or 2' checks if x equals 2. In Python, '2' is evaluated as a standalone truthy expression."
            },
            {
                "index": 2,
                "text": "SyntaxError: invalid syntax",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Syntax Confusion",
                "explanation": "This is syntactically valid Python, although logically problematic."
            },
            {
                "index": 3,
                "text": "None",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Evaluation Omission",
                "explanation": "An if-statement branch always executes when condition is met."
            }
        ],
        "explanation": "In Python, non-zero numbers are truthy. (x == 1) or 2 evaluates to False or 2, which is truthy (2)."
    },
    {
        "concept_code": "COND",
        "difficulty": "intermediate",
        "title": "Chained Comparison Evaluation",
        "prompt": "What does the expression (1 < 2 < 3 == 3) evaluate to in Python?",
        "code_snippet": "result = 1 < 2 < 3 == 3\nprint(result)",
        "options": [
            {
                "index": 0,
                "text": "True",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Chained comparisons are evaluated as (1 < 2) and (2 < 3) and (3 == 3). All clauses are True."
            },
            {
                "index": 1,
                "text": "False",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Chained Evaluation Collapse Fallacy",
                "explanation": "Believing 1 < 2 becomes True, and True < 3 comparison fails."
            },
            {
                "index": 2,
                "text": "SyntaxError",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Syntax Invalidity Error",
                "explanation": "Python natively supports chained comparisons of arbitrary length."
            },
            {
                "index": 3,
                "text": "TypeError",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Comparison Type Error",
                "explanation": "All elements in the chain are numeric."
            }
        ],
        "explanation": "In Python, chained comparisons unpack into pairwise comparisons joined by logical 'and'."
    },
    {
        "concept_code": "COND",
        "difficulty": "intermediate",
        "title": "Truthiness of Empty Collections",
        "prompt": "What will be printed when running this code?",
        "code_snippet": "items = []\nif items:\n    print('Populated')\nelif items == False:\n    print('Is False')\nelse:\n    print('Empty')",
        "options": [
            {
                "index": 0,
                "text": "Empty",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "An empty list evaluates to False in boolean contexts (if items: is false), but [] == False evaluates to False because [] is a list, not the boolean object False."
            },
            {
                "index": 1,
                "text": "Is False",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Falsy Equality Fallacy",
                "explanation": "Believing that being 'falsy' implies equality (==) with False. [] is falsy, but [] is not equal to False."
            },
            {
                "index": 2,
                "text": "Populated",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Object Truthiness Fallacy",
                "explanation": "Assuming an existing list object is always truthy. Empty collections in Python evaluate to False."
            },
            {
                "index": 3,
                "text": "TypeError: cannot evaluate list in condition",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "Type Check Invalidation",
                "explanation": "Python natively permits truth-value testing on any collection."
            }
        ],
        "explanation": "Empty list is falsy for 'if items', but does not equal the boolean False under '==' comparison. Thus 'else' executes."
    },
    {
        "concept_code": "COND",
        "difficulty": "advanced",
        "title": "Short-Circuit Logical Operator Evaluation",
        "prompt": "What is the return value of the following expression?",
        "code_snippet": "val = [] or 'default' and 100\nprint(val)",
        "options": [
            {
                "index": 0,
                "text": "100",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "'and' has higher precedence than 'or'. 'default' and 100 evaluates to 100. Then [] or 100 evaluates to 100."
            },
            {
                "index": 1,
                "text": "True",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Boolean Cast Assumption",
                "explanation": "In Python, logical operators 'and'/'or' return one of the actual operands, not a boolean True/False."
            },
            {
                "index": 2,
                "text": "'default'",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Short-Circuit Precedence Misunderstanding",
                "explanation": "'and' binds tighter than 'or'. 'default' and 100 evaluates to 100, not 'default'."
            },
            {
                "index": 3,
                "text": "[]",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "First Operand Fallacy",
                "explanation": "[] is falsy, so 'or' moves to evaluate the right-hand expression."
            }
        ],
        "explanation": "Due to operator precedence, this evaluates as [] or ('default' and 100) -> [] or 100 -> 100."
    },

    # ------------------ Concept 3: LOOP ------------------
    {
        "concept_code": "LOOP",
        "difficulty": "beginner",
        "title": "Range Bounds and Iteration Count",
        "prompt": "How many times does the print statement execute in this loop?",
        "code_snippet": "for i in range(2, 8, 2):\n    print(i)",
        "options": [
            {
                "index": 0,
                "text": "3 times (values: 2, 4, 6)",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "range(2, 8, 2) starts at 2, steps by 2, and terminates before reaching 8. The values generated are 2, 4, 6."
            },
            {
                "index": 1,
                "text": "4 times (values: 2, 4, 6, 8)",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Inclusive Stop Bound Fallacy",
                "explanation": "Assuming range stop parameter is inclusive. In Python, range(start, stop) excludes the stop value."
            },
            {
                "index": 2,
                "text": "6 times (all integers from 2 to 7)",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Ignored Step Argument",
                "explanation": "The third argument '2' specifies the step size; it does not increment by 1."
            },
            {
                "index": 3,
                "text": "2 times (values: 2, 4)",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Premature Termination Fallacy",
                "explanation": "6 is strictly less than 8, so it is included."
            }
        ],
        "explanation": "range(2, 8, 2) produces 2, 4, and 6. 8 is excluded because stop is non-inclusive."
    },
    {
        "concept_code": "LOOP",
        "difficulty": "intermediate",
        "title": "Nested Loop Iteration Counter",
        "prompt": "What is the final value of count?",
        "code_snippet": "count = 0\nfor i in range(3):\n    for j in range(2):\n        count += 1\nprint(count)",
        "options": [
            {
                "index": 0,
                "text": "6",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "The outer loop runs 3 times (i = 0, 1, 2) and the inner loop runs 2 times for each outer pass. Total = 3 * 2 = 6."
            },
            {
                "index": 1,
                "text": "5",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Additive Combination Fallacy",
                "explanation": "Adding loop bounds (3 + 2 = 5) instead of multiplying iterations for nested loops."
            },
            {
                "index": 2,
                "text": "4",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Off-by-One Nested Error",
                "explanation": "Both ranges execute their full iterations."
            },
            {
                "index": 3,
                "text": "2",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Inner Loop Only Assumption",
                "explanation": "The inner loop runs on each pass of the outer loop, not just once."
            }
        ],
        "explanation": "Nested loops execute multiplicatively: 3 iterations * 2 iterations = 6 total executions."
    },
    {
        "concept_code": "LOOP",
        "difficulty": "intermediate",
        "title": "While Loop State Mutation and Bounds",
        "prompt": "What is the final value of counter after the loop terminates?",
        "code_snippet": "counter = 1\nwhile counter < 10:\n    counter += 3\nprint(counter)",
        "options": [
            {
                "index": 0,
                "text": "10",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Values of counter across iterations: initially 1 -> 4 -> 7 -> 10. When counter is 10, 10 < 10 is False, so the loop terminates."
            },
            {
                "index": 1,
                "text": "7",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Pre-Check Exit Fallacy",
                "explanation": "When counter is 7, 7 < 10 is True, so one more addition (7 + 3 = 10) occurs."
            },
            {
                "index": 2,
                "text": "9",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Bound Rounding Error",
                "explanation": "Adding 3 repeatedly to 1 produces: 1, 4, 7, 10. 9 is never generated."
            },
            {
                "index": 3,
                "text": "13",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Late Exit Fallacy",
                "explanation": "The loop condition checks before the iteration body, preventing counter from reaching 13."
            }
        ],
        "explanation": "Iterations: 1 (enters, becomes 4), 4 (enters, becomes 7), 7 (enters, becomes 10). At 10, the condition 10 < 10 fails."
    },
    {
        "concept_code": "LOOP",
        "difficulty": "advanced",
        "title": "Loop else Clause Execution Invariant",
        "prompt": "What is printed when this snippet executes?",
        "code_snippet": "for n in range(1, 5):\n    if n % 2 == 0 and n > 3:\n        print('Found', n)\n        break\nelse:\n    print('Exhausted')",
        "options": [
            {
                "index": 0,
                "text": "Found 4",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "When n = 4, 4 % 2 == 0 and 4 > 3 is True. 'Found 4' is printed, and break halts the loop. The else block is skipped because break executed."
            },
            {
                "index": 1,
                "text": "Found 4 followed by Exhausted",
                "is_correct": False,
                "misconception_code": "LOOP_TERMINATION_STEP",
                "misconception_name": "Loop-Else Guarantee Fallacy",
                "explanation": "The else block of a loop ONLY executes if the loop terminates normally without encountering a break."
            },
            {
                "index": 2,
                "text": "Exhausted",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Range Exclusion Fallacy",
                "explanation": "range(1, 5) includes 4, which triggers the break."
            },
            {
                "index": 3,
                "text": "Found 2",
                "is_correct": False,
                "misconception_code": "BOOLEAN_SHORT_CIRCUIT",
                "misconception_name": "Conjunction Ignore Fallacy",
                "explanation": "At n = 2, 2 > 3 is False, so the condition fails."
            }
        ],
        "explanation": "In Python, a loop's else suite is executed if and only if the loop terminates naturally without a break statement."
    },

    # ------------------ Concept 4: LIST ------------------
    {
        "concept_code": "LIST",
        "difficulty": "beginner",
        "title": "List Slicing and Negative Indices",
        "prompt": "What does the following slice produce?",
        "code_snippet": "nums = [10, 20, 30, 40, 50]\nprint(nums[-3:-1])",
        "options": [
            {
                "index": 0,
                "text": "[30, 40]",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Index -3 corresponds to 30, -2 to 40, and -1 to 50. Slicing stops before index -1, yielding [30, 40]."
            },
            {
                "index": 1,
                "text": "[30, 40, 50]",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Inclusive Slice Stop Fallacy",
                "explanation": "Slice stop index is always excluded. To include the last element with slicing, omit the stop parameter: nums[-3:]."
            },
            {
                "index": 2,
                "text": "[20, 30]",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Negative Index 0-Shift Fallacy",
                "explanation": "Negative indices start at -1 (the last item), not 0. -3 is index 2 (value 30)."
            },
            {
                "index": 3,
                "text": "[]",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Directional Slicing Misconception",
                "explanation": "-3 comes before -1 in left-to-right ordering, so a non-empty slice is produced."
            }
        ],
        "explanation": "nums[-3] is 30, and nums[-1] is 50. Since slice stop is excluded, elements at indices -3 and -2 are returned: [30, 40]."
    },
    {
        "concept_code": "LIST",
        "difficulty": "intermediate",
        "title": "List Mutation via Slice Assignment",
        "prompt": "What is the content of lst after slice assignment?",
        "code_snippet": "lst = [1, 2, 3, 4]\nlst[1:3] = [8, 9, 10]\nprint(lst)",
        "options": [
            {
                "index": 0,
                "text": "[1, 8, 9, 10, 4]",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Slice [1:3] (elements 2 and 3) is replaced with the 3 elements [8, 9, 10]. The list expands dynamically."
            },
            {
                "index": 1,
                "text": "[1, [8, 9, 10], 4]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Slice Nested Insertion Fallacy",
                "explanation": "Slice assignment splices elements into the sequence rather than nesting the right-hand list as a sublist."
            },
            {
                "index": 2,
                "text": "ValueError: slice length mismatch",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Fixed Length Assumption",
                "explanation": "In Python, slice assignment can replace a slice with an iterable of any length."
            },
            {
                "index": 3,
                "text": "[1, 8, 9, 4]",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Slice Truncation Error",
                "explanation": "All elements of the replacement iterable are inserted."
            }
        ],
        "explanation": "Python slice assignment replaces elements at index 1 and 2 with the items [8, 9, 10], splicing them seamlessly."
    },
    {
        "concept_code": "LIST",
        "difficulty": "intermediate",
        "title": "List Assignment and Memory Aliasing",
        "prompt": "What is printed by this code snippet?",
        "code_snippet": "a = [1, 2, 3]\nb = a\nb.append(99)\nprint(a)",
        "options": [
            {
                "index": 0,
                "text": "[1, 2, 3, 99]",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "b = a binds b to the same list object as a. Appending to b mutates the shared underlying object, reflecting in a."
            },
            {
                "index": 1,
                "text": "[1, 2, 3]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Independent Copy Fallacy",
                "explanation": "Believing assignment b = a creates a distinct clone. It only assigns a reference to the existing list."
            },
            {
                "index": 2,
                "text": "[[1, 2, 3], 99]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Nesting Misconception",
                "explanation": "append() appends the element to the flat list, not nesting the original list."
            },
            {
                "index": 3,
                "text": "AttributeError",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Method Validity Confusion",
                "explanation": "append is a built-in method of Python lists."
            }
        ],
        "explanation": "In Python, variable assignment binds references. Both a and b point to the identical list."
    },
    {
        "concept_code": "LIST",
        "difficulty": "advanced",
        "title": "List Multiplication and Shallow References",
        "prompt": "What is the final state of the matrix?",
        "code_snippet": "matrix = [[0] * 2] * 2\nmatrix[0][0] = 7\nprint(matrix)",
        "options": [
            {
                "index": 0,
                "text": "[[7, 0], [7, 0]]",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "The outer multiplication replicates the reference to the inner list twice. Mutating matrix[0][0] mutates the shared inner list."
            },
            {
                "index": 1,
                "text": "[[7, 0], [0, 0]]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Deep Copy Multiplication Fallacy",
                "explanation": "Multiplying a list containing a mutable object duplicates the pointer, not the underlying sublist."
            },
            {
                "index": 2,
                "text": "[[7, 7], [7, 7]]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Sub-element Propagation Error",
                "explanation": "Only index 0 of the inner list was updated; index 1 remains 0."
            },
            {
                "index": 3,
                "text": "[7, 0, 0, 0]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Flattening Assumption",
                "explanation": "The matrix remains a 2D nested list."
            }
        ],
        "explanation": "List repetition duplicates object references. Both rows point to the exact same list in heap memory."
    },

    # ------------------ Concept 5: FUNC ------------------
    {
        "concept_code": "FUNC",
        "difficulty": "beginner",
        "title": "Return Value vs Standard Output Printing",
        "prompt": "What is the value of result after this snippet executes?",
        "code_snippet": "def compute(x, y):\n    print(x + y)\n\nresult = compute(10, 5)\nprint(result)",
        "options": [
            {
                "index": 0,
                "text": "None",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "The compute function prints 15 to stdout, but lacks a return statement. In Python, functions without explicit return evaluate to None."
            },
            {
                "index": 1,
                "text": "15",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Print-Return Equivalence Fallacy",
                "explanation": "Confusing printing to the screen with returning a value to the caller. print() returns None."
            },
            {
                "index": 2,
                "text": "'15'",
                "is_correct": False,
                "misconception_code": "TYPE_COERCION_CONFUSION",
                "misconception_name": "String Representation Fallacy",
                "explanation": "No string is returned; the variable result captures None."
            },
            {
                "index": 3,
                "text": "TypeError: function cannot be assigned",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Assignment Validity Confusion",
                "explanation": "Function call results can always be assigned to variables in Python."
            }
        ],
        "explanation": "print() displays output on the console and returns None. To capture the sum, the function must use 'return x + y'."
    },
    {
        "concept_code": "FUNC",
        "difficulty": "intermediate",
        "title": "Mutable Argument In-Place Side Effects",
        "prompt": "What is the output of this function call?",
        "code_snippet": "def modify(items):\n    items.append('new')\n\nmy_list = ['old']\nmodify(my_list)\nprint(my_list)",
        "options": [
            {
                "index": 0,
                "text": "['old', 'new']",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Python passes object references. Modifying a mutable object inside a function affects the caller object."
            },
            {
                "index": 1,
                "text": "['old']",
                "is_correct": False,
                "misconception_code": "SCOPE_LEAKAGE",
                "misconception_name": "Pass-by-Value Copy Assumption",
                "explanation": "Assuming Python passes full copies of lists to functions. Python uses pass-by-object-reference."
            },
            {
                "index": 2,
                "text": "None",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Return Value Confusion",
                "explanation": "my_list was mutated in-place and is printed, not the return of modify."
            },
            {
                "index": 3,
                "text": "['new']",
                "is_correct": False,
                "misconception_code": "VARIABLE_MUTATION_CONFUSION",
                "misconception_name": "Overwrite Assumption",
                "explanation": "append adds to the end; it does not replace previous elements."
            }
        ],
        "explanation": "Lists are mutable objects passed by reference. Calling .append() mutates the caller's list directly."
    },
    {
        "concept_code": "FUNC",
        "difficulty": "intermediate",
        "title": "Local Scope Isolation",
        "prompt": "What is printed when this code is executed?",
        "code_snippet": "val = 100\n\ndef update():\n    val = 200\n\nupdate()\nprint(val)",
        "options": [
            {
                "index": 0,
                "text": "100",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Inside update(), 'val = 200' creates a local variable within update's scope frame. The global val is shadowed and remains 100."
            },
            {
                "index": 1,
                "text": "200",
                "is_correct": False,
                "misconception_code": "SCOPE_LEAKAGE",
                "misconception_name": "Global Mutation Fallacy",
                "explanation": "Assuming assigning to a variable inside a function modifies the outer scope. Without the 'global' keyword, assignment creates a local binding."
            },
            {
                "index": 2,
                "text": "UnboundLocalError",
                "is_correct": False,
                "misconception_code": "SCOPE_LEAKAGE",
                "misconception_name": "Unbound Variable Confusion",
                "explanation": "val is not accessed before assignment in update(), so no UnboundLocalError occurs."
            },
            {
                "index": 3,
                "text": "None",
                "is_correct": False,
                "misconception_code": "RETURN_VALUE_OMISSION",
                "misconception_name": "Scope Destruction Misunderstanding",
                "explanation": "The global variable val remains intact."
            }
        ],
        "explanation": "Assignment inside a function defaults to local scope unless declared with 'global val'."
    },
    {
        "concept_code": "FUNC",
        "difficulty": "advanced",
        "title": "Default Parameter Evaluation Time",
        "prompt": "What does the second call to append_item produce?",
        "code_snippet": "def append_item(val, target=[]):\n    target.append(val)\n    return target\n\nprint(append_item(1))\nprint(append_item(2))",
        "options": [
            {
                "index": 0,
                "text": "[1, 2]",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "In Python, default arguments are evaluated once at function definition time, not at invocation. The list target persists and accumulates elements."
            },
            {
                "index": 1,
                "text": "[2]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Default Argument Re-Instantiation Fallacy",
                "explanation": "Believing a new empty list is created on every function invocation. Default arguments are instantiated only once when the function is parsed."
            },
            {
                "index": 2,
                "text": "[[1], 2]",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Nesting Misconception",
                "explanation": "The list is flat, storing elements sequentially."
            },
            {
                "index": 3,
                "text": "TypeError: default cannot be mutable",
                "is_correct": False,
                "misconception_code": "LIST_ALIASING_SHADOWING",
                "misconception_name": "Language Restriction Misunderstanding",
                "explanation": "Mutable defaults are syntactically permitted in Python, despite being considered an antipattern."
            }
        ],
        "explanation": "Default argument expressions are evaluated once when the function is defined. The shared list accumulates values."
    },

    # ------------------ Concept 6: REC ------------------
    {
        "concept_code": "REC",
        "difficulty": "beginner",
        "title": "Base Case Termination Condition",
        "prompt": "What happens when this recursive function is executed?",
        "code_snippet": "def count_down(n):\n    print(n)\n    count_down(n - 1)\n\ncount_down(3)",
        "options": [
            {
                "index": 0,
                "text": "RecursionError: maximum recursion depth exceeded",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "The function has no base case to halt recursion. It continues decrementing n and pushing stack frames until the recursion limit is exceeded."
            },
            {
                "index": 1,
                "text": "Prints 3, 2, 1, 0 and halts",
                "is_correct": False,
                "misconception_code": "BASE_CASE_OMISSION",
                "misconception_name": "Implicit Zero Termination Fallacy",
                "explanation": "Assuming recursive functions naturally stop at 0 without an explicit conditional check."
            },
            {
                "index": 2,
                "text": "Prints 3, 2, 1 and halts",
                "is_correct": False,
                "misconception_code": "BASE_CASE_OMISSION",
                "misconception_name": "Natural Boundary Assumption",
                "explanation": "Python does not automatically stop recursion at positive boundaries."
            },
            {
                "index": 3,
                "text": "SyntaxError",
                "is_correct": False,
                "misconception_code": "BASE_CASE_OMISSION",
                "misconception_name": "Syntax Invalidation",
                "explanation": "The syntax is valid; it fails at runtime with RecursionError."
            }
        ],
        "explanation": "A recursive function must have a base case (e.g., 'if n <= 0: return') to prevent infinite recursion."
    },
    {
        "concept_code": "REC",
        "difficulty": "intermediate",
        "title": "Recursive String Reversal Accumulator",
        "prompt": "What does reverse_str('cat') return?",
        "code_snippet": "def reverse_str(s):\n    if len(s) <= 1:\n        return s\n    return reverse_str(s[1:]) + s[0]\n\nprint(reverse_str('cat'))",
        "options": [
            {
                "index": 0,
                "text": "tac",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "reverse_str('cat') -> reverse_str('at') + 'c' -> (reverse_str('t') + 'a') + 'c' -> 't' + 'a' + 'c' = 'tac'."
            },
            {
                "index": 1,
                "text": "cat",
                "is_correct": False,
                "misconception_code": "RECURSIVE_ACCUMULATOR_RETURN",
                "misconception_name": "Preserved Order Fallacy",
                "explanation": "s[0] is concatenated to the right of the recursive call, which reverses the sequence."
            },
            {
                "index": 2,
                "text": "t",
                "is_correct": False,
                "misconception_code": "BASE_CASE_OMISSION",
                "misconception_name": "Base Case Only Fallacy",
                "explanation": "The unwinding frames concatenate the preceding characters."
            },
            {
                "index": 3,
                "text": "act",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Slice Offset Error",
                "explanation": "s[1:] cleanly skips the first character for recursive processing."
            }
        ],
        "explanation": "The recursive formulation recursively reverses the tail s[1:] and appends the head s[0] to the end, producing 'tac'."
    },
    {
        "concept_code": "REC",
        "difficulty": "intermediate",
        "title": "Recursive Result Propagation and Return",
        "prompt": "What is the return value of mystery(3)?",
        "code_snippet": "def mystery(n):\n    if n <= 1:\n        return 1\n    mystery(n - 1)\n\nprint(mystery(3))",
        "options": [
            {
                "index": 0,
                "text": "None",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "In the recursive branch (when n > 1), mystery(n - 1) is invoked, but its return value is NOT returned! The top-level call reaches the implicit end and returns None."
            },
            {
                "index": 1,
                "text": "1",
                "is_correct": False,
                "misconception_code": "RECURSIVE_ACCUMULATOR_RETURN",
                "misconception_name": "Automatic Stack Propagation Fallacy",
                "explanation": "Assuming the inner return 1 bubbles all the way up through callers automatically. Every frame must explicitly 'return mystery(n - 1)'."
            },
            {
                "index": 2,
                "text": "3",
                "is_correct": False,
                "misconception_code": "RECURSIVE_ACCUMULATOR_RETURN",
                "misconception_name": "Argument Echo Fallacy",
                "explanation": "The function does not echo the input parameter."
            },
            {
                "index": 3,
                "text": "6",
                "is_correct": False,
                "misconception_code": "RECURSIVE_ACCUMULATOR_RETURN",
                "misconception_name": "Factorial Assumption",
                "explanation": "There is no multiplication operator here."
            }
        ],
        "explanation": "Because the branch does not say 'return mystery(n - 1)', the result computed at the base case is discarded."
    },
    {
        "concept_code": "REC",
        "difficulty": "advanced",
        "title": "Call Stack Unwinding and Backtracking Order",
        "prompt": "What is the exact printed output sequence?",
        "code_snippet": "def walk(n):\n    if n == 0:\n        return\n    walk(n - 1)\n    print(n, end=' ')\n\nwalk(3)",
        "options": [
            {
                "index": 0,
                "text": "1 2 3 ",
                "is_correct": True,
                "misconception_code": "NONE",
                "misconception_name": "Correct Understanding",
                "explanation": "Because the recursive call precedes the print statement, prints occur during stack unwinding. The deepest frame (n=1) prints first, followed by n=2, then n=3."
            },
            {
                "index": 1,
                "text": "3 2 1 ",
                "is_correct": False,
                "misconception_code": "BASE_CASE_OMISSION",
                "misconception_name": "Descent Order Printing Fallacy",
                "explanation": "Assuming print happens on descent. The print statement is located AFTER the recursive call, executing on stack return."
            },
            {
                "index": 2,
                "text": "0 1 2 3 ",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Base Case Execution Fallacy",
                "explanation": "When n == 0, the function returns immediately before print is reached."
            },
            {
                "index": 3,
                "text": "3 2 1 0 ",
                "is_correct": False,
                "misconception_code": "OFF_BY_ONE_INDEX",
                "misconception_name": "Inclusive Zero Descent Error",
                "explanation": "Neither descent order nor 0 inclusion is correct."
            }
        ],
        "explanation": "Post-order recursive traversal: the execution stack descends to n=0 first, then unwinds printing 1, 2, and 3."
    }
]


def seed_database(force: bool = False) -> None:
    """Initializes the database and seeds subjects, courses, concepts, lessons, questions, and demo profiles."""
    init_db(force=force)

    with get_db_connection() as conn:
        cur = conn.cursor()

        # Check if already seeded with courses
        cur.execute("SELECT COUNT(*) as cnt FROM courses")
        if cur.fetchone()["cnt"] > 0 and not force:
            return

        # Clear existing data if forced or upgrading
        if force:
            conn.execute("DELETE FROM lesson_progress")
            conn.execute("DELETE FROM learning_recommendations")
            conn.execute("DELETE FROM student_mastery")
            conn.execute("DELETE FROM assessment_attempts")
            conn.execute("DELETE FROM learning_content")
            conn.execute("DELETE FROM questions")
            conn.execute("DELETE FROM concepts")
            conn.execute("DELETE FROM courses")
            conn.execute("DELETE FROM subjects")
            conn.execute("DELETE FROM users")
            conn.commit()

        # 1. Seed Subjects
        subject_map = {}
        for s in SUBJECTS:
            cur.execute("""
                INSERT OR IGNORE INTO subjects (code, name, category, description, icon, is_active, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (s["code"], s["name"], s["category"], s["description"], s["icon"], 1, s["order_index"]))
            cur.execute("SELECT id FROM subjects WHERE code = ?", (s["code"],))
            subject_map[s["code"]] = cur.fetchone()["id"]

        # 2. Seed Courses
        course_map = {}
        for c in COURSES:
            s_id = subject_map[c["subject_code"]]
            cur.execute("""
                INSERT OR IGNORE INTO courses (subject_id, code, name, description, difficulty_level, is_active, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (s_id, c["code"], c["name"], c["description"], c["difficulty_level"], 1, c["order_index"]))
            cur.execute("SELECT id FROM courses WHERE code = ?", (c["code"],))
            course_map[c["code"]] = cur.fetchone()["id"]

        # 3. Seed Concepts (Python, C Programming, Mathematics)
        concept_id_map = {}

        # 3A. Python Concepts
        py_subj_id = subject_map["programming"]
        py_course_id = course_map["python"]
        for c in CONCEPTS:
            cur.execute("""
                INSERT OR REPLACE INTO concepts (subject_id, course_id, code, name, description, order_index, p_init, p_transit, p_guess, p_slip, prerequisites)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (py_subj_id, py_course_id, c["code"], c["name"], c["description"], c["order_index"], c["p_init"], c["p_transit"], c["p_guess"], c["p_slip"], c["prerequisites"]))
            cur.execute("SELECT id FROM concepts WHERE code = ?", (c["code"],))
            concept_id_map[c["code"]] = cur.fetchone()["id"]

        # 3B. C Programming Concepts
        c_subj_id = subject_map["programming"]
        c_course_id = course_map["c_programming"]
        for c in C_CONCEPTS:
            cur.execute("""
                INSERT OR REPLACE INTO concepts (subject_id, course_id, code, name, description, order_index, p_init, p_transit, p_guess, p_slip, prerequisites)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (c_subj_id, c_course_id, c["code"], c["name"], c["description"], c["order_index"], c["p_init"], c["p_transit"], c["p_guess"], c["p_slip"], c["prerequisites"]))
            cur.execute("SELECT id FROM concepts WHERE code = ?", (c["code"],))
            concept_id_map[c["code"]] = cur.fetchone()["id"]

        # 3C. Mathematics Concepts
        math_subj_id = subject_map["mathematics"]
        math_course_id = course_map["calculus_linear_algebra"]
        for c in MATH_CONCEPTS:
            cur.execute("""
                INSERT OR REPLACE INTO concepts (subject_id, course_id, code, name, description, order_index, p_init, p_transit, p_guess, p_slip, prerequisites)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (math_subj_id, math_course_id, c["code"], c["name"], c["description"], c["order_index"], c["p_init"], c["p_transit"], c["p_guess"], c["p_slip"], c["prerequisites"]))
            cur.execute("SELECT id FROM concepts WHERE code = ?", (c["code"],))
            concept_id_map[c["code"]] = cur.fetchone()["id"]

        # 4. Seed Learning Content (Python, C, Mathematics)
        all_lessons = LESSONS + C_LESSONS + MATH_LESSONS
        for l in all_lessons:
            if l["concept_code"] in concept_id_map:
                cid = concept_id_map[l["concept_code"]]
                cur.execute("""
                    INSERT OR REPLACE INTO learning_content (
                        concept_id, title, summary, reading_time_min, introduction,
                        learning_objectives_json, detailed_explanation,
                        code_examples_json, common_mistakes_json, practice_exercises_json, order_index
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cid, l["title"], l["summary"], l["reading_time_min"], l["introduction"],
                    json.dumps(l["learning_objectives"]), l["detailed_explanation"],
                    json.dumps(l["code_examples"]), json.dumps(l["common_mistakes"]),
                    json.dumps(l["practice_exercises"]), l["order_index"]
                ))

        # 5. Seed Assessment Questions (Python, C, Mathematics)
        all_questions = QUESTIONS + C_QUESTIONS + MATH_QUESTIONS
        question_id_map = {}
        for q in all_questions:
            if q["concept_code"] in concept_id_map:
                cid = concept_id_map[q["concept_code"]]
                cur.execute("""
                    INSERT INTO questions (
                        concept_id, difficulty, title, prompt, code_snippet, options_json, explanation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    cid, q["difficulty"], q["title"], q["prompt"], q.get("code_snippet"),
                    json.dumps(q["options"]), q["explanation"]
                ))
                question_id_map[q["title"]] = cur.lastrowid

        conn.commit()

    # 6. Seed Demo Users
    pwd_hash, salt = AuthService.hash_password("student123")
    student_id = create_user(
        username="student@123",
        email="student@123",
        password_hash=pwd_hash,
        salt=salt,
        full_name="Alex Rivera",
        role="student",
        is_demo=1,
        target_difficulty="adaptive",
        daily_goal=5
    )

    alex_id = create_user(
        username="alex_rivera",
        email="alex.rivera@example.edu",
        password_hash=pwd_hash,
        salt=salt,
        full_name="Alex Rivera",
        role="student",
        is_demo=1,
        target_difficulty="adaptive",
        daily_goal=5
    )

    sophia_id = create_user(
        username="sophia_chen",
        email="sophia.chen@example.edu",
        password_hash=pwd_hash,
        salt=salt,
        full_name="Sophia Chen",
        role="student",
        is_demo=1,
        target_difficulty="advanced",
        daily_goal=10
    )

    teacher_pwd_hash, teacher_salt = AuthService.hash_password("learnsphere123")
    create_user(
        username="dr_bennett",
        email="s.bennett@university.edu",
        password_hash=teacher_pwd_hash,
        salt=teacher_salt,
        full_name="Dr. Sarah Bennett",
        role="teacher",
        is_demo=1
    )

    # 7. Populate Simulated Learning Histories for Demo Accounts across Multi-Subject Tracks
    _seed_alex_history(student_id, concept_id_map, question_id_map)
    _seed_alex_history(alex_id, concept_id_map, question_id_map)
    _seed_sophia_history(sophia_id, concept_id_map, question_id_map)


def _seed_alex_history(alex_id: int, concept_map: dict, q_map: dict) -> None:
    """Alex Rivera: Multi-subject telemetry with realistic mastery profiles."""
    # Python Track
    if "VAR" in concept_map:
        update_student_mastery_record(alex_id, concept_map["VAR"], 0.88, True)
    if "COND" in concept_map:
        update_student_mastery_record(alex_id, concept_map["COND"], 0.72, True)
    if "LOOP" in concept_map:
        update_student_mastery_record(alex_id, concept_map["LOOP"], 0.38, False)
    if "LIST" in concept_map:
        update_student_mastery_record(alex_id, concept_map["LIST"], 0.42, False)
    if "FUNC" in concept_map:
        update_student_mastery_record(alex_id, concept_map["FUNC"], 0.28, False)
    if "REC" in concept_map:
        update_student_mastery_record(alex_id, concept_map["REC"], 0.15, False)

    # C Programming Track
    if "C_DATA_TYPES" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_DATA_TYPES"], 0.85, True)
    if "C_CONTROL_FLOW" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_CONTROL_FLOW"], 0.75, True)
    if "C_POINTERS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_POINTERS"], 0.32, False)
    if "C_ARRAYS_STRINGS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_ARRAYS_STRINGS"], 0.40, False)
    if "C_MEMORY_MGMT" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_MEMORY_MGMT"], 0.25, False)
    if "C_STRUCTS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["C_STRUCTS"], 0.20, False)

    # Mathematics Track
    if "MATH_LIMITS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_LIMITS"], 0.82, True)
    if "MATH_DERIVATIVES" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_DERIVATIVES"], 0.45, False)
    if "MATH_INTEGRALS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_INTEGRALS"], 0.25, False)
    if "MATH_MATRICES" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_MATRICES"], 0.70, True)
    if "MATH_VECTORS" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_VECTORS"], 0.40, False)
    if "MATH_EIGEN" in concept_map:
        update_student_mastery_record(alex_id, concept_map["MATH_EIGEN"], 0.18, False)

    now = datetime.now()
    attempts = [
        # Python attempts
        (alex_id, q_map.get("Type Casting and String Concatenation", 1), concept_map.get("VAR", 1), 0, True, "beginner", 14.2, "NONE", 0.30, 0.65, now - timedelta(days=4)),
        (alex_id, q_map.get("String Method In-Place Immutability", 2), concept_map.get("VAR", 1), 0, True, "intermediate", 22.1, "NONE", 0.65, 0.88, now - timedelta(days=4, hours=1)),
        (alex_id, q_map.get("Range Bounds and Iteration Count", 7), concept_map.get("LOOP", 3), 1, False, "beginner", 12.3, "OFF_BY_ONE_INDEX", 0.20, 0.12, now - timedelta(days=2)),
        (alex_id, q_map.get("List Assignment and Memory Aliasing", 11), concept_map.get("LIST", 4), 1, False, "intermediate", 19.5, "LIST_ALIASING_SHADOWING", 0.09, 0.06, now - timedelta(hours=14)),
        (alex_id, q_map.get("Base Case Termination Condition", 16), concept_map.get("REC", 6), 1, False, "beginner", 11.2, "BASE_CASE_OMISSION", 0.10, 0.05, now - timedelta(hours=2)),

        # C Programming attempts
        (alex_id, q_map.get("Integer Division Truncation in C", 1), concept_map.get("C_DATA_TYPES", 7), 0, True, "beginner", 16.0, "NONE", 0.40, 0.72, now - timedelta(days=3)),
        (alex_id, q_map.get("Address-Of (&) and Dereference (*) Semantics", 1), concept_map.get("C_POINTERS", 9), 0, True, "beginner", 20.0, "NONE", 0.25, 0.55, now - timedelta(days=2)),
        (alex_id, q_map.get("Uninitialized / Wild Pointer Dereference", 1), concept_map.get("C_POINTERS", 9), 1, False, "intermediate", 28.5, "C_WILD_POINTER_DEREF", 0.55, 0.32, now - timedelta(days=1)),
        (alex_id, q_map.get("Missing Null-Terminator in C String Literals", 1), concept_map.get("C_ARRAYS_STRINGS", 10), 1, False, "beginner", 14.0, "C_STRING_NULL_TERMINATOR", 0.30, 0.18, now - timedelta(hours=18)),
        (alex_id, q_map.get("Memory Leak Identification", 1), concept_map.get("C_MEMORY_MGMT", 11), 1, False, "intermediate", 35.0, "C_MEMORY_LEAK_NO_FREE", 0.20, 0.10, now - timedelta(hours=6)),

        # Mathematics attempts
        (alex_id, q_map.get("Evaluating Limits of Rational Functions (0/0)", 1), concept_map.get("MATH_LIMITS", 13), 0, True, "beginner", 24.0, "NONE", 0.45, 0.82, now - timedelta(days=3, hours=5)),
        (alex_id, q_map.get("Power Rule vs Exponential Derivative", 1), concept_map.get("MATH_DERIVATIVES", 14), 1, False, "beginner", 18.5, "MATH_POWER_RULE_EXPONENT", 0.40, 0.22, now - timedelta(days=2, hours=3)),
        (alex_id, q_map.get("Composite Function Chain Rule", 1), concept_map.get("MATH_DERIVATIVES", 14), 1, False, "intermediate", 31.0, "MATH_CHAIN_RULE_OMISSION", 0.22, 0.14, now - timedelta(days=1, hours=4)),
        (alex_id, q_map.get("Matrix Multiplication Commutativity", 1), concept_map.get("MATH_MATRICES", 16), 0, True, "beginner", 15.0, "NONE", 0.35, 0.70, now - timedelta(hours=10))
    ]

    with get_db_connection() as conn:
        for att in attempts:
            conn.execute("""
                INSERT INTO assessment_attempts (
                    user_id, question_id, concept_id, selected_option_index,
                    is_correct, difficulty, response_time_sec, misconception_code,
                    prior_mastery, posterior_mastery, attempted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                att[0], att[1], att[2], att[3], 1 if att[4] else 0,
                att[5], att[6], att[7], att[8], att[9], att[10].isoformat()
            ))
        conn.commit()


def _seed_sophia_history(sophia_id: int, concept_map: dict, q_map: dict) -> None:
    """Sophia Chen: Advanced proficient learner across all curriculum tracks."""
    for c_code, cid in concept_map.items():
        update_student_mastery_record(sophia_id, cid, 0.88, True)

    now = datetime.now()
    attempts = [
        (sophia_id, q_map.get("Type Casting and String Concatenation", 1), concept_map.get("VAR", 1), 0, True, "beginner", 8.4, "NONE", 0.40, 0.85, now - timedelta(days=5)),
        (sophia_id, q_map.get("String Method In-Place Immutability", 2), concept_map.get("VAR", 1), 0, True, "intermediate", 12.1, "NONE", 0.85, 0.96, now - timedelta(days=5, hours=1)),
        (sophia_id, q_map.get("Integer Division Truncation in C", 1), concept_map.get("C_DATA_TYPES", 7), 0, True, "beginner", 9.5, "NONE", 0.50, 0.88, now - timedelta(days=4)),
        (sophia_id, q_map.get("Address-Of (&) and Dereference (*) Semantics", 1), concept_map.get("C_POINTERS", 9), 0, True, "beginner", 11.2, "NONE", 0.55, 0.90, now - timedelta(days=3)),
        (sophia_id, q_map.get("Evaluating Limits of Rational Functions (0/0)", 1), concept_map.get("MATH_LIMITS", 13), 0, True, "beginner", 14.0, "NONE", 0.50, 0.92, now - timedelta(days=2)),
        (sophia_id, q_map.get("Matrix Multiplication Commutativity", 1), concept_map.get("MATH_MATRICES", 16), 0, True, "beginner", 12.0, "NONE", 0.60, 0.94, now - timedelta(days=1))
    ]

    with get_db_connection() as conn:
        for att in attempts:
            conn.execute("""
                INSERT INTO assessment_attempts (
                    user_id, question_id, concept_id, selected_option_index,
                    is_correct, difficulty, response_time_sec, misconception_code,
                    prior_mastery, posterior_mastery, attempted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                att[0], att[1], att[2], att[3], 1 if att[4] else 0,
                att[5], att[6], att[7], att[8], att[9], att[10].isoformat()
            ))
        conn.commit()


if __name__ == "__main__":
    seed_database(force=True)
    print("Database successfully initialized and seeded with multi-subject curriculum.")
