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
    record_assessment_attempt, get_user_attempts
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
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">Sarva Vidya Adaptive Assessment</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Latent concept mastery evaluation with distractor-based cognitive misconception detection.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Subject and Filter Controls
    curr_course_id = active_course["id"]

    # Detect course switch and reset q_index cleanly
    prev_course_track_key = f"assess_prev_course_{user_id}"
    if st.session_state.get(prev_course_track_key) != curr_course_id:
        st.session_state[prev_course_track_key] = curr_course_id
        st.session_state["q_index"] = 0

    # Build concept map
    concept_options = {"All Concepts in Track": None}
    for c in concepts:
        concept_options[f"{c['code']} - {c['name']}"] = c["id"]

    select_key = f"assess_concept_choice_{curr_course_id}"
    all_concept_labels = list(concept_options.keys())

    # Handle incoming concept navigation from search / dashboard
    incoming_concept_id = st.session_state.pop("assessment_concept_id", None) or st.session_state.pop("active_concept_id", None)
    if incoming_concept_id is not None:
        for label, cid in concept_options.items():
            if cid == incoming_concept_id:
                st.session_state[select_key] = label
                st.session_state["q_index"] = 0
                break

    # Initialize key in session state if not set or invalid for current course
    if select_key not in st.session_state or st.session_state[select_key] not in all_concept_labels:
        st.session_state[select_key] = all_concept_labels[0]

    col_t, col_c, col_d = st.columns([1.2, 1.4, 1.0])
    with col_t:
        render_course_selector(key="assess_track_selector", label="Select Track", on_change_rerun=True)

    with col_c:
        selected_label = st.selectbox(
            "Curriculum Concept Target",
            all_concept_labels,
            key=select_key,
            label_visibility="collapsed"
        )
        selected_concept_id = concept_options.get(selected_label)

    # Detect concept change to reset q_index cleanly without rerun conflicts
    if st.session_state.get(f"assess_prev_label_{curr_course_id}") != selected_label:
        st.session_state[f"assess_prev_label_{curr_course_id}"] = selected_label
        st.session_state["q_index"] = 0

    diff_key = "assess_difficulty_choice"
    diff_options = ["Adaptive (AI Selected)", "Beginner", "Intermediate", "Advanced"]
    if diff_key not in st.session_state or st.session_state[diff_key] not in diff_options:
        st.session_state[diff_key] = "Adaptive (AI Selected)"

    with col_d:
        difficulty_mode = st.selectbox(
            "Difficulty Selection",
            diff_options,
            key=diff_key,
            label_visibility="collapsed"
        )

    if st.session_state.get("assess_prev_diff_choice") != difficulty_mode:
        st.session_state["assess_prev_diff_choice"] = difficulty_mode
        st.session_state["q_index"] = 0

    # 2. Determine questions pool based on target concept and difficulty mode
    if difficulty_mode == "Adaptive (AI Selected)":
        if selected_concept_id:
            m_rec = get_student_concept_mastery(user_id, selected_concept_id)
            current_mastery = m_rec["mastery_prob"] if m_rec else 0.20
        else:
            current_mastery = 0.50
        actual_diff = RecommenderEngine.get_adaptive_difficulty(current_mastery)

        all_concept_qs = get_questions_by_concept_and_difficulty(selected_concept_id, "all", course_id=active_course["id"])
        if selected_concept_id:
            # Order questions so student's current adaptive level appears first, followed by other questions in the concept
            matching_qs = [q for q in all_concept_qs if q.get("difficulty") == actual_diff]
            other_qs = [q for q in all_concept_qs if q.get("difficulty") != actual_diff]
            questions = matching_qs + other_qs if matching_qs else all_concept_qs
        else:
            # For "All Concepts", prioritize adaptive difficulty questions across track
            matching_qs = [q for q in all_concept_qs if q.get("difficulty") == actual_diff]
            questions = matching_qs if matching_qs else all_concept_qs
    else:
        actual_diff = difficulty_mode.lower()
        questions = get_questions_by_concept_and_difficulty(selected_concept_id, actual_diff, course_id=active_course["id"])
        if not questions:
            questions = get_questions_by_concept_and_difficulty(selected_concept_id, "all", course_id=active_course["id"])

    if not questions:
        # Fallback to all questions in active track if the specific concept filter yielded none
        questions = get_questions_by_concept_and_difficulty(None, "all", course_id=active_course["id"])

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

    # 3. Completion Tracking for Navigation Grid
    user_attempts = get_user_attempts(user_id, limit=300, course_id=active_course["id"])
    completed_q_ids = {a["question_id"] for a in user_attempts}
    if "completed_assessment_q_ids" in st.session_state:
        completed_q_ids.update(st.session_state["completed_assessment_q_ids"])
    for q in questions:
        if f"eval_{q['id']}" in st.session_state:
            completed_q_ids.add(q["id"])

    # 4. Two-Column Layout: Question Interface (Left) + Question Navigation & Stats (Right)
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

        # Format Options with clean alphabetical keys (A, B, C, D)
        options = current_q["options"]
        opt_display_labels = [f"{chr(65+idx)}.  {opt['text']}" for idx, opt in enumerate(options)]
        label_to_opt = {f"{chr(65+idx)}.  {opt['text']}": opt for idx, opt in enumerate(options)}

        eval_key = f"eval_{current_q['id']}"
        is_evaluated = eval_key in st.session_state

        if not is_evaluated:
            # ACTIVE QUESTION FORM: Clean selection and submission
            form_key = f"q_form_{current_q['id']}_{q_idx}"
            with st.form(form_key):
                selected_display = st.radio(
                    "Select your response:",
                    opt_display_labels,
                    index=None,
                    key=f"radio_{current_q['id']}_{q_idx}",
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

            if submit_answer:
                if selected_display is None:
                    st.error("Please select an answer option before submitting.")
                else:
                    elapsed_time = round(time.time() - st.session_state.get(q_key, time.time()), 2)
                    chosen_opt = label_to_opt[selected_display]
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

                    completed_q_ids.add(current_q["id"])
                    if "completed_assessment_q_ids" not in st.session_state:
                        st.session_state["completed_assessment_q_ids"] = set()
                    st.session_state["completed_assessment_q_ids"].add(current_q["id"])
                    st.rerun()

        else:
            # EVALUATED STATE: Visual card feedback showing selected vs correct answer
            res = st.session_state[eval_key]
            chosen_opt_text = res["chosen_opt"]["text"]
            is_corr = res["is_correct"]

            st.markdown("<div style='margin-bottom: 0.85rem;'>", unsafe_allow_html=True)
            for idx, opt in enumerate(options):
                opt_letter = chr(65 + idx)
                opt_txt = opt["text"]
                was_chosen = (opt_txt == chosen_opt_text)
                is_this_corr = bool(opt.get("is_correct", False))

                if was_chosen and is_this_corr:
                    card_border = "#36A879"
                    card_bg = "#EDF8F3"
                    badge = '<span class="lm-pill pill-completed" style="font-size:0.65rem;">Your Answer &bull; Correct</span>'
                elif was_chosen and not is_this_corr:
                    card_border = "#D96B6B"
                    card_bg = "#FDF2F2"
                    badge = '<span class="lm-pill pill-lagging" style="font-size:0.65rem;">Your Answer &bull; Incorrect</span>'
                elif is_this_corr:
                    card_border = "#36A879"
                    card_bg = "#F0FDF4"
                    badge = '<span class="lm-pill pill-ahead" style="font-size:0.65rem;">Correct Answer</span>'
                else:
                    card_border = "#E4E8ED"
                    card_bg = "#FAFAFA"
                    badge = ""

                st.markdown(f"""
                <div style="background:{card_bg}; border:1.5px solid {card_border}; border-radius:8px; padding:0.65rem 0.85rem; margin-bottom:0.4rem; display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-weight:700; font-size:0.75rem; color:#243B64; background:#FFFFFF; border:1px solid #CBD5E1; width:22px; height:22px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;">{opt_letter}</span>
                        <span style="font-size:0.825rem; color:#172943; font-weight:500;">{opt_txt}</span>
                    </div>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Detailed Pedagogical Diagnostic Feedback
            if is_corr:
                st.markdown(f"""
                <div class="lm-card" style="border-left: 4px solid #36A879; background-color: #EDF8F3; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem;">
                    <div style="font-weight: 700; color: #166534; font-size: 0.95rem; margin-bottom: 0.25rem;">
                        Correct Answer Verified
                    </div>
                    <div style="color: #14532D; font-size: 0.825rem; line-height: 1.5; margin-bottom: 0.4rem;">
                        {res['chosen_opt'].get('explanation', current_q.get('explanation', ''))}
                    </div>
                    <div style="font-size: 0.75rem; color: #166534;">
                        Latency: {res['elapsed_time']}s &bull; BKT Mastery updated from <strong>{res['prior_mastery']:.0%}</strong> to <strong>{res['posterior_mastery']:.0%}</strong>.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                m_code = res["chosen_opt"].get("misconception_code")
                m_info = MisconceptionEngine.get_info(m_code)
                m_name = m_info["name"] if m_info else "Incorrect Mental Model"
                m_rem = m_info["remediation"] if m_info else "Review core curriculum principles."

                st.markdown(f"""
                <div class="lm-card" style="border-left: 4px solid #D96B6B; background-color: #FDF2F2; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem;">
                    <div style="font-weight: 700; color: #991B1B; font-size: 0.95rem; margin-bottom: 0.25rem;">
                        Misconception Identified: {m_name}
                    </div>
                    <div style="color: #881337; font-size: 0.825rem; line-height: 1.5; margin-bottom: 0.4rem;">
                        <strong>Why this error occurs:</strong> {res['chosen_opt'].get('explanation', '')}
                    </div>
                    <div style="background-color: #FFFFFF; padding: 0.5rem 0.75rem; border-radius: 6px; border: 1px solid #FECDD3; color: #991B1B; font-size: 0.775rem; margin-bottom: 0.4rem;">
                        <strong>Pedagogical Remediation:</strong> {m_rem}
                    </div>
                    <div style="font-size: 0.75rem; color: #991B1B;">
                        BKT Mastery adjusted from <strong>{res['prior_mastery']:.0%}</strong> to <strong>{res['posterior_mastery']:.0%}</strong>.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Evaluated Action Buttons
            col_next_q, col_retry, col_review = st.columns([1.2, 1.0, 1.0])
            with col_next_q:
                if st.button("Proceed to Next Question →", key="btn_next_q_after_eval", type="primary", use_container_width=True):
                    st.session_state.pop(eval_key, None)
                    st.session_state[f"q_start_time_{current_q['id']}"] = time.time()
                    st.session_state["q_index"] = (st.session_state["q_index"] + 1) % len(questions)
                    st.rerun()
            with col_retry:
                if st.button("Try Question Again", key=f"btn_retry_{current_q['id']}", use_container_width=True):
                    st.session_state.pop(eval_key, None)
                    st.session_state[f"q_start_time_{current_q['id']}"] = time.time()
                    st.rerun()
            with col_review:
                if st.button("Review in Library", key="btn_rev_q_lib", use_container_width=True):
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["_synced_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = current_q["concept_code"]
                    st.rerun()

    with col_q_nav:
        # Question Navigation Panel
        st.markdown("""
        <div class="lm-card" style="padding: 0.85rem; margin-bottom: 0.75rem;">
            <div style="font-weight: 700; font-size: 0.8rem; color: #243B64; margin-bottom: 0.5rem;">Question Navigation</div>
        """, unsafe_allow_html=True)

        # Dynamic CSS for question buttons: Completed buttons appear in emerald green!
        nav_css = []
        for i, q in enumerate(questions):
            q_comp = q["id"] in completed_q_ids
            q_curr = (i == q_idx)

            if q_comp and q_curr:
                nav_css.append(f"""
                .st-key-assess_qnav_btn_{i} button,
                div[class*="st-key-assess_qnav_btn_{i}"] button {{
                    background-color: #2F9168 !important;
                    border: 2px solid #D6B56D !important;
                    box-shadow: 0 0 0 2px rgba(214, 181, 109, 0.45) !important;
                }}
                .st-key-assess_qnav_btn_{i} button p,
                div[class*="st-key-assess_qnav_btn_{i}"] button p {{
                    color: #FFFFFF !important;
                    font-weight: 800 !important;
                }}
                """)
            elif q_comp:
                nav_css.append(f"""
                .st-key-assess_qnav_btn_{i} button,
                div[class*="st-key-assess_qnav_btn_{i}"] button {{
                    background-color: #36A879 !important;
                    border: 1.5px solid #28875E !important;
                    box-shadow: 0 1px 3px rgba(54, 168, 121, 0.25) !important;
                }}
                .st-key-assess_qnav_btn_{i} button p,
                div[class*="st-key-assess_qnav_btn_{i}"] button p {{
                    color: #FFFFFF !important;
                    font-weight: 700 !important;
                }}
                .st-key-assess_qnav_btn_{i} button:hover,
                div[class*="st-key-assess_qnav_btn_{i}"] button:hover {{
                    background-color: #2F9168 !important;
                    border-color: #206E4C !important;
                }}
                """)
            elif q_curr:
                nav_css.append(f"""
                .st-key-assess_qnav_btn_{i} button,
                div[class*="st-key-assess_qnav_btn_{i}"] button {{
                    background-color: #172943 !important;
                    border: 1.5px solid #D6B56D !important;
                    box-shadow: 0 2px 5px rgba(23, 41, 67, 0.25) !important;
                }}
                .st-key-assess_qnav_btn_{i} button p,
                div[class*="st-key-assess_qnav_btn_{i}"] button p {{
                    color: #FFFFFF !important;
                    font-weight: 700 !important;
                }}
                """)
            else:
                nav_css.append(f"""
                .st-key-assess_qnav_btn_{i} button,
                div[class*="st-key-assess_qnav_btn_{i}"] button {{
                    background-color: #FFFFFF !important;
                    border: 1px solid #E4E8ED !important;
                }}
                .st-key-assess_qnav_btn_{i} button p,
                div[class*="st-key-assess_qnav_btn_{i}"] button p {{
                    color: #172943 !important;
                    font-weight: 600 !important;
                }}
                .st-key-assess_qnav_btn_{i} button:hover,
                div[class*="st-key-assess_qnav_btn_{i}"] button:hover {{
                    background-color: #FAF5EA !important;
                    border-color: #D6B56D !important;
                }}
                """)

        st.markdown(f"<style>{''.join(nav_css)}</style>", unsafe_allow_html=True)

        # Mini grid of question buttons
        q_cols = st.columns(4)
        for i in range(len(questions)):
            with q_cols[i % 4]:
                if st.button(f"{i+1}", key=f"assess_qnav_btn_{i}", use_container_width=True):
                    st.session_state["q_index"] = i
                    st.rerun()

        st.markdown("""
        <div style="display: flex; gap: 8px; margin-top: 0.65rem; font-size: 0.68rem; color: #718096; align-items: center; justify-content: space-between; padding-top: 0.4rem; border-top: 1px solid #E4E8ED;">
            <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 8px; height: 8px; border-radius: 2px; background: #36A879; display: inline-block;"></span> Answered</span>
            <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 8px; height: 8px; border-radius: 2px; background: #172943; border: 1px solid #D6B56D; display: inline-block;"></span> Active</span>
            <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 8px; height: 8px; border-radius: 2px; background: #FFFFFF; border: 1px solid #E4E8ED; display: inline-block;"></span> Pending</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

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
