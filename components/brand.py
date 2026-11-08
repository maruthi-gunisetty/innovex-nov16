"""
SARVAVIDYA: Centralized Brand Identity Component
Provides standardized rendering of the Sarva Vidya golden lotus emblem, typography,
and tagline across all application interfaces and views.
"""

import streamlit as st
import os

BRAND_NAME = "Sarva Vidya"
TAGLINE = "One Platform. Every Subject. Infinite Knowledge."

# Inline SVG Assets for instant, zero-latency rendering without network or file lookup delays
# Composition: Golden lotus combined with open book base on left, 4 distinct petals for disciplines,
# glowing AI geometric diamond node at center.
SYMBOL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" style="width: 100%; height: 100%; display: block;">
  <defs>
    <linearGradient id="svGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F5E0A3" />
      <stop offset="50%" stop-color="#D6B56D" />
      <stop offset="100%" stop-color="#B88F3A" />
    </linearGradient>
    <linearGradient id="svPetalLt" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBECC6" />
      <stop offset="100%" stop-color="#C59E4E" />
    </linearGradient>
    <linearGradient id="svPetalRt" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FBECC6" />
      <stop offset="100%" stop-color="#C59E4E" />
    </linearGradient>
    <radialGradient id="svCoreGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#F5E0A3" />
      <stop offset="80%" stop-color="#D6B56D" />
      <stop offset="100%" stop-color="#172943" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Open Book Base (Foundation of Wisdom) -->
  <g id="book-base">
    <path d="M 60,86 C 44,85 26,89 16,95 C 16,77 34,70 60,71 Z" fill="url(#svGoldGrad)" opacity="0.95" />
    <path d="M 60,86 C 46,84 32,87 20,92 C 22,78 38,73 60,74 Z" fill="#172943" opacity="0.25" />
    <path d="M 60,86 C 76,85 94,89 104,95 C 104,77 86,70 60,71 Z" fill="url(#svGoldGrad)" opacity="0.95" />
    <path d="M 60,86 C 74,84 88,87 100,92 C 98,78 82,73 60,74 Z" fill="#172943" opacity="0.25" />
    <line x1="60" y1="71" x2="60" y2="88" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.9" />
  </g>

  <!-- 4 Lotus Petals (Programming, Mathematics, Engineering, Science) -->
  <g id="lotus-petals">
    <!-- 1. Outer Left: Programming -->
    <path d="M 60,71 C 45,68 25,62 18,45 C 18,36 29,32 38,39 C 48,47 56,60 60,71 Z" fill="url(#svPetalLt)" opacity="0.95" />
    <!-- 2. Inner Left: Mathematics -->
    <path d="M 60,71 C 52,58 40,44 48,22 C 55,20 60,33 60,71 Z" fill="url(#svGoldGrad)" opacity="0.98" />
    <!-- 3. Inner Right: Engineering -->
    <path d="M 60,71 C 60,33 65,20 72,22 C 80,44 68,58 60,71 Z" fill="url(#svGoldGrad)" opacity="0.98" />
    <!-- 4. Outer Right: Science -->
    <path d="M 60,71 C 64,60 72,47 82,39 C 91,32 102,36 102,45 C 95,62 75,68 60,71 Z" fill="url(#svPetalRt)" opacity="0.95" />
  </g>

  <!-- Central AI Geometric Diamond Core with Glowing Apex -->
  <g id="ai-core">
    <line x1="60" y1="71" x2="60" y2="46" stroke="#FFFFFF" stroke-width="1.4" stroke-dasharray="2,2" opacity="0.8" />
    <polygon points="60,35 64,43.5 72,46 64,48.5 60,57 56,48.5 48,46 56,43.5" fill="url(#svGoldGrad)" stroke="#FFFFFF" stroke-width="1" />
    <circle cx="60" cy="46" r="3.5" fill="url(#svCoreGlow)" />
    <circle cx="60" cy="46" r="1.6" fill="#FFFFFF" />
  </g>
</svg>"""


def get_symbol_html(size: int = 36) -> str:
    """Returns HTML wrapper for the golden lotus symbol."""
    return f"""<div style="width: {size}px; height: {size}px; min-width: {size}px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;">
        {SYMBOL_SVG}
    </div>"""


def render_sidebar_brand():
    """
    Renders the Sarva Vidya brand lockup in the navigation sidebar.
    Directly replaces the old [LS] blue badge with the Golden Lotus + Book + AI emblem,
    and replaces 'LearnSphereAI' with 'Sarva Vidya'.
    """
    st.markdown(f"""
    <div style="padding: 0.2rem 0 0.75rem 0; display: flex; align-items: center; gap: 9px; border-bottom: 1px solid #E4E8ED; margin-bottom: 0.75rem;">
        <div style="width: 36px; height: 36px; min-width: 36px; background: #172943; border: 1.5px solid #D6B56D; border-radius: 9px; display: flex; align-items: center; justify-content: center; padding: 3px; box-shadow: 0 2px 6px rgba(23, 41, 67, 0.2);">
            {SYMBOL_SVG}
        </div>
        <div style="line-height: 1.18; overflow: hidden;">
            <div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; font-size: 1.15rem; color: #172943; letter-spacing: -0.02em;">
                Sarva <span style="color: #D6B56D;">Vidya</span>
            </div>
            <div style="font-size: 0.625rem; color: #718096; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 0.02em; margin-top: 1px;">
                One Platform &bull; Infinite Knowledge
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_topbar_brand():
    """Renders the compact Sarva Vidya logo in the top horizontal bar."""
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; padding-top: 0.2rem;">
        <div style="width: 30px; height: 30px; min-width: 30px; background: #172943; border: 1.2px solid #D6B56D; border-radius: 7px; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 1px 4px rgba(23, 41, 67, 0.15);">
            {SYMBOL_SVG}
        </div>
        <div style="line-height: 1.1;">
            <div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; font-size: 1.05rem; color: #172943; letter-spacing: -0.01em;">
                Sarva <span style="color: #D6B56D;">Vidya</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_full_hero_brand(center: bool = True):
    """Renders the full Sarva Vidya brand lockup for landing and authentication pages."""
    align_style = "text-align: center; justify-content: center;" if center else "text-align: left; justify-content: flex-start;"
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: {'center' if center else 'flex-start'}; margin-bottom: 1.25rem;">
        <div style="display: inline-flex; align-items: center; gap: 14px; margin-bottom: 0.5rem;">
            <div style="width: 54px; height: 54px; min-width: 54px; background: #172943; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 5px; box-shadow: 0 4px 12px rgba(23, 41, 67, 0.22); border: 1.5px solid #D6B56D;">
                {SYMBOL_SVG}
            </div>
            <div style="text-align: left; line-height: 1.05;">
                <div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 2.2rem; font-weight: 800; color: #172943; letter-spacing: -0.02em;">
                    Sarva <span style="color: #D6B56D;">Vidya</span>
                </div>
            </div>
        </div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #D6B56D; letter-spacing: 0.05em; text-transform: uppercase;">
            {TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)
