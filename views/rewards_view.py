"""
SARVAVIDYA REWARDS: Premium Gamified Learning & Virtual Marketplace View
"Learn. Achieve. Earn. Redeem."
Features:
- Student Coin Wallet (available balance, lifetime earned, lifetime spent, level)
- Level Progression Gauge (Bronze -> Silver -> Gold -> Diamond)
- Daily Missions Hub with live progress bars and atomic reward claim
- Weekly Streak Calendar with milestone bonuses & Streak Freeze shield protection
- In-Platform Reward Store (Avatars, Frames, Themes, Powerups)
- Inventory Management & Immutable Transaction Ledger
"""

import streamlit as st
from datetime import date
from core.rewards_engine import RewardsEngine, REWARD_RULES


def render_rewards_page(user: dict):
    user_id = user["id"]
    today_str = date.today().isoformat()

    # Fetch live rewards dashboard data
    data = RewardsEngine.get_rewards_dashboard_data(user_id)
    wallet = data["wallet"]
    transactions = data["transactions"]
    missions = data["missions"]
    store_items = data["store_items"]
    inventory = data["inventory"]
    streak_days = data["streak_days"]

    # ==========================================================
    # 1. HEADER BANNER: BRAND LOCKUP & WALLET QUICK STATS
    # ==========================================================
    level_color_map = {
        "Diamond Learner": ("#0284C7", "#E0F2FE", "💎"),
        "Gold Learner": ("#D97706", "#FEF3C7", "🥇"),
        "Silver Learner": ("#64748B", "#F1F5F9", "🥈"),
        "Bronze Learner": ("#B45309", "#FFEDD5", "🥉")
    }
    lvl_color, lvl_bg, lvl_icon = level_color_map.get(wallet["current_level"], ("#4338CA", "#EEF2FF", "🎓"))

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #172943 0%, #243B64 50%, #1E1B4B 100%); border: 2px solid #D6B56D; border-radius: 16px; padding: 1.35rem 1.75rem; color: #FFFFFF; margin-bottom: 1.25rem; box-shadow: 0 8px 24px rgba(23, 41, 67, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.6rem;">🪙</span>
                    <h1 style="font-size: 1.65rem; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: -0.02em;">
                        SARVAVIDYA REWARDS
                    </h1>
                </div>
                <div style="font-size: 0.85rem; color: #D6B56D; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">
                    Learn. Achieve. Earn. Redeem.
                </div>
                <div style="font-size: 0.775rem; color: #94A3B8; margin-top: 4px;">
                    Academic mastery unlocks spendable virtual coins. Redeem for custom avatars, profile frames, themes, and study shields.
                </div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <div style="background: {lvl_bg}; border: 1.5px solid {lvl_color}; color: {lvl_color}; padding: 6px 14px; border-radius: 30px; font-weight: 800; font-size: 0.825rem; display: flex; align-items: center; gap: 6px;">
                    <span>{lvl_icon}</span>
                    <span>{wallet['current_level']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # 2. TOP METRIC SUMMARY CARDS
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="lm-card" style="padding: 1rem 1.15rem; margin-bottom: 0.75rem;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Available Balance</div>
            <div style="font-size: 1.65rem; font-weight: 800; color: #D97706; margin: 0.2rem 0; display: flex; align-items: center; gap: 6px;">
                <span>🪙</span>
                <span>{wallet['available_coins']:,}</span>
            </div>
            <div style="font-size: 0.725rem; color: #718096;">Ready to spend in Store</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="lm-card" style="padding: 1rem 1.15rem; margin-bottom: 0.75rem;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Lifetime Earned</div>
            <div style="font-size: 1.65rem; font-weight: 800; color: #172943; margin: 0.2rem 0;">
                {wallet['lifetime_earned_coins']:,}
            </div>
            <div style="font-size: 0.725rem; color: #10B981; font-weight: 600;">Spent: {wallet['lifetime_spent_coins']:,} coins</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="lm-card" style="padding: 1rem 1.15rem; margin-bottom: 0.75rem;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Learning Streak</div>
            <div style="font-size: 1.65rem; font-weight: 800; color: #DC2626; margin: 0.2rem 0; display: flex; align-items: center; gap: 6px;">
                <span>🔥</span>
                <span>{wallet['current_streak']} Days</span>
            </div>
            <div style="font-size: 0.725rem; color: #718096;">Personal Best: {wallet['longest_streak']} days</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="lm-card" style="padding: 1rem 1.15rem; margin-bottom: 0.75rem;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Streak Freeze Shields</div>
            <div style="font-size: 1.65rem; font-weight: 800; color: #0284C7; margin: 0.2rem 0; display: flex; align-items: center; gap: 6px;">
                <span>❄️</span>
                <span>{wallet['streak_freeze_tokens']}</span>
            </div>
            <div style="font-size: 0.725rem; color: #718096;">Protects missed study days</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 3. LEVEL PROGRESSION GAUGE
    # ==========================================================
    next_lvl = wallet.get("next_level_name")
    progress_pct = wallet.get("level_progress_pct", 0.0)
    thresh = wallet.get("next_level_threshold", 700)

    st.markdown(f"""
    <div class="lm-card" style="padding: 0.85rem 1.25rem; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
            <div style="font-weight: 700; font-size: 0.825rem; color: #172943;">
                Tier Progression: <span style="color: #4338CA;">{wallet['current_level']}</span>
                {' → <span style="color: #0284C7;">' + next_lvl + '</span>' if next_lvl else ' (MAX TIER REACHED)'}
            </div>
            <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">
                {wallet['lifetime_earned_coins']} / {thresh} Lifetime Coins ({progress_pct}%)
            </div>
        </div>
        <div class="lm-progress-wrap" style="height: 8px;">
            <div class="lm-progress-bar" style="width: {min(100.0, max(5.0, progress_pct))}%; background: linear-gradient(90deg, #6366F1, #D97706);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # 4. PRIMARY REWARDS TABS
    # ==========================================================
    tab_missions, tab_streak, tab_store, tab_wallet = st.tabs([
        "🎯 Daily Missions",
        "🔥 Streak Calendar & Milestones",
        "🛒 Reward Store (Marketplace)",
        "💼 Wallet & Inventory"
    ])

    # ----------------------------------------------------------
    # TAB 1: DAILY MISSIONS
    # ----------------------------------------------------------
    with tab_missions:
        st.markdown("""
        <div style="margin-bottom: 0.75rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #172943; margin-bottom: 0.2rem;">Today's Learning Missions</h3>
            <p style="font-size: 0.775rem; color: #64748B; margin: 0;">Complete syllabus drills, maintain accuracy, and claim your verified daily coins.</p>
        </div>
        """, unsafe_allow_html=True)

        for m in missions:
            m_id = m["id"]
            curr = m["current_count"]
            target = m["target_count"]
            coins = m["reward_coins"]
            is_comp = bool(m["is_completed"])
            is_claimed = bool(m["is_claimed"])

            pct = min(100, int((curr / target) * 100)) if target > 0 else 100

            col_m_info, col_m_prog, col_m_btn = st.columns([1.6, 1.2, 0.8])
            with col_m_info:
                st.markdown(f"""
                <div style="padding: 4px 0;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: #172943;">{m['title']}</div>
                    <div style="font-size: 0.75rem; color: #64748B;">{m['description']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_m_prog:
                st.markdown(f"""
                <div style="padding: 4px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.725rem; margin-bottom: 2px;">
                        <span style="color: #64748B;">Progress: {curr} / {target}</span>
                        <span style="font-weight: 700; color: #D97706;">+{coins} Coins</span>
                    </div>
                    <div class="lm-progress-wrap" style="height: 6px;">
                        <div class="lm-progress-bar" style="width: {pct}%; background: {'#10B981' if is_comp else '#6366F1'};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_m_btn:
                if is_claimed:
                    st.markdown("""
                    <div style="padding-top: 6px;">
                        <span style="background: #F1F5F9; color: #64748B; padding: 4px 10px; border-radius: 6px; font-size: 0.725rem; font-weight: 700;">
                            ✓ Claimed
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                elif is_comp:
                    if st.button(f"Claim +{coins} 🪙", key=f"btn_claim_m_{m_id}", type="primary", use_container_width=True):
                        ok, msg = RewardsEngine.claim_mission_reward(user_id, m_id)
                        if ok:
                            st.toast(f"🎉 {msg}", icon="🪙")
                            st.rerun()
                        else:
                            st.error(msg)
                else:
                    st.markdown("""
                    <div style="padding-top: 6px;">
                        <span style="background: #F8FAFC; border: 1px solid #E2E8F0; color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 0.725rem; font-weight: 600;">
                            In Progress
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr style='border-color: #F1F5F9; margin: 0.4rem 0;'>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # TAB 2: STREAK CALENDAR & MILESTONES
    # ----------------------------------------------------------
    with tab_streak:
        st.markdown("""
        <div style="margin-bottom: 0.85rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #172943; margin-bottom: 0.2rem;">Weekly Study Calendar</h3>
            <p style="font-size: 0.775rem; color: #64748B; margin: 0;">Complete at least one verified assessment or syllabus activity each day to build your streak.</p>
        </div>
        """, unsafe_allow_html=True)

        # 7-Day Calendar Grid
        cal_cols = st.columns(7)
        for idx, day_info in enumerate(streak_days):
            with cal_cols[idx]:
                border = "#3B82F6" if day_info["is_today"] else ("#10B981" if day_info["is_active"] else "#E2E8F0")
                bg = "#EFF6FF" if day_info["is_today"] else ("#ECFDF5" if day_info["is_active"] else "#FAFAFA")
                icon = "🔥" if day_info["is_active"] else ("📍" if day_info["is_today"] else "⚪")

                st.markdown(f"""
                <div style="background: {bg}; border: 1.5px solid {border}; border-radius: 10px; padding: 0.65rem 0.35rem; text-align: center;">
                    <div style="font-size: 0.7rem; font-weight: 700; color: #64748B;">{day_info['day_name']}</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #172943; margin: 2px 0;">{day_info['day_num']}</div>
                    <div style="font-size: 0.95rem;">{icon}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Streak Milestones
        st.markdown("""
        <h4 style="font-size: 0.95rem; font-weight: 700; color: #172943; margin-bottom: 0.5rem;">Streak Milestone Bonuses</h4>
        """, unsafe_allow_html=True)

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"""
            <div class="lm-card" style="padding: 0.85rem; border-left: 4px solid #F59E0B;">
                <div style="font-weight: 700; font-size: 0.825rem; color: #92400E;">🔥 3-Day Streak</div>
                <div style="font-size: 0.75rem; color: #B45309; margin: 3px 0;">+10 Bonus Coins awarded automatically upon hitting 3 consecutive days.</div>
                <div style="font-size: 0.7rem; font-weight: 700; color: {'#15803D' if wallet['current_streak'] >= 3 else '#64748B'};">
                    {'✓ Reached' if wallet['current_streak'] >= 3 else f'{wallet["current_streak"]}/3 Days'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="lm-card" style="padding: 0.85rem; border-left: 4px solid #10B981;">
                <div style="font-weight: 700; font-size: 0.825rem; color: #065F46;">🏆 7-Day Mastery Streak</div>
                <div style="font-size: 0.75rem; color: #047857; margin: 3px 0;">+30 Bonus Coins + 'Iron Will' achievement profile milestone.</div>
                <div style="font-size: 0.7rem; font-weight: 700; color: {'#15803D' if wallet['current_streak'] >= 7 else '#64748B'};">
                    {'✓ Reached' if wallet['current_streak'] >= 7 else f'{wallet["current_streak"]}/7 Days'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="lm-card" style="padding: 0.85rem; border-left: 4px solid #0284C7;">
                <div style="font-weight: 700; font-size: 0.825rem; color: #075985;">❄️ Streak Freeze Shield</div>
                <div style="font-size: 0.75rem; color: #0369A1; margin: 3px 0;">Have a busy day? Streak Freeze shields automatically protect your active streak.</div>
                <div style="font-size: 0.7rem; font-weight: 700; color: #0284C7;">
                    Active Shields: {wallet['streak_freeze_tokens']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # TAB 3: REWARD STORE (MARKETPLACE)
    # ----------------------------------------------------------
    with tab_store:
        st.markdown("""
        <div style="margin-bottom: 0.85rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #172943; margin-bottom: 0.2rem;">SARVAVIDYA Reward Store</h3>
            <p style="font-size: 0.775rem; color: #64748B; margin: 0;">Redeem your hard-earned academic coins for exclusive avatars, themes, badges, and learning powerups.</p>
        </div>
        """, unsafe_allow_html=True)

        store_filter = st.radio(
            "Category Filter",
            ["All Rewards", "Avatars", "Profile Frames", "Dashboard Themes", "Powerups & Badges"],
            horizontal=True,
            label_visibility="collapsed"
        )

        filter_cat = None
        if store_filter == "Avatars":
            filter_cat = ["avatar"]
        elif store_filter == "Profile Frames":
            filter_cat = ["frame"]
        elif store_filter == "Dashboard Themes":
            filter_cat = ["theme"]
        elif store_filter == "Powerups & Badges":
            filter_cat = ["powerup", "badge"]

        filtered_items = [
            it for it in store_items 
            if not filter_cat or it["category"] in filter_cat
        ]

        # 3-Column Store Grid
        cols_per_row = 3
        for i in range(0, len(filtered_items), cols_per_row):
            row_items = filtered_items[i:i + cols_per_row]
            row_cols = st.columns(cols_per_row)
            for j, item in enumerate(row_items):
                with row_cols[j]:
                    is_owned = bool(item["is_owned"])
                    is_equipped = bool(item["is_equipped"])
                    is_consumable = bool(item["is_consumable"])
                    price = item["coin_price"]
                    can_afford = (wallet["available_coins"] >= price)

                    st.markdown(f"""
                    <div class="lm-card" style="padding: 1rem; margin-bottom: 0.75rem; display: flex; flex-direction: column; justify-content: space-between; min-height: 220px;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <span style="font-size: 2.2rem;">{item['icon']}</span>
                                <span style="background: #FEF3C7; color: #92400E; font-weight: 800; font-size: 0.75rem; padding: 2px 8px; border-radius: 12px; border: 1px solid #FDE68A;">
                                    🪙 {price} Coins
                                </span>
                            </div>
                            <div style="font-weight: 700; font-size: 0.875rem; color: #172943; margin-bottom: 0.2rem;">{item['name']}</div>
                            <div style="font-size: 0.75rem; color: #64748B; line-height: 1.4; margin-bottom: 0.5rem;">{item['description']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if is_owned and not is_consumable:
                        if is_equipped:
                            st.button("Equipped ✓", key=f"btn_eq_{item['id']}", disabled=True, use_container_width=True)
                        else:
                            if st.button("Equip Item", key=f"btn_eq_act_{item['id']}", type="secondary", use_container_width=True):
                                ok, msg = RewardsEngine.equip_item(user_id, item["id"])
                                if ok:
                                    st.toast(msg, icon="✨")
                                    st.rerun()
                                else:
                                    st.error(msg)
                    else:
                        btn_txt = f"Redeem ({price} 🪙)"
                        if is_consumable and is_owned:
                            btn_txt = f"Buy Another ({price} 🪙)"

                        if st.button(
                            btn_txt,
                            key=f"btn_buy_{item['id']}",
                            type="primary" if can_afford else "secondary",
                            disabled=not can_afford,
                            use_container_width=True
                        ):
                            ok, msg = RewardsEngine.redeem_store_item(user_id, item["id"])
                            if ok:
                                st.toast(f"🎉 {msg}", icon="🪙")
                                st.rerun()
                            else:
                                st.error(msg)

    # ----------------------------------------------------------
    # TAB 4: WALLET & INVENTORY
    # ----------------------------------------------------------
    with tab_wallet:
        st.markdown("""
        <div style="margin-bottom: 0.85rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #172943; margin-bottom: 0.2rem;">My Inventory & Ledger</h3>
            <p style="font-size: 0.775rem; color: #64748B; margin: 0;">Equip your unlocked rewards and view your complete, tamper-proof coin transaction history.</p>
        </div>
        """, unsafe_allow_html=True)

        # Inventory Section
        st.markdown("<h4 style='font-size: 0.925rem; font-weight: 700; color: #172943; margin-bottom: 0.5rem;'>Unlocked Inventory Items</h4>", unsafe_allow_html=True)
        if not inventory:
            st.info("You haven't unlocked any store items yet! Earn coins through daily missions and assessment drills to redeem items.")
        else:
            inv_cols = st.columns(4)
            for idx, inv_item in enumerate(inventory):
                with inv_cols[idx % 4]:
                    is_eq = bool(inv_item["is_equipped"])
                    st.markdown(f"""
                    <div class="lm-card" style="padding: 0.75rem; text-align: center; margin-bottom: 0.5rem; border: 1.5px solid {'#6366F1' if is_eq else '#E2E8F0'};">
                        <div style="font-size: 2rem;">{inv_item['icon']}</div>
                        <div style="font-weight: 700; font-size: 0.8rem; color: #172943; margin: 2px 0;">{inv_item['name']}</div>
                        <div style="font-size: 0.7rem; color: #64748B;">{inv_item['category'].capitalize()} &bull; Qty: {inv_item['quantity']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if inv_item["category"] in ["avatar", "frame", "theme"]:
                        if is_eq:
                            st.caption("Active / Equipped")
                        else:
                            if st.button("Equip", key=f"inv_equip_{inv_item['id']}", use_container_width=True):
                                RewardsEngine.equip_item(user_id, inv_item["item_id"])
                                st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Transaction Ledger Table
        st.markdown("<h4 style='font-size: 0.925rem; font-weight: 700; color: #172943; margin-bottom: 0.5rem;'>Coin Transaction Ledger</h4>", unsafe_allow_html=True)
        if not transactions:
            st.caption("No transaction records found yet.")
        else:
            t_header = """
            <table style="width: 100%; border-collapse: collapse; font-size: 0.775rem;">
                <thead>
                    <tr style="border-bottom: 2px solid #E2E8F0; text-align: left; color: #64748B;">
                        <th style="padding: 8px 6px;">Type</th>
                        <th style="padding: 8px 6px;">Description</th>
                        <th style="padding: 8px 6px;">Amount</th>
                        <th style="padding: 8px 6px;">Balance After</th>
                        <th style="padding: 8px 6px;">Date & Time</th>
                    </tr>
                </thead>
                <tbody>
            """
            rows = ""
            for t in transactions:
                t_type = t["transaction_type"]
                amount = t["amount"]
                if t_type in ["EARN", "BONUS"]:
                    amt_str = f"<span style='color: #10B981; font-weight: 700;'>+{amount} 🪙</span>"
                    badge_style = "background: #ECFDF5; color: #047857;"
                elif t_type == "SPEND":
                    amt_str = f"<span style='color: #DC2626; font-weight: 700;'>-{amount} 🪙</span>"
                    badge_style = "background: #FEF2F2; color: #B91C1C;"
                else:
                    amt_str = "<span style='color: #0284C7; font-weight: 700;'>Shield ❄️</span>"
                    badge_style = "background: #F0F9FF; color: #0369A1;"

                rows += f"""
                <tr style="border-bottom: 1px solid #F1F5F9;">
                    <td style="padding: 8px 6px;"><span style="padding: 2px 6px; border-radius: 4px; font-weight: 700; {badge_style}">{t_type}</span></td>
                    <td style="padding: 8px 6px; color: #1E293B; font-weight: 500;">{t['description']}</td>
                    <td style="padding: 8px 6px;">{amt_str}</td>
                    <td style="padding: 8px 6px; font-weight: 700; color: #172943;">{t['balance_after']} 🪙</td>
                    <td style="padding: 8px 6px; color: #94A3B8;">{t['created_at'][:19]}</td>
                </tr>
                """
            t_html = t_header + rows + "</tbody></table>"
            st.markdown(t_html, unsafe_allow_html=True)
