"""
LearnSphere AI: Intelligent Adaptive Assessment Module
Delivers multiple choice questions with labeled distractors, real-time BKT updates,
response latency recording, and immediate misconception feedback.
Modern minimalist SaaS design inspired by Linear and Stripe.
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


def render_assessment_page(user: dict):
    user_id = user["id"]
    concepts = get_all_concepts()

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #172554; margin: 0; letter-spacing: -0.025em;">
            Intelligent Adaptive Assessment
        </h2>
        <p style="color: #64748B; font-size: 0.875rem; margin-top: 0.25rem;">
            Test your comprehension. The AI engine dynamically evaluates your latent concept mastery and diagnoses specific cognitive bugs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Subject and Filter Controls
    col_sub, col_c, col_d = st.columns([1, 2, 1.5])
    with col_sub:
        st.selectbox("Subject Area", ["Python Programming"], disabled=True)

    concept_options = {"All Concepts": None}
    for c in concepts:
        concept_options[f"{c['code']} - {c['name']}"] = c["id"]

    # Pre-select concept if passed from dashboard recommendation
    preselected_id = st.session_state.pop("assessment_concept_id", None)
    default_c_idx = 0
    if preselected_id:
        for idx, (label, cid) in enumerate(concept_options.items()):
            if cid == preselected_id:
                default_c_idx = idx
                break

    with col_c:
        selected_label = st.selectbox("Target Concept", list(concept_options.keys()), index=default_c_idx)
        selected_concept_id = concept_options[selected_label]

    with col_d:
        difficulty_mode = st.selectbox(
            "Difficulty Selection",
            ["Adaptive (AI Selected)", "Beginner", "Intermediate", "Advanced"],
            index=0
        )

    # 2. Determine questions pool based on difficulty mode
    actual_diff = None
    if difficulty_mode == "Adaptive (AI Selected)":
        if selected_concept_id:
            m_rec = get_student_concept_mastery(user_id, selected_concept_id)
            current_mastery = m_rec["mastery_prob"] if m_rec else 0.20
        else:
            current_mastery = 0.50
        actual_diff = RecommenderEngine.get_adaptive_difficulty(current_mastery)
        st.caption(f"Adaptive Engine matched current mastery ({current_mastery:.0%}) to **{actual_diff.capitalize()}** difficulty.")
    else:
        actual_diff = difficulty_mode.lower()

    questions = get_questions_by_concept_and_difficulty(selected_concept_id, actual_diff)

    if not questions:
        questions = get_questions_by_concept_and_difficulty(selected_concept_id, "all")

    if not questions:
        st.warning("No questions found matching the selected filters. Please adjust your criteria.")
        return

    # Manage question pagination state
    if "q_index" not in st.session_state:
        st.session_state["q_index"] = 0

    if st.session_state["q_index"] >= len(questions):
        st.session_state["q_index"] = 0

    q_idx = st.session_state["q_index"]
    current_q = questions[q_idx]

    # Initialize question start time for latency tracking
    q_key = f"q_start_time_{current_q['id']}"
    if q_key not in st.session_state:
        st.session_state[q_key] = time.time()

    # 3. Render Question Card
    diff_badge_class = "badge-mastered" if current_q["difficulty"] == "beginner" else ("badge-proficient" if current_q["difficulty"] == "intermediate" else "badge-developing")
    st.markdown(f"""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-demo" style="margin-right: 0.5rem;">Question {q_idx + 1} of {len(questions)}</span>
                <span class="ls-badge {diff_badge_class}">{current_q['difficulty'].capitalize()}</span>
                <span style="color: #64748B; font-size: 0.85rem; margin-left: 0.75rem;">Topic: {current_q['concept_name']}</span>
            </div>
            <div style="font-size: 0.8rem; color: #64748B;">Item ID: #{current_q['id']}</div>
        </div>
        <h3 style="font-size: 1.15rem; font-weight: 600; color: #172554; margin-bottom: 0.75rem; letter-spacing: -0.015em;">
            {current_q['title']}
        </h3>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">
            {current_q['prompt']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if current_q.get("code_snippet"):
        st.code(current_q["code_snippet"], language="python")

    # Options Form
    options = current_q["options"]
    option_labels = [opt["text"] for opt in options]

    form_key = f"q_form_{current_q['id']}_{q_idx}"
    with st.form(form_key):
        selected_text = st.radio(
            "Select the most accurate response:",
            option_labels,
            index=None,
            key=f"radio_{current_q['id']}"
        )
        col_sub_btn, col_skip = st.columns([1, 1])
        with col_sub_btn:
            submit_answer = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)

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
            attempt_id = record_assessment_attempt(
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
            <div class="ls-success-box">
                <div style="font-weight: 700; color: #166534; font-size: 1.05rem; margin-bottom: 0.35rem;">
                    Correct Answer Verified
                </div>
                <div style="color: #14532D; font-size: 0.9rem; line-height: 1.55; margin-bottom: 0.5rem;">
                    {res['chosen_opt']['explanation']}
                </div>
                <div style="font-size: 0.825rem; color: #166534;">
                    Response recorded in {res['elapsed_time']}s &bull; BKT Mastery increased from <strong>{res['prior_mastery']:.1%}</strong> to <strong>{res['posterior_mastery']:.1%}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            m_code = res["chosen_opt"].get("misconception_code")
            m_info = MisconceptionEngine.get_info(m_code)
            m_name = m_info["name"] if m_info else "Incorrect Logic"
            m_rem = m_info["remediation"] if m_info else "Review fundamental rules in the curriculum."

            st.markdown(f"""
            <div class="ls-diagnostic-box">
                <div style="font-weight: 700; color: #991B1B; font-size: 1.05rem; margin-bottom: 0.35rem;">
                    Misconception Identified: {m_name}
                </div>
                <div style="color: #881337; font-size: 0.9rem; line-height: 1.55; margin-bottom: 0.5rem;">
                    <strong>Why this error occurs:</strong> {res['chosen_opt']['explanation']}
                </div>
                <div style="background-color: #FFFFFF; padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid #FECDD3; color: #991B1B; font-size: 0.85rem; margin-bottom: 0.5rem;">
                    <strong>Pedagogical Remediation:</strong> {m_rem}
                </div>
                <div style="font-size: 0.825rem; color: #991B1B;">
                    BKT Mastery adjusted from <strong>{res['prior_mastery']:.1%}</strong> to <strong>{res['posterior_mastery']:.1%}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ls-info-box">
            <strong style="color: #172554;">Comprehensive Solution:</strong>
            <p style="color: #475569; font-size: 0.875rem; margin-top: 0.25rem; line-height: 1.55;">
                {res['explanation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_next, col_lib = st.columns([1, 1])
        with col_next:
            if st.button("Proceed to Next Question", type="primary", use_container_width=True):
                st.session_state.pop(eval_key, None)
                st.session_state[f"q_start_time_{current_q['id']}"] = time.time()
                st.session_state["q_index"] = (st.session_state["q_index"] + 1) % len(questions)
                st.rerun()
        with col_lib:
            if st.button("Review Lesson in Library", use_container_width=True):
                st.session_state["current_page"] = "learning_library"
                st.session_state["selected_lesson_code"] = current_q["concept_code"]
                st.rerun()
