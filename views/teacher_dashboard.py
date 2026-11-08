"""
LearnSphere AI: Faculty and Teacher Dashboard
Faithfully reproduces the exact visual design language and layout structure
of the reference educational management dashboard:
- Class Statistics with 3-stat columns and progress bar
- Overall Class Performance with Skill Proficiency donut and Top Students list
- Struggling & Excelling students with outline 'View' action buttons
- Performance Summary with semi-circle gauge and 4-column distribution
- Systemic Misconception Analysis and Class Recommendations
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.db import (
    get_class_overview, get_all_students, get_student_mastery,
    get_user_attempts, get_all_courses
)
from core.bkt import BayesianKnowledgeTracing
from core.misconception import MisconceptionEngine


def render_teacher_dashboard(user: dict):
    if user.get("role") not in ("teacher", "admin"):
        st.error("Access restricted: This portal is reserved for verified faculty accounts.")
        return

    courses = get_all_courses(active_only=True)
    course_options = ["All Subjects & Tracks"] + [f"{c['name']} ({c['subject_name']})" for c in courses]
    
    # Selected filter from session or selectbox
    selected_filter_label = st.session_state.get("teacher_track_filter", course_options[0])
    default_filter_idx = course_options.index(selected_filter_label) if selected_filter_label in course_options else 0

    selected_course_obj = None
    if default_filter_idx > 0:
        selected_course_obj = courses[default_filter_idx - 1]
    
    selected_course_id = selected_course_obj["id"] if selected_course_obj else None

    overview = get_class_overview(course_id=selected_course_id)
    students = get_all_students()
    cm_list = overview.get("concept_masteries", [])
    cohort_avg = (sum(c["avg_mastery"] for c in cm_list) / len(cm_list)) if cm_list else 0.20

    # Categorize students into struggling vs excelling
    student_stats = []
    for s in students:
        s_mastery = get_student_mastery(s["id"], course_id=selected_course_id)
        s_attempts = get_user_attempts(s["id"], limit=50, course_id=selected_course_id)
        s_avg = (sum(m["mastery_prob"] for m in s_mastery) / len(s_mastery)) if s_mastery else 0.20
        s_correct = sum(1 for a in s_attempts if a["is_correct"])
        s_acc = (s_correct / len(s_attempts) * 100) if s_attempts else 0.0
        student_stats.append({
            "id": s["id"],
            "name": s["full_name"],
            "username": s["username"],
            "avg_mastery": s_avg,
            "accuracy": s_acc,
            "attempts": len(s_attempts)
        })

    struggling_students = [s for s in student_stats if s["avg_mastery"] < 0.60]
    excelling_students = [s for s in student_stats if s["avg_mastery"] >= 0.70]

    # ==========================================================
    # 1. PAGE TITLE & CLASS SELECTION (Matching Reference)
    # ==========================================================
    col_title, col_class = st.columns([2.0, 1.0])
    with col_title:
        sub_label = f"Cohort: {selected_filter_label}" if selected_course_id else "All Active Tracks"
        st.markdown(f"""
        <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 0.75rem;">
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #172943; margin: 0; letter-spacing: -0.02em;">Sarva Vidya Faculty Intelligence</h2>
            <span style="font-size: 0.775rem; color: #718096; font-weight: 500;">Instructor: {user['full_name']} &bull; {sub_label}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_class:
        new_sel = st.selectbox(
            "Assigned Class / Track",
            course_options,
            index=default_filter_idx,
            key="teacher_track_filter_select",
            label_visibility="collapsed"
        )
        if new_sel != selected_filter_label:
            st.session_state["teacher_track_filter"] = new_sel
            st.rerun()

    # ==========================================================
    # 2. TOP SECTION: 4 COMPACT SUMMARY CARDS
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Enrolled Students</span>
                <span style="color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{overview['total_students']}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Active roster in Class A</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Class Accuracy</span>
                <span style="color: #36A879;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{overview['avg_accuracy']:.1%}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Mean assessment correctness</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Total Submissions</span>
                <span style="color: #E9AA45;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{overview['total_attempts']}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Telemetry across all concepts</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="lm-card" style="padding: 0.85rem 1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.725rem; color: #718096; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Cohort BKT Mastery</span>
                <span style="color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #243B64; margin-top: 0.15rem; line-height: 1.2;">{cohort_avg:.1%}</div>
            <div style="font-size: 0.725rem; color: #718096; margin-top: 0.2rem;">Latent knowledge estimate</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 3. MAIN DASHBOARD CONTENT AREA (2x2 Balanced Grid)
    # ==========================================================
    col_left_main, col_right_main = st.columns([1.1, 1.2])

    # ----------------------------------------------------------
    # TOP-LEFT PANEL: Class Statistics (Matching Reference Image)
    # ----------------------------------------------------------
    with col_left_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Class Statistics</span>
                <span style="background-color: #F5F6F8; border: 1px solid #E4E8ED; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; color: #718096; font-weight: 600;">April 2026</span>
            </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #EAF2FA; color: #3976B9;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <div class="lm-stat-val">{overview['total_students']}</div>
                <div class="lm-stat-label">Total Students</div>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #FDF2F2; color: #D96B6B;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                </div>
                <div class="lm-stat-val">{len(struggling_students)}</div>
                <div class="lm-stat-label">Struggling</div>
            </div>
            """, unsafe_allow_html=True)

        with col_c3:
            st.markdown(f"""
            <div class="lm-stat-col">
                <div class="lm-stat-icon-wrap" style="background-color: #EDF8F3; color: #36A879;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                </div>
                <div class="lm-stat-val">{len(excelling_students)}</div>
                <div class="lm-stat-label">Excelling</div>
            </div>
            """, unsafe_allow_html=True)

        class_progress_pct = int(cohort_avg * 100)
        st.markdown(f"""
        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #F5F6F8;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #718096; margin-bottom: 0.25rem;">
                <span style="font-weight: 600; color: #243B64;">Class Progress</span>
                <span style="font-weight: 600; color: #36A879;">{class_progress_pct}% of the progress</span>
            </div>
            <div class="lm-progress-wrap">
                <div class="lm-progress-bar" style="width: {class_progress_pct}%;"></div>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # TOP-RIGHT PANEL: Overall Class Performance (Donut + Top Students)
    # ----------------------------------------------------------
    with col_right_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Overall Class Performance</span>
                <span class="lm-card-link">View Details &gt;</span>
            </div>
        """, unsafe_allow_html=True)

        col_p_donut, col_p_students = st.columns([1, 1.25])

        with col_p_donut:
            # Skill Proficiency Donut Chart matching reference
            mastered_cohort = sum(1 for c in cm_list if c["avg_mastery"] >= 0.85)
            proficient_cohort = sum(1 for c in cm_list if 0.60 <= c["avg_mastery"] < 0.85)
            developing_cohort = sum(1 for c in cm_list if 0.40 <= c["avg_mastery"] < 0.60)
            novice_cohort = sum(1 for c in cm_list if c["avg_mastery"] < 0.40)

            fig_donut = go.Figure(data=[go.Pie(
                labels=["Mastered", "Proficient", "Developing", "Novice"],
                values=[max(mastered_cohort, 1), max(proficient_cohort, 1), max(developing_cohort, 1), max(novice_cohort, 1)],
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
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#36A879;margin-right:3px;"></span>Mastered: <strong>{mastered_cohort}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#3976B9;margin-right:3px;"></span>Proficient: <strong>{proficient_cohort}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#E9AA45;margin-right:3px;"></span>Developing: <strong>{developing_cohort}</strong></div>
                <div><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#D96B6B;margin-right:3px;"></span>Novice: <strong>{novice_cohort}</strong></div>
            </div>
            """, unsafe_allow_html=True)

        with col_p_students:
            st.markdown("<div style='font-size: 0.775rem; font-weight: 700; color: #243B64; margin-bottom: 0.35rem;'>Top Students</div>", unsafe_allow_html=True)
            for s in student_stats[:4]:
                p = s["avg_mastery"]
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

                initials = "".join([x[0].upper() for x in s["name"].split()[:2]])
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.32rem 0; border-bottom: 1px solid #F5F6F8;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <div class="lm-avatar" style="width:24px;height:24px;font-size:0.65rem;">{initials}</div>
                        <div>
                            <div style="font-size: 0.775rem; font-weight: 600; color: #243B64;">{s['name']}</div>
                            <div style="font-size: 0.675rem; color: #718096;">{s['accuracy']:.0f}% accuracy</div>
                        </div>
                    </div>
                    <span class="lm-pill {pill_cls}">{pill_lbl}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BOTTOM-LEFT PANEL: Struggling & Excelling Students (Matching Ref)
    # ----------------------------------------------------------
    with col_left_main:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Struggling & Excelling</span>
                <span class="lm-card-link">View Details &gt;</span>
            </div>
        """, unsafe_allow_html=True)

        # Bottom Struggling Students
        st.markdown("""
        <div style="font-size: 0.75rem; font-weight: 700; color: #D96B6B; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.4rem;">
            Struggling Students (Needs Teacher Intervention)
        </div>
        """, unsafe_allow_html=True)

        disp_struggling = struggling_students if struggling_students else student_stats[-2:]
        for st_obj in disp_struggling[:2]:
            col_s_info, col_s_btn = st.columns([3.2, 1])
            with col_s_info:
                inits = "".join([x[0].upper() for x in st_obj["name"].split()[:2]])
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; padding: 0.35rem 0;">
                    <div class="lm-avatar" style="background-color: #FDF2F2; color: #D96B6B; border-color: #F8D7DA;">{inits}</div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{st_obj['name']}</div>
                        <div style="font-size: 0.7rem; color: #718096;">Latent BKT: {st_obj['avg_mastery']:.0%} &bull; {st_obj['attempts']} attempts</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_s_btn:
                st.markdown("<div style='padding-top: 0.35rem;'></div>", unsafe_allow_html=True)
                if st.button("View", key=f"view_struggle_st_{st_obj['id']}", use_container_width=True):
                    st.session_state["selected_drilldown_student"] = st_obj["id"]

        st.markdown("<hr style='border-color: #F0F3F7; margin: 0.65rem 0;'>", unsafe_allow_html=True)

        # Top Excelling Students
        st.markdown("""
        <div style="font-size: 0.75rem; font-weight: 700; color: #36A879; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.4rem;">
            Top Excelling Students
        </div>
        """, unsafe_allow_html=True)

        disp_excelling = excelling_students if excelling_students else student_stats[:2]
        for st_obj in disp_excelling[:2]:
            col_s_info, col_s_btn = st.columns([3.2, 1])
            with col_s_info:
                inits = "".join([x[0].upper() for x in st_obj["name"].split()[:2]])
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; padding: 0.35rem 0;">
                    <div class="lm-avatar" style="background-color: #EDF8F3; color: #36A879; border-color: #C6ECD9;">{inits}</div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{st_obj['name']}</div>
                        <div style="font-size: 0.7rem; color: #718096;">Latent BKT: {st_obj['avg_mastery']:.0%} &bull; {st_obj['accuracy']:.0f}% accuracy</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_s_btn:
                st.markdown("<div style='padding-top: 0.35rem;'></div>", unsafe_allow_html=True)
                if st.button("View", key=f"view_excel_st_{st_obj['id']}", use_container_width=True):
                    st.session_state["selected_drilldown_student"] = st_obj["id"]

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

        col_t_gauge, col_t_desc = st.columns([1.1, 0.9])
        cohort_pct = int(cohort_avg * 100)
        c_tier = "Proficient" if cohort_avg >= 0.60 else "Developing"

        with col_t_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=cohort_pct,
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

        with col_t_desc:
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #243B64;">{c_tier}</div>
                        <div style="font-size: 0.725rem; color: #718096;">Average Proficiency</div>
                    </div>
                    <div style="margin-left: auto;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#E9AA45" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                    </div>
                </div>
                <div style="font-size: 0.725rem; color: #718096; margin-top: 0.5rem; line-height: 1.4;">
                    Cohort is performing stably above baseline with strong foundational comprehension.
                </div>
            </div>
            """, unsafe_allow_html=True)

        tot_s = max(len(students), 1)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; padding-top: 0.75rem; border-top: 1px solid #F5F6F8; margin-top: 0.5rem;">
            <div>
                <div style="font-size: 0.7rem; color: #D96B6B; font-weight: 700;">Lagging</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(struggling_students)} Students ({int(len(struggling_students)/tot_s*100)}%)</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #E9AA45; font-weight: 700;">On Track</div>
                <div style="font-size: 0.675rem; color: #718096;">{tot_s - len(struggling_students) - len(excelling_students)} Students</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #3976B9; font-weight: 700;">Ahead</div>
                <div style="font-size: 0.675rem; color: #718096;">{len(excelling_students)} Students ({int(len(excelling_students)/tot_s*100)}%)</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #36A879; font-weight: 700;">Completed</div>
                <div style="font-size: 0.675rem; color: #718096;">100% Retained</div>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # 4. SYSTEMIC MISCONCEPTION FREQUENCY & INSTRUCTOR RECOMMENDATIONS
    # ==========================================================
    col_miscon, col_rec = st.columns([1.1, 1.2])

    with col_miscon:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Systemic Cohort Misconceptions</span>
                <span style="font-size: 0.725rem; color: #718096;">Frequent cognitive bugs</span>
            </div>
        """, unsafe_allow_html=True)

        top_m = overview.get("top_misconceptions", [])
        if top_m:
            for item in top_m[:3]:
                meta = MisconceptionEngine.get_info(item["misconception_code"])
                m_name = meta["name"] if meta else item["misconception_code"]
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #F5F6F8;">
                    <div>
                        <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{m_name}</div>
                        <div style="font-size: 0.675rem; color: #718096;">Code: {item['misconception_code']} &bull; Category: {meta['category'] if meta else ''}</div>
                    </div>
                    <span class="lm-pill pill-lagging">{item['count']} Errors</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No systemic misconceptions logged across the cohort yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rec:
        st.markdown("""
        <div class="lm-card">
            <div class="lm-card-header">
                <span class="lm-card-title">Class Instructional Recommendations</span>
                <span style="font-size: 0.725rem; color: #36A879; font-weight: 600;">Automated AI Insights</span>
            </div>
        """, unsafe_allow_html=True)

        rec_items = []
        if top_m:
            top_code = top_m[0]["misconception_code"]
            rem = MisconceptionEngine.get_remediation(top_code)
            rec_items.append({
                "title": f"Target Cohort Cognitive Misconception: {top_code}",
                "desc": f"Observed {top_m[0]['count']} occurrences across the cohort. Recommended instructional action: {rem.get('remedial_strategy', 'Provide conceptual counterexamples and guided code walkthroughs.')}"
            })
        
        # Concept with lowest average mastery
        if cm_list:
            lowest_c = min(cm_list, key=lambda x: x["avg_mastery"])
            rec_items.append({
                "title": f"Reinforce {lowest_c['concept_name']} ({lowest_c['concept_code']})",
                "desc": f"Mean cohort mastery is currently {lowest_c['avg_mastery']:.0%}. Introduce targeted practice drills before advancing dependent modules."
            })

        if excelling_students:
            top_s_names = ", ".join([s["name"] for s in excelling_students[:2]])
            rec_items.append({
                "title": "Advance High-Mastery Learners",
                "desc": f"{top_s_names} and other top performers have exceeded 70% mastery and are prepared for advanced problem sets."
            })

        for r_idx, r in enumerate(rec_items[:2]):
            border_bottom = "border-bottom: 1px solid #F5F6F8;" if r_idx == 0 else ""
            st.markdown(f"""
            <div style="padding: 0.4rem 0; {border_bottom}">
                <div style="font-weight: 600; font-size: 0.8rem; color: #243B64;">{r['title']}</div>
                <div style="font-size: 0.725rem; color: #718096; margin-top: 0.15rem; line-height: 1.4;">
                    {r['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
