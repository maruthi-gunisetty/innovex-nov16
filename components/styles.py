"""
SARVAVIDYA: Enterprise Educational Management Design System
Brand Identity:
- Deep Navy: #172943
- Royal Navy: #243B64
- Premium Gold: #D6B56D
- Soft Gold: #E8C879
- White: #FFFFFF
- Canvas Background: #F5F6F8
- Borders: #E4E8ED
- Success: #36A879, Warning: #E9AA45, Danger: #D96B6B
Tagline: One Platform. Every Subject. Infinite Knowledge.
Zero emojis, strict professional typography, and compact information density.
"""

ICONS = {
    "dashboard": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>""",
    "assessment": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>""",
    "ai": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v14"/></svg>""",
    "path": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
    "library": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>""",
    "progress": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "users": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "analytics": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>""",
    "profile": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>""",
    "settings": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>""",
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/></svg>""",
    "bell": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>""",
    "trophy": """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#D6B56D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>""",
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>"""
}

CUSTOM_CSS = """
<style>
/* Modern Typography - Roboto & Material Symbols */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400;1,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], button, input, textarea, select, div, span, p, h1, h2, h3, h4, h5, h6 {
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #172943;
    background-color: #F5F6F8;
}

*:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded):not([class*="material-symbols"]) {
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

[data-testid="stIconMaterial"], .material-symbols-rounded, [class*="material-symbols"] {
    font-family: 'Material Symbols Rounded' !important;
}

/* Completely eliminate Streamlit default header, decoration, and rerun toolbar overlay */
header[data-testid="stHeader"],
[data-testid="stHeader"],
.stAppHeader,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
    visibility: hidden !important;
    z-index: -9999 !important;
}

.stApp > header {
    display: none !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Page Container Density - Zero Top Gap */
.block-container,
[data-testid="stAppViewBlockContainer"],
.main .block-container {
    padding-top: 0.35rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 1320px !important;
}

/* Sidebar Customization - Compact White 225px, Always Visible */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    margin-left: 0 !important;
    background-color: #FFFFFF !important;
    border-right: 1px solid #E4E8ED !important;
    width: 225px !important;
    min-width: 210px !important;
    max-width: 240px !important;
    z-index: 100 !important;
}

/* Ensure sidebar collapse toggle button is accessible if needed */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 999999 !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

/* Sidebar Radio Navigation */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.25rem !important;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 0.45rem 0.65rem !important;
    border-radius: 8px !important;
    font-size: 0.825rem !important;
    font-weight: 500 !important;
    color: #718096 !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background-color: #F8FAFC !important;
    color: #172943 !important;
}

[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio label[data-selected="true"],
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background-color: #FAF5EA !important;
    color: #172943 !important;
    font-weight: 600 !important;
    border-left: 3px solid #D6B56D !important;
}

/* ==========================================================
   GLOBAL RADIO BUTTON STYLING (Sidebar & Assessment Pages)
   Ensures the radio circle fills with gold (#D6B56D) when selected.
   ========================================================== */

/* 1. Unselected Radio Circle: Neutral border with clean white interior */
.stRadio [data-testid="stRadioOption"] div[class*="ex50key4"],
.stRadio [data-testid="stRadioOption"] > div > div:first-child,
.stRadio label > div > div:first-child,
div[role="radiogroup"] label > div > div:first-child,
[data-testid="stRadioGroup"] label > div > div:first-child {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 50% !important;
    width: 16px !important;
    height: 16px !important;
    min-width: 16px !important;
    min-height: 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease !important;
    box-sizing: border-box !important;
}

/* 2. Unselected Inner Dot (Hidden) */
.stRadio [data-testid="stRadioOption"] div[class*="ex50key5"],
.stRadio [data-testid="stRadioOption"] > div > div:first-child > div,
.stRadio label > div > div:first-child > div,
div[role="radiogroup"] label > div > div:first-child > div,
[data-testid="stRadioGroup"] label > div > div:first-child > div {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
}

/* 3. Hover state for unselected radio circle */
.stRadio [data-testid="stRadioOption"]:hover div[class*="ex50key4"],
.stRadio [data-testid="stRadioOption"]:hover > div > div:first-child,
.stRadio label:hover > div > div:first-child,
div[role="radiogroup"] label:hover > div > div:first-child {
    border-color: #D6B56D !important;
    background-color: #FAF5EA !important;
}

/* 4. SELECTED Radio Circle: Fills with Gold (#D6B56D) */
.stRadio [data-testid="stRadioOption"]:has(input:checked) div[class*="ex50key4"],
.stRadio [data-testid="stRadioOption"][data-selected="true"] div[class*="ex50key4"],
.stRadio [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child,
.stRadio [data-testid="stRadioOption"][data-selected="true"] > div > div:first-child,
.stRadio label:has(input:checked) div[class*="ex50key4"],
.stRadio label[data-selected="true"] div[class*="ex50key4"],
.stRadio label:has(input:checked) > div > div:first-child,
.stRadio label[data-selected="true"] > div > div:first-child,
.stRadio label[data-checked="true"] > div > div:first-child,
.stRadio label[aria-checked="true"] > div > div:first-child,
div[role="radiogroup"] label:has(input:checked) > div > div:first-child,
div[role="radiogroup"] label[data-selected="true"] > div > div:first-child,
div[role="radiogroup"] label[aria-checked="true"] > div > div:first-child,
[data-testid="stRadioGroup"] label:has(input:checked) > div > div:first-child,
[data-testid="stRadioGroup"] label[data-selected="true"] > div > div:first-child {
    background-color: #D6B56D !important;
    border: 2px solid #D6B56D !important;
    box-shadow: 0 0 0 2px rgba(214, 181, 109, 0.28) !important;
}

/* 5. SELECTED Radio Inner Dot: Crisp 6px white center dot */
.stRadio [data-testid="stRadioOption"]:has(input:checked) div[class*="ex50key5"],
.stRadio [data-testid="stRadioOption"][data-selected="true"] div[class*="ex50key5"],
.stRadio [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child > div,
.stRadio [data-testid="stRadioOption"][data-selected="true"] > div > div:first-child > div,
.stRadio label:has(input:checked) div[class*="ex50key5"],
.stRadio label[data-selected="true"] div[class*="ex50key5"],
.stRadio label:has(input:checked) > div > div:first-child > div,
.stRadio label[data-selected="true"] > div > div:first-child > div,
.stRadio label[data-checked="true"] > div > div:first-child > div,
.stRadio label[aria-checked="true"] > div > div:first-child > div,
div[role="radiogroup"] label:has(input:checked) > div > div:first-child > div,
div[role="radiogroup"] label[data-selected="true"] > div > div:first-child > div,
div[role="radiogroup"] label[aria-checked="true"] > div > div:first-child > div,
[data-testid="stRadioGroup"] label:has(input:checked) > div > div:first-child > div,
[data-testid="stRadioGroup"] label[data-selected="true"] > div > div:first-child > div {
    display: block !important;
    background-color: #FFFFFF !important;
    width: 6px !important;
    height: 6px !important;
    min-width: 6px !important;
    min-height: 6px !important;
    border-radius: 50% !important;
    margin: auto !important;
    opacity: 1 !important;
}

/* Top Navigation Bar */
.lm-topbar {
    background-color: #FFFFFF;
    border: 1px solid #E4E8ED;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(23, 41, 67, 0.04);
}

.lm-search-box {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: #F5F6F8;
    border: 1px solid #E4E8ED;
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
    color: #718096;
    font-size: 0.8rem;
    width: 300px;
}

/* Sleek Interactive Top Navigation Search Input */
[data-testid="stTextInput"]:has(input[placeholder*="Search for concepts"]) {
    margin-bottom: 0 !important;
}

[data-testid="stTextInput"]:has(input[placeholder*="Search for concepts"]) > div {
    background-color: transparent !important;
    border: none !important;
}

[data-testid="stTextInput"]:has(input[placeholder*="Search for concepts"]) input {
    background-color: #F5F6F8 !important;
    border: 1px solid #E4E8ED !important;
    border-radius: 8px !important;
    padding: 0.35rem 0.75rem 0.35rem 2.2rem !important;
    font-size: 0.8rem !important;
    color: #172943 !important;
    height: 35px !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23718096' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: 10px center !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextInput"]:has(input[placeholder*="Search for concepts"]) input:focus {
    border-color: #D6B56D !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 0 0 2px rgba(214, 181, 109, 0.22) !important;
    color: #172943 !important;
}

/* Quick Search Clear & Popover Buttons in Top Bar */
button[key="top_search_clear_btn"] {
    height: 35px !important;
    min-height: 35px !important;
    border-radius: 8px !important;
    border: 1px solid #E4E8ED !important;
    background-color: #F5F6F8 !important;
    color: #718096 !important;
    font-weight: 700 !important;
}

button[key="top_search_clear_btn"]:hover {
    border-color: #D96B6B !important;
    color: #D96B6B !important;
    background-color: #FDF2F2 !important;
}

.lm-user-pill {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.lm-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #172943;
    color: #D6B56D;
    font-weight: 700;
    font-size: 0.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #D6B56D;
}

/* Reference Card Component */
.lm-card {
    background-color: #FFFFFF;
    border: 1px solid #E4E8ED;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 3px rgba(23, 41, 67, 0.03);
}

.lm-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
    padding-bottom: 0.4rem;
}

.lm-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #172943;
    margin: 0;
    letter-spacing: -0.01em;
}

.lm-card-link {
    font-size: 0.75rem;
    color: #D6B56D;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
}

/* 3-Column Top Stat Cards */
.lm-stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    text-align: center;
    gap: 0.5rem;
    padding: 0.75rem 0;
}

.lm-stat-col {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.lm-stat-icon-wrap {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.4rem;
}

.lm-stat-val {
    font-size: 1.45rem;
    font-weight: 700;
    color: #172943;
    line-height: 1.15;
}

.lm-stat-label {
    font-size: 0.75rem;
    color: #718096;
    margin-top: 0.2rem;
    font-weight: 500;
}

/* Progress bar inside card */
.lm-progress-wrap {
    background-color: #F5F6F8;
    border-radius: 9999px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.lm-progress-bar {
    background: linear-gradient(90deg, #D6B56D, #36A879);
    height: 100%;
    border-radius: 9999px;
}

/* Reference Status Pills */
.lm-pill {
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    text-transform: capitalize;
}

.pill-lagging {
    background-color: #FDF2F2;
    color: #D96B6B;
    border: 1px solid #F8D7DA;
}

.pill-ontrack {
    background-color: #FEF9EE;
    color: #E9AA45;
    border: 1px solid #FDE8C7;
}

.pill-ahead {
    background-color: #FAF5EA;
    color: #BA9447;
    border: 1px solid #E8C879;
}

.pill-completed {
    background-color: #EDF8F3;
    color: #36A879;
    border: 1px solid #C6ECD9;
}

/* Bottom Sidebar Action Card */
.lm-sidebar-cta {
    background: linear-gradient(135deg, #172943, #243B64);
    border: 1px solid #D6B56D;
    border-radius: 12px;
    padding: 0.9rem;
    margin-top: 1rem;
    text-align: center;
    color: #FFFFFF;
}

.lm-sidebar-cta-icon {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background-color: #D6B56D;
    color: #172943;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.4rem;
}

/* Primary Button Styling */
button[kind="primary"] {
    background-color: #172943 !important;
    border: 1px solid #D6B56D !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-size: 0.825rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    box-shadow: 0 1px 3px rgba(23, 41, 67, 0.15) !important;
}

button[kind="primary"]:hover {
    background-color: #243B64 !important;
    border-color: #E8C879 !important;
    color: #FFFFFF !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #172943 !important;
    border: 1px solid #E4E8ED !important;
    border-radius: 8px !important;
    font-size: 0.825rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
}

button[kind="secondary"]:hover {
    background-color: #FAF5EA !important;
    border-color: #D6B56D !important;
    color: #172943 !important;
}

/* Tables */
.lm-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.825rem;
}

.lm-table th {
    background-color: #F5F6F8;
    color: #718096;
    font-weight: 600;
    text-align: left;
    padding: 0.6rem 0.85rem;
    border-bottom: 1px solid #E4E8ED;
    font-size: 0.725rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.lm-table td {
    padding: 0.6rem 0.85rem;
    border-bottom: 1px solid #F5F6F8;
    color: #172943;
}

.lm-table tr:hover td {
    background-color: #FAF5EA;
}

/* Popover styling for Login Portal */
[data-testid="stPopoverBody"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E4E8ED !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px rgba(23, 41, 67, 0.15) !important;
    padding: 1rem !important;
    max-width: 420px !important;
    z-index: 999999 !important;
}

[data-testid="stPopover"] button {
    border-radius: 8px !important;
    font-size: 0.825rem !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

[data-testid="stPopover"] button [data-testid="stIconMaterial"] {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1rem !important;
    line-height: 1 !important;
}
</style>
"""


def get_icon(name: str) -> str:
    """Returns SVG icon string by name."""
    return ICONS.get(name, "")
