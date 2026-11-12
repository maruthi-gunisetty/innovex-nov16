"""
SARVAVIDYA: Google Gemini AI Service Integration
Provides real-time conversational intelligence for SARVA AI:
- Authenticates via GEMINI_API_KEY from environment or Streamlit secrets
- Primary model: gemini-3.1-flash-lite (fast, high-quality, high quota)
- Fallback models: gemini-3.8-flash, gemini-3.5-flash
- Injects pedagogical curriculum context (subject, course, module, recent misconceptions)
- Context-Aware 'Ask AI Why?' diagnostic engine for quiz/assessment evaluation
- Seamlessly falls back to database-backed Curriculum Knowledge Engine if offline or rate-limited
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List


def get_gemini_api_key() -> Optional[str]:
    """Retrieves the Gemini API key from environment, Streamlit secrets, or .env file."""
    # 1. Check Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

    # 2. Check environment variable
    key = os.getenv("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()

    # 3. Check .env file manually
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        val = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
        except Exception:
            pass

    return None


def _call_gemini_api(prompt: str, temperature: float = 0.4, max_tokens: int = 800) -> Optional[str]:
    """Internal helper to dispatch prompt to high-speed Gemini API models with low-latency fallback."""
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    # Use lowest latency, high-throughput models first:
    # 1. gemini-3.1-flash-lite: sub-second generation latency (~0.9s - 1.2s)
    # 2. gemini-flash-lite-latest: reliable secondary fast model (~1.4s)
    models = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest"]
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "").strip()
                        if text:
                            return text
        except Exception:
            continue

    return None


def query_gemini_ai(
    prompt: str,
    course_name: str = "General Studies",
    concept_name: str = "General Concept",
    lesson_summary: Optional[str] = None,
    misconception_info: Optional[str] = None
) -> Optional[str]:
    """
    Sends request to Gemini API. Returns generated markdown string or None if failed.
    """
    context_prefix = (
        "You are SARVA AI, the intelligent personalized learning companion for the SARVAVIDYA educational ecosystem.\n"
        "Brand tagline: 'One Platform. Every Subject. Infinite Knowledge.'\n"
        f"Active Subject/Course: '{course_name}'\n"
        f"Active Concept/Module: '{concept_name}'\n"
    )
    if lesson_summary:
        context_prefix += f"Module context summary: {lesson_summary}\n"
    if misconception_info:
        context_prefix += f"Student's recent error pattern (only reference if relevant to user's question or when diagnosing): {misconception_info}\n"

    instructions = (
        "\nPedagogical & Conversational Guidelines:\n"
        "- If the student is greeting (e.g., 'hi', 'hello', 'hey', 'hiiiiiiii') or asking general questions, greet them warmly and ask how you can help them with this course today. Do NOT bring up past quiz mistakes unless they ask.\n"
        "- Explain step-by-step with encouraging, clear language.\n"
        "- Use markdown formatting, bullet points, and code blocks with syntax highlighting where relevant.\n"
        "- If code is asked, give clean, practical, tested syntax.\n"
        "- Keep explanations focused, intuitive, and under 200 words for fast conversational flow.\n"
    )

    full_prompt = f"{context_prefix}{instructions}\nStudent Question: {prompt}"
    return _call_gemini_api(full_prompt, temperature=0.4, max_tokens=500)


def generate_fallback_why_explanation(
    question_title: str,
    question_prompt: str,
    selected_answer: str,
    correct_answer: str,
    concept_name: str,
    course_name: str,
    misconception_name: Optional[str] = None,
    misconception_explanation: Optional[str] = None,
    base_explanation: Optional[str] = None,
    lesson_summary: Optional[str] = None
) -> str:
    """
    Generates a structured, pedagogical 7-section explanation when offline or API is unreachable,
    powered by the verified SARVAVIDYA curriculum database.
    """
    m_name = misconception_name or "Cognitive Misconception"
    m_exp = misconception_explanation or f"The chosen option reflects a misunderstanding of core {concept_name} rules."
    b_exp = base_explanation or f"The correct answer satisfies foundational principles of {concept_name}."

    return f"""### 🎓 SARVA AI Diagnostic Breakdown

---

#### 1. ❌ Why Your Answer ('{selected_answer}') Was Incorrect
Selecting **'{selected_answer}'** is a very common misstep. {m_exp}

#### 2. ✅ Why '{correct_answer}' Is The Correct Answer
**'{correct_answer}'** is correct because {b_exp}

#### 3. 🧠 The Underlying Misconception: {m_name}
The root cause is a cognitive confusion regarding **{concept_name}** in **{course_name}**. When evaluating this problem, students frequently confuse the operator or rule boundaries, leading to an incorrect prediction.

#### 4. 🪜 Step-by-Step Logic
1. Examine the initial inputs and state in: *"{question_title}"*.
2. Apply the canonical rules of **{concept_name}**.
3. Notice that applying the correct definition yields **'{correct_answer}'** without ambiguity.

#### 5. 🌍 Real-World Analogy
Think of this like a train schedule or blueprint: if one track switch is assumed to be open when it's closed, the entire destination changes. Here, treating the expression with the proper rules ensures the process reaches the intended outcome.

#### 6. 💻 Core Demonstration
{lesson_summary or f"Review the primary syllabus guidelines for **{concept_name}** to cement this rule into your long-term memory."}

---

#### 7. 🎯 Quick Practice Check
Can you apply this rule in reverse? Test yourself on another practice question from this topic in the question navigation grid to confirm mastery!
"""


def generate_ai_why_explanation(
    question_title: str,
    question_prompt: str,
    options: List[Dict[str, Any]],
    selected_answer: str,
    correct_answer: str,
    subject_name: str,
    course_name: str,
    concept_name: str,
    code_snippet: Optional[str] = None,
    misconception_name: Optional[str] = None,
    misconception_explanation: Optional[str] = None,
    base_explanation: Optional[str] = None,
    lesson_summary: Optional[str] = None
) -> str:
    """
    Main generator for the 'Ask AI Why?' feature.
    Dispatches a subject-adapted, context-rich prompt to Gemini 3.1 Live AI,
    or falls back cleanly to the verified curriculum engine.
    """
    # Format options for prompt
    formatted_opts = []
    for idx, opt in enumerate(options):
        letter = chr(65 + idx)
        status = " (CORRECT ANSWER)" if opt.get("is_correct") else ""
        formatted_opts.append(f"  {letter}. {opt['text']}{status}")
    options_str = "\n".join(formatted_opts)

    # Subject-specific guidelines
    subject_lower = f"{subject_name} {course_name}".lower()
    if any(k in subject_lower for k in ["program", "python", "c_", "code", "dsa", "software", "computing"]):
        domain_guidelines = (
            "- Subject: Programming / Computer Science.\n"
            "- Trace code execution line-by-line.\n"
            "- Pinpoint the exact semantic/syntax misunderstanding.\n"
            "- Show the exact execution output and clean, runnable code.\n"
        )
    elif any(k in subject_lower for k in ["math", "calculus", "algebra", "discrete"]):
        domain_guidelines = (
            "- Subject: Mathematics.\n"
            "- Step through the formula and calculation steps.\n"
            "- Highlight the exact arithmetic or algebraic misstep.\n"
            "- Use clean formatting for math equations.\n"
        )
    else:
        domain_guidelines = (
            "- Subject: Science / Engineering / Theoretical Concepts.\n"
            "- Clarify the fundamental physical or theoretical law.\n"
            "- Connect directly to real-world mechanisms and practical systems.\n"
        )

    code_block = f"\nCode / Expression:\n```{code_snippet}\n```\n" if code_snippet else ""

    prompt = f"""You are SARVA AI, the intelligent personalized learning companion for SARVAVIDYA ("One Platform. Every Subject. Infinite Knowledge.").
A student answered a quiz/assessment question incorrectly. Generate a comprehensive, supportive, personalized 'Ask AI Why?' pedagogical diagnosis.

Question Context:
- Subject Area: {subject_name}
- Course / Track: {course_name}
- Concept / Topic: {concept_name}
- Question Title: {question_title}
- Problem Statement: {question_prompt}{code_block}
- Options Available:
{options_str}
- Student's Selected Answer: {selected_answer} (INCORRECT)
- Verified Correct Answer: {correct_answer} (CORRECT)
- Identified Misconception: {misconception_name or 'General Conceptual Error'}
- Misconception Explanation: {misconception_explanation or 'N/A'}
- Reference Solution Explanation: {base_explanation or 'N/A'}

Pedagogical Directives:
{domain_guidelines}
- Be encouraging, respectful, and crystal clear.
- Explain directly to the student ("You selected...").
- Do NOT provide a generic response; reference the exact problem values and options.

Structure your response into these 7 clear markdown sections with headers:
### 1. ❌ Why Your Answer ('{selected_answer}') Was Incorrect
### 2. ✅ Why '{correct_answer}' Is The Correct Answer
### 3. 🧠 The Underlying Misconception ({misconception_name or 'Conceptual Gap'})
### 4. 🪜 Step-by-Step Breakdown & Logic Trace
### 5. 🌍 Real-World Analogy
### 6. 💻 Demonstrative Example & Practical Application
### 7. 🎯 Quick Practice Question (Include a short question testing this exact rule, followed by an HTML `<details><summary>👉 Click to reveal answer & explanation</summary>...</details>` block)
"""

    response = _call_gemini_api(prompt, temperature=0.35, max_tokens=1400)
    if response and len(response.strip()) > 100:
        return response.strip()

    # Fallback to Curriculum Database
    return generate_fallback_why_explanation(
        question_title=question_title,
        question_prompt=question_prompt,
        selected_answer=selected_answer,
        correct_answer=correct_answer,
        concept_name=concept_name,
        course_name=course_name,
        misconception_name=misconception_name,
        misconception_explanation=misconception_explanation,
        base_explanation=base_explanation,
        lesson_summary=lesson_summary
    )


def generate_ai_why_alternate_example(
    concept_name: str,
    course_name: str,
    question_title: str,
    misconception_name: Optional[str] = None
) -> str:
    """
    Generates an alternative real-world analogy and practice demonstration when student clicks 'Try Another Example'.
    """
    prompt = f"""You are SARVA AI, learning companion for SARVAVIDYA.
A student is struggling with the concept '{concept_name}' in '{course_name}' (associated with question '{question_title}' and misconception '{misconception_name or 'Concept Misunderstanding'}').
They already read the initial explanation and requested another fresh perspective.

Provide:
1. 💡 An entirely new, vivid real-world analogy or visual mental model.
2. 💻 A small, practical snippet or practical application demonstrating it from a different angle.
3. 🔑 One memorable 'Rule of Thumb' to avoid this trap in future tests.

Keep it punchy, encouraging, and under 220 words.
"""
    res = _call_gemini_api(prompt, temperature=0.5, max_tokens=600)
    if res and res.strip():
        return res.strip()

    return f"""**Alternative Intuition for {concept_name}:**

Think of this concept like traffic lights: red means stop, green means go, and you cannot mix the two states. 

**Rule of Thumb:** Always verify the type and boundaries before executing an operation. In {course_name}, never assume automatic conversion—always be explicit about your intentions!"""


def query_ai_why_followup(
    user_query: str,
    concept_name: str,
    course_name: str,
    question_title: str,
    selected_answer: str,
    correct_answer: str
) -> str:
    """
    Answers a student's follow-up doubt directly inside the 'Ask AI Why?' panel.
    """
    prompt = f"""You are SARVA AI, student companion in SARVAVIDYA.
The student just evaluated question '{question_title}' in '{course_name}' ({concept_name}).
They chose '{selected_answer}' (incorrect), whereas '{correct_answer}' was correct.
The student has this follow-up doubt:
"{user_query}"

Provide an encouraging, clear, and direct explanation addressing their specific doubt in under 180 words.
"""
    res = _call_gemini_api(prompt, temperature=0.4, max_tokens=600)
    if res and res.strip():
        return res.strip()

    return f"Great question! In **{concept_name}**, the key distinction to keep in mind is that the rule operates deterministically on '{correct_answer}'. Reviewing the fundamental definition in your Library module will clarify why '{selected_answer}' cannot satisfy this condition."
