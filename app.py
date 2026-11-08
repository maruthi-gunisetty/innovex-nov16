"""
LearnSphere AI: Main Application Entry Point
Adaptive Intelligence for Personalized Learning and Misconception Detection
"""

import streamlit as st
import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components.styles import CUSTOM_CSS
from components.navigation import render_navigation
from components.search_view import render_search_results_view
from database.seed_data import seed_database
from views.landing import render_landing_page
from views.auth import render_auth_page
from views.student_dashboard import render_student_dashboard
from views.assessment import render_assessment_page
from views.learning_path import render_learning_path_page
from views.library import render_library_page
from views.misconception_view import render_misconception_page
from views.analytics import render_analytics_page
from views.teacher_dashboard import render_teacher_dashboard
from views.settings import render_settings_page


def main():
    # 1. Page Configuration (Strictly no emojis)
    favicon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "brand", "favicon.png")
    st.set_page_config(
        page_title="Sarva Vidya – One Platform. Every Subject. Infinite Knowledge.",
        page_icon=favicon_path if os.path.exists(favicon_path) else None,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Inject SaaS Design System CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 3. Ensure Database and Seed Content Exist
    seed_database(force=False)

    # 4. Handle Redirection State
    if "target_view" in st.session_state:
        st.session_state["current_page"] = st.session_state.pop("target_view")

    # 5. Render Navigation
    render_navigation()

    # 5.1 Handle Active Global Search Overlay
    active_search = st.session_state.get("global_search_query", "").strip()
    if active_search:
        render_search_results_view(active_search)
        return

    # 6. Current Routing
    current_page = st.session_state.get("current_page", "landing")
    user = st.session_state.get("user")

    # Access Guard: Redirect to auth if attempting to view private page while unauthenticated
    protected_pages = [
        "student_dashboard", "assessment", "learning_path",
        "learning_library", "misconceptions", "analytics",
        "teacher_dashboard", "settings"
    ]
    if current_page in protected_pages and not user:
        st.session_state["current_page"] = "auth"
        render_auth_page()
        return

    # Route Rendering
    if current_page == "landing":
        render_landing_page()
    elif current_page == "auth":
        render_auth_page()
    elif current_page == "student_dashboard":
        render_student_dashboard(user)
    elif current_page == "assessment":
        render_assessment_page(user)
    elif current_page == "learning_path":
        render_learning_path_page(user)
    elif current_page == "learning_library":
        render_library_page(user)
    elif current_page == "misconceptions":
        render_misconception_page(user)
    elif current_page == "analytics":
        render_analytics_page(user)
    elif current_page == "teacher_dashboard":
        render_teacher_dashboard(user)
    elif current_page == "settings":
        render_settings_page(user)
    else:
        render_landing_page()


if __name__ == "__main__":
    main()

