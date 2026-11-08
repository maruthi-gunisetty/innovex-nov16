"""
LearnSphere AI: Premium Modern SaaS Design System
Inspired by Linear, Stripe, and Notion.
Clean minimalist layout, strict color tokens, Inter typography, and zero emojis.
"""

ICONS = {
    "brain": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v14"/></svg>""",
    "target": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "book": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>""",
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>""",
    "compass": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
    "shield": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>""",
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>"""
}


CUSTOM_CSS = """
<style>
/* Modern Typography System - Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #0F172A;
    background-color: #F8FAFC;
}

/* Container Structure */
.block-container {
    padding-top: 1.25rem;
    padding-bottom: 2.5rem;
    max-width: 1200px;
}

/* Header Brand Navigation Bar */
.ls-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.25rem;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
}

.ls-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: #172554;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ls-brand span {
    color: #635BDB;
}

/* Modern Card Containers */
.ls-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03), 0 1px 2px -1px rgba(15, 23, 42, 0.03);
    transition: border-color 0.15s ease;
}

.ls-card:hover {
    border-color: #CBD5E1;
}

.ls-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 0.75rem;
}

.ls-card-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.015em;
}

.ls-card-desc {
    color: #64748B;
    font-size: 0.825rem;
    margin-top: 0.2rem;
    line-height: 1.5;
}

/* Linear-Style Minimal Metric Boxes */
.ls-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.ls-metric-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.ls-metric-box:hover {
    border-color: #CBD5E1;
    transform: translateY(-1px);
}

.ls-metric-label {
    font-size: 0.725rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748B;
    margin-bottom: 0.4rem;
}

.ls-metric-val {
    font-size: 1.85rem;
    font-weight: 700;
    color: #172554;
    line-height: 1.2;
    letter-spacing: -0.03em;
}

.ls-metric-sub {
    font-size: 0.775rem;
    color: #64748B;
    margin-top: 0.35rem;
}

/* Crisp Badges and Status Indicators */
.ls-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.725rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.badge-mastered {
    background-color: #F0FDF4;
    color: #16A34A;
    border: 1px solid #BBF7D0;
}

.badge-proficient {
    background-color: #EFF6FF;
    color: #2563EB;
    border: 1px solid #BFDBFE;
}

.badge-developing {
    background-color: #FFFBEB;
    color: #D97706;
    border: 1px solid #FDE68A;
}

.badge-novice {
    background-color: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
}

.badge-violet {
    background-color: #EEF2FF;
    color: #635BDB;
    border: 1px solid #C7D2FE;
}

.badge-demo {
    background-color: #F8FAFC;
    color: #475569;
    border: 1px solid #E2E8F0;
}

/* Callout Diagnostics */
.ls-diagnostic-box {
    background-color: #FFF1F2;
    border-left: 4px solid #DC2626;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

.ls-success-box {
    background-color: #F0FDF4;
    border-left: 4px solid #16A34A;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

.ls-info-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #635BDB;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

/* Clean Stripe-Style Data Table */
.ls-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}

.ls-table th {
    background-color: #F8FAFC;
    color: #475569;
    font-weight: 600;
    text-align: left;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #E2E8F0;
    font-size: 0.775rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.ls-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #F1F5F9;
    color: #0F172A;
}

.ls-table tr:hover td {
    background-color: #F8FAFC;
}

/* Form Controls and Streamlit Polish */
button[kind="primary"] {
    background-color: #172554 !important;
    border: 1px solid #172554 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    transition: all 0.15s ease !important;
}

button[kind="primary"]:hover {
    background-color: #1E3A8A !important;
    border-color: #1E3A8A !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}

button[kind="secondary"]:hover {
    border-color: #CBD5E1 !important;
    background-color: #F8FAFC !important;
}

/* Progress Bar Customization */
.stProgress > div > div > div > div {
    background-color: #635BDB !important;
}

/* Footer Minimalist */
.ls-footer {
    text-align: center;
    padding: 2.5rem 0 1rem 0;
    margin-top: 3rem;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
    font-size: 0.8rem;
}
</style>
"""


def get_icon(name: str) -> str:
    """Returns SVG icon string by name or empty string if not found."""
    return ICONS.get(name, "")


def render_card(title: str, content_html: str, subtitle: str = "") -> str:
    """Renders a standard SaaS card HTML snippet."""
    sub_html = f"<div class='ls-card-desc'>{subtitle}</div>" if subtitle else ""
    return f"""
    <div class="ls-card">
        <div class="ls-card-header">
            <div>
                <h3 class="ls-card-title">{title}</h3>
                {sub_html}
            </div>
        </div>
        <div>
            {content_html}
        </div>
    </div>
    """


def render_metric(label: str, value: str, subtext: str = "") -> str:
    """Renders a metric container HTML snippet."""
    sub_html = f"<div class='ls-metric-sub'>{subtext}</div>" if subtext else ""
    return f"""
    <div class="ls-metric-box">
        <div class="ls-metric-label">{label}</div>
        <div class="ls-metric-val">{value}</div>
        {sub_html}
    </div>
    """
