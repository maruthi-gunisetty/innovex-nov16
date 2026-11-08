"""
LearnSphere AI: Public Educational Management Landing Page
Enterprise educational design language matching the reference dashboard:
Primary Navy #243B64, Secondary Blue #3976B9, Light Blue #EAF2FA,
Cards #FFFFFF, Borders #E4E8ED, Canvas #F5F6F8.
Zero emojis, strict professional typography, and responsive layouts.
"""

import streamlit as st


def render_landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2.25rem 1rem 1.75rem 1rem; max-width: 860px; margin: 0 auto;">
        <div style="display: inline-flex; align-items: center; gap: 6px; background-color: #EAF2FA; color: #243B64; border: 1px solid #D2E4F6; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-bottom: 1rem;">
            Enterprise Educational Management &bull; Adaptive Intelligence
        </div>
        <h1 style="font-size: 2.45rem; font-weight: 800; color: #243B64; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 1rem;">
            Learning That Understands Every Student.
        </h1>
        <p style="font-size: 1.05rem; color: #718096; line-height: 1.55; margin-bottom: 1.75rem;">
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
        if st.button("Faculty Analytics Portal", use_container_width=True):
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
    <div class="lm-card" style="margin-top: 1.5rem; border-left: 4px solid #3976B9;">
        <div class="lm-card-header">
            <div>
                <span class="lm-pill pill-ahead">Evaluation Credentials</span>
                <h3 class="lm-card-title" style="margin-top: 0.25rem;">Evaluation Credentials &bull; Quick Access</h3>
                <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Sign in using the top-right Login Portal or use these credentials:</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.85rem; margin-top: 0.5rem;">
            <div style="background-color: #F5F6F8; border: 1px solid #D2E4F6; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #243B64;">Student Account (Requested)</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">Email / User: <code>student@123</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">Active telemetry with struggle points in Loops and Recursion.</div>
            </div>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #243B64;">Faculty / Teacher Account</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">User: <code>dr_bennett</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>learnsphere123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">Cohort-wide mastery distributions and systemic misconception telemetry.</div>
            </div>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #243B64;">Advanced Student Profile</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">User: <code>sophia_chen</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">High proficiency student profile exceeding mastery thresholds.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core AI System & Features Grid
    st.markdown("""
    <div style="margin-top: 1.5rem; margin-bottom: 0.75rem;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #243B64; margin-bottom: 0.25rem;">
            Educational Management & Adaptive Intelligence
        </h3>
        <p style="color: #718096; font-size: 0.825rem; margin: 0;">
            A rigorous cognitive modeling platform combining Corbett & Anderson Bayesian Knowledge Tracing with labeled-distractor diagnostics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_feat1, c_feat2 = st.columns(2)
    with c_feat1:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Bayesian Knowledge Tracing (BKT)</span>
                <span class="lm-pill pill-completed">Probabilistic AI</span>
            </div>
            <p style="color: #718096; font-size: 0.825rem; line-height: 1.55; margin-bottom: 0.75rem;">
                Estimates latent student mastery using empirical parameters: prior mastery, learning transit probability, slip probability, and guess probability.
            </p>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 6px; padding: 0.65rem; font-size: 0.775rem; color: #263445;">
                P(L<sub>t</sub>) = P(L<sub>t-1</sub> | Obs) + (1 - P(L<sub>t-1</sub> | Obs)) &times; P(T)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_feat2:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Cognitive Misconception Detection</span>
                <span class="lm-pill pill-ahead">Distractor Diagnostics</span>
            </div>
            <p style="color: #718096; font-size: 0.825rem; line-height: 1.55; margin-bottom: 0.75rem;">
                Identifies 10 computer science misconceptions directly from chosen answer choices, distinguishing careless slips from deep mental model bugs.
            </p>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 6px; padding: 0.65rem; font-size: 0.775rem; color: #263445;">
                Examples: Off-by-one indexing, missing recursion base cases, reference alias mutation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; margin-top: 2rem; border-top: 1px solid #E4E8ED; color: #718096; font-size: 0.775rem;">
        LearnSphere AI &copy; 2026. Adaptive Intelligence for Personalized Learning. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
