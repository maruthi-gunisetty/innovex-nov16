"""
LearnSphere AI: Personalized Learning Path and Roadmap
Visualizes curriculum dependency graphs, prerequisite bottlenecks,
mastery statuses, and tailored progression milestones.
Modern minimalist SaaS design inspired by Linear and Notion.
"""

import streamlit as st
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress
)
from core.bkt import BayesianKnowledgeTracing
from core.recommender import RecommenderEngine


def render_learning_path_page(user: dict):
    user_id = user["id"]
    mastery_data = get_student_mastery(user_id)
    attempts = get_user_attempts(user_id, limit=30)
    lesson_progress = get_user_lesson_progress(user_id)
    mastery_map = {m["concept_code"]: m["mastery_prob"] for m in mastery_data}

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #172554; margin: 0; letter-spacing: -0.025em;">
            Personalized Curriculum Roadmap
        </h2>
        <p style="color: #64748B; font-size: 0.875rem; margin-top: 0.25rem;">
            Dynamic learning pathway built from concept prerequisite dependencies and Bayesian Knowledge Tracing scores.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Dependency Graph / Linear Flow Overview
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <h3 class="ls-card-title">Curriculum Prerequisite Progression</h3>
                <div class="ls-card-desc">Concepts unlock when prerequisites achieve the 60% mastery benchmark.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    bkt = BayesianKnowledgeTracing()
    for idx, c_code in enumerate(RecommenderEngine.CONCEPT_ORDER):
        m_row = next((m for m in mastery_data if m["concept_code"] == c_code), None)
        if not m_row:
            continue

        c_prob = m_row["mastery_prob"]
        prereq_eval = RecommenderEngine.evaluate_prerequisites(c_code, mastery_map)
        classification = bkt.classify_mastery(c_prob)

        # Status logic
        if not prereq_eval["eligible"]:
            status_text = "Locked by Prerequisites"
            status_badge = '<span class="ls-badge badge-novice">Prerequisite Gap</span>'
            card_border = "#FECACA"
            bg_color = "#FFFFFF"
        elif c_prob >= 0.85:
            status_text = "Concept Mastered"
            status_badge = '<span class="ls-badge badge-mastered">Mastered</span>'
            card_border = "#BBF7D0"
            bg_color = "#FFFFFF"
        elif c_prob >= 0.60:
            status_text = "Proficient &bull; Unlocked"
            status_badge = '<span class="ls-badge badge-proficient">Proficient</span>'
            card_border = "#BFDBFE"
            bg_color = "#FFFFFF"
        else:
            status_text = "Active Learning Target"
            status_badge = '<span class="ls-badge badge-developing">In Progress</span>'
            card_border = "#FDE68A"
            bg_color = "#FFFFFF"

        prereqs_str = ", ".join(prereq_eval["prerequisites"]) if prereq_eval["prerequisites"] else "None (Foundational Entry)"
        suggested_diff = RecommenderEngine.get_adaptive_difficulty(c_prob).capitalize()

        col_left, col_right = st.columns([4, 1.2])
        with col_left:
            st.markdown(f"""
            <div style="background-color: {bg_color}; border: 1px solid {card_border}; border-radius: 8px; padding: 1.1rem 1.25rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-weight: 700; color: #172554; font-size: 1.05rem;">{idx + 1}. {m_row['concept_name']}</span>
                        <span style="font-size: 0.725rem; color: #64748B; font-weight: 600;">[{c_code}]</span>
                    </div>
                    {status_badge}
                </div>
                <div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.5rem;">
                    {m_row['description']}
                </div>
                <div style="display: flex; gap: 1.5rem; font-size: 0.775rem; color: #64748B;">
                    <span>Prerequisites: <strong>{prereqs_str}</strong></span>
                    <span>BKT Mastery: <strong style="color: #0F172A;">{c_prob:.1%}</strong></span>
                    <span>Recommended Difficulty: <strong>{suggested_diff}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if prereq_eval["eligible"]:
                if st.button("Study Concept", key=f"lp_study_{c_code}", use_container_width=True):
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = c_code
                    st.rerun()
                if st.button("Practice Questions", key=f"lp_prac_{c_code}", use_container_width=True, type="primary"):
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = m_row["concept_id"]
                    st.rerun()
            else:
                unmet_names = [u["concept_code"] for u in prereq_eval["unmet_prerequisites"]]
                st.caption(f"Requires: {', '.join(unmet_names)}")
                if st.button("Resolve Prerequisite", key=f"lp_resolve_{c_code}", use_container_width=True, type="secondary"):
                    first_unmet = prereq_eval["unmet_prerequisites"][0]["concept_code"]
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = first_unmet
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Strategic Next Action Recommendation
    recs = RecommenderEngine.generate_recommendations(user_id, mastery_data, attempts, lesson_progress)
    if recs:
        primary = recs[0]
        st.markdown(f"""
        <div class="ls-card" style="border-left: 4px solid #635BDB;">
            <div class="ls-card-header">
                <div>
                    <span class="ls-badge badge-violet">Recommended Immediate Action</span>
                    <h3 class="ls-card-title" style="margin-top: 0.35rem;">{primary['title']}</h3>
                </div>
            </div>
            <p style="color: #475569; font-size: 0.875rem; line-height: 1.6; margin-bottom: 1rem;">
                {primary['reason']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            if st.button("Open Recommended Lesson", type="primary", use_container_width=True):
                st.session_state["current_page"] = "learning_library"
                st.session_state["selected_lesson_code"] = primary["concept_code"]
                st.rerun()
        with col_act2:
            if st.button("Launch Adaptive Practice Drill", use_container_width=True):
                st.session_state["current_page"] = "assessment"
                st.session_state["assessment_concept_id"] = primary["concept_id"]
                st.rerun()
