"""
SARVAVIDYA: Admin Portal - AI Configuration & Gemini API Management
Restricted strictly to authenticated administrators.
Provides:
- Gemini API provider status (Active, Inactive, Quota Exceeded, Unconfigured)
- Masked API key display
- Test Connection with minimal safe live ping
- Atomic save of validated replacement key (no restart required)
- Strict error categorization (Invalid key, 403 Forbidden, 429 Quota Exceeded, Network Error)
- Admin-configurable teacher reward rules (Task 5)
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any
from core.ai_service import (
    get_ai_configuration_status, test_gemini_connection,
    save_gemini_api_key, get_gemini_api_key, mask_api_key
)
from core.rewards_engine import RewardsEngine


def render_ai_config_page(user: dict):
    # Strict role verification: only admins permitted
    if not user or user.get("role") != "admin":
        st.error("Access Restricted: This configuration console requires Administrator privileges.")
        st.info("Please log in as an administrator to manage platform AI settings.")
        return

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
        <div>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">Admin Portal &bull; AI Configuration</h2>
            <div style="font-size: 0.775rem; color: #718096; margin-top: 0.15rem;">Manage Google Gemini live API keys, monitor quota telemetry, and configure academic reward parameters.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    status_data = get_ai_configuration_status()
    current_status = status_data["status"]

    # Status Pill Color
    if current_status == "Active":
        stat_color = "#166534"
        stat_bg = "#DCFCE7"
        stat_border = "#86EFAC"
    elif current_status in ("Quota Exceeded", "Invalid Key", "Permission Denied"):
        stat_color = "#991B1B"
        stat_bg = "#FEE2E2"
        stat_border = "#FCA5A5"
    else:
        stat_color = "#92400E"
        stat_bg = "#FEF3C7"
        stat_border = "#FDE68A"

    col_left, col_right = st.columns([1.1, 0.9])

    # ==========================================================
    # 1. LEFT COLUMN: GEMINI API PROVIDER STATUS & KEY REPLACEMENT
    # ==========================================================
    with col_left:
        st.markdown(f"""
        <div class="lm-card" style="margin-bottom: 0.9rem;">
            <div class="lm-card-header">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">✨</span>
                    <span class="lm-card-title">Google Gemini Live AI Provider</span>
                </div>
                <span style="background: {stat_bg}; color: {stat_color}; border: 1px solid {stat_border}; font-size: 0.725rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;">
                    {current_status}
                </span>
            </div>
            <div style="font-size: 0.775rem; color: #64748B; margin-bottom: 0.75rem;">
                Powering SARVA AI multi-turn conversational tutoring and contextual "Ask AI Why?" assessment diagnostics.
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Current Key:** `{status_data['masked_key']}`")
        with c2:
            st.markdown(f"**Models:** `gemini-flash-lite`, `gemini-3.1-flash`")

        # Quota handling alert if quota is exceeded
        if current_status == "Quota Exceeded":
            st.warning("""
            **Quota / Rate Limit Warning (HTTP 429)**  
            Google Gemini reports that the current API key has exhausted its rate limit or free-tier quota.  
            *Note: SARVA AI will automatically fall back to the built-in pedagogical curriculum engine until a valid key with available quota is provided.*
            """)

        st.markdown("<hr style='border-color: #E2E8F0; margin: 0.75rem 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #172943; margin-bottom: 0.4rem;'>Configure Replacement API Key</div>", unsafe_allow_html=True)

        new_key_input = st.text_input(
            "Enter Replacement Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            key="input_new_gemini_key",
            help="Your API key is never committed to Git and is masked across all public interfaces."
        )

        col_test_btn, col_save_btn = st.columns([1, 1])

        # Test Connection button
        test_clicked = False
        with col_test_btn:
            if st.button("🔍 Test Connection", key="btn_test_gemini", type="secondary", use_container_width=True):
                test_clicked = True
                target_key = new_key_input.strip() if new_key_input.strip() else get_gemini_api_key()
                if not target_key:
                    st.error("Please enter an API key to test.")
                else:
                    with st.spinner("Pinging Google Gemini API..."):
                        res = test_gemini_connection(target_key)
                    if res["success"]:
                        st.session_state["gemini_test_success_key"] = target_key
                        st.session_state["gemini_test_result"] = res
                        st.success(f"✓ {res['message']}")
                    else:
                        st.session_state.pop("gemini_test_success_key", None)
                        st.session_state["gemini_test_result"] = res
                        st.error(f"✗ {res['message']}")

        # Save New Key button: enabled when a tested and validated replacement key is ready
        test_valid_key = st.session_state.get("gemini_test_success_key")
        can_save = bool(test_valid_key and new_key_input.strip() and test_valid_key == new_key_input.strip())

        with col_save_btn:
            if st.button(
                "💾 Save New Key",
                key="btn_save_gemini_key",
                type="primary",
                disabled=not can_save,
                use_container_width=True,
                help="Requires successful connection test before saving."
            ):
                ok, msg = save_gemini_api_key(test_valid_key)
                if ok:
                    st.session_state.pop("gemini_test_success_key", None)
                    st.success(f"🎉 {msg}")
                    st.rerun()
                else:
                    st.error(msg)

        if new_key_input.strip() and not can_save and not test_clicked:
            st.caption("ℹ️ Click **Test Connection** to validate this replacement key before saving.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # 2. RIGHT COLUMN: CONNECTION TELEMETRY & SYSTEM CONFIG
    # ==========================================================
    with col_right:
        # Connection Telemetry Card
        st.markdown("""
        <div class="lm-card" style="margin-bottom: 0.9rem;">
            <div class="lm-card-header">
                <span class="lm-card-title">Live Connection Telemetry</span>
            </div>
        """, unsafe_allow_html=True)

        last_test = status_data.get("last_tested") or "Not tested this session"
        last_latency = f"{status_data['last_latency_ms']} ms" if status_data.get("last_latency_ms") else "N/A"
        last_msg = status_data.get("last_message") or "Ready for connection verification."

        st.markdown(f"""
        <table style="width: 100%; font-size: 0.775rem; border-collapse: collapse; margin-bottom: 0.5rem;">
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 6px 0; color: #64748B; font-weight: 600;">Status:</td>
                <td style="padding: 6px 0; text-align: right; font-weight: 700; color: {stat_color};">{current_status}</td>
            </tr>
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 6px 0; color: #64748B; font-weight: 600;">Last Tested:</td>
                <td style="padding: 6px 0; text-align: right; color: #172943;">{last_test}</td>
            </tr>
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 6px 0; color: #64748B; font-weight: 600;">Latency:</td>
                <td style="padding: 6px 0; text-align: right; color: #172943;">{last_latency}</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; color: #64748B; font-weight: 600;">Diagnostics:</td>
                <td style="padding: 6px 0; text-align: right; color: #64748B; font-size: 0.725rem;">{last_msg}</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        # Configurable Teacher Reward Rules (Task 5)
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Faculty Reward Rules Configuration</span>
            </div>
            <p style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.75rem;">
                Administrators can configure the coin incentives awarded for educator activities:
            </p>
        """, unsafe_allow_html=True)

        with st.form("admin_reward_rules_form"):
            curr_publish = RewardsEngine.get_reward_rule_value("TEACHER_RESOURCE_PUBLISH")
            curr_milestone = RewardsEngine.get_reward_rule_value("TEACHER_MILESTONE")

            new_publish = st.number_input(
                "Resource Publication Reward (Coins)",
                min_value=5,
                max_value=200,
                value=int(curr_publish),
                help="Awarded when educator creates or approves curriculum content"
            )
            new_milestone = st.number_input(
                "Teaching Milestone Reward (Coins)",
                min_value=10,
                max_value=500,
                value=int(curr_milestone),
                help="Awarded when educator reaches cohort mastery milestones"
            )

            if st.form_submit_button("Update Faculty Reward Values", type="primary", use_container_width=True):
                RewardsEngine.set_reward_rule_value("TEACHER_RESOURCE_PUBLISH", new_publish)
                RewardsEngine.set_reward_rule_value("TEACHER_MILESTONE", new_milestone)
                st.success("Faculty reward parameters updated successfully.")

        st.markdown("</div>", unsafe_allow_html=True)
