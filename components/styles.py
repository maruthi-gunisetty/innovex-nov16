"""
LearnSphere AI: UI Style and Theme System
SaaS design tokens: Clean white/slate background, deep navy text,
indigo/purple accents, professional card containers, badges, and zero emojis.
"""

# Lucide-inspired SVG Icon helper
ICONS = {
    "brain": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v14"/></svg>""",
    "target": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "book": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>""",
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>""",
    "compass": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
    "shield": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>""",
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "arrow_right": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" x2="19" y1="12" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>""",
    "user": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>""",
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>"""
}


CUSTOM_CSS = """
<style>
/* Global SaaS Typography and Spacing */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #0f172a;
    background-color: #f8fafc;
}

/* Remove default Streamlit top decoration padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Header & Navigation Styling */
.ls-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 2rem;
    border-radius: 8px;
}

.ls-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ls-brand span {
    color: #4f46e5;
}

/* Card Containers */
.ls-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.ls-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.75rem;
}

.ls-card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}

.ls-card-desc {
    color: #64748b;
    font-size: 0.875rem;
    margin-top: 0.25rem;
    line-height: 1.5;
}

/* Metrics Displays */
.ls-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.ls-metric-box {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.ls-metric-label {
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    margin-bottom: 0.5rem;
}

.ls-metric-val {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
}

.ls-metric-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.4rem;
}

/* Badges and Status Pills */
.ls-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.badge-mastered {
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.badge-proficient {
    background-color: #eff6ff;
    color: #1e40af;
    border: 1px solid #bfdbfe;
}

.badge-developing {
    background-color: #fffbeb;
    color: #92400e;
    border: 1px solid #fde68a;
}

.badge-novice {
    background-color: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.badge-demo {
    background-color: #f5f3ff;
    color: #5b21b6;
    border: 1px solid #ddd6fe;
}

/* Misconception Diagnostic Callouts */
.ls-diagnostic-box {
    background-color: #fff1f2;
    border-left: 4px solid #e11d48;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

.ls-success-box {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

.ls-info-box {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #4f46e5;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem;
    margin: 1rem 0;
}

/* Custom Table Styling */
.ls-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}

.ls-table th {
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    text-align: left;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e2e8f0;
}

.ls-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
}

.ls-table tr:hover td {
    background-color: #f8fafc;
}

/* Question Option Containers */
.ls-option-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 0.875rem 1rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.15s ease;
}

.ls-option-card:hover {
    border-color: #4f46e5;
}

/* Footer */
.ls-footer {
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 0.825rem;
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

