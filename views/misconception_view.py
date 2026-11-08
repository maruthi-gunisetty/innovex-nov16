"""
LearnSphere AI: AI Intelligence & Cognitive Misconception Dashboard
Follows the compact enterprise design language of the reference dashboard.
Panels:
1. Bayesian Knowledge Tracing mastery chart
2. Concept mastery comparison
3. Learning probability P(T), Guess P(G), Slip P(S)
4. Misconception frequency distribution
5. Weak concept analysis
6. Adaptive difficulty distribution
7. Personalized AI recommendations
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress
)
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine
from core.recommender import RecommenderEngine


def render_misconception_page(user: dict):
    user_id = user["id"]
    mastery_data = get_student_mastery(user_id)
    attempts = get_user_attempts(user_id, limit=50)
    lesson_progress = get_user_lesson_progress(user_id)
    summary = MisconceptionEngine.summarize_patterns(attempts)
    patterns = summary["patterns"]

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin: 0; letter-spacing: -0.02em;">AI Learning Intelligence Dashboard</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Corbett & Anderson (1995) Bayesian Knowledge Tracing & Cognitive Distractor Diagnostics.</div>
        </div>
        <span class="lm-pill pill-ahead">BKT Engine Active</span>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # 1. BKT CORE HYPERPARAMETERS ROW (P(L0), P(T), P(G), P(S))
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Prior Probability P(L0)</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin-top: 0.15rem;">0.20</div>
            <div style="font-size: 0.7rem; color: #718096;">Baseline initial concept mastery</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Learning Probability P(T)</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #36A879; margin-top: 0.15rem;">0.15</div>
            <div style="font-size: 0.7rem; color: #718096;">Transition probability per attempt</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Guess Probability P(G)</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #E9AA45; margin-top: 0.15rem;">0.20</div>
            <div style="font-size: 0.7rem; color: #718096;">Correct answer chance without mastery</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Slip Probability P(S)</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #D96B6B; margin-top: 0.15rem;">0.10</div>
            <div style="font-size: 0.7rem; color: #718096;">Accidental error despite mastery</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 2. MAIN 2-COLUMN INTELLIGENCE PANELS
    # ==========================================================
    col_left, col_right = st.columns([1.1, 1.2])

    with col_left:
        # Panel 1: Concept Mastery Comparison Bar Chart
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Concept Mastery Comparison (BKT Latent P(L))</span>
                <span style="font-size: 0.7rem; color: #718096;">Benchmark: 60%</span>
            </div>
        """, unsafe_allow_html=True)

        if mastery_data:
            df_m = pd.DataFrame(mastery_data)
            df_m["mastery_pct"] = df_m["mastery_prob"] * 100

            fig_bar = px.bar(
                df_m,
                x="concept_code",
                y="mastery_pct",
                color="mastery_pct",
                labels={"concept_code": "Concept", "mastery_pct": "Mastery (%)"},
                color_continuous_scale=["#D96B6B", "#E9AA45", "#3976B9", "#36A879"]
            )
            fig_bar.add_hline(y=60, line_dash="dash", line_color="#718096")
            fig_bar.update_layout(
                height=180,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                coloraxis_showscale=False,
                yaxis=dict(range=[0, 100], gridcolor="#F5F6F8"),
                xaxis=dict(gridcolor="#F5F6F8")
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Panel 2: Weak Concept Analysis
        weak_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.60]
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Weak Concept Vulnerability Analysis</span>
                <span class="lm-pill pill-lagging">Attention Required</span>
            </div>
        """, unsafe_allow_html=True)

        if weak_concepts:
            for wc in weak_concepts:
                st.markdown(f"""
                <div style="padding: 0.4rem 0; border-bottom: 1px solid #F5F6F8;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; font-size: 0.825rem; color: #243B64;">{wc['concept_name']} [{wc['concept_code']}]</span>
                        <span style="font-size: 0.75rem; font-weight: 700; color: #D96B6B;">{wc['mastery_prob']:.0%} P(L)</span>
                    </div>
                    <div style="font-size: 0.725rem; color: #718096; margin-top: 0.15rem;">
                        Vulnerability: Latent mastery is below 60% gating threshold. Prerequisite bottlenecks will stall recursion progression.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size: 0.775rem; color: #36A879;'>No critical vulnerabilities identified. All active topics meet the proficiency threshold.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Panel 3: Misconception Frequency Distribution
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Cognitive Misconception Frequency</span>
                <span style="font-size: 0.7rem; color: #718096;">Distractor patterns</span>
            </div>
        """, unsafe_allow_html=True)

        if patterns:
            df_p = pd.DataFrame(patterns)
            fig_mf = px.bar(
                df_p,
                x="count",
                y="name",
                orientation="h",
                color="category",
                labels={"count": "Times Triggered", "name": "Misconception"},
                color_discrete_map={"Boundary Condition": "#D96B6B", "Control Flow": "#E9AA45", "Data Structure": "#3976B9", "Recursion": "#243B64"}
            )
            fig_mf.update_layout(
                height=180,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                showlegend=False,
                xaxis=dict(gridcolor="#F5F6F8"),
                yaxis=dict(gridcolor="#F5F6F8")
            )
            st.plotly_chart(fig_mf, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No misconceptions logged in current telemetry.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Panel 4: Personalized AI Recommendations
        recs = RecommenderEngine.generate_recommendations(user_id, mastery_data, attempts, lesson_progress)
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Personalized AI Pedagogical Action Items</span>
                <span class="lm-pill pill-completed">Real-Time</span>
            </div>
        """, unsafe_allow_html=True)

        if recs:
            for idx, r in enumerate(recs[:2]):
                col_r_info, col_r_btn = st.columns([3.2, 1])
                with col_r_info:
                    st.markdown(f"""
                    <div style="padding: 0.35rem 0;">
                        <div style="font-weight: 700; font-size: 0.8rem; color: #243B64;">{r['title']}</div>
                        <div style="font-size: 0.725rem; color: #718096; margin-top: 0.15rem; line-height: 1.35;">{r['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_r_btn:
                    st.markdown("<div style='padding-top: 0.35rem;'></div>", unsafe_allow_html=True)
                    if st.button("Execute", key=f"rec_exec_{idx}", use_container_width=True, type="primary"):
                        if r["recommended_action"] == "library":
                            st.session_state["current_page"] = "learning_library"
                            st.session_state["selected_lesson_code"] = r["concept_code"]
                        else:
                            st.session_state["current_page"] = "assessment"
                            st.session_state["assessment_concept_id"] = r["concept_id"]
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
