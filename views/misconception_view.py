"""
LearnSphere AI: Misconception Diagnostics and Cognitive Bug Tracking
Visualizes detected misconception categories, frequency distributions,
and links directly to targeted corrective lessons.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.db import get_user_attempts, get_all_concepts
from core.misconception import MisconceptionEngine


def render_misconception_page(user: dict):
    user_id = user["id"]
    attempts = get_user_attempts(user_id, limit=50)

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0;">
            Cognitive Misconception Analysis
        </h2>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.25rem;">
            Detailed diagnosis of recurring cognitive bugs, mental model misalignments, and corrective actions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Summarize patterns from attempt history
    summary = MisconceptionEngine.summarize_patterns(attempts)
    patterns = summary["patterns"]

    # 1. High-Level Summary Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Total Misconceptions Detected</div>
            <div class="ls-metric-val">{summary['total_misconceptions_detected']}</div>
            <div class="ls-metric-sub">Distractor pattern occurrences</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Distinct Cognitive Fallacies</div>
            <div class="ls-metric-val">{summary['unique_patterns_count']}</div>
            <div class="ls-metric-sub">Cataloged error categories</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Dominant Difficulty Domain</div>
            <div class="ls-metric-val" style="font-size: 1.4rem;">{summary['dominant_category']}</div>
            <div class="ls-metric-sub">Most frequent mistake domain</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Plotly Frequency Distribution
    if patterns:
        df_p = pd.DataFrame(patterns)
        fig = px.bar(
            df_p,
            x="count",
            y="name",
            orientation="h",
            labels={"count": "Detected Occurrences", "name": "Misconception"},
            color="severity",
            color_discrete_map={"High": "#dc2626", "Moderate": "#d97706", "Low": "#2563eb"}
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(family="Inter, sans-serif", size=12, color="#0f172a"),
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False)
        )

        st.markdown("""
        <div class="ls-card">
            <div class="ls-card-header">
                <h3 class="ls-card-title">Cognitive Fallacy Frequency Distribution</h3>
                <span class="ls-card-desc">Frequency of specific distractor selections across your assessment attempts.</span>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Detailed Misconception Cards with Pedagogical Remediation
        st.markdown("""
        <div class="ls-card">
            <div class="ls-card-header">
                <h3 class="ls-card-title">Identified Cognitive Bugs and Remedial Actions</h3>
            </div>
        """, unsafe_allow_html=True)

        for p in patterns:
            meta = MisconceptionEngine.get_info(p["code"])
            sev_badge = "badge-novice" if p["severity"] == "High" else ("badge-developing" if p["severity"] == "Moderate" else "badge-proficient")
            col_info, col_action = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div style="padding: 1rem 0; border-bottom: 1px solid #f1f5f9;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
                        <span class="ls-badge {sev_badge}">{p['severity']} Severity</span>
                        <strong style="color: #0f172a; font-size: 1rem;">{p['name']}</strong>
                        <span style="color: #64748b; font-size: 0.8rem;">({p['category']}) &bull; {p['count']} occurrences</span>
                    </div>
                    <p style="color: #475569; font-size: 0.875rem; margin-bottom: 0.5rem; line-height: 1.5;">
                        <strong>Root Cause:</strong> {meta['description'] if meta else ''}
                    </p>
                    <div style="background-color: #f8fafc; border-left: 3px solid #2563eb; padding: 0.5rem 0.75rem; font-size: 0.825rem; color: #1e3a8a; border-radius: 0 4px 4px 0;">
                        <strong>Remediation Strategy:</strong> {p['remediation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_action:
                st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
                if st.button("Review Module", key=f"fix_btn_{p['code']}", use_container_width=True):
                    # Map category to lesson
                    cat_map = {
                        "Data Structures": "LIST",
                        "Data Types": "VAR",
                        "Variables": "VAR",
                        "Conditional Logic": "COND",
                        "Control Flow": "LOOP",
                        "Functions": "FUNC",
                        "Recursion": "REC"
                    }
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = cat_map.get(p["category"], "VAR")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ls-card">
            <div class="ls-card-header">
                <h3 class="ls-card-title">No Recurring Misconceptions Detected</h3>
            </div>
            <p style="color: #64748b; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                Either no assessment attempts have been submitted yet, or all previous answers demonstrated correct cognitive models. Complete additional assessments to monitor your learning trajectory.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 4. Taxonomy Reference
    st.markdown("""
    <div class="ls-card" style="margin-top: 1.5rem;">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Cognitive Taxonomy Architecture</h3>
        </div>
        <p style="color: #475569; font-size: 0.85rem; line-height: 1.55;">
            LearnSphere AI utilizes an explicit, rule-verified taxonomy of programming misconceptions based on computer science education research (CSEd). Each distractor choice in the question bank is tagged with its cognitive bug code, allowing deterministic error tracking without opaque hallucinations.
        </p>
    </div>
    """, unsafe_allow_html=True)

