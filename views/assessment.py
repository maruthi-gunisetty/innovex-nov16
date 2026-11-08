"""
LearnSphere AI: Enterprise Adaptive Assessment Module
Professional educational testing interface matching the reference dashboard design:
- Assessment title, topic, difficulty badge, and progress bar
- Question navigation panel allowing direct jumping between items
- Compact 4-option radio selector and code viewer
- Real-time BKT updates and labeled-distractor misconception feedback
"""

import streamlit as st
import time
from database.db import (
    get_all_concepts, get_questions_by_concept_and_difficulty,
    get_student_concept_mastery, update_student_mastery_record,
    record_assessment_attempt
)
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine
from core.recommender import RecommenderEngine
from core.course_manager import get_active_course, render_course_selector


def render_assessment_page(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    concepts = get_all_concepts(course_id=active_course["id"])

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">SARVAVIDYA Adaptive Assessment</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Latent concept mastery evaluation with distractor-based cognitive misconception detection.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Subject and Filter Controls
    col_t, col_c, col_d = st.columns([1.2, 1.4, 1.0])
    with col_t:
        render_course_selector(key="assess_track_selector", label="Select Track", on_change_rerun=True)

    concept_options = {"All Concepts in Track": None}
    for c in concepts:
        concept_options[f"{c['code']} - {c['name']}"] = c["id"]

    preselected_id = st.session_state.pop("assessment_concept_id", None)
    default_c_idx = 0
    if preselected_id:
        for idx, (label, cid) in enumerate(concept_options.items()):
            if cid == preselected_id:
                default_c_idx = idx
                break

    with col_c:
        selected_label = st.selectbox("Curriculum Concept Target", list(concept_options.keys()), index=default_c_idx, label_visibility="collapsed")
        selected_concept_id = concept_options[selected_label]

    with col_d:
        difficulty_mode = st.selectbox(
            "Difficulty Selection",
            ["Adaptive (AI Selected)", "Beginner", "Intermediate", "Advanced"],
            index=0,
            label_visibility="collapsed"
        )

    # 2. Determine questions pool based on difficulty mode
    if difficulty_mode == "Adaptive (AI Selected)":
        if selected_concept_id:
            m_rec = get_student_concept_mastery(user_id, selected_concept_id)
            current_mastery = m_rec["mastery_prob"] if m_rec else 0.20
        else:
            current_mastery = 0.50
        actual_diff = RecommenderEngine.get_adaptive_difficulty(current_mastery)
    else:
        actual_diff = difficulty_mode.lower()

    questions = get_questions_by_concept_and_difficulty(selected_concept_id, actual_diff, course_id=active_course["id"])
    if not questions:
        questions = get_questions_by_concept_and_difficulty(selected_concept_id, "all", course_id=active_course["id"])

    if not questions:
        st.warning("No questions found matching the selected filters. Please adjust your criteria.")
        return

    # Pagination state
    if "q_index" not in st.session_state:
        st.session_state["q_index"] = 0
    if st.session_state["q_index"] >= len(questions):
        st.session_state["q_index"] = 0

    q_idx = st.session_state["q_index"]
    current_q = questions[q_idx]

    q_key = f"q_start_time_{current_q['id']}"
    if q_key not in st.session_state:
        st.session_state[q_key] = time.time()

    # 3. Two-Column Layout: Question Interface (Left) + Question Navigation & Stats (Right)
    col_q_main, col_q_nav = st.columns([2.5, 1])

    with col_q_main:
        # Progress Bar and Header
        prog_pct = int(((q_idx + 1) / len(questions)) * 100)
        diff_pill = "pill-completed" if current_q["difficulty"] == "beginner" else ("pill-ahead" if current_q["difficulty"] == "intermediate" else "pill-ontrack")

        st.markdown(f"""
        <div class="lm-card" style="padding: 1rem 1.25rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 700; font-size: 0.75rem; color: #3976B9; background: #EAF2FA; padding: 2px 8px; border-radius: 4px;">QUESTION {q_idx + 1} OF {len(questions)}</span>
                    <span class="lm-pill {diff_pill}">{current_q['difficulty'].capitalize()}</span>
                    <span style="font-size: 0.75rem; color: #718096;">Topic: {current_q['concept_name']}</span>
                </div>
                <div style="font-size: 0.725rem; color: #718096;">Item #{current_q['id']}</div>
            </div>
            <div class="lm-progress-wrap" style="height: 4px; margin-bottom: 0.75rem;">
                <div class="lm-progress-bar" style="width: {prog_pct}%;"></div>
            </div>
            <h3 style="font-size: 1.05rem; font-weight: 700; color: #243B64; margin-bottom: 0.4rem;">
                {current_q['title']}
            </h3>
            <p style="color: #263445; font-size: 0.875rem; line-height: 1.55; margin-bottom: 0.75rem;">
                {current_q['prompt']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if current_q.get("code_snippet"):
            c_code_tag = str(current_q.get("concept_code", "")).upper()
            code_lang = "c" if c_code_tag.startswith("C_") else ("python" if c_code_tag.startswith("PY_") else "text")
            st.code(current_q["code_snippet"], language=code_lang)

        # Answer Options Form
        options = current_q["options"]
        opt_labels = [opt["text"] for opt in options]

        form_key = f"q_form_{current_q['id']}_{q_idx}"
        with st.form(form_key):
            selected_text = st.radio(
                "Select your response:",
                opt_labels,
                index=None,
                key=f"radio_{current_q['id']}",
                label_visibility="collapsed"
            )

            col_sub, col_prev, col_next = st.columns([1.5, 1, 1])
            with col_sub:
                submit_answer = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)
            with col_prev:
                prev_btn = st.form_submit_button("Previous", use_container_width=True)
            with col_next:
                next_btn = st.form_submit_button("Next", use_container_width=True)

            if prev_btn:
                st.session_state["q_index"] = max(0, q_idx - 1)
                st.rerun()
            if next_btn:
                st.session_state["q_index"] = min(len(questions) - 1, q_idx + 1)
                st.rerun()

    with col_q_nav:
        # Question Navigation Panel
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem; margin-bottom: 0.75rem;">
            <div style="font-weight: 700; font-size: 0.8rem; color: #243B64; margin-bottom: 0.5rem;">Question Navigation</div>
        """, unsafe_allow_html=True)

        # Mini grid of question buttons
        q_cols = st.columns(4)
        for i in range(len(questions)):
            with q_cols[i % 4]:
                btn_type = "primary" if i == q_idx else "secondary"
                if st.button(f"{i+1}", key=f"q_nav_btn_{i}", use_container_width=True, type=btn_type):
                    st.session_state["q_index"] = i
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Assessment Live Statistics
        m_curr = get_student_concept_mastery(user_id, current_q["concept_id"])
        c_prob = m_curr["mastery_prob"] if m_curr else 0.20
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem;">
            <div style="font-weight: 700; font-size: 0.8rem; color: #243B64; margin-bottom: 0.35rem;">Telemetry Metrics</div>
            <div style="font-size: 0.725rem; color: #718096; margin-bottom: 0.25rem;">
                Target: <strong>{current_q['concept_name']}</strong>
            </div>
            <div style="font-size: 0.725rem; color: #718096; margin-bottom: 0.25rem;">
                Current Mastery: <strong style="color: #243B64;">{c_prob:.0%}</strong>
            </div>
            <div style="font-size: 0.725rem; color: #718096;">
                Engine Mode: <strong>{difficulty_mode}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Handle Submission and Cognitive Feedback
    eval_key = f"eval_{current_q['id']}"
    if submit_answer:
        if selected_text is None:
            st.error("Please select an answer option before submitting.")
        else:
            elapsed_time = round(time.time() - st.session_state.get(q_key, time.time()), 2)
            chosen_opt = next(opt for opt in options if opt["text"] == selected_text)
            is_correct = bool(chosen_opt.get("is_correct", False))
            misconception_code = chosen_opt.get("misconception_code")

            concept_id = current_q["concept_id"]
            m_rec = get_student_concept_mastery(user_id, concept_id)
            prior_mastery = m_rec["mastery_prob"] if m_rec else 0.20

            bkt = BayesianKnowledgeTracing(
                p_init=m_rec.get("p_init", 0.20) if m_rec else 0.20,
                p_transit=m_rec.get("p_transit", 0.15) if m_rec else 0.15,
                p_guess=m_rec.get("p_guess", 0.20) if m_rec else 0.20,
                p_slip=m_rec.get("p_slip", 0.10) if m_rec else 0.10
            )
            posterior_obs, next_prior = bkt.update(prior_mastery, is_correct)
            update_student_mastery_record(user_id, concept_id, next_prior, is_correct)

            record_assessment_attempt(
                user_id=user_id,
                question_id=current_q["id"],
                concept_id=concept_id,
                selected_option_index=chosen_opt["index"],
                is_correct=is_correct,
                difficulty=current_q["difficulty"],
                response_time_sec=elapsed_time,
                misconception_code=misconception_code,
                prior_mastery=prior_mastery,
                posterior_mastery=next_prior
            )

            st.session_state[eval_key] = {
                "is_correct": is_correct,
                "chosen_opt": chosen_opt,
                "prior_mastery": prior_mastery,
                "posterior_mastery": next_prior,
                "elapsed_time": elapsed_time,
                "explanation": current_q["explanation"]
            }

    # 5. Display Evaluation Results
    if eval_key in st.session_state:
        res = st.session_state[eval_key]
        if res["is_correct"]:
            st.markdown(f"""
            <div class="lm-card" style="border-left: 4px solid #36A879; background-color: #EDF8F3; padding: 0.9rem 1.1rem; margin-top: 0.75rem;">
                <div style="font-weight: 700; color: #166534; font-size: 0.95rem; margin-bottom: 0.25rem;">
                    Correct Answer Verified
                </div>
                <div style="color: #14532D; font-size: 0.825rem; line-height: 1.5; margin-bottom: 0.4rem;">
                    {res['chosen_opt']['explanation']}
                </div>
                <div style="font-size: 0.75rem; color: #166534;">
                    Latency: {res['elapsed_time']}s &bull; BKT Mastery increased from <strong>{res['prior_mastery']:.0%}</strong> to <strong>{res['posterior_mastery']:.0%}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            m_code = res["chosen_opt"].get("misconception_code")
            m_info = MisconceptionEngine.get_info(m_code)
            m_name = m_info["name"] if m_info else "Incorrect Mental Model"
            m_rem = m_info["remediation"] if m_info else "Review core curriculum principles."

            st.markdown(f"""
            <div class="lm-card" style="border-left: 4px solid #D96B6B; background-color: #FDF2F2; padding: 0.9rem 1.1rem; margin-top: 0.75rem;">
                <div style="font-weight: 700; color: #991B1B; font-size: 0.95rem; margin-bottom: 0.25rem;">
                    Misconception Identified: {m_name}
                </div>
                <div style="color: #881337; font-size: 0.825rem; line-height: 1.5; margin-bottom: 0.4rem;">
                    <strong>Why this error occurs:</strong> {res['chosen_opt']['explanation']}
                </div>
                <div style="background-color: #FFFFFF; padding: 0.5rem 0.75rem; border-radius: 6px; border: 1px solid #FECDD3; color: #991B1B; font-size: 0.775rem; margin-bottom: 0.4rem;">
                    <strong>Pedagogical Remediation:</strong> {m_rem}
                </div>
                <div style="font-size: 0.75rem; color: #991B1B;">
                    BKT Mastery adjusted from <strong>{res['prior_mastery']:.0%}</strong> to <strong>{res['posterior_mastery']:.0%}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)

        col_next_q, col_review = st.columns(2)
        with col_next_q:
            if st.button("Proceed to Next Question", key="btn_next_q_after_eval", type="primary", use_container_width=True):
                st.session_state.pop(eval_key, None)
                st.session_state[f"q_start_time_{current_q['id']}"] = time.time()
                st.session_state["q_index"] = (st.session_state["q_index"] + 1) % len(questions)
                st.rerun()
        with col_review:
            if st.button("Review Concept in Library", key="btn_rev_q_lib", use_container_width=True):
                st.session_state["current_page"] = "learning_library"
                st.session_state["selected_lesson_code"] = current_q["concept_code"]
                st.rerun()
