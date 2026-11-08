"""
LearnSphere AI: Comprehensive Learning Content Library
Displays in-depth modules covering Python concepts, memory models,
code examples, common cognitive mistakes, and practice exercises.
"""

import streamlit as st
from database.db import (
    get_all_learning_content, get_user_lesson_progress, toggle_lesson_progress
)


def render_library_page(user: dict):
    user_id = user["id"]
    lessons = get_all_learning_content()
    progress_map = get_user_lesson_progress(user_id)

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0;">
            Python Learning Content Library
        </h2>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.25rem;">
            Rigorous conceptual curriculum designed to prevent subtle cognitive bugs and establish robust mental models.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Lesson Selector Tabs / Dropdown
    lesson_titles = [f"{l['order_index']}. {l['concept_name']}" for l in lessons]
    lesson_codes = [l["concept_code"] for l in lessons]

    # Pre-select lesson if passed via session state
    preselected_code = st.session_state.pop("selected_lesson_code", None)
    default_idx = 0
    if preselected_code and preselected_code in lesson_codes:
        default_idx = lesson_codes.index(preselected_code)

    selected_title = st.selectbox("Select Learning Module", lesson_titles, index=default_idx)
    selected_idx = lesson_titles.index(selected_title)
    lesson = lessons[selected_idx]

    content_id = lesson["id"]
    is_completed = progress_map.get(content_id, False)

    # 2. Lesson Header Card
    completed_badge = '<span class="ls-badge badge-mastered">Completed</span>' if is_completed else '<span class="ls-badge badge-developing">In Progress</span>'
    st.markdown(f"""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-demo">Module {lesson['order_index']}</span>
                <span style="font-size: 0.85rem; color: #64748b; margin-left: 0.5rem;">{lesson['reading_time_min']} min estimated reading</span>
            </div>
            {completed_badge}
        </div>
        <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">
            {lesson['title']}
        </h2>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">
            {lesson['summary']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Learning Objectives
    st.markdown("""
    <div class="ls-card">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.75rem;">
            Learning Objectives
        </h4>
        <ul style="color: #334155; font-size: 0.9rem; line-height: 1.7; padding-left: 1.25rem; margin: 0;">
    """, unsafe_allow_html=True)
    for obj in lesson["learning_objectives"]:
        st.markdown(f"<li>{obj}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)

    # 4. Introduction and Detailed Conceptual Explanation
    st.markdown(f"""
    <div class="ls-card">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.75rem;">
            Conceptual Framework
        </h4>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">
            {lesson['introduction']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(lesson["detailed_explanation"])

    # 5. Interactive Python Code Examples
    st.markdown("""
    <div class="ls-card" style="margin-top: 1.5rem;">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.75rem;">
            Annotated Code Demonstrations
        </h4>
    </div>
    """, unsafe_allow_html=True)

    for ex in lesson["code_examples"]:
        with st.expander(f"Code Demonstration: {ex['title']}", expanded=True):
            st.code(ex["code"], language="python")
            col_out, col_notes = st.columns([1, 1])
            with col_out:
                st.caption("Standard Output:")
                st.code(ex["output"], language="text")
            with col_notes:
                st.caption("Pedagogical Notes:")
                st.info(ex["notes"])

    # 6. Common Mistakes and Misconceptions Analysis
    st.markdown("""
    <div class="ls-card" style="margin-top: 1.5rem;">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.75rem;">
            Common Cognitive Pitfalls in This Topic
        </h4>
        <div class="ls-card-desc">Recognizing these anti-patterns directly prevents assessment errors.</div>
    </div>
    """, unsafe_allow_html=True)

    for cm in lesson["common_mistakes"]:
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #991b1b; font-size: 0.95rem; margin-bottom: 0.5rem;">
                Mistake Pattern: {cm['title']}
            </div>
            <p style="color: #475569; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.75rem;">
                {cm['explanation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_w, col_c = st.columns(2)
        with col_w:
            st.caption("Flawed Implementation:")
            st.code(cm["wrong_code"], language="python")
        with col_c:
            st.caption("Correct Idiomatic Solution:")
            st.code(cm["correct_code"], language="python")

    # 7. Practice Exercises
    st.markdown("""
    <div class="ls-card" style="margin-top: 1.5rem;">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.75rem;">
            Practice Exercises
        </h4>
    </div>
    """, unsafe_allow_html=True)

    for p_idx, pe in enumerate(lesson["practice_exercises"]):
        st.markdown(f"**Exercise {p_idx + 1}:** {pe['prompt']}")
        with st.expander("View Hint and Solution"):
            st.write(f"**Hint:** {pe['hint']}")
            st.code(pe["solution"], language="python")

    # 8. Interactive Python Code Sandbox
    st.markdown("""
    <div class="ls-card" style="margin-top: 1.5rem;">
        <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.35rem;">
            Interactive Python Code Sandbox
        </h4>
        <div class="ls-card-desc">Experiment with the concepts taught in this module. Edit and execute Python code in real-time.</div>
    """, unsafe_allow_html=True)

    default_sandbox_code = lesson["code_examples"][0]["code"] if lesson.get("code_examples") else "print('Hello LearnSphere AI')"
    user_code = st.text_area("Python Editor", value=default_sandbox_code, height=130, key=f"sandbox_{lesson['concept_code']}")

    if st.button("Execute Python Code", key=f"run_sb_{lesson['concept_code']}", type="primary"):
        import io
        import contextlib

        stdout_buf = io.StringIO()
        err_msg = None
        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec_globals = {"__builtins__": __builtins__}
                exec(user_code, exec_globals)
        except Exception as exc:
            err_msg = f"{type(exc).__name__}: {str(exc)}"

        output_str = stdout_buf.getvalue()
        if output_str:
            st.caption("Execution Output (stdout):")
            st.code(output_str, language="text")
        if err_msg:
            st.error(f"Runtime Exception: {err_msg}")
        if not output_str and not err_msg:
            st.info("Code executed successfully with no stdout output.")

    st.markdown("</div>", unsafe_allow_html=True)

    # 8. Action Controls: Completion Toggle and Assessment Jump
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    col_comp, col_test = st.columns([1, 1])

    with col_comp:
        new_status = not is_completed
        toggle_label = "Mark as Complete" if not is_completed else "Mark as Incomplete"
        btn_type = "primary" if not is_completed else "secondary"
        if st.button(toggle_label, type=btn_type, use_container_width=True):
            toggle_lesson_progress(user_id, content_id, new_status)
            st.rerun()

    with col_test:
        if st.button("Take Assessment on this Topic", use_container_width=True):
            st.session_state["current_page"] = "assessment"
            st.session_state["assessment_concept_id"] = lesson["concept_id"]
            st.rerun()

