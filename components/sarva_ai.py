"""
SARVAVIDYA: SARVA AI – Intelligent Learning Assistant
Provides a persistent, floating, subject-aware learning companion:
- Subject & Course Context Awareness (Python, C, Mathematics, DSA, Quantum, etc.)
- Concept explanations, practical code examples, formula step-throughs, and misconception diagnosis
- Transparent AI engine: uses external GenAI when API key is configured, or the built-in
  Verified Curriculum Knowledge Engine directly querying database lessons and question banks.
- Chatting does NOT alter BKT mastery (strictly formative educational support).
"""

import streamlit as st
import os
import json
from typing import Dict, Any, List, Optional
from database.db import (
    get_learning_content_by_concept, get_concepts_by_course,
    get_user_attempts, get_student_concept_mastery,
    save_chat_message, get_chat_history, clear_chat_history
)
from core.course_manager import get_active_course
from core.ai_service import query_gemini_ai, get_gemini_api_key


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

    # Fetch verified lesson content if concept is active
    lesson = None
    if concept_id:
        lesson = get_learning_content_by_concept(concept_id)

    # Fetch recent attempts for misconception context
    recent_attempts = get_user_attempts(user_id, limit=5, course_id=course["id"])
    last_incorrect = next((a for a in recent_attempts if not a.get("is_correct")), None)

    p_lower = prompt.lower().strip()

    # 1. Action: Explain concept / simple terms
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

    # 2. Action: Code / Practical Example
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

    # 3. Action: Why was my answer wrong / Mistakes
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

    # 4. Action: Practice Question / Drill
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

    # 5. Action: Summarize Topic
    elif any(k in p_lower for k in ["summary", "summarize", "recap", "review"]):
        if lesson:
            return (
                f"**Topic Summary: {concept_name}**\n\n"
                f"{lesson.get('summary', '')}\n\n"
                f"⏱️ Estimated Reading Time: {lesson.get('reading_time_min', 15)} minutes.\n\n"
                f"**Core Objectives:**\n" +
                "\n".join([f"1. {obj}" for obj in lesson.get("learning_objectives", [])])
            )
        else:
            return f"**{concept_name} ({course_name}) Summary:** Review fundamental definitions, trace examples, and verify BKT mastery in the Analytics view."

    # Default informative response
    return (
        f"Hello {user.get('full_name', 'Scholar')}! I am **SARVA AI**, your personal learning companion for **{course_name}**.\n\n"
        f"You are currently working on **{concept_name}**. How can I help you right now?\n"
        f"• **Explain this concept** in simple language\n"
        f"• Show me a **practical code example**\n"
        f"• Explain **why an answer was incorrect**\n"
        f"• Give me a **practice exercise**\n"
        f"• **Summarize** key rules and takeaways"
    )


def render_sarva_ai_widget(user: dict):
    """
    Renders the floating bottom-right SARVA AI assistant interface.
    Cleanly docked, supports light/dark themes, and never obstructs page controls.
    """
    if not user:
        return

    user_id = user["id"]
    active_course = get_active_course()

    # Session state initialization
    if "sarva_ai_is_open" not in st.session_state:
        st.session_state["sarva_ai_is_open"] = False
    if "sarva_ai_history" not in st.session_state:
        # Load from database
        db_history = get_chat_history(user_id, course_id=active_course.get("id"), limit=20)
        st.session_state["sarva_ai_history"] = [
            {"sender": h["sender"], "message": h["message"], "mode": h.get("mode", "curriculum_engine")}
            for h in db_history
        ]

    # Look up active concept if selected in assessment or library
    active_concepts = get_concepts_by_course(active_course["id"])
    active_concept = active_concepts[0] if active_concepts else None

    # Clean Sidebar Link directly opening SARVA AI Companion Studio
    with st.sidebar:
        st.markdown("<hr style='border-color: #E4E8ED; margin: 0.75rem 0;'>", unsafe_allow_html=True)
        col_ai_btn, col_ai_txt = st.columns([0.35, 0.65])
        with col_ai_btn:
            if st.button("💬 AI", key="open_sarva_ai_sidebar_btn", use_container_width=True):
                st.session_state["current_page"] = "sarva_ai_page"
                st.session_state["_synced_page"] = "sarva_ai_page"
                st.session_state["sidebar_nav_radio"] = "SARVA AI Companion"
                st.session_state["_active_nav_label"] = "SARVA AI Companion"
                st.rerun()
        with col_ai_txt:
            st.markdown("""
            <div style="line-height: 1.1; padding-top: 2px;">
                <div style="font-weight: 700; font-size: 0.775rem; color: #172943;">SARVA AI</div>
                <div style="font-size: 0.65rem; color: #6366F1; font-weight: 600;">✨ Gemini 3.1 Live</div>
            </div>
            """, unsafe_allow_html=True)


def _handle_chat_input(user_text: str, user: dict, course: dict, concept: Optional[dict]):
    """Processes user input, records message, calls engine, and saves response."""
    user_id = user["id"]
    course_id = course["id"]
    concept_id = concept["id"] if concept else None

    # 1. Save and append user message
    st.session_state["sarva_ai_history"].append({"sender": "user", "message": user_text, "mode": "user"})
    save_chat_message(user_id, course_id, concept_id, "user", user_text, mode="user")

    # 2. Gather lesson & misconception context
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

    # 3. Query Gemini Live AI if key is present
    reply = query_gemini_ai(
        prompt=user_text,
        course_name=course["name"],
        concept_name=concept["name"] if concept else "General Curriculum",
        lesson_summary=lesson_summary,
        misconception_info=misconception_info
    )
    mode = "gemini_live"

    # 4. Fallback to Verified Curriculum Engine if external API fails or is offline
    if not reply:
        reply = _get_curriculum_response(user_text, user, course, concept)
        mode = "curriculum_engine"

    # 5. Save and append assistant message
    st.session_state["sarva_ai_history"].append({"sender": "assistant", "message": reply, "mode": mode})
    save_chat_message(user_id, course_id, concept_id, "assistant", reply, mode=mode)

    st.rerun()

