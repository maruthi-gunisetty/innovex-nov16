"""
LearnSphere AI: Public Landing Page
Professional SaaS introduction presenting the problem statement,
Bayesian Knowledge Tracing architecture, and platform capabilities.
"""

import streamlit as st
from components.styles import get_icon


def render_landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2.5rem 1rem 2rem 1rem; max-width: 860px; margin: 0 auto;">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; padding: 0.35rem 0.85rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; margin-bottom: 1.25rem;">
            Problem Statement 03: Intelligent Education
        </div>
        <h1 style="font-size: 2.75rem; font-weight: 800; color: #0f172a; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 1.25rem;">
            Learning That Understands Every Student.
        </h1>
        <p style="font-size: 1.15rem; color: #475569; line-height: 1.6; margin-bottom: 2rem;">
            An intelligent learning platform that identifies knowledge gaps, understands learning difficulties, detects misconceptions, and creates personalized educational journeys.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Action CTA buttons
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
    with col_cta1:
        if st.button("Explore Student Experience", use_container_width=True, type="primary"):
            st.session_state["target_view"] = "auth"
            st.session_state["auth_tab"] = "student"
            st.rerun()
    with col_cta2:
        if st.button("Teacher Analytics Portal", use_container_width=True):
            st.session_state["target_view"] = "auth"
            st.session_state["auth_tab"] = "teacher"
            st.rerun()
    with col_cta3:
        if st.button("Instant Demonstration Mode", use_container_width=True):
            st.session_state["target_view"] = "auth"
            st.session_state["auth_tab"] = "demo"
            st.rerun()

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # Problem Statement and Proposed Solution
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Problem Statement and Proposed Solution</h3>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div style="padding: 1rem; background-color: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                <h4 style="color: #991b1b; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem;">The Challenge in Conventional Learning</h4>
                <p style="color: #475569; font-size: 0.875rem; line-height: 1.55; margin: 0;">
                    Traditional e-learning platforms treat assessment as static binary scoring. A score of 70% does not reveal which foundational concepts are missing, whether mistakes stem from simple slips or deep cognitive misconceptions, or what sequential topic the learner is cognitively ready to acquire next.
                </p>
            </div>
            <div style="padding: 1rem; background-color: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                <h4 style="color: #1e40af; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem;">The LearnSphere AI Approach</h4>
                <p style="color: #475569; font-size: 0.875rem; line-height: 1.55; margin: 0;">
                    LearnSphere AI implements genuine Bayesian Knowledge Tracing to infer latent student mastery after every interaction. By combining probabilistic mastery modeling with labeled distractor misconception diagnostics, the platform delivers targeted pedagogical interventions tailored to each learner.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How the AI Learning System Works
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">How the AI Learning Engine Operates</h3>
            <span class="ls-card-desc">Interpretable Probabilistic Machine Learning</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
            <div style="padding: 1rem; border: 1px solid #f1f5f9; border-radius: 6px;">
                <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.35rem;">1. Knowledge State Modeling</div>
                <p style="color: #64748b; font-size: 0.825rem; line-height: 1.5; margin: 0;">
                    Estimates latent concept mastery using Bayesian Knowledge Tracing with parameters: Initial Mastery P(L0), Learning Transition P(T), Guess Probability P(G), and Slip Probability P(S).
                </p>
            </div>
            <div style="padding: 1rem; border: 1px solid #f1f5f9; border-radius: 6px;">
                <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.35rem;">2. Cognitive Misconception Detection</div>
                <p style="color: #64748b; font-size: 0.825rem; line-height: 1.5; margin: 0;">
                    Every incorrect answer option is mapped to a verified cognitive bug (e.g., Off-by-One indexing, mutable reference aliasing, or unreturned recursion) rather than marked as an undifferentiated failure.
                </p>
            </div>
            <div style="padding: 1rem; border: 1px solid #f1f5f9; border-radius: 6px;">
                <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.35rem;">3. Adaptive Question Selection</div>
                <p style="color: #64748b; font-size: 0.825rem; line-height: 1.5; margin: 0;">
                    Maintains the student in their Zone of Proximal Development by matching real-time BKT mastery levels to appropriate question difficulties (Beginner, Intermediate, Advanced).
                </p>
            </div>
            <div style="padding: 1rem; border: 1px solid #f1f5f9; border-radius: 6px;">
                <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.35rem;">4. Prerequisite-Aware Pathways</div>
                <p style="color: #64748b; font-size: 0.825rem; line-height: 1.5; margin: 0;">
                    Evaluates concept dependency directed acyclic graphs (DAGs) to identify root prerequisite gaps when advanced topics encounter resistance.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mathematical Rigor Box
    st.markdown("""
    <div class="ls-card" style="background-color: #fbfcfe; border-left: 4px solid #4f46e5;">
        <h4 style="font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
            Mathematical Foundation: Bayesian Knowledge Tracing Formulation
        </h4>
        <p style="color: #475569; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.75rem;">
            Following the Corbett and Anderson framework, when an observation is received, posterior mastery is updated using Bayes' rule:
        </p>
        <div style="background-color: #ffffff; padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid #e2e8f0; font-family: monospace; font-size: 0.825rem; color: #1e293b; margin-bottom: 0.5rem;">
            P(L_t | Correct) = [P(L_t) * (1 - P(S))] / [P(L_t) * (1 - P(S)) + (1 - P(L_t)) * P(G)]<br>
            P(L_t | Incorrect) = [P(L_t) * P(S)] / [P(L_t) * P(S) + (1 - P(L_t)) * (1 - P(G))]<br>
            P(L_t+1) = P(L_t | obs) + [1 - P(L_t | obs)] * P(T)
        </div>
        <div style="color: #64748b; font-size: 0.8rem;">
            This formulation maintains interpretable probabilities, eliminates random guessing noise, and distinguishes probabilistic competence from measured raw test percentage.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Platform Capabilities & Technology
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 2rem;">
        <div class="ls-card" style="margin-bottom: 0;">
            <div class="ls-card-header">
                <h4 class="ls-card-title">Benefits for Students</h4>
            </div>
            <ul style="color: #475569; font-size: 0.875rem; line-height: 1.7; padding-left: 1.25rem; margin: 0;">
                <li>Immediate targeted feedback explaining why a chosen answer represents a misconception.</li>
                <li>Dynamic learning roadmap adapting to mastery progress rather than fixed linear chapters.</li>
                <li>Clear distinction between foundational understanding and exam execution slips.</li>
                <li>Interactive curriculum covering Python fundamentals, data structures, and recursion.</li>
            </ul>
        </div>
        <div class="ls-card" style="margin-bottom: 0;">
            <div class="ls-card-header">
                <h4 class="ls-card-title">Benefits for Teachers and Institutions</h4>
            </div>
            <ul style="color: #475569; font-size: 0.875rem; line-height: 1.7; padding-left: 1.25rem; margin: 0;">
                <li>Aggregated class mastery heatmaps identifying cohort-wide conceptual bottlenecks.</li>
                <li>Frequency diagnostics pinpointing systemic misunderstandings before exams.</li>
                <li>Individual student inspection for personalized office hour interventions.</li>
                <li>Evidence-based learning analytics powered by transparent machine learning.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Privacy and Responsible AI
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Responsible AI and Data Governance</h3>
        </div>
        <p style="color: #475569; font-size: 0.875rem; line-height: 1.6; margin: 0;">
            LearnSphere AI adheres to responsible educational AI principles: all models are interpretable (no opaque black boxes deciding student grades), passwords are salted and hashed using PBKDF2 with 100,000 iterations, student records are strictly partitioned, and no proprietary student data is transmitted to external commercial APIs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="ls-footer">
        LearnSphere AI &copy; 2026. Built for PS 03 Intelligent Education. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
