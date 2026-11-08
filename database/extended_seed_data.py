"""
Sarva Vidya: Extended Subject Curriculum Dataset
Complete curriculum concepts, calibrated assessment questions, and learning modules
for Data Structures & Algorithms, Quantum Computing, Digital Logic, and Classical Mechanics.
"""

import json
from database.db import get_db_connection

# ==============================================================================
# 1. CONCEPTS
# ==============================================================================
EXTENDED_CONCEPTS = {
    # --------------------------------------------------------------------------
    # Course 6: Data Structures & Algorithms (Computer Science, subject_id: 5)
    # --------------------------------------------------------------------------
    "dsa": [
        {
            "code": "DSA_COMPLEXITY",
            "name": "Asymptotic Complexity & Big-O Notation",
            "description": "Worst-case, best-case, average-case analysis, Master Theorem, and asymptotic bounds (O, Omega, Theta).",
            "order_index": 1,
            "p_init": 0.25,
            "p_transit": 0.18,
            "p_guess": 0.20,
            "p_slip": 0.08,
            "prerequisites": json.dumps([])
        },
        {
            "code": "DSA_TREES_HEAPS",
            "name": "Binary Trees, BSTs & Binary Heaps",
            "description": "Tree traversals (in-order, pre-order, post-order), BST invariant, and min/max binary heap properties.",
            "order_index": 2,
            "p_init": 0.20,
            "p_transit": 0.15,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["DSA_COMPLEXITY"])
        },
        {
            "code": "DSA_GRAPHS",
            "name": "Graph Traversal (BFS & DFS)",
            "description": "Adjacency lists, Breadth-First Search shortest paths, Depth-First Search cycle detection and back edges.",
            "order_index": 3,
            "p_init": 0.18,
            "p_transit": 0.14,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["DSA_TREES_HEAPS"])
        },
        {
            "code": "DSA_DP",
            "name": "Dynamic Programming & Memoization",
            "description": "Optimal substructure, overlapping subproblems, top-down memoization, and bottom-up tabulation.",
            "order_index": 4,
            "p_init": 0.12,
            "p_transit": 0.12,
            "p_guess": 0.20,
            "p_slip": 0.12,
            "prerequisites": json.dumps(["DSA_COMPLEXITY"])
        }
    ],

    # --------------------------------------------------------------------------
    # Course 7: Intro to Qubits (Quantum Computing, subject_id: 7)
    # --------------------------------------------------------------------------
    "qc_101": [
        {
            "code": "QC_SUPERPOSITION",
            "name": "Quantum Superposition & State Vectors",
            "description": "Qubit representation, complex probability amplitudes, normalization, and the Bloch Sphere.",
            "order_index": 1,
            "p_init": 0.22,
            "p_transit": 0.16,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps([])
        },
        {
            "code": "QC_GATES",
            "name": "Quantum Logic Gates (Pauli, Hadamard, CNOT)",
            "description": "Single-qubit unitary operations, Hadamard superposition generation, Pauli rotations, and two-qubit CNOT gates.",
            "order_index": 2,
            "p_init": 0.18,
            "p_transit": 0.14,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["QC_SUPERPOSITION"])
        },
        {
            "code": "QC_ENTANGLEMENT",
            "name": "Quantum Entanglement & Bell States",
            "description": "Maximally entangled Bell states, EPR pairs, quantum non-locality, and the No-Cloning Theorem.",
            "order_index": 3,
            "p_init": 0.15,
            "p_transit": 0.12,
            "p_guess": 0.20,
            "p_slip": 0.12,
            "prerequisites": json.dumps(["QC_SUPERPOSITION", "QC_GATES"])
        },
        {
            "code": "QC_MEASUREMENT",
            "name": "Quantum Measurement & Wavefunction Collapse",
            "description": "Projective measurement, Born rule probability calculations, basis changes, and collapse dynamics.",
            "order_index": 4,
            "p_init": 0.20,
            "p_transit": 0.15,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["QC_SUPERPOSITION"])
        }
    ],

    # --------------------------------------------------------------------------
    # Course 4: Digital Logic & Microprocessors (Engineering, subject_id: 3)
    # --------------------------------------------------------------------------
    "digital_electronics": [
        {
            "code": "ENG_BOOLEAN_LOGIC",
            "name": "Boolean Algebra & Logic Gates",
            "description": "Basic logic gates (AND, OR, NOT, NAND, NOR, XOR), truth tables, Boolean axioms, and De Morgan's laws.",
            "order_index": 1,
            "p_init": 0.28,
            "p_transit": 0.20,
            "p_guess": 0.20,
            "p_slip": 0.08,
            "prerequisites": json.dumps([])
        },
        {
            "code": "ENG_COMBINATIONAL",
            "name": "Combinational Circuits & Karnaugh Maps",
            "description": "K-map minimization, Gray code grouping, adders (half/full), multiplexers, and decoders.",
            "order_index": 2,
            "p_init": 0.20,
            "p_transit": 0.16,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["ENG_BOOLEAN_LOGIC"])
        },
        {
            "code": "ENG_SEQUENTIAL",
            "name": "Sequential Logic, Latches & Flip-Flops",
            "description": "Clocking, level vs edge triggering, SR latches, D flip-flops, JK flip-flops, setup and hold timing.",
            "order_index": 3,
            "p_init": 0.16,
            "p_transit": 0.14,
            "p_guess": 0.20,
            "p_slip": 0.12,
            "prerequisites": json.dumps(["ENG_BOOLEAN_LOGIC"])
        },
        {
            "code": "ENG_CPU_ARCH",
            "name": "ALU, Registers & Microprocessor Architecture",
            "description": "Arithmetic Logic Unit flags, Program Counter, instruction fetch-decode-execute cycle, and pipelining hazards.",
            "order_index": 4,
            "p_init": 0.14,
            "p_transit": 0.12,
            "p_guess": 0.20,
            "p_slip": 0.12,
            "prerequisites": json.dumps(["ENG_COMBINATIONAL", "ENG_SEQUENTIAL"])
        }
    ],

    # --------------------------------------------------------------------------
    # Course 5: Classical Mechanics & Kinematics (Science, subject_id: 4)
    # --------------------------------------------------------------------------
    "physics_mechanics": [
        {
            "code": "PHYS_KINEMATICS",
            "name": "1D/2D Kinematics & Motion Vectors",
            "description": "Displacement, velocity, acceleration, kinematic equations under constant g, and projectile motion trajectories.",
            "order_index": 1,
            "p_init": 0.28,
            "p_transit": 0.20,
            "p_guess": 0.20,
            "p_slip": 0.08,
            "prerequisites": json.dumps([])
        },
        {
            "code": "PHYS_NEWTON_LAWS",
            "name": "Newton's Laws of Motion & Free Body Diagrams",
            "description": "Inertia, F = ma, action-reaction pairs, free body diagrams, normal force, friction, and tension.",
            "order_index": 2,
            "p_init": 0.22,
            "p_transit": 0.18,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["PHYS_KINEMATICS"])
        },
        {
            "code": "PHYS_ENERGY_WORK",
            "name": "Work, Kinetic Energy & Conservation Laws",
            "description": "Work-Energy Theorem, conservative forces, gravitational and elastic potential energy, and mechanical energy conservation.",
            "order_index": 3,
            "p_init": 0.18,
            "p_transit": 0.15,
            "p_guess": 0.20,
            "p_slip": 0.10,
            "prerequisites": json.dumps(["PHYS_NEWTON_LAWS"])
        },
        {
            "code": "PHYS_MOMENTUM",
            "name": "Linear Momentum & Collisions",
            "description": "Momentum definition (p = mv), impulse-momentum theorem, elastic vs inelastic collisions, and center of mass.",
            "order_index": 4,
            "p_init": 0.16,
            "p_transit": 0.14,
            "p_guess": 0.20,
            "p_slip": 0.11,
            "prerequisites": json.dumps(["PHYS_NEWTON_LAWS"])
        }
    ]
}

# ==============================================================================
# 2. QUESTIONS (4 questions per concept, answers cycled 1, 2, 0, 3)
# ==============================================================================
EXTENDED_QUESTIONS = [
    # --------------------------------------------------------------------------
    # DSA_COMPLEXITY (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "DSA_COMPLEXITY",
        "difficulty": "beginner",
        "title": "Array Index Lookup Complexity",
        "prompt": "What is the worst-case time complexity of accessing an element by index in a contiguous array of size n?",
        "options": [
            {"index": 0, "text": "O(n)", "is_correct": False, "misconception_code": "LINEAR_SCAN_FALLACY", "misconception_name": "Linear Scan Assumption", "explanation": "Direct indexing does not iterate across the array."},
            {"index": 1, "text": "O(1)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Contiguous arrays calculate element addresses in O(1) via base + (index * element_size)."},
            {"index": 2, "text": "O(log n)", "is_correct": False, "misconception_code": "BINARY_SEARCH_CONFUSION", "misconception_name": "Binary Search Confusion", "explanation": "Logarithmic time applies to binary search on sorted data, not direct indexing."},
            {"index": 3, "text": "O(n^2)", "is_correct": False, "misconception_code": "QUADRATIC_CONFUSION", "misconception_name": "Quadratic Misunderstanding", "explanation": "Accessing a single memory address never requires nested execution."}
        ],
        "explanation": "Array indexing computes the exact memory address in constant O(1) time using pointer arithmetic."
    },
    {
        "concept_code": "DSA_COMPLEXITY",
        "difficulty": "intermediate",
        "title": "Merge Sort Recurrence Relation",
        "prompt": "Which recurrence relation describes the divide-and-conquer execution of Merge Sort on an array of size n?",
        "options": [
            {"index": 0, "text": "T(n) = T(n - 1) + O(1)", "is_correct": False, "misconception_code": "LINEAR_DECREMENT_FALLACY", "misconception_name": "Linear Decrement Misconception", "explanation": "Merge sort divides the array in half rather than decrementing by one."},
            {"index": 1, "text": "T(n) = 2T(n/2) + O(n^2)", "is_correct": False, "misconception_code": "QUADRATIC_MERGE_FALLACY", "misconception_name": "Quadratic Merge Assumption", "explanation": "Merging two sorted subarrays requires linear O(n) comparisons, not quadratic."},
            {"index": 2, "text": "T(n) = 2T(n/2) + O(n)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Merge Sort recursively solves two subproblems of size n/2 and merges them in linear O(n) time."},
            {"index": 3, "text": "T(n) = T(n/2) + O(1)", "is_correct": False, "misconception_code": "BINARY_SEARCH_RECURRENCE", "misconception_name": "Binary Search Recurrence", "explanation": "This recurrence describes binary search where only one half is explored."}
        ],
        "explanation": "Merge Sort splits the input into two subproblems of size n/2 and merges the results in O(n) time, yielding T(n) = 2T(n/2) + O(n)."
    },
    {
        "concept_code": "DSA_COMPLEXITY",
        "difficulty": "intermediate",
        "title": "Hash Table Worst-Case Lookup",
        "prompt": "What is the worst-case time complexity of searching for a key in a Hash Table that resolves collisions via separate chaining?",
        "options": [
            {"index": 0, "text": "O(n) when all n keys collide into a single bucket list", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "If a pathological hash function maps all keys to the same bucket, lookup degenerates to searching a linked list of length n."},
            {"index": 1, "text": "O(1) strictly guaranteed across all possible inputs", "is_correct": False, "misconception_code": "HASH_WORST_CASE_FALLACY", "misconception_name": "Average vs Worst Case Confusion", "explanation": "O(1) is the average-case expectation under uniform hashing, not the theoretical worst case."},
            {"index": 2, "text": "O(log n) due to internal tree indexing", "is_correct": False, "misconception_code": "TREE_HASH_CONFUSION", "misconception_name": "Tree Hash Confusion", "explanation": "Standard separate chaining uses linked lists with linear scan unless explicitly treeified."},
            {"index": 3, "text": "O(n log n) due to rehashing latency", "is_correct": False, "misconception_code": "REHASH_CONFUSION", "misconception_name": "Rehash Misunderstanding", "explanation": "Search operations do not trigger rehashing."}
        ],
        "explanation": "Under worst-case hash collisions where all keys fall into one bucket, search time degrades to linear O(n)."
    },
    {
        "concept_code": "DSA_COMPLEXITY",
        "difficulty": "advanced",
        "title": "Master Theorem Evaluation",
        "prompt": "Applying the Master Theorem, what is the asymptotic solution to the recurrence T(n) = 4T(n/2) + n?",
        "options": [
            {"index": 0, "text": "Theta(n)", "is_correct": False, "misconception_code": "ROOT_DOMINANCE_FALLACY", "misconception_name": "Root Dominance Fallacy", "explanation": "The work at the leaves dominates the linear root combination work."},
            {"index": 1, "text": "Theta(n log n)", "is_correct": False, "misconception_code": "BALANCED_CASE_CONFUSION", "misconception_name": "Case 2 Misapplication", "explanation": "f(n) = n is polynomially smaller than n^(log_b a) = n^2."},
            {"index": 2, "text": "Theta(n sqrt(n))", "is_correct": False, "misconception_code": "FRACTIONAL_EXPONENT_CONFUSION", "misconception_name": "Exponent Miscalculation", "explanation": "log_2 4 equals 2, an integer."},
            {"index": 3, "text": "Theta(n^2)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "With a=4, b=2, log_b(a) = log_2(4) = 2. Since f(n) = n = O(n^(2-epsilon)), Master Theorem Case 1 yields Theta(n^2)."}
        ],
        "explanation": "Because log_2(4) = 2 and f(n) = n = O(n^(2 - 1)), Case 1 applies and T(n) = Theta(n^2)."
    },

    # --------------------------------------------------------------------------
    # DSA_TREES_HEAPS (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "DSA_TREES_HEAPS",
        "difficulty": "beginner",
        "title": "Binary Min-Heap Root Property",
        "prompt": "In a valid binary min-heap with n elements, where is the smallest key always located?",
        "options": [
            {"index": 0, "text": "At the rightmost leaf node", "is_correct": False, "misconception_code": "LEAF_MIN_FALLACY", "misconception_name": "Leaf Minimum Fallacy", "explanation": "Leaves in a min-heap hold large values, not the minimum."},
            {"index": 1, "text": "At the root node", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By definition, the min-heap property ensures every parent node is less than or equal to its children."},
            {"index": 2, "text": "At the middle index of the array", "is_correct": False, "misconception_code": "MEDIAN_ROOT_CONFUSION", "misconception_name": "Median Confusion", "explanation": "The array middle stores internal parent nodes, not the minimum."},
            {"index": 3, "text": "At index n - 1", "is_correct": False, "misconception_code": "ARRAY_END_CONFUSION", "misconception_name": "End of Array Confusion", "explanation": "Index n - 1 is a leaf node holding one of the larger values."}
        ],
        "explanation": "In a min-heap, the root node (index 0 or 1) always contains the minimum element."
    },
    {
        "concept_code": "DSA_TREES_HEAPS",
        "difficulty": "intermediate",
        "title": "BST In-Order Traversal",
        "prompt": "Which tree traversal order outputs the values of a Binary Search Tree (BST) in sorted ascending sequence?",
        "options": [
            {"index": 0, "text": "Pre-order traversal (Root, Left, Right)", "is_correct": False, "misconception_code": "PREORDER_SORT_CONFUSION", "misconception_name": "Pre-Order Sort Confusion", "explanation": "Pre-order visits the parent before its left child, so values will not be sorted."},
            {"index": 1, "text": "Post-order traversal (Left, Right, Root)", "is_correct": False, "misconception_code": "POSTORDER_SORT_CONFUSION", "misconception_name": "Post-Order Sort Confusion", "explanation": "Post-order visits root last, placing the root after all right subtree values."},
            {"index": 2, "text": "In-order traversal (Left, Root, Right)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Because all nodes in the left subtree are smaller than root and all in right subtree are larger, In-order traversal visits nodes in ascending order."},
            {"index": 3, "text": "Breadth-first level-order traversal", "is_correct": False, "misconception_code": "BFS_SORT_CONFUSION", "misconception_name": "BFS Sort Confusion", "explanation": "Level-order traverses tier by tier rather than respecting tree key ordering."}
        ],
        "explanation": "In-order traversal (Left -> Node -> Right) visits BST keys in strictly non-decreasing sorted order."
    },
    {
        "concept_code": "DSA_TREES_HEAPS",
        "difficulty": "intermediate",
        "title": "Min-Heap Extract-Min Complexity",
        "prompt": "What is the time complexity of the extract_min operation in a binary min-heap containing n elements?",
        "options": [
            {"index": 0, "text": "O(log n) because the replacement root must sift down the tree height", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Replacing root with the last leaf and bubbling down takes time proportional to tree height h = log_2 n."},
            {"index": 1, "text": "O(1) constant time lookup", "is_correct": False, "misconception_code": "PEEK_VS_EXTRACT_CONFUSION", "misconception_name": "Peek vs Extract Confusion", "explanation": "Finding min is O(1), but removing it and restoring the heap invariant requires O(log n)."},
            {"index": 2, "text": "O(n) linear scan across all elements", "is_correct": False, "misconception_code": "UNSORTED_ARRAY_CONFUSION", "misconception_name": "Unsorted Array Assumption", "explanation": "Heaps are balanced trees, avoiding linear scans during restoration."},
            {"index": 3, "text": "O(n log n) full rebuild", "is_correct": False, "misconception_code": "BUILD_HEAP_CONFUSION", "misconception_name": "Build Heap Confusion", "explanation": "Only one path from root to leaf is traversed during sift-down."}
        ],
        "explanation": "Extract-min takes O(log n) time because the replacement root travels down at most the tree height h = floor(log_2 n)."
    },
    {
        "concept_code": "DSA_TREES_HEAPS",
        "difficulty": "advanced",
        "title": "Full Binary Tree Node Bound",
        "prompt": "What is the maximum number of nodes in a binary tree of height h (where a single root node has height h = 0)?",
        "options": [
            {"index": 0, "text": "2h + 1", "is_correct": False, "misconception_code": "LINEAR_NODE_FORMULA", "misconception_name": "Linear Node Formula", "explanation": "Node count doubles at every depth level rather than increasing linearly."},
            {"index": 1, "text": "2^h", "is_correct": False, "misconception_code": "LEAF_COUNT_CONFUSION", "misconception_name": "Leaf Count Confusion", "explanation": "2^h is the number of nodes at level h alone, not the cumulative total."},
            {"index": 2, "text": "h^2 - 1", "is_correct": False, "misconception_code": "POLYNOMIAL_TREE_CONFUSION", "misconception_name": "Polynomial Tree Confusion", "explanation": "Tree capacity grows exponentially, not polynomially."},
            {"index": 3, "text": "2^(h + 1) - 1", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Summing 2^0 + 2^1 + ... + 2^h yields the geometric series sum 2^(h + 1) - 1."}
        ],
        "explanation": "A complete binary tree of height h has sum_{i=0}^h 2^i = 2^(h+1) - 1 maximum nodes."
    },

    # --------------------------------------------------------------------------
    # DSA_GRAPHS (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "DSA_GRAPHS",
        "difficulty": "beginner",
        "title": "BFS Traversal Data Structure",
        "prompt": "Which auxiliary data structure is fundamentally required to implement Breadth-First Search (BFS) iteratively?",
        "options": [
            {"index": 0, "text": "LIFO Stack", "is_correct": False, "misconception_code": "STACK_BFS_CONFUSION", "misconception_name": "Stack for BFS Confusion", "explanation": "Stacks implement Depth-First Search (DFS) via LIFO order, not BFS."},
            {"index": 1, "text": "FIFO Queue", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Breadth-First Search explores vertices level by level using a First-In-First-Out (FIFO) queue."},
            {"index": 2, "text": "Binary Min-Heap", "is_correct": False, "misconception_code": "DIJKSTRA_CONFUSION", "misconception_name": "Dijkstra Priority Confusion", "explanation": "Priority heaps are used in weighted search (Dijkstra), not unweighted BFS."},
            {"index": 3, "text": "Hash Set without ordering", "is_correct": False, "misconception_code": "UNORDERED_VISITED_CONFUSION", "misconception_name": "Visited Set Only Fallacy", "explanation": "A set tracks visited vertices, but cannot maintain level-order sequencing."}
        ],
        "explanation": "BFS uses a FIFO queue to guarantee that vertices closer to the source are visited before vertices farther away."
    },
    {
        "concept_code": "DSA_GRAPHS",
        "difficulty": "intermediate",
        "title": "Shortest Path in Unweighted Graphs",
        "prompt": "In an unweighted graph, which algorithm is guaranteed to find the shortest path (minimum edge count) between two vertices?",
        "options": [
            {"index": 0, "text": "Depth-First Search (DFS)", "is_correct": False, "misconception_code": "DFS_SHORTEST_PATH_FALLACY", "misconception_name": "DFS Shortest Path Fallacy", "explanation": "DFS explores deep paths first and may return a non-optimal long path."},
            {"index": 1, "text": "Prim's Minimum Spanning Tree algorithm", "is_correct": False, "misconception_code": "MST_SHORTEST_PATH_CONFUSION", "misconception_name": "MST vs Shortest Path Confusion", "explanation": "Prim's finds a tree spanning all vertices with minimal total weight, not individual shortest paths."},
            {"index": 2, "text": "Breadth-First Search (BFS)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Because BFS explores vertices in non-decreasing distance from the start node, the first time target is popped, the shortest path is found."},
            {"index": 3, "text": "In-order Traversal", "is_correct": False, "misconception_code": "TREE_TRAVERSAL_ON_GRAPH", "misconception_name": "Tree Traversal on Graph", "explanation": "In-order traversal is only defined for binary trees."}
        ],
        "explanation": "BFS guarantees finding the path with the fewest edges in unweighted graphs because it explores outward in concentric distance rings."
    },
    {
        "concept_code": "DSA_GRAPHS",
        "difficulty": "intermediate",
        "title": "BFS Adjacency List Complexity",
        "prompt": "What is the time complexity of Breadth-First Search on a graph with V vertices and E edges represented by an adjacency list?",
        "options": [
            {"index": 0, "text": "O(V + E)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Every vertex is enqueued/dequeued once (O(V)), and every edge is examined once or twice (O(E))."},
            {"index": 1, "text": "O(V * E)", "is_correct": False, "misconception_code": "MULTIPLICATIVE_COMPLEXITY_FALLACY", "misconception_name": "Multiplicative Complexity Fallacy", "explanation": "Adjacency lists avoid iterating over all edges for each individual vertex."},
            {"index": 2, "text": "O(V^2)", "is_correct": False, "misconception_code": "ADJACENCY_MATRIX_CONFUSION", "misconception_name": "Adjacency Matrix Assumption", "explanation": "O(V^2) applies when BFS traverses an adjacency matrix, not an adjacency list."},
            {"index": 3, "text": "O(E log V)", "is_correct": False, "misconception_code": "DIJKSTRA_COMPLEXITY_CONFUSION", "misconception_name": "Dijkstra Complexity Confusion", "explanation": "O(E log V) is Dijkstra's complexity with a priority queue, not standard BFS."}
        ],
        "explanation": "With an adjacency list, BFS visits each vertex once and traverses each incident edge once, taking O(V + E) time."
    },
    {
        "concept_code": "DSA_GRAPHS",
        "difficulty": "advanced",
        "title": "Cycle Detection via DFS Edge Types",
        "prompt": "In a directed graph, the discovery of which edge type during Depth-First Search confirms the existence of a directed cycle?",
        "options": [
            {"index": 0, "text": "Tree edge", "is_correct": False, "misconception_code": "TREE_EDGE_CONFUSION", "misconception_name": "Tree Edge Confusion", "explanation": "Tree edges expand the DFS forest to unvisited vertices and cannot close a cycle."},
            {"index": 1, "text": "Forward edge", "is_correct": False, "misconception_code": "FORWARD_EDGE_CONFUSION", "misconception_name": "Forward Edge Confusion", "explanation": "Forward edges connect an ancestor to an already finished descendant in the tree."},
            {"index": 2, "text": "Cross edge", "is_correct": False, "misconception_code": "CROSS_EDGE_CONFUSION", "misconception_name": "Cross Edge Confusion", "explanation": "Cross edges connect vertices across different branches without an ancestor relationship."},
            {"index": 3, "text": "Back edge", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "A back edge points from a vertex to an active ancestor currently on the DFS call stack, forming a directed cycle."}
        ],
        "explanation": "A back edge connects a vertex to an active ancestor on the recursion stack, proving a closed directed cycle."
    },

    # --------------------------------------------------------------------------
    # DSA_DP (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "DSA_DP",
        "difficulty": "beginner",
        "title": "Dynamic Programming Core Properties",
        "prompt": "What are the two fundamental problem characteristics required for Dynamic Programming to be applicable?",
        "options": [
            {"index": 0, "text": "Greedy choice property and continuous state space", "is_correct": False, "misconception_code": "GREEDY_DP_CONFUSION", "misconception_name": "Greedy DP Confusion", "explanation": "Greedy problems make local choices without caching subproblems."},
            {"index": 1, "text": "Optimal substructure and overlapping subproblems", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "DP requires optimal solutions of subproblems to form global solutions, with identical subproblems being resolved repeatedly."},
            {"index": 2, "text": "Disjoint subproblems and divide-and-conquer independence", "is_correct": False, "misconception_code": "DIVIDE_CONQUER_CONFUSION", "misconception_name": "Divide and Conquer Confusion", "explanation": "Disjoint subproblems indicate standard Divide and Conquer (e.g., Merge Sort), not DP."},
            {"index": 3, "text": "Strict monotonicity and single-variable convexity", "is_correct": False, "misconception_code": "CONVEX_OPTIMIZATION_CONFUSION", "misconception_name": "Convex Optimization Confusion", "explanation": "Monotonicity is not a strict requirement for dynamic programming."}
        ],
        "explanation": "Dynamic programming applies when a problem exhibits both optimal substructure and overlapping subproblems."
    },
    {
        "concept_code": "DSA_DP",
        "difficulty": "intermediate",
        "title": "Top-Down vs Bottom-Up DP",
        "prompt": "What is the structural difference between Top-Down Memoization and Bottom-Up Tabulation in Dynamic Programming?",
        "options": [
            {"index": 0, "text": "Top-Down is asymptotically faster by an order of magnitude", "is_correct": False, "misconception_code": "ASYMPTOTIC_SPEED_FALLACY", "misconception_name": "Asymptotic Speed Fallacy", "explanation": "Both approaches solve the same subproblems and generally share identical Big-O complexity."},
            {"index": 1, "text": "Bottom-Up uses recursion with call stack overhead", "is_correct": False, "misconception_code": "RECURSION_DIRECTION_CONFUSION", "misconception_name": "Recursion Direction Inversion", "explanation": "Top-Down uses recursion; Bottom-Up uses iterative loops."},
            {"index": 2, "text": "Top-Down uses recursion with lookup cache; Bottom-Up iteratively fills a table starting from base cases", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Top-down starts from the target state and caches recursive results, while bottom-up builds iteratively from base cases."},
            {"index": 3, "text": "Top-Down requires exponential memory while Bottom-Up is always O(1) space", "is_correct": False, "misconception_code": "SPACE_COMPLEXITY_FALLACY", "misconception_name": "Space Complexity Fallacy", "explanation": "Both approaches typically use table or hash map storage proportional to the state space."}
        ],
        "explanation": "Top-Down memoizes recursive function calls, while Bottom-Up iteratively populates a state table starting from base conditions."
    },
    {
        "concept_code": "DSA_DP",
        "difficulty": "intermediate",
        "title": "Iterative Fibonacci Complexity",
        "prompt": "What is the time complexity of computing the n-th Fibonacci number using 1D Bottom-Up Dynamic Programming?",
        "options": [
            {"index": 0, "text": "O(n) time with O(1) space by tracking only the last two values", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "A single loop from 2 to n updating two variables computes Fib(n) in linear time with constant memory."},
            {"index": 1, "text": "O(2^n) exponential time", "is_correct": False, "misconception_code": "NAIVE_RECURSION_CONFUSION", "misconception_name": "Naive Recursion Confusion", "explanation": "O(2^n) is the runtime of unmemoized naive recursion, not dynamic programming."},
            {"index": 2, "text": "O(n^2) quadratic time", "is_correct": False, "misconception_code": "QUADRATIC_LOOP_CONFUSION", "misconception_name": "Quadratic Loop Misunderstanding", "explanation": "Each state requires only one addition of the preceding two values, taking O(1) per step."},
            {"index": 3, "text": "O(n log n) divide and conquer time", "is_correct": False, "misconception_code": "LOG_LINEAR_CONFUSION", "misconception_name": "Log-Linear Misconception", "explanation": "Fibonacci DP does not divide problem sizes."}
        ],
        "explanation": "Bottom-up DP evaluates each state F(i) = F(i-1) + F(i-2) in O(1) time across n iterations, taking O(n) total time."
    },
    {
        "concept_code": "DSA_DP",
        "difficulty": "advanced",
        "title": "0/1 Knapsack Pseudo-Polynomial Complexity",
        "prompt": "In the 0/1 Knapsack problem with n items and capacity W, why is the standard DP runtime O(n * W) termed pseudo-polynomial?",
        "options": [
            {"index": 0, "text": "Because it only produces an approximate decimal result", "is_correct": False, "misconception_code": "APPROXIMATION_CONFUSION", "misconception_name": "Approximation Confusion", "explanation": "The DP algorithm computes the exact global optimum."},
            {"index": 1, "text": "Because it requires polynomial space while running in exponential time", "is_correct": False, "misconception_code": "SPACE_TIME_INVERSION", "misconception_name": "Space Time Inversion", "explanation": "The term pseudo-polynomial specifically characterizes the time complexity dependence on numeric input values."},
            {"index": 2, "text": "Because the runtime depends on logarithmic tree depth", "is_correct": False, "misconception_code": "TREE_DEPTH_FALLACY", "misconception_name": "Tree Depth Fallacy", "explanation": "Knapsack DP uses a 2D table grid, not tree structures."},
            {"index": 3, "text": "Because W represents numeric magnitude, whose bit-length is log(W), making runtime exponential in input size", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Input length is proportional to the number of bits log(W). Since W = 2^(log W), O(n * W) is exponential with respect to the input length."}
        ],
        "explanation": "An algorithm is pseudo-polynomial when its runtime is polynomial in the numeric value of an input (W), which is exponential in its bit length log(W)."
    },

    # --------------------------------------------------------------------------
    # QC_SUPERPOSITION (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_SUPERPOSITION",
        "difficulty": "beginner",
        "title": "Qubit Normalization Condition",
        "prompt": "A pure single-qubit state is expressed as |psi> = alpha|0> + beta|1>. What constraint must the complex amplitudes satisfy?",
        "options": [
            {"index": 0, "text": "|alpha| + |beta| = 1", "is_correct": False, "misconception_code": "L1_NORM_FALLACY", "misconception_name": "L1 Norm Misconception", "explanation": "Classical probabilities sum linearly, but quantum amplitudes normalize via squared moduli."},
            {"index": 1, "text": "|alpha|^2 + |beta|^2 = 1", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By the Born rule, the sum of probabilities for all mutually exclusive outcomes must equal 1."},
            {"index": 2, "text": "alpha * beta = 0", "is_correct": False, "misconception_code": "ORTHOGONALITY_CONFUSION", "misconception_name": "Orthogonality Confusion", "explanation": "Amplitudes need not be zero; superposition allows non-zero alpha and beta."},
            {"index": 3, "text": "alpha^2 - beta^2 = 1", "is_correct": False, "misconception_code": "HYPERBOLIC_CONFUSION", "misconception_name": "Hyperbolic Norm Fallacy", "explanation": "State vectors exist in Euclidean/Hilbert space with positive definite norm."}
        ],
        "explanation": "Conservation of total probability dictates |alpha|^2 + |beta|^2 = 1."
    },
    {
        "concept_code": "QC_SUPERPOSITION",
        "difficulty": "intermediate",
        "title": "Superposition Measurement Probability",
        "prompt": "If a qubit is in the state |psi> = (1/sqrt(2))|0> + (1/sqrt(2))|1>, what is the probability of measuring the outcome 0?",
        "options": [
            {"index": 0, "text": "25% (0.25)", "is_correct": False, "misconception_code": "DOUBLE_SQUARING_FALLACY", "misconception_name": "Double Squaring Error", "explanation": "The amplitude is 1/sqrt(2), so squaring yields 1/2, not 1/4."},
            {"index": 1, "text": "100% (1.0)", "is_correct": False, "misconception_code": "DETERMINISTIC_COLLAPSE_FALLACY", "misconception_name": "Deterministic Fallacy", "explanation": "The qubit is in an equal superposition; measurement is probabilistic."},
            {"index": 2, "text": "50% (0.50)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By Born's rule, P(0) = |1/sqrt(2)|^2 = 1/2 = 50%."},
            {"index": 3, "text": "0% (0.0)", "is_correct": False, "misconception_code": "ZERO_PROBABILITY_FALLACY", "misconception_name": "Zero Probability Error", "explanation": "The amplitude for state |0> is non-zero."}
        ],
        "explanation": "According to Born's rule, P(0) = |alpha|^2 = |1/sqrt(2)|^2 = 0.50."
    },
    {
        "concept_code": "QC_SUPERPOSITION",
        "difficulty": "intermediate",
        "title": "Geometric State Representation",
        "prompt": "Geometrically, any pure single-qubit quantum state can be visualized as a point on the surface of which mathematical sphere?",
        "options": [
            {"index": 0, "text": "The Bloch Sphere", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The Bloch Sphere maps 2-dimensional complex state vectors onto a 3-dimensional unit sphere."},
            {"index": 1, "text": "The Riemann Horizon Sphere", "is_correct": False, "misconception_code": "RIEMANN_CONFUSION", "misconception_name": "Riemann Sphere Confusion", "explanation": "The Riemann sphere models the extended complex plane, not qubit spin coordinates."},
            {"index": 2, "text": "The Poincare Light Cone", "is_correct": False, "misconception_code": "RELATIVITY_CONFUSION", "misconception_name": "Minkowski Relativity Confusion", "explanation": "Light cones model spacetime causality in special relativity."},
            {"index": 3, "text": "The Hilbert Torus", "is_correct": False, "misconception_code": "TORUS_TOPOLOGY_CONFUSION", "misconception_name": "Torus Topology Misconception", "explanation": "Pure single qubit states have spherical S^2 topology, not toroidal."}
        ],
        "explanation": "Single pure qubit states are represented as unit vectors on the surface of the Bloch Sphere."
    },
    {
        "concept_code": "QC_SUPERPOSITION",
        "difficulty": "advanced",
        "title": "N-Qubit Hilbert Space Dimensionality",
        "prompt": "How many complex probability amplitudes are required to describe an arbitrary entangled pure state of n qubits?",
        "options": [
            {"index": 0, "text": "n", "is_correct": False, "misconception_code": "CLASSICAL_BIT_ASSUMPTION", "misconception_name": "Classical Scaling Fallacy", "explanation": "Classical states scale linearly (n bits), whereas quantum superposition spans the tensor product space."},
            {"index": 1, "text": "2n", "is_correct": False, "misconception_code": "INDEPENDENT_SUM_FALLACY", "misconception_name": "Independent Amplitudes Fallacy", "explanation": "Summing amplitudes linearly ignores entanglement across tensor products."},
            {"index": 2, "text": "n^2", "is_correct": False, "misconception_code": "QUADRATIC_SCALING_CONFUSION", "misconception_name": "Quadratic Dimension Confusion", "explanation": "n^2 is matrix dimension, not state vector length."},
            {"index": 3, "text": "2^n", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The Hilbert space of n qubits is the tensor product (C^2)^(tensor n), which has dimension 2^n."}
        ],
        "explanation": "Due to quantum tensor products, an n-qubit register exists in a 2^n dimensional complex Hilbert space."
    },

    # --------------------------------------------------------------------------
    # QC_GATES (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_GATES",
        "difficulty": "beginner",
        "title": "Hadamard Gate on Ground State",
        "prompt": "What is the resulting quantum state when a Hadamard gate (H) is applied to the computational basis state |0>?",
        "options": [
            {"index": 0, "text": "|1>", "is_correct": False, "misconception_code": "BIT_FLIP_CONFUSION", "misconception_name": "Pauli-X Bit Flip Confusion", "explanation": "The Pauli-X gate flips |0> to |1>, not the Hadamard gate."},
            {"index": 1, "text": "|+> = (1/sqrt(2))(|0> + |1>)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The Hadamard gate maps basis states into equal superposition: H|0> = |+>."},
            {"index": 2, "text": "|-> = (1/sqrt(2))(|0> - |1>)", "is_correct": False, "misconception_code": "PHASE_SIGN_CONFUSION", "misconception_name": "Phase Inversion Error", "explanation": "H|1> yields |-> with a minus sign; H|0> yields |+> with positive phase."},
            {"index": 3, "text": "i|0>", "is_correct": False, "misconception_code": "PHASE_GATE_CONFUSION", "misconception_name": "Phase Gate Confusion", "explanation": "Adding an imaginary phase factor is done by the S or T gate."}
        ],
        "explanation": "Applying H to |0> produces the balanced superposition |+> = (1/sqrt(2))(|0> + |1>)."
    },
    {
        "concept_code": "QC_GATES",
        "difficulty": "intermediate",
        "title": "Quantum Gate Unitarity",
        "prompt": "All valid quantum logic operations represented by matrices U must satisfy which condition to preserve state normalization?",
        "options": [
            {"index": 0, "text": "They must have a determinant of exactly 0", "is_correct": False, "misconception_code": "SINGULAR_MATRIX_FALLACY", "misconception_name": "Singular Matrix Fallacy", "explanation": "A determinant of zero means non-invertible information loss, violating quantum reversibility."},
            {"index": 1, "text": "They must be strictly diagonal matrices", "is_correct": False, "misconception_code": "DIAGONAL_GATE_RESTRICTION", "misconception_name": "Diagonal Restriction Misconception", "explanation": "Gates like Pauli-X and Hadamard have non-zero off-diagonal terms."},
            {"index": 2, "text": "They must be Unitary (U_dagger * U = I)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Unitary operators preserve inner products and length, guaranteeing that total probability remains 1."},
            {"index": 3, "text": "They must contain exclusively non-negative real numbers", "is_correct": False, "misconception_code": "STOCHASTIC_MATRIX_CONFUSION", "misconception_name": "Classical Markov Matrix Confusion", "explanation": "Quantum amplitudes are complex numbers with both positive and negative phases."}
        ],
        "explanation": "Quantum gates must be unitary (U^dagger U = I) to ensure all probability amplitudes remain normalized to 1."
    },
    {
        "concept_code": "QC_GATES",
        "difficulty": "intermediate",
        "title": "Pauli-X Operation",
        "prompt": "What is the algebraic action of the Pauli-X gate applied to the computational basis state |1>?",
        "options": [
            {"index": 0, "text": "|0> (Quantum NOT operation)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The Pauli-X matrix [[0, 1], [1, 0]] exchanges amplitudes, transforming |1> into |0>."},
            {"index": 1, "text": "-|1> (Phase flip)", "is_correct": False, "misconception_code": "PAULI_Z_CONFUSION", "misconception_name": "Pauli-Z Confusion", "explanation": "The Pauli-Z gate flips the phase of |1> to -|1>, without changing the bit value."},
            {"index": 2, "text": "i|1>", "is_correct": False, "misconception_code": "PHASE_ROTATION_CONFUSION", "misconception_name": "Phase Rotation Confusion", "explanation": "Pauli-X does not introduce imaginary phase on computational basis vectors."},
            {"index": 3, "text": "|+>", "is_correct": False, "misconception_code": "HADAMARD_CONFUSION", "misconception_name": "Hadamard Confusion", "explanation": "Pauli-X is a discrete bit flip, not a superposition generator."}
        ],
        "explanation": "The Pauli-X gate acts as a quantum NOT gate, flipping |0> to |1> and |1> to |0>."
    },
    {
        "concept_code": "QC_GATES",
        "difficulty": "advanced",
        "title": "CNOT Gate Behavior",
        "prompt": "Under what exact condition does the two-qubit Controlled-NOT (CNOT) gate flip the state of the target qubit?",
        "options": [
            {"index": 0, "text": "When the target qubit is in state |+>", "is_correct": False, "misconception_code": "TARGET_TRIGGER_CONFUSION", "misconception_name": "Target State Trigger Fallacy", "explanation": "The control qubit determines the operation, not the target qubit's state."},
            {"index": 1, "text": "When an external classical measurement occurs", "is_correct": False, "misconception_code": "MEASUREMENT_TRIGGER_FALLACY", "misconception_name": "Measurement Required Fallacy", "explanation": "CNOT is a unitary coherent gate, operating without measurement."},
            {"index": 2, "text": "When the control qubit is in state |0>", "is_correct": False, "misconception_code": "INVERTED_CONTROL_LOGIC", "misconception_name": "Inverted Control Logic", "explanation": "If control is |0>, CNOT acts as identity and leaves target unchanged."},
            {"index": 3, "text": "When the control qubit is in state |1>", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The CNOT matrix maps |10> -> |11> and |11> -> |10>, flipping target if and only if control is |1>."}
        ],
        "explanation": "A CNOT gate applies a Pauli-X (NOT) operation to the target qubit when the control qubit is in the |1> state."
    },

    # --------------------------------------------------------------------------
    # QC_ENTANGLEMENT (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_ENTANGLEMENT",
        "difficulty": "beginner",
        "title": "Bell State Circuit Construction",
        "prompt": "Which quantum circuit generates the canonical Bell state |Phi+> = (1/sqrt(2))(|00> + |11>) from initial state |00>?",
        "options": [
            {"index": 0, "text": "Applying Pauli-X to both qubits simultaneously", "is_correct": False, "misconception_code": "SEPARABLE_X_CONFUSION", "misconception_name": "Separable Bit Flip Fallacy", "explanation": "X|0> * X|0> yields |11>, which is a separable product state, not entangled."},
            {"index": 1, "text": "Applying a Hadamard gate to qubit 0, followed by a CNOT with control qubit 0 and target qubit 1", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "H on qubit 0 produces (1/sqrt(2))(|0>+|1>)|0> = (1/sqrt(2))(|00>+|10>). CNOT then maps |10> to |11>, giving (1/sqrt(2))(|00>+|11>)."},
            {"index": 2, "text": "Applying two CNOT gates in series with swapped control qubits", "is_correct": False, "misconception_code": "DOUBLE_CNOT_FALLACY", "misconception_name": "Double CNOT Fallacy", "explanation": "CNOT cannot generate superposition from computational basis inputs without a Hadamard gate."},
            {"index": 3, "text": "Measuring qubit 0 and transmitting the bit to qubit 1", "is_correct": False, "misconception_code": "CLASSICAL_CHANNEL_CONFUSION", "misconception_name": "Classical Teleportation Confusion", "explanation": "Measurement destroys coherence and cannot create quantum entanglement."}
        ],
        "explanation": "Applying H to the first qubit creates superposition, and the subsequent CNOT creates entanglement."
    },
    {
        "concept_code": "QC_ENTANGLEMENT",
        "difficulty": "intermediate",
        "title": "No-Cloning Theorem",
        "prompt": "What fundamental principle of quantum mechanics states that an arbitrary unknown quantum state cannot be replicated exactly?",
        "options": [
            {"index": 0, "text": "Bell's Inequality", "is_correct": False, "misconception_code": "BELL_INEQUALITY_CONFUSION", "misconception_name": "Bell Inequality Confusion", "explanation": "Bell's inequality tests whether local hidden variable models can explain quantum correlations."},
            {"index": 1, "text": "Heisenberg Uncertainty Principle", "is_correct": False, "misconception_code": "UNCERTAINTY_CONFUSION", "misconception_name": "Uncertainty Principle Confusion", "explanation": "The uncertainty principle bounds measurement precision of conjugate variables (e.g. position and momentum)."},
            {"index": 2, "text": "The No-Cloning Theorem", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The linearity of unitary quantum mechanics makes it mathematically impossible to build a universal cloning machine U|psi>|0> = |psi>|psi>."},
            {"index": 3, "text": "Pauli Exclusion Principle", "is_correct": False, "misconception_code": "FERMION_EXCLUSION_CONFUSION", "misconception_name": "Pauli Exclusion Confusion", "explanation": "Pauli exclusion applies to identical fermions in atomic orbitals."}
        ],
        "explanation": "The No-Cloning theorem proves that linearity of unitary operators forbids copying an unknown arbitrary quantum state."
    },
    {
        "concept_code": "QC_ENTANGLEMENT",
        "difficulty": "intermediate",
        "title": "Entangled Pair Measurement Correlation",
        "prompt": "For the Bell state |Phi+> = (1/sqrt(2))(|00> + |11>), if measuring qubit 0 yields the outcome 1, what is the state of qubit 1?",
        "options": [
            {"index": 0, "text": "It collapses immediately to |1> with 100% certainty", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The only component of |Phi+> compatible with qubit 0 being 1 is |11>. Hence qubit 1 collapses to |1> with probability 1."},
            {"index": 1, "text": "It remains in an equal 50/50 superposition", "is_correct": False, "misconception_code": "INDEPENDENT_COLLAPSE_FALLACY", "misconception_name": "Independent Collapse Fallacy", "explanation": "The two qubits are entangled; measuring one updates the joint state vector instantaneously."},
            {"index": 2, "text": "It collapses to |0> due to anti-correlation", "is_correct": False, "misconception_code": "SINGLET_CONFUSION", "misconception_name": "Singlet State Confusion", "explanation": "Anti-correlation occurs in |Psi-> = (1/sqrt(2))(|01> - |10>), not |Phi+>."},
            {"index": 3, "text": "It enters an unobservable mixed noise state", "is_correct": False, "misconception_code": "DECOHERENCE_CONFUSION", "misconception_name": "Decoherence Noise Confusion", "explanation": "Projective measurement collapses the register into a well-defined basis state."}
        ],
        "explanation": "In |Phi+>, measuring qubit 0 as 1 projects the joint state onto |11>, instantly collapsing qubit 1 to |1>."
    },
    {
        "concept_code": "QC_ENTANGLEMENT",
        "difficulty": "advanced",
        "title": "Superluminal Signaling Restriction",
        "prompt": "Why does quantum entanglement NOT enable faster-than-light (superluminal) communication between separated observers?",
        "options": [
            {"index": 0, "text": "Because entanglement decays after traveling a few meters", "is_correct": False, "misconception_code": "DISTANCE_LIMIT_FALLACY", "misconception_name": "Distance Limitation Fallacy", "explanation": "Entanglement has been verified across satellite distances over 1,200 km."},
            {"index": 1, "text": "Because photons cannot travel faster than light", "is_correct": False, "misconception_code": "PHOTON_SPEED_TRIVIALITY", "misconception_name": "Photon Speed Triviality", "explanation": "The question concerns instantaneous correlation, not physical carrier speed."},
            {"index": 2, "text": "Because measuring a qubit requires cooling to absolute zero", "is_correct": False, "misconception_code": "TEMPERATURE_CONFUSION", "misconception_name": "Cryogenic Confusion", "explanation": "Hardware cooling constraints do not define the fundamental information-theoretic limits."},
            {"index": 3, "text": "Because local measurement outcomes are completely random, requiring a classical channel to compare results (No-Communication Theorem)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "An observer cannot control the random outcome of their measurement. Without a classical comparison channel, local density matrices remain identical."}
        ],
        "explanation": "The No-Communication theorem proves that local measurements on entangled states yield uniformly random results that cannot transmit signals without classical communication."
    },

    # --------------------------------------------------------------------------
    # QC_MEASUREMENT (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_MEASUREMENT",
        "difficulty": "beginner",
        "title": "Wavefunction Collapse Dynamics",
        "prompt": "What happens to a qubit in superposition upon undergoing a projective measurement in the computational basis?",
        "options": [
            {"index": 0, "text": "It retains its continuous superposition while copying state data", "is_correct": False, "misconception_code": "NON_DESTRUCTIVE_MEASUREMENT_FALLACY", "misconception_name": "Non-Destructive Measurement Fallacy", "explanation": "Projective measurement alters the state vector non-reversibly."},
            {"index": 1, "text": "The wavefunction collapses irreversibly to either |0> or |1>", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Measurement forces the qubit into one of the eigenstates of the measurement operator."},
            {"index": 2, "text": "It converts into an entangled pair of photons", "is_correct": False, "misconception_code": "PAIR_PRODUCTION_CONFUSION", "misconception_name": "Pair Production Confusion", "explanation": "Measurement does not create new physical particles."},
            {"index": 3, "text": "Its phase angle rotates continuously by pi/2", "is_correct": False, "misconception_code": "UNITARY_ROTATION_CONFUSION", "misconception_name": "Unitary vs Projection Confusion", "explanation": "Measurement is a non-unitary projection, not a continuous rotation."}
        ],
        "explanation": "Projective measurement collapses the qubit's wavefunction probabilistically into one of the measurement basis states."
    },
    {
        "concept_code": "QC_MEASUREMENT",
        "difficulty": "intermediate",
        "title": "Born Rule Calculation",
        "prompt": "If |psi> = (sqrt(3)/2)|0> - (1/2)|1>, what is the probability of measuring the outcome 1 in the computational basis?",
        "options": [
            {"index": 0, "text": "75% (0.75)", "is_correct": False, "misconception_code": "STATE_ZERO_AMPLITUDE_SQUARED", "misconception_name": "Wrong Amplitude Squaring", "explanation": "0.75 is |sqrt(3)/2|^2, which is the probability of measuring state |0>."},
            {"index": 1, "text": "50% (0.50)", "is_correct": False, "misconception_code": "UNIFORM_PROBABILITY_ASSUMPTION", "misconception_name": "Uniform Probability Assumption", "explanation": "The amplitudes sqrt(3)/2 and -1/2 are unequal, so probabilities are not 50/50."},
            {"index": 2, "text": "25% (0.25)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By Born's rule, P(1) = |-1/2|^2 = 1/4 = 0.25 = 25%."},
            {"index": 3, "text": "-25% (Negative probability)", "is_correct": False, "misconception_code": "NEGATIVE_PROBABILITY_FALLACY", "misconception_name": "Negative Probability Fallacy", "explanation": "Probabilities are squared magnitudes |beta|^2 and are always non-negative real numbers."}
        ],
        "explanation": "The probability of measuring |1> is |-1/2|^2 = 1/4 = 0.25."
    },
    {
        "concept_code": "QC_MEASUREMENT",
        "difficulty": "intermediate",
        "title": "Quantum Measurement Postulate",
        "prompt": "Which foundational rule dictates that the probability of obtaining outcome m is given by P(m) = <psi|M_m^dagger M_m|psi>?",
        "options": [
            {"index": 0, "text": "Born's Rule", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Formulated by Max Born in 1926, the Born rule links quantum state vectors to observable measurement probabilities."},
            {"index": 1, "text": "Bayes' Theorem", "is_correct": False, "misconception_code": "CLASSICAL_INFERENCE_CONFUSION", "misconception_name": "Bayesian Inference Confusion", "explanation": "Bayes' theorem is a classical mathematical formula for conditional probability."},
            {"index": 2, "text": "Ampere's Law", "is_correct": False, "misconception_code": "ELECTROMAGNETISM_CONFUSION", "misconception_name": "Electromagnetism Confusion", "explanation": "Ampere's law relates magnetic fields to electric currents in classical physics."},
            {"index": 3, "text": "Shannon's Theorem", "is_correct": False, "misconception_code": "INFORMATION_THEORY_CONFUSION", "misconception_name": "Classical Information Confusion", "explanation": "Shannon's theorem bounds data compression and noisy channel limits."}
        ],
        "explanation": "Born's Rule provides the mathematical formula connecting quantum state amplitudes to physical measurement probabilities."
    },
    {
        "concept_code": "QC_MEASUREMENT",
        "difficulty": "advanced",
        "title": "Hadamard Basis Measurement",
        "prompt": "If a qubit in state |0> is measured in the Hadamard basis {|+>, |->}, what are the probabilities of outcomes |+> and |->?",
        "options": [
            {"index": 0, "text": "100% for |+> and 0% for |->", "is_correct": False, "misconception_code": "GROUND_STATE_BIAS", "misconception_name": "Ground State Bias", "explanation": "In the Hadamard basis, |0> = (1/sqrt(2))(|+> + |->), which is a superposition."},
            {"index": 1, "text": "0% for |+> and 100% for |->", "is_correct": False, "misconception_code": "INVERTED_BASIS_FALLACY", "misconception_name": "Inverted Basis Fallacy", "explanation": "|0> has equal projection onto both |+> and |->."},
            {"index": 2, "text": "Undefined because basis conversion is physically forbidden", "is_correct": False, "misconception_code": "BASIS_FORBIDDEN_FALLACY", "misconception_name": "Basis Forbidden Fallacy", "explanation": "Measuring in the Hadamard basis is routinely performed by applying an H gate prior to standard measurement."},
            {"index": 3, "text": "50% for |+> and 50% for |->", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "|<+|0>|^2 = |1/sqrt(2)|^2 = 1/2, and |<-|0>|^2 = |1/sqrt(2)|^2 = 1/2."}
        ],
        "explanation": "Because |0> = (1/sqrt(2))(|+> + |->), measuring in the Hadamard basis yields outcomes |+> and |-> with equal 50% probability."
    },

    # --------------------------------------------------------------------------
    # ENG_BOOLEAN_LOGIC (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "ENG_BOOLEAN_LOGIC",
        "difficulty": "beginner",
        "title": "NAND Gate Truth Table",
        "prompt": "Which logic gate outputs a LOW (0) voltage if and only if all of its input terminals are HIGH (1)?",
        "options": [
            {"index": 0, "text": "AND gate", "is_correct": False, "misconception_code": "AND_INVERSION_CONFUSION", "misconception_name": "AND Inversion Confusion", "explanation": "An AND gate outputs HIGH (1) when all inputs are 1."},
            {"index": 1, "text": "NAND gate", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "A NAND gate is an inverted AND: it outputs 0 only when every input is 1."},
            {"index": 2, "text": "NOR gate", "is_correct": False, "misconception_code": "NOR_CONFUSION", "misconception_name": "NOR Gate Confusion", "explanation": "A NOR gate outputs 0 whenever ANY input is 1."},
            {"index": 3, "text": "XOR gate", "is_correct": False, "misconception_code": "XOR_CONFUSION", "misconception_name": "XOR Gate Confusion", "explanation": "An XOR gate outputs 0 when inputs are equal, including when all inputs are 0."}
        ],
        "explanation": "The NAND (Not-AND) gate produces a 0 only when all inputs are 1."
    },
    {
        "concept_code": "ENG_BOOLEAN_LOGIC",
        "difficulty": "intermediate",
        "title": "De Morgan's Theorem Application",
        "prompt": "According to De Morgan's Laws, what is the exact algebraic equivalent of the negated conjunction ~(A * B)?",
        "options": [
            {"index": 0, "text": "~A * ~B", "is_correct": False, "misconception_code": "INCOMPLETE_DEMORGAN_FALLACY", "misconception_name": "Literal Negation Fallacy", "explanation": "De Morgan's law requires changing the AND operator to an OR operator."},
            {"index": 1, "text": "A + B", "is_correct": False, "misconception_code": "DROPPED_NEGATION_FALLACY", "misconception_name": "Dropped Inversion Error", "explanation": "The individual variables must remain inverted: ~A + ~B."},
            {"index": 2, "text": "~A + ~B", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "De Morgan's first theorem establishes that ~(A * B) = ~A + ~B."},
            {"index": 3, "text": "~(A + B)", "is_correct": False, "misconception_code": "NOR_EQUIVALENCE_FALLACY", "misconception_name": "NOR Equivalence Fallacy", "explanation": "~(A + B) is equal to ~A * ~B, not ~(A * B)."}
        ],
        "explanation": "De Morgan's law states that the complement of a product equals the sum of the complements: ~(A * B) = ~A + ~B."
    },
    {
        "concept_code": "ENG_BOOLEAN_LOGIC",
        "difficulty": "intermediate",
        "title": "Universal Gate Property",
        "prompt": "Why are NAND and NOR gates classified as 'Universal Gates' in digital system design?",
        "options": [
            {"index": 0, "text": "Because any arbitrary Boolean logic function can be constructed using solely NAND or solely NOR gates", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "NAND and NOR gates can implement NOT, AND, and OR operations, enabling complete circuit synthesis."},
            {"index": 1, "text": "Because they operate without ground connections", "is_correct": False, "misconception_code": "FLOATING_GROUND_FALLACY", "misconception_name": "Floating Ground Fallacy", "explanation": "All physical digital logic ICs require power (Vcc) and ground (GND)."},
            {"index": 2, "text": "Because their propagation delay is mathematically zero", "is_correct": False, "misconception_code": "ZERO_DELAY_FALLACY", "misconception_name": "Zero Propagation Delay Fallacy", "explanation": "Physical transistors exhibit finite gate switching propagation delays."},
            {"index": 3, "text": "Because they accept an infinite number of input lines", "is_correct": False, "misconception_code": "FAN_IN_FALLACY", "misconception_name": "Infinite Fan-In Fallacy", "explanation": "Physical logic gates have finite fan-in limits dictated by drive current and capacitance."}
        ],
        "explanation": "NAND and NOR gates are universal because a network of either can implement any combinational or sequential logic circuit."
    },
    {
        "concept_code": "ENG_BOOLEAN_LOGIC",
        "difficulty": "advanced",
        "title": "Boolean Simplification Theorem",
        "prompt": "What is the minimal simplified form of the Boolean expression F = A + (~A * B)?",
        "options": [
            {"index": 0, "text": "A", "is_correct": False, "misconception_code": "ABSORPTION_MISAPPLICATION", "misconception_name": "Absorption Misapplication", "explanation": "A + AB simplifies to A, but A + ~AB retains B."},
            {"index": 1, "text": "B", "is_correct": False, "misconception_code": "DOMINANT_TERM_CONFUSION", "misconception_name": "Dominant Term Confusion", "explanation": "Setting A=1 makes F=1 even if B=0, so F cannot simply equal B."},
            {"index": 2, "text": "A * B", "is_correct": False, "misconception_code": "AND_COLLAPSE_FALLACY", "misconception_name": "AND Collapse Fallacy", "explanation": "F is a sum of products, not a product."},
            {"index": 3, "text": "A + B", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By distributivity: A + ~A*B = (A + ~A)(A + B) = 1 * (A + B) = A + B."}
        ],
        "explanation": "Using the distributive rule, A + ~AB = (A + ~A)(A + B) = 1 * (A + B) = A + B."
    },

    # --------------------------------------------------------------------------
    # ENG_COMBINATIONAL (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "ENG_COMBINATIONAL",
        "difficulty": "beginner",
        "title": "K-Map Gray Code Cell Sequence",
        "prompt": "Why are row and column headings in a Karnaugh Map (K-Map) sequenced in Gray code (00, 01, 11, 10)?",
        "options": [
            {"index": 0, "text": "To make arithmetic addition faster", "is_correct": False, "misconception_code": "ARITHMETIC_SPEED_FALLACY", "misconception_name": "Arithmetic Speed Fallacy", "explanation": "K-maps are used for algebraic minimization, not execution arithmetic."},
            {"index": 1, "text": "So that adjacent cells differ by exactly one binary variable, enabling algebraic grouping", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Unit distance between adjacent cells allows combining minterms via x + ~x = 1."},
            {"index": 2, "text": "To ensure compatible clock edge synchronization", "is_correct": False, "misconception_code": "CLOCK_TIMING_CONFUSION", "misconception_name": "Clock Timing Confusion", "explanation": "Combinational circuits and K-maps have no clock signals."},
            {"index": 3, "text": "To prevent floating ground oscillations", "is_correct": False, "misconception_code": "ANALOG_OSCILLATION_CONFUSION", "misconception_name": "Analog Noise Confusion", "explanation": "Gray coding in K-maps is a mathematical tool for Boolean minimization."}
        ],
        "explanation": "Gray code ensures adjacent cells change by only 1 bit, allowing terms differing by a literal to combine and eliminate that variable."
    },
    {
        "concept_code": "ENG_COMBINATIONAL",
        "difficulty": "intermediate",
        "title": "Multiplexer Select Line Requirement",
        "prompt": "How many select control lines (s) are required to address a 16-to-1 Multiplexer (MUX)?",
        "options": [
            {"index": 0, "text": "2 lines", "is_correct": False, "misconception_code": "LOG2_UNDERSHOOT", "misconception_name": "Undershot Selection", "explanation": "2 select lines address 2^2 = 4 input channels."},
            {"index": 1, "text": "8 lines", "is_correct": False, "misconception_code": "HALF_INPUT_FALLACY", "misconception_name": "Half Input Fallacy", "explanation": "Select lines decode inputs exponentially (2^s), not linearly (s = n/2)."},
            {"index": 2, "text": "4 lines", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "A multiplexer with 2^s inputs requires s select lines: 2^4 = 16, so 4 select lines are needed."},
            {"index": 3, "text": "16 lines", "is_correct": False, "misconception_code": "ONE_HOT_CONFUSION", "misconception_name": "One-Hot Select Confusion", "explanation": "Multiplexers use binary decoded select lines, not one-hot select lines."}
        ],
        "explanation": "For an N-to-1 MUX, the number of select lines is s = log_2(N). For N = 16, s = log_2(16) = 4."
    },
    {
        "concept_code": "ENG_COMBINATIONAL",
        "difficulty": "intermediate",
        "title": "Half Adder vs Full Adder",
        "prompt": "What is the structural difference between a Half Adder and a Full Adder circuit?",
        "options": [
            {"index": 0, "text": "A Full Adder includes a Carry-In (Cin) input from previous stages, whereas a Half Adder only adds two 1-bit inputs", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Half adders compute Sum = A ^ B and Cout = A * B. Full adders accept A, B, and Cin to enable multi-bit ripple addition."},
            {"index": 1, "text": "A Half Adder uses clock pulses while a Full Adder is purely asynchronous", "is_correct": False, "misconception_code": "SEQUENTIAL_ADDER_CONFUSION", "misconception_name": "Sequential Adder Confusion", "explanation": "Both half and full adders are purely combinational circuits."},
            {"index": 2, "text": "A Full Adder has only one output terminal", "is_correct": False, "misconception_code": "SINGLE_OUTPUT_FALLACY", "misconception_name": "Single Output Fallacy", "explanation": "Both adder circuits produce two outputs: Sum and Carry-out."},
            {"index": 3, "text": "A Half Adder supports floating point while a Full Adder only supports integers", "is_correct": False, "misconception_code": "ALU_DATATYPE_CONFUSION", "misconception_name": "Data Type Misconception", "explanation": "Both circuits operate on binary bits (0 or 1)."}
        ],
        "explanation": "A full adder accepts three inputs (A, B, Cin) while a half adder only handles two inputs (A, B) without carry-in."
    },
    {
        "concept_code": "ENG_COMBINATIONAL",
        "difficulty": "advanced",
        "title": "K-Map Valid Group Sizes",
        "prompt": "When grouping 1s in a Karnaugh Map for product-of-sums or sum-of-products minimization, what group sizes are mathematically valid?",
        "options": [
            {"index": 0, "text": "Any integer size: 1, 2, 3, 4, 5, 6", "is_correct": False, "misconception_code": "ANY_INTEGER_GROUP_FALLACY", "misconception_name": "Arbitrary Group Size Fallacy", "explanation": "Groups of 3, 5, or 6 cannot eliminate variables algebraically."},
            {"index": 1, "text": "Even numbers only: 2, 4, 6, 8, 10", "is_correct": False, "misconception_code": "EVEN_NUMBER_FALLACY", "misconception_name": "Even Number Fallacy", "explanation": "6 and 10 are not powers of two and cannot form valid K-map loops."},
            {"index": 2, "text": "Prime numbers only: 2, 3, 5, 7", "is_correct": False, "misconception_code": "PRIME_GROUP_CONFUSION", "misconception_name": "Prime Number Confusion", "explanation": "Prime numbers do not match Boolean hypercube faces."},
            {"index": 3, "text": "Strictly powers of two: 1, 2, 4, 8, or 16", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Grouping 2^k adjacent cells eliminates k Boolean variables from the product term."}
        ],
        "explanation": "K-map groups must be rectangular and contain 2^k cells (1, 2, 4, 8, 16) to eliminate k variables."
    },

    # --------------------------------------------------------------------------
    # ENG_SEQUENTIAL (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "ENG_SEQUENTIAL",
        "difficulty": "beginner",
        "title": "Latch vs Flip-Flop Triggering",
        "prompt": "What is the defining operational difference between a latch and a flip-flop?",
        "options": [
            {"index": 0, "text": "Latches store bytes while flip-flops store only single bits", "is_correct": False, "misconception_code": "BIT_CAPACITY_FALLACY", "misconception_name": "Bit Capacity Fallacy", "explanation": "Both standard basic latches and flip-flops store a single bit of state."},
            {"index": 1, "text": "A latch is level-sensitive (transparent while enabled), while a flip-flop is edge-triggered (samples on clock transition)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Latches continuously reflect data while the enable is active; flip-flops only capture data during a rising or falling clock edge."},
            {"index": 2, "text": "Flip-flops do not require power supply connections", "is_correct": False, "misconception_code": "PASSIVE_STORAGE_CONFUSION", "misconception_name": "Passive Storage Fallacy", "explanation": "Both are active electronic semiconductor circuits."},
            {"index": 3, "text": "Latches cannot be used in digital computers", "is_correct": False, "misconception_code": "PRACTICAL_USE_FALLACY", "misconception_name": "Practical Use Misconception", "explanation": "Latches are widely utilized in SRAM cells and pipeline registers."}
        ],
        "explanation": "Latches are transparent during active voltage levels, whereas flip-flops update state only on clock transition edges."
    },
    {
        "concept_code": "ENG_SEQUENTIAL",
        "difficulty": "intermediate",
        "title": "SR Latch Prohibited Input State",
        "prompt": "In an active-HIGH SR latch built with NOR gates, what occurs when both S = 1 and R = 1 are asserted simultaneously?",
        "options": [
            {"index": 0, "text": "The latch reliably toggles its output state", "is_correct": False, "misconception_code": "TOGGLE_CONFUSION", "misconception_name": "JK Toggle Confusion", "explanation": "Toggling on 1-1 occurs in JK flip-flops, not SR latches."},
            {"index": 1, "text": "The latch retains its previous state Q", "is_correct": False, "misconception_code": "HOLD_CONDITION_CONFUSION", "misconception_name": "Hold Condition Confusion", "explanation": "Hold occurs when S = 0 and R = 0 in an active-HIGH NOR latch."},
            {"index": 2, "text": "An invalid/prohibited state occurs forcing both Q and ~Q to 0, causing a race condition upon release", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "S=1 and R=1 forces both NOR outputs to 0 (violating Q != ~Q). When inputs drop back to 0, propagation delays determine an unpredictable race."},
            {"index": 3, "text": "The circuit disconnects from the output bus", "is_correct": False, "misconception_code": "HIGH_Z_CONFUSION", "misconception_name": "Tri-State Confusion", "explanation": "NOR latches do not enter high-impedance mode."}
        ],
        "explanation": "S=1 and R=1 is prohibited in NOR latches because it forces both outputs to 0 and induces a race condition."
    },
    {
        "concept_code": "ENG_SEQUENTIAL",
        "difficulty": "intermediate",
        "title": "JK Flip-Flop Toggle Mode",
        "prompt": "What is the next-state behavior of a JK flip-flop when both J = 1 and K = 1 on the arrival of an active clock edge?",
        "options": [
            {"index": 0, "text": "The output toggles (Q_next = ~Q)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "JK flip-flops resolve the SR latch invalid state by defining J=1, K=1 as the toggle condition."},
            {"index": 1, "text": "The output resets to 0 regardless of prior state", "is_correct": False, "misconception_code": "RESET_OVERRIDE_FALLACY", "misconception_name": "Reset Dominance Fallacy", "explanation": "Reset occurs when J=0 and K=1, not when both are 1."},
            {"index": 2, "text": "The output sets to 1 unconditionally", "is_correct": False, "misconception_code": "SET_OVERRIDE_FALLACY", "misconception_name": "Set Dominance Fallacy", "explanation": "Set occurs when J=1 and K=0."},
            {"index": 3, "text": "An indeterminate metastable glitch occurs", "is_correct": False, "misconception_code": "SR_INVALID_CONFUSION", "misconception_name": "SR Invalid Confusion", "explanation": "JK flip-flops eliminate invalid states by feeding output back into input AND gates."}
        ],
        "explanation": "When J=1 and K=1, the JK flip-flop inverts its output on each active clock edge."
    },
    {
        "concept_code": "ENG_SEQUENTIAL",
        "difficulty": "advanced",
        "title": "Flip-Flop Setup Time Constraint",
        "prompt": "In digital synchronous timing analysis, what does the 'Setup Time' (t_su) of an edge-triggered flip-flop specify?",
        "options": [
            {"index": 0, "text": "The time required for the power supply voltage to stabilize after boot", "is_correct": False, "misconception_code": "POWERUP_DELAY_CONFUSION", "misconception_name": "Power-up Timing Confusion", "explanation": "Setup time is a dynamic clocking constraint, not board power-on sequencing."},
            {"index": 1, "text": "The propagation delay between clock edge and output Q change", "is_correct": False, "misconception_code": "CLK_TO_Q_CONFUSION", "misconception_name": "Clock-to-Q Delay Confusion", "explanation": "The delay from clock edge to valid output is t_cq, not setup time t_su."},
            {"index": 2, "text": "The minimum pulse width of the clock HIGH period", "is_correct": False, "misconception_code": "CLOCK_WIDTH_CONFUSION", "misconception_name": "Clock Pulse Width Confusion", "explanation": "Minimum clock high/low time is a separate clock specification."},
            {"index": 3, "text": "The minimum duration the data input (D) must remain stable BEFORE the active clock edge arrives", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Violating setup time (changing D too close to the clock edge) causes internal metastability."}
        ],
        "explanation": "Setup time t_su is the minimum time data must remain constant before the clock edge to prevent metastability."
    },

    # --------------------------------------------------------------------------
    # ENG_CPU_ARCH (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "ENG_CPU_ARCH",
        "difficulty": "beginner",
        "title": "CPU Control Unit Role",
        "prompt": "Which component of the central processing unit is responsible for decoding instruction opcodes and coordinating system control signals?",
        "options": [
            {"index": 0, "text": "Arithmetic Logic Unit (ALU)", "is_correct": False, "misconception_code": "ALU_ROLE_CONFUSION", "misconception_name": "ALU Role Confusion", "explanation": "The ALU performs arithmetic and logical operations, not instruction decoding."},
            {"index": 1, "text": "Control Unit (CU)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The Control Unit interprets instructions from the Instruction Register and generates multiplexer, register load, and ALU select signals."},
            {"index": 2, "text": "Data Bus Buffer", "is_correct": False, "misconception_code": "BUS_BUFFER_CONFUSION", "misconception_name": "Bus Buffer Confusion", "explanation": "Bus buffers isolate signal lines electrically."},
            {"index": 3, "text": "Floating Point Unit (FPU)", "is_correct": False, "misconception_code": "FPU_CONFUSION", "misconception_name": "FPU Confusion", "explanation": "The FPU executes IEEE-754 floating point arithmetic."}
        ],
        "explanation": "The Control Unit orchestrates CPU instruction fetch, decode, and execute cycles by driving control signals."
    },
    {
        "concept_code": "ENG_CPU_ARCH",
        "difficulty": "intermediate",
        "title": "Program Counter Register Function",
        "prompt": "What is the primary function of the Program Counter (PC) register in a classical CPU architecture?",
        "options": [
            {"index": 0, "text": "Tracking total instruction cycles executed since CPU power-on", "is_correct": False, "misconception_code": "CYCLE_COUNTER_CONFUSION", "misconception_name": "Cycle Counter Fallacy", "explanation": "Cycle counters measure benchmark execution cycles, not instruction memory locations."},
            {"index": 1, "text": "Holding the output result of the most recent ALU computation", "is_correct": False, "misconception_code": "ACCUMULATOR_CONFUSION", "misconception_name": "Accumulator Confusion", "explanation": "ALU computation results are stored in the Accumulator or general-purpose registers."},
            {"index": 2, "text": "Holding the memory address of the NEXT instruction to be fetched and executed", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The PC points to the next memory address, automatically incrementing or taking branch jump target addresses."},
            {"index": 3, "text": "Storing the memory address of the top of the call stack", "is_correct": False, "misconception_code": "STACK_POINTER_CONFUSION", "misconception_name": "Stack Pointer Confusion", "explanation": "The top of the call stack is tracked by the Stack Pointer (SP) register."}
        ],
        "explanation": "The Program Counter (PC) stores the memory address of the next instruction to be fetched."
    },
    {
        "concept_code": "ENG_CPU_ARCH",
        "difficulty": "intermediate",
        "title": "von Neumann Bottleneck",
        "prompt": "In computer architecture, what defines the classic 'von Neumann bottleneck'?",
        "options": [
            {"index": 0, "text": "Throughput limitation caused by sharing a single physical memory bus between instruction fetch and data read/write", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Because instructions and data share the same bus, CPU performance is throttled by memory bus transfer speed."},
            {"index": 1, "text": "Inability of an 8-bit CPU to execute 32-bit arithmetic operations", "is_correct": False, "misconception_code": "WORD_SIZE_CONFUSION", "misconception_name": "Word Size Confusion", "explanation": "Multi-precision software arithmetic allows any CPU to compute large values regardless of architecture."},
            {"index": 2, "text": "Thermal throttling of silicon gates under clock overclocking", "is_correct": False, "misconception_code": "THERMAL_WALL_CONFUSION", "misconception_name": "Thermal Wall Confusion", "explanation": "The thermal wall is a semiconductor scaling constraint, not the von Neumann memory bottleneck."},
            {"index": 3, "text": "Incompatibility between little-endian and big-endian network bytes", "is_correct": False, "misconception_code": "ENDIANNESS_CONFUSION", "misconception_name": "Endianness Confusion", "explanation": "Endianness refers to byte order in memory, not the CPU-memory bus bottleneck."}
        ],
        "explanation": "The von Neumann bottleneck is the throughput restriction caused by sharing a single bus for both instruction and data memory."
    },
    {
        "concept_code": "ENG_CPU_ARCH",
        "difficulty": "advanced",
        "title": "Pipeline Hazard Classification",
        "prompt": "Which category of pipeline hazard occurs when an instruction requires the result of an earlier instruction that has not yet completed execution?",
        "options": [
            {"index": 0, "text": "Structural hazard", "is_correct": False, "misconception_code": "STRUCTURAL_HAZARD_CONFUSION", "misconception_name": "Structural Hazard Confusion", "explanation": "Structural hazards arise from hardware resource conflicts (e.g., single memory port)."},
            {"index": 1, "text": "Control / branch hazard", "is_correct": False, "misconception_code": "CONTROL_HAZARD_CONFUSION", "misconception_name": "Control Hazard Confusion", "explanation": "Control hazards arise from branch decisions determining the next PC value."},
            {"index": 2, "text": "Thermal hazard", "is_correct": False, "misconception_code": "THERMAL_CONFUSION", "misconception_name": "Non-Architectural Term", "explanation": "Thermal management is not a classical pipeline instruction hazard category."},
            {"index": 3, "text": "Data hazard (Read-After-Write / RAW)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "A data hazard occurs when instructions read or write registers out of original program dependency order."}
        ],
        "explanation": "Data hazards occur when instruction operands depend on earlier instructions still in the execution pipeline."
    },

    # --------------------------------------------------------------------------
    # PHYS_KINEMATICS (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "PHYS_KINEMATICS",
        "difficulty": "beginner",
        "title": "Position-Time Graph under Constant Acceleration",
        "prompt": "What geometric shape does the position-time graph x(t) trace for an object experiencing constant non-zero acceleration?",
        "options": [
            {"index": 0, "text": "A straight line with constant non-zero slope", "is_correct": False, "misconception_code": "CONSTANT_VELOCITY_CONFUSION", "misconception_name": "Constant Velocity Confusion", "explanation": "A linear graph indicates constant velocity (zero acceleration)."},
            {"index": 1, "text": "A parabola (quadratic curve: x = x0 + v0*t + 0.5*a*t^2)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Because position depends on t^2 under constant acceleration, the graph forms a parabola."},
            {"index": 2, "text": "A horizontal line parallel to the time axis", "is_correct": False, "misconception_code": "STATIONARY_CONFUSION", "misconception_name": "Stationary Object Fallacy", "explanation": "A horizontal position graph represents an object at rest."},
            {"index": 3, "text": "An exponential curve", "is_correct": False, "misconception_code": "EXPONENTIAL_CONFUSION", "misconception_name": "Exponential Confusion", "explanation": "Constant acceleration produces a quadratic polynomial in time, not an exponential."}
        ],
        "explanation": "Integrating constant acceleration a twice yields x(t) = x0 + v0*t + (1/2)*a*t^2, which is parabolic."
    },
    {
        "concept_code": "PHYS_KINEMATICS",
        "difficulty": "intermediate",
        "title": "Projectile Maximum Range Angle",
        "prompt": "Neglecting air resistance, at what angle above horizontal does a projectile achieve maximum horizontal range on flat terrain?",
        "options": [
            {"index": 0, "text": "30 degrees", "is_correct": False, "misconception_code": "LOW_TRAJECTORY_BIAS", "misconception_name": "Low Trajectory Bias", "explanation": "30 degrees yields lower flight time, producing range R = (v^2/g)*sin(60) = 0.866 * R_max."},
            {"index": 1, "text": "60 degrees", "is_correct": False, "misconception_code": "HIGH_HANGTIME_BIAS", "misconception_name": "Hangtime Bias", "explanation": "60 degrees produces identical range to 30 degrees, below the maximum."},
            {"index": 2, "text": "45 degrees", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Range is R = (v^2/g)*sin(2*theta). The sine function achieves its maximum 1 when 2*theta = 90 degrees, so theta = 45 degrees."},
            {"index": 3, "text": "90 degrees", "is_correct": False, "misconception_code": "VERTICAL_LAUNCH_CONFUSION", "misconception_name": "Vertical Launch Confusion", "explanation": "90 degrees is a straight vertical launch with zero horizontal range."}
        ],
        "explanation": "The range formula R = (v^2/g)*sin(2*theta) peaks when sin(2*theta) = 1, giving theta = 45 degrees."
    },
    {
        "concept_code": "PHYS_KINEMATICS",
        "difficulty": "intermediate",
        "title": "Velocity at Trajectory Apex",
        "prompt": "At the highest apex point of its parabolic flight, what is the vertical component of velocity (v_y) of a projectile?",
        "options": [
            {"index": 0, "text": "Exactly 0 m/s (instantaneously zero while vertical acceleration remains -g)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "At the apex, the projectile momentarily ceases upward motion before falling, so v_y = 0 while gravity continues acting."},
            {"index": 1, "text": "Equal to initial launch velocity v0", "is_correct": False, "misconception_code": "CONSTANT_SPEED_FALLACY", "misconception_name": "Constant Speed Fallacy", "explanation": "Initial speed v0 has degraded due to gravitational deceleration in the vertical axis."},
            {"index": 2, "text": "-9.8 m/s", "is_correct": False, "misconception_code": "ACCELERATION_AS_VELOCITY", "misconception_name": "Acceleration as Velocity Confusion", "explanation": "-9.8 m/s^2 is the gravitational acceleration, not the velocity."},
            {"index": 3, "text": "Equal to the horizontal component v_x", "is_correct": False, "misconception_code": "ISOTROPIC_VELOCITY_CONFUSION", "misconception_name": "Isotropic Velocity Confusion", "explanation": "The horizontal component remains v_x while vertical velocity v_y reaches zero."}
        ],
        "explanation": "At the trajectory peak, vertical velocity v_y is instantaneously 0, while acceleration remains g downward."
    },
    {
        "concept_code": "PHYS_KINEMATICS",
        "difficulty": "advanced",
        "title": "Stopping Distance vs Speed Scaling",
        "prompt": "A car traveling at speed v requires a minimum braking distance d under constant friction. If its speed doubles to 2v, what is the new braking distance?",
        "options": [
            {"index": 0, "text": "d (unchanged)", "is_correct": False, "misconception_code": "INERTIA_INDEPENDENT_FALLACY", "misconception_name": "Speed Independent Fallacy", "explanation": "Higher speeds carry significantly more kinetic energy to dissipate."},
            {"index": 1, "text": "2d (linear scaling)", "is_correct": False, "misconception_code": "LINEAR_ENERGY_FALLACY", "misconception_name": "Linear Velocity Scaling Fallacy", "explanation": "Stopping distance depends on kinetic energy, which scales quadratically with speed."},
            {"index": 2, "text": "3d", "is_correct": False, "misconception_code": "ODD_MULTIPLE_CONFUSION", "misconception_name": "Odd Multiple Confusion", "explanation": "Kinetic energy quadruples: (2v)^2 = 4v^2."},
            {"index": 3, "text": "4d (quadratic scaling with v^2)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By the work-energy theorem, W = F * d = (1/2)*m*v^2. Doubling speed multiplies kinetic energy by 2^2 = 4, requiring 4 times the stopping distance."}
        ],
        "explanation": "Because braking distance d = v^2 / (2*a) scales quadratically with speed, doubling velocity quadruples braking distance to 4d."
    },

    # --------------------------------------------------------------------------
    # PHYS_NEWTON_LAWS (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "PHYS_NEWTON_LAWS",
        "difficulty": "beginner",
        "title": "Newton's First Law (Inertia)",
        "prompt": "According to Newton's First Law of Motion, what occurs when the net external force acting on an object is zero?",
        "options": [
            {"index": 0, "text": "The object must immediately decelerate to rest", "is_correct": False, "misconception_code": "ARISTOTELIAN_REST_BIAS", "misconception_name": "Aristotelian Rest Bias", "explanation": "Objects do not require a force to maintain uniform motion in a vacuum."},
            {"index": 1, "text": "The object maintains its velocity (remains at rest or continues at constant speed in a straight line)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Inertia maintains constant velocity in the absence of net external force."},
            {"index": 2, "text": "The object accelerates in the direction of its mass vector", "is_correct": False, "misconception_code": "SPONTANEOUS_ACCELERATION_FALLACY", "misconception_name": "Spontaneous Acceleration Fallacy", "explanation": "Acceleration strictly requires non-zero net force (F = ma)."},
            {"index": 3, "text": "Its momentum decays exponentially over time", "is_correct": False, "misconception_code": "MOMENTUM_DECAY_FALLACY", "misconception_name": "Momentum Decay Fallacy", "explanation": "Momentum is strictly conserved when net external force is zero."}
        ],
        "explanation": "Newton's First Law states that a body remains at rest or in uniform motion unless acted upon by a net external force."
    },
    {
        "concept_code": "PHYS_NEWTON_LAWS",
        "difficulty": "intermediate",
        "title": "Newton's Third Law Reaction Force",
        "prompt": "A book rests on a table. What is the Newton's Third Law reaction partner to the gravitational force exerted by the Earth on the book?",
        "options": [
            {"index": 0, "text": "The upward normal force exerted by the table on the book", "is_correct": False, "misconception_code": "NORMAL_FORCE_REACTION_FALLACY", "misconception_name": "Normal Force Reaction Fallacy", "explanation": "The normal force balances gravity to produce equilibrium on the book, but action-reaction pairs act on different interacting bodies."},
            {"index": 1, "text": "The contact pressure exerted by the book down on the table", "is_correct": False, "misconception_code": "CONTACT_REACTION_CONFUSION", "misconception_name": "Contact Reaction Confusion", "explanation": "The book-table contact pair is separate from the gravitational interaction."},
            {"index": 2, "text": "The upward gravitational force exerted by the book on the Earth", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "If body A (Earth) exerts gravitational force on body B (book), body B exerts an equal and opposite gravitational force on body A."},
            {"index": 3, "text": "Static friction between book and air", "is_correct": False, "misconception_code": "FRICTION_REACTION_CONFUSION", "misconception_name": "Friction Confusion", "explanation": "Friction acts tangentially to surfaces and is unrelated to gravity."}
        ],
        "explanation": "Action-reaction pairs act on opposite interacting bodies; Earth's gravity on the book pairs with the book's upward gravitational pull on Earth."
    },
    {
        "concept_code": "PHYS_NEWTON_LAWS",
        "difficulty": "intermediate",
        "title": "F = ma Block Acceleration",
        "prompt": "A 5 kg block on a frictionless horizontal table is pulled by a constant horizontal force of 20 N. What is its acceleration?",
        "options": [
            {"index": 0, "text": "4 m/s^2 (a = F / m = 20 / 5)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Using Newton's second law a = F/m = 20 N / 5 kg = 4 m/s^2."},
            {"index": 1, "text": "100 m/s^2 (multiplying F * m)", "is_correct": False, "misconception_code": "INVERTED_NEWTON_FORMULA", "misconception_name": "Inverted Formula Fallacy", "explanation": "Multiplying force by mass (F*m) violates a = F/m."},
            {"index": 2, "text": "2.5 m/s^2", "is_correct": False, "misconception_code": "ARITHMETIC_ERROR", "misconception_name": "Calculation Error", "explanation": "20 / 5 = 4, not 2.5."},
            {"index": 3, "text": "0.25 m/s^2 (inverting m / F)", "is_correct": False, "misconception_code": "INVERTED_RATIO_FALLACY", "misconception_name": "Inverted Ratio Fallacy", "explanation": "m/F = 5/20 = 0.25 is inverse acceleration."}
        ],
        "explanation": "According to Newton's Second Law, a = F_net / m = 20 N / 5 kg = 4 m/s^2."
    },
    {
        "concept_code": "PHYS_NEWTON_LAWS",
        "difficulty": "advanced",
        "title": "Elevator Apparent Weight",
        "prompt": "An elevator accelerates upward with acceleration a. What is the apparent weight reading on a scale for a passenger of mass m?",
        "options": [
            {"index": 0, "text": "m * g", "is_correct": False, "misconception_code": "STATIC_WEIGHT_CONFUSION", "misconception_name": "Static Weight Confusion", "explanation": "mg is true only when the elevator is stationary or moving at constant speed."},
            {"index": 1, "text": "m * (g - a)", "is_correct": False, "misconception_code": "ACCELERATION_SIGN_ERROR", "misconception_name": "Acceleration Sign Inversion", "explanation": "m(g - a) is the apparent weight when accelerating downward."},
            {"index": 2, "text": "m * a", "is_correct": False, "misconception_code": "NET_FORCE_AS_WEIGHT", "misconception_name": "Net Force Confusion", "explanation": "ma is the net force, not the contact normal force read by the scale."},
            {"index": 3, "text": "m * (g + a)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "The scale normal force N must overcome gravity and provide upward acceleration: N - mg = ma => N = m(g + a)."}
        ],
        "explanation": "Newton's second law gives N - mg = ma, so the normal force (apparent weight) is N = m(g + a)."
    },

    # --------------------------------------------------------------------------
    # PHYS_ENERGY_WORK (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "PHYS_ENERGY_WORK",
        "difficulty": "beginner",
        "title": "Work Done by Centripetal Force",
        "prompt": "What is the net work performed by a centripetal force on a satellite in a uniform circular orbit?",
        "options": [
            {"index": 0, "text": "Equal to its orbital kinetic energy", "is_correct": False, "misconception_code": "KINETIC_WORK_CONFUSION", "misconception_name": "Kinetic Energy Equivalence Error", "explanation": "Centripetal force does not change the speed of the satellite."},
            {"index": 1, "text": "Exactly zero Joules (force is perpendicular to instantaneous displacement: cos(90) = 0)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Work W = F * d * cos(theta). Because centripetal force is always radial while motion is tangential, theta = 90 degrees and W = 0."},
            {"index": 2, "text": "2 * pi * r * F", "is_correct": False, "misconception_code": "CIRCUMFERENCE_FORCE_PRODUCT", "misconception_name": "Circumference Force Product", "explanation": "Displacement is perpendicular to the force at every instant."},
            {"index": 3, "text": "Negative work proportional to orbital radius", "is_correct": False, "misconception_code": "NEGATIVE_WORK_FALLACY", "misconception_name": "Negative Work Fallacy", "explanation": "Centripetal force does not oppose velocity, so work is not negative."}
        ],
        "explanation": "Because centripetal force is perpendicular to velocity at every point (cos 90 = 0), work done is zero."
    },
    {
        "concept_code": "PHYS_ENERGY_WORK",
        "difficulty": "intermediate",
        "title": "Work-Energy Theorem",
        "prompt": "According to the Work-Energy Theorem, the net work performed on an object by all external forces equals:",
        "options": [
            {"index": 0, "text": "The change in its potential energy (Delta U)", "is_correct": False, "misconception_code": "POTENTIAL_WORK_CONFUSION", "misconception_name": "Potential Energy Inversion", "explanation": "Work done by conservative forces equals -Delta U, but net work on the object equals Delta K."},
            {"index": 1, "text": "The instantaneous rate of change of momentum", "is_correct": False, "misconception_code": "FORCE_MOMENTUM_CONFUSION", "misconception_name": "Force Definition Confusion", "explanation": "Rate of change of momentum is force (F = dp/dt), not work."},
            {"index": 2, "text": "The change in its kinetic energy (Delta K = K_final - K_initial)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "W_net = integral(F dx) = (1/2)*m*v_f^2 - (1/2)*m*v_i^2 = Delta K."},
            {"index": 3, "text": "Total mechanical power output multiplied by distance", "is_correct": False, "misconception_code": "POWER_DISTANCE_FALLACY", "misconception_name": "Power Distance Fallacy", "explanation": "Work equals power integrated over time, not multiplied by distance."}
        ],
        "explanation": "The Work-Energy Theorem proves that net work done on a body equals its change in kinetic energy: W_net = Delta K."
    },
    {
        "concept_code": "PHYS_ENERGY_WORK",
        "difficulty": "intermediate",
        "title": "Spring Potential Energy Formula",
        "prompt": "What is the elastic potential energy stored in an ideal spring of stiffness constant k compressed by distance x?",
        "options": [
            {"index": 0, "text": "(1/2) * k * x^2", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Integrating Hooke's restoring force F = -kx gives U_s = (1/2)*k*x^2."},
            {"index": 1, "text": "k * x (Hooke's restoring force)", "is_correct": False, "misconception_code": "FORCE_AS_ENERGY_CONFUSION", "misconception_name": "Force as Energy Confusion", "explanation": "k*x is the instantaneous force magnitude, not the stored potential energy."},
            {"index": 2, "text": "(1/2) * k^2 * x", "is_correct": False, "misconception_code": "SQUARED_CONSTANT_CONFUSION", "misconception_name": "Squared Spring Constant Error", "explanation": "The displacement x is squared, not the spring constant k."},
            {"index": 3, "text": "m * g * x", "is_correct": False, "misconception_code": "GRAVITATIONAL_POTENTIAL_CONFUSION", "misconception_name": "Gravitational Confusion", "explanation": "mgx is gravitational potential energy, not elastic spring energy."}
        ],
        "explanation": "Elastic potential energy is U_s = (1/2)*k*x^2."
    },
    {
        "concept_code": "PHYS_ENERGY_WORK",
        "difficulty": "advanced",
        "title": "Conservation of Mechanical Energy Speed",
        "prompt": "A block of mass m slides from rest down a frictionless ramp of vertical height h. What is its speed at the base of the ramp?",
        "options": [
            {"index": 0, "text": "g * h", "is_correct": False, "misconception_code": "DIMENSIONAL_ANALYSIS_ERROR", "misconception_name": "Dimensional Error", "explanation": "g*h has units of m^2/s^2, which is velocity squared, not velocity."},
            {"index": 1, "text": "2 * g * h", "is_correct": False, "misconception_code": "MISSING_SQUAREROOT_FALLACY", "misconception_name": "Missing Square Root Fallacy", "explanation": "2gh is v^2; the square root must be taken."},
            {"index": 2, "text": "sqrt(g * h)", "is_correct": False, "misconception_code": "HALF_FACTOR_OMISSION", "misconception_name": "Half Factor Omission", "explanation": "Omits the factor of 2 from (1/2)*m*v^2."},
            {"index": 3, "text": "sqrt(2 * g * h)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "By conservation of mechanical energy: m*g*h = (1/2)*m*v^2 => v = sqrt(2*g*h)."}
        ],
        "explanation": "Equating initial gravitational potential energy to final kinetic energy gives mgh = (1/2)mv^2, solving to v = sqrt(2gh)."
    },

    # --------------------------------------------------------------------------
    # PHYS_MOMENTUM (Answers at 1, 2, 0, 3)
    # --------------------------------------------------------------------------
    {
        "concept_code": "PHYS_MOMENTUM",
        "difficulty": "beginner",
        "title": "Elastic Collision Conservation Laws",
        "prompt": "In an ideal elastic collision between two isolated bodies, which quantities are conserved?",
        "options": [
            {"index": 0, "text": "Only linear momentum is conserved", "is_correct": False, "misconception_code": "INELASTIC_CONFUSION", "misconception_name": "Inelastic Collision Confusion", "explanation": "Conserving only momentum is the definition of an inelastic collision."},
            {"index": 1, "text": "Both total linear momentum AND total kinetic energy are conserved", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "An elastic collision preserves both total momentum and kinetic energy without thermal dissipation."},
            {"index": 2, "text": "Only kinetic energy is conserved while momentum changes", "is_correct": False, "misconception_code": "MOMENTUM_NONCONSERVATION_FALLACY", "misconception_name": "Momentum Non-conservation Fallacy", "explanation": "Momentum is always conserved in isolated systems."},
            {"index": 3, "text": "Neither momentum nor kinetic energy is conserved", "is_correct": False, "misconception_code": "TOTAL_DISSIPATION_FALLACY", "misconception_name": "Total Dissipation Fallacy", "explanation": "Isolated systems strictly conserve linear momentum."}
        ],
        "explanation": "Elastic collisions preserve both total system momentum and total system kinetic energy."
    },
    {
        "concept_code": "PHYS_MOMENTUM",
        "difficulty": "intermediate",
        "title": "Impulse-Momentum Theorem",
        "prompt": "What physical quantity is defined as the time integral of net force J = integral(F dt) and equals change in momentum?",
        "options": [
            {"index": 0, "text": "Work", "is_correct": False, "misconception_code": "WORK_IMPULSE_CONFUSION", "misconception_name": "Work vs Impulse Confusion", "explanation": "Work is the integral of force over displacement (integral F dx), not time."},
            {"index": 1, "text": "Torque", "is_correct": False, "misconception_code": "TORQUE_CONFUSION", "misconception_name": "Torque Confusion", "explanation": "Torque is the rotational cross product tau = r x F."},
            {"index": 2, "text": "Impulse (J = Delta p)", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Impulse is defined as the time integral of force, which equals change in linear momentum."},
            {"index": 3, "text": "Power", "is_correct": False, "misconception_code": "POWER_CONFUSION", "misconception_name": "Power Confusion", "explanation": "Power is the rate of doing work (P = dW/dt)."}
        ],
        "explanation": "Impulse J = integral(F dt) = Delta p represents the change in an object's linear momentum."
    },
    {
        "concept_code": "PHYS_MOMENTUM",
        "difficulty": "intermediate",
        "title": "Completely Inelastic Collision Momentum",
        "prompt": "In an isolated system with no external forces, what happens to total momentum during a completely inelastic collision where bodies stick together?",
        "options": [
            {"index": 0, "text": "Total linear momentum is strictly conserved", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Because no external forces act, total momentum is conserved in all collisions, even completely inelastic ones."},
            {"index": 1, "text": "Total momentum drops to zero Joules", "is_correct": False, "misconception_code": "ZERO_MOMENTUM_FALLACY", "misconception_name": "Momentum Loss Fallacy", "explanation": "Kinetic energy is dissipated, but momentum cannot be lost without external force."},
            {"index": 2, "text": "Total momentum is reduced by half", "is_correct": False, "misconception_code": "HALF_MOMENTUM_FALLACY", "misconception_name": "Half Momentum Fallacy", "explanation": "Conservation laws permit zero net momentum loss in isolated systems."},
            {"index": 3, "text": "Total momentum transforms entirely into angular momentum", "is_correct": False, "misconception_code": "ANGULAR_MOMENTUM_CONVERSION", "misconception_name": "Angular Momentum Confusion", "explanation": "Linear momentum and angular momentum are independently conserved quantities."}
        ],
        "explanation": "Total linear momentum is always conserved in isolated systems regardless of whether kinetic energy is lost."
    },
    {
        "concept_code": "PHYS_MOMENTUM",
        "difficulty": "advanced",
        "title": "Completely Inelastic Post-Collision Velocity",
        "prompt": "A moving cart of mass m with velocity v collides with and latches onto an identical stationary cart of mass 2m. What is their final common velocity?",
        "options": [
            {"index": 0, "text": "v", "is_correct": False, "misconception_code": "UNCHANGED_VELOCITY_FALLACY", "misconception_name": "Unchanged Velocity Fallacy", "explanation": "The increased total mass must reduce final velocity to conserve momentum."},
            {"index": 1, "text": "v / 2", "is_correct": False, "misconception_code": "EQUAL_MASS_BIAS", "misconception_name": "Equal Mass Bias", "explanation": "v/2 would occur if the stationary cart had mass m. Here total mass is m + 2m = 3m."},
            {"index": 2, "text": "(2/3) * v", "is_correct": False, "misconception_code": "INVERTED_FRACTION_CONFUSION", "misconception_name": "Fractional Inversion Error", "explanation": "m / (m + 2m) is 1/3, not 2/3."},
            {"index": 3, "text": "v / 3", "is_correct": True, "misconception_code": "NONE", "misconception_name": "Correct Understanding", "explanation": "Conserving momentum: m*v = (m + 2m)*v_final => v_final = m*v / (3m) = v/3."}
        ],
        "explanation": "Conservation of momentum gives m*v = (m + 2m)*v' => v' = v/3."
    }
]

# ==============================================================================
# 3. LEARNING CONTENT LESSONS (1 lesson per concept)
# ==============================================================================
EXTENDED_LESSONS = [
    {
        "concept_code": "DSA_COMPLEXITY",
        "title": "Asymptotic Analysis, Big-O Notation, and the Master Theorem",
        "summary": "Master runtime complexities, best/worst/average case bounds, and divide-and-conquer recurrences with the Master Theorem.",
        "reading_time_min": 9,
        "introduction": "Asymptotic analysis mathematically characterizes the performance scaling of algorithms as input size approaches infinity.",
        "learning_objectives": [
            "Differentiate between Big-O (upper bound), Big-Omega (lower bound), and Big-Theta (tight bound).",
            "Identify common complexities: O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n).",
            "Apply the Master Theorem to divide-and-conquer recurrence relations T(n) = aT(n/b) + f(n)."
        ],
        "detailed_explanation": "### Asymptotic Bounds\n- **O(g(n))**: f(n) <= c*g(n) for large n (asymptotic upper bound).\n- **Omega(g(n))**: f(n) >= c*g(n) for large n (asymptotic lower bound).\n- **Theta(g(n))**: c1*g(n) <= f(n) <= c2*g(n) (asymptotically tight bound).\n\n### The Master Theorem\nFor recurrences of the form $T(n) = aT(n/b) + f(n)$:\n1. If $f(n) = O(n^{\\log_b a - \\epsilon})$, then $T(n) = \\Theta(n^{\\log_b a})$.\n2. If $f(n) = \\Theta(n^{\\log_b a})$, then $T(n) = \\Theta(n^{\\log_b a} \\log n)$.\n3. If $f(n) = \\Omega(n^{\\log_b a + \\epsilon})$ and regularity condition holds, $T(n) = \\Theta(f(n))$.",
        "code_examples": [
            {
                "title": "Binary Search vs Linear Search Complexity",
                "code": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n# Time Complexity: O(log n), Space: O(1)",
                "output": "Returns index in O(log n) comparisons",
                "notes": "Halving the search space each step produces logarithmic runtime."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming Average Case equals Worst Case in Hash Tables",
                "wrong_code": "hash_table_lookup = O(1) always",
                "correct_code": "Average: O(1), Worst Case (all keys collide): O(n)",
                "misconception_code": "HASH_WORST_CASE_FALLACY",
                "explanation": "Under extreme hash collisions, search degrades to linear linked-list traversal."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Solve T(n) = 2T(n/2) + O(n).",
                "hint": "Compare n^(log_2 2) with f(n) = n.",
                "solution": "log_2(2) = 1. Since f(n) = Theta(n^1), Master Theorem Case 2 yields Theta(n log n)."
            }
        ],
        "order_index": 1
    },
    {
        "concept_code": "DSA_TREES_HEAPS",
        "title": "Binary Search Trees, In-Order Traversals, and Binary Min-Heaps",
        "summary": "Understand BST invariants, sorting via in-order traversal, and heap priority structures with sift-down operations.",
        "reading_time_min": 8,
        "introduction": "Hierarchical tree structures organize data to achieve efficient search, insertion, and priority extraction.",
        "learning_objectives": [
            "Verify the BST invariant: Left < Node < Right.",
            "Understand why In-Order traversal sorts BST nodes in ascending order.",
            "Implement binary min/max heaps and extract_min in O(log n) time."
        ],
        "detailed_explanation": "### Binary Search Tree (BST)\nFor every node $X$:\n- All nodes in left subtree have keys $< X$.\n- All nodes in right subtree have keys $> X$.\nIn-Order traversal (Left -> Node -> Right) visits keys in strictly sorted order.\n\n### Binary Min-Heap\nA complete binary tree where every parent node has key $\\le$ its children.\n- Root contains the minimum element.\n- Stored compactly in arrays: Parent $(i-1)//2$, Left $2i+1$, Right $2i+2$.",
        "code_examples": [
            {
                "title": "In-Order BST Traversal",
                "code": "def in_order(node):\n    if not node:\n        return []\n    return in_order(node.left) + [node.val] + in_order(node.right)",
                "output": "[1, 2, 3, 4, 5, 6]",
                "notes": "Always produces ascending output on valid BSTs."
            }
        ],
        "common_mistakes": [
            {
                "title": "Checking BST property only on immediate children",
                "wrong_code": "if node.left and node.left.val >= node.val: return False",
                "correct_code": "Must enforce global bounds: low < node.val < high",
                "misconception_code": "LOCAL_BST_FALLACY",
                "explanation": "A node in the left subtree must be less than all ancestors, not just its direct parent."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "What is the time complexity of building a binary heap of n elements using bottom-up heapify?",
                "hint": "Sum of heights across all nodes.",
                "solution": "Bottom-up build_heap takes O(n) linear time, while repeated insertion takes O(n log n)."
            }
        ],
        "order_index": 2
    },
    {
        "concept_code": "DSA_GRAPHS",
        "title": "Graph Representations and Traversal: BFS and DFS",
        "summary": "Explore graphs using FIFO queues in BFS for shortest unweighted paths and LIFO recursion in DFS for cycle detection.",
        "reading_time_min": 9,
        "introduction": "Graphs represent pairwise relations between vertices connected by edges.",
        "learning_objectives": [
            "Compare Adjacency List (O(V+E)) vs Adjacency Matrix (O(V^2)) storage.",
            "Implement Breadth-First Search (BFS) for shortest path discovery in unweighted graphs.",
            "Implement Depth-First Search (DFS) and detect directed cycles using back edges."
        ],
        "detailed_explanation": "### BFS vs DFS\n- **BFS**: Uses a FIFO queue. Traverses outward in distance rings. Finds shortest path in unweighted graphs in $O(V + E)$ time.\n- **DFS**: Uses a recursion stack. Traverses deep down branches before backtracking. Useful for topological sorting and cycle detection.\n\n### Directed Cycle Detection\nA cycle exists in a directed graph if and only if DFS encounters a **back edge** pointing to a vertex currently in the active recursion call stack.",
        "code_examples": [
            {
                "title": "BFS Shortest Path Implementation",
                "code": "from collections import deque\ndef bfs_shortest_path(graph, start, goal):\n    queue = deque([(start, [start])])\n    visited = {start}\n    while queue:\n        curr, path = queue.popleft()\n        if curr == goal:\n            return path\n        for nxt in graph[curr]:\n            if nxt not in visited:\n                visited.add(nxt)\n                queue.append((nxt, path + [nxt]))\n    return None",
                "output": "['A', 'C', 'F']",
                "notes": "Guarantees minimum edge count on unweighted networks."
            }
        ],
        "common_mistakes": [
            {
                "title": "Using DFS for Unweighted Shortest Path",
                "wrong_code": "dfs_find_path(graph, start, end)",
                "correct_code": "bfs_shortest_path(graph, start, end)",
                "misconception_code": "DFS_SHORTEST_PATH_FALLACY",
                "explanation": "DFS explores deep arbitrary paths first and does not guarantee shortest path."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "What is the space complexity of BFS on a tree with branching factor b and depth d?",
                "hint": "How many leaf nodes exist at level d?",
                "solution": "The queue must store the entire bottom tier, requiring O(b^d) memory."
            }
        ],
        "order_index": 3
    },
    {
        "concept_code": "DSA_DP",
        "title": "Dynamic Programming: Optimal Substructure and Memoization",
        "summary": "Solve complex optimization problems by caching subproblems via Top-Down memoization and Bottom-Up tabulation.",
        "reading_time_min": 10,
        "introduction": "Dynamic Programming breaks problems down into overlapping subproblems, computing each subproblem solution once.",
        "learning_objectives": [
            "Identify optimal substructure and overlapping subproblems.",
            "Transform exponential recursive formulations into polynomial dynamic programming solutions.",
            "Implement bottom-up state tables and space-optimize memory."
        ],
        "detailed_explanation": "### Two Approaches\n1. **Top-Down with Memoization**: Keep the natural recursive tree and cache calculated results in a hash map or table.\n2. **Bottom-Up Tabulation**: Iteratively evaluate base cases first and build up to the target state without recursion.\n\n### Classic Problems\n- **Fibonacci**: $F(n) = F(n-1) + F(n-2)$, solved in $O(n)$ time and $O(1)$ space.\n- **0/1 Knapsack**: $dp[i][w] = \\max(dp[i-1][w], v_i + dp[i-1][w - w_i])$. Pseudo-polynomial $O(n W)$ runtime.",
        "code_examples": [
            {
                "title": "Optimized Bottom-Up Fibonacci",
                "code": "def fib(n):\n    if n <= 1:\n        return n\n    prev, curr = 0, 1\n    for _ in range(2, n + 1):\n        prev, curr = curr, prev + curr\n    return curr\n# O(n) time, O(1) space",
                "output": "fib(10) -> 55",
                "notes": "Tracks only the two preceding states."
            }
        ],
        "common_mistakes": [
            {
                "title": "Confusing Divide & Conquer with Dynamic Programming",
                "wrong_code": "Using DP when subproblems are completely disjoint",
                "correct_code": "Use DP only when subproblems repeat (overlap)",
                "misconception_code": "DIVIDE_CONQUER_CONFUSION",
                "explanation": "If subproblems do not overlap (like Merge Sort), caching provides zero benefit."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Explain why 0/1 Knapsack is pseudo-polynomial.",
                "hint": "Consider the number of bits in capacity W.",
                "solution": "Input size depends on log(W) bits. An algorithm running in O(n * 2^(log W)) is exponential in bit length."
            }
        ],
        "order_index": 4
    },

    # --------------------------------------------------------------------------
    # QC_SUPERPOSITION
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_SUPERPOSITION",
        "title": "Qubits, Quantum Superposition, and the Bloch Sphere",
        "summary": "Understand probability amplitudes, the Born normalization rule, state vectors, and geometric representation on the Bloch Sphere.",
        "reading_time_min": 8,
        "introduction": "Unlike a classical bit which is strictly 0 or 1, a qubit can exist in a linear superposition of both basis states.",
        "learning_objectives": [
            "Represent pure qubit states as state vectors in complex 2D Hilbert space.",
            "Apply the Born rule: P(0) = |alpha|^2 and P(1) = |beta|^2 with normalization |alpha|^2 + |beta|^2 = 1.",
            "Visualize state vectors on the unit Bloch Sphere using polar angles theta and phi."
        ],
        "detailed_explanation": "### Qubit State Formulation\n$$|\\psi\\rangle = \\alpha |0\\rangle + \\beta |1\\rangle$$\nwhere $\\alpha, \\beta \\in \\mathbb{C}$ and $|\\alpha|^2 + |\\beta|^2 = 1$.\n\n### The Bloch Sphere\nAny pure state can be written as:\n$$|\\psi\\rangle = \\cos(\\theta / 2)|0\\rangle + e^{i\\phi} \\sin(\\theta / 2)|1\\rangle$$\n- North Pole: $|0\\rangle$ ($\\theta = 0$)\n- South Pole: $|1\\rangle$ ($\\theta = \\pi$)\n- Equator: Equal superpositions $|+\\rangle, |-\\rangle, |+i\\rangle, |-i\\rangle$.",
        "code_examples": [
            {
                "title": "Qiskit Single Qubit State Definition",
                "code": "import numpy as np\n# Define equal superposition |+>\nalpha = 1 / np.sqrt(2)\nbeta = 1 / np.sqrt(2)\nprob_0 = np.abs(alpha)**2\nprob_1 = np.abs(beta)**2\nprint(f'P(0): {prob_0:.2f}, P(1): {prob_1:.2f}, Total: {prob_0 + prob_1:.2f}')",
                "output": "P(0): 0.50, P(1): 0.50, Total: 1.00",
                "notes": "Satisfies unitary normalization."
            }
        ],
        "common_mistakes": [
            {
                "title": "Treating Amplitudes as Classical Probabilities",
                "wrong_code": "alpha + beta = 1",
                "correct_code": "|alpha|^2 + |beta|^2 = 1",
                "misconception_code": "L1_NORM_FALLACY",
                "explanation": "Quantum probabilities are squared magnitudes of complex amplitudes."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "If a qubit is in state |psi> = 0.6|0> + 0.8i|1>, find P(0) and P(1).",
                "hint": "Calculate |0.6|^2 and |0.8i|^2.",
                "solution": "P(0) = 0.6^2 = 0.36 (36%), P(1) = |0.8i|^2 = 0.8^2 = 0.64 (64%). Total = 1.00."
            }
        ],
        "order_index": 1
    },

    # --------------------------------------------------------------------------
    # QC_GATES
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_GATES",
        "title": "Quantum Logic Gates: Pauli, Hadamard, and CNOT",
        "summary": "Master unitary quantum gates, phase rotations, Hadamard superposition generation, and 2-qubit CNOT interactions.",
        "reading_time_min": 9,
        "introduction": "Quantum gates are unitary operators that manipulate qubits reversibly without collapsing quantum state vectors.",
        "learning_objectives": [
            "Compute outputs for Pauli-X (NOT), Pauli-Y, and Pauli-Z (phase flip) gates.",
            "Generate superpositions with the Hadamard gate: H|0> = |+> and H|1> = |->.",
            "Construct multi-qubit entangling circuits using the Controlled-NOT (CNOT) gate."
        ],
        "detailed_explanation": "### Standard Unitary Gates\n- **Pauli-X (NOT)**: $\\begin{pmatrix} 0 & 1 \\\\ 1 & 0 \\end{pmatrix}$, $X|0\\rangle = |1\\rangle$, $X|1\\rangle = |0\\rangle$.\n- **Pauli-Z**: $\\begin{pmatrix} 1 & 0 \\\\ 0 & -1 \\end{pmatrix}$, $Z|0\\rangle = |0\\rangle$, $Z|1\\rangle = -|1\\rangle$.\n- **Hadamard (H)**: $\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 & 1 \\\\ 1 & -1 \\end{pmatrix}$, creates equal superpositions.\n- **CNOT**: Flips target qubit if control qubit is $|1\\rangle$.",
        "code_examples": [
            {
                "title": "Hadamard Matrix Transformation",
                "code": "import numpy as np\nH = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])\nstate_0 = np.array([1, 0])\nplus_state = np.dot(H, state_0)\nprint('H|0> =', plus_state)",
                "output": "H|0> = [0.70710678 0.70710678]",
                "notes": "Generates the |+> balanced state vector."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming Non-Unitary Operators are Valid Gates",
                "wrong_code": "Applying projection operators as logic gates",
                "correct_code": "All quantum gates must be unitary: U^dagger * U = I",
                "misconception_code": "SINGULAR_MATRIX_FALLACY",
                "explanation": "Non-unitary operations violate probability conservation and are irreversible."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "What is H * H applied to any qubit state?",
                "hint": "Check H^2 matrix multiplication.",
                "solution": "H is Hermitian and unitary, so H^2 = I. Applying Hadamard twice restores the initial state."
            }
        ],
        "order_index": 2
    },

    # --------------------------------------------------------------------------
    # QC_ENTANGLEMENT
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_ENTANGLEMENT",
        "title": "Quantum Entanglement, Bell States, and the No-Cloning Theorem",
        "summary": "Discover maximally entangled Bell states, quantum correlation non-locality, and the fundamental No-Cloning theorem.",
        "reading_time_min": 9,
        "introduction": "Entanglement is a non-classical correlation where individual subsystem states cannot be described independently.",
        "learning_objectives": [
            "Construct the four canonical Bell states using H and CNOT gates.",
            "Analyze instantaneous measurement correlations in EPR pairs.",
            "Understand why the No-Cloning theorem forbids copying arbitrary quantum states."
        ],
        "detailed_explanation": "### The Four Bell States\n$$|\\Phi^{\\pm}\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle \\pm |11\\rangle)$$\n$$|\\Psi^{\\pm}\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle \\pm |10\\rangle)$$\n\n### The No-Cloning Theorem\nSuppose a unitary operator $U$ clones arbitrary states: $U|\\psi\\rangle|0\\rangle = |\\psi\\rangle|\\psi\\rangle$ and $U|\\phi\\rangle|0\\rangle = |\\phi\\rangle|\\phi\\rangle$.\nTaking the inner product yields $\\langle \\psi | \\phi \\rangle = (\\langle \\psi | \\phi \\rangle)^2$, which holds only if states are identical or orthogonal. Hence universal cloning is mathematically impossible.",
        "code_examples": [
            {
                "title": "Bell State Circuit Representation",
                "code": "# Bell state generation logic:\n# Step 1: H on qubit 0 -> (|00> + |10>) / sqrt(2)\n# Step 2: CNOT(0, 1) -> (|00> + |11>) / sqrt(2)\nprint('Bell State |Phi+> created successfully.')",
                "output": "Bell State |Phi+> created successfully.",
                "notes": "Standard building block of quantum teleportation and cryptography."
            }
        ],
        "common_mistakes": [
            {
                "title": "Believing Entanglement Enables Faster-Than-Light Messaging",
                "wrong_code": "Transmitting classical bits instantly via Bell pairs",
                "correct_code": "No-Communication Theorem: classical channel required",
                "misconception_code": "DISTANCE_LIMIT_FALLACY",
                "explanation": "Measurement results are individually random; correlations can only be decoded with classical messages."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Show that |Phi+> cannot be factored into (|a> * |b>).",
                "hint": "Attempt to solve (a0|0> + a1|1>)(b0|0> + b1|1>) = (|00> + |11>)/sqrt(2).",
                "solution": "Requires a0*b1 = 0 and a1*b0 = 0 while a0*b0 != 0 and a1*b1 != 0, an algebraic contradiction."
            }
        ],
        "order_index": 3
    },

    # --------------------------------------------------------------------------
    # QC_MEASUREMENT
    # --------------------------------------------------------------------------
    {
        "concept_code": "QC_MEASUREMENT",
        "title": "Quantum Measurement and Wavefunction Collapse",
        "summary": "Analyze projective observables, eigenstate collapse dynamics, and measurement in rotated bases.",
        "reading_time_min": 8,
        "introduction": "Measurement acts as a bridge between quantum superposition and the definite macroscopic world.",
        "learning_objectives": [
            "Compute measurement probabilities using projection operators M_m = |m><m|.",
            "Understand post-measurement state collapse: |psi'> = M_m|psi> / sqrt(P(m)).",
            "Perform measurements in alternative bases (e.g. Hadamard X-basis)."
        ],
        "detailed_explanation": "### Projective Measurement Postulate\nAn observable $M$ has spectral decomposition $M = \\sum_m m P_m$ where $P_m$ is the projector onto the eigenspace of eigenvalue $m$.\n- **Probability of outcome $m$**: $P(m) = \\langle \\psi | P_m | \\psi \\rangle$.\n- **Post-measurement state**: $|\\psi'\\rangle = \\frac{P_m |\\psi\\rangle}{\\sqrt{P(m)}}$.",
        "code_examples": [
            {
                "title": "Simulated Measurement Sampling",
                "code": "import numpy as np\nprob_0, prob_1 = 0.85, 0.15\noutcomes = np.random.choice([0, 1], size=1000, p=[prob_0, prob_1])\nprint(f'Measured 0: {np.mean(outcomes == 0):.2f}, Measured 1: {np.mean(outcomes == 1):.2f}')",
                "output": "Measured 0: 0.85, Measured 1: 0.15",
                "notes": "Matches theoretical probabilities over repeated trials."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming Quantum State Survives Measurement Intact",
                "wrong_code": "Re-measuring expecting original superposition amplitudes",
                "correct_code": "Post-measurement state is an eigenstate; subsequent measurements repeat outcome",
                "misconception_code": "NON_DESTRUCTIVE_MEASUREMENT_FALLACY",
                "explanation": "Measurement collapses the superposition irreversibly."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "If a qubit in state |0> is measured in the X-basis {|+>, |->}, what is the post-measurement state if outcome + is observed?",
                "hint": "Project |0> onto |+>.",
                "solution": "The post-measurement state is exactly |+> = (|0> + |1>)/sqrt(2)."
            }
        ],
        "order_index": 4
    },

    # --------------------------------------------------------------------------
    # ENG_BOOLEAN_LOGIC
    # --------------------------------------------------------------------------
    {
        "concept_code": "ENG_BOOLEAN_LOGIC",
        "title": "Boolean Algebra, Truth Tables, and Universal Logic Gates",
        "summary": "Master fundamental logic gates, truth table analysis, De Morgan's theorems, and universal NAND/NOR synthesis.",
        "reading_time_min": 8,
        "introduction": "Digital computers represent information using binary logic levels governed by Boolean algebraic laws.",
        "learning_objectives": [
            "Construct truth tables for AND, OR, NOT, NAND, NOR, and XOR gates.",
            "Apply De Morgan's theorems to invert and simplify Boolean expressions.",
            "Synthesize basic logic functions using exclusively universal NAND or NOR gates."
        ],
        "detailed_explanation": "### De Morgan's Theorems\n1. $\\overline{A \\cdot B} = \\overline{A} + \\overline{B}$ (NAND equals negative-OR)\n2. $\\overline{A + B} = \\overline{A} \\cdot \\overline{B}$ (NOR equals negative-AND)\n\n### Universal Gates\nAny logic function can be constructed using only NAND gates:\n- NOT: $A \\text{ NAND } A = \\overline{A}$\n- AND: $(A \\text{ NAND } B) \\text{ NAND } (A \\text{ NAND } B) = A \\cdot B$\n- OR: $(\\overline{A}) \\text{ NAND } (\\overline{B}) = A + B$",
        "code_examples": [
            {
                "title": "Python Boolean Logic Simulation",
                "code": "def nand_gate(a, b): return not (a and b)\ndef not_gate(a): return nand_gate(a, a)\ndef and_gate(a, b): return not_gate(nand_gate(a, b))\nprint('NAND universal NOT(1):', not_gate(1))\nprint('NAND universal AND(1, 0):', and_gate(1, 0))",
                "output": "NAND universal NOT(1): False\nNAND universal AND(1, 0): False",
                "notes": "Demonstrates NAND functional completeness."
            }
        ],
        "common_mistakes": [
            {
                "title": "Incorrect De Morgan Operator Switching",
                "wrong_code": "not (A and B) == not A and not B",
                "correct_code": "not (A and B) == not A or not B",
                "misconception_code": "INCOMPLETE_DEMORGAN_FALLACY",
                "explanation": "Negating a product requires changing the conjunction to a disjunction (OR)."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "Simplify F = A + ~A*B.",
                "hint": "Distribute A + (~A * B).",
                "solution": "(A + ~A)(A + B) = 1 * (A + B) = A + B."
            }
        ],
        "order_index": 1
    },

    # --------------------------------------------------------------------------
    # PHYS_KINEMATICS
    # --------------------------------------------------------------------------
    {
        "concept_code": "PHYS_KINEMATICS",
        "title": "1D and 2D Kinematics, Motion Graphs, and Projectile Trajectories",
        "summary": "Master displacement, constant acceleration equations, velocity vectors, and projectile motion trajectories.",
        "reading_time_min": 8,
        "introduction": "Kinematics describes the motion of points, bodies, and systems without consideration of the forces that cause them.",
        "learning_objectives": [
            "Use the kinematic equations under constant acceleration.",
            "Decompose 2D projectile motion into independent horizontal and vertical components.",
            "Calculate flight time, maximum apex height, and horizontal range."
        ],
        "detailed_explanation": "### Kinematic Equations for Constant Acceleration\n1. $v = v_0 + a t$\n2. $x = x_0 + v_0 t + \\frac{1}{2} a t^2$\n3. $v^2 = v_0^2 + 2 a (x - x_0)$\n\n### Projectile Motion\n- Horizontal: $a_x = 0 \\implies x(t) = (v_0 \\cos\\theta) t$\n- Vertical: $a_y = -g \\implies y(t) = (v_0 \\sin\\theta) t - \\frac{1}{2} g t^2$\n- Apex occurs when $v_y = 0$, maximum range on flat terrain occurs at $\\theta = 45^\\circ$.",
        "code_examples": [
            {
                "title": "Projectile Maximum Range Calculation",
                "code": "import numpy as np\ndef projectile_range(v0, theta_deg, g=9.8):\n    theta_rad = np.radians(theta_deg)\n    return (v0**2 / g) * np.sin(2 * theta_rad)\nprint(f'Range at 45 deg: {projectile_range(20, 45):.1f}m')\nprint(f'Range at 30 deg: {projectile_range(20, 30):.1f}m')",
                "output": "Range at 45 deg: 40.8m\nRange at 30 deg: 35.3m",
                "notes": "Range is maximized at 45 degrees."
            }
        ],
        "common_mistakes": [
            {
                "title": "Assuming Stopping Distance Scales Linearly with Velocity",
                "wrong_code": "stopping_dist = k * v",
                "correct_code": "stopping_dist = v^2 / (2 * a)",
                "misconception_code": "LINEAR_ENERGY_FALLACY",
                "explanation": "Braking distance is proportional to velocity squared due to kinetic energy."
            }
        ],
        "practice_exercises": [
            {
                "prompt": "How high does a ball thrown vertically upwards at 19.6 m/s travel before stopping?",
                "hint": "Use v^2 = v0^2 - 2gh with v = 0.",
                "solution": "0 = 19.6^2 - 2(9.8)h => h = 384.16 / 19.6 = 19.6 meters."
            }
        ],
        "order_index": 1
    }
]


def seed_extended_curriculum(force: bool = False):
    """
    Idempotently seeds concepts, questions, and lessons for DSA, Quantum Computing,
    Digital Electronics, and Classical Mechanics into the active database.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        # Check courses in database
        courses = cur.execute("SELECT id, code, subject_id FROM courses").fetchall()
        course_map = {c["code"]: c["id"] for c in courses}
        subject_map = {c["code"]: c["subject_id"] for c in courses}

        print(f"Active courses in DB: {list(course_map.keys())}")

        # 1. Seed Concepts
        concept_id_map = {}
        for course_code, concept_list in EXTENDED_CONCEPTS.items():
            if course_code not in course_map:
                print(f"Skipping {course_code} - not in courses table")
                continue
            c_id = course_map[course_code]
            s_id = subject_map[course_code]

            for cp in concept_list:
                cur.execute("""
                    INSERT OR REPLACE INTO concepts (subject_id, course_id, code, name, description, order_index, p_init, p_transit, p_guess, p_slip, prerequisites)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (s_id, c_id, cp["code"], cp["name"], cp["description"], cp["order_index"], cp["p_init"], cp["p_transit"], cp["p_guess"], cp["p_slip"], cp["prerequisites"]))
                cur.execute("SELECT id FROM concepts WHERE code = ?", (cp["code"],))
                concept_id_map[cp["code"]] = cur.fetchone()["id"]

        print(f"Seeded {len(concept_id_map)} extended concepts.")

        # 2. Seed Questions (Checking for duplicates by title)
        seeded_q_count = 0
        for q in EXTENDED_QUESTIONS:
            c_code = q["concept_code"]
            if c_code not in concept_id_map:
                cur.execute("SELECT id FROM concepts WHERE code = ?", (c_code,))
                row = cur.fetchone()
                if row:
                    concept_id_map[c_code] = row["id"]
                else:
                    continue

            cid = concept_id_map[c_code]

            # Check if question with this title already exists
            cur.execute("SELECT id FROM questions WHERE title = ? AND concept_id = ?", (q["title"], cid))
            existing = cur.fetchone()
            if existing and not force:
                continue

            opts_json = json.dumps(q["options"])
            if existing and force:
                cur.execute("""
                    UPDATE questions SET difficulty = ?, prompt = ?, code_snippet = ?, options_json = ?, explanation = ?
                    WHERE id = ?
                """, (q["difficulty"], q["prompt"], q.get("code_snippet"), opts_json, q["explanation"], existing["id"]))
            else:
                cur.execute("""
                    INSERT INTO questions (concept_id, difficulty, title, prompt, code_snippet, options_json, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (cid, q["difficulty"], q["title"], q["prompt"], q.get("code_snippet"), opts_json, q["explanation"]))
                seeded_q_count += 1

        print(f"Seeded {seeded_q_count} new assessment questions.")

        # 3. Seed Lessons in learning_content
        seeded_lesson_count = 0
        for l in EXTENDED_LESSONS:
            c_code = l["concept_code"]
            if c_code not in concept_id_map:
                continue
            cid = concept_id_map[c_code]

            cur.execute("SELECT id FROM learning_content WHERE concept_id = ?", (cid,))
            existing = cur.fetchone()
            if existing and not force:
                continue

            if existing and force:
                cur.execute("""
                    UPDATE learning_content SET title = ?, summary = ?, reading_time_min = ?, introduction = ?,
                    learning_objectives_json = ?, detailed_explanation = ?, code_examples_json = ?,
                    common_mistakes_json = ?, practice_exercises_json = ?, order_index = ?
                    WHERE id = ?
                """, (
                    l["title"], l["summary"], l["reading_time_min"], l["introduction"],
                    json.dumps(l["learning_objectives"]), l["detailed_explanation"],
                    json.dumps(l["code_examples"]), json.dumps(l["common_mistakes"]),
                    json.dumps(l["practice_exercises"]), l["order_index"], existing["id"]
                ))
            else:
                cur.execute("""
                    INSERT INTO learning_content (
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
                seeded_lesson_count += 1

        print(f"Seeded {seeded_lesson_count} new learning content lessons.")
        conn.commit()


if __name__ == "__main__":
    seed_extended_curriculum(force=True)
    print("Extended subject curriculum seeding completed.")
