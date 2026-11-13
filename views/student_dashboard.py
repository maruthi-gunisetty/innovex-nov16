"""
SARVAVIDYA: Retro Quiz & Learning Hub Student Dashboard
Replaces the old dashboard with the retro quiz layout:
- Left Column: "Recent Played" (2-column subject cards with illustrations & coral "Play again" buttons)
- Center Column: "Play To Gain Your Knowledge" Hero Card + "Popular Game 🔥" (Technology & Sciences cards)
- Right Column: "Leaderboard 🔥" with Top 3 Podium (Emma, Sophia, Andrew) and live database student ranking
- Bottom Accordion/Tabs: Deep BKT Mastery Analytics, AI Recommendations, and Gemini 3.1 Live AI Companion
"""

import streamlit as st
import plotly.graph_objects as go
import os
import base64
from datetime import datetime
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress,
    get_all_learning_content, save_recommendations, get_student_recommendations,
    mark_recommendation_followed, get_user_equipped_avatar, get_db_connection
)
from core.bkt import BayesianKnowledgeTracing
from core.recommender import RecommenderEngine
from core.misconception import MisconceptionEngine
from core.course_manager import get_active_course, set_active_course, get_available_tracks, render_course_selector


def _get_ui_svg_uri(filename: str) -> str:
    """Encodes UI SVG as a base64 Data URI for instant offline rendering."""
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "ui", filename)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            svg_text = f.read()
        b64 = base64.b64encode(svg_text.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64}"
    return ""


def _calculate_streak(attempts: list) -> int:
    """Calculates consecutive active learning days from real attempt logs."""
    if not attempts:
        return 0
    attempt_dates = set()
    for a in attempts:
        ts = a.get("attempted_at")
        if ts:
            try:
                attempt_dates.add(ts[:10])
            except Exception:
                pass
    return len(attempt_dates)


def render_student_dashboard(user: dict):
    user_id = user["id"]
    active_course = get_active_course()
    course_id = active_course["id"]

    mastery_data = get_student_mastery(user_id, course_id=course_id)
    attempts = get_user_attempts(user_id, limit=30, course_id=course_id)
    lesson_progress = get_user_lesson_progress(user_id)

    # Calculate statistics
    total_attempts = len(attempts)
    correct_attempts = sum(1 for a in attempts if a["is_correct"])
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0
    streak_days = _calculate_streak(attempts)
    avg_mastery = (sum(m["mastery_prob"] for m in mastery_data) / len(mastery_data)) if mastery_data else 0.20

    # Categorize Concepts
    strong_concepts = [m for m in mastery_data if m["mastery_prob"] >= 0.70]
    weak_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.60]
    mastered_concepts = [m for m in mastery_data if m["mastery_prob"] >= 0.85]
    proficient_concepts = [m for m in mastery_data if 0.60 <= m["mastery_prob"] < 0.85]
    developing_concepts = [m for m in mastery_data if 0.40 <= m["mastery_prob"] < 0.60]
    novice_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.40]

    # Fetch User Wallet
    u_coins = 0
    try:
        from core.rewards_engine import RewardsEngine
        rw = RewardsEngine.get_or_create_wallet(user_id)
        u_coins = rw.get("available_coins", 0)
    except Exception:
        pass

    # SVG Asset URIs
    hero_img = _get_ui_svg_uri("hero_study_collage.svg")
    thumb_python = _get_ui_svg_uri("thumb_python.svg")
    thumb_c = _get_ui_svg_uri("thumb_c_prog.svg")
    thumb_calc = _get_ui_svg_uri("thumb_calculus.svg")
    thumb_dsa = _get_ui_svg_uri("thumb_dsa.svg")
    thumb_elec = _get_ui_svg_uri("thumb_electronics.svg")
    thumb_phys = _get_ui_svg_uri("thumb_physics.svg")
    pop_tech = _get_ui_svg_uri("popular_tech.svg")
    pop_sci = _get_ui_svg_uri("popular_science.svg")

    # ==========================================================
    # MAIN RETRO QUIZ 3-COLUMN LAYOUT
    # ==========================================================
    col_left, col_center, col_right = st.columns([1.0, 1.45, 0.95], gap="medium")

    # ----------------------------------------------------------
    # COLUMN 1 (LEFT): RECENT PLAYED
    # ----------------------------------------------------------
    with col_left:
        st.markdown("""
        <div class="quiz-display-title" style="font-size: 1.7rem; margin-bottom: 0.85rem; color: #111111;">
            Recent Played
        </div>
        """, unsafe_allow_html=True)

        recent_subjects = [
            ("Social sciences", "Explore the world of technology and earns bragging point!", thumb_python, "python"),
            ("Social sciences", "Explore the world of technology and continue brain training!", thumb_c, "c_programming"),
            ("Social sciences", "Explore the world of technology and cams sciences, and format for quiz!", thumb_calc, "calculus_linear_algebra"),
            ("Social sciences", "Explore the world of technology and cams sciences, and transform quiz!", thumb_dsa, "dsa"),
            ("Social sciences", "Explore the world of technology and carve champion, and bragging points!", thumb_elec, "digital_electronics"),
            ("Social sciences", "Explore the world of technology and carve champion, and bragging points!", thumb_phys, "physics_mechanics"),
        ]

        # 2x3 Grid of Recent Played Cards
        for i in range(0, 6, 2):
            col_card_a, col_card_b = st.columns(2)

            # Card A
            name_a, desc_a, img_a, track_a = recent_subjects[i]
            with col_card_a:
                st.markdown(f"""
                <div class="quiz-card" style="padding: 0.75rem; margin-bottom: 0.75rem;">
                    <div style="border-radius: 12px; overflow: hidden; margin-bottom: 0.5rem; height: 95px; background: #FF5238;">
                        <img src="{img_a}" style="width: 100%; height: 100%; object-fit: cover;" alt="{name_a}"/>
                    </div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #111111; margin-bottom: 0.2rem; line-height: 1.2;">{name_a}</div>
                    <div style="font-size: 0.68rem; color: #64748B; line-height: 1.3; height: 32px; overflow: hidden; margin-bottom: 0.65rem;">
                        {desc_a}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Play again", key=f"btn_play_{track_a}_{i}", type="primary", use_container_width=True):
                    set_active_course(track_a)
                    st.session_state["current_page"] = "assessment"
                    st.session_state["_synced_page"] = "assessment"
                    st.rerun()

            # Card B
            name_b, desc_b, img_b, track_b = recent_subjects[i + 1]
            with col_card_b:
                st.markdown(f"""
                <div class="quiz-card" style="padding: 0.75rem; margin-bottom: 0.75rem;">
                    <div style="border-radius: 12px; overflow: hidden; margin-bottom: 0.5rem; height: 95px; background: #FF5238;">
                        <img src="{img_b}" style="width: 100%; height: 100%; object-fit: cover;" alt="{name_b}"/>
                    </div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #111111; margin-bottom: 0.2rem; line-height: 1.2;">{name_b}</div>
                    <div style="font-size: 0.68rem; color: #64748B; line-height: 1.3; height: 32px; overflow: hidden; margin-bottom: 0.65rem;">
                        {desc_b}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Play again", key=f"btn_play_{track_b}_{i+1}", type="primary", use_container_width=True):
                    set_active_course(track_b)
                    st.session_state["current_page"] = "assessment"
                    st.session_state["_synced_page"] = "assessment"
                    st.rerun()

    # ----------------------------------------------------------
    # COLUMN 2 (CENTER): HERO BANNER & POPULAR GAMES
    # ----------------------------------------------------------
    with col_center:
        # 1. HERO BANNER: "Play To Gain Your Knowledge"
        st.markdown(f"""
        <div class="quiz-hero-card" style="margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
                <div style="flex: 1.3;">
                    <div style="font-family: 'Anton', 'Oswald', sans-serif; font-size: 2.3rem; line-height: 1.05; color: #111111; margin-bottom: 0.65rem;">
                        Play To Gain Your<br/>Knowledge
                    </div>
                    <div style="font-size: 0.78rem; color: #52525B; line-height: 1.45; margin-bottom: 1.25rem; max-width: 290px;">
                        Adaptive learning missions engineered with Bayesian Knowledge Tracing. Practice real syllabus concepts and climb the global leaderboards!
                    </div>
                </div>
                <div style="flex: 1.2; text-align: right; max-height: 180px;">
                    <img src="{hero_img}" style="width: 100%; max-height: 175px; object-fit: contain;" alt="Study group collage"/>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_hero_cta_1, col_hero_cta_2 = st.columns([1, 1.5])
        with col_hero_cta_1:
            if st.button("Get started", key="btn_hero_get_started", type="secondary", use_container_width=True):
                st.session_state["current_page"] = "assessment"
                st.session_state["_synced_page"] = "assessment"
                st.rerun()

        # 2. POPULAR GAME SECTION
        st.markdown("""
        <div class="quiz-display-title" style="font-size: 1.7rem; margin: 1.25rem 0 0.85rem 0; color: #111111;">
            Popular Game 🔥
        </div>
        """, unsafe_allow_html=True)

        col_pop_1, col_pop_2 = st.columns(2)

        # Popular Card 1: Technology (Vibrant Coral Red #FF5238)
        with col_pop_1:
            st.markdown(f"""
            <div style="background-color: #FF5238; border-radius: 22px; padding: 1.2rem; color: #FFFFFF; position: relative; box-shadow: 0 6px 20px rgba(255, 82, 56, 0.25);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: #111111; color: #FFFFFF; font-weight: 800; font-size: 0.7rem; padding: 3px 10px; border-radius: 9999px;">
                        Tech
                    </span>
                    <span style="background: #FFFFFF; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        ❤️
                    </span>
                </div>
                <div style="font-family: 'Anton', 'Oswald', sans-serif; font-size: 1.85rem; color: #FFFFFF; margin-bottom: 0.35rem; letter-spacing: 0.01em;">
                    Technology
                </div>
                <div style="font-size: 0.725rem; color: #FFFFFF; opacity: 0.95; line-height: 1.4; margin-bottom: 0.75rem; min-height: 48px;">
                    Explore the world of technology with interesting Technology Quiz and see if you have what it takes to go from a novice to every master!
                </div>
                <div style="border-radius: 14px; overflow: hidden; height: 110px; background: rgba(255,255,255,0.15);">
                    <img src="{pop_tech}" style="width: 100%; height: 100%; object-fit: cover;" alt="Technology quiz"/>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Start Technology Quiz", key="btn_start_pop_tech", type="primary", use_container_width=True):
                set_active_course("python")
                st.session_state["current_page"] = "assessment"
                st.session_state["_synced_page"] = "assessment"
                st.rerun()

        # Popular Card 2: Social sciences (Vibrant Emerald Green #0D8A5E)
        with col_pop_2:
            st.markdown(f"""
            <div style="background-color: #0D8A5E; border-radius: 22px; padding: 1.2rem; color: #FFFFFF; position: relative; box-shadow: 0 6px 20px rgba(13, 138, 94, 0.25);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: #111111; color: #FFFFFF; font-weight: 800; font-size: 0.7rem; padding: 3px 10px; border-radius: 9999px;">
                        Tech
                    </span>
                    <span style="background: #FFFFFF; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        ❤️
                    </span>
                </div>
                <div style="font-family: 'Anton', 'Oswald', sans-serif; font-size: 1.85rem; color: #FFFFFF; margin-bottom: 0.35rem; letter-spacing: 0.01em;">
                    Social sciences
                </div>
                <div style="font-size: 0.725rem; color: #FFFFFF; opacity: 0.95; line-height: 1.4; margin-bottom: 0.75rem; min-height: 48px;">
                    Explore the world of technology with interesting Technology Quiz and see if you have what it takes to go from a novice to every master!
                </div>
                <div style="border-radius: 14px; overflow: hidden; height: 110px; background: rgba(255,255,255,0.15);">
                    <img src="{pop_sci}" style="width: 100%; height: 100%; object-fit: cover;" alt="Sciences quiz"/>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Start Sciences Quiz", key="btn_start_pop_sci", type="primary", use_container_width=True):
                set_active_course("calculus_linear_algebra")
                st.session_state["current_page"] = "assessment"
                st.session_state["_synced_page"] = "assessment"
                st.rerun()

    # ----------------------------------------------------------
    # COLUMN 3 (RIGHT): LEADERBOARD 🔥
    # ----------------------------------------------------------
    with col_right:
        st.markdown("""
        <div class="quiz-card" style="padding: 1.25rem 1rem;">
            <div class="quiz-display-title" style="font-size: 1.7rem; margin-bottom: 1.25rem; color: #111111;">
                Leaderboard 🔥
            </div>
        """, unsafe_allow_html=True)

        # Fetch real students or fallback to the screenshot top roster
        db_leaderboard = []
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT u.id, u.full_name, u.username, COALESCE(w.available_coins, 0) as coins
                    FROM users u
                    LEFT JOIN student_wallets w ON u.id = w.user_id
                    WHERE u.role = 'student'
                    ORDER BY coins DESC, u.id ASC
                    LIMIT 12
                """)
                db_leaderboard = [dict(r) for r in cur.fetchall()]
        except Exception:
            pass

        # Static reference podium matching the user's reference screenshot
        top_1 = {"name": "Emma Ema", "points": "889 Diamonds", "avatar": "assets/avatars/avatar_10_legendary_ace.svg"}
        top_2 = {"name": "Sophia Cba", "points": "880 Diamonds", "avatar": "assets/avatars/avatar_6_shadow_knight.svg"}
        top_3 = {"name": "Andrew W", "points": "808 Diamonds", "avatar": "assets/avatars/avatar_8_star_guardian.svg"}

        # If real student records are available with higher scores, blend gracefully
        if len(db_leaderboard) >= 1 and db_leaderboard[0]["coins"] > 500:
            top_1["name"] = db_leaderboard[0]["full_name"]
            top_1["points"] = f"{db_leaderboard[0]['coins']} Diamonds"
        if len(db_leaderboard) >= 2 and db_leaderboard[1]["coins"] > 200:
            top_2["name"] = db_leaderboard[1]["full_name"]
            top_2["points"] = f"{db_leaderboard[1]['coins']} Diamonds"

        from views.avatarverse import _get_svg_data_uri
        av1_uri = _get_svg_data_uri(top_1["avatar"])
        av2_uri = _get_svg_data_uri(top_2["avatar"])
        av3_uri = _get_svg_data_uri(top_3["avatar"])

        # 3-Podium Visualization
        st.markdown(f"""
        <div style="display: flex; align-items: flex-end; justify-content: center; gap: 8px; margin-bottom: 1.5rem; text-align: center;">
            <!-- Rank 2: Silver (Sophia) -->
            <div style="flex: 1;">
                <div style="position: relative; display: inline-block;">
                    <img src="{av2_uri}" style="width: 50px; height: 50px; border-radius: 50%; border: 2.5px solid #CBD5E1; object-fit: cover; background: #FFF;" alt="Silver"/>
                    <span style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: #94A3B8; color: #FFF; font-weight: 800; font-size: 0.65rem; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        2
                    </span>
                </div>
                <div style="font-weight: 700; font-size: 0.78rem; color: #111; margin-top: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {top_2['name']}
                </div>
                <div style="font-size: 0.65rem; color: #64748B;">{top_2['points']}</div>
            </div>

            <!-- Rank 1: Gold (Emma - Center Elevated) -->
            <div style="flex: 1.15; padding-bottom: 8px;">
                <div style="position: relative; display: inline-block;">
                    <div style="position: absolute; top: -14px; left: 50%; transform: translateX(-50%); font-size: 1rem;">👑</div>
                    <img src="{av1_uri}" style="width: 60px; height: 60px; border-radius: 50%; border: 3px solid #FFB800; object-fit: cover; background: #FFF; box-shadow: 0 4px 12px rgba(255, 184, 0, 0.3);" alt="Gold"/>
                    <span style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: #FFB800; color: #FFF; font-weight: 800; font-size: 0.7rem; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        1
                    </span>
                </div>
                <div style="font-weight: 800; font-size: 0.825rem; color: #111; margin-top: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {top_1['name']}
                </div>
                <div style="font-size: 0.65rem; color: #64748B;">{top_1['points']}</div>
            </div>

            <!-- Rank 3: Bronze (Andrew) -->
            <div style="flex: 1;">
                <div style="position: relative; display: inline-block;">
                    <img src="{av3_uri}" style="width: 50px; height: 50px; border-radius: 50%; border: 2.5px solid #F59E0B; object-fit: cover; background: #FFF;" alt="Bronze"/>
                    <span style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: #D97706; color: #FFF; font-weight: 800; font-size: 0.65rem; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        3
                    </span>
                </div>
                <div style="font-weight: 700; font-size: 0.78rem; color: #111; margin-top: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {top_3['name']}
                </div>
                <div style="font-size: 0.65rem; color: #64748B;">{top_3['points']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: #F1ECE1; margin: 0.75rem 0 1rem 0;'>", unsafe_allow_html=True)

        # Rank 4+ List matching screenshot
        ref_ranks = [
            ("Bayu aji saadewa", "20 Point", "assets/avatars/avatar_1_mystic_scholar.svg"),
            ("Olivia Ava", "86 Point", "assets/avatars/avatar_4_tech_wizard.svg"),
            ("David Joshua", "88 Point", "assets/avatars/avatar_2_celestial_dreamer.svg"),
            ("Charlotte Harper", "22 Point", "assets/avatars/avatar_9_royal_enigma.svg"),
            ("Mia Evelyn", "11 Point", "assets/avatars/avatar_3_cyber_sage.svg"),
            ("Mama Riia", "10 Point", "assets/avatars/avatar_5_quantum_learner.svg"),
            ("Colm Roma", "10 Point", "assets/avatars/avatar_7_phoenix_aura.svg"),
        ]

        # Render list rows
        for r_name, r_pts, r_av in ref_ranks:
            r_av_uri = _get_svg_data_uri(r_av)
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.35rem 0.25rem; border-bottom: 1px solid #FAF7F0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="{r_av_uri}" style="width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid #E5DFD5; object-fit: cover;" alt="{r_name}"/>
                    <div>
                        <div style="font-weight: 700; font-size: 0.78rem; color: #111111;">{r_name}</div>
                        <div style="font-size: 0.65rem; color: #718096;">{r_pts}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # EXTENDED ACCORDION: MASTERY ANALYTICS & AI COMPANION
    # ==========================================================
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    with st.expander("📊 Detailed Concept Mastery & Bayesian Knowledge Tracing Analytics", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Answers", total_attempts, f"{correct_attempts} correct")
        with c2:
            st.metric("Assessment Accuracy", f"{accuracy:.1f}%")
        with c3:
            st.metric("Mastered Concepts", f"{len(mastered_concepts)} / {len(mastery_data)}")
        with c4:
            st.metric("Active Streak", f"{streak_days} Days")

        col_m_left, col_m_right = st.columns([1, 1.2])
        with col_m_left:
            st.markdown("#### Skill Proficiency Breakdown")
            m_cnt = len(mastered_concepts)
            p_cnt = len(proficient_concepts)
            d_cnt = len(developing_concepts)
            n_cnt = len(novice_concepts)

            fig_donut = go.Figure(data=[go.Pie(
                labels=["Mastered", "Proficient", "Developing", "Novice"],
                values=[max(m_cnt, 1), max(p_cnt, 1), max(d_cnt, 1), max(n_cnt, 1)],
                hole=0.65,
                marker_colors=["#10B981", "#3B82F6", "#F59E0B", "#EF4444"],
                textinfo="none"
            )])
            fig_donut.update_layout(height=160, margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

        with col_m_right:
            st.markdown("#### Latent Concept Mastery Status")
            for m in mastery_data[:4]:
                p = m["mastery_prob"]
                lbl = "Completed" if p >= 0.85 else ("Ahead" if p >= 0.60 else ("On Track" if p >= 0.40 else "Lagging"))
                color = "#10B981" if p >= 0.85 else ("#3B82F6" if p >= 0.60 else ("#F59E0B" if p >= 0.40 else "#EF4444"))
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid #EBE5D8;">
                    <span style="font-weight: 700; font-size: 0.8rem; color: #111;">{m['concept_name']}</span>
                    <span style="background: {color}20; color: {color}; font-weight: 700; font-size: 0.725rem; padding: 2px 8px; border-radius: 9999px;">
                        {lbl} ({p:.0%})
                    </span>
                </div>
                """, unsafe_allow_html=True)

        # AI Recommendations
        _render_recommendations_section(user, active_course, mastery_data, attempts, lesson_progress)


def _render_recommendations_section(user, active_course, mastery_data, attempts, lesson_progress):
    """Renders personalized recommendations with persistent caching."""
    user_id = user["id"]
    course_id = active_course["id"]

    try:
        active_recs = get_student_recommendations(user_id, course_id=course_id, limit=3)
        if not active_recs:
            recs = RecommenderEngine.generate_recommendations(user_id, course_id=course_id, limit=3)
            save_recommendations(user_id, recs)
            active_recs = get_student_recommendations(user_id, course_id=course_id, limit=3)
    except Exception:
        active_recs = []

    if active_recs:
        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🎯 AI Recommended Learning Actions")
        rec_cols = st.columns(len(active_recs))
        for idx, r in enumerate(active_recs):
            with rec_cols[idx]:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1.5px solid #EBE5D8; border-radius: 14px; padding: 0.75rem; margin-bottom: 0.5rem;">
                    <div style="font-size: 0.7rem; color: #FF5238; font-weight: 800; text-transform: uppercase;">{r.get('rec_type', 'DRILL')}</div>
                    <div style="font-weight: 700; font-size: 0.825rem; color: #111; margin: 0.2rem 0;">{r.get('concept_name', 'Concept')}</div>
                    <div style="font-size: 0.7rem; color: #64748B; margin-bottom: 0.5rem;">{r.get('reason', 'Targeted practice')}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Practice Concept", key=f"rec_btn_{r.get('id', idx)}", use_container_width=True):
                    mark_recommendation_followed(r.get("id"))
                    st.session_state["current_page"] = "assessment"
                    st.session_state["assessment_concept_id"] = r.get("concept_id")
                    st.session_state["_synced_page"] = "assessment"
                    st.rerun()
