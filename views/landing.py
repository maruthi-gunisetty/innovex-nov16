"""
SARVAVIDYA: Public Educational Management Landing Page
Brand: SARVAVIDYA
Tagline: One Platform. Every Subject. Infinite Knowledge.
Colors: Deep Navy #172943, Royal Navy #243B64, Premium Gold #D6B56D, Soft Gold #E8C879, White #FFFFFF.
Zero emojis, strict professional typography, and responsive SaaS layout.
"""

import streamlit as st
from components.brand import render_full_hero_brand, BRAND_NAME, TAGLINE


def render_landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 1rem 1rem 1rem; max-width: 900px; margin: 0 auto;">
        <div style="display: inline-flex; align-items: center; gap: 6px; background-color: #FAF5EA; color: #172943; border: 1px solid #E8C879; padding: 0.25rem 0.85rem; border-radius: 9999px; font-size: 0.725rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">
            Unified Multi-Subject Cognitive Architecture
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Full SARVAVIDYA Brand Hero Lockup (Golden Lotus + Open Book + SARVAVIDYA + Tagline)
    render_full_hero_brand(center=True)

    st.markdown("""
    <div style="text-align: center; max-width: 820px; margin: 0 auto 1.5rem auto;">
        <p style="font-size: 1.05rem; color: #718096; line-height: 1.6; margin: 0;">
            An internationally competitive learning platform unifying <strong>Programming</strong>, <strong>Mathematics</strong>, <strong>Engineering</strong>, and <strong>Science</strong>. Diagnosing student misconceptions with Corbett & Anderson Bayesian Knowledge Tracing and delivering adaptive learning pathways.
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
    <div class="lm-card" style="margin-top: 1.5rem; border-left: 4px solid #D6B56D;">
        <div class="lm-card-header">
            <div>
                <span class="lm-pill pill-ahead">Evaluation Credentials</span>
                <h3 class="lm-card-title" style="margin-top: 0.25rem;">Sarva Vidya Evaluation Credentials &bull; Quick Access</h3>
                <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Sign in using the top-right portal or use these verified accounts:</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.85rem; margin-top: 0.5rem;">
            <div style="background-color: #F5F6F8; border: 1px solid #E8C879; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #172943;">Student Account</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">Email / User: <code>student@123</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">Active telemetry across Python, C Systems, and Calculus.</div>
            </div>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #172943;">Faculty / Instructor Account</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">User: <code>dr_bennett</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>learnsphere123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">Multi-subject cohort telemetry and systemic misconception analytics.</div>
            </div>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.9rem;">
                <div style="font-weight: 700; font-size: 0.875rem; color: #172943;">Advanced Scholar Profile</div>
                <div style="font-size: 0.8rem; color: #263445; margin: 0.2rem 0;">User: <code>sophia_chen</code></div>
                <div style="font-size: 0.8rem; color: #263445; margin-bottom: 0.4rem;">Password: <code>student123</code></div>
                <div style="font-size: 0.725rem; color: #718096;">High-mastery profile excelling in Algorithms and Linear Algebra.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core AI System & Features Grid
    st.markdown("""
    <div style="margin-top: 1.5rem; margin-bottom: 0.75rem;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #172943; margin-bottom: 0.25rem;">
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
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 6px; padding: 0.65rem; font-size: 0.775rem; color: #172943;">
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
                Identifies deep cognitive fallacies across Programming, Mathematics, Engineering, and Science directly from student response selections.
            </p>
            <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 6px; padding: 0.65rem; font-size: 0.775rem; color: #172943;">
                Examples: Pointer dereferencing, recursion base omission, power-rule exponent fallacies.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 1rem 0; margin-top: 2rem; border-top: 1px solid #E4E8ED; color: #718096; font-size: 0.775rem;">
        <strong>{BRAND_NAME}</strong> &copy; 2026 &bull; {TAGLINE} &bull; Enterprise Educational Management. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
