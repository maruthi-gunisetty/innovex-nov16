"""
LearnSphere AI: Navigation and Header Management
Features a responsive top navbar with Login Portal in the right-side top corner,
fake/demonstration login credentials, and role-based sidebar navigation.
Zero emojis, strict professional typography, and seamless session control.
"""

import streamlit as st
from database.db import get_user_by_username, get_user_by_email
from core.auth_service import AuthService


def render_navigation():
    user = st.session_state.get("user")

    # ==========================================================
    # TOP NAVBAR WITH LOGIN PORTAL IN THE RIGHT SIDE TOP CORNER
    # ==========================================================
    col_nav_brand, col_nav_portal = st.columns([1.6, 1.4])

    with col_nav_brand:
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 0.4rem 0;">
            <div style="font-size: 1.35rem; font-weight: 700; color: #172554; letter-spacing: -0.025em;">
                LearnSphere <span style="color: #635BDB;">AI</span>
            </div>
            <span class="ls-badge badge-violet" style="margin-left: 0.75rem;">
                PS 03 Intelligent Education
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_nav_portal:
        if user:
            # Authenticated Top-Right Status
            col_u_info, col_u_out = st.columns([2, 1])
            with col_u_info:
                role_cap = user.get("role", "student").capitalize()
                demo_label = " (Demo Profile)" if user.get("is_demo") else ""
                st.markdown(f"""
                <div style="text-align: right; padding-top: 0.35rem;">
                    <strong style="color: #0f172a; font-size: 0.9rem;">{user['full_name']}</strong>
                    <div style="font-size: 0.75rem; color: #64748b;">{role_cap}{demo_label}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_u_out:
                if st.button("Sign Out", key="top_signout_action", use_container_width=True, type="secondary"):
                    st.session_state.clear()
                    st.session_state["current_page"] = "landing"
                    st.rerun()

        else:
            # Unauthenticated: Login Portal in Right-Side Top Corner
            col_port_drop, col_port_btn = st.columns([1.5, 1])

            with col_port_drop:
                with st.popover("Login Portal & Fake Credentials", use_container_width=True):
                    st.markdown("""
                    <div style="margin-bottom: 0.5rem;">
                        <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a;">Demonstration Login Credentials</div>
                        <div style="font-size: 0.75rem; color: #64748b;">Use these fake accounts to evaluate the platform:</div>
                    </div>
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.65rem; margin-bottom: 0.75rem; font-size: 0.8rem; line-height: 1.5;">
                        <div style="margin-bottom: 0.4rem; padding-bottom: 0.35rem; border-bottom: 1px solid #f1f5f9;">
                            <strong>Student Credentials:</strong><br>
                            Email / User: <code>student@123</code><br>
                            Password: <code>student123</code>
                        </div>
                        <div style="margin-bottom: 0.35rem;">
                            <strong>Advanced Student:</strong> <code>sophia_chen</code> &bull; Password: <code>student123</code>
                        </div>
                        <div>
                            <strong>Faculty:</strong> <code>dr_bennett</code> &bull; Password: <code>learnsphere123</code>
                        </div>
                    </div>
                    <div style="font-weight: 600; font-size: 0.8rem; margin-bottom: 0.35rem; color: #0f172a;">Instant One-Click Access:</div>
                    """, unsafe_allow_html=True)

                    if st.button("Quick Login as Student (student@123)", key="pop_btn_alex", use_container_width=True, type="primary"):
                        u = get_user_by_email("student@123") or get_user_by_username("student@123")
                        if u:
                            st.session_state["user"] = u
                            st.session_state["current_page"] = "student_dashboard"
                            st.rerun()

                    if st.button("Quick Login as Sophia Chen", key="pop_btn_sophia", use_container_width=True):
                        u = get_user_by_username("sophia_chen")
                        if u:
                            st.session_state["user"] = u
                            st.session_state["current_page"] = "student_dashboard"
                            st.rerun()

                    if st.button("Quick Login as Dr. Sarah Bennett", key="pop_btn_teacher", use_container_width=True):
                        u = get_user_by_username("dr_bennett")
                        if u:
                            st.session_state["user"] = u
                            st.session_state["current_page"] = "teacher_dashboard"
                            st.rerun()

                    st.markdown("<hr style='margin: 0.65rem 0;'>", unsafe_allow_html=True)
                    st.markdown("<div style='font-weight: 600; font-size: 0.8rem; margin-bottom: 0.25rem;'>Standard Credentials Sign In:</div>", unsafe_allow_html=True)
                    quick_u = st.text_input("Username or Email", key="top_quick_u")
                    quick_p = st.text_input("Password", type="password", key="top_quick_p")
                    if st.button("Sign In to Portal", key="top_quick_submit", type="primary", use_container_width=True):
                        u = get_user_by_username(quick_u) or get_user_by_email(quick_u)
                        if u and AuthService.verify_password(quick_p, u["salt"], u["password_hash"]):
                            st.session_state["user"] = u
                            st.session_state["current_page"] = "student_dashboard" if u["role"] == "student" else "teacher_dashboard"
                            st.rerun()
                        else:
                            st.error("Invalid credentials.")

            with col_port_btn:
                if st.button("Sign In Portal", key="top_signin_portal_nav", use_container_width=True, type="primary"):
                    st.session_state["current_page"] = "auth"
                    st.rerun()

    st.markdown("<hr style='border-color: #e2e8f0; margin: 0.75rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # ==========================================================
    # SIDEBAR NAVIGATION
    # ==========================================================
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.25rem 0 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">LearnSphere AI</div>
            <div style="font-size: 0.75rem; color: #64748b;">Adaptive Education Platform</div>
        </div>
        """, unsafe_allow_html=True)

        if user:
            # Authenticated User Badge
            role_label = user.get("role", "student").capitalize()
            demo_text = " (Demo Profile)" if user.get("is_demo") else ""
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

            curr = st.session_state.get("current_page", list(page_options.values())[0])
            curr_label = next((k for k, v in page_options.items() if v == curr), list(page_options.keys())[0])

            selected_label = st.radio("Navigation", list(page_options.keys()), index=list(page_options.keys()).index(curr_label))
            st.session_state["current_page"] = page_options[selected_label]

            st.markdown("<hr style='border-color: #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

            if st.button("Sign Out from Application", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.session_state["current_page"] = "landing"
                st.rerun()

        else:
            # Unauthenticated Sidebar: Clean Info and Fake Credentials (NO 'Platform Overview')
            st.markdown("""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; margin-bottom: 1rem;">
                <div style="font-weight: 600; font-size: 0.85rem; color: #0f172a; margin-bottom: 0.35rem;">Student Login Credentials</div>
                <div style="font-size: 0.75rem; color: #64748b; line-height: 1.5; margin-bottom: 0.75rem;">
                    Sign in using the portal in the right side top corner:
                </div>
                <div style="font-size: 0.75rem; color: #334155; line-height: 1.6;">
                    &bull; <strong>Email:</strong> <code>student@123</code><br>
                    &bull; <strong>Password:</strong> <code>student123</code><br>
                    &bull; <strong>Teacher:</strong> <code>dr_bennett</code> (<code>learnsphere123</code>)
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Open Login Portal", key="side_open_auth_btn", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "auth"
                st.rerun()
