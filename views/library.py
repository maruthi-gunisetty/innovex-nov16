"""
LearnSphere AI: Structured Course and Learning Content Library
Features:
- Compact course cards in a clean grid matching the reference dashboard style
- Course title, description, difficulty, lesson count, exercises, completion %
- Search filter, category filters, and sorting
- In-depth module viewer with Python code demonstrations, mistake analysis, and live sandbox
"""

import streamlit as st
import io
import contextlib
from database.db import (
    get_all_learning_content, get_user_lesson_progress, toggle_lesson_progress
)


def render_library_page(user: dict):
    user_id = user["id"]
    lessons = get_all_learning_content()
    progress_map = get_user_lesson_progress(user_id)

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #243B64; margin: 0; letter-spacing: -0.02em;">Learning Content Library</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Structured Python programming modules designed to prevent cognitive bugs and build robust mental models.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Search, Category Filter, and Sorting Controls
    col_search, col_cat, col_sort = st.columns([1.5, 1, 1])
    with col_search:
        search_query = st.text_input("Search Modules", placeholder="Search title or concept...", label_visibility="collapsed", key="lib_search")
    with col_cat:
        category_filter = st.selectbox(
            "Filter Category",
            ["All Concepts", "Foundational Syntax", "Control Flow", "Data Structures", "Functions & Recursion"],
            index=0,
            label_visibility="collapsed"
        )
    with col_sort:
        sort_order = st.selectbox(
            "Sort By",
            ["Curriculum Sequence", "Reading Duration", "Completion Status"],
            index=0,
            label_visibility="collapsed"
        )

    # Filter lessons based on search query
    filtered_lessons = lessons
    if search_query:
        filtered_lessons = [l for l in filtered_lessons if search_query.lower() in l["title"].lower() or search_query.lower() in l["concept_name"].lower()]

    if sort_order == "Reading Duration":
        filtered_lessons = sorted(filtered_lessons, key=lambda x: x["reading_time_min"])
    elif sort_order == "Completion Status":
        filtered_lessons = sorted(filtered_lessons, key=lambda x: progress_map.get(x["id"], False), reverse=True)

    # Check if a lesson is currently active in session state
    active_code = st.session_state.get("selected_lesson_code", filtered_lessons[0]["concept_code"] if filtered_lessons else None)

    # 2. Compact Course Cards Grid
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #243B64; margin: 0.75rem 0 0.5rem 0;'>Available Curriculum Courses</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    for idx, l in enumerate(filtered_lessons):
        cid = l["id"]
        is_done = progress_map.get(cid, False)
        comp_pct = 100 if is_done else 45
        diff_label = "Beginner" if l["order_index"] <= 2 else ("Intermediate" if l["order_index"] <= 4 else "Advanced")
        pill_cls = "pill-completed" if is_done else "pill-ontrack"
        pill_text = "Completed" if is_done else "In Progress"

        with cols[idx % 3]:
            st.markdown(f"""
            <div class="lm-card" style="padding: 0.9rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.675rem; font-weight: 700; color: #3976B9; background: #EAF2FA; padding: 2px 6px; border-radius: 4px;">MODULE {l['order_index']}</span>
                    <span class="lm-pill {pill_cls}">{pill_text}</span>
                </div>
                <div style="font-weight: 700; font-size: 0.875rem; color: #243B64; line-height: 1.3; margin-bottom: 0.25rem;">
                    {l['title']}
                </div>
                <div style="font-size: 0.725rem; color: #718096; line-height: 1.4; height: 38px; overflow: hidden; margin-bottom: 0.5rem;">
                    {l['summary'][:95]}...
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.675rem; color: #718096; margin-bottom: 0.25rem;">
                    <span>Difficulty: <strong>{diff_label}</strong></span>
                    <span>{l['reading_time_min']} min &bull; 4 Exercises</span>
                </div>
                <div class="lm-progress-wrap" style="height: 5px; margin: 0.25rem 0 0.5rem 0;">
                    <div class="lm-progress-bar" style="width: {comp_pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Continue Learning", key=f"btn_lib_sel_{l['concept_code']}", use_container_width=True, type="primary" if l["concept_code"] == active_code else "secondary"):
                st.session_state["selected_lesson_code"] = l["concept_code"]
                st.rerun()

    # 3. Active Detailed Lesson Viewer
    active_lesson = next((l for l in lessons if l["concept_code"] == active_code), filtered_lessons[0] if filtered_lessons else None)
    if not active_lesson:
        return

    content_id = active_lesson["id"]
    is_completed = progress_map.get(content_id, False)

    st.markdown("<hr style='border-color: #E4E8ED; margin: 1.25rem 0 1rem 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="lm-card" style="border-left: 4px solid #3976B9;">
        <div class="lm-card-header">
            <div>
                <span class="lm-pill pill-ahead">Active Course Unit: Module {active_lesson['order_index']}</span>
                <h3 class="lm-card-title" style="font-size: 1.15rem; margin-top: 0.25rem;">{active_lesson['title']}</h3>
                <div style="font-size: 0.775rem; color: #718096;">Concept: {active_lesson['concept_name']} &bull; {active_lesson['reading_time_min']} min estimated study time</div>
            </div>
            <span class="lm-pill {'pill-completed' if is_completed else 'pill-ontrack'}">{'Completed' if is_completed else 'In Progress'}</span>
        </div>
        <p style="color: #263445; font-size: 0.85rem; line-height: 1.55; margin-bottom: 0.5rem;">
            {active_lesson['introduction']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Learning Objectives
    st.markdown("""
    <div class="lm-card">
        <div style="font-weight: 700; font-size: 0.85rem; color: #243B64; margin-bottom: 0.4rem;">Learning Objectives</div>
        <ul style="color: #263445; font-size: 0.8rem; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
    """, unsafe_allow_html=True)
    for obj in active_lesson["learning_objectives"]:
        st.markdown(f"<li>{obj}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)

    # Detailed Conceptual Framework
    st.markdown(active_lesson["detailed_explanation"])

    # Code Demonstrations
    st.markdown("<div style='font-size: 0.875rem; font-weight: 700; color: #243B64; margin: 1rem 0 0.5rem 0;'>Annotated Code Demonstrations</div>", unsafe_allow_html=True)
    for ex in active_lesson["code_examples"]:
        with st.expander(f"Code Demonstration: {ex['title']}", expanded=True):
            st.code(ex["code"], language="python")
            c_out, c_note = st.columns(2)
            with c_out:
                st.caption("Standard Output:")
                st.code(ex["output"], language="text")
            with c_note:
                st.caption("Pedagogical Notes:")
                st.info(ex["notes"])

    # Common Cognitive Pitfalls
    st.markdown("<div style='font-size: 0.875rem; font-weight: 700; color: #243B64; margin: 1rem 0 0.5rem 0;'>Common Cognitive Pitfalls</div>", unsafe_allow_html=True)
    for cm in active_lesson["common_mistakes"]:
        st.markdown(f"""
        <div class="lm-card" style="border-left: 3px solid #D96B6B; padding: 0.85rem; margin-bottom: 0.65rem;">
            <div style="font-weight: 700; color: #D96B6B; font-size: 0.825rem; margin-bottom: 0.2rem;">Anti-Pattern: {cm['title']}</div>
            <div style="color: #718096; font-size: 0.775rem; line-height: 1.45; margin-bottom: 0.4rem;">{cm['explanation']}</div>
        </div>
        """, unsafe_allow_html=True)
        cw, cc = st.columns(2)
        with cw:
            st.caption("Flawed Implementation:")
            st.code(cm["wrong_code"], language="python")
        with cc:
            st.caption("Idiomatic Solution:")
            st.code(cm["correct_code"], language="python")

    # In-Browser Live Code Sandbox
    st.markdown("""
    <div class="lm-card" style="margin-top: 1rem;">
        <div class="lm-card-header">
            <span class="lm-card-title">Interactive Python Code Sandbox</span>
            <span style="font-size: 0.725rem; color: #718096;">Edit and execute code in real time</span>
        </div>
    """, unsafe_allow_html=True)
    default_code = active_lesson["code_examples"][0]["code"] if active_lesson.get("code_examples") else "print('LearnSphere AI Sandbox')"
    sandbox_input = st.text_area("Python Editor", value=default_code, height=120, key=f"sb_editor_{active_lesson['concept_code']}")

    if st.button("Execute Python Code", key=f"run_sb_{active_lesson['concept_code']}", type="primary"):
        stdout_buf = io.StringIO()
        err_msg = None
        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec_globals = {"__builtins__": __builtins__}
                exec(sandbox_input, exec_globals)
        except Exception as exc:
            err_msg = f"{type(exc).__name__}: {str(exc)}"

        out_str = stdout_buf.getvalue()
        if out_str:
            st.caption("Execution Output:")
            st.code(out_str, language="text")
        if err_msg:
            st.error(f"Runtime Exception: {err_msg}")
        if not out_str and not err_msg:
            st.info("Code executed successfully with no stdout output.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Action Buttons: Toggle Complete and Jump to Assessment
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        toggle_label = "Mark Module as Completed" if not is_completed else "Mark as In Progress"
        if st.button(toggle_label, use_container_width=True, type="primary" if not is_completed else "secondary"):
            toggle_lesson_progress(user_id, content_id, not is_completed)
            st.rerun()
    with col_t2:
        if st.button("Take Assessment on this Concept", use_container_width=True):
            st.session_state["current_page"] = "assessment"
            st.session_state["assessment_concept_id"] = active_lesson["concept_id"]
            st.rerun()
