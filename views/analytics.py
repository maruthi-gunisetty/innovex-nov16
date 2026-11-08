"""
LearnSphere AI: Interactive Student Learning Analytics
Generates Plotly interactive data visualizations covering BKT mastery radar,
longitudinal performance trends, and difficulty breakdowns.
Modern minimalist SaaS design inspired by Linear and Stripe.
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
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #172554; margin: 0; letter-spacing: -0.025em;">
            Learning Intelligence and Performance Analytics
        </h2>
        <p style="color: #64748B; font-size: 0.875rem; margin-top: 0.25rem;">
            Empirical telemetry tracing Bayesian Knowledge Tracing scores, cognitive accuracy, and response latency.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not attempts:
        st.info("Complete assessment exercises to populate detailed analytical visualizations.")
        return

    df_att = pd.DataFrame(attempts)
    df_att["attempt_number"] = range(len(df_att), 0, -1)
    df_att = df_att.sort_values("attempt_number")

    # 1. Concept Mastery Radar / Bar Visual
    col_chart1, col_chart2 = st.columns([1.2, 1])

    with col_chart1:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 0.95rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
                Curriculum Concept Mastery (BKT Latent Estimates)
            </h4>
        """, unsafe_allow_html=True)

        categories = [m["concept_code"] for m in mastery_data]
        values = [m["mastery_prob"] * 100 for m in mastery_data]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(99, 91, 219, 0.20)',
            line=dict(color='#635BDB', width=2),
            name='Student Mastery'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[60] * (len(categories) + 1),
            theta=categories + [categories[0]],
            line=dict(color='#94A3B8', width=1.5, dash='dot'),
            name='Proficiency Benchmark (60%)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#64748B', gridcolor='#E2E8F0'),
                angularaxis=dict(color='#0F172A', gridcolor='#E2E8F0')
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.15),
            margin=dict(l=30, r=30, t=20, b=30),
            height=320,
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 0.95rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
                Assessment Accuracy Distribution
            </h4>
        """, unsafe_allow_html=True)

        correct_count = sum(1 for a in attempts if a["is_correct"])
        incorrect_count = len(attempts) - correct_count

        fig_pie = go.Figure(data=[go.Pie(
            labels=["Correct Responses", "Misconceptions Flagged"],
            values=[correct_count, incorrect_count],
            hole=0.6,
            marker_colors=["#16A34A", "#DC2626"]
        )])
        fig_pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            paper_bgcolor="#FFFFFF",
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.1),
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Mastery Evolution Over Time
    st.markdown("""
    <div class="ls-card">
        <h4 style="font-size: 0.95rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
            Longitudinal Knowledge Tracing Evolution
        </h4>
        <div class="ls-card-desc">Chronological progression of BKT posterior mastery estimates across successive attempts.</div>
    """, unsafe_allow_html=True)

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
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", range=[0.0, 1.0]),
        legend=dict(orientation="h", y=-0.25),
        font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Difficulty Tier and Response Latency Breakdown
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 0.95rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
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
            color_discrete_map={"beginner": "#16A34A", "intermediate": "#2563EB", "advanced": "#635BDB"}
        )
        fig_diff.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            showlegend=False,
            yaxis=dict(range=[0, 100], gridcolor="#F1F5F9"),
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
        )
        st.plotly_chart(fig_diff, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 0.95rem; font-weight: 600; color: #172554; margin-bottom: 0.5rem;">
                Response Latency Distribution (Seconds)
            </h4>
        """, unsafe_allow_html=True)

        fig_hist = px.histogram(
            df_att,
            x="response_time_sec",
            nbins=12,
            labels={"response_time_sec": "Time to Answer (sec)"},
            color_discrete_sequence=["#172554"]
        )
        fig_hist.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            xaxis=dict(gridcolor="#F1F5F9"),
            yaxis=dict(gridcolor="#F1F5F9"),
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Supervised Machine Learning Risk Engine (Scikit-Learn)
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-violet">Supervised Machine Learning</span>
                <h3 class="ls-card-title" style="margin-top: 0.25rem;">Scikit-Learn Predictive Cognitive Risk Model</h3>
                <div class="ls-card-desc">Trained on empirical telemetry (prior mastery, question tier, latency, curriculum order) to forecast success probabilities.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    from core.ml_predictor import PredictiveLearningEngine
    ml_engine = PredictiveLearningEngine()
    train_meta = ml_engine.train()

    col_ml_coef, col_ml_sim = st.columns([1, 1])
    with col_ml_coef:
        st.markdown(f"**Model Specifications:** Logistic Regression &bull; Dataset Size: `{train_meta['sample_count']}` observations &bull; Accuracy: `{train_meta['training_accuracy']:.1%}`")
        df_coef = pd.DataFrame([
            {"Feature": k.replace("_", " ").title(), "Coefficient Weight": v}
            for k, v in train_meta["coefficients"].items()
        ]).sort_values("Coefficient Weight", ascending=False)

        fig_coef = px.bar(
            df_coef,
            x="Coefficient Weight",
            y="Feature",
            orientation="h",
            color="Coefficient Weight",
            color_continuous_scale=["#DC2626", "#94A3B8", "#16A34A"]
        )
        fig_coef.update_layout(
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            coloraxis_showscale=False,
            font=dict(family="Inter, sans-serif", size=11, color="#0F172A")
        )
        st.plotly_chart(fig_coef, use_container_width=True)

    with col_ml_sim:
        st.markdown("**Simulate Success Probability for Target Assessment:**")
        sim_c_order = st.slider("Curriculum Concept Order (1 = VAR, 6 = REC)", 1, 6, 3)
        sim_diff = st.selectbox("Simulated Question Difficulty", ["beginner", "intermediate", "advanced"], index=1)
        sim_lat = st.slider("Hypothetical Response Latency (seconds)", 5.0, 60.0, 20.0, 1.0)

        hist_acc = (sum(1 for a in attempts if a["is_correct"]) / len(attempts)) if attempts else 0.50
        curr_mastery = mastery_data[sim_c_order - 1]["mastery_prob"] if sim_c_order <= len(mastery_data) else 0.50

        pred_res = ml_engine.predict_success_probability(
            prior_mastery=curr_mastery,
            difficulty=sim_diff,
            response_time_sec=sim_lat,
            concept_order=sim_c_order,
            historical_accuracy=hist_acc
        )

        risk_color = "#16A34A" if pred_res["risk_tier"] == "Low Risk" else ("#F59E0B" if pred_res["risk_tier"] == "Moderate Risk" else "#DC2626")
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; margin-top: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="font-size: 0.85rem; color: #64748B;">Predicted Success Probability:</span>
                <strong style="font-size: 1.15rem; color: #172554;">{pred_res['success_probability']:.1%}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.85rem; color: #64748B;">Risk Classification:</span>
                <strong style="color: {risk_color};">{pred_res['risk_tier']}</strong>
            </div>
            <div style="font-size: 0.775rem; color: #64748B; margin-top: 0.5rem;">
                Primary Driver: {pred_res['primary_driver']} &bull; Based on Current Concept Mastery: {curr_mastery:.1%}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Export Telemetry Dataset
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    csv_bytes = df_att.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Learning Telemetry to CSV",
        data=csv_bytes,
        file_name=f"learnsphere_telemetry_{user.get('username', 'student')}.csv",
        mime="text/csv",
        use_container_width=True
    )
