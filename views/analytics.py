"""
LearnSphere AI: Interactive Student Learning Analytics
Generates Plotly interactive data visualizations covering BKT mastery radar,
longitudinal performance trends, and difficulty breakdowns.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.db import get_student_mastery, get_user_attempts


def render_analytics_page(user: dict):
    user_id = user["id"]
    mastery_data = get_student_mastery(user_id)
    attempts = get_user_attempts(user_id, limit=100)

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0;">
            Learning Intelligence and Performance Analytics
        </h2>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.25rem;">
            Empirical telemetry tracing Bayesian Knowledge Tracing scores, cognitive accuracy, and response latency.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not attempts:
        st.info("Complete assessment exercises to populate detailed analytical visualizations.")
        return

    # 1. Concept Mastery Radar / Bar Visual
    col_chart1, col_chart2 = st.columns([1.2, 1])

    with col_chart1:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Curriculum Concept Mastery (BKT Latent Estimates)
            </h4>
        """, unsafe_allow_html=True)

        categories = [m["concept_code"] for m in mastery_data]
        values = [m["mastery_prob"] * 100 for m in mastery_data]

        # Radar chart
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(79, 70, 229, 0.25)',
            line=dict(color='#4f46e5', width=2),
            name='Student Mastery'
        ))
        # Add proficiency benchmark threshold at 60%
        fig_radar.add_trace(go.Scatterpolar(
            r=[60] * (len(categories) + 1),
            theta=categories + [categories[0]],
            line=dict(color='#94a3b8', width=1, dash='dot'),
            name='Proficiency Benchmark (60%)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#64748b', gridcolor='#e2e8f0'),
                angularaxis=dict(color='#0f172a', gridcolor='#e2e8f0')
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.2),
            margin=dict(l=30, r=30, t=20, b=30),
            height=320,
            paper_bgcolor="#ffffff"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Assessment Accuracy Distribution
            </h4>
        """, unsafe_allow_html=True)

        correct_count = sum(1 for a in attempts if a["is_correct"])
        incorrect_count = len(attempts) - correct_count

        fig_pie = go.Figure(data=[go.Pie(
            labels=["Correct Responses", "Incorrect (Misconception Detected)"],
            values=[correct_count, incorrect_count],
            hole=0.6,
            marker_colors=["#16a34a", "#dc2626"]
        )])
        fig_pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            paper_bgcolor="#ffffff",
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.1)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Mastery Evolution Over Time
    st.markdown("""
    <div class="ls-card">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
            Longitudinal Knowledge Tracing Evolution
        </h4>
        <div class="ls-card-desc">Chronological progression of BKT posterior mastery estimates across successive attempts.</div>
    """, unsafe_allow_html=True)

    # Convert attempts to DataFrame sorted chronologically
    df_att = pd.DataFrame(attempts)
    df_att["attempt_number"] = range(len(df_att), 0, -1)
    df_att = df_att.sort_values("attempt_number")

    fig_trend = px.line(
        df_att,
        x="attempt_number",
        y="posterior_mastery",
        color="concept_name",
        markers=True,
        labels={"attempt_number": "Sequential Opportunity Index", "posterior_mastery": "Posterior Mastery P(L)"}
    )
    fig_trend.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", range=[0.0, 1.0]),
        legend=dict(orientation="h", y=-0.25)
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Difficulty Tier and Response Latency Breakdown
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Performance by Difficulty Tier
            </h4>
        """, unsafe_allow_html=True)

        diff_summary = df_att.groupby("difficulty").agg(
            total=("is_correct", "count"),
            correct=("is_correct", "sum")
        ).reset_index()
        diff_summary["accuracy"] = (diff_summary["correct"] / diff_summary["total"]) * 100

        fig_diff = px.bar(
            diff_summary,
            x="difficulty",
            y="accuracy",
            color="difficulty",
            labels={"difficulty": "Tier", "accuracy": "Accuracy (%)"},
            color_discrete_map={"beginner": "#16a34a", "intermediate": "#2563eb", "advanced": "#7c3aed"}
        )
        fig_diff.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            showlegend=False,
            yaxis=dict(range=[0, 100], gridcolor="#f1f5f9")
        )
        st.plotly_chart(fig_diff, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Response Latency Distribution (Seconds)
            </h4>
        """, unsafe_allow_html=True)

        fig_hist = px.histogram(
            df_att,
            x="response_time_sec",
            nbins=12,
            labels={"response_time_sec": "Time to Answer (sec)"},
            color_discrete_sequence=["#4f46e5"]
        )
        fig_hist.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis=dict(gridcolor="#f1f5f9"),
            yaxis=dict(gridcolor="#f1f5f9")
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
