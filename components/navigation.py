"""
SARVAVIDYA: Navigation and Header Management
Provides authenticated platform navigation:
- Sleek horizontal top bar with global search, notifications, user avatar, and Sign Out button.
- Compact 225px left sidebar with SARVAVIDYA brand lockup, active track indicator,
  track switcher, and complete options board (Dashboard, Assessments, AI Intelligence,
  Learning Path, Learning Library, Student Progress, Manage Students, Analytics,
  My Profile, Settings, Sign Out).
- Automatically hidden when visitor is unauthenticated or on the login portal.
"""

import streamlit as st
from database.db import get_user_by_username, get_user_by_email
from core.course_manager import get_active_course, render_course_selector
from components.brand import render_sidebar_brand, render_topbar_brand, BRAND_NAME, TAGLINE
from components.search_view import render_search_input
from components.styles import get_icon


def render_navigation():
    user = st.session_state.get("user")
    current_page = st.session_state.get("current_page", "student_dashboard")

    # If user is not authenticated or currently on the login portal, do not render navigation or sidebar
    if not user or current_page == "auth":
        return

    # ==========================================================
    # 1. TOP HORIZONTAL NAVIGATION BAR (Authenticated View)
    # ==========================================================
    col_search, col_user_portal = st.columns([1.35, 1.65])

    with col_search:
        col_logo_mini, col_search_box = st.columns([0.65, 1.35])
        with col_logo_mini:
            render_topbar_brand()
        with col_search_box:
            render_search_input()

    with col_user_portal:
        col_streak, col_coins, col_track, col_u_profile, col_signout = st.columns([0.48, 0.48, 0.95, 1.15, 0.74])
        
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

        with col_streak:
            st.markdown(f"""
            <div style="display: flex; align-items: center; height: 100%; padding-top: 0.35rem;">
                <span class="lm-pill" style="background:#FEF2F2; color:#DC2626; border:1px solid #FECDD3; font-size: 0.7rem; padding: 3px 8px; font-weight: 700; white-space: nowrap;" title="Current Learning Streak">
                    🔥 {u_streak}d
                </span>
            </div>
            """, unsafe_allow_html=True)

        with col_coins:
            st.markdown(f"""
            <div style="display: flex; align-items: center; height: 100%; padding-top: 0.35rem;">
                <span class="lm-pill" style="background:#FFFBEB; color:#D97706; border:1px solid #FDE68A; font-size: 0.7rem; padding: 3px 8px; font-weight: 700; white-space: nowrap;" title="SARVAVIDYA Coin Balance">
                    🪙 {u_coins:,}
                </span>
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
            role_title = "K-12 Faculty" if user.get("role") == "teacher" else "Student &bull; Level 3"
            initials = "".join([part[0].upper() for part in user.get("full_name", "User").split()[:2]])

            # Check if user has an equipped 3D cartoon avatar
            from database.db import get_user_equipped_avatar
            eq_avatar = get_user_equipped_avatar(user["id"])
            if eq_avatar:
                from views.avatarverse import _get_svg_data_uri
                av_uri = _get_svg_data_uri(eq_avatar["asset_rel"])
                avatar_display_html = f'<img src="{av_uri}" style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid #D6B56D; object-fit: cover;" title="{eq_avatar["name"]} (Level {eq_avatar["level"]})"/>'
            else:
                avatar_display_html = f'<div class="lm-avatar">{initials}</div>'

            user_pill_html = f"""
<div class="lm-user-pill" style="justify-content: flex-end; padding-top: 0.2rem;">
    {avatar_display_html}
    <div style="text-align: left; line-height: 1.2;">
        <div style="font-weight: 600; font-size: 0.825rem; color: #243B64; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 110px;">{user.get('full_name', 'Scholar')}</div>
        <div style="font-size: 0.7rem; color: #718096;">{role_title}</div>
    </div>
</div>
"""
            st.markdown("\n".join(l.strip() for l in user_pill_html.splitlines() if l.strip()), unsafe_allow_html=True)
        with col_signout:
            if st.button("Sign Out", key="top_signout_btn", use_container_width=True):
                st.session_state.pop("user", None)
                st.session_state["current_page"] = "auth"
                st.session_state.pop("sidebar_nav_radio", None)
                st.session_state.pop("_active_nav_label", None)
                st.session_state.pop("_synced_page", None)
                st.rerun()

    st.markdown("<hr style='border-color: #E4E8ED; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # ==========================================================
    # 2. LEFT COMPACT SIDEBAR (AUTHENTICATED ONLY)
    # ==========================================================
    with st.sidebar:
        # Brand Logo Header matching SARVAVIDYA identity
        render_sidebar_brand()

        # Track Indicator
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
            if st.button("Browse All Subjects Hub", key="btn_browse_hub_sidebar", use_container_width=True):
                st.session_state["current_page"] = "subjects"
                st.session_state["_synced_page"] = "subjects"
                st.rerun()

        # Options Board Items
        if user.get("role") == "teacher":
            nav_map = {
                "Dashboard": "teacher_dashboard",
                "Subjects Hub": "subjects",
                "Assessments": "assessment",
                "SARVA AI Companion": "sarva_ai_page",
                "Learning Path": "learning_path",
                "Student Progress": "analytics",
                "Manage Students": "teacher_dashboard",
                "Avatar Store (AvatarVerse)": "avatarverse",
                "SARVAVIDYA Rewards": "rewards",
                "My Profile": "settings",
                "Settings": "settings",
                "Sign Out": "auth"
            }
        else:
            nav_map = {
                "Dashboard": "student_dashboard",
                "Subjects Hub": "subjects",
                "Assessments": "assessment",
                "SARVA AI Companion": "sarva_ai_page",
                "Learning Path": "learning_path",
                "Student Progress": "analytics",
                "Avatar Store (AvatarVerse)": "avatarverse",
                "SARVAVIDYA Rewards": "rewards",
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
