"""
LearnSphere AI: Student Learning Dashboard
Provides personalized performance metrics, BKT concept mastery estimates,
activity streaks, weak/strong topic classifications, and targeted recommendations.
Clean modern SaaS design inspired by Linear, Stripe, and Notion.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.db import (
    get_student_mastery, get_user_attempts, get_user_lesson_progress,
    get_all_learning_content
)
from core.bkt import BayesianKnowledgeTracing
from core.recommender import RecommenderEngine
from core.misconception import MisconceptionEngine


def render_student_dashboard(user: dict):
    user_id = user["id"]
    mastery_data = get_student_mastery(user_id)
    attempts = get_user_attempts(user_id, limit=30)
    lesson_progress = get_user_lesson_progress(user_id)

    # 1. Header and Profile Banner
    demo_badge = '<span class="ls-badge badge-demo" style="margin-left: 0.75rem;">Demonstration Account</span>' if user.get("is_demo") else ''
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
        <div>
            <h2 style="font-size: 1.75rem; font-weight: 700; color: #172554; margin: 0; letter-spacing: -0.025em; display: flex; align-items: center;">
                Welcome, {user['full_name']} {demo_badge}
            </h2>
            <p style="color: #64748B; font-size: 0.875rem; margin-top: 0.25rem;">
                Adaptive Student Dashboard &bull; Track mastery, review diagnostic feedback, and advance your curriculum.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate Summary Statistics from Actual Database Records
    total_attempts = len(attempts)
    correct_attempts = sum(1 for a in attempts if a["is_correct"])
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0

    # Calculate Activity Streak from attempt dates
    streak_days = _calculate_streak(attempts)

    # Average BKT Mastery Probability
    avg_mastery = (sum(m["mastery_prob"] for m in mastery_data) / len(mastery_data)) if mastery_data else 0.20

    # 2. Key Metrics Row (Linear Style)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Questions Attempted</div>
            <div class="ls-metric-val">{total_attempts}</div>
            <div class="ls-metric-sub">{correct_attempts} correct submissions</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Assessment Accuracy</div>
            <div class="ls-metric-val">{accuracy:.1f}%</div>
            <div class="ls-metric-sub">Observed exam performance</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Average BKT Mastery</div>
            <div class="ls-metric-val">{avg_mastery:.1%}</div>
            <div class="ls-metric-sub">Latent cognitive estimate</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="ls-metric-box">
            <div class="ls-metric-label">Activity Streak</div>
            <div class="ls-metric-val">{streak_days} Days</div>
            <div class="ls-metric-sub">Consecutive active study</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Personalized Pedagogical Recommendations
    recs = RecommenderEngine.generate_recommendations(user_id, mastery_data, attempts, lesson_progress)
    st.markdown("""
    <div class="ls-card" style="border-left: 4px solid #635BDB;">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-violet">Personalized Intelligence</span>
                <h3 class="ls-card-title" style="margin-top: 0.25rem;">Intelligent Learning Recommendations</h3>
                <div class="ls-card-desc">Generated dynamically from concept dependencies and Bayesian mastery scores.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if recs:
        for r in recs:
            badge_class = "badge-developing" if "misconception" in r["type"] else ("badge-novice" if "prerequisite" in r["type"] else "badge-proficient")
            type_label = r["type"].replace("_", " ").title()
            col_rec_text, col_rec_act = st.columns([4, 1])
            with col_rec_text:
                st.markdown(f"""
                <div style="padding: 0.75rem 0; border-bottom: 1px solid #F1F5F9;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span class="ls-badge {badge_class}">{type_label}</span>
                        <strong style="color: #0F172A; font-size: 0.95rem;">{r['title']}</strong>
                    </div>
                    <div style="color: #475569; font-size: 0.85rem; line-height: 1.5;">{r['reason']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_rec_act:
                btn_label = "Open Lesson" if r["recommended_action"] == "library" else "Take Practice"
                btn_type = "primary" if "misconception" in r["type"] or "prerequisite" in r["type"] else "secondary"
                if st.button(btn_label, key=f"rec_btn_{r['concept_code']}_{r['type']}", use_container_width=True, type=btn_type):
                    if r["recommended_action"] == "library":
                        st.session_state["current_page"] = "learning_library"
                        st.session_state["selected_lesson_code"] = r["concept_code"]
                    else:
                        st.session_state["current_page"] = "assessment"
                        st.session_state["assessment_concept_id"] = r["concept_id"]
                    st.rerun()
    else:
        st.info("You are on track across all curriculum prerequisites. Continue through the learning library.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Weak Concepts and Strong Concepts Breakdown
    strong_concepts = [m for m in mastery_data if m["mastery_prob"] >= 0.70]
    weak_concepts = [m for m in mastery_data if m["mastery_prob"] < 0.60]

    col_weak, col_strong = st.columns(2)
    with col_weak:
        st.markdown("""
        <div class="ls-card" style="border-left: 4px solid #DC2626;">
            <div class="ls-card-header">
                <div>
                    <span class="ls-badge badge-novice">Attention Required</span>
                    <h3 class="ls-card-title" style="margin-top: 0.25rem;">Weak Concepts</h3>
                    <div class="ls-card-desc">Concepts below the 60% proficiency threshold requiring focused practice.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if weak_concepts:
            for wc in weak_concepts:
                col_w_text, col_w_btn = st.columns([3, 1.2])
                with col_w_text:
                    st.markdown(f"""
                    <div style="padding: 0.5rem 0; border-bottom: 1px solid #F1F5F9;">
                        <strong style="color: #172554; font-size: 0.9rem;">{wc['concept_name']}</strong>
                        <div style="font-size: 0.775rem; color: #DC2626; font-weight: 600;">
                            BKT Mastery: {wc['mastery_prob']:.1%} &bull; {wc['total_attempts']} attempts
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_w_btn:
                    if st.button("Practice Concept", key=f"weak_prac_{wc['concept_id']}", use_container_width=True, type="primary"):
                        st.session_state["current_page"] = "assessment"
                        st.session_state["assessment_concept_id"] = wc["concept_id"]
                        st.rerun()
        else:
            st.markdown("<p style='color: #16A34A; font-size: 0.85rem; padding: 0.5rem 0;'>No weak concepts detected. All active topics meet the proficiency benchmark.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_strong:
        st.markdown("""
        <div class="ls-card" style="border-left: 4px solid #16A34A;">
            <div class="ls-card-header">
                <div>
                    <span class="ls-badge badge-mastered">Demonstrated Fluency</span>
                    <h3 class="ls-card-title" style="margin-top: 0.25rem;">Strong Concepts</h3>
                    <div class="ls-card-desc">Topics exceeding 70% BKT mastery with demonstrated fluency.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if strong_concepts:
            for sc in strong_concepts:
                col_s_text, col_s_btn = st.columns([3, 1.2])
                with col_s_text:
                    st.markdown(f"""
                    <div style="padding: 0.5rem 0; border-bottom: 1px solid #F1F5F9;">
                        <strong style="color: #172554; font-size: 0.9rem;">{sc['concept_name']}</strong>
                        <div style="font-size: 0.775rem; color: #16A34A; font-weight: 600;">
                            BKT Mastery: {sc['mastery_prob']:.1%} &bull; {sc['correct_attempts']}/{sc['total_attempts']} correct
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_s_btn:
                    if st.button("Advanced Drill", key=f"strong_drill_{sc['concept_id']}", use_container_width=True, type="secondary"):
                        st.session_state["current_page"] = "assessment"
                        st.session_state["assessment_concept_id"] = sc["concept_id"]
                        st.rerun()
        else:
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; padding: 0.5rem 0;'>Continue completing assessments to demonstrate concept mastery.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. Upcoming Learning Activities and Pending Tasks
    all_lessons = get_all_learning_content()
    pending_tasks = []

    # Incomplete curriculum lessons
    for les in all_lessons:
        cid = les["id"]
        if not lesson_progress.get(cid, False):
            pending_tasks.append({
                "type": "Curriculum Module",
                "badge": "badge-violet",
                "title": f"Study {les['concept_name']}: {les['title']}",
                "detail": f"{les['reading_time_min']} min reading &bull; Conceptual foundation and code sandbox",
                "action_type": "library",
                "target_code": les["concept_code"],
                "btn_label": "Run Task: Open Lesson"
            })

    # Weak concepts needing reinforcement
    for wc in weak_concepts[:2]:
        pending_tasks.append({
            "type": "Diagnostic Drill",
            "badge": "badge-novice",
            "title": f"Strengthen Mastery in {wc['concept_name']}",
            "detail": f"Current BKT score {wc['mastery_prob']:.0%} is below benchmark (60%). Reinforce latent mastery.",
            "action_type": "assessment",
            "target_id": wc["concept_id"],
            "btn_label": "Run Task: Take Drill"
        })

    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <span class="ls-badge badge-violet">Action Queue</span>
                <h3 class="ls-card-title" style="margin-top: 0.25rem;">Upcoming Learning Activities and Pending Tasks</h3>
                <div class="ls-card-desc">Scheduled curriculum modules, diagnostic exercises, and cognitive remediation tasks ready to run.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if pending_tasks:
        for idx, task in enumerate(pending_tasks[:5]):
            col_t_info, col_t_btn = st.columns([4, 1.2])
            with col_t_info:
                st.markdown(f"""
                <div style="padding: 0.65rem 0; border-bottom: 1px solid #F1F5F9;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span class="ls-badge {task['badge']}">{task['type']}</span>
                        <strong style="color: #0F172A; font-size: 0.925rem;">{task['title']}</strong>
                    </div>
                    <div style="color: #64748B; font-size: 0.825rem;">{task['detail']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_t_btn:
                st.markdown("<div style='margin-top: 0.25rem;'></div>", unsafe_allow_html=True)
                if st.button(task["btn_label"], key=f"run_pending_task_{idx}", use_container_width=True, type="primary"):
                    if task["action_type"] == "library":
                        st.session_state["current_page"] = "learning_library"
                        st.session_state["selected_lesson_code"] = task["target_code"]
                    else:
                        st.session_state["current_page"] = "assessment"
                        st.session_state["assessment_concept_id"] = task["target_id"]
                    st.rerun()
    else:
        st.markdown("<p style='color: #16A34A; font-size: 0.85rem;'>All curriculum modules and practice drills completed. You are completely caught up!</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. Concept Mastery Grid (BKT Estimates)
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <h3 class="ls-card-title">Curriculum Concept Mastery Matrix</h3>
                <div class="ls-card-desc">Probabilistic knowledge tracing estimates versus raw interaction counts.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    bkt = BayesianKnowledgeTracing()
    for idx, m in enumerate(mastery_data):
        with cols[idx % 3]:
            classification = bkt.classify_mastery(m["mastery_prob"])
            prob_pct = int(m["mastery_prob"] * 100)
            st.markdown(f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.1rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <div>
                        <div style="font-size: 0.725rem; font-weight: 600; color: #64748B;">{m['concept_code']}</div>
                        <div style="font-weight: 600; font-size: 0.95rem; color: #172554;">{m['concept_name']}</div>
                    </div>
                    <span class="ls-badge {classification['badge_class']}">{classification['tier']}</span>
                </div>
                <div style="margin: 0.75rem 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-bottom: 0.25rem;">
                        <span>BKT Latent Estimate</span>
                        <strong style="color: #0F172A;">{m['mastery_prob']:.1%}</strong>
                    </div>
                    <div style="background-color: #E2E8F0; height: 6px; border-radius: 9999px; overflow: hidden;">
                        <div style="background-color: {classification['color']}; width: {prob_pct}%; height: 100%; border-radius: 9999px;"></div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748B;">
                    <span>Attempts: {m['total_attempts']}</span>
                    <span>Correct: {m['correct_attempts']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Practice Concept", key=f"btn_prac_{m['concept_id']}", use_container_width=True):
                st.session_state["current_page"] = "assessment"
                st.session_state["assessment_concept_id"] = m["concept_id"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Recent Assessment Activity Table (Stripe Style)
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <h3 class="ls-card-title">Recent Assessment Telemetry</h3>
                <div class="ls-card-desc">Chronological log of submissions with cognitive diagnostics.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if attempts:
        table_rows = ""
        for a in attempts[:8]:
            status_badge = '<span class="ls-badge badge-mastered">Correct</span>' if a["is_correct"] else '<span class="ls-badge badge-novice">Incorrect</span>'
            m_code = a.get("misconception_code") or "NONE"
            m_info = MisconceptionEngine.get_info(m_code)
            diag_text = m_info["name"] if m_info else "Standard Execution"
            att_time = a["attempted_at"][:16].replace("T", " ") if "T" in a["attempted_at"] else a["attempted_at"][:16]

            table_rows += f"""
            <tr>
                <td><strong>{a['question_title']}</strong><br><span style="color:#64748B; font-size:0.75rem;">{a['concept_name']}</span></td>
                <td>{a['difficulty'].capitalize()}</td>
                <td>{status_badge}</td>
                <td>{diag_text}</td>
                <td>{a['prior_mastery']:.0%} &rarr; {a['posterior_mastery']:.0%}</td>
                <td style="color:#64748B; font-size:0.8rem;">{att_time}</td>
            </tr>
            """

        st.markdown(f"""
        <table class="ls-table">
            <thead>
                <tr>
                    <th>Question / Topic</th>
                    <th>Difficulty</th>
                    <th>Result</th>
                    <th>Diagnostic Finding</th>
                    <th>Mastery Shift</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#64748B; font-size:0.85rem;'>No assessment attempts recorded yet. Launch an assessment to begin tracking your mastery.</p>", unsafe_allow_html=True)

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
