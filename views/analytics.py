"""
LearnSphere AI: Interactive Learning Performance Analytics
Compact enterprise educational visualizations:
- Concept mastery radar chart with 60% proficiency benchmark
- Assessment accuracy donut chart
- Longitudinal BKT knowledge tracing trend line
- Performance by difficulty tier and latency distribution
- Supervised machine learning predictive cognitive risk model
- CSV telemetry export
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
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin: 0; letter-spacing: -0.02em;">Learning Analytics & Performance Intelligence</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Empirical telemetry tracing BKT scores, accuracy distribution, and psychometric latency.</div>
        </div>
        <span class="lm-pill pill-completed">Telemetry Sync</span>
    </div>
    """, unsafe_allow_html=True)

    if not attempts:
        st.info("Complete assessment exercises to populate detailed analytical visualizations.")
        return

    df_att = pd.DataFrame(attempts)
    df_att["attempt_number"] = range(len(df_att), 0, -1)
    df_att = df_att.sort_values("attempt_number")

    # 1. Concept Mastery Radar & Accuracy Donut
    col_chart1, col_chart2 = st.columns([1.2, 1])

    with col_chart1:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Concept Mastery Radar (BKT Latent Estimates)</span>
                <span style="font-size: 0.7rem; color: #718096;">Benchmark 60%</span>
            </div>
        """, unsafe_allow_html=True)

        categories = [m["concept_code"] for m in mastery_data]
        values = [m["mastery_prob"] * 100 for m in mastery_data]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(57, 118, 185, 0.18)',
            line=dict(color='#3976B9', width=2),
            name='Learner Mastery'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[60] * (len(categories) + 1),
            theta=categories + [categories[0]],
            line=dict(color='#718096', width=1.5, dash='dot'),
            name='Proficiency (60%)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#718096', gridcolor='#E4E8ED'),
                angularaxis=dict(color='#243B64', gridcolor='#E4E8ED')
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.15, font=dict(size=10)),
            margin=dict(l=25, r=25, t=15, b=25),
            height=250,
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", size=11, color="#263445")
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Assessment Accuracy Distribution</span>
                <span style="font-size: 0.7rem; color: #718096;">Total: {} Items</span>
            </div>
        """.format(len(attempts)), unsafe_allow_html=True)

        correct_count = sum(1 for a in attempts if a["is_correct"])
        incorrect_count = len(attempts) - correct_count

        fig_pie = go.Figure(data=[go.Pie(
            labels=["Correct Responses", "Misconceptions Flagged"],
            values=[correct_count, incorrect_count],
            hole=0.65,
            marker_colors=["#36A879", "#D96B6B"]
        )])
        fig_pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=250,
            paper_bgcolor="#FFFFFF",
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.1, font=dict(size=10)),
            font=dict(family="Inter, sans-serif", size=11, color="#263445")
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Longitudinal Knowledge Tracing Evolution
    st.markdown("""
    <div class="lm-card">
        <div class="lm-card-header">
            <span class="lm-card-title">Longitudinal Knowledge Tracing Evolution</span>
            <span style="font-size: 0.7rem; color: #718096;">Posterior P(L) progression across opportunities</span>
        </div>
    """, unsafe_allow_html=True)

    fig_trend = px.line(
        df_att,
        x="attempt_number",
        y="posterior_mastery",
        color="concept_name",
        markers=True,
        labels={"attempt_number": "Opportunity Index", "posterior_mastery": "BKT P(L)"},
        color_discrete_sequence=["#3976B9", "#36A879", "#E9AA45", "#243B64", "#D96B6B", "#718096"]
    )
    fig_trend.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=True, gridcolor="#F5F6F8"),
        yaxis=dict(showgrid=True, gridcolor="#F5F6F8", range=[0.0, 1.0]),
        legend=dict(orientation="h", y=-0.25, font=dict(size=10)),
        font=dict(family="Inter, sans-serif", size=11, color="#263445")
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Supervised Machine Learning Risk Engine
    st.markdown("""
    <div class="lm-card">
        <div class="lm-card-header">
            <span class="lm-card-title">Scikit-Learn Predictive Cognitive Risk Model</span>
            <span class="lm-pill pill-ahead">Supervised Model</span>
        </div>
    """, unsafe_allow_html=True)

    from core.ml_predictor import PredictiveLearningEngine
    ml_engine = PredictiveLearningEngine()
    train_meta = ml_engine.train()

    col_ml_meta, col_ml_sim = st.columns(2)
    with col_ml_meta:
        st.markdown(f"""
        <div style="font-size: 0.775rem; color: #718096; margin-bottom: 0.5rem;">
            Model: <strong>Logistic Regression</strong> &bull; Samples: <code>{train_meta['sample_count']}</code> &bull; Accuracy: <code>{train_meta['training_accuracy']:.1%}</code>
        </div>
        """, unsafe_allow_html=True)

        df_coef = pd.DataFrame([
            {"Feature": k.replace("_", " ").title(), "Weight": v}
            for k, v in train_meta["coefficients"].items()
        ]).sort_values("Weight", ascending=False)

        fig_coef = px.bar(
            df_coef,
            x="Weight",
            y="Feature",
            orientation="h",
            color="Weight",
            color_continuous_scale=["#D96B6B", "#718096", "#36A879"]
        )
        fig_coef.update_layout(
            height=160,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            coloraxis_showscale=False,
            font=dict(family="Inter, sans-serif", size=10, color="#263445")
        )
        st.plotly_chart(fig_coef, use_container_width=True, config={"displayModeBar": False})

    with col_ml_sim:
        st.markdown("<div style='font-size: 0.775rem; font-weight: 700; color: #243B64; margin-bottom: 0.35rem;'>Simulate Outcome Probability</div>", unsafe_allow_html=True)
        sim_c_order = st.slider("Curriculum Index (1 = VAR, 6 = REC)", 1, 6, 3)
        sim_diff = st.selectbox("Question Difficulty", ["beginner", "intermediate", "advanced"], index=1)
        sim_lat = st.slider("Hypothetical Latency (sec)", 5.0, 60.0, 20.0, 1.0)

        hist_acc = (sum(1 for a in attempts if a["is_correct"]) / len(attempts)) if attempts else 0.50
        curr_mastery = mastery_data[sim_c_order - 1]["mastery_prob"] if sim_c_order <= len(mastery_data) else 0.50

        pred_res = ml_engine.predict_success_probability(
            prior_mastery=curr_mastery,
            difficulty=sim_diff,
            response_time_sec=sim_lat,
            concept_order=sim_c_order,
            historical_accuracy=hist_acc
        )

        r_color = "#36A879" if pred_res["risk_tier"] == "Low Risk" else ("#E9AA45" if pred_res["risk_tier"] == "Moderate Risk" else "#D96B6B")
        st.markdown(f"""
        <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.75rem; margin-top: 0.35rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.775rem; color: #718096;">Predicted Success Probability:</span>
                <strong style="font-size: 1rem; color: #243B64;">{pred_res['success_probability']:.1%}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.2rem;">
                <span style="font-size: 0.775rem; color: #718096;">Cognitive Risk Level:</span>
                <strong style="color: {r_color}; font-size: 0.85rem;">{pred_res['risk_tier']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Export Telemetry Dataset
    csv_bytes = df_att.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Learning Telemetry to CSV",
        data=csv_bytes,
        file_name=f"learnsphere_telemetry_{user.get('username', 'student')}.csv",
        mime="text/csv",
        use_container_width=True
    )
