"""
SARVAVIDYA: AI-Powered "Ask AI Why?" Assessment Diagnostic Component
Provides real-time, context-aware pedagogical remediation for incorrect quiz answers:
- Evaluates student's chosen incorrect option against the correct answer and specific syllabus context.
- Generates 7-tier explanation: Why incorrect, why correct, underlying misconception, step-by-step logic,
  real-world analogy, practical demonstration, and quick practice self-test.
- Caches generated explanations in session state to prevent redundant API calls.
- Offers interactive 'Try Another Example', follow-up doubt resolution, and 'Got It' dismissal.
- Connects with BKT mastery profile to suggest remedial practice when concept mastery is low (<60%).
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from database.db import get_learning_content_by_concept
from core.misconception import MisconceptionEngine
from core.ai_service import (
    generate_ai_why_explanation,
    generate_ai_why_alternate_example,
    query_ai_why_followup,
    get_gemini_api_key
)


def render_ask_ai_why_component(
    current_q: Dict[str, Any],
    options: List[Dict[str, Any]],
    chosen_opt: Dict[str, Any],
    is_correct: bool,
    eval_res: Dict[str, Any],
    active_course: Dict[str, Any],
    user: Dict[str, Any]
):
    """
    Renders the 'Ask AI Why?' interactive trigger and diagnostic card
    strictly when an answer is evaluated and found incorrect.
    """
    # 1. Enforce requirement: only display for incorrect evaluated answers
    if is_correct:
        return

    q_id = current_q["id"]
    chosen_idx = chosen_opt.get("index", 0)
    chosen_text = chosen_opt.get("text", "")

    # Locate correct option
    correct_opt = next((o for o in options if o.get("is_correct")), None)
    correct_text = correct_opt.get("text", "") if correct_opt else "Correct Option"

    # Identify misconception details
    m_code = chosen_opt.get("misconception_code")
    m_info = MisconceptionEngine.get_info(m_code)
    m_name = m_info["name"] if m_info else "Conceptual Misunderstanding"
    m_remediation = m_info["remediation"] if m_info else "Review fundamental syllabus rules."

    # Cache keys
    show_key = f"show_ai_why_{q_id}"
    cache_key = f"ai_why_cache_{q_id}_{chosen_idx}"
    alt_key = f"ai_why_alt_{q_id}_{chosen_idx}"
    followup_key = f"ai_why_followups_{q_id}_{chosen_idx}"

    if show_key not in st.session_state:
        st.session_state[show_key] = False

    is_panel_open = st.session_state[show_key]
    has_gemini = bool(get_gemini_api_key())

    # 2. Prominent "Ask AI Why?" Action Bar
    st.markdown("""
    <style>
    .ai-why-trigger-box {
        background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
        border: 1.5px solid #818CF8;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.65rem 0 0.85rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.08);
    }
    @media (max-width: 640px) {
        .ai-why-trigger-box {
            flex-direction: column;
            align-items: flex-start;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    col_btn, col_desc = st.columns([0.42, 0.58])
    with col_btn:
        if st.button(
            "✨ Ask AI Why? (Open Assistant)",
            key=f"btn_modal_ai_why_{q_id}",
            type="primary",
            use_container_width=True
        ):
            st.session_state["sarva_ai_dialog_open"] = True
            st.session_state["sarva_ai_active_context"] = {
                "type": "ask_ai_why",
                "question": current_q,
                "options": options,
                "chosen_opt": chosen_opt,
                "is_correct": is_correct,
                "eval_res": eval_res
            }
            # Also award engagement coins
            try:
                from core.rewards_engine import RewardsEngine
                RewardsEngine.update_mission_progress(user["id"], "ai_activity", 1)
                RewardsEngine.award_coins(
                    user_id=user["id"],
                    amount=5,
                    source_activity="ASK_AI_WHY_ENGAGEMENT",
                    entity_id=f"why_{q_id}",
                    description=f"Consulted SARVA AI Why for Q#{q_id}",
                    idempotency_key=f"why_consult_{user['id']}_{q_id}"
                )
            except Exception:
                pass
            st.rerun()

    with col_desc:
        engine_label = "Gemini 3.1 Live AI" if has_gemini else "Curriculum Diagnostic Engine"
        st.markdown(f"""
        <div style="padding-top: 4px; line-height: 1.35;">
            <div style="font-size: 0.825rem; font-weight: 700; color: #3730A3;">
                🤖 Don't understand why your answer was wrong?
            </div>
            <div style="font-size: 0.725rem; color: #4F46E5;">
                Click <strong>Ask AI Why?</strong> to launch the centered AI diagnostic coach powered by <em>{engine_label}</em>.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Expandable AI Explanation Panel
    if is_panel_open:
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

        # Retrieve explanation from session state or generate
        if cache_key not in st.session_state:
            with st.spinner("🧠 SARVA AI is analyzing your answer against curriculum knowledge and generating your step-by-step diagnostic breakdown..."):
                # Fetch lesson context if concept is active
                lesson_summary = None
                if current_q.get("concept_id"):
                    lesson = get_learning_content_by_concept(current_q["concept_id"])
                    if lesson:
                        lesson_summary = lesson.get("summary")

                explanation_text = generate_ai_why_explanation(
                    question_title=current_q["title"],
                    question_prompt=current_q["prompt"],
                    options=options,
                    selected_answer=chosen_text,
                    correct_answer=correct_text,
                    subject_name=active_course.get("subject_name", "General Studies"),
                    course_name=active_course.get("name", "Active Course"),
                    concept_name=current_q.get("concept_name", "Current Topic"),
                    code_snippet=current_q.get("code_snippet"),
                    misconception_name=m_name,
                    misconception_explanation=chosen_opt.get("explanation"),
                    base_explanation=current_q.get("explanation"),
                    lesson_summary=lesson_summary
                )
                st.session_state[cache_key] = explanation_text
        else:
            explanation_text = st.session_state[cache_key]

        # RENDER FULL AI WHY STUDIO PANEL
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #6366F1; border-radius: 12px; padding: 1.25rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 4px 18px rgba(99, 102, 241, 0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E0E7FF; padding-bottom: 0.65rem; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 32px; height: 32px; border-radius: 8px; background: #4338CA; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem;">
                        SA
                    </div>
                    <div>
                        <div style="font-weight: 800; font-size: 0.95rem; color: #1E1B4B; line-height: 1.2;">
                            SARVA AI Diagnostic Coach &bull; <span style="font-weight: 600; color: #6366F1;">Context-Aware Breakdown</span>
                        </div>
                        <div style="font-size: 0.725rem; color: #6B7280;">
                            Target Concept: <strong>{current_q.get('concept_name', 'Topic')}</strong> &bull; Diagnosed Pattern: <span style="color: #DC2626; font-weight: 600;">{m_name}</span>
                        </div>
                    </div>
                </div>
                <div>
                    <span style="background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;">
                        {'✨ Powered by Gemini 3.1 Live AI' if has_gemini else '📚 Verified Curriculum Engine'}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Markdown Rendered Diagnosis
        st.markdown(explanation_text, unsafe_allow_html=True)

        # Alternate Example Card (if requested)
        if alt_key in st.session_state:
            st.markdown(f"""
            <div style="background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 8px; padding: 0.85rem 1rem; margin: 0.85rem 0;">
                <div style="font-weight: 700; color: #166534; font-size: 0.85rem; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 6px;">
                    <span>💡 Alternative Intuition & Mental Model</span>
                </div>
                <div style="color: #14532D; font-size: 0.825rem; line-height: 1.5;">
                    {st.session_state[alt_key]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # BKT Mastery Alert & Remediation Recommendation
        posterior_m = eval_res.get("posterior_mastery", 0.20)
        if posterior_m < 0.60:
            st.markdown(f"""
            <div style="background: #FFFBEB; border: 1.5px solid #FCD34D; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 0.75rem;">
                <div style="font-weight: 700; color: #92400E; font-size: 0.825rem; display: flex; align-items: center; gap: 6px;">
                    <span>⚠️ BKT Mastery Level: Developing ({posterior_m:.0%})</span>
                </div>
                <div style="font-size: 0.75rem; color: #B45309; margin-top: 0.2rem; line-height: 1.4;">
                    Your knowledge probability in <strong>{current_q.get('concept_name', 'this concept')}</strong> is below the 60% proficiency threshold. 
                    We recommend reading the dedicated curriculum module or completing a targeted practice drill.
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_rec_lib, col_rec_space = st.columns([0.45, 0.55])
            with col_rec_lib:
                if st.button("📖 Review Lesson in Library", key=f"btn_why_rec_lib_{q_id}", use_container_width=True):
                    st.session_state["current_page"] = "learning_library"
                    st.session_state["_synced_page"] = "learning_library"
                    st.session_state["selected_lesson_code"] = current_q.get("concept_code")
                    st.rerun()

        st.markdown("<hr style='border-color: #E2E8F0; margin: 1rem 0 0.75rem 0;'>", unsafe_allow_html=True)

        # Action Buttons Row: Try Another Example + Got It
        col_act1, col_act2, col_act3 = st.columns([0.35, 0.35, 0.30])
        with col_act1:
            if st.button("🔄 Try Another Example", key=f"btn_alt_ex_{q_id}_{chosen_idx}", use_container_width=True):
                with st.spinner("Generating fresh alternative analogy and example..."):
                    alt_res = generate_ai_why_alternate_example(
                        concept_name=current_q.get("concept_name", "Current Topic"),
                        course_name=active_course.get("name", "Active Course"),
                        question_title=current_q["title"],
                        misconception_name=m_name
                    )
                    st.session_state[alt_key] = alt_res
                    st.rerun()

        with col_act2:
            if st.button("✅ Got It (Close)", key=f"btn_got_it_{q_id}", type="primary", use_container_width=True):
                st.session_state[show_key] = False
                st.rerun()

        with col_act3:
            if st.button("💬 Ask in AI Studio", key=f"btn_goto_studio_{q_id}", use_container_width=True):
                st.session_state["current_page"] = "sarva_ai_page"
                st.session_state["_synced_page"] = "sarva_ai_page"
                st.session_state["sidebar_nav_radio"] = "SARVA AI Companion"
                st.rerun()

        # Follow-Up Question Doubts Interface
        st.markdown("""
        <div style="margin-top: 0.85rem; padding-top: 0.75rem; border-top: 1px dashed #E2E8F0;">
            <div style="font-weight: 700; font-size: 0.8rem; color: #1E293B; margin-bottom: 0.35rem;">
                💬 Have a follow-up doubt about this concept?
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display previous follow-ups for this question
        followups = st.session_state.get(followup_key, [])
        if followups:
            for item in followups:
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <div style="background: #F1F5F9; border-radius: 6px; padding: 0.45rem 0.65rem; font-size: 0.775rem; color: #334155; margin-bottom: 0.25rem;">
                        <strong>You asked:</strong> {item['query']}
                    </div>
                    <div style="background: #F8FAFC; border-left: 3px solid #6366F1; border-radius: 4px; padding: 0.5rem 0.75rem; font-size: 0.8rem; color: #1E293B; line-height: 1.45;">
                        <strong>SARVA AI:</strong> {item['response']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Follow-up input form
        with st.form(key=f"form_followup_{q_id}_{chosen_idx}"):
            col_f_in, col_f_btn = st.columns([0.8, 0.2])
            with col_f_in:
                user_followup = st.text_input(
                    "Your follow-up question:",
                    placeholder=f"e.g., Why doesn't {chosen_text} work here? What if I used another method?",
                    key=f"input_followup_{q_id}_{chosen_idx}",
                    label_visibility="collapsed"
                )
            with col_f_btn:
                send_f = st.form_submit_button("Ask Doubt", type="primary", use_container_width=True)

            if send_f and user_followup.strip():
                with st.spinner("SARVA AI is analyzing your doubt..."):
                    reply = query_ai_why_followup(
                        user_query=user_followup.strip(),
                        concept_name=current_q.get("concept_name", "Current Topic"),
                        course_name=active_course.get("name", "Active Course"),
                        question_title=current_q["title"],
                        selected_answer=chosen_text,
                        correct_answer=correct_text
                    )
                    if followup_key not in st.session_state:
                        st.session_state[followup_key] = []
                    st.session_state[followup_key].append({
                        "query": user_followup.strip(),
                        "response": reply
                    })
                    st.rerun()

        # Close Outer Wrapper
        st.markdown("</div>", unsafe_allow_html=True)

