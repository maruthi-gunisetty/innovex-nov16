"""
SARVAVIDYA: SARVA AI – Dedicated Learning Companion Studio
Full-page interactive learning environment powered by Google Gemini 3.1 Flash AI:
- Subject & Course Context Awareness (Python, C, Mathematics, DSA, Quantum, etc.)
- Concept explanations, practical code examples, formula step-throughs, and misconception diagnosis
- Live Google Gemini 3.1 Flash integration with instant fallback to Curriculum Knowledge Engine
"""

import streamlit as st
from typing import Optional
from database.db import (
    get_learning_content_by_concept, get_concepts_by_course,
    get_user_attempts, save_chat_message, get_chat_history, clear_chat_history
)
from core.course_manager import get_active_course
from core.ai_service import query_gemini_ai, get_gemini_api_key


def render_sarva_ai_page(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    has_gemini = bool(get_gemini_api_key())

    # Header Card
    badge_html = """
    <span style="background: linear-gradient(135deg, #4338CA 0%, #6366F1 100%); color: #FFFFFF; padding: 5px 14px; border-radius: 12px; font-size: 0.775rem; font-weight: 700; box-shadow: 0 2px 10px rgba(99, 102, 241, 0.35);">
        ✨ Powered by Google Gemini 3.1 Live AI
    </span>
    """ if has_gemini else """
    <span style="background: #E2E8F0; color: #475569; padding: 5px 14px; border-radius: 12px; font-size: 0.775rem; font-weight: 700;">
        Verified Curriculum Engine
    </span>
    """

    header_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E4E8ED; border-radius: 16px; padding: 1.25rem 1.65rem; margin-bottom: 1.25rem; box-shadow: 0 4px 16px rgba(23, 41, 67, 0.04);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: #172943; color: #D6B56D; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; border: 1.5px solid #D6B56D;">SA</div>
            <div>
                <h1 style="font-size: 1.5rem; font-weight: 800; color: #172943; margin: 0; line-height: 1.2;">SARVA AI Companion</h1>
                <p style="font-size: 0.775rem; color: #718096; margin: 0;">Your Intelligent Pedagogical Learning Assistant &bull; <em>One Platform. Every Subject. Infinite Knowledge.</em></p>
            </div>
        </div>
        <div>
            {badge_html}
        </div>
    </div>
</div>
"""
    st.markdown("\n".join(l.strip() for l in header_html.splitlines() if l.strip()), unsafe_allow_html=True)

    # Active concept lookup
    active_concepts = get_concepts_by_course(active_course["id"])
    active_concept = active_concepts[0] if active_concepts else None

    # Load session history
    if "sarva_ai_page_history" not in st.session_state:
        db_history = get_chat_history(user_id, course_id=active_course.get("id"), limit=30)
        st.session_state["sarva_ai_page_history"] = [
            {"sender": h["sender"], "message": h["message"], "mode": h.get("mode", "gemini_live")}
            for h in db_history
        ]

    # Quick Action Chips Row
    st.markdown("<p style='font-size: 0.775rem; font-weight: 700; color: #718096; text-transform: uppercase; margin-bottom: 0.4rem; letter-spacing: 0.04em;'>Quick AI Learning Prompts</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💡 Explain Concept", key="page_chip_explain", use_container_width=True):
            _process_prompt(f"Explain {active_concept['name'] if active_concept else active_course['name']} step-by-step with simple analogies", user, active_course, active_concept)
    with c2:
        if st.button("💻 Practical Code", key="page_chip_code", use_container_width=True):
            _process_prompt(f"Give me a practical tested code example demonstrating {active_concept['name'] if active_concept else active_course['name']}", user, active_course, active_concept)
    with c3:
        if st.button("❓ Diagnose Mistake", key="page_chip_why", use_container_width=True):
            _process_prompt("Why was my previous answer incorrect? Explain the misconception and how to solve it correctly.", user, active_course, active_concept)
    with c4:
        if st.button("🎯 Practice Challenge", key="page_chip_quiz", use_container_width=True):
            _process_prompt("Give me a challenging question to test my understanding of this topic, and don't reveal the answer until I try.", user, active_course, active_concept)

    # Chat Display Container
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state["sarva_ai_page_history"] and not st.session_state.get("sarva_ai_page_pending"):
            empty_html = f"""
<div style="text-align: center; padding: 3.5rem 1rem; color: #94A3B8;">
    <div style="font-size: 2.8rem; margin-bottom: 0.75rem;">🎓</div>
    <h3 style="color: #172943; font-size: 1.2rem; font-weight: 700; margin-bottom: 0.35rem;">Ask SARVA AI Anything</h3>
    <p style="font-size: 0.85rem; max-width: 520px; margin: 0 auto; line-height: 1.5; color: #64748B;">
        Live integration active with <strong>Google Gemini 3.1 Flash AI</strong>. Ask for mathematical derivations, code syntax breakdowns, debugging help, or deep conceptual intuition.
    </p>
</div>
"""
            st.markdown("\n".join(l.strip() for l in empty_html.splitlines() if l.strip()), unsafe_allow_html=True)
        else:
            for msg in st.session_state["sarva_ai_page_history"]:
                if msg["sender"] == "user":
                    st.chat_message("user").write(msg["message"])
                else:
                    mode_tag = " ✨ *Gemini 3.1 AI*" if msg.get("mode") == "gemini_live" else " 📚 *Curriculum Engine*"
                    with st.chat_message("assistant", avatar="🎓"):
                        st.markdown(msg["message"])
                        st.caption(mode_tag)

        # Check for pending user prompt
        pending_page_query = st.session_state.pop("sarva_ai_page_pending", None)
        if pending_page_query:
            # 1. Immediately render user message
            st.chat_message("user").write(pending_page_query)
            st.session_state["sarva_ai_page_history"].append({"sender": "user", "message": pending_page_query, "mode": "user"})
            save_chat_message(user_id, active_course["id"], active_concept["id"] if active_concept else None, "user", pending_page_query, mode="user")

            # 2. Render assistant response with live spinner
            with st.chat_message("assistant", avatar="🎓"):
                with st.spinner("✨ SARVA AI is formulating your response..."):
                    # Gather context
                    lesson_summary = None
                    if active_concept:
                        lesson = get_learning_content_by_concept(active_concept["id"])
                        if lesson:
                            lesson_summary = lesson.get("summary")

                    recent_attempts = get_user_attempts(user_id, limit=5, course_id=active_course["id"])
                    last_incorrect = next((a for a in recent_attempts if not a.get("is_correct")), None)
                    misconception_info = None
                    if last_incorrect:
                        misconception_info = f"Question: '{last_incorrect.get('question_title')}', Code: {last_incorrect.get('misconception_code')}"

                    reply = query_gemini_ai(
                        prompt=pending_page_query,
                        course_name=active_course["name"],
                        concept_name=active_concept["name"] if active_concept else "General Curriculum",
                        lesson_summary=lesson_summary,
                        misconception_info=misconception_info
                    )
                    mode = "gemini_live"

                    if not reply:
                        from components.sarva_ai import _get_curriculum_response
                        reply = _get_curriculum_response(pending_page_query, user, active_course, active_concept)
                        mode = "curriculum_engine"

                st.markdown(reply)
                mode_tag = " ✨ *Gemini 3.1 AI*" if mode == "gemini_live" else " 📚 *Curriculum Engine*"
                st.caption(mode_tag)

                # Save assistant message
                st.session_state["sarva_ai_page_history"].append({"sender": "assistant", "message": reply, "mode": mode})
                save_chat_message(user_id, active_course["id"], active_concept["id"] if active_concept else None, "assistant", reply, mode=mode)

    # Input Controls (Auto-clears typed text immediately on submission)
    with st.form(key="sarva_ai_page_form", clear_on_submit=True):
        inp_col, snd_col = st.columns([0.84, 0.16])
        with inp_col:
            user_input = st.text_input(
                "Ask SARVA AI...",
                placeholder=f"Ask any question about {active_course['name']}...",
                key="sarva_ai_page_text_input",
                label_visibility="collapsed"
            )
        with snd_col:
            send_btn = st.form_submit_button("Send Message", type="primary", use_container_width=True)

        if send_btn and user_input.strip():
            st.session_state["sarva_ai_page_pending"] = user_input.strip()
            st.rerun()

    # Bottom Actions
    b_col1, b_col2 = st.columns([0.22, 0.78])
    with b_col1:
        if st.button("Clear Chat History", key="clear_sarva_page_history_btn", use_container_width=True):
            clear_chat_history(user_id, active_course.get("id"))
            st.session_state["sarva_ai_page_history"] = []
            st.session_state["sarva_ai_history"] = []
            st.rerun()


def _process_prompt(text: str, user: dict, course: dict, concept: Optional[dict]):
    st.session_state["sarva_ai_page_pending"] = text
    st.rerun()

