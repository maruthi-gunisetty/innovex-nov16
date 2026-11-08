"""
LearnSphere AI: Navigation System
Coordinates top brand banner, role-aware sidebar navigation, and session termination.
Zero emojis, strict professional typography, and responsive state handling.
"""

import streamlit as st
from components.styles import get_icon


def render_navigation():
    user = st.session_state.get("user")

    # Render top brand bar
    st.markdown("""
    <div class="ls-navbar">
        <div class="ls-brand">
            LearnSphere <span>AI</span>
        </div>
        <div style="font-size: 0.825rem; font-weight: 500; color: #64748b; letter-spacing: 0.02em;">
            Adaptive Intelligence &bull; PS 03
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">LearnSphere AI</div>
            <div style="font-size: 0.75rem; color: #64748b;">Adaptive Education Platform</div>
        </div>
        """, unsafe_allow_html=True)

        if user:
            # Authenticated User Badge
            role_label = user.get("role", "student").capitalize()
            demo_text = " (Demo)" if user.get("is_demo") else ""
            st.markdown(f"""
            <div style="background-color: #f1f5f9; border-radius: 6px; padding: 0.75rem; margin-bottom: 1.25rem;">
                <div style="font-weight: 600; font-size: 0.875rem; color: #0f172a;">{user['full_name']}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Role: {role_label}{demo_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # Role-Specific Navigation Options
            if user.get("role") == "student":
                page_options = {
                    "Dashboard": "student_dashboard",
                    "Adaptive Assessment": "assessment",
                    "Learning Roadmap": "learning_path",
                    "Learning Content Library": "learning_library",
                    "Misconception Diagnostics": "misconceptions",
                    "Performance Analytics": "analytics",
                    "Profile and Settings": "settings"
                }
            elif user.get("role") == "teacher":
                page_options = {
                    "Faculty Dashboard": "teacher_dashboard",
                    "Class Analytics": "analytics",
                    "Profile and Settings": "settings"
                }
            else:
                page_options = {
                    "Dashboard": "student_dashboard",
                    "Settings": "settings"
                }

            # Map current page
            curr = st.session_state.get("current_page", list(page_options.values())[0])
            curr_label = next((k for k, v in page_options.items() if v == curr), list(page_options.keys())[0])

            selected_label = st.radio("Navigation", list(page_options.keys()), index=list(page_options.keys()).index(curr_label))
            st.session_state["current_page"] = page_options[selected_label]

            st.markdown("<hr style='border-color: #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

            if st.button("Sign Out", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.session_state["current_page"] = "landing"
                st.rerun()

        else:
            # Public Navigation Options
            pub_options = {
                "Platform Overview": "landing",
                "Sign In / Register": "auth"
            }
            curr = st.session_state.get("current_page", "landing")
            if curr not in pub_options.values():
                curr = "landing"
            curr_label = next((k for k, v in pub_options.items() if v == curr), "Platform Overview")

            selected_pub = st.radio("Explore", list(pub_options.keys()), index=list(pub_options.keys()).index(curr_label))
            st.session_state["current_page"] = pub_options[selected_pub]

            st.markdown("<hr style='border-color: #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size: 0.8rem; color: #64748b; line-height: 1.5;">
                <strong>Quick Evaluation:</strong><br>
                Navigate to Sign In &rarr; Demonstration Mode to immediately test sample student and faculty personas.
            </div>
            """, unsafe_allow_html=True)
