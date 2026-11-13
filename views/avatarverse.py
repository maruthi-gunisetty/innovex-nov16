"""
SARVAVIDYA AVATARVERSE: Premium 10-Level 3D Avatar Store
"Snapchat Bitmoji-inspired 3D cartoon digital identities for students and educators."

Features:
- Exactly 10 Avatar Levels:
  - Levels 1-5: EPIC (Mystic Scholar, Celestial Dreamer, Cyber Sage, Tech Wizard, Quantum Learner)
  - Levels 6-10: LEGENDARY (Shadow Knight, Phoenix Aura, Star Guardian, Royal Enigma, Legendary Ace)
- Native Streamlit image rendering (st.image) for guaranteed cross-platform graphics display
- Try Before Buying: Interactive live preview modal rendering user's equipped profile badge
- Secure Purchase Confirmation before coin deduction
- Equip Avatar functionality with persistent inventory and profile integration
- Both students and faculty supported with independent wallets and collections
"""

import streamlit as st
import os
import base64
from typing import Dict, Any, List, Optional
from core.avatarverse_data import (
    AVATAR_CATALOG, AVATAR_BY_ID, get_user_avatar_state, seed_avatarverse_items
)
from core.rewards_engine import RewardsEngine


def _get_asset_abs_path(rel_path: str) -> str:
    """Returns absolute path to local avatar asset file."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel_path)


def _get_svg_data_uri(rel_path: str) -> str:
    """Reads local SVG asset and encodes into a fast base64 data URI."""
    abs_path = _get_asset_abs_path(rel_path)
    if os.path.exists(abs_path):
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
            b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
        except Exception:
            pass
    return ""


@st.dialog("👁️ Try Before Buying: Live Avatar Preview")
def _show_try_before_buying_modal(avatar: dict, user: dict, wallet: dict):
    """Interactive preview dialog showing how the avatar appears when equipped on user's profile."""
    img_path = _get_asset_abs_path(avatar["asset_rel"])
    tier = avatar["tier"]
    price = avatar["coin_price"]
    level = avatar["level"]

    c1, c2, c3 = st.columns([0.25, 0.5, 0.25])
    with c2:
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)

    tier_emoji = "👑" if tier == "Legendary" else "💜"
    st.markdown(f"<div style='text-align: center; margin-top: 4px;'><strong>{tier_emoji} Level {level} • {tier} Digital Identity</strong><h2 style='margin: 4px 0 6px 0; color: #172943;'>{avatar['name']}</h2><p style='color: #64748B; font-size: 0.9rem;'>{avatar['title']}</p></div>", unsafe_allow_html=True)
    st.write(avatar["description"])

    # Profile Badge Preview Simulation
    with st.container(border=True):
        st.caption("DASHBOARD PROFILE BADGE SIMULATION")
        sim_col1, sim_col2 = st.columns([0.22, 0.78])
        with sim_col1:
            if os.path.exists(img_path):
                st.image(img_path, width=44)
        with sim_col2:
            st.markdown(f"**{user.get('full_name', 'Scholar')}**")
            st.caption(f"Equipped: **{avatar['name']}** • {user.get('role', 'student').capitalize()}")

    can_afford = wallet["available_coins"] >= price
    if avatar.get("is_owned"):
        if avatar.get("is_equipped"):
            st.info("You currently have this avatar equipped on your profile.")
        else:
            if st.button("Equip This Avatar Now ✨", type="primary", use_container_width=True):
                ok, msg = RewardsEngine.equip_item(user["id"], avatar["id"])
                if ok:
                    st.toast(msg, icon="✨")
                    st.rerun()
    else:
        c_buy, c_close = st.columns([1, 1])
        with c_buy:
            if st.button(
                f"Buy Now ({price:,} 🪙)",
                type="primary",
                disabled=not can_afford,
                use_container_width=True
            ):
                st.session_state["confirm_buy_avatar"] = avatar["id"]
                st.rerun()
        with c_close:
            if st.button("Close Preview", use_container_width=True):
                st.session_state.pop("preview_avatar_modal", None)
                st.rerun()


@st.dialog("🪙 Confirm Avatar Purchase")
def _show_purchase_confirmation_modal(avatar: dict, user: dict, wallet: dict):
    """Explicit purchase confirmation ensuring coins are not deducted by accident."""
    user_id = user["id"]
    price = avatar["coin_price"]
    curr_bal = wallet["available_coins"]
    rem_bal = curr_bal - price
    img_path = _get_asset_abs_path(avatar["asset_rel"])

    c1, c2, c3 = st.columns([0.3, 0.4, 0.3])
    with c2:
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)

    st.markdown(f"<div style='text-align: center;'><h3>Unlock {avatar['name']}?</h3><p style='color: #64748B;'>Level {avatar['level']} &bull; {avatar['tier']} 3D Avatar</p></div>", unsafe_allow_html=True)

    with st.container(border=True):
        col_lbl, col_val = st.columns(2)
        with col_lbl:
            st.write("Item Price:")
            st.write("Current Balance:")
            st.write("**Remaining Balance:**")
        with col_val:
            st.markdown(f"**🪙 {price:,} Coins**")
            st.markdown(f"🪙 {curr_bal:,} Coins")
            if rem_bal >= 0:
                st.markdown(f"<span style='color: #16A34A; font-weight: bold;'>🪙 {rem_bal:,} Coins</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #DC2626; font-weight: bold;'>🪙 {rem_bal:,} Coins</span>", unsafe_allow_html=True)

    if curr_bal < price:
        st.error(f"Insufficient coins. You need {price - curr_bal:,} more coins to unlock this avatar.")
        if st.button("Close", use_container_width=True):
            st.session_state.pop("confirm_buy_avatar", None)
            st.rerun()
        return

    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("Confirm Purchase & Unlock", type="primary", use_container_width=True):
            ok, msg = RewardsEngine.redeem_store_item(user_id, avatar["id"])
            st.session_state.pop("confirm_buy_avatar", None)
            if ok:
                RewardsEngine.equip_item(user_id, avatar["id"])
                st.toast(f"🎉 {msg} Equipped automatically!", icon="👑")
                st.rerun()
            else:
                st.error(msg)
    with col_cancel:
        if st.button("Cancel", use_container_width=True):
            st.session_state.pop("confirm_buy_avatar", None)
            st.rerun()


def render_avatarverse_page(user: dict):
    """Main rendering entry point for the SARVAVIDYA AvatarVerse store and collection."""
    user_id = user["id"]
    seed_avatarverse_items()

    # Load user wallet & avatar state
    wallet = RewardsEngine.get_or_create_wallet(user_id)
    avatar_state = get_user_avatar_state(user_id)
    all_avatars = avatar_state["avatars"]
    equipped_avatar = avatar_state["equipped"]
    total_owned = avatar_state["total_owned"]

    # Handle pending confirmation modal
    pending_buy_id = st.session_state.get("confirm_buy_avatar")
    if pending_buy_id and pending_buy_id in AVATAR_BY_ID:
        target_av = next((a for a in all_avatars if a["id"] == pending_buy_id), AVATAR_BY_ID[pending_buy_id])
        _show_purchase_confirmation_modal(target_av, user, wallet)

    # Handle pending preview modal
    pending_preview_id = st.session_state.get("preview_avatar_modal")
    if pending_preview_id and pending_preview_id in AVATAR_BY_ID:
        target_av = next((a for a in all_avatars if a["id"] == pending_preview_id), AVATAR_BY_ID[pending_preview_id])
        _show_try_before_buying_modal(target_av, user, wallet)

    # ==========================================================
    # 1. HERO HEADER: NATIVE STREAMLIT LAYOUT (NO RAW HTML CODE)
    # ==========================================================
    with st.container(border=True):
        col_brand, col_eq_box, col_wal_box = st.columns([1.5, 1.1, 0.7])
        with col_brand:
            st.markdown("### 🎭 SARVAVIDYA AVATARVERSE")
            st.markdown("**10-Level 3D Cartoon Digital Identities**")
            st.caption("Snapchat Bitmoji-inspired 3D avatars for students and faculty. Unlock with verified study coins, preview live, and equip to your profile.")

        with col_eq_box:
            st.caption("EQUIPPED PROFILE AVATAR")
            if equipped_avatar:
                eq_img_path = _get_asset_abs_path(equipped_avatar["asset_rel"])
                c_e1, c_e2 = st.columns([0.35, 0.65])
                with c_e1:
                    if os.path.exists(eq_img_path):
                        st.image(eq_img_path, width=44)
                with c_e2:
                    st.markdown(f"**{equipped_avatar['name']}**")
                    st.caption(f"Level {equipped_avatar['level']} • {equipped_avatar['tier']}")
            else:
                c_e1, c_e2 = st.columns([0.25, 0.75])
                with c_e1:
                    st.markdown("<div style='font-size: 2rem;'>🎓</div>", unsafe_allow_html=True)
                with c_e2:
                    st.markdown("**Default Scholar**")
                    st.caption("Level 0 • Standard")

        with col_wal_box:
            st.caption("WALLET BALANCE")
            st.metric(label="Coins", value=f"🪙 {wallet['available_coins']:,}", label_visibility="collapsed")

    # ==========================================================
    # 2. FILTER TABS (All, Epic, Legendary, My Collection)
    # ==========================================================
    tab_all, tab_epic, tab_legendary, tab_collection = st.tabs([
        "🌟 All Avatars (10)",
        "💜 Epic (Levels 1–5)",
        "👑 Legendary (Levels 6–10)",
        f"🎒 My Collection ({total_owned})"
    ])

    with tab_all:
        _render_avatar_grid(all_avatars, user, wallet, tab_key="all")

    with tab_epic:
        epic_list = [a for a in all_avatars if a["tier"] == "Epic"]
        _render_avatar_grid(epic_list, user, wallet, tab_key="epic")

    with tab_legendary:
        leg_list = [a for a in all_avatars if a["tier"] == "Legendary"]
        _render_avatar_grid(leg_list, user, wallet, tab_key="leg")

    with tab_collection:
        owned_list = [a for a in all_avatars if a.get("is_owned")]
        if not owned_list:
            st.info("You haven't unlocked any avatars yet! Browse the **Epic** and **Legendary** tabs to unlock your first 3D student avatar with earned coins.")
        else:
            _render_avatar_grid(owned_list, user, wallet, tab_key="coll")


def _render_avatar_grid(avatars: List[Dict[str, Any]], user: dict, wallet: dict, tab_key: str):
    """Renders responsive 3-column avatar card grid using native Streamlit containers and images."""
    user_id = user["id"]
    cols_per_row = 3

    for i in range(0, len(avatars), cols_per_row):
        chunk = avatars[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for col, av in zip(cols, chunk):
            with col:
                av_id = av["id"]
                level = av["level"]
                tier = av["tier"]
                price = av["coin_price"]
                is_owned = av.get("is_owned", False)
                is_equipped = av.get("is_equipped", False)
                can_afford = wallet["available_coins"] >= price
                img_path = _get_asset_abs_path(av["asset_rel"])
                is_legendary = (tier == "Legendary")

                # Native Streamlit bordered card container
                with st.container(border=True):
                    # 1. Card Top Badge & Price Header
                    col_tier, col_status = st.columns([0.6, 0.4])
                    with col_tier:
                        tier_badge = "👑 LEGENDARY" if is_legendary else "💜 EPIC"
                        st.caption(f"{tier_badge} • Lvl {level}")
                    with col_status:
                        if is_equipped:
                            st.caption("🟢 **Equipped**")
                        elif is_owned:
                            st.caption("🔵 **Owned**")
                        else:
                            st.markdown(f"**🪙 {price:,}**")

                    # 2. 3D Cartoon Avatar Graphic displayed in actual image format
                    c_sp1, c_img, c_sp2 = st.columns([0.15, 0.7, 0.15])
                    with c_img:
                        if os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)

                    # 3. Avatar Name, Identity Title, and Story Description
                    st.markdown(f"#### {av['name']}")
                    st.caption(f"✨ {av['title']}")
                    st.write(av["description"])

                    # 4. Action Buttons
                    col_prev, col_act = st.columns([0.45, 0.55])
                    with col_prev:
                        if st.button("👁️ Try On", key=f"btn_prev_{tab_key}_{av_id}", use_container_width=True):
                            st.session_state["preview_avatar_modal"] = av_id
                            st.rerun()

                    with col_act:
                        if is_equipped:
                            st.button("Equipped ✓", key=f"btn_eq_done_{tab_key}_{av_id}", disabled=True, use_container_width=True)
                        elif is_owned:
                            if st.button("Equip", key=f"btn_eq_act_{tab_key}_{av_id}", type="primary", use_container_width=True):
                                ok, msg = RewardsEngine.equip_item(user_id, av_id)
                                if ok:
                                    st.toast(f"✨ {msg}", icon="👑")
                                    st.rerun()
                                else:
                                    st.error(msg)
                        else:
                            btn_label = f"Buy ({price} 🪙)"
                            if st.button(
                                btn_label,
                                key=f"btn_buy_act_{tab_key}_{av_id}",
                                type="primary" if can_afford else "secondary",
                                disabled=not can_afford,
                                use_container_width=True
                            ):
                                st.session_state["confirm_buy_avatar"] = av_id
                                st.rerun()

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
