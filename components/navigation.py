"""
SARVAVIDYA: Retro Quiz Theme Navigation & Header Management
Implements the retro quiz top bar:
- Left: Brand Title "Quiz 🏆" (in bold display font)
- Center: Floating capsule pill navigation (Home, Explore, Leaderboard, AvatarVerse, AI Tutor)
- Right: Diamond/Coin balance badge (💎 20) + User avatar pill & Sign Out
- Synchronized sidebar drawer for advanced management & role features.
"""

import streamlit as st
import os
from database.db import get_user_by_username, get_user_by_email, get_user_equipped_avatar
from core.course_manager import get_active_course, render_course_selector
from components.brand import render_sidebar_brand, render_topbar_brand, BRAND_NAME, TAGLINE
from components.search_view import render_search_input
from components.styles import get_icon


def render_navigation():
    user = st.session_state.get("user")
    current_page = st.session_state.get("current_page", "student_dashboard")

    # If user is not authenticated or currently on login portal, do not render navigation
    if not user or current_page == "auth":
        return

    # Fetch wallet info for compact header display
    u_coins = 0
    u_streak = 0
    try:
        from core.rewards_engine import RewardsEngine
        w = RewardsEngine.get_or_create_wallet(user["id"])
        u_coins = w.get("available_coins", 0)
        u_streak = w.get("current_streak", 0)
    except Exception:
        pass

    # Equipped 3D Cartoon Avatar
    eq_avatar = get_user_equipped_avatar(user["id"])
    avatar_html = ""
    if eq_avatar:
        from views.avatarverse import _get_svg_data_uri
        av_uri = _get_svg_data_uri(eq_avatar["asset_rel"])
        avatar_html = f'<img src="{av_uri}" style="width: 38px; height: 38px; border-radius: 50%; border: 2px solid #FFB800; object-fit: cover; background: #FFF;" title="{eq_avatar["name"]} (Level {eq_avatar["level"]})"/>'
    else:
        initials = "".join([part[0].upper() for part in user.get("full_name", "User").split()[:2]])
        avatar_html = f'<div style="width: 38px; height: 38px; border-radius: 50%; background: #111; color: #FFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; border: 2px solid #E5DFD5;">{initials}</div>'

    # ==========================================================
    # 1. TOP HORIZONTAL NAVIGATION BAR (Matching Reference Screenshot)
    # ==========================================================
    st.markdown("""
    <style>
    .quiz-topbar-wrap {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.25rem 0 1rem 0;
        margin-bottom: 0.5rem;
    }
    .quiz-logo-title {
        font-family: 'Anton', 'Oswald', sans-serif;
        font-size: 2.3rem;
        letter-spacing: -0.01em;
        color: #111111;
        display: flex;
        align-items: center;
        gap: 6px;
        text-decoration: none;
    }
    .quiz-nav-capsule {
        background-color: #FFFFFF;
        border: 1.5px solid #EBE5D8;
        border-radius: 9999px;
        padding: 4px 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    .quiz-diamond-badge {
        background-color: #FFFFFF;
        border: 1.5px solid #EBE5D8;
        border-radius: 9999px;
        padding: 6px 16px;
        font-weight: 800;
        font-size: 0.9rem;
        color: #111111;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    </style>
    """, unsafe_allow_html=True)

    col_brand, col_pills, col_actions = st.columns([1.1, 2.0, 1.4])

    with col_brand:
        st.markdown("""
        <div style="display: flex; align-items: center; height: 100%;">
            <span class="quiz-logo-title">
                Quiz <span style="font-size: 2rem;">🏆</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_pills:
        # Floating Capsule Nav Menu
        col_nav_1, col_nav_2, col_nav_3, col_nav_4, col_nav_5 = st.columns(5)
        
        home_target = "teacher_dashboard" if user.get("role") == "teacher" else "student_dashboard"
        is_home_active = current_page in ("student_dashboard", "teacher_dashboard")
        
        with col_nav_1:
            if st.button("Home", key="top_nav_home", type="primary" if is_home_active else "secondary", use_container_width=True):
                st.session_state["current_page"] = home_target
                st.session_state["_synced_page"] = home_target
                st.rerun()

        with col_nav_2:
            is_explore_active = current_page in ("assessment", "subjects", "learning_library")
            if st.button("Explore", key="top_nav_explore", type="primary" if is_explore_active else "secondary", use_container_width=True):
                st.session_state["current_page"] = "assessment"
                st.session_state["_synced_page"] = "assessment"
                st.rerun()

        with col_nav_3:
            is_lead_active = current_page == "rewards"
            if st.button("Leaderboard", key="top_nav_lead", type="primary" if is_lead_active else "secondary", use_container_width=True):
                st.session_state["current_page"] = "rewards"
                st.session_state["_synced_page"] = "rewards"
                st.rerun()

        with col_nav_4:
            is_av_active = current_page == "avatarverse"
            if st.button("AvatarVerse", key="top_nav_avatar", type="primary" if is_av_active else "secondary", use_container_width=True):
                st.session_state["current_page"] = "avatarverse"
                st.session_state["_synced_page"] = "avatarverse"
                st.rerun()

        with col_nav_5:
            is_ai_active = current_page == "sarva_ai_page"
            if st.button("AI Tutor", key="top_nav_ai", type="primary" if is_ai_active else "secondary", use_container_width=True):
                st.session_state["current_page"] = "sarva_ai_page"
                st.session_state["_synced_page"] = "sarva_ai_page"
                st.rerun()

    with col_actions:
        col_diam, col_user_pic, col_logout = st.columns([1.1, 0.7, 0.9])
        
        with col_diam:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; height: 100%; padding-top: 0.15rem;">
                <span class="quiz-diamond-badge">
                    <span style="color: #06B6D4;">💎</span> {u_coins:,}
                </span>
            </div>
            """, unsafe_allow_html=True)

        with col_user_pic:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                {avatar_html}
            </div>
            """, unsafe_allow_html=True)

        with col_logout:
            if st.button("Sign Out", key="top_quiz_signout", use_container_width=True):
                st.session_state.pop("user", None)
                st.session_state["current_page"] = "auth"
                st.session_state.pop("sidebar_nav_radio", None)
                st.session_state.pop("_active_nav_label", None)
                st.session_state.pop("_synced_page", None)
                st.rerun()

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # ==========================================================
    # 2. RESPONSIVE SIDEBAR DRAWER (Full System Access)
    # ==========================================================
    with st.sidebar:
        render_sidebar_brand()
        
        # Track Indicator
        active_c = get_active_course()
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1.5px solid #EBE5D8; border-radius: 12px; padding: 0.65rem 0.85rem; margin-bottom: 0.65rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                <span style="font-size: 0.65rem; font-weight: 700; color: #718096; text-transform: uppercase;">Active Track</span>
                <span style="background: #FFF1EE; color: #FF5238; font-weight: 700; font-size: 0.625rem; padding: 1px 6px; border-radius: 9999px;">{active_c.get('subject_name', 'Tech')}</span>
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #111111; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {active_c.get('name', 'Python Fundamentals')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Switch Syllabus Track", expanded=False):
            render_course_selector(key="sidebar_track_selector", label="Select Track", on_change_rerun=True)

        # Options Board Items
        if user.get("role") == "teacher":
            nav_map = {
                "Dashboard": "teacher_dashboard",
                "Avatar Store (AvatarVerse)": "avatarverse",
                "SARVAVIDYA Rewards": "rewards",
                "Subjects Hub": "subjects",
                "Assessments": "assessment",
                "SARVA AI Companion": "sarva_ai_page",
                "AI Intelligence": "misconceptions",
                "Learning Path": "learning_path",
                "Learning Library": "learning_library",
                "Student Progress": "analytics",
                "Manage Students": "teacher_dashboard",
                "Analytics": "analytics",
                "My Profile": "settings",
                "Settings": "settings",
                "Sign Out": "auth"
            }
        else:
            nav_map = {
                "Dashboard": "student_dashboard",
                "Avatar Store (AvatarVerse)": "avatarverse",
                "SARVAVIDYA Rewards": "rewards",
                "Subjects Hub": "subjects",
                "Assessments": "assessment",
                "SARVA AI Companion": "sarva_ai_page",
                "AI Intelligence": "misconceptions",
                "Learning Path": "learning_path",
                "Learning Library": "learning_library",
                "Student Progress": "analytics",
                "Analytics": "analytics",
                "My Profile": "settings",
                "Settings": "settings",
                "Sign Out": "auth"
            }

        curr = st.session_state.get("current_page", list(nav_map.values())[0])
        curr_label = next((k for k, v in nav_map.items() if v == curr), "Dashboard")
        nav_keys = list(nav_map.keys())
        default_idx = nav_keys.index(curr_label) if curr_label in nav_keys else 0

        # Sync radio state when current_page changed externally
        if st.session_state.get("_synced_page") != curr:
            st.session_state["_synced_page"] = curr
            st.session_state["sidebar_nav_radio"] = curr_label
            st.session_state["_active_nav_label"] = curr_label

        def _on_nav_change():
            sel = st.session_state.get("sidebar_nav_radio")
            if sel == "Sign Out":
                st.session_state.pop("user", None)
                st.session_state["current_page"] = "auth"
                st.session_state.pop("sidebar_nav_radio", None)
                st.session_state.pop("_active_nav_label", None)
                st.session_state.pop("_synced_page", None)
            elif sel in nav_map:
                tgt = nav_map[sel]
                st.session_state["current_page"] = tgt
                st.session_state["_synced_page"] = tgt
                st.session_state["_active_nav_label"] = sel

        selected_nav = st.radio(
            "Navigation",
            nav_keys,
            index=default_idx,
            label_visibility="collapsed",
            key="sidebar_nav_radio",
            on_change=_on_nav_change
        )
