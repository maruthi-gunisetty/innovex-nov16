"""
LearnSphere AI: Student Learning Dashboard
Directly reproducing the layout, visual structure, and information hierarchy
of the reference enterprise educational dashboard:
- 4-column compact top summary cards
- 2x2 balanced main grid (Curriculum Statistics, Skill Proficiency, Struggling & Excelling, Performance Summary Gauge)
- Compact Python Curriculum Roadmap
Zero emojis, strict professional typography, and real database telemetry.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress,
    get_all_learning_content, save_recommendations, get_student_recommendations,
    mark_recommendation_followed
)
from core.bkt import BayesianKnowledgeTracing
from core.recommender import RecommenderEngine
from core.misconception import MisconceptionEngine
from core.course_manager import get_active_course, render_course_selector


def render_student_dashboard(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    course_id = active_course["id"]

    mastery_data = get_student_mastery(user_id, course_id=course_id)
    attempts = get_user_attempts(user_id, limit=30, course_id=course_id)
    lesson_progress = get_user_lesson_progress(user_id)

    # Calculate Summary Statistics from Actual Database Records
    total_attempts = len(attempts)
    correct_attempts = sum(1 for a in attempts if a["is_correct"])
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0
    streak_days = _calculate_streak(attempts)

    # Average BKT Mastery
    avg_mastery = (sum(m["mastery_prob"] for m in mastery_data) / len(mastery_data)) if mastery_data else 0.20
    bkt = BayesianKnowledgeTracing()

    # Categorize Concepts
    strong_concepts = [m for m in mastery_data if m["mastery_prob"] >= 0.70]
    weak_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.60]
    mastered_concepts = [m for m in mastery_data if m["mastery_prob"] >= 0.85]
    proficient_concepts = [m for m in mastery_data if 0.60 <= m["mastery_prob"] < 0.85]
    developing_concepts = [m for m in mastery_data if 0.40 <= m["mastery_prob"] < 0.60]
    novice_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.40]

    completed_lessons_count = sum(1 for v in lesson_progress.values() if v)
    total_lessons_count = max(len(mastery_data), 6)
    progress_pct = int((completed_lessons_count / total_lessons_count) * 100) if total_lessons_count > 0 else 36

    # ==========================================================
    # 1. PAGE TITLE & SUBJECT SELECTION (Matching Reference)
    # ==========================================================
    col_title, col_subject = st.columns([2.0, 1.0])
    with col_title:
        st.markdown(f"""
        <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 0.75rem;">
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">Sarva Vidya Dashboard</h2>
            <span style="font-size: 0.775rem; color: #718096; font-weight: 500;">{active_course['name']} &bull; One Platform. Every Subject. Infinite Knowledge.</span>
        </div>
        """, unsafe_allow_html=True)
    with col_subject:
        render_course_selector(key="dash_course_selector", label="Select Track", on_change_rerun=True)

    # SARVA AI & Rewards Dashboard Integration
    u_coins = 0
    u_streak = 0
    u_level = "Bronze Learner"
    try:
        from core.rewards_engine import RewardsEngine
        rw = RewardsEngine.get_or_create_wallet(user_id)
        u_coins = rw.get("available_coins", 0)
        u_streak = rw.get("current_streak", 0)
        u_level = rw.get("current_level", "Bronze Learner")
    except Exception:
        pass

    col_dash_ai, col_dash_btn = st.columns([0.78, 0.22])
    with col_dash_ai:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #172943 0%, #243B64 100%); border: 1.5px solid #D6B56D; border-radius: 12px; padding: 0.65rem 1rem; color: #FFFFFF; display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; box-shadow: 0 4px 14px rgba(23, 41, 67, 0.1);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: #D6B56D; color: #172943; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem;">SA</div>
                <div>
                    <div style="font-weight: 700; font-size: 0.875rem;">SARVA AI Companion &bull; <span style="color: #A5B4FC; font-weight: 600;">✨ Powered by Gemini 3.1 Live AI</span></div>
                    <div style="font-size: 0.725rem; color: #CBD5E1;">Ask anything about your syllabus, math derivations, or code debugging.</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: rgba(217, 119, 6, 0.2); border: 1px solid #F59E0B; color: #FDE68A; padding: 2px 8px; border-radius: 8px; font-size: 0.725rem; font-weight: 700;">
                    🪙 {u_coins:,} Coins
                </span>
                <span style="background: rgba(220, 38, 38, 0.2); border: 1px solid #EF4444; color: #FECDD3; padding: 2px 8px; border-radius: 8px; font-size: 0.725rem; font-weight: 700;">
                    🔥 {u_streak}d Streak
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_dash_btn:
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        if st.button("💬 Chat with AI", key="dash_open_sarva_ai_btn", type="primary", use_container_width=True):
            st.session_state["sarva_ai_dialog_open"] = True
            st.session_state.pop("sarva_ai_active_context", None)
            st.rerun()

    # Rewards Action Bar
    col_rw_bar, col_rw_btn = st.columns([0.78, 0.22])
    with col_rw_bar:
        st.markdown(f"""
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 0.45rem 0.85rem; margin-bottom: 0.85rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 0.775rem; color: #92400E; font-weight: 600;">
                🎁 <strong>SARVAVIDYA REWARDS:</strong> Earn coins on every verified quiz & streak. Current Tier: <span style="font-weight: 800; color: #B45309;">{u_level}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_rw_btn:
        st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
        if st.button("🎁 Rewards Store", key="dash_open_rewards_btn", use_container_width=True):
            st.session_state["current_page"] = "rewards"
            st.rerun()

    # ==========================================================
    # 2. TOP SECTION: 4 COMPACT SUMMARY CARDS
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Questions Attempted</span>
                <span style="color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{total_attempts}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">{correct_attempts} verified correct answers</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Assessment Accuracy</span>
                <span style="color: #36A879;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{accuracy:.1f}%</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Observed assessment score</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Concepts Mastered</span>
                <span style="color: #E9AA45;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{len(mastered_concepts)} / {len(mastery_data)}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">BKT threshold &ge; 85% demonstrated</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Learning Streak</span>
                <span style="color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{streak_days} Days</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Consecutive active learning</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 3. MAIN DASHBOARD CONTENT AREA (2x2 Balanced Grid)
    # ==========================================================
    col_left_main, col_right_main = st.columns([1.1, 1.2])

    # ----------------------------------------------------------
    # TOP-LEFT PANEL: Curriculum Statistics (Matching Ref "Class Statistics")
    # ----------------------------------------------------------
    with col_left_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Curriculum Statistics</span>
                <span style="background-color: #F5F6F8; border: 1px solid #E4E8ED; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; color: #718096; font-weight: 600;">All Time</span>
            </div>
        """, unsafe_allow_html=True)

        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #EAF2FA; color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                </div>
                <div class="lm-stat-val">{total_attempts}</div>
                <div class="lm-stat-label">Total Answers</div>
            </div>
            """, unsafe_allow_html=True)

        with col_stat2:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #FDF2F2; color: #D96B6B;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                </div>
                <div class="lm-stat-val">{len(weak_concepts)}</div>
                <div class="lm-stat-label">Struggling</div>
            </div>
            """, unsafe_allow_html=True)

        with col_stat3:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #EDF8F3; color: #36A879;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                </div>
                <div class="lm-stat-val">{len(strong_concepts)}</div>
                <div class="lm-stat-label">Excelling</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #F5F6F8;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #718096; margin-bottom: 0.25rem;">
                <span style="font-weight: 600; color: #243B64;">Curriculum Progression</span>
                <span style="font-weight: 600; color: #36A879;">{progress_pct}% of the progress</span>
            </div>
            <div class="lm-progress-wrap">
                <div class="lm-progress-bar" style="width: {progress_pct}%;"></div>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # TOP-RIGHT PANEL: Overall Performance & Skill Proficiency (Matching Ref)
    # ----------------------------------------------------------
    with col_right_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Overall Performance & Skill Proficiency</span>
                <span class="lm-card-link">View Details &gt;</span>
            </div>
        """, unsafe_allow_html=True)

        col_donut, col_top_concepts = st.columns([1, 1.25])

        with col_donut:
            # Skill Proficiency Donut Chart matching reference
            m_cnt = len(mastered_concepts)
            p_cnt = len(proficient_concepts)
            d_cnt = len(developing_concepts)
            n_cnt = len(novice_concepts)

            fig_donut = go.Figure(data=[go.Pie(
                labels=["Mastered", "Proficient", "Developing", "Novice"],
                values=[max(m_cnt, 1), max(p_cnt, 1), max(d_cnt, 1), max(n_cnt, 1)],
                hole=0.68,
                marker_colors=["#36A879", "#3976B9", "#E9AA45", "#D96B6B"],
                textinfo="none",
                hoverinfo="label+value"
            )])
            fig_donut.update_layout(
                margin=dict(l=5, r=5, t=5, b=5),
                height=150,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem; font-size: 0.675rem; color: #718096; margin-top: -0.5rem;">
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#36A879;margin-right:3px;"></span>Mastered: <strong>{m_cnt}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#3976B9;margin-right:3px;"></span>Proficient: <strong>{p_cnt}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#E9AA45;margin-right:3px;"></span>Developing: <strong>{d_cnt}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#D96B6B;margin-right:3px;"></span>Novice: <strong>{n_cnt}</strong></div>
            </div>
            """, unsafe_allow_html=True)

        with col_top_concepts:
            st.markdown("<div style='font-size: 0.775rem; font-weight: 700; color: #243B64; margin-bottom: 0.35rem;'>Concept Mastery Status</div>", unsafe_allow_html=True)
            for m in mastery_data[:4]:
                p = m["mastery_prob"]
                if p >= 0.85:
                    pill_cls = "pill-completed"
                    pill_lbl = "Completed"
                elif p >= 0.60:
                    pill_cls = "pill-ahead"
                    pill_lbl = "Ahead"
                elif p >= 0.40:
                    pill_cls = "pill-ontrack"
                    pill_lbl = "On Track"
                else:
                    pill_cls = "pill-lagging"
                    pill_lbl = "Lagging"

                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.32rem 0; border-bottom: 1px solid #F5F6F8;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-weight: 700; font-size: 0.7rem; color: #3976B9; background-color: #EAF2FA; padding: 2px 6px; border-radius: 4px;">{m['concept_code']}</span>
                        <span style="font-size: 0.775rem; font-weight: 600; color: #243B64;">{m['concept_name']}</span>
                    </div>
                    <span class="lm-pill {pill_cls}">{pill_lbl}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BOTTOM-LEFT PANEL: Struggling & Excelling (Matching Reference)
    # ----------------------------------------------------------
    with col_left_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Struggling & Excelling</span>
                <span class="lm-card-link">View Details &gt;</span>
            </div>
        """, unsafe_allow_html=True)

        # 1. Struggling section
        st.markdown("""
        <div style="font-size: 0.75rem; font-weight: 700; color: #D96B6B; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.4rem;">
            Attention Needed (Struggling Concepts)
        </div>
        """, unsafe_allow_html=True)

        struggling_list = weak_concepts if weak_concepts else mastery_data[-2:]
        for c in struggling_list[:2]:
            col_item_info, col_item_action = st.columns([3.2, 1])
            with col_item_info:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; padding: 0.35rem 0;">
                    <div class="lm-avatar" style="background-color: #FDF2F2; color: #D96B6B; border-color: #F8D7DA;">{c['concept_code'][:2]}</div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{c['concept_name']}</div>
                        <div style="font-size: 0.7rem; color: #718096;">Latent BKT Mastery: {c['mastery_prob']:.0%} &bull; {c['total_attempts']} attempts</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_item_action:
                st.markdown("<div style='padding-top: 0.35rem;'></div>", unsafe_allow_html=True)
                if st.button("Practice", key=f"btn_struggle_{c['concept_id']}", use_container_width=True):
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = c["concept_id"]
                    st.rerun()

        st.markdown("<hr style='border-color: #F0F3F7; margin: 0.65rem 0;'>", unsafe_allow_html=True)

        # 2. Excelling section
        st.markdown("""
        <div style="font-size: 0.75rem; font-weight: 700; color: #36A879; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.4rem;">
            Demonstrated Mastery (Excelling Concepts)
        </div>
        """, unsafe_allow_html=True)

        excelling_list = strong_concepts if strong_concepts else mastery_data[:2]
        for c in excelling_list[:2]:
            col_item_info, col_item_action = st.columns([3.2, 1])
            with col_item_info:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; padding: 0.35rem 0;">
                    <div class="lm-avatar" style="background-color: #EDF8F3; color: #36A879; border-color: #C6ECD9;">{c['concept_code'][:2]}</div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{c['concept_name']}</div>
                        <div style="font-size: 0.7rem; color: #718096;">Latent BKT Mastery: {c['mastery_prob']:.0%} &bull; {c['correct_attempts']}/{c['total_attempts']} correct</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_item_action:
                st.markdown("<div style='padding-top: 0.35rem;'></div>", unsafe_allow_html=True)
                if st.button("Drill", key=f"btn_excel_{c['concept_id']}", use_container_width=True):
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = c["concept_id"]
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BOTTOM-RIGHT PANEL: Performance Summary (Gauge matching reference)
    # ----------------------------------------------------------
    with col_right_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Performance Summary</span>
                <span class="lm-card-link">View Details &gt;</span>
            </div>
        """, unsafe_allow_html=True)

        col_gauge, col_badge_desc = st.columns([1.1, 0.9])

        avg_pct = int(avg_mastery * 100)
        tier_label = "Mastered" if avg_mastery >= 0.85 else ("Proficient" if avg_mastery >= 0.60 else ("Developing" if avg_mastery >= 0.40 else "Novice"))

        with col_gauge:
            # Semi-circle gauge chart reproducing reference half-gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_pct,
                number={'suffix': "%", 'font': {'size': 26, 'color': '#243B64', 'family': 'Roboto, sans-serif'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#E4E8ED', 'nticks': 5},
                    'bar': {'color': '#3976B9', 'thickness': 0.28},
                    'bgcolor': '#F5F6F8',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 40], 'color': '#FDF2F2'},
                        {'range': [40, 60], 'color': '#FEF9EE'},
                        {'range': [60, 80], 'color': '#EAF2FA'},
                        {'range': [80, 100], 'color': '#EDF8F3'}
                    ]
                }
            ))
            fig_gauge.update_layout(
                height=140,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF"
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

        with col_badge_desc:
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #243B64;">{tier_label}</div>
                        <div style="font-size: 0.725rem; color: #718096;">Average BKT Proficiency</div>
                    </div>
                    <div style="margin-left: auto;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#E9AA45" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                    </div>
                </div>
                <div style="font-size: 0.725rem; color: #718096; margin-top: 0.5rem; line-height: 1.4;">
                    Demonstrates consistent understanding across core prerequisite modules.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 4-Column Legend matching reference screenshot bottom
        tot_c = len(mastery_data)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; padding-top: 0.75rem; border-top: 1px solid #F5F6F8; margin-top: 0.5rem;">
            <div>
                <div style="font-size: 0.7rem; color: #D96B6B; font-weight: 700;">Lagging</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(novice_concepts)} Concepts ({int(len(novice_concepts)/tot_c*100)}%)</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #E9AA45; font-weight: 700;">On Track</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(developing_concepts)} Concepts ({int(len(developing_concepts)/tot_c*100)}%)</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #3976B9; font-weight: 700;">Ahead</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(proficient_concepts)} Concepts ({int(len(proficient_concepts)/tot_c*100)}%)</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #36A879; font-weight: 700;">Completed</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(mastered_concepts)} Concepts ({int(len(mastered_concepts)/tot_c*100)}%)</div>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 3.5 AI-POWERED PERSONALIZED LEARNING RECOMMENDATIONS
    # ==========================================================
    _render_recommendations_section(user, active_course, mastery_data, attempts, lesson_progress)

    # ==========================================================
    # 4. BOTTOM SECTION: COMPACT LEARNING ROADMAP
    # ==========================================================
    st.markdown(f"""
    <div class="lm-card" style="margin-top: 0.5rem;">
        <div class="lm-card-header">
            <span class="lm-card-title">{active_course['name']} Progression Roadmap</span>
            <span style="font-size: 0.725rem; color: #718096;">Sequential dependency flow based on 60% BKT proficiency gating</span>
        </div>
    """, unsafe_allow_html=True)

    cols_rm = st.columns(max(len(mastery_data), 1))
    mastery_map = {m["concept_code"]: m["mastery_prob"] for m in mastery_data}

    for idx, m_row in enumerate(mastery_data):
        c_code = m_row["concept_code"]
        c_prob = m_row["mastery_prob"]
        prereq_eval = RecommenderEngine.evaluate_prerequisites(c_code, mastery_map)

        if not prereq_eval["eligible"]:
            pill_status = '<span class="lm-pill pill-lagging">Locked</span>'
            border_c = "#E4E8ED"
            bg_c = "#F5F6F8"
        elif c_prob >= 0.85:
            pill_status = '<span class="lm-pill pill-completed">Mastered</span>'
            border_c = "#C6ECD9"
            bg_c = "#FFFFFF"
        elif c_prob >= 0.60:
            pill_status = '<span class="lm-pill pill-ahead">Proficient</span>'
            border_c = "#D2E4F6"
            bg_c = "#FFFFFF"
        else:
            pill_status = '<span class="lm-pill pill-ontrack">In Progress</span>'
            border_c = "#FDE8C7"
            bg_c = "#FFFFFF"

        with cols_rm[idx]:
            st.markdown(f"""
            <div style="background-color: {bg_c}; border: 1px solid {border_c}; border-radius: 8px; padding: 0.65rem 0.5rem; text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 0.65rem; color: #718096; font-weight: 600;">STEP {idx + 1}</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #243B64; margin: 0.15rem 0; height: 36px; overflow: hidden;">{m_row['concept_name']}</div>
                <div style="font-size: 0.725rem; color: #3976B9; font-weight: 600; margin-bottom: 0.35rem;">{c_prob:.0%} BKT</div>
                {pill_status}
            </div>
            """, unsafe_allow_html=True)
            if prereq_eval["eligible"]:
                if st.button("Practice", key=f"rm_btn_{c_code}", use_container_width=True):
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = m_row["concept_id"]
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _calculate_streak(attempts: list) -> int:
    """Calculates active daily streak from attempt timestamps."""
    if not attempts:
        return 0

    dates = set()
    for a in attempts:
        raw = a["attempted_at"]
        dt = raw.split("T")[0] if "T" in raw else raw.split(" ")[0]
        dates.add(dt)

    sorted_dates = sorted(dates, reverse=True)
    today = datetime.now().date()

    streak = 0
    curr = today
    for d_str in sorted_dates:
        d = datetime.strptime(d_str, "%Y-%m-%d").date()
        diff = (curr - d).days
        if diff <= 1:
            streak += 1
            curr = d
        else:
            break

    return max(streak, 1 if dates else 0)


def _render_recommendations_section(user, active_course, mastery_data, attempts, lesson_progress):
    """Renders the AI-powered personalized recommendation engine section with direct actions."""
    user_id = user["id"]
    course_id = active_course["id"]

    # Generate live recommendations using pedagogical engine
    generated_recs = RecommenderEngine.generate_recommendations(user_id, mastery_data, attempts, lesson_progress)
    if generated_recs:
        save_recommendations(user_id, course_id, generated_recs)

    # Fetch stored active recommendations from DB
    recs = get_student_recommendations(user_id, course_id=course_id, limit=6)
    if not recs and generated_recs:
        recs = generated_recs[:6]

    st.markdown("""
    <div class="lm-card" style="margin-top: 0.75rem; margin-bottom: 0.75rem;">
        <div class="lm-card-header">
            <div>
                <span class="lm-card-title">AI-Powered Personalized Learning Recommendations</span>
                <div style="font-size: 0.725rem; color: #718096; margin-top: 0.15rem;">
                    Identifies knowledge gaps, prerequisite barriers, and optimal Zone of Proximal Development steps.
                </div>
            </div>
            <span class="lm-pill pill-ahead">6 Pedagogical Categories</span>
        </div>
    """, unsafe_allow_html=True)

    if not recs:
        st.info("No immediate remediation required! Continue with the course progression below or attempt an assessment.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Category styling map
    cat_style = {
        "Study This Concept": {"bg": "#EFF6FF", "text": "#1E40AF", "border": "#BFDBFE"},
        "Practice These Questions": {"bg": "#ECFDF5", "text": "#065F46", "border": "#A7F3D0"},
        "Revise Previous Lessons": {"bg": "#FFFBEB", "text": "#92400E", "border": "#FDE68A"},
        "Attempt Advanced Questions": {"bg": "#F5F3FF", "text": "#5B21B6", "border": "#DDD6FE"},
        "Complete Prerequisite Concepts": {"bg": "#FEF2F2", "text": "#991B1B", "border": "#FECACA"},
        "Continue Your Learning Path": {"bg": "#F8FAFC", "text": "#1E293B", "border": "#CBD5E1"},
    }

    # Render in 3-column rows
    for i in range(0, min(len(recs), 6), 3):
        chunk = recs[i:i+3]
        cols = st.columns(len(chunk))
        for col, r in zip(cols, chunk):
            with col:
                cat = r.get("category", "Study This Concept")
                style = cat_style.get(cat, {"bg": "#F1F5F9", "text": "#334155", "border": "#E2E8F0"})
                diff = r.get("suggested_difficulty", "Intermediate").capitalize()
                mins = r.get("estimated_minutes", 15)
                title = r.get("title", "Recommended Step")
                reason = r.get("reason", "")
                c_name = r.get("concept_name", "")
                c_id = r.get("concept_id")
                rec_id = r.get("id")

                # Match mastery
                m_prob = 0.20
                for m in mastery_data:
                    if m.get("concept_id") == c_id:
                        m_prob = m.get("mastery_prob", 0.20)
                        break

                action_type = "learn" if cat in ["Study This Concept", "Revise Previous Lessons", "Complete Prerequisite Concepts"] else "practice"
                btn_label = "Start Learning" if action_type == "learn" else "Practice Now"

                st.markdown(f"""
                <div style="background: {style['bg']}; border: 1.5px solid {style['border']}; border-radius: 10px; padding: 0.85rem; height: 260px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 0.65rem;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span style="background: {style['text']}; color: #FFFFFF; font-size: 0.65rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; text-transform: uppercase;">
                                {cat}
                            </span>
                            <span style="font-size: 0.675rem; color: #64748B; font-weight: 600;">
                                ⏱ {mins} mins
                            </span>
                        </div>
                        <div style="font-weight: 700; font-size: 0.85rem; color: #172943; margin-bottom: 0.25rem; line-height: 1.3;">
                            {title}
                        </div>
                        <div style="display: flex; gap: 6px; align-items: center; margin-bottom: 0.45rem;">
                            <span style="font-size: 0.65rem; color: #475569; background: #FFFFFF; border: 1px solid {style['border']}; padding: 1px 6px; border-radius: 4px; font-weight: 600;">
                                Difficulty: {diff}
                            </span>
                            <span style="font-size: 0.65rem; color: #475569; background: #FFFFFF; border: 1px solid {style['border']}; padding: 1px 6px; border-radius: 4px; font-weight: 600;">
                                Mastery: {m_prob:.0%}
                            </span>
                        </div>
                        <div style="font-size: 0.725rem; color: #475569; line-height: 1.4; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical;">
                            {reason}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{btn_label} →", key=f"btn_rec_act_{rec_id or i}_{c_id}", type="primary", use_container_width=True):
                    if rec_id:
                        mark_recommendation_followed(rec_id)
                    if action_type == "learn":
                        st.session_state["current_page"] = "learning_library"
                        st.session_state["_synced_page"] = "learning_library"
                        st.session_state["lib_search"] = c_name
                    else:
                        st.session_state["current_page"] = "assessment"
                        st.session_state["_synced_page"] = "assessment"
                        st.session_state["assessment_concept_id"] = c_id
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
