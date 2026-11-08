"""
LearnSphere AI: Profile and Account Settings
Allows modifying learning preferences, updating security credentials,
and resetting demonstration data for live presentations.
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
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0;">
            Account Profile and System Preferences
        </h2>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.25rem;">
            Manage your personal profile, adaptive learning difficulty preferences, and security credentials.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # 1. Profile Overview & Learning Preferences
    with col1:
        st.markdown("""
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Learner Profile Details
            </h4>
        """, unsafe_allow_html=True)

        st.text_input("Full Name", value=current_user["full_name"], disabled=True)
        st.text_input("Username", value=current_user["username"], disabled=True)
        st.text_input("Email Address", value=current_user["email"], disabled=True)
        st.text_input("Assigned Role", value=current_user["role"].capitalize(), disabled=True)

        st.markdown("<hr style='border-color: #f1f5f9; margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #0f172a;'>Learning Preferences</h4>", unsafe_allow_html=True)

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
        <div class="ls-card">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">
                Security and Password Management
            </h4>
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
        <div class="ls-card" style="border-left: 4px solid #d97706;">
            <h4 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.25rem;">
                Live Demonstration Maintenance
            </h4>
            <p style="color: #64748b; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1rem;">
                Reset the local SQLite database to pristine demo seed state at any time during a live hackathon presentation.
            </p>
        """, unsafe_allow_html=True)

        if st.button("Reset Database to Demonstration State", use_container_width=True):
            seed_database(force=True)
            st.session_state.clear()
            st.success("Demonstration environment reset to pristine baseline.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

