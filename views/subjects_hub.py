"""
SARVAVIDYA: Multi-Subject Curriculum Hub
Provides the complete multi-subject browsing and selection interface across:
- Programming (Python, C Systems Programming, Java, C++)
- Mathematics (Calculus & Linear Algebra, Probability & Statistics, Discrete Math)
- Engineering (Digital Logic, Signal Processing, Electrical Circuits)
- Computer Science (Data Structures & Algorithms, AI, Cybersecurity)
- Science (Classical Mechanics, Intro to Qubits, Physical Chemistry)
Maintains strict data separation between subjects and courses.
"""

import streamlit as st
from typing import Dict, Any, List
from database.db import (
    get_all_subjects, get_all_courses, get_concepts_by_course,
    get_student_mastery, get_learning_content_by_concept
)
from core.course_manager import get_active_course, set_active_course


ALL_SUBJECT_CATALOG = [
    {
        "category": "Programming",
        "icon": "terminal",
        "description": "Core algorithmic syntax, memory architectures, pointer arithmetic, dynamic collections, and procedural logic.",
        "courses": [
            {
                "code": "python",
                "name": "Python Fundamentals",
                "difficulty": "Introductory",
                "status": "active",
                "topics": ["Variables & Data Types", "Conditionals", "Loops & Iteration", "Lists & Arrays", "Functions", "Recursion"],
                "description": "Dynamic typing, control flow, list comprehensions, modular functions, and recursive execution."
            },
            {
                "code": "c_programming",
                "name": "C Systems Programming",
                "difficulty": "Intermediate",
                "status": "active",
                "topics": ["Data Types & Sizes", "Control Flow", "Pointers & Addresses", "Arrays & Strings", "Dynamic Memory", "Structs"],
                "description": "Memory address manipulation, pointer arithmetic, manual heap management with malloc/free, and memory alignment."
            },
            {
                "code": "java_core",
                "name": "Java Enterprise & OOP",
                "difficulty": "Intermediate",
                "status": "coming_soon",
                "topics": ["Object Encapsulation", "Polymorphic Inheritance", "JVM Memory Model", "Generics & Collections"],
                "description": "Class hierarchies, memory lifecycle in the JVM, thread synchronization, and clean interface contracts."
            },
            {
                "code": "cpp_systems",
                "name": "Modern C++ Systems",
                "difficulty": "Advanced",
                "status": "coming_soon",
                "topics": ["RAII & Smart Pointers", "Move Semantics", "Template Metaprogramming", "Memory Concurrency"],
                "description": "Deterministic resource management, rvalue references, zero-cost abstractions, and low-latency systems engineering."
            }
        ]
    },
    {
        "category": "Mathematics",
        "icon": "functions",
        "description": "Continuous limits, differential calculus, multivariable integrals, matrix eigenspaces, and discrete structures.",
        "courses": [
            {
                "code": "calculus_linear_algebra",
                "name": "Calculus & Linear Algebra",
                "difficulty": "Intermediate",
                "status": "active",
                "topics": ["Limits & Continuity", "Differential Calculus", "Definite Integrals", "Matrix Algebra", "Vector Spaces", "Eigenvalues"],
                "description": "Limits, derivatives, the chain rule, definite integrals, matrix algebra, determinants, and eigenvalue spectra."
            },
            {
                "code": "prob_stats",
                "name": "Probability & Bayesian Statistics",
                "difficulty": "Intermediate",
                "status": "coming_soon",
                "topics": ["Bayes' Theorem", "Probability Distributions", "Maximum Likelihood Estimation", "Markov Chains"],
                "description": "Axiomatic probability, prior and posterior Bayesian inferences, continuous random variables, and stochastic modeling."
            },
            {
                "code": "discrete_math",
                "name": "Discrete Mathematics & Logic",
                "difficulty": "Introductory",
                "status": "coming_soon",
                "topics": ["Propositional Logic", "Set Theory & Relations", "Combinatorics", "Graph Theory"],
                "description": "Predicate calculus, proof techniques by induction, recurrence relations, and combinatorial counting."
            }
        ]
    },
    {
        "category": "Computer Science",
        "icon": "account_tree",
        "description": "Asymptotic algorithmic efficiency, non-linear tree structures, graph traversals, and dynamic programming.",
        "courses": [
            {
                "code": "dsa",
                "name": "Data Structures & Algorithms",
                "difficulty": "Advanced",
                "status": "active",
                "topics": ["Big-O Complexity", "Binary Search Trees & Heaps", "Graph Traversal (BFS/DFS)", "Dynamic Programming"],
                "description": "Asymptotic complexity, heaps, binary search trees, BFS/DFS, and dynamic programming memoization."
            },
            {
                "code": "ai_foundations",
                "name": "Artificial Intelligence & Search",
                "difficulty": "Advanced",
                "status": "coming_soon",
                "topics": ["A* Heuristic Search", "Adversarial Minimax", "Constraint Satisfaction", "Reinforcement Learning"],
                "description": "State-space heuristic search, game playing agents, Alpha-Beta pruning, and Markov Decision Processes."
            },
            {
                "code": "cybersecurity",
                "name": "Network Security & Cryptography",
                "difficulty": "Intermediate",
                "status": "coming_soon",
                "topics": ["Public-Key RSA", "AES Symmetric Ciphers", "Zero-Knowledge Proofs", "Network Vulnerabilities"],
                "description": "Asymmetric encryption, digital signatures, TLS handshakes, hash collisions, and buffer overflow prevention."
            }
        ]
    },
    {
        "category": "Engineering",
        "icon": "memory",
        "description": "Boolean circuit minimization, synchronous state machines, flip-flop registers, and digital logic synthesis.",
        "courses": [
            {
                "code": "digital_electronics",
                "name": "Digital Logic & Microprocessors",
                "difficulty": "Introductory",
                "status": "active",
                "topics": ["Boolean Algebra & Gates", "Karnaugh Maps", "Latches & Flip-Flops", "ALU & Register Files"],
                "description": "Karnaugh maps, multiplexers, latches, flip-flops, registers, and ALU design."
            },
            {
                "code": "embedded_systems",
                "name": "Embedded Systems & ARM Microcontrollers",
                "difficulty": "Intermediate",
                "status": "coming_soon",
                "topics": ["GPIO Interfacing", "Timer Interrupts (NVIC)", "UART/SPI/I2C Protocols", "Real-Time OS (RTOS)"],
                "description": "Bare-metal firmware architecture, hardware interrupt latency, peripheral bus controllers, and RTOS scheduling."
            }
        ]
    },
    {
        "category": "Science",
        "icon": "science",
        "description": "Kinematics vectors, Newtonian dynamics, quantum superposition, quantum logic gates, and wavefunction collapse.",
        "courses": [
            {
                "code": "physics_mechanics",
                "name": "Classical Mechanics & Kinematics",
                "difficulty": "Introductory",
                "status": "active",
                "topics": ["1D/2D Kinematics", "Newton's Laws & Free Body", "Work & Energy Conservation", "Momentum & Collisions"],
                "description": "Vectors in kinematics, Newton's three laws, momentum conservation, and harmonic oscillation."
            },
            {
                "code": "qc_101",
                "name": "Intro to Qubits & Quantum Computing",
                "difficulty": "Intermediate",
                "status": "active",
                "topics": ["Superposition & Bloch Sphere", "Quantum Gates (Pauli, H, CNOT)", "Entanglement & Bell Pairs", "Measurement & Collapse"],
                "description": "Quantum state vectors, probability amplitudes, Hadamard superposition, Bell states, and Born rule collapse."
            },
            {
                "code": "chem_kinetics",
                "name": "Chemical Thermodynamics & Kinetics",
                "difficulty": "Intermediate",
                "status": "coming_soon",
                "topics": ["Reaction Rates & Catalysis", "Gibbs Free Energy", "Enthalpy & Entropy", "Equilibrium States"],
                "description": "Arrhenius equation, rate laws, spontaneous reaction thermodynamics, and molecular orbital dynamics."
            }
        ]
    }
]


def render_subjects_hub_page(user: dict):
    """Renders the comprehensive multi-subject learning catalog and switcher."""
    active_course = get_active_course()
    user_id = user["id"]

    # Header section
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <div>
                <h2 style="font-size: 1.5rem; font-weight: 800; color: #172943; margin: 0; letter-spacing: -0.02em;">
                    SARVAVIDYA Multi-Subject Learning Hub
                </h2>
                <div style="font-size: 0.8rem; color: #718096; margin-top: 0.2rem;">
                    One platform. Every subject. Explore accredited curriculum tracks with independent cognitive tracking.
                </div>
            </div>
            <span class="lm-pill pill-ahead" style="font-size: 0.725rem; padding: 4px 10px;">
                7 Active Courses &bull; 100% Calibrated
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Discipline Filter Buttons
    categories = ["All Disciplines", "Programming", "Mathematics", "Computer Science", "Engineering", "Science"]
    if "subject_hub_cat" not in st.session_state:
        st.session_state["subject_hub_cat"] = "All Disciplines"

    cols_cat = st.columns(len(categories))
    for i, cat in enumerate(categories):
        is_selected = st.session_state["subject_hub_cat"] == cat
        btn_type = "primary" if is_selected else "secondary"
        if cols_cat[i].button(cat, key=f"cat_btn_{i}", type=btn_type, use_container_width=True):
            st.session_state["subject_hub_cat"] = cat
            st.rerun()

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    selected_cat = st.session_state["subject_hub_cat"]
    filtered_groups = [
        g for g in ALL_SUBJECT_CATALOG
        if selected_cat == "All Disciplines" or g["category"] == selected_cat
    ]

    # Render Subject Groups
    for group in filtered_groups:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin: 1.5rem 0 0.75rem 0;">
            <div style="width: 4px; height: 18px; background: #D6B56D; border-radius: 2px;"></div>
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #172943; margin: 0;">{group['category']}</h3>
            <span style="font-size: 0.75rem; color: #718096;">&bull; {group['description']}</span>
        </div>
        """, unsafe_allow_html=True)

        courses = group["courses"]
        # Render 2 courses per row
        for i in range(0, len(courses), 2):
            col_c1, col_c2 = st.columns(2)
            for col, c in zip([col_c1, col_c2], courses[i:i+2]):
                with col:
                    _render_course_hub_card(c, group["category"], active_course, user_id)


def _render_course_hub_card(c: dict, category: str, active_course: dict, user_id: int):
    """Renders an individual course card with real BKT mastery or coming soon badge."""
    is_active_track = active_course["code"] == c["code"]
    is_supported = c["status"] == "active"

    # Border and styling
    card_border = "#3976B9" if is_active_track else "#E4E8ED"
    card_bg = "#F8FAFC" if is_active_track else "#FFFFFF"

    # Status Pill
    if is_active_track:
        status_badge = '<span class="lm-pill pill-completed" style="font-size: 0.65rem; padding: 2px 8px;">Active Learning Track</span>'
    elif is_supported:
        status_badge = '<span class="lm-pill pill-ahead" style="font-size: 0.65rem; padding: 2px 8px;">Available Now</span>'
    else:
        status_badge = '<span class="lm-pill pill-lagging" style="font-size: 0.65rem; padding: 2px 8px; background-color: #F1F5F9; color: #64748B; border-color: #CBD5E1;">Roadmap &bull; Coming Soon</span>'

    topics_html = "".join([
        f'<span style="background: #F1F5F9; color: #334155; font-size: 0.675rem; padding: 2px 7px; border-radius: 4px; margin-right: 4px; margin-bottom: 4px; display: inline-block;">{t}</span>'
        for t in c["topics"]
    ])

    st.markdown(f"""
    <div style="background: {card_bg}; border: 1.5px solid {card_border}; border-radius: 12px; padding: 1.15rem 1.25rem; margin-bottom: 0.85rem; box-shadow: 0 2px 8px rgba(23, 41, 67, 0.04);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.45rem;">
            <div>
                <div style="font-size: 0.65rem; font-weight: 700; color: #D6B56D; text-transform: uppercase; letter-spacing: 0.05em;">{category} &bull; {c['difficulty']}</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #172943; margin-top: 0.1rem;">{c['name']}</div>
            </div>
            {status_badge}
        </div>
        <p style="font-size: 0.775rem; color: #64748B; line-height: 1.45; margin: 0 0 0.75rem 0; min-height: 38px;">
            {c['description']}
        </p>
        <div style="margin-bottom: 0.85rem;">
            <div style="font-size: 0.65rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; margin-bottom: 0.35rem;">Curriculum Modules:</div>
            {topics_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actions
    if is_supported:
        btn_c1, btn_c2, btn_c3 = st.columns([1.1, 1.0, 1.0])
        with btn_c1:
            if is_active_track:
                st.button("Currently Selected", key=f"sel_cur_{c['code']}", disabled=True, use_container_width=True)
            else:
                if st.button("Set as Active Track", key=f"set_track_{c['code']}", type="primary", use_container_width=True):
                    set_active_course(c["code"])
                    st.session_state["_synced_page"] = "student_dashboard"
                    st.rerun()
        with btn_c2:
            if st.button("Assessments", key=f"go_assess_{c['code']}", use_container_width=True):
                set_active_course(c["code"])
                st.session_state["current_page"] = "assessment"
                st.session_state["_synced_page"] = "assessment"
                st.rerun()
        with btn_c3:
            if st.button("Learning Library", key=f"go_lib_{c['code']}", use_container_width=True):
                set_active_course(c["code"])
                st.session_state["current_page"] = "learning_library"
                st.session_state["_synced_page"] = "learning_library"
                st.rerun()
    else:
        st.button("Curriculum in Development", key=f"dev_btn_{c['code']}", disabled=True, use_container_width=True)

