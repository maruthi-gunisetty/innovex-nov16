"""
SARVAVIDYA: Advanced AI Intelligence and Learning Analytics
Directly demonstrates how SARVAVIDYA understands and tracks student learning:
1. Bayesian Knowledge Tracing Visualization (P(L0), P(Lt), P(T), P(G), P(S) & Live Updating Math)
2. Concept Mastery Categorization (Mastered, Proficient, Developing, Struggling, Revision Needed)
3. Calibrated Cognitive Misconception Detection & Pedagogical Remediation
4. Zone of Proximal Development (ZPD) Adaptive Difficulty Engine
5. "How SARVAVIDYA Understands Your Learning" Architecture Walkthrough for Students & Judges
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress
)
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine
from core.recommender import RecommenderEngine
from core.course_manager import get_active_course, render_course_selector


def render_misconception_page(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    course_id = active_course["id"]

    mastery_data = get_student_mastery(user_id, course_id=course_id)
    attempts = get_user_attempts(user_id, limit=50, course_id=course_id)
    lesson_progress = get_user_lesson_progress(user_id)
    summary = MisconceptionEngine.summarize_patterns(attempts)
    patterns = summary["patterns"]

    col_h_title, col_h_track = st.columns([2.0, 1.0])
    with col_h_title:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
            <div>
                <h2 style="font-size: 1.5rem; font-weight: 800; color: #172943; margin: 0; letter-spacing: -0.02em;">
                    SARVAVIDYA Cognitive Intelligence &bull; {active_course['name']}
                </h2>
                <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">
                    Corbett & Anderson (1995) Bayesian Knowledge Tracing, Adaptive Question Calibration & Cognitive Diagnostics.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h_track:
        render_course_selector(key="ai_track_selector", label="Select Track", on_change_rerun=True)

    # ==========================================================
    # 1. BKT CORE HYPERPARAMETERS ROW (P(L0), P(T), P(G), P(S))
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.675rem; color: #718096; font-weight: 700; text-transform: uppercase;">Prior Probability P(L₀)</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #243B64; margin-top: 0.15rem;">0.20</div>
            <div style="font-size: 0.7rem; color: #718096;">Baseline initial concept mastery</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.675rem; color: #718096; font-weight: 700; text-transform: uppercase;">Transition Probability P(T)</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #36A879; margin-top: 0.15rem;">0.15</div>
            <div style="font-size: 0.7rem; color: #718096;">Learning gain chance per attempt</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.675rem; color: #718096; font-weight: 700; text-transform: uppercase;">Guess Probability P(G)</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #E9AA45; margin-top: 0.15rem;">0.20</div>
            <div style="font-size: 0.7rem; color: #718096;">Lucky correct answer probability</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.675rem; color: #718096; font-weight: 700; text-transform: uppercase;">Slip Probability P(S)</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #D96B6B; margin-top: 0.15rem;">0.10</div>
            <div style="font-size: 0.7rem; color: #718096;">Accidental error probability</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 2. MAIN 2-COLUMN INTELLIGENCE PANELS
    # ==========================================================
    col_left, col_right = st.columns([1.1, 1.2])

    with col_left:
        # Panel 1: Concept Mastery Comparison Chart
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Concept Mastery Telemetry (BKT Latent P(L))</span>
                <span class="lm-pill pill-ahead">Benchmark: 60%</span>
            </div>
        """, unsafe_allow_html=True)

        if mastery_data:
            codes = [m["concept_code"] for m in mastery_data]
            pcts = [m["mastery_prob"] * 100 for m in mastery_data]
            colors = [
                "#36A879" if p >= 85 else "#3976B9" if p >= 60 else "#E9AA45" if p >= 40 else "#D96B6B"
                for p in pcts
            ]
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=codes,
                    y=pcts,
                    marker_color=colors,
                    text=[f"{p:.0f}%" for p in pcts],
                    textposition="auto"
                )
            ])
            fig_bar.add_hline(y=60, line_dash="dash", line_color="#718096", annotation_text="Proficiency Benchmark (60%)", annotation_position="top right")
            fig_bar.update_layout(
                height=190,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                yaxis=dict(range=[0, 100], gridcolor="#F5F6F8", title="Mastery (%)"),
                xaxis=dict(gridcolor="#F5F6F8", title="Concept")
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Panel 2: Learning Gaps Categorization
        gaps = RecommenderEngine.analyze_learning_gaps(mastery_data, attempts)
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Concept Mastery Categorization</span>
                <span style="font-size: 0.7rem; color: #718096;">Cognitive Breakdown</span>
            </div>
        """, unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.65rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 0.75rem; color: #1E40AF;">Mastered (≥ 85%)</span>
                    <span class="lm-pill pill-completed" style="font-size: 0.625rem;">{len(gaps['advanced_ready'])} Modules</span>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.2rem;">
                    {", ".join([m['concept_code'] for m in gaps['advanced_ready']]) if gaps['advanced_ready'] else 'None yet'}
                </div>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 0.75rem; color: #166534;">Proficient (60% - 84%)</span>
                    <span class="lm-pill pill-ahead" style="font-size: 0.625rem;">{len(gaps['strong'])} Modules</span>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.2rem;">
                    {", ".join([m['concept_code'] for m in gaps['strong']]) if gaps['strong'] else 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_g2:
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.65rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 0.75rem; color: #B45309;">Developing (40% - 59%)</span>
                    <span class="lm-pill pill-ontrack" style="font-size: 0.625rem;">{len(gaps['partial'])} Modules</span>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.2rem;">
                    {", ".join([m['concept_code'] for m in gaps['partial']]) if gaps['partial'] else 'None'}
                </div>
            </div>
            <div style="background: #FAF5F5; border: 1px solid #FECACA; border-radius: 8px; padding: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 0.75rem; color: #991B1B;">Struggling (< 40%)</span>
                    <span class="lm-pill pill-lagging" style="font-size: 0.625rem;">{len(gaps['weak'])} Modules</span>
                </div>
                <div style="font-size: 0.7rem; color: #DC2626; margin-top: 0.2rem;">
                    {", ".join([m['concept_code'] for m in gaps['weak']]) if gaps['weak'] else 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Panel 3: Cognitive Misconception Frequency Distribution
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Identified Cognitive Misconceptions</span>
                <span style="font-size: 0.7rem; color: #718096;">Distractor Patterns Flagged</span>
            </div>
        """, unsafe_allow_html=True)

        if patterns:
            counts = [p["count"] for p in patterns]
            names = [p["name"] for p in patterns]
            fig_mf = go.Figure(data=[
                go.Bar(
                    x=counts,
                    y=names,
                    orientation="h",
                    marker_color="#D96B6B",
                    text=counts,
                    textposition="auto"
                )
            ])
            fig_mf.update_layout(
                height=180,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                xaxis=dict(gridcolor="#F5F6F8", title="Times Triggered"),
                yaxis=dict(gridcolor="#F5F6F8")
            )
            st.plotly_chart(fig_mf, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No recurring cognitive misconceptions detected in recent assessment submissions.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Panel 4: Adaptive Difficulty Engine (ZPD)
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Adaptive Difficulty Engine (Zone of Proximal Development)</span>
                <span class="lm-pill pill-ahead">Dynamic Calibration</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-top: 0.35rem;">
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #166534; text-transform: uppercase;">Beginner Tier</div>
                    <div style="font-size: 0.875rem; font-weight: 800; color: #15803D; margin: 2px 0;">P(L) < 45%</div>
                    <div style="font-size: 0.65rem; color: #4B5563;">Foundational syntax & definitions</div>
                </div>
                <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #1E40AF; text-transform: uppercase;">Intermediate</div>
                    <div style="font-size: 0.875rem; font-weight: 800; color: #1D4ED8; margin: 2px 0;">45% ≤ P(L) < 75%</div>
                    <div style="font-size: 0.65rem; color: #4B5563;">Execution traces & combinations</div>
                </div>
                <div style="background: #FAF5FF; border: 1px solid #E9D5FF; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #6B21A8; text-transform: uppercase;">Advanced Tier</div>
                    <div style="font-size: 0.875rem; font-weight: 800; color: #7E22CE; margin: 2px 0;">P(L) ≥ 75%</div>
                    <div style="font-size: 0.65rem; color: #4B5563;">Boundary cases & optimizations</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 3. INTERACTIVE BKT STEP-THROUGH CALCULATOR
    # ==========================================================
    with st.expander("🔬 Interactive Bayesian Updating Mathematics (Step-by-Step Simulator)", expanded=False):
        st.markdown("""
        Inspect how SARVAVIDYA mathematically updates posterior belief when a student answers an assessment question.
        $$P(L_t \\mid \\text{Correct}) = \\frac{P(L_{t-1}) \\cdot (1 - P(S))}{P(L_{t-1}) \\cdot (1 - P(S)) + (1 - P(L_{t-1})) \\cdot P(G)}$$
        $$P(L_t \\mid \\text{Incorrect}) = \\frac{P(L_{t-1}) \\cdot P(S)}{P(L_{t-1}) \\cdot P(S) + (1 - P(L_{t-1})) \\cdot (1 - P(G))}$$
        $$P(L_{t+1}) = P(L_t \\mid \\text{Obs}) + (1 - P(L_t \\mid \\text{Obs})) \\cdot P(T)$$
        """, unsafe_allow_html=True)

        col_sim_prior, col_sim_obs = st.columns([1.2, 1.0])
        with col_sim_prior:
            sim_prior = st.slider("Simulated Prior Mastery P(Lt-1)", 0.05, 0.95, 0.50, 0.05, key="sim_bkt_prior")
        with col_sim_obs:
            sim_result = st.radio("Student Assessment Response", ["Correct Submission", "Incorrect Submission"], horizontal=True, key="sim_bkt_res")

        is_corr = sim_result == "Correct Submission"
        new_mastery = BayesianKnowledgeTracing.update_mastery(sim_prior, is_corr)
        delta = new_mastery - sim_prior

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Prior Mastery P(Lt-1)", f"{sim_prior:.1%}")
        with col_m2:
            st.metric("Updated Posterior P(Lt+1)", f"{new_mastery:.1%}", delta=f"{delta:+.1%}")
        with col_m3:
            adaptive_tier = RecommenderEngine.get_adaptive_difficulty(new_mastery).capitalize()
            st.metric("Recommended Adaptive Tier", adaptive_tier)

    # ==========================================================
    # 4. "HOW SARVAVIDYA UNDERSTANDS YOUR LEARNING" PANEL
    # ==========================================================
    st.markdown("""
    <div style="margin-top: 1.5rem; margin-bottom: 0.75rem;">
        <h3 style="font-size: 1.25rem; font-weight: 800; color: #172943; margin: 0 0 0.25rem 0;">
            How SARVAVIDYA Understands Your Learning
        </h3>
        <p style="font-size: 0.775rem; color: #718096; margin: 0;">
            Our end-to-end cognitive architecture for hackathon evaluation and empirical student tracking.
        </p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 1.5rem;">
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; box-shadow: 0 2px 6px rgba(23,41,67,0.04);">
            <div style="font-size: 0.65rem; font-weight: 800; color: #D6B56D; text-transform: uppercase;">STEP 1</div>
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin: 3px 0;">Performance Telemetry</div>
            <div style="font-size: 0.7rem; color: #64748B; line-height: 1.4;">
                Every interaction logs accuracy, response latency, and selected distractor options.
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; box-shadow: 0 2px 6px rgba(23,41,67,0.04);">
            <div style="font-size: 0.65rem; font-weight: 800; color: #D6B56D; text-transform: uppercase;">STEP 2</div>
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin: 3px 0;">Bayesian Tracing</div>
            <div style="font-size: 0.7rem; color: #64748B; line-height: 1.4;">
                BKT updates latent mastery probabilities P(L) accounting for lucky guesses and accidental slips.
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; box-shadow: 0 2px 6px rgba(23,41,67,0.04);">
            <div style="font-size: 0.65rem; font-weight: 800; color: #D6B56D; text-transform: uppercase;">STEP 3</div>
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin: 3px 0;">Misconception Detection</div>
            <div style="font-size: 0.7rem; color: #64748B; line-height: 1.4;">
                Incorrect choices map directly to labeled cognitive errors rather than generic false scores.
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; box-shadow: 0 2px 6px rgba(23,41,67,0.04);">
            <div style="font-size: 0.65rem; font-weight: 800; color: #D6B56D; text-transform: uppercase;">STEP 4</div>
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin: 3px 0;">Adaptive Questions</div>
            <div style="font-size: 0.7rem; color: #64748B; line-height: 1.4;">
                Questions dynamically scale to maintain the student in their Zone of Proximal Development.
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; box-shadow: 0 2px 6px rgba(23,41,67,0.04);">
            <div style="font-size: 0.65rem; font-weight: 800; color: #D6B56D; text-transform: uppercase;">STEP 5</div>
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin: 3px 0;">Personalized Paths</div>
            <div style="font-size: 0.7rem; color: #64748B; line-height: 1.4;">
                Actionable recommendations span 6 pedagogical categories with estimated study effort.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Misconception Catalog
    st.markdown("<div style='font-size: 0.875rem; font-weight: 700; color: #243B64; margin: 1rem 0 0.5rem 0;'>Cataloged Cognitive Fallacy Descriptions & Remediation</div>", unsafe_allow_html=True)
    if patterns:
        for p in patterns:
            meta = MisconceptionEngine.get_info(p["code"])
            st.markdown(f"""
            <div class="lm-card" style="padding: 0.85rem; margin-bottom: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 700; font-size: 0.825rem; color: #243B64;">{p['name']}</span>
                        <span style="font-size: 0.675rem; color: #718096; background: #F5F6F8; padding: 2px 6px; border-radius: 4px;">{p['code']}</span>
                    </div>
                    <span class="lm-pill pill-lagging">{p['count']} Identified</span>
                </div>
                <div style="font-size: 0.75rem; color: #718096; margin-bottom: 0.35rem; line-height: 1.4;">
                    <strong>Underlying Cognition:</strong> {meta['description'] if meta else ''}
                </div>
                <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.75rem; color: #36A879;">
                    <strong>Pedagogical Remediation:</strong> {meta['remediation'] if meta else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
