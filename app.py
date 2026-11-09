"""
LearnSphere AI: Main Application Entry Point
Adaptive Intelligence for Personalized Learning and Misconception Detection
"""

import streamlit as st
import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components.styles import CUSTOM_CSS, SIDEBAR_CSS, AUTH_PAGE_CSS
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
from views.subjects_hub import render_subjects_hub_page
from components.sarva_ai import render_sarva_ai_widget


def main():
    # 1. Page Configuration (Strictly no emojis)
    # Automatically collapse sidebar for unauthenticated visitors
    user = st.session_state.get("user")
    initial_sidebar = "expanded" if user else "collapsed"

    favicon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "brand", "favicon.png")
    st.set_page_config(
        page_title="Sarva Vidya – One Platform. Every Subject. Infinite Knowledge.",
        page_icon=favicon_path if os.path.exists(favicon_path) else None,
        layout="wide",
        initial_sidebar_state=initial_sidebar
    )

    # 2. Inject Base SaaS Design System CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 3. Ensure Database and Seed Content Exist
    seed_database(force=False)

    # 4. Handle Redirection State & Query Params
    if "target_view" in st.session_state:
        st.session_state["current_page"] = st.session_state.pop("target_view")
    query_page = st.query_params.get("page")
    if query_page and "current_page" not in st.session_state:
        st.session_state["current_page"] = query_page

    # 5. Global Authentication Gate
    # When user is not authenticated, strictly show only the login portal with sidebar hidden
    if not user:
        st.session_state["current_page"] = "auth"
        st.markdown(AUTH_PAGE_CSS, unsafe_allow_html=True)
        render_auth_page()
        return

    # Authenticated user session
    current_page = st.session_state.get("current_page", "student_dashboard")
    if current_page == "auth":
        current_page = "teacher_dashboard" if user.get("role") == "teacher" else "student_dashboard"
        st.session_state["current_page"] = current_page

    # Role-based access control
    if current_page == "teacher_dashboard" and user.get("role") != "teacher":
        st.warning("Access restricted to faculty members. Redirecting to student dashboard.")
        st.session_state["current_page"] = "student_dashboard"
        st.rerun()

    # 6. Inject Authenticated Sidebar Styling & Render Navigation
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    render_navigation()

    # 6.1 Handle Active Global Search Overlay
    active_search = st.session_state.get("global_search_query", "").strip()
    if active_search:
        render_search_results_view(active_search)
        return

    # 7. Authenticated Route Rendering
    if current_page == "student_dashboard":
        render_student_dashboard(user)
    elif current_page == "teacher_dashboard":
        render_teacher_dashboard(user)
    elif current_page == "subjects":
        render_subjects_hub_page(user)
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
    elif current_page == "settings":
        render_settings_page(user)
    elif current_page == "landing":
        render_landing_page()
    else:
        # Default fallback for student or teacher
        if user.get("role") == "teacher":
            render_teacher_dashboard(user)
        else:
            render_student_dashboard(user)

    # 8. Render Floating SARVA AI Assistant (Subject-Aware, Non-BKT Affecting)
    render_sarva_ai_widget(user)


if __name__ == "__main__":
    main()

