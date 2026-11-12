"""
SARVAVIDYA: Google Gemini AI Service Integration
Provides real-time conversational intelligence for SARVA AI:
- Authenticates via GEMINI_API_KEY from environment or Streamlit secrets
- Primary model: gemini-3.1-flash-lite (fast, high-quality, high quota)
- Fallback models: gemini-3.8-flash, gemini-3.5-flash
- Injects pedagogical curriculum context (subject, course, module, recent misconceptions)
- Seamlessly falls back to database-backed Curriculum Knowledge Engine if offline or rate-limited
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


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
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    # Context-aware system prompt
    context_prefix = (
        "You are SARVA AI, the intelligent personalized learning companion for the SARVAVIDYA educational ecosystem.\n"
        "Brand tagline: 'One Platform. Every Subject. Infinite Knowledge.'\n"
        f"Active Subject/Course: '{course_name}'\n"
        f"Active Concept/Module: '{concept_name}'\n"
    )
    if lesson_summary:
        context_prefix += f"Module context summary: {lesson_summary}\n"
    if misconception_info:
        context_prefix += f"Student's recent error pattern to remediate: {misconception_info}\n"

    instructions = (
        "\nPedagogical Guidelines:\n"
        "- Explain step-by-step with encouraging, clear language.\n"
        "- Use markdown formatting, bullet points, and code blocks with syntax highlighting where relevant.\n"
        "- If code is asked, give clean, practical, tested syntax.\n"
        "- Keep explanations focused, intuitive, and under 250 words.\n"
    )

    full_prompt = f"{context_prefix}{instructions}\nStudent Question: {prompt}"

    models = ["gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-3.5-flash"]
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800
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
            with urllib.request.urlopen(req, timeout=12) as response:
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

