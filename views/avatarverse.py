"""
SARVAVIDYA AVATARVERSE: Premium 10-Level 3D Avatar Store
"Snapchat Bitmoji-inspired 3D cartoon digital identities for students and educators."

Features:
- Exactly 10 Avatar Levels:
  - Levels 1-5: EPIC (Mystic Scholar, Celestial Dreamer, Cyber Sage, Tech Wizard, Quantum Learner)
  - Levels 6-10: LEGENDARY (Shadow Knight, Phoenix Aura, Star Guardian, Royal Enigma, Legendary Ace)
- Deep navy background (#0B132B / #0F172A), royal blue buttons (#2563EB / #3B82F6), subtle gold details (#D6B56D)
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


def _clean_html(html_str: str) -> str:
    """Strips all leading and trailing whitespace per line to strictly prevent CommonMark from rendering HTML as indented code blocks."""
    return "\n".join(line.strip() for line in html_str.strip().splitlines() if line.strip())


def _get_svg_data_uri(rel_path: str) -> str:
    """Reads local SVG asset and encodes into a fast, self-contained base64 data URI."""
    abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel_path)
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
    data_uri = _get_svg_data_uri(avatar["asset_rel"])
    tier_color = "#EAB308" if avatar["tier"] == "Legendary" else "#818CF8"

    modal_html = f"""
    <div style="background: #0B132B; border: 1.5px solid {tier_color}; border-radius: 14px; padding: 1.25rem; color: #FFFFFF; text-align: center; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: center; margin-bottom: 0.75rem;">
            <div style="width: 130px; height: 130px; border-radius: 50%; border: 3px solid {tier_color}; box-shadow: 0 0 20px {tier_color}40; overflow: hidden; background: #0F172A;">
                <img src="{data_uri}" style="width: 100%; height: 100%; object-fit: cover;" alt="{avatar['name']}"/>
            </div>
        </div>
        <div style="font-size: 0.75rem; font-weight: 800; color: {tier_color}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px;">
            Level {avatar['level']} &bull; {avatar['tier']} Digital Identity
        </div>
        <h3 style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; margin: 0 0 0.35rem 0;">
            {avatar['name']}
        </h3>
        <p style="font-size: 0.825rem; color: #94A3B8; max-width: 360px; margin: 0 auto 0.75rem auto; line-height: 1.45;">
            {avatar['description']}
        </p>
        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 0.75rem; margin-top: 0.75rem; text-align: left;">
            <div style="font-size: 0.675rem; color: #D6B56D; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Dashboard Profile Badge Simulation</div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="{data_uri}" style="width: 38px; height: 38px; border-radius: 50%; border: 2px solid {tier_color};" alt="preview"/>
                <div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: #FFFFFF;">{user.get('full_name', 'Scholar')}</div>
                    <div style="font-size: 0.725rem; color: #64748B;">Equipped: <strong style="color: {tier_color};">{avatar['name']}</strong> &bull; {user.get('role', 'student').capitalize()}</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(modal_html), unsafe_allow_html=True)

    can_afford = wallet["available_coins"] >= avatar["coin_price"]
    if avatar.get("is_owned"):
        if avatar.get("is_equipped"):
            st.info("You currently have this avatar equipped.")
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
                f"Buy Now ({avatar['coin_price']} 🪙)",
                type="primary",
                disabled=not can_afford,
                use_container_width=True
            ):
                st.session_state["confirm_buy_avatar"] = avatar["id"]
                st.rerun()
        with c_close:
            if st.button("Close Preview", use_container_width=True):
                st.rerun()


@st.dialog("🪙 Confirm Avatar Purchase")
def _show_purchase_confirmation_modal(avatar: dict, user: dict, wallet: dict):
    """Explicit purchase confirmation ensuring coins are not deducted by accident."""
    user_id = user["id"]
    price = avatar["coin_price"]
    curr_bal = wallet["available_coins"]
    rem_bal = curr_bal - price
    data_uri = _get_svg_data_uri(avatar["asset_rel"])
    tier_color = "#EAB308" if avatar["tier"] == "Legendary" else "#818CF8"

    confirm_html = f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <div style="display: flex; justify-content: center; margin-bottom: 0.75rem;">
            <div style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid {tier_color}; overflow: hidden; background: #0F172A;">
                <img src="{data_uri}" style="width: 100%; height: 100%; object-fit: cover;" alt="{avatar['name']}"/>
            </div>
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 800; color: #172943; margin-bottom: 0.25rem;">
            Unlock {avatar['name']}?
        </h3>
        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.85rem;">
            Level {avatar['level']} &bull; {avatar['tier']} 3D Avatar
        </p>
        <div style="background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 10px; padding: 0.75rem 1rem; text-align: left; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 6px;">
                <span style="color: #64748B;">Item Price:</span>
                <span style="font-weight: 800; color: #D97706;">🪙 {price:,} Coins</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 6px;">
                <span style="color: #64748B;">Current Wallet Balance:</span>
                <span style="font-weight: 700; color: #172943;">🪙 {curr_bal:,} Coins</span>
            </div>
            <hr style="border-color: #E2E8F0; margin: 6px 0;"/>
            <div style="display: flex; justify-content: space-between; font-size: 0.825rem;">
                <span style="font-weight: 700; color: #172943;">Remaining Balance:</span>
                <span style="font-weight: 800; color: {'#16A34A' if rem_bal >= 0 else '#DC2626'};">
                    🪙 {rem_bal:,} Coins
                </span>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(confirm_html), unsafe_allow_html=True)

    if curr_bal < price:
        st.error(f"Insufficient coins. You need {price - curr_bal} more coins to unlock this avatar.")
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
                # Automatically equip new purchase for instant delight
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
    # 1. HERO HEADER: DEEP NAVY, GOLD ACCENTS, ROYAL BLUE BUTTONS
    # ==========================================================
    if equipped_avatar:
        eq_uri = _get_svg_data_uri(equipped_avatar["asset_rel"])
        equipped_img_html = (
            f'<div style="display: flex; align-items: center; gap: 10px; background: rgba(15, 23, 42, 0.65); border: 1.5px solid #D6B56D; border-radius: 12px; padding: 6px 14px;">'
            f'<img src="{eq_uri}" style="width: 38px; height: 38px; border-radius: 50%; border: 2px solid #D6B56D; object-fit: cover;" alt="Equipped"/>'
            f'<div>'
            f'<div style="font-size: 0.65rem; color: #D6B56D; font-weight: 700; text-transform: uppercase;">Equipped Avatar</div>'
            f'<div style="font-size: 0.85rem; font-weight: 800; color: #FFFFFF;">{equipped_avatar["name"]}</div>'
            f'</div>'
            f'</div>'
        )
    else:
        equipped_img_html = (
            f'<div style="display: flex; align-items: center; gap: 8px; background: rgba(15, 23, 42, 0.65); border: 1.5px solid #475569; border-radius: 12px; padding: 6px 14px;">'
            f'<div style="width: 32px; height: 32px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; color: #94A3B8;">🎓</div>'
            f'<div>'
            f'<div style="font-size: 0.65rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Equipped Avatar</div>'
            f'<div style="font-size: 0.825rem; font-weight: 700; color: #CBD5E1;">Default Scholar</div>'
            f'</div>'
            f'</div>'
        )

    hero_html = f"""
    <div style="background: linear-gradient(135deg, #0B132B 0%, #172943 50%, #0F172A 100%); border: 2px solid #D6B56D; border-radius: 16px; padding: 1.35rem 1.75rem; color: #FFFFFF; margin-bottom: 1.25rem; box-shadow: 0 10px 30px rgba(11, 19, 43, 0.25);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.75rem;">🎭</span>
                    <h1 style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: -0.02em;">
                        SARVAVIDYA AVATARVERSE
                    </h1>
                </div>
                <div style="font-size: 0.85rem; color: #D6B56D; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">
                    10-Level 3D Cartoon Digital Identities
                </div>
                <div style="font-size: 0.775rem; color: #94A3B8; margin-top: 4px;">
                    Snapchat Bitmoji-inspired 3D avatars for students and faculty. Unlock with verified study coins, preview live, and equip to your profile.
                </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                {equipped_img_html}
                <div style="background: rgba(214, 181, 109, 0.15); border: 1.5px solid #D6B56D; padding: 8px 16px; border-radius: 12px; text-align: center;">
                    <div style="font-size: 0.65rem; color: #D6B56D; font-weight: 800; text-transform: uppercase;">Wallet Balance</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #F59E0B; display: flex; align-items: center; justify-content: center; gap: 4px;">
                        <span>🪙</span>
                        <span>{wallet['available_coins']:,}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(hero_html), unsafe_allow_html=True)

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
    """Renders responsive 3-column avatar card grid matching the approved styling specifications."""
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
                data_uri = _get_svg_data_uri(av["asset_rel"])

                # Styling colors based on rarity
                is_legendary = (tier == "Legendary")
                card_border = "#D6B56D" if is_legendary else "#818CF8"
                tier_badge_bg = "rgba(214, 181, 109, 0.18)" if is_legendary else "rgba(99, 102, 241, 0.15)"
                tier_badge_color = "#EAB308" if is_legendary else "#818CF8"

                # Status pill in top right
                if is_equipped:
                    status_html = '<span style="background: #10B981; color: #FFFFFF; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 10px;">Equipped ✓</span>'
                elif is_owned:
                    status_html = '<span style="background: #3B82F6; color: #FFFFFF; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 10px;">Owned</span>'
                else:
                    status_html = f'<span style="background: rgba(245, 158, 11, 0.2); border: 1px solid #F59E0B; color: #F59E0B; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 10px;">🪙 {price:,}</span>'

                # Card HTML container (Deep navy background, minimal interface)
                card_html = f"""
                <div style="background: #0F172A; border: 1.5px solid {card_border}; border-radius: 14px; padding: 1.1rem; margin-bottom: 0.85rem; box-shadow: 0 4px 16px rgba(0,0,0,0.25); display: flex; flex-direction: column; justify-content: space-between; min-height: 380px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;">
                            <div style="display: flex; gap: 6px; align-items: center;">
                                <span style="background: {tier_badge_bg}; color: {tier_badge_color}; border: 1px solid {tier_badge_color}; font-size: 0.625rem; font-weight: 800; padding: 1px 7px; border-radius: 6px; text-transform: uppercase;">
                                    {tier}
                                </span>
                                <span style="background: #1E293B; color: #94A3B8; font-size: 0.625rem; font-weight: 700; padding: 1px 6px; border-radius: 6px;">
                                    Level {level}
                                </span>
                            </div>
                            {status_html}
                        </div>
                        <div style="display: flex; justify-content: center; margin: 0.5rem 0 0.75rem 0;">
                            <div style="width: 140px; height: 140px; border-radius: 50%; border: 2.5px solid {card_border}; overflow: hidden; background: #0B132B; box-shadow: 0 6px 18px rgba(0,0,0,0.35); display: flex; align-items: center; justify-content: center;">
                                <img src="{data_uri}" style="width: 100%; height: 100%; object-fit: cover;" alt="{av['name']}"/>
                            </div>
                        </div>
                        <div style="text-align: center; margin-bottom: 0.5rem;">
                            <h4 style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF; margin: 0 0 2px 0;">{av['name']}</h4>
                            <div style="font-size: 0.7rem; color: #D6B56D; font-weight: 600;">{av['title']}</div>
                        </div>
                        <p style="font-size: 0.75rem; color: #94A3B8; line-height: 1.45; text-align: center; margin: 0 0 0.75rem 0; min-height: 48px;">
                            {av['description']}
                        </p>
                    </div>
                </div>
                """
                st.markdown(_clean_html(card_html), unsafe_allow_html=True)

                # Action Controls Row
                col_prev, col_act = st.columns([0.45, 0.55])
                with col_prev:
                    if st.button("👁️ Try On", key=f"btn_prev_{tab_key}_{av_id}", use_container_width=True):
                        st.session_state["preview_avatar_modal"] = av_id
                        st.rerun()

                with col_act:
                    if is_equipped:
                        st.button("Equipped ✓", key=f"btn_eq_done_{tab_key}_{av_id}", disabled=True, use_container_width=True)
                    elif is_owned:
                        if st.button("Equip Avatar", key=f"btn_eq_act_{tab_key}_{av_id}", type="primary", use_container_width=True):
                            ok, msg = RewardsEngine.equip_item(user_id, av_id)
                            if ok:
                                st.toast(f"✨ {msg}", icon="👑")
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        btn_label = f"Buy Now ({price} 🪙)"
                        if st.button(
                            btn_label,
                            key=f"btn_buy_act_{tab_key}_{av_id}",
                            type="primary" if can_afford else "secondary",
                            disabled=not can_afford,
                            use_container_width=True
                        ):
                            st.session_state["confirm_buy_avatar"] = av_id
                            st.rerun()

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
