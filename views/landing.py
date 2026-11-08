"""
LearnSphere AI: Public SaaS Landing Page
Modern minimalist interface inspired by Linear, Stripe, and Notion.
Color system: Deep Navy #172554, AI Violet #635BDB, Canvas #F8FAFC, Cards #FFFFFF.
Zero emojis, strict professional typography, and responsive layouts.
"""

import streamlit as st
from components.styles import get_icon


def render_landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2.75rem 1rem 2rem 1rem; max-width: 880px; margin: 0 auto;">
        <h1 style="font-size: 2.85rem; font-weight: 800; color: #172554; line-height: 1.15; letter-spacing: -0.035em; margin-bottom: 1.25rem;">
            Learning That Understands Every Student.
        </h1>
        <p style="font-size: 1.15rem; color: #64748B; line-height: 1.6; margin-bottom: 2rem;">
            An intelligent learning platform that identifies knowledge gaps, understands learning difficulties and creates personalized educational journeys.
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

    # Demonstration Fake Login Credentials Card
    st.markdown("""
    <div class="ls-card" style="margin-top: 2rem; border-left: 4px solid #635BDB; background-color: #FFFFFF;">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-violet">Evaluation Credentials</span>
                <h3 class="ls-card-title" style="margin-top: 0.35rem;">Evaluation Credentials &bull; Quick Access</h3>
                <div class="ls-card-desc">Use the Login Portal in the right side top corner or sign in using these pre-seeded accounts:</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-top: 0.5rem;">
            <div style="background-color: #F8FAFC; border: 1px solid #BFDBFE; border-radius: 8px; padding: 1.1rem;">
                <div style="font-weight: 600; font-size: 0.95rem; color: #172554;">Student Account (Requested)</div>
                <div style="font-size: 0.85rem; color: #0F172A; margin: 0.25rem 0;">Email / User: <code>student@123</code></div>
                <div style="font-size: 0.85rem; color: #0F172A; margin-bottom: 0.5rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.775rem; color: #64748B;">Active cognitive misconceptions in Loops and Recursion.</div>
            </div>
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.1rem;">
                <div style="font-weight: 600; font-size: 0.95rem; color: #172554;">Advanced Student (Sophia Chen)</div>
                <div style="font-size: 0.85rem; color: #0F172A; margin: 0.25rem 0;">Username: <code>sophia_chen</code></div>
                <div style="font-size: 0.85rem; color: #0F172A; margin-bottom: 0.5rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.775rem; color: #64748B;">High curriculum mastery, advancing into algorithmic synthesis.</div>
            </div>
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.1rem;">
                <div style="font-weight: 600; font-size: 0.95rem; color: #172554;">Faculty Portal (Dr. Sarah Bennett)</div>
                <div style="font-size: 0.85rem; color: #0F172A; margin: 0.25rem 0;">Username: <code>dr_bennett</code></div>
                <div style="font-size: 0.85rem; color: #0F172A; margin-bottom: 0.5rem;">Password: <code>learnsphere123</code></div>
                <div style="font-size: 0.775rem; color: #64748B;">Cohort-wide mastery analytics and student deep-dive inspection.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # Problem Statement and Proposed Solution
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Problem Statement and Proposed Solution</h3>
            <span class="ls-card-desc">Addressing the structural bottleneck of conventional assessment</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div style="padding: 1.25rem; background-color: #F8FAFC; border-radius: 8px; border: 1px solid #E2E8F0;">
                <h4 style="color: #DC2626; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem;">The Challenge in Conventional Learning</h4>
                <p style="color: #475569; font-size: 0.875rem; line-height: 1.6; margin: 0;">
                    Traditional e-learning platforms treat assessment as static binary scoring. A score of 70% does not reveal which foundational concepts are missing, whether mistakes stem from simple slips or deep cognitive misconceptions, or what sequential topic the learner is cognitively ready to acquire next.
                </p>
            </div>
            <div style="padding: 1.25rem; background-color: #F8FAFC; border-radius: 8px; border: 1px solid #E2E8F0;">
                <h4 style="color: #172554; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem;">The LearnSphere AI Approach</h4>
                <p style="color: #475569; font-size: 0.875rem; line-height: 1.6; margin: 0;">
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
            <div style="padding: 1.1rem; border: 1px solid #E2E8F0; border-radius: 8px; background-color: #F8FAFC;">
                <div style="font-weight: 600; color: #172554; margin-bottom: 0.35rem;">1. Knowledge State Modeling</div>
                <p style="color: #64748B; font-size: 0.825rem; line-height: 1.55; margin: 0;">
                    Estimates latent concept mastery using Bayesian Knowledge Tracing with parameters: Initial Mastery P(L0), Learning Transition P(T), Guess Probability P(G), and Slip Probability P(S).
                </p>
            </div>
            <div style="padding: 1.1rem; border: 1px solid #E2E8F0; border-radius: 8px; background-color: #F8FAFC;">
                <div style="font-weight: 600; color: #172554; margin-bottom: 0.35rem;">2. Cognitive Misconception Detection</div>
                <p style="color: #64748B; font-size: 0.825rem; line-height: 1.55; margin: 0;">
                    Every incorrect answer option is mapped to a verified cognitive bug (e.g., Off-by-One indexing, mutable reference aliasing, or unreturned recursion) rather than marked as an undifferentiated failure.
                </p>
            </div>
            <div style="padding: 1.1rem; border: 1px solid #E2E8F0; border-radius: 8px; background-color: #F8FAFC;">
                <div style="font-weight: 600; color: #172554; margin-bottom: 0.35rem;">3. Adaptive Question Selection</div>
                <p style="color: #64748B; font-size: 0.825rem; line-height: 1.55; margin: 0;">
                    Maintains the student in their Zone of Proximal Development by matching real-time BKT mastery levels to appropriate question difficulties (Beginner, Intermediate, Advanced).
                </p>
            </div>
            <div style="padding: 1.1rem; border: 1px solid #E2E8F0; border-radius: 8px; background-color: #F8FAFC;">
                <div style="font-weight: 600; color: #172554; margin-bottom: 0.35rem;">4. Prerequisite-Aware Pathways</div>
                <p style="color: #64748B; font-size: 0.825rem; line-height: 1.55; margin: 0;">
                    Evaluates concept dependency directed acyclic graphs (DAGs) to identify root prerequisite gaps when advanced topics encounter resistance.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mathematical Rigor Box
    st.markdown("""
    <div class="ls-card" style="border-left: 4px solid #635BDB;">
        <h4 style="font-size: 1rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
            Mathematical Foundation: Bayesian Knowledge Tracing Formulation
        </h4>
        <p style="color: #475569; font-size: 0.875rem; line-height: 1.6; margin-bottom: 0.75rem;">
            Following the Corbett and Anderson framework, when an observation is received, posterior mastery is updated using Bayes' rule:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.caption("Posterior Update (Given Correct Response):")
        st.latex(r"P(L_t \mid \text{obs}=1) = \frac{P(L_t)(1 - P(S))}{P(L_t)(1 - P(S)) + (1 - P(L_t))P(G)}")
    with col_m2:
        st.caption("Next State Transition (Prior for Next Opportunity):")
        st.latex(r"P(L_{t+1}) = P(L_t \mid \text{obs}) + [1 - P(L_t \mid \text{obs})] \times P(T)")

    # Platform Capabilities & Technology
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-top: 1.5rem; margin-bottom: 2rem;">
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
        LearnSphere AI &copy; 2026. Adaptive Intelligence for Personalized Learning. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
