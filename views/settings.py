"""
LearnSphere AI: Profile and Account Settings
Allows modifying learning preferences, updating security credentials,
and resetting demonstration data for live presentations.
Enterprise educational management aesthetic.
"""

import streamlit as st
from core.auth_service import AuthService
from database.db import (
    get_user_by_id, update_user_preferences, update_user_password
)
from database.seed_data import seed_database


def render_settings_page(user: dict):
    user_id = user["id"]
    current_user = get_user_by_id(user_id) or user

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">SARVAVIDYA Profile & Settings</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Manage personal credentials, adaptive assessment preferences, and system maintenance.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # 1. Profile Overview & Learning Preferences
    with col1:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Learner Profile Details</span>
            </div>
        """, unsafe_allow_html=True)

        st.text_input("Full Name", value=current_user["full_name"], disabled=True)
        st.text_input("Username", value=current_user["username"], disabled=True)
        st.text_input("Email Address", value=current_user["email"], disabled=True)
        st.text_input("Assigned Role", value=current_user["role"].capitalize(), disabled=True)

        st.markdown("<hr style='border-color: #F5F6F8; margin: 0.75rem 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #243B64; margin-bottom: 0.35rem;'>Adaptive Learning Preferences</div>", unsafe_allow_html=True)

        with st.form("pref_form"):
            diff_options = ["adaptive", "beginner", "intermediate", "advanced"]
            current_target = current_user.get("target_difficulty", "adaptive")
            target_diff = st.selectbox(
                "Target Assessment Mode",
                diff_options,
                index=diff_options.index(current_target) if current_target in diff_options else 0,
                format_func=lambda x: f"{x.capitalize()} Engine"
            )
            daily_goal = st.number_input(
                "Daily Question Goal",
                min_value=1,
                max_value=50,
                value=int(current_user.get("daily_goal", 5))
            )
            save_prefs = st.form_submit_button("Update Learning Preferences", type="primary", use_container_width=True)

            if save_prefs:
                update_user_preferences(user_id, target_diff, daily_goal)
                st.session_state["user"]["target_difficulty"] = target_diff
                st.session_state["user"]["daily_goal"] = daily_goal
                st.success("Learning preferences updated successfully.")

        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Security and Demonstration Maintenance
    with col2:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Security & Password Management</span>
            </div>
        """, unsafe_allow_html=True)

        with st.form("password_change_form"):
            current_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            change_pwd_btn = st.form_submit_button("Change Password", use_container_width=True)

            if change_pwd_btn:
                if not AuthService.verify_password(current_pwd, current_user["salt"], current_user["password_hash"]):
                    st.error("Current password verification failed.")
                elif len(new_pwd) < 6:
                    st.error("New password must contain at least 6 characters.")
                elif new_pwd != confirm_pwd:
                    st.error("New passwords do not match.")
                else:
                    new_hash, new_salt = AuthService.hash_password(new_pwd)
                    update_user_password(user_id, new_hash, new_salt)
                    st.session_state["user"]["password_hash"] = new_hash
                    st.session_state["user"]["salt"] = new_salt
                    st.success("Password changed securely.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Demonstration Maintenance Box
        st.markdown("""
        <div class="lm-card" style="border-left: 4px solid #E9AA45;">
            <div class="lm-card-header">
                <span class="lm-card-title">Live Demonstration Maintenance</span>
            </div>
            <p style="color: #718096; font-size: 0.775rem; line-height: 1.45; margin-bottom: 0.75rem;">
                Reset the local SQLite database to pristine demo seed state at any time during a live presentation.
            </p>
        """, unsafe_allow_html=True)

        if st.button("Reset Database to Demonstration State", use_container_width=True):
            seed_database(force=True)
            st.session_state.clear()
            st.success("Demonstration environment reset to pristine baseline.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
