"""
LearnSphere AI: Authentication and Access Management
Supports student registration, student sign-in, teacher access,
and quick demonstration profile switching.
"""

import streamlit as st
from core.auth_service import AuthService
from database.db import (
    get_user_by_username, get_user_by_email, create_user
)
from components.brand import render_full_hero_brand, BRAND_NAME, TAGLINE


def render_auth_page():
    render_full_hero_brand(center=True)
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.25rem;">
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">
            Sign in to your personalized multi-subject workspace or launch a verified academic persona.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Determine default active tab from session state if set
    default_tab = st.session_state.get("auth_tab", "student")
    tab_index = 0
    if default_tab == "teacher":
        tab_index = 1
    elif default_tab == "register":
        tab_index = 2
    elif default_tab == "demo":
        tab_index = 3

    tabs = st.tabs(["Student Login", "Teacher Login", "Create Account", "Demonstration Mode"])

    # 1. Student Login
    with tabs[0]:
        _render_student_login()

    # 2. Teacher Login
    with tabs[1]:
        _render_teacher_login()

    # 3. Registration
    with tabs[2]:
        _render_registration()

    # 4. Instant Demo Mode
    with tabs[3]:
        _render_demo_switcher()


def _render_student_login():
    st.markdown("""
    <div class="lm-card" style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 1rem; font-weight: 700; color: #243B64; margin-bottom: 0.25rem;">
            Student Sign In
        </h4>
        <div style="font-size: 0.8rem; color: #64748b;">
            Default demo credentials pre-filled: <code>student@123</code> / <code>student123</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("1-Click Instant Student Login (student@123)", key="quick_btn_student", type="primary", use_container_width=True):
        user = get_user_by_email("student@123") or get_user_by_username("student@123")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "student_dashboard"
            st.session_state.pop("auth_tab", None)
            st.rerun()

    st.markdown("""
    <div style="display: flex; align-items: center; text-align: center; margin: 0.75rem 0; color: #94a3b8; font-size: 0.75rem;">
        <div style="flex-grow: 1; border-bottom: 1px solid #e2e8f0;"></div>
        <span style="padding: 0 8px;">OR SIGN IN WITH FORM</span>
        <div style="flex-grow: 1; border-bottom: 1px solid #e2e8f0;"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_login_form"):
        username = st.text_input("Username or Email", value="student@123", placeholder="e.g. student@123", key="stu_login_user")
        password = st.text_input("Password", value="student123", type="password", key="stu_login_pass")
        st.caption("Pre-filled Demo Credentials: Email: `student@123` &bull; Password: `student123`")
        submitted = st.form_submit_button("Sign In as Student", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password.")
                return

            user = get_user_by_username(username) or get_user_by_email(username)
            if not user or user["role"] != "student":
                st.error("Invalid student credentials or user does not exist.")
                return

            if AuthService.verify_password(password, user["salt"], user["password_hash"]):
                st.session_state["user"] = user
                st.session_state["current_page"] = "student_dashboard"
                st.session_state.pop("auth_tab", None)
                st.success(f"Welcome back, {user['full_name']}.")
                st.rerun()
            else:
                st.error("Incorrect password. Please verify your credentials.")


def _render_teacher_login():
    st.markdown("""
    <div class="lm-card" style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 1rem; font-weight: 700; color: #243B64; margin-bottom: 0.25rem;">
            Teacher and Faculty Sign In
        </h4>
        <div style="font-size: 0.8rem; color: #64748b;">
            Default demo credentials pre-filled: <code>teacher@123</code> / <code>teacher123</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("1-Click Instant Teacher Login (teacher@123)", key="quick_btn_teacher", type="primary", use_container_width=True):
        user = get_user_by_email("teacher@123") or get_user_by_username("teacher@123")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "teacher_dashboard"
            st.session_state.pop("auth_tab", None)
            st.rerun()

    st.markdown("""
    <div style="display: flex; align-items: center; text-align: center; margin: 0.75rem 0; color: #94a3b8; font-size: 0.75rem;">
        <div style="flex-grow: 1; border-bottom: 1px solid #e2e8f0;"></div>
        <span style="padding: 0 8px;">OR SIGN IN WITH FORM</span>
        <div style="flex-grow: 1; border-bottom: 1px solid #e2e8f0;"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("teacher_login_form"):
        username = st.text_input("Username or Email", value="teacher@123", placeholder="e.g. teacher@123", key="tchr_login_user")
        password = st.text_input("Password", value="teacher123", type="password", key="tchr_login_pass")
        st.caption("Pre-filled Demo Credentials: Email: `teacher@123` &bull; Password: `teacher123`")
        submitted = st.form_submit_button("Sign In to Faculty Portal", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password.")
                return

            user = get_user_by_username(username) or get_user_by_email(username)
            if not user or user["role"] != "teacher":
                st.error("Invalid faculty credentials or insufficient permissions.")
                return

            if AuthService.verify_password(password, user["salt"], user["password_hash"]):
                st.session_state["user"] = user
                st.session_state["current_page"] = "teacher_dashboard"
                st.session_state.pop("auth_tab", None)
                st.success(f"Authenticated as {user['full_name']}.")
                st.rerun()
            else:
                st.error("Incorrect password.")


def _render_registration():
    st.markdown("""
    <div class="lm-card">
        <h4 style="font-size: 1rem; font-weight: 700; color: #243B64; margin-bottom: 0.75rem;">
            Student Registration
        </h4>
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form"):
        full_name = st.text_input("Full Name", placeholder="e.g. Maya Patel")
        username = st.text_input("Desired Username", placeholder="e.g. maya_p")
        email = st.text_input("Institutional or Personal Email", placeholder="e.g. maya@example.edu")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            password = st.text_input("Password", type="password", help="Minimum 6 characters")
        with col_p2:
            confirm_pwd = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Create Learning Account", type="primary", use_container_width=True)

        if submitted:
            valid, err = AuthService.validate_registration(username, email, password, confirm_pwd, full_name)
            if not valid:
                st.error(err)
                return

            if get_user_by_username(username):
                st.error("Username is already registered. Please choose another.")
                return

            if get_user_by_email(email):
                st.error("Email is already associated with an existing account.")
                return

            pwd_hash, salt = AuthService.hash_password(password)
            user_id = create_user(
                username=username,
                email=email,
                password_hash=pwd_hash,
                salt=salt,
                full_name=full_name,
                role="student"
            )

            user = get_user_by_username(username)
            st.session_state["user"] = user
            st.session_state["current_page"] = "student_dashboard"
            st.session_state.pop("auth_tab", None)
            st.success(f"Account created successfully. Welcome, {full_name}!")
            st.rerun()


def _render_demo_switcher():
    st.markdown("""
    <div class="ls-card">
        <div class="ls-card-header">
            <h4 class="ls-card-title">Pre-Configured Demonstration Profiles</h4>
            <span class="ls-badge badge-demo">Evaluation Mode</span>
        </div>
        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 1.25rem;">
            Select a verified demonstration persona to immediately evaluate the Bayesian Knowledge Tracing engine, misconception detection diagnostics, and personalized recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color: #ffffff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 1.25rem; height: 100%;">
            <div style="font-weight: 600; color: #1e40af; margin-bottom: 0.25rem;">Student Demo (student@123)</div>
            <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 0.5rem;">User/Email: <code>student@123</code> &bull; Pass: <code>student123</code></div>
            <div style="font-size: 0.825rem; color: #475569; line-height: 1.5; margin-bottom: 1rem;">
                Shows mastered Variables and Conditionals, but possesses repeating cognitive misconceptions in Loops (Off-by-One) and Recursion.
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="ls-badge badge-developing">Active Misconceptions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Student Profile (student@123)", key="launch_alex", use_container_width=True, type="primary"):
            user = get_user_by_email("student@123") or get_user_by_username("student@123")
            if user:
                st.session_state["user"] = user
                st.session_state["current_page"] = "student_dashboard"
                st.rerun()

    with col2:
        st.markdown("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1.25rem; height: 100%;">
            <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.25rem;">Sophia Chen</div>
            <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 0.75rem;">Student Profile 2</div>
            <div style="font-size: 0.825rem; color: #475569; line-height: 1.5; margin-bottom: 1rem;">
                Advanced proficient learner. High BKT mastery across core modules, working on advanced Recursion and algorithmic efficiency.
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="ls-badge badge-mastered">High Mastery</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Sophia Chen Profile", key="launch_sophia", use_container_width=True):
            user = get_user_by_username("sophia_chen")
            if user:
                st.session_state["user"] = user
                st.session_state["current_page"] = "student_dashboard"
                st.rerun()

    with col3:
        st.markdown("""
        <div style="background-color: #ffffff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 1.25rem; height: 100%;">
            <div style="font-weight: 600; color: #1e40af; margin-bottom: 0.25rem;">Teacher Demo (teacher@123)</div>
            <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 0.5rem;">User/Email: <code>teacher@123</code> &bull; Pass: <code>teacher123</code></div>
            <div style="font-size: 0.825rem; color: #475569; line-height: 1.5; margin-bottom: 1rem;">
                Faculty portal with access to cohort-wide mastery distributions, common misconception frequencies, and student inspection tools.
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="ls-badge badge-proficient">Faculty Role</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Teacher Profile (teacher@123)", key="launch_teacher", use_container_width=True, type="primary"):
            user = get_user_by_email("teacher@123") or get_user_by_username("teacher@123") or get_user_by_username("dr_bennett")
            if user:
                st.session_state["user"] = user
                st.session_state["current_page"] = "teacher_dashboard"
                st.rerun()

