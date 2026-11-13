"""
LearnSphere AI: Profile and Account Settings
Allows modifying learning preferences, updating security credentials,
and resetting demonstration data for live presentations.
Enterprise educational management aesthetic.
"""

import streamlit as st
import os
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
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">Sarva Vidya Profile & Settings</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Manage personal credentials, adaptive assessment preferences, and system maintenance.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # 1. Profile Overview & Learning Preferences
    with col1:
        from database.db import get_user_equipped_avatar
        eq_avatar = get_user_equipped_avatar(user_id)
        if eq_avatar:
            from views.avatarverse import _get_svg_data_uri
            av_uri = _get_svg_data_uri(eq_avatar["asset_rel"])
            av_badge_html = f"""
            <div style="display: flex; align-items: center; gap: 14px; background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 0.85rem 1.15rem; margin-bottom: 0.85rem;">
                <div style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #D6B56D; overflow: hidden; background: #F8FAFC;">
                    <img src="{av_uri}" style="width: 100%; height: 100%; object-fit: cover;" alt="{eq_avatar['name']}"/>
                </div>
                <div>
                    <div style="font-size: 0.65rem; color: #D97706; font-weight: 800; text-transform: uppercase;">Equipped 3D Avatar &bull; Level {eq_avatar['level']}</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #172943;">{eq_avatar['name']}</div>
                    <div style="font-size: 0.725rem; color: #64748B;">{eq_avatar['tier']} Digital Identity</div>
                </div>
            </div>
            """
        else:
            av_badge_html = """
            <div style="display: flex; align-items: center; gap: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.65rem 1rem; margin-bottom: 0.75rem;">
                <div style="width: 44px; height: 44px; border-radius: 50%; background: #E2E8F0; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">🎓</div>
                <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #172943;">Default Scholar Avatar</div>
                    <div style="font-size: 0.7rem; color: #64748B;">Visit the 10-Level AvatarVerse to unlock custom 3D cartoon avatars.</div>
                </div>
            </div>
            """

        st.markdown(f"""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Learner Profile Details</span>
            </div>
            {av_badge_html}
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

        # ==========================================================
        # 3. Firebase Cloud Firestore Integration
        # ==========================================================
        from database.firebase_db import is_firebase_connected, sync_sqlite_to_firestore, get_credentials_path

        fb_connected = is_firebase_connected()
        status_color = "#36A879" if fb_connected else "#D97706"
        status_text = "Connected & Active" if fb_connected else "Setup Required"
        status_bg = "#ECFDF5" if fb_connected else "#FFFBEB"

        st.markdown(f"""
        <div class="lm-card" style="border-left: 4px solid {status_color}; margin-top: 1rem;">
            <div class="lm-card-header">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">🔥</span>
                    <span class="lm-card-title">Firebase Cloud Database</span>
                </div>
                <span style="background: {status_bg}; color: {status_color}; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;">
                    {status_text}
                </span>
            </div>
            <p style="color: #718096; font-size: 0.775rem; line-height: 1.45; margin-bottom: 0.65rem;">
                Connect your Google Firebase Cloud Firestore database to sync student progress, avatars, and coin wallets to the cloud in real time.
            </p>
        """, unsafe_allow_html=True)

        if fb_connected:
            cred_file = os.path.basename(get_credentials_path() or "firebase_credentials.json")
            st.success(f"✓ Connected to Cloud Firestore via `{cred_file}`")
            if st.button("🔄 Sync Local Database to Cloud Firestore", key="btn_sync_firebase", type="primary", use_container_width=True):
                res = sync_sqlite_to_firestore()
                st.toast(f"Synced {res.get('synced_users', 0)} users and {res.get('synced_wallets', 0)} wallets to Firebase Firestore!", icon="🔥")
        else:
            st.info("To connect: Download your service account private key from **Firebase Console > Project Settings > Service Accounts**, then upload it below:")
            uploaded_cred = st.file_uploader("Upload Firebase Service Account Key (JSON)", type=["json"], key="fb_cred_upload")
            if uploaded_cred is not None:
                try:
                    import os
                    content = uploaded_cred.read()
                    cred_target = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "firebase_credentials.json")
                    with open(cred_target, "wb") as f:
                        f.write(content)
                    st.success("Firebase credentials saved! Initializing connection...")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save credentials: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
