"""
LearnSphere AI: Navigation and Header Management
Faithfully reproduces the layout structure and navigation of the reference dashboard:
- Thin horizontal top bar with global search, notification bell, user avatar, and subject/class badge.
- Compact 210px left sidebar with outline icons, active light-blue background, and bottom CTA card.
- Login Portal & Demonstration Credentials in the top right.
Zero emojis, strict professional typography, and seamless session management.
"""

import streamlit as st
from database.db import get_user_by_username, get_user_by_email
from core.auth_service import AuthService
from core.course_manager import get_active_course, render_course_selector
from components.brand import render_sidebar_brand, render_topbar_brand, BRAND_NAME, TAGLINE
from components.styles import get_icon


def render_navigation():
    user = st.session_state.get("user")

    # ==========================================================
    # TOP HORIZONTAL NAVIGATION BAR (Matching Reference)
    # ==========================================================
    col_search, col_user_portal = st.columns([1.6, 1.4])

    with col_search:
        col_logo_mini, col_search_box = st.columns([0.65, 1.35])
        with col_logo_mini:
            render_topbar_brand()
        with col_search_box:
            st.markdown("""
            <div class="lm-search-box">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/></svg>
                <span>Search for concepts, progress, assignments...</span>
            </div>
            """, unsafe_allow_html=True)

    with col_user_portal:
        if user:
            col_notif, col_track, col_u_profile, col_signout = st.columns([0.25, 0.95, 1.35, 0.7])
            with col_notif:
                st.markdown("""
                <div style="display: flex; align-items: center; justify-content: center; padding-top: 0.45rem;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #F5F6F8; display: flex; align-items: center; justify-content: center; color: #718096; border: 1px solid #E4E8ED;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_track:
                active_c = get_active_course()
                st.markdown(f"""
                <div style="display: flex; align-items: center; height: 100%; padding-top: 0.35rem;">
                    <span class="lm-pill pill-ahead" style="font-size: 0.7rem; padding: 3px 8px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{active_c['name']} ({active_c.get('subject_name', '')})">
                        {active_c['subject_name']}: {active_c['name']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_u_profile:
                # User Avatar and Role Label
                role_title = "K-12 Faculty" if user.get("role") == "teacher" else "Student &bull; Level 3"
                initials = "".join([part[0].upper() for part in user["full_name"].split()[:2]])
                st.markdown(f"""
                <div class="lm-user-pill" style="justify-content: flex-end; padding-top: 0.2rem;">
                    <div class="lm-avatar">{initials}</div>
                    <div style="text-align: left; line-height: 1.2;">
                        <div style="font-weight: 600; font-size: 0.825rem; color: #243B64;">{user['full_name']}</div>
                        <div style="font-size: 0.7rem; color: #718096;">{role_title}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_signout:
                if st.button("Sign Out", key="top_signout_action", use_container_width=True, type="secondary"):
                    st.session_state.clear()
                    st.session_state["current_page"] = "landing"
                    st.rerun()

        else:
            # Unauthenticated: Login Portal in Right-Side Top Corner
            col_port_drop, col_port_btn = st.columns([1.5, 1])
            with col_port_drop:
                with st.popover("SARVAVIDYA Evaluation Portal", use_container_width=True):
                    st.markdown("""
                    <div style="margin-bottom: 0.5rem;">
                        <div style="font-weight: 700; font-size: 0.925rem; color: #172943;">SARVAVIDYA Evaluation Credentials</div>
                        <div style="font-size: 0.75rem; color: #718096;">Pre-seeded accounts for academic evaluation:</div>
                    </div>
                    <div style="background-color: #F5F6F8; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.65rem; margin-bottom: 0.75rem; font-size: 0.8rem; line-height: 1.5;">
                        <div style="margin-bottom: 0.4rem; padding-bottom: 0.35rem; border-bottom: 1px solid #E4E8ED;">
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
                    <div style="font-weight: 600; font-size: 0.775rem; margin-bottom: 0.35rem; color: #243B64;">Instant One-Click Sign In:</div>
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

                    st.markdown("<hr style='margin: 0.65rem 0; border-color: #E4E8ED;'>", unsafe_allow_html=True)
                    st.markdown("<div style='font-weight: 600; font-size: 0.775rem; margin-bottom: 0.25rem;'>Standard Credentials Sign In:</div>", unsafe_allow_html=True)
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

    st.markdown("<hr style='border-color: #E4E8ED; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # ==========================================================
    # LEFT COMPACT SIDEBAR (Matching Reference Proportions)
    # ==========================================================
    with st.sidebar:
        # Brand Logo Header matching SARVAVIDYA identity
        render_sidebar_brand()

        if user:
            active_c = get_active_course()
            st.markdown(f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.55rem 0.65rem; margin-bottom: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                    <span style="font-size: 0.65rem; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.04em;">Current Track</span>
                    <span class="lm-pill pill-ahead" style="font-size: 0.625rem; padding: 1px 6px;">{active_c.get('subject_name', 'Programming')}</span>
                </div>
                <div style="font-size: 0.775rem; font-weight: 700; color: #243B64; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {active_c.get('name', 'Python Fundamentals')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Switch Track", expanded=False):
                render_course_selector(key="sidebar_track_selector", label="Select Track", on_change_rerun=True)

            # Navigation Items requested:
            # 1. Dashboard, 2. Assessments, 3. AI Intelligence, 4. Learning Path, 5. Learning Library,
            # 6. Student Progress, 7. Manage Students, 8. Analytics, 9. My Profile, 10. Settings
            if user.get("role") == "student":
                nav_map = {
                    "Dashboard": "student_dashboard",
                    "Assessments": "assessment",
                    "AI Intelligence": "misconceptions",
                    "Learning Path": "learning_path",
                    "Learning Library": "learning_library",
                    "Student Progress": "analytics",
                    "Manage Students": "teacher_dashboard",
                    "Analytics": "analytics",
                    "My Profile": "settings",
                    "Settings": "settings"
                }
            else:
                nav_map = {
                    "Dashboard": "teacher_dashboard",
                    "Assessments": "assessment",
                    "AI Intelligence": "misconceptions",
                    "Learning Path": "learning_path",
                    "Learning Library": "learning_library",
                    "Student Progress": "analytics",
                    "Manage Students": "teacher_dashboard",
                    "Analytics": "analytics",
                    "My Profile": "settings",
                    "Settings": "settings"
                }

            curr = st.session_state.get("current_page", list(nav_map.values())[0])
            curr_label = next((k for k, v in nav_map.items() if v == curr), "Dashboard")
            nav_keys = list(nav_map.keys())
            default_idx = nav_keys.index(curr_label) if curr_label in nav_keys else 0

            selected_nav = st.radio(
                "Navigation",
                nav_keys,
                index=default_idx,
                label_visibility="collapsed",
                key="sidebar_nav_radio"
            )

            # When selection changes, update page
            if nav_map[selected_nav] != st.session_state.get("current_page"):
                st.session_state["current_page"] = nav_map[selected_nav]
                st.rerun()

            # Bottom Sidebar CTA Card (Matching SARVAVIDYA identity)
            st.markdown("""
            <div class="lm-sidebar-cta">
                <div class="lm-sidebar-cta-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                </div>
                <div style="font-weight: 700; font-size: 0.85rem; color: #FFFFFF;">SARVAVIDYA Cohort</div>
                <div style="font-size: 0.7rem; color: #D6B56D; margin-top: 0.2rem; line-height: 1.4;">
                    Collaborate with peer scholars, explore cross-domain topics, and join live study cohorts.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Launch Adaptive Drill", key="sidebar_cta_btn", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "assessment"
                st.rerun()

        else:
            # Unauthenticated Sidebar Info
            st.markdown("""
            <div style="background-color: #FFFFFF; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.85rem; margin-bottom: 0.75rem;">
                <div style="font-weight: 700; font-size: 0.8rem; color: #172943; margin-bottom: 0.25rem;">SARVAVIDYA Credentials</div>
                <div style="font-size: 0.725rem; color: #718096; line-height: 1.5;">
                    Sign in with the top-right portal:<br>
                    &bull; <strong>Student:</strong> <code>student@123</code><br>
                    &bull; <strong>Password:</strong> <code>student123</code><br>
                    &bull; <strong>Faculty:</strong> <code>dr_bennett</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Open Login Portal", key="side_open_auth_btn", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "auth"
                st.rerun()
