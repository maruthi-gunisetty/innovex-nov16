"""
SARVAVIDYA: SARVA AI – Intelligent Learning Assistant
Provides a centralized, responsive, floating launcher and large centered modal assistant:
- Floating launcher positioned on the right edge of viewport with subtle pulse animation
- Centered, backdrop-dimmed, high-elevation large modal dialog accessible across all supported pages
- Seamlessly handles both general syllabus learning Q&A and contextual 'Ask AI Why?' diagnostics
- Subject & Course Context Awareness (Python, C, Mathematics, DSA, Digital Electronics, Quantum, etc.)
- Transparent AI engine: uses external GenAI when API key is configured, or verified curriculum engine fallback
- Formative pedagogical support that does NOT arbitrarily alter BKT mastery probabilities
"""

import streamlit as st
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from database.db import (
    get_learning_content_by_concept, get_concepts_by_course,
    get_user_attempts, get_student_concept_mastery,
    save_chat_message, get_chat_history, clear_chat_history
)
from core.course_manager import get_active_course
from core.ai_service import (
    query_gemini_ai, get_gemini_api_key,
    generate_ai_why_explanation, generate_ai_why_alternate_example, query_ai_why_followup
)
from core.misconception import MisconceptionEngine


def _get_curriculum_response(prompt: str, user: dict, course: dict, concept: Optional[dict]) -> str:
    """
    Intelligent curriculum-backed response generator querying verified database content.
    Identified transparently as the SARVA AI Curriculum Engine.
    """
    user_id = user["id"]
    course_name = course["name"]
    course_code = course["code"]
    concept_name = concept["name"] if concept else "General Curriculum"
    concept_id = concept["id"] if concept else None

    lesson = None
    if concept_id:
        lesson = get_learning_content_by_concept(concept_id)

    recent_attempts = get_user_attempts(user_id, limit=5, course_id=course["id"])
    last_incorrect = next((a for a in recent_attempts if not a.get("is_correct")), None)

    p_lower = prompt.lower().strip()

    if any(k in p_lower for k in ["explain", "simple language", "what is", "meaning", "concept"]):
        if lesson:
            objectives = "\n".join([f"• {obj}" for obj in lesson.get("learning_objectives", [])[:3]])
            return (
                f"**Understanding {concept_name} ({course_name})**\n\n"
                f"{lesson.get('summary', '')}\n\n"
                f"**Key Conceptual Principles:**\n{objectives}\n\n"
                f"**Detailed Overview:**\n{lesson.get('introduction', '')}\n\n"
                f"💡 *Tip: Try asking me for a code example or practice exercise for this topic!*"
            )
        else:
            return (
                f"**Overview for {course_name} &bull; {concept_name}**\n\n"
                f"In this module, you study foundational principles of {course_name}. "
                f"Ensure you understand the core prerequisites before advancing to deeper applications.\n\n"
                f"Would you like to examine a code example or inspect common pitfalls?"
            )

    elif any(k in p_lower for k in ["example", "code", "syntax", "snippet", "demonstrate"]):
        if lesson and lesson.get("code_examples"):
            examples = lesson["code_examples"]
            ex = examples[0]
            code = ex.get("code", "")
            output = ex.get("output", "")
            notes = ex.get("notes", "")
            lang = "python" if "python" in course_code else ("c" if "c" in course_code else "text")
            return (
                f"**Practical Example: {ex.get('title', concept_name)}**\n\n"
                f"```{lang}\n{code}\n```\n\n"
                f"**Execution Output:**\n```text\n{output}\n```\n\n"
                f"**Analysis:** {notes}"
            )
        else:
            return (
                f"**Sample Implementation ({course_name}):**\n\n"
                f"Focus on declaring variables cleanly, respecting boundary conditions, "
                f"and tracing execution line-by-line. Switch to a specific topic to inspect dedicated code traces!"
            )

    elif any(k in p_lower for k in ["wrong", "incorrect", "mistake", "error", "misconception", "why"]):
        if last_incorrect:
            q_title = last_incorrect.get("question_title", "Recent Question")
            m_code = last_incorrect.get("misconception_code", "COMMON_ERROR")
            clean_m = m_code.replace("_", " ").title()
            return (
                f"**Diagnostic Error Analysis**\n\n"
                f"In your recent attempt on **'{q_title}'**, our BKT diagnostic engine detected the pattern: **{clean_m}**.\n\n"
                f"**Why this happens:** Students often confuse assignment with equality or assume implicit type coercion. "
                f"Review the problem specification carefully and check operator precedence before submitting."
            )
        elif lesson and lesson.get("common_mistakes"):
            mistake = lesson["common_mistakes"][0]
            return (
                f"**Common Student Pitfall in {concept_name}**\n\n"
                f"**Frequent Error:** `{mistake.get('wrong_code', '')}`\n\n"
                f"**Correct Approach:** `{mistake.get('correct_code', '')}`\n\n"
                f"**Cognitive Cause:** {mistake.get('explanation', '')}"
            )
        else:
            return (
                "You currently have no recent flagged misconceptions in this track! Keep solving adaptive drills "
                "to maintain your high accuracy score."
            )

    elif any(k in p_lower for k in ["practice", "question", "quiz", "drill", "exercise"]):
        if lesson and lesson.get("practice_exercises"):
            ex = lesson["practice_exercises"][0]
            return (
                f"**Practice Challenge: {concept_name}**\n\n"
                f"📝 **Problem:** {ex.get('prompt', '')}\n\n"
                f"🔍 **Hint:** {ex.get('hint', '')}\n\n"
                f"<details><summary>Click to reveal verified solution</summary>\n\n"
                f"**Solution:** {ex.get('solution', '')}\n</details>"
            )
        else:
            return (
                f"To practice verified questions for {course_name}, head to the **Assessments** tab where our "
                f"Bayesian Knowledge Tracing engine dynamically calibrates difficulty to your current mastery!"
            )

    return (
        f"Hello {user.get('full_name', 'Scholar')}! I am **SARVA AI**, your personal learning companion for **{course_name}**.\n\n"
        f"You are currently working on **{concept_name}**. How can I help you right now?\n"
        f"• **Explain this concept** in simple language\n"
        f"• Show me a **practical code example**\n"
        f"• Explain **why an answer was incorrect**\n"
        f"• Give me a **practice exercise**\n"
        f"• **Summarize** key rules and takeaways"
    )


@st.dialog("🎓 SARVA AI Companion Studio", width="large")
def render_sarva_ai_modal(user: dict):
    """
    Renders the large, centered, responsive AI Assistant interface in the centre of the screen.
    Includes dimmed background, full conversational experience, and contextual 'Ask AI Why?' integration.
    """
    user_id = user["id"]
    active_course = get_active_course()
    has_gemini = bool(get_gemini_api_key())

    # Active concept lookup
    active_concepts = get_concepts_by_course(active_course["id"])
    active_concept = active_concepts[0] if active_concepts else None

    # Check for contextual 'Ask AI Why?' mode
    active_ctx = st.session_state.get("sarva_ai_active_context")

    # Header Card
    badge_html = (
        '<span style="background: linear-gradient(135deg, #4338CA 0%, #6366F1 100%); color: #FFFFFF; padding: 4px 12px; border-radius: 12px; font-size: 0.725rem; font-weight: 700; box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);">'
        '✨ Powered by Google Gemini 3.1 Live AI'
        '</span>'
    ) if has_gemini else (
        '<span style="background: #E2E8F0; color: #475569; padding: 4px 12px; border-radius: 12px; font-size: 0.725rem; font-weight: 700;">'
        '📚 Verified Curriculum Engine'
        '</span>'
    )

    st.markdown(
        f'<div style="background: #FFFFFF; border: 1.5px solid #E0E7FF; border-radius: 12px; padding: 0.85rem 1.15rem; margin-bottom: 0.75rem; box-shadow: 0 2px 10px rgba(99, 102, 241, 0.05);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<div style="width: 36px; height: 36px; border-radius: 10px; background: #172943; color: #D6B56D; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; border: 1.5px solid #D6B56D;">SA</div>'
        f'<div>'
        f'<h3 style="font-size: 1.15rem; font-weight: 800; color: #172943; margin: 0; line-height: 1.2;">SARVA AI Companion</h3>'
        f'<p style="font-size: 0.75rem; color: #64748B; margin: 0;">{active_course["name"]} ({active_course.get("subject_name", "General")}) &bull; <em>One Platform. Every Subject. Infinite Knowledge.</em></p>'
        f'</div></div>'
        f'<div>{badge_html}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    # ==========================================================
    # BRANCH 1: CONTEXTUAL "ASK AI WHY?" MODE
    # ==========================================================
    if active_ctx and active_ctx.get("type") == "ask_ai_why":
        q = active_ctx["question"]
        chosen_opt = active_ctx["chosen_opt"]
        options = active_ctx["options"]
        correct_opt = next((o for o in options if o.get("is_correct")), None)
        correct_text = correct_opt.get("text", "") if correct_opt else "Correct Answer"

        m_code = chosen_opt.get("misconception_code")
        m_info = MisconceptionEngine.get_info(m_code)
        m_name = m_info["name"] if m_info else "Cognitive Misconception"

        st.markdown(f"""
        <div style="background: #FDF2F2; border-left: 4px solid #EF4444; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.85rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="font-weight: 700; color: #991B1B; font-size: 0.85rem;">🎯 Context: Question #{q['id']} - {q['title']}</span>
                <span style="font-size: 0.725rem; background: #FFFFFF; border: 1px solid #FECDD3; color: #DC2626; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{m_name}</span>
            </div>
            <div style="font-size: 0.8rem; color: #7F1D1D; line-height: 1.4;">
                <strong>Selected:</strong> <code style="color:#B91C1C;">{chosen_opt.get('text')}</code> (Incorrect) &bull; <strong>Correct:</strong> <code style="color:#15803D;">{correct_text}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cache key for explanation
        cache_key = f"modal_why_{q['id']}_{chosen_opt.get('index', 0)}"
        if cache_key not in st.session_state:
            with st.spinner("🧠 SARVA AI is analyzing your exact answer and formulating your personalized 7-section diagnosis..."):
                explanation = generate_ai_why_explanation(
                    question_title=q["title"],
                    question_prompt=q["prompt"],
                    options=options,
                    selected_answer=chosen_opt.get("text", ""),
                    correct_answer=correct_text,
                    subject_name=active_course.get("subject_name", "General Studies"),
                    course_name=active_course.get("name", "Active Course"),
                    concept_name=q.get("concept_name", "Current Topic"),
                    code_snippet=q.get("code_snippet"),
                    misconception_name=m_name,
                    misconception_explanation=chosen_opt.get("explanation"),
                    base_explanation=q.get("explanation")
                )
                st.session_state[cache_key] = explanation
        else:
            explanation = st.session_state[cache_key]

        # Scrollable Diagnostic Container
        chat_box = st.container(height=380)
        with chat_box:
            st.markdown(explanation, unsafe_allow_html=True)

            # Alternate example card if generated
            alt_key = f"modal_alt_{q['id']}"
            if alt_key in st.session_state:
                st.markdown(f"""
                <div style="background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 0.75rem;">
                    <div style="font-weight: 700; color: #166534; font-size: 0.85rem; margin-bottom: 0.25rem;">💡 Alternative Intuition & Demonstration</div>
                    <div style="color: #14532D; font-size: 0.8rem; line-height: 1.45;">{st.session_state[alt_key]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Followup messages for this question
            fup_key = f"modal_fups_{q['id']}"
            if fup_key in st.session_state:
                for item in st.session_state[fup_key]:
                    st.chat_message("user").write(item["query"])
                    with st.chat_message("assistant", avatar="🎓"):
                        st.markdown(item["response"])

            # Check for pending follow-up doubt
            pending_fup_key = f"modal_fup_pending_{q['id']}"
            pending_fup = st.session_state.pop(pending_fup_key, None)
            if pending_fup:
                st.chat_message("user").write(pending_fup)
                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner("✨ SARVA AI is analyzing your follow-up doubt..."):
                        ans = query_ai_why_followup(
                            user_query=pending_fup,
                            concept_name=q.get("concept_name", "Current Topic"),
                            course_name=active_course.get("name", "Active Course"),
                            question_title=q["title"],
                            selected_answer=chosen_opt.get("text", ""),
                            correct_answer=correct_text
                        )
                        if fup_key not in st.session_state:
                            st.session_state[fup_key] = []
                        st.session_state[fup_key].append({"query": pending_fup, "response": ans})
                    st.markdown(ans)

        # Context Action Controls
        col_c1, col_c2, col_c3 = st.columns([0.35, 0.35, 0.30])
        with col_c1:
            if st.button("🔄 Try Another Example", key="modal_btn_alt_ex", use_container_width=True):
                with st.spinner("Generating alternative analogy..."):
                    alt_res = generate_ai_why_alternate_example(
                        concept_name=q.get("concept_name", "Current Topic"),
                        course_name=active_course.get("name", "Active Course"),
                        question_title=q["title"],
                        misconception_name=m_name
                    )
                    st.session_state[alt_key] = alt_res
                    st.session_state["sarva_ai_dialog_open"] = True
                    st.rerun()
        with col_c2:
            if st.button("💬 General Q&A Mode", key="modal_btn_switch_general", use_container_width=True):
                st.session_state.pop("sarva_ai_active_context", None)
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()
        with col_c3:
            if st.button("Close Assistant", key="modal_btn_close_ctx", type="primary", use_container_width=True):
                st.session_state["sarva_ai_dialog_open"] = False
                st.session_state.pop("sarva_ai_active_context", None)
                st.rerun()

        # Follow-up Input Form (Auto-clears on submit and triggers instant responsive rerun)
        with st.form(key=f"modal_fup_form_{q['id']}", clear_on_submit=True):
            fup_col_in, fup_col_btn = st.columns([0.82, 0.18])
            with fup_col_in:
                fup_query = st.text_input(
                    "Follow-up doubt:",
                    placeholder=f"Ask follow-up doubt about {q.get('concept_name', 'this concept')}...",
                    key=f"modal_fup_in_{q['id']}",
                    label_visibility="collapsed"
                )
            with fup_col_btn:
                fup_submit = st.form_submit_button("Send Doubt", type="primary", use_container_width=True)

            if fup_submit and fup_query.strip():
                st.session_state[f"modal_fup_pending_{q['id']}"] = fup_query.strip()
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()

    # ==========================================================
    # BRANCH 2: GENERAL COMPANION CHAT MODE
    # ==========================================================
    else:
        # Load conversation history
        if "sarva_ai_modal_history" not in st.session_state:
            db_history = get_chat_history(user_id, course_id=active_course.get("id"), limit=25)
            st.session_state["sarva_ai_modal_history"] = [
                {"sender": h["sender"], "message": h["message"], "mode": h.get("mode", "gemini_live")}
                for h in db_history
            ]

        # Quick action chips
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("💡 Explain", key="m_chip_exp", use_container_width=True):
                st.session_state["sarva_ai_modal_pending"] = f"Explain {active_concept['name'] if active_concept else active_course['name']} in simple terms with analogies"
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()
        with c2:
            if st.button("💻 Code Example", key="m_chip_code", use_container_width=True):
                st.session_state["sarva_ai_modal_pending"] = f"Show a practical code demonstration for {active_concept['name'] if active_concept else active_course['name']}"
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()
        with c3:
            if st.button("❓ Diagnose", key="m_chip_diag", use_container_width=True):
                st.session_state["sarva_ai_modal_pending"] = "Diagnose my recent mistakes in this subject and show how to fix them."
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()
        with c4:
            if st.button("🎯 Practice", key="m_chip_quiz", use_container_width=True):
                st.session_state["sarva_ai_modal_pending"] = "Give me a challenging practice question for this topic."
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()

        # Chat container
        chat_container = st.container(height=360)
        with chat_container:
            if not st.session_state["sarva_ai_modal_history"] and not st.session_state.get("sarva_ai_modal_pending"):
                st.markdown(f"""
                <div style="text-align: center; padding: 2.5rem 1rem; color: #94A3B8;">
                    <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🎓</div>
                    <h4 style="color: #172943; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem;">Ask SARVA AI Anything</h4>
                    <p style="font-size: 0.8rem; max-width: 460px; margin: 0 auto; color: #64748B;">
                        Ask for step-by-step mathematical derivations, code syntax breakdowns, debugging help, or deep conceptual intuition.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state["sarva_ai_modal_history"]:
                    if msg["sender"] == "user":
                        st.chat_message("user").write(msg["message"])
                    else:
                        mode_tag = " ✨ *Gemini 3.1 AI*" if msg.get("mode") == "gemini_live" else " 📚 *Curriculum Engine*"
                        with st.chat_message("assistant", avatar="🎓"):
                            st.markdown(msg["message"])
                            st.caption(mode_tag)

            # Check if there is a pending user prompt to process
            pending_query = st.session_state.pop("sarva_ai_modal_pending", None)
            if pending_query:
                # 1. Immediately render user message
                st.chat_message("user").write(pending_query)
                st.session_state["sarva_ai_modal_history"].append({"sender": "user", "message": pending_query, "mode": "user"})
                save_chat_message(user_id, active_course["id"], active_concept["id"] if active_concept else None, "user", pending_query, mode="user")

                # 2. Render assistant response with live spinner inside container
                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner("✨ SARVA AI is formulating your response..."):
                        reply, mode = _handle_assistant_generation(pending_query, user, active_course, active_concept)
                    st.markdown(reply)
                    mode_tag = " ✨ *Gemini 3.1 AI*" if mode == "gemini_live" else " 📚 *Curriculum Engine*"
                    st.caption(mode_tag)

        # Input form (Auto-clears input field immediately upon submission)
        with st.form(key="sarva_ai_modal_form", clear_on_submit=True):
            col_in, col_snd = st.columns([0.82, 0.18])
            with col_in:
                user_msg = st.text_input(
                    "Ask question:",
                    placeholder=f"Ask anything about {active_course['name']}...",
                    key="sarva_ai_modal_input",
                    label_visibility="collapsed"
                )
            with col_snd:
                send_sub = st.form_submit_button("Send", type="primary", use_container_width=True)

            if send_sub and user_msg.strip():
                st.session_state["sarva_ai_modal_pending"] = user_msg.strip()
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()

        # Bottom row: Clear History & Close Assistant
        b1, b2, b3 = st.columns([0.35, 0.35, 0.30])
        with b1:
            if st.button("Clear Conversation", key="modal_clear_btn", use_container_width=True):
                clear_chat_history(user_id, active_course.get("id"))
                st.session_state["sarva_ai_modal_history"] = []
                st.session_state["sarva_ai_page_history"] = []
                st.session_state["sarva_ai_dialog_open"] = True
                st.rerun()
        with b2:
            if st.button("Open Full Studio ↗", key="modal_open_studio_btn", use_container_width=True):
                st.session_state["sarva_ai_dialog_open"] = False
                st.session_state["current_page"] = "sarva_ai_page"
                st.session_state["_synced_page"] = "sarva_ai_page"
                st.rerun()
        with b3:
            if st.button("Close Assistant", key="modal_close_btn", type="primary", use_container_width=True):
                st.session_state["sarva_ai_dialog_open"] = False
                st.session_state.pop("sarva_ai_active_context", None)
                st.rerun()


def _handle_assistant_generation(text: str, user: dict, course: dict, concept: Optional[dict]):
    """Generates assistant response with multi-tier fallback and rewards tracking."""
    user_id = user["id"]
    course_id = course["id"]
    concept_id = concept["id"] if concept else None

    # Lesson summary
    lesson_summary = None
    if concept_id:
        lesson = get_learning_content_by_concept(concept_id)
        if lesson:
            lesson_summary = lesson.get("summary")

    recent_attempts = get_user_attempts(user_id, limit=5, course_id=course_id)
    last_incorrect = next((a for a in recent_attempts if not a.get("is_correct")), None)
    misconception_info = None
    if last_incorrect:
        misconception_info = f"Question: '{last_incorrect.get('question_title')}', Code: {last_incorrect.get('misconception_code')}"

    # Query Gemini
    reply = query_gemini_ai(
        prompt=text,
        course_name=course["name"],
        concept_name=concept["name"] if concept else "General Curriculum",
        lesson_summary=lesson_summary,
        misconception_info=misconception_info
    )
    mode = "gemini_live"

    if not reply:
        reply = _get_curriculum_response(text, user, course, concept)
        mode = "curriculum_engine"

    st.session_state["sarva_ai_modal_history"].append({"sender": "assistant", "message": reply, "mode": mode})
    save_chat_message(user_id, course_id, concept_id, "assistant", reply, mode=mode)

    # Award AI inquiry coins if first time today
    try:
        from core.rewards_engine import RewardsEngine
        RewardsEngine.update_mission_progress(user_id, "ai_activity", 1)
        RewardsEngine.award_coins(
            user_id=user_id,
            amount=5,
            source_activity="ASK_AI_WHY_ENGAGEMENT",
            entity_id=f"ai_chat_{datetime.now().strftime('%Y%m%d')}",
            description="Daily SARVA AI Learning Consultation",
            idempotency_key=f"ai_consult_{user_id}_{datetime.now().strftime('%Y%m%d')}"
        )
    except Exception:
        pass

    return reply, mode


def _process_modal_prompt(text: str, user: dict, course: dict, concept: Optional[dict]):
    """Processes chat prompt inside modal dialog."""
    st.session_state["sarva_ai_modal_pending"] = text
    st.rerun()


def render_sarva_ai_launcher():
    """
    Renders fixed floating launcher on the right-hand side of screen.
    Desktop: Near right-center or bottom-right edge of viewport.
    Mobile: Bottom-right corner respecting screen boundaries.
    """
    st.markdown("""
    <style>
    /* Fixed Floating SARVA AI Launcher */
    div.element-container:has(> div > div > button.sarva-float-btn),
    div[data-testid="stVerticalBlock"] div:has(> button[key="floating_sarva_ai_launcher_btn"]) {
        position: fixed !important;
        bottom: 26px !important;
        right: 26px !important;
        z-index: 999990 !important;
        width: auto !important;
    }
    
    button[key="floating_sarva_ai_launcher_btn"] {
        background: linear-gradient(135deg, #4338CA 0%, #6366F1 50%, #8B5CF6 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #C7D2FE !important;
        border-radius: 50px !important;
        padding: 11px 22px !important;
        font-size: 0.925rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45), 0 0 15px rgba(139, 92, 246, 0.25) !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: pulse-glow-ai 3s infinite ease-in-out !important;
        cursor: pointer !important;
    }
    button[key="floating_sarva_ai_launcher_btn"]:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.6) !important;
    }
    @keyframes pulse-glow-ai {
        0%, 100% { box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45); }
        50% { box-shadow: 0 12px 32px rgba(139, 92, 246, 0.65), 0 0 20px rgba(99, 102, 241, 0.4); }
    }
    @media (max-width: 640px) {
        div[data-testid="stVerticalBlock"] div:has(> button[key="floating_sarva_ai_launcher_btn"]) {
            bottom: 18px !important;
            right: 16px !important;
        }
        button[key="floating_sarva_ai_launcher_btn"] {
            padding: 9px 16px !important;
            font-size: 0.825rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("✨ Ask AI", key="floating_sarva_ai_launcher_btn", use_container_width=False):
        st.session_state["sarva_ai_dialog_open"] = True
        st.session_state.pop("sarva_ai_active_context", None)
        st.rerun()


def render_sarva_ai_widget(user: dict):
    """
    Renders both the floating launcher and (when active) the central modal AI assistant.
    Strictly opens ONLY when the user clicks an AI launcher or 'Ask AI Why?' option.
    """
    if not user:
        return

    # 1. Floating Launcher
    render_sarva_ai_launcher()

    # 2. Central Modal Dialog (Only opens when explicitly triggered by AI button)
    if st.session_state.get("sarva_ai_dialog_open", False):
        # Consume the single-open trigger immediately so subsequent page/option interactions do NOT re-open the dialog!
        st.session_state["sarva_ai_dialog_open"] = False
        render_sarva_ai_modal(user)
