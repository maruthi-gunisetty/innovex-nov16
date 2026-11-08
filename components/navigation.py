"""
LearnSphere AI: Navigation and Header Management
Faithfully reproduces the layout structure and navigation of the reference dashboard:
- Thin horizontal top bar with global search, notification bell, user avatar, and subject/class badge.
- Compact 225px left sidebar with outline icons, active light-blue background, and bottom CTA card.
- Options Board (Dashboard, Assessments, AI Intelligence, Learning Path, Learning Library,
  Student Progress, Manage Students, Analytics, My Profile, Settings) is ALWAYS visible.
Zero emojis, strict professional typography, and seamless session management.
"""

import streamlit as st
from database.db import get_user_by_username, get_user_by_email
from core.auth_service import AuthService
from core.course_manager import get_active_course, render_course_selector
from components.brand import render_sidebar_brand, render_topbar_brand, BRAND_NAME, TAGLINE
from components.search_view import render_search_input
from components.styles import get_icon


def render_navigation():
    user = st.session_state.get("user")
    current_page = st.session_state.get("current_page", "student_dashboard")

    # ==========================================================
    # 1. TOP HORIZONTAL NAVIGATION BAR
    # ==========================================================
    if current_page == "auth":
        # On Login/Auth page: Keep top bar minimal to prevent text merging
        col_logo, col_action = st.columns([2.0, 1.0])
        with col_logo:
            render_topbar_brand()
        with col_action:
            if user:
                col_sp, col_b = st.columns([1.2, 1.0])
                with col_b:
                    if st.button("To Dashboard", key="top_to_dash_btn", use_container_width=True, type="primary"):
                        st.session_state["current_page"] = "teacher_dashboard" if user.get("role") == "teacher" else "student_dashboard"
                        st.rerun()
        st.markdown("<hr style='border-color: #E4E8ED; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    else:
        # Standard Platform Pages Top Bar
        col_search, col_user_portal = st.columns([1.5, 1.5])

        with col_search:
            col_logo_mini, col_search_box = st.columns([0.65, 1.35])
            with col_logo_mini:
                render_topbar_brand()
            with col_search_box:
                render_search_input()

        with col_user_portal:
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
                if user:
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
                else:
                    st.markdown("""
                    <div class="lm-user-pill" style="justify-content: flex-end; padding-top: 0.2rem;">
                        <div class="lm-avatar">SV</div>
                        <div style="text-align: left; line-height: 1.2;">
                            <div style="font-weight: 600; font-size: 0.825rem; color: #243B64;">Demo Learner</div>
                            <div style="font-size: 0.7rem; color: #718096;">Student Access</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            with col_signout:
                if user:
                    if st.button("Sign Out", key="top_signout_action", use_container_width=True, type="secondary"):
                        st.session_state.clear()
                        st.session_state["current_page"] = "auth"
                        st.rerun()
                else:
                    if st.button("Sign In", key="top_signin_portal_nav", use_container_width=True, type="primary"):
                        st.session_state["current_page"] = "auth"
                        st.rerun()

        st.markdown("<hr style='border-color: #E4E8ED; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # ==========================================================
    # 2. LEFT COMPACT SIDEBAR (ALWAYS VISIBLE WITH OPTIONS BOARD)
    # ==========================================================
    with st.sidebar:
        # Brand Logo Header matching SARVAVIDYA identity
        render_sidebar_brand()

        # Track Selector
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

        # Options Board Items:
        # 1. Dashboard, 2. Assessments, 3. AI Intelligence, 4. Learning Path, 5. Learning Library,
        # 6. Student Progress, 7. Manage Students, 8. Analytics, 9. My Profile, 10. Settings
        if user and user.get("role") == "teacher":
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
        else:
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
            target_page = nav_map[selected_nav]
            if not user:
                if target_page == "teacher_dashboard":
                    st.session_state["user"] = get_user_by_email("teacher@123") or get_user_by_username("teacher@123")
                else:
                    st.session_state["user"] = get_user_by_email("student@123") or get_user_by_username("student@123")
            st.session_state["current_page"] = target_page
            st.rerun()

        # Bottom Sidebar CTA Card (Matching Sarva Vidya identity)
        st.markdown("""
        <div class="lm-sidebar-cta">
            <div class="lm-sidebar-cta-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            </div>
            <div style="font-weight: 700; font-size: 0.85rem; color: #FFFFFF;">Sarva Vidya Cohort</div>
            <div style="font-size: 0.7rem; color: #D6B56D; margin-top: 0.2rem; line-height: 1.4;">
                Collaborate with peer scholars, explore cross-domain topics, and join live study cohorts.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Launch Adaptive Drill", key="sidebar_cta_btn", use_container_width=True, type="primary"):
            if not user:
                st.session_state["user"] = get_user_by_email("student@123") or get_user_by_username("student@123")
            st.session_state["current_page"] = "assessment"
            st.rerun()

        if not user:
            st.markdown("""
            <div style="background-color: #FFFFFF; border: 1px solid #E4E8ED; border-radius: 8px; padding: 0.75rem; margin-top: 0.65rem;">
                <div style="font-weight: 700; font-size: 0.775rem; color: #172943; margin-bottom: 0.2rem;">Quick Sign In</div>
                <div style="font-size: 0.7rem; color: #718096; line-height: 1.4;">
                    Student: <code>student@123</code><br>
                    Teacher: <code>teacher@123</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Sign In Portal", key="side_open_auth_btn", use_container_width=True):
                st.session_state["current_page"] = "auth"
                st.rerun()
