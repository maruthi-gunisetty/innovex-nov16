"""
LearnSphere AI: Faculty and Teacher Dashboard
Provides class-wide learning telemetry, cohort mastery distributions,
common misconception trends, and individual student diagnostic inspection.
Modern minimalist SaaS design inspired by Linear and Stripe.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.db import (
    get_class_overview, get_all_students, get_student_mastery,
    get_user_attempts
)
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine


def render_teacher_dashboard(user: dict):
    if user.get("role") not in ("teacher", "admin"):
        st.error("Access restricted: This portal is reserved for verified faculty accounts.")
        return

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: #EEF2FF; color: #635BDB; border: 1px solid #C7D2FE; padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.725rem; font-weight: 600; text-transform: uppercase;">
            Faculty Management Portal
        </div>
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #172554; margin-top: 0.5rem; margin-bottom: 0.25rem; letter-spacing: -0.025em;">
            Cohort Performance and Learning Gap Analytics
        </h2>
        <p style="color: #64748B; font-size: 0.875rem;">
            Instructor: {user['full_name']} &bull; Monitor cohort-wide knowledge distribution and diagnose systemic instructional gaps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    overview = get_class_overview()
    students = get_all_students()

    # 1. High-Level Class Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Enrolled Students</div>
            <div class="ls-metric-val">{overview['total_students']}</div>
            <div class="ls-metric-sub">Active learner records</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Assessments Completed</div>
            <div class="ls-metric-val">{overview['total_attempts']}</div>
            <div class="ls-metric-sub">Across all concepts</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Class Average Accuracy</div>
            <div class="ls-metric-val">{overview['avg_accuracy']:.1%}</div>
            <div class="ls-metric-sub">Raw empirical performance</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        cm_list = overview["concept_masteries"]
        cohort_avg = (sum(c["avg_mastery"] for c in cm_list) / len(cm_list)) if cm_list else 0.20
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Cohort Average BKT</div>
            <div class="ls-metric-val">{cohort_avg:.1%}</div>
            <div class="ls-metric-sub">Latent mastery estimate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Class-Wide Concept Mastery Comparison
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Class-Wide Concept Mastery Distribution</h3>
            <span class="ls-card-desc">Average latent mastery P(L) across all active students per curriculum unit.</span>
        </div>
    """, unsafe_allow_html=True)

    if cm_list:
        df_cm = pd.DataFrame(cm_list)
        df_cm["avg_pct"] = df_cm["avg_mastery"] * 100
        fig_cm = px.bar(
            df_cm,
            x="concept_name",
            y="avg_pct",
            labels={"concept_name": "Curriculum Concept", "avg_pct": "Average BKT Mastery (%)"},
            color="avg_pct",
            color_continuous_scale=["#DC2626", "#F59E0B", "#2563EB", "#16A34A"]
        )
        fig_cm.add_hline(y=60, line_dash="dash", line_color="#475569", annotation_text="Target Benchmark (60%)")
        fig_cm.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            coloraxis_showscale=False,
            yaxis=dict(range=[0, 100], gridcolor="#F1F5F9"),
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
        )
        st.plotly_chart(fig_cm, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Systemic Misconception Frequency (Class Bottlenecks)
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Systemic Cohort Misconceptions</h3>
            <span class="ls-card-desc">Cognitive bugs repeatedly triggered by multiple students during assessment.</span>
        </div>
    """, unsafe_allow_html=True)

    top_m = overview.get("top_misconceptions", [])
    if top_m:
        cols = st.columns(len(top_m))
        for idx, item in enumerate(top_m):
            meta = MisconceptionEngine.get_info(item["misconception_code"])
            m_name = meta["name"] if meta else item["misconception_code"]
            with cols[idx]:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 1px solid #FECACA; border-radius: 8px; padding: 1rem; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 700; color: #DC2626;">{item['count']}</div>
                    <div style="font-weight: 600; color: #172554; font-size: 0.85rem; margin-top: 0.25rem;">{m_name}</div>
                    <div style="font-size: 0.725rem; color: #64748B; margin-top: 0.25rem;">{meta['category'] if meta else ''}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No systemic misconceptions logged across the student cohort yet.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Individual Student Deep-Dive Inspection
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h3 class="ls-card-title">Individual Student Diagnostic Deep Dive</h3>
            <span class="ls-card-desc">Inspect specific student knowledge states and diagnosed misconceptions.</span>
        </div>
    """, unsafe_allow_html=True)

    student_options = {f"{s['full_name']} ({s['username']})": s["id"] for s in students}
    if student_options:
        selected_stu_label = st.selectbox("Select Student for Diagnostic Inspection", list(student_options.keys()))
        selected_stu_id = student_options[selected_stu_label]
        target_student = next(s for s in students if s["id"] == selected_stu_id)

        stu_mastery = get_student_mastery(selected_stu_id)
        stu_attempts = get_user_attempts(selected_stu_id, limit=20)

        col_st1, col_st2 = st.columns([1, 1])
        with col_st1:
            st.markdown(f"**Student Profile:** {target_student['full_name']} &bull; Email: `{target_student['email']}`")
            bkt = BayesianKnowledgeTracing()
            for m in stu_mastery:
                cls_info = bkt.classify_mastery(m["mastery_prob"])
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #F1F5F9; font-size: 0.85rem;">
                    <span><strong>{m['concept_name']}</strong></span>
                    <span>
                        <span class="ls-badge {cls_info['badge_class']}">{cls_info['tier']}</span>
                        <strong style="margin-left: 0.5rem; color: #0F172A;">{m['mastery_prob']:.1%}</strong>
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with col_st2:
            st.markdown(f"**Recent Cognitive Diagnoses ({len(stu_attempts)} recorded attempts):**")
            incorrect_diagnoses = [a for a in stu_attempts if not a["is_correct"]]
            if incorrect_diagnoses:
                for att in incorrect_diagnoses[:5]:
                    m_code = att.get("misconception_code")
                    m_info = MisconceptionEngine.get_info(m_code)
                    st.markdown(f"""
                    <div style="background-color: #FFF1F2; border: 1px solid #FECDD3; border-radius: 6px; padding: 0.5rem 0.75rem; margin-bottom: 0.5rem; font-size: 0.825rem;">
                        <strong>{att['question_title']}</strong> &bull; {att['concept_name']}<br>
                        <span style="color: #991B1B;">Diagnostic Code: <strong>{m_code}</strong> ({m_info['name'] if m_info else ''})</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #16A34A; font-size: 0.85rem;'>No recent incorrect attempts recorded for this student.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Cohort Telemetry Export
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if cm_list:
        df_cohort = pd.DataFrame(cm_list)
        csv_cohort_bytes = df_cohort.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export Cohort Concept Mastery Dataset to CSV",
            data=csv_cohort_bytes,
            file_name="learnsphere_cohort_mastery.csv",
            mime="text/csv",
            use_container_width=True
        )
