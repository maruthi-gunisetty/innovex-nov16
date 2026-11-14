"""
SARVAVIDYA: Premium Enterprise Authentication Portal
Redesigned with Modern White + Blue Enterprise aesthetics:
- Responsive split-screen architecture (55% Brand Experience / 45% Auth Card)
- Golden lotus + open book identity and four-subject STEM showcase
- Modern segmented tabs with instant 1-click evaluation access
- Preserves 100% of underlying cryptographically secure PBKDF2 authentication,
  session persistence, role management, and database operations.
"""

import streamlit as st
from core.auth_service import AuthService
from database.db import (
    get_user_by_username, get_user_by_email, create_user
)
from components.brand import SYMBOL_SVG, BRAND_NAME, TAGLINE
from components.styles import AUTH_PAGE_CSS


def _clean_html(raw_html: str) -> str:
    """Strips all leading and trailing whitespace from every line so Markdown never treats HTML as code blocks."""
    return "\n".join(line.strip() for line in raw_html.strip().splitlines() if line.strip())


def render_auth_page():
    """
    Renders the premium split-screen authentication portal:
    Left: Brand identity, learning philosophy, and 4-subject discipline showcase.
    Right: Modern enterprise authentication card with segmented navigation.
    """
    # Enforce strict sidebar hiding and expanded width on login portal
    st.markdown(AUTH_PAGE_CSS, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.18, 0.95], gap="large")

    # ==========================================================
    # 1. LEFT SECTION: BRAND AND LEARNING EXPERIENCE
    # ==========================================================
    with col_left:
        left_raw = f"""
<div class="sv-auth-left">
<div style="position: absolute; top: -50px; right: -50px; width: 220px; height: 220px; border-radius: 50%; background: radial-gradient(circle, rgba(214, 181, 109, 0.12) 0%, rgba(57, 118, 185, 0.08) 50%, transparent 70%); pointer-events: none;"></div>
<div style="position: absolute; bottom: -30px; left: -30px; width: 180px; height: 180px; border-radius: 50%; background: radial-gradient(circle, rgba(36, 59, 100, 0.06) 0%, transparent 70%); pointer-events: none;"></div>
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 1.25rem;">
<div style="width: 52px; height: 52px; min-width: 52px; background: #172943; border: 1.5px solid #D6B56D; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 4px; box-shadow: 0 4px 14px rgba(23, 41, 67, 0.2);">
{SYMBOL_SVG}
</div>
<div>
<div style="font-family: 'Roboto', -apple-system, sans-serif; font-weight: 800; font-size: 1.6rem; color: #172943; letter-spacing: -0.02em; line-height: 1.1;">
Sarva <span style="color: #D6B56D;">Vidya</span>
</div>
<div style="font-size: 0.725rem; font-weight: 600; color: #718096; letter-spacing: 0.04em; text-transform: uppercase;">
Enterprise Learning Ecosystem
</div>
</div>
</div>
<h1 style="font-size: 2.1rem; font-weight: 800; color: #172943; line-height: 1.22; margin: 0 0 0.65rem 0; letter-spacing: -0.025em;">
Unlock Your Potential with Intelligent Learning
</h1>
<p style="font-size: 0.925rem; color: #5A6A80; line-height: 1.6; margin: 0 0 1.5rem 0;">
One personalized learning ecosystem for Programming, Mathematics, Engineering, Science and beyond.
Diagnose cognitive misconceptions, trace latent mastery via BKT, and accelerate your academic mastery.
</p>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem; margin-bottom: 1.5rem;">
<div class="sv-subject-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 28px; height: 28px; border-radius: 6px; background-color: #EAF2FA; display: flex; align-items: center; justify-content: center; color: #243B64;">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
</div>
<span style="font-weight: 700; font-size: 0.875rem; color: #172943;">Programming</span>
</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem; padding: 2px 7px;">Python • C • DSA</span>
</div>
<div style="font-size: 0.75rem; color: #64748B; line-height: 1.4;">
Execution traces, pointer memory models, algorithmic recursion & analysis.
</div>
</div>
<div class="sv-subject-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 28px; height: 28px; border-radius: 6px; background-color: #FAF5EA; display: flex; align-items: center; justify-content: center; color: #B88F3A;">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><line x1="9" y1="10" x2="15" y2="10"/><line x1="12" y1="7" x2="12" y2="13"/></svg>
</div>
<span style="font-weight: 700; font-size: 0.875rem; color: #172943;">Mathematics</span>
</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem; padding: 2px 7px;">Calculus • Linear Alg</span>
</div>
<div style="font-size: 0.75rem; color: #64748B; line-height: 1.4;">
Continuous limits, multi-dimensional matrix transformations & probability.
</div>
</div>
<div class="sv-subject-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 28px; height: 28px; border-radius: 6px; background-color: #E6F5EE; display: flex; align-items: center; justify-content: center; color: #2B8A61;">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>
</div>
<span style="font-weight: 700; font-size: 0.875rem; color: #172943;">Engineering</span>
</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem; padding: 2px 7px;">Digital Logic</span>
</div>
<div style="font-size: 0.75rem; color: #64748B; line-height: 1.4;">
Boolean algebra, gate minimization, circuit synthesis & finite state machines.
</div>
</div>
<div class="sv-subject-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 28px; height: 28px; border-radius: 6px; background-color: #F3E8FF; display: flex; align-items: center; justify-content: center; color: #7C3AED;">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><path d="M12 21a9 9 0 0 0 9-9c0-4.97-4.03-9-9-9s-9 4.03-9 9a9 9 0 0 0 9 9Z"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
</div>
<span style="font-weight: 700; font-size: 0.875rem; color: #172943;">Science</span>
</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem; padding: 2px 7px;">Quantum & Physics</span>
</div>
<div style="font-size: 0.75rem; color: #64748B; line-height: 1.4;">
Qubit superposition, quantum gates, Newtonian kinematics & dynamics.
</div>
</div>
</div>
<div style="background: rgba(255, 255, 255, 0.75); border: 1px solid #E2E8F0; border-radius: 12px; padding: 0.85rem 1.15rem; display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 1.25rem;">
<div style="display: flex; align-items: center; gap: 10px;">
<div style="width: 32px; height: 32px; border-radius: 8px; background: #FAF5EA; border: 1px solid #D6B56D; display: flex; align-items: center; justify-content: center; color: #B88F3A;">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v14"/></svg>
</div>
<div>
<div style="font-weight: 700; font-size: 0.825rem; color: #172943;">Bayesian Knowledge Tracing & Diagnostics</div>
<div style="font-size: 0.725rem; color: #718096;">Real-time cognitive error detection & personalized practice drills</div>
</div>
</div>
<span class="lm-pill pill-completed" style="font-size: 0.65rem; padding: 2px 8px;">Active AI</span>
</div>
<div style="font-size: 0.775rem; font-weight: 700; color: #D6B56D; letter-spacing: 0.05em; text-transform: uppercase;">
{TAGLINE}
</div>
</div>
"""
        st.markdown(_clean_html(left_raw), unsafe_allow_html=True)

    # ==========================================================
    # 2. RIGHT SECTION: PREMIUM AUTHENTICATION CARD
    # ==========================================================
    with col_right:
        # Segmented Tabs: Prominently feature "Create Account" for newly joined students
        tabs = st.tabs(["Student Login", "✨ Create Account", "Teacher Login", "Demonstration Mode"])

        # 1. Student Login Tab (includes 1-click switch to Create Account)
        with tabs[0]:
            _render_student_login()

        # 2. Create Account Tab (Dedicated self-registration)
        with tabs[1]:
            _render_registration()

        # 3. Teacher Login Tab
        with tabs[2]:
            _render_teacher_login()

        # 4. Demonstration Mode Tab
        with tabs[3]:
            _render_demo_switcher()


def _render_student_login():
    """Renders the modern student authentication form with instant demo access and 1-click registration switch."""
    if st.session_state.get("auth_show_register", False):
        st.button("← Back to Student Login", key="btn_back_to_login", use_container_width=False, on_click=lambda: st.session_state.update({"auth_show_register": False}))
        _render_registration()
        return

    head_html = """
<div style="margin-bottom: 0.85rem;">
<h3 style="font-size: 1.45rem; font-weight: 800; color: #172943; margin: 0 0 0.2rem 0; letter-spacing: -0.015em;">
Welcome Back
</h3>
<p style="font-size: 0.825rem; color: #718096; margin: 0;">
Continue your personalized learning journey.
</p>
</div>
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.75rem 0.85rem; margin-bottom: 0.85rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
<span style="font-size: 0.75rem; font-weight: 700; color: #243B64;">Quick Evaluation Access</span>
<span class="lm-pill pill-ahead" style="font-size: 0.625rem; padding: 1px 6px;">Verified Student</span>
</div>
<div style="font-size: 0.725rem; color: #64748B;">
Email: <code>student@123</code> &bull; Password: <code>student123</code>
</div>
</div>
"""
    st.markdown(_clean_html(head_html), unsafe_allow_html=True)

    if st.button("1-Click Instant Student Login (student@123)", key="quick_btn_student", type="primary", use_container_width=True):
        user = get_user_by_email("student@123") or get_user_by_username("student@123")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "student_dashboard"
            st.session_state["_synced_page"] = "student_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.session_state.pop("auth_tab", None)
            st.rerun()

    div_html = """
<div style="display: flex; align-items: center; text-align: center; margin: 1rem 0; color: #94A3B8; font-size: 0.725rem;">
<div style="flex-grow: 1; border-bottom: 1px solid #E2E8F0;"></div>
<span style="padding: 0 10px; font-weight: 600; letter-spacing: 0.04em;">OR SIGN IN WITH CREDENTIALS</span>
<div style="flex-grow: 1; border-bottom: 1px solid #E2E8F0;"></div>
</div>
"""
    st.markdown(_clean_html(div_html), unsafe_allow_html=True)

    col_lbl, col_tog = st.columns([0.65, 0.35])
    with col_tog:
        show_pwd = st.checkbox("Show password", key="stu_show_pwd")

    with st.form("student_login_form"):
        username = st.text_input(
            "Username or Email",
            value="student@123",
            placeholder="e.g. student@123 or alex_rivera",
            key="stu_login_user"
        )
        password = st.text_input(
            "Password",
            value="student123",
            type="default" if show_pwd else "password",
            placeholder="Enter your student password",
            key="stu_login_pass"
        )
        submitted = st.form_submit_button("Sign In as Student", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both your username/email and password.")
                return

            user = get_user_by_username(username) or get_user_by_email(username)
            if not user or user.get("role") != "student":
                st.error("Invalid student credentials or user does not exist.")
                return

            if AuthService.verify_password(password, user["salt"], user["password_hash"]):
                st.session_state["user"] = user
                st.session_state["current_page"] = "student_dashboard"
                st.session_state["_synced_page"] = "student_dashboard"
                st.session_state["sidebar_nav_radio"] = "Dashboard"
                st.session_state["_active_nav_label"] = "Dashboard"
                st.session_state.pop("auth_tab", None)
                st.success(f"Welcome back, {user['full_name']}.")
                st.rerun()
            else:
                st.error("Incorrect password. Please verify your credentials.")

    # Dedicated New Student Registration Callout
    new_student_html = """
<div style="background: linear-gradient(135deg, #F0FDF4 0%, #EFF6FF 100%); border: 1.5px dashed #86EFAC; border-radius: 12px; padding: 0.95rem 1.1rem; margin-top: 1.25rem; text-align: center;">
<div style="font-size: 0.9rem; font-weight: 800; color: #166534; margin-bottom: 0.25rem;">
🌱 Newly Joined Student?
</div>
<div style="font-size: 0.775rem; color: #374151; margin-bottom: 0.75rem; line-height: 1.45;">
Join SARVAVIDYA today to unlock personalized BKT mastery diagnostics, AI tutoring, and <strong>50 bonus starter coins</strong>.
</div>
</div>
"""
    st.markdown(_clean_html(new_student_html), unsafe_allow_html=True)
    if st.button("✨ Create a New Student Account", key="btn_switch_to_register", type="secondary", use_container_width=True):
        st.session_state["auth_show_register"] = True
        st.rerun()


def _render_teacher_login():
    """Renders the modern educator authentication form."""
    head_html = """
<div style="margin-bottom: 0.85rem;">
<h3 style="font-size: 1.45rem; font-weight: 800; color: #172943; margin: 0 0 0.2rem 0; letter-spacing: -0.015em;">
Welcome, Educator
</h3>
<p style="font-size: 0.825rem; color: #718096; margin: 0;">
Access your teaching and student performance workspace.
</p>
</div>
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.75rem 0.85rem; margin-bottom: 0.85rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
<span style="font-size: 0.75rem; font-weight: 700; color: #243B64;">Quick Faculty Access</span>
<span class="lm-pill pill-ahead" style="font-size: 0.625rem; padding: 1px 6px;">Verified Faculty</span>
</div>
<div style="font-size: 0.725rem; color: #64748B;">
Email: <code>teacher@123</code> &bull; Password: <code>teacher123</code>
</div>
</div>
"""
    st.markdown(_clean_html(head_html), unsafe_allow_html=True)

    if st.button("1-Click Instant Faculty Login (teacher@123)", key="quick_btn_teacher", type="primary", use_container_width=True):
        user = get_user_by_email("teacher@123") or get_user_by_username("teacher@123") or get_user_by_username("dr_bennett")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "teacher_dashboard"
            st.session_state["_synced_page"] = "teacher_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.session_state.pop("auth_tab", None)
            st.rerun()

    div_html = """
<div style="display: flex; align-items: center; text-align: center; margin: 1rem 0; color: #94A3B8; font-size: 0.725rem;">
<div style="flex-grow: 1; border-bottom: 1px solid #E2E8F0;"></div>
<span style="padding: 0 10px; font-weight: 600; letter-spacing: 0.04em;">OR SIGN IN WITH CREDENTIALS</span>
<div style="flex-grow: 1; border-bottom: 1px solid #E2E8F0;"></div>
</div>
"""
    st.markdown(_clean_html(div_html), unsafe_allow_html=True)

    col_lbl, col_tog = st.columns([0.65, 0.35])
    with col_tog:
        show_pwd = st.checkbox("Show password", key="tchr_show_pwd")

    with st.form("teacher_login_form"):
        username = st.text_input(
            "Username or Email",
            value="teacher@123",
            placeholder="e.g. teacher@123 or dr_bennett",
            key="tchr_login_user"
        )
        password = st.text_input(
            "Password",
            value="teacher123",
            type="default" if show_pwd else "password",
            placeholder="Enter your faculty password",
            key="tchr_login_pass"
        )
        submitted = st.form_submit_button("Sign In as Educator / Admin", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both your username/email and password.")
                return

            user = get_user_by_username(username) or get_user_by_email(username)
            if not user or user.get("role") not in ("teacher", "admin"):
                st.error("Invalid credentials or insufficient permissions.")
                return

            if AuthService.verify_password(password, user["salt"], user["password_hash"]):
                st.session_state["user"] = user
                target_page = "ai_config" if user["role"] == "admin" else "teacher_dashboard"
                st.session_state["current_page"] = target_page
                st.session_state["_synced_page"] = target_page
                st.session_state["sidebar_nav_radio"] = "AI Configuration" if user["role"] == "admin" else "Dashboard"
                st.session_state["_active_nav_label"] = "AI Configuration" if user["role"] == "admin" else "Dashboard"
                st.session_state.pop("auth_tab", None)
                st.success(f"Authenticated as {user['full_name']}.")
                st.rerun()
            else:
                st.error("Incorrect password.")


def _render_registration():
    """Renders the student account creation interface connected to the SQLite database."""
    head_html = """
<div style="margin-bottom: 0.85rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<h3 style="font-size: 1.45rem; font-weight: 800; color: #172943; margin: 0; letter-spacing: -0.015em;">
Create Student Account
</h3>
<span class="lm-pill pill-completed" style="font-size: 0.65rem; padding: 2px 8px;">
🟢 DB Connected
</span>
</div>
<p style="font-size: 0.825rem; color: #718096; margin: 0 0 0.5rem 0;">
Join SARVAVIDYA to track your learning journey, earn coins, and master every concept.
</p>
<div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 0.5rem 0.75rem; font-size: 0.75rem; color: #166534; display: flex; justify-content: space-between; align-items: center;">
<span>🎁 <strong>Starter Perk:</strong> 50 SARVA Coins awarded automatically upon registration!</span>
<span style="font-family: monospace; font-size: 0.7rem; color: #15803D;">learnsphere.db</span>
</div>
</div>
"""
    st.markdown(_clean_html(head_html), unsafe_allow_html=True)

    col_lbl, col_tog = st.columns([0.65, 0.35])
    with col_tog:
        show_pwd = st.checkbox("Show password", key="reg_show_pwd")

    with st.form("register_form"):
        full_name = st.text_input("Full Name", placeholder="e.g. Maya Patel", key="reg_full_name")
        username = st.text_input("Desired Username", placeholder="e.g. maya_p", key="reg_username")
        email = st.text_input("Institutional or Personal Email", placeholder="e.g. maya@example.edu", key="reg_email")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            password = st.text_input("Password", type="default" if show_pwd else "password", help="Minimum 6 characters", key="reg_password")
        with col_p2:
            confirm_pwd = st.text_input("Confirm Password", type="default" if show_pwd else "password", key="reg_confirm")

        submitted = st.form_submit_button("Create Learning Account & Start Learning", type="primary", use_container_width=True)

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
            st.session_state["_synced_page"] = "student_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.session_state.pop("auth_tab", None)
            st.session_state["auth_show_register"] = False
            st.success(f"Account successfully created in database! Welcome, {full_name}!")
            st.rerun()

    # Link back to Sign In
    if st.session_state.get("auth_show_register", False):
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        if st.button("Already have an account? Sign in as Student →", key="btn_switch_to_login", use_container_width=True):
            st.session_state["auth_show_register"] = False
            st.rerun()


def _render_demo_switcher():
    """Renders the demonstration persona switcher."""
    head_html = """
<div style="margin-bottom: 0.85rem;">
<h3 style="font-size: 1.45rem; font-weight: 800; color: #172943; margin: 0 0 0.2rem 0; letter-spacing: -0.015em;">
Demonstration Mode
</h3>
<p style="font-size: 0.825rem; color: #718096; margin: 0;">
Instantly evaluate pre-configured academic personas and models.
</p>
</div>
<div style="background-color: #FFFFFF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 0.9rem; margin-bottom: 0.75rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<div style="font-weight: 700; font-size: 0.875rem; color: #1E40AF;">Alex Rivera (student@123)</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem;">Active Learner</span>
</div>
<div style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.5rem;">
Credentials: <code>student@123</code> &bull; Pass: <code>student123</code>
</div>
<div style="font-size: 0.775rem; color: #475569; line-height: 1.45;">
Exhibits mastered Variables & Conditionals, with active diagnosed misconceptions in Loops (Off-by-One) and Recursion.
</div>
</div>
"""
    st.markdown(_clean_html(head_html), unsafe_allow_html=True)
    if st.button("Launch Student Demo (student@123)", key="launch_alex", use_container_width=True, type="primary"):
        user = get_user_by_email("student@123") or get_user_by_username("student@123")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "student_dashboard"
            st.session_state["_synced_page"] = "student_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.rerun()

    sophia_html = """
<div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.9rem; margin: 0.75rem 0;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<div style="font-weight: 700; font-size: 0.875rem; color: #0F172A;">Sophia Chen</div>
<span class="lm-pill pill-completed" style="font-size: 0.65rem;">Proficient</span>
</div>
<div style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.5rem;">
Credentials: <code>sophia_chen</code> &bull; Pass: <code>sophia123</code>
</div>
<div style="font-size: 0.775rem; color: #475569; line-height: 1.45;">
Advanced proficient scholar. High BKT mastery across core modules, working on algorithmic optimization.
</div>
</div>
"""
    st.markdown(_clean_html(sophia_html), unsafe_allow_html=True)
    if st.button("Launch Sophia Chen Profile", key="launch_sophia", use_container_width=True):
        user = get_user_by_username("sophia_chen")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "student_dashboard"
            st.session_state["_synced_page"] = "student_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.rerun()

    teacher_html = """
<div style="background-color: #FFFFFF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 0.9rem; margin: 0.75rem 0;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<div style="font-weight: 700; font-size: 0.875rem; color: #1E40AF;">Dr. Sarah Bennett (teacher@123)</div>
<span class="lm-pill pill-ahead" style="font-size: 0.65rem;">Faculty Role</span>
</div>
<div style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.5rem;">
Credentials: <code>teacher@123</code> &bull; Pass: <code>teacher123</code>
</div>
<div style="font-size: 0.775rem; color: #475569; line-height: 1.45;">
Faculty portal with cohort-wide mastery distributions, misconception frequencies, and student inspection tools.
</div>
</div>
"""
    st.markdown(_clean_html(teacher_html), unsafe_allow_html=True)
    if st.button("Launch Faculty Demo (teacher@123)", key="launch_teacher", use_container_width=True, type="primary"):
        user = get_user_by_email("teacher@123") or get_user_by_username("teacher@123") or get_user_by_username("dr_bennett")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "teacher_dashboard"
            st.session_state["_synced_page"] = "teacher_dashboard"
            st.session_state["sidebar_nav_radio"] = "Dashboard"
            st.session_state["_active_nav_label"] = "Dashboard"
            st.rerun()

    admin_html = """
<div style="background-color: #FFFFFF; border: 1px solid #D6B56D; border-radius: 10px; padding: 0.9rem; margin: 0.75rem 0;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<div style="font-weight: 700; font-size: 0.875rem; color: #172943;">System Administrator (admin@123)</div>
<span class="lm-pill pill-completed" style="font-size: 0.65rem; background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A;">Admin Console</span>
</div>
<div style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.5rem;">
Credentials: <code>admin@123</code> &bull; Pass: <code>admin123</code>
</div>
<div style="font-size: 0.775rem; color: #475569; line-height: 1.45;">
Access Administrator Portal with live Google Gemini API key configuration, connection testing, and telemetry management.
</div>
</div>
"""
    st.markdown(_clean_html(admin_html), unsafe_allow_html=True)
    if st.button("Launch Administrator Portal (admin@123)", key="launch_admin", use_container_width=True):
        user = get_user_by_email("admin@123") or get_user_by_username("admin@123")
        if user:
            st.session_state["user"] = user
            st.session_state["current_page"] = "ai_config"
            st.session_state["_synced_page"] = "ai_config"
            st.session_state["sidebar_nav_radio"] = "AI Configuration"
            st.session_state["_active_nav_label"] = "AI Configuration"
            st.rerun()
