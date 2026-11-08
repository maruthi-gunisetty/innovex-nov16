"""
LearnSphere AI: Personalized Learning Path and Curriculum Roadmap
Enterprise educational management interface:
- Overall progress, lessons completed, current learning topic, recommended next topic
- Concept dependency progression with 60% BKT proficiency gating
- Interactive practice and study action links
"""

import streamlit as st
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress
)
from core.bkt import BayesianKnowledgeTracing
from core.recommender import RecommenderEngine
from core.course_manager import get_active_course, render_course_selector


def render_learning_path_page(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    course_id = active_course["id"]

    mastery_data = get_student_mastery(user_id, course_id=course_id)
    attempts = get_user_attempts(user_id, limit=30, course_id=course_id)
    lesson_progress = get_user_lesson_progress(user_id)
    mastery_map = {m["concept_code"]: m["mastery_prob"] for m in mastery_data}

    completed_count = sum(1 for v in lesson_progress.values() if v)
    total_count = max(len(mastery_data), 6)
    progress_pct = int((completed_count / total_count) * 100) if total_count > 0 else 50

    col_h_title, col_h_track = st.columns([2.0, 1.0])
    with col_h_title:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
            <div>
                <h2 style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin: 0; letter-spacing: -0.02em;">{active_course['name']} Roadmap</h2>
                <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Sequential concept progression governed by prerequisite mastery gates.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h_track:
        render_course_selector(key="lpath_track_selector", label="Select Track", on_change_rerun=True)

    # 1. Four Summary Header Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Curriculum Progress</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin-top: 0.15rem;">{progress_pct}%</div>
            <div class="lm-progress-wrap" style="height: 4px; margin: 0.25rem 0 0 0;">
                <div class="lm-progress-bar" style="width: {progress_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Modules Completed</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #36A879; margin-top: 0.15rem;">{completed_count} / {total_count}</div>
            <div style="font-size: 0.7rem; color: #718096;">Verified lessons finished</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        # Determine Current Learning Topic dynamically
        curr_topic = mastery_data[0]["concept_name"] if mastery_data else "Foundational Units"
        next_topic = mastery_data[1]["concept_name"] if len(mastery_data) > 1 else "Advanced Applications"
        for m_idx, m in enumerate(mastery_data):
            if m["mastery_prob"] < 0.60:
                curr_topic = m["concept_name"]
                if m_idx + 1 < len(mastery_data):
                    next_topic = mastery_data[m_idx + 1]["concept_name"]
                break

        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Current Learning Topic</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #243B64; margin-top: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{curr_topic}</div>
            <div style="font-size: 0.7rem; color: #718096;">Active focus milestone</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="font-size: 0.7rem; color: #718096; font-weight: 600; text-transform: uppercase;">Recommended Next</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #3976B9; margin-top: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{next_topic}</div>
            <div style="font-size: 0.7rem; color: #718096;">Upcoming curriculum unit</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Sequential Concept Roadmap
    st.markdown(f"""
    <div class="lm-card">
        <div class="lm-card-header">
            <span class="lm-card-title">{active_course['name']} Prerequisite Progression</span>
            <span style="font-size: 0.725rem; color: #718096;">Concepts unlock sequentially when prerequisites achieve &ge; 60% BKT mastery</span>
        </div>
    """, unsafe_allow_html=True)

    bkt = BayesianKnowledgeTracing()
    for idx, m_row in enumerate(mastery_data):
        c_code = m_row["concept_code"]
        c_prob = m_row["mastery_prob"]
        prereq_eval = RecommenderEngine.evaluate_prerequisites(c_code, mastery_map)

        if not prereq_eval["eligible"]:
            pill_badge = '<span class="lm-pill pill-lagging">Locked</span>'
            border_c = "#E4E8ED"
            bg_c = "#F5F6F8"
        elif c_prob >= 0.85:
            pill_badge = '<span class="lm-pill pill-completed">Mastered</span>'
            border_c = "#C6ECD9"
            bg_c = "#FFFFFF"
        elif c_prob >= 0.60:
            pill_badge = '<span class="lm-pill pill-ahead">Proficient</span>'
            border_c = "#D2E4F6"
            bg_c = "#FFFFFF"
        else:
            pill_badge = '<span class="lm-pill pill-ontrack">In Progress</span>'
            border_c = "#FDE8C7"
            bg_c = "#FFFFFF"

        prereqs_str = ", ".join(prereq_eval["prerequisites"]) if prereq_eval["prerequisites"] else "None (Foundational Entry)"
        suggested_diff = RecommenderEngine.get_adaptive_difficulty(c_prob).capitalize()

        col_desc, col_actions = st.columns([3.8, 1.2])
        with col_desc:
            st.markdown(f"""
            <div style="background-color: {bg_c}; border: 1px solid {border_c}; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 700; color: #243B64; font-size: 0.925rem;">{idx + 1}. {m_row['concept_name']}</span>
                        <span style="font-size: 0.675rem; color: #718096; background: #F5F6F8; padding: 1px 5px; border-radius: 3px;">[{c_code}]</span>
                    </div>
                    {pill_badge}
                </div>
                <div style="font-size: 0.775rem; color: #718096; margin-bottom: 0.35rem; line-height: 1.4;">
                    {m_row['description']}
                </div>
                <div style="display: flex; gap: 1.2rem; font-size: 0.725rem; color: #718096;">
                    <span>Prerequisites: <strong>{prereqs_str}</strong></span>
                    <span>BKT Mastery: <strong style="color: #243B64;">{c_prob:.0%}</strong></span>
                    <span>Difficulty: <strong>{suggested_diff}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_actions:
            st.markdown("<div style='padding-top: 0.4rem;'></div>", unsafe_allow_html=True)
            if prereq_eval["eligible"]:
                if st.button("Study Lesson", key=f"lp_study_{c_code}", use_container_width=True):
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = c_code
                    st.rerun()
                if st.button("Practice Drill", key=f"lp_prac_{c_code}", use_container_width=True, type="primary"):
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = m_row["concept_id"]
                    st.rerun()
            else:
                unmet = [u["concept_code"] for u in prereq_eval["unmet_prerequisites"]]
                st.caption(f"Requires: {', '.join(unmet)}")

    st.markdown("</div>", unsafe_allow_html=True)
