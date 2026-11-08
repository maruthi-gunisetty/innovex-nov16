"""
Sarva Vidya: Unified Global Search Component
Provides real-time interactive search across:
- Concepts and Knowledge Components
- Learning Content and Interactive Code Lessons
- Practice Drills and Adaptive Assessments
- Platform Feature Modules (Progress, BKT Mastery, Misconceptions, Analytics)
- Multi-Subject Discipline Tracks and Courses
"""

import streamlit as st
from typing import Dict, Any, List
from core.search_service import SearchService
from core.course_manager import set_active_course_by_id, get_active_course


def clear_search():
    """Resets global search query and bumps widget key version to prevent widget re-binding errors."""
    st.session_state["global_search_query"] = ""
    st.session_state["search_input_version"] = st.session_state.get("search_input_version", 0) + 1


def render_search_input():
    """
    Renders the live interactive search bar in the top navigation bar.
    Uses versioned widget keys so setting search terms programmatically never mutates active widget state.
    """
    if "search_input_version" not in st.session_state:
        st.session_state["search_input_version"] = 0
    if "global_search_query" not in st.session_state:
        st.session_state["global_search_query"] = ""

    curr_version = st.session_state["search_input_version"]
    current_val = st.session_state["global_search_query"]

    col_input, col_action = st.columns([0.88, 0.12])

    with col_input:
        new_val = st.text_input(
            "Search for concepts, progress, assignments...",
            value=current_val,
            placeholder="Search for concepts, progress, assignments...",
            key=f"search_box_input_{curr_version}",
            label_visibility="collapsed"
        )
        # If user pressed Enter with a new query
        if new_val != current_val:
            st.session_state["global_search_query"] = new_val
            st.rerun()

    with col_action:
        if current_val:
            if st.button("✕", key="top_search_clear_btn", help="Clear search query", use_container_width=True):
                clear_search()
                st.rerun()
        else:
            with st.popover("⚡", use_container_width=True, help="Explore popular search terms"):
                st.markdown("""
                <div style="font-weight: 700; font-size: 0.825rem; color: #172943; margin-bottom: 0.35rem;">
                    Suggested Searches
                </div>
                """, unsafe_allow_html=True)
                suggestions = [
                    ("Loops & Control Flow", "loops"),
                    ("Variables & Data Types", "variables"),
                    ("Pointers & Memory (C)", "pointers"),
                    ("Limits & Continuity (Math)", "limits"),
                    ("Adaptive Assessments", "assessment"),
                    ("Student Progress & BKT", "progress"),
                    ("AI Misconceptions", "misconceptions"),
                ]
                for label, term in suggestions:
                    if st.button(label, key=f"sug_btn_{term}", use_container_width=True):
                        st.session_state["global_search_query"] = term
                        st.session_state["search_input_version"] = curr_version + 1
                        st.rerun()


def render_search_results_view(query: str):
    """
    Renders the complete, structured Search Results view when a search query is active.
    Allows students and faculty to immediately jump to the matching lesson, assessment, or module.
    """
    curr_version = st.session_state.get("search_input_version", 0)
    results = SearchService.search(query)
    total = results["total_count"]

    # Header Card with Query info and Close button
    st.markdown(f"""
    <div class="lm-card" style="margin-bottom: 1.25rem; border-left: 4px solid #D6B56D; padding: 1.15rem 1.35rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="lm-pill pill-ahead" style="font-size: 0.725rem; padding: 2px 8px; font-weight: 700;">Global Search</span>
                    <span style="font-size: 0.8rem; color: #718096;">{total} match{'es' if total != 1 else ''} found</span>
                </div>
                <h2 style="font-size: 1.35rem; font-weight: 800; color: #172943; margin: 0.35rem 0 0 0; letter-spacing: -0.02em;">
                    Results for "<span style="color: #D6B56D;">{query}</span>"
                </h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn_back, _ = st.columns([0.3, 0.7])
    with col_btn_back:
        if st.button("← Return to Previous View", key="search_return_btn", type="secondary", use_container_width=True):
            clear_search()
            st.rerun()

    if total == 0:
        # Zero Results State with helpful Suggestions
        st.markdown(f"""
        <div class="lm-card" style="text-align: center; padding: 3rem 1.5rem; margin-top: 1rem;">
            <div style="width: 52px; height: 52px; border-radius: 50%; background-color: #FAF5EA; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 1rem; border: 1px solid #E8C879;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D6B56D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            </div>
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #172943; margin-bottom: 0.35rem;">No direct matches found</h3>
            <p style="font-size: 0.85rem; color: #718096; max-width: 480px; margin: 0 auto 1.5rem auto;">
                We couldn't find any concepts, lessons, or assignments matching "<strong>{query}</strong>". Try searching for core programming, mathematics, or platform keywords:
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #172943; margin: 1rem 0 0.5rem 0;'>Recommended Searches:</div>", unsafe_allow_html=True)
        col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
        with col_s1:
            if st.button("Loops & Iteration", key="empty_sug_loops", use_container_width=True):
                st.session_state["global_search_query"] = "loops"
                st.session_state["search_input_version"] = curr_version + 1
                st.rerun()
        with col_s2:
            if st.button("Pointers (C)", key="empty_sug_pointers", use_container_width=True):
                st.session_state["global_search_query"] = "pointers"
                st.session_state["search_input_version"] = curr_version + 1
                st.rerun()
        with col_s3:
            if st.button("Limits & Continuity", key="empty_sug_limits", use_container_width=True):
                st.session_state["global_search_query"] = "limits"
                st.session_state["search_input_version"] = curr_version + 1
                st.rerun()
        with col_s4:
            if st.button("Adaptive Assessments", key="empty_sug_assess", use_container_width=True):
                st.session_state["global_search_query"] = "assessment"
                st.session_state["search_input_version"] = curr_version + 1
                st.rerun()
        with col_s5:
            if st.button("BKT Mastery Progress", key="empty_sug_prog", use_container_width=True):
                st.session_state["global_search_query"] = "progress"
                st.session_state["search_input_version"] = curr_version + 1
                st.rerun()
        return

    # 1. Platform Modules & Telemetry (e.g. Progress, Assessments, AI Misconceptions)
    if results["modules"]:
        st.markdown(f"""
        <div style="font-weight: 700; font-size: 0.95rem; color: #172943; margin: 1.25rem 0 0.65rem 0; display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D6B56D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
            Platform Modules & Features ({len(results['modules'])})
        </div>
        """, unsafe_allow_html=True)

        for mod in results["modules"]:
            c_info, c_action = st.columns([0.8, 0.2])
            with c_info:
                st.markdown(f"""
                <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.25rem;">
                        <span class="lm-pill pill-completed" style="font-size: 0.65rem;">{mod['badge']}</span>
                        <span style="font-weight: 700; font-size: 0.9rem; color: #172943;">{mod['title']}</span>
                    </div>
                    <div style="font-size: 0.775rem; color: #718096;">{mod['subtitle']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c_action:
                st.write("")
                if st.button(mod["action_label"], key=f"btn_mod_{mod['id']}", use_container_width=True, type="primary"):
                    st.session_state["current_page"] = mod["target_page"]
                    clear_search()
                    st.rerun()

    # 2. Concepts & Knowledge Components
    if results["concepts"]:
        st.markdown(f"""
        <div style="font-weight: 700; font-size: 0.95rem; color: #172943; margin: 1.25rem 0 0.65rem 0; display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3976B9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            Concepts & Knowledge Components ({len(results['concepts'])})
        </div>
        """, unsafe_allow_html=True)

        for concept in results["concepts"]:
            c_info, c_action1, c_action2 = st.columns([0.64, 0.18, 0.18])
            with c_info:
                st.markdown(f"""
                <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.25rem;">
                        <span class="lm-pill pill-ahead" style="font-size: 0.65rem;">{concept['subject_name']}: {concept['course_name']}</span>
                        <span style="font-weight: 700; font-size: 0.9rem; color: #172943;">{concept['title']}</span>
                        <code style="font-size: 0.675rem; color: #718096;">{concept['code']}</code>
                    </div>
                    <div style="font-size: 0.775rem; color: #718096;">{concept['subtitle']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c_action1:
                st.write("")
                if st.button("Read Lesson", key=f"btn_c_read_{concept['id']}", use_container_width=True, type="secondary"):
                    if concept["course_id"]:
                        set_active_course_by_id(concept["course_id"])
                    st.session_state["active_concept_id"] = concept["id"]
                    st.session_state["current_page"] = "learning_library"
                    clear_search()
                    st.rerun()
            with c_action2:
                st.write("")
                if st.button("Practice Drill", key=f"btn_c_drill_{concept['id']}", use_container_width=True, type="primary"):
                    if concept["course_id"]:
                        set_active_course_by_id(concept["course_id"])
                    st.session_state["assessment_concept_id"] = concept["id"]
                    st.session_state["current_page"] = "assessment"
                    clear_search()
                    st.rerun()

    # 3. Learning Content / Lessons
    if results["lessons"]:
        st.markdown(f"""
        <div style="font-weight: 700; font-size: 0.95rem; color: #172943; margin: 1.25rem 0 0.65rem 0; display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#36A879" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            Curriculum Lessons & Sandboxes ({len(results['lessons'])})
        </div>
        """, unsafe_allow_html=True)

        for lesson in results["lessons"]:
            c_info, c_action = st.columns([0.8, 0.2])
            with c_info:
                st.markdown(f"""
                <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.25rem;">
                        <span class="lm-pill pill-ontrack" style="font-size: 0.65rem;">{lesson['badge']}</span>
                        <span style="font-size: 0.725rem; color: #718096; font-weight: 600;">{lesson['course_name']} &bull; {lesson['concept_name']}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 0.9rem; color: #172943; margin-bottom: 0.2rem;">{lesson['title']}</div>
                    <div style="font-size: 0.775rem; color: #718096;">{lesson['subtitle']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c_action:
                st.write("")
                if st.button("Open in Library", key=f"btn_l_open_{lesson['id']}", use_container_width=True, type="primary"):
                    if lesson["course_id"]:
                        set_active_course_by_id(lesson["course_id"])
                    st.session_state["active_concept_id"] = lesson["concept_id"]
                    st.session_state["current_page"] = "learning_library"
                    clear_search()
                    st.rerun()

    # 4. Adaptive Assessment Practice Drills
    if results["assessments"]:
        st.markdown(f"""
        <div style="font-weight: 700; font-size: 0.95rem; color: #172943; margin: 1.25rem 0 0.65rem 0; display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E9AA45" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/></svg>
            Diagnostic Questions & Assessment Drills ({len(results['assessments'])})
        </div>
        """, unsafe_allow_html=True)

        for q in results["assessments"]:
            c_info, c_action = st.columns([0.8, 0.2])
            with c_info:
                st.markdown(f"""
                <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.25rem;">
                        <span class="lm-pill pill-lagging" style="font-size: 0.65rem;">{q['badge']}</span>
                        <span style="font-weight: 700; font-size: 0.9rem; color: #172943;">{q['title']}</span>
                        <span style="font-size: 0.725rem; color: #718096;">({q['concept_name']})</span>
                    </div>
                    <div style="font-size: 0.775rem; color: #718096;">{q['subtitle']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c_action:
                st.write("")
                if st.button("Practice Drill", key=f"btn_q_drill_{q['id']}", use_container_width=True, type="primary"):
                    if q["course_id"]:
                        set_active_course_by_id(q["course_id"])
                    st.session_state["assessment_concept_id"] = q["concept_id"]
                    st.session_state["current_page"] = "assessment"
                    clear_search()
                    st.rerun()

    # 5. Courses & Discipline Tracks
    if results["courses"]:
        st.markdown(f"""
        <div style="font-weight: 700; font-size: 0.95rem; color: #172943; margin: 1.25rem 0 0.65rem 0; display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#243B64" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
            Subject Tracks & Courses ({len(results['courses'])})
        </div>
        """, unsafe_allow_html=True)

        for course in results["courses"]:
            c_info, c_action = st.columns([0.8, 0.2])
            with c_info:
                st.markdown(f"""
                <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.25rem;">
                        <span class="lm-pill pill-ahead" style="font-size: 0.65rem;">{course['badge']}</span>
                        <span style="font-weight: 700; font-size: 0.9rem; color: #172943;">{course['title']}</span>
                        <span style="font-size: 0.725rem; color: #718096;">Level: {course['difficulty_level']}</span>
                    </div>
                    <div style="font-size: 0.775rem; color: #718096;">{course['subtitle']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c_action:
                st.write("")
                if st.button("Switch Track", key=f"btn_crs_switch_{course['id']}", use_container_width=True, type="primary"):
                    set_active_course_by_id(course["id"])
                    st.session_state["current_page"] = "student_dashboard"
                    clear_search()
                    st.rerun()
