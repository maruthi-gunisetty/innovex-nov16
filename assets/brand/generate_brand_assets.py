"""
SARVAVIDYA: Brand Identity Assets Generator
Creates production-grade vector SVGs and raster PNG icons for:
- Symbol Only (Lotus + Open Book + AI Diamond Core)
- Horizontal Full Logo (Light and Dark variants)
- 32x32 and 64x64 crisp Favicons
"""

import os
from PIL import Image, ImageDraw

BRAND_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. PURE SYMBOL SVG (ViewBox 0 0 120 120)
SYMBOL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="goldLinear" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8C879" />
      <stop offset="50%" stop-color="#D6B56D" />
      <stop offset="100%" stop-color="#BA9447" />
    </linearGradient>
    <linearGradient id="goldPetalLeft" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F2D898" />
      <stop offset="100%" stop-color="#C59E4E" />
    </linearGradient>
    <linearGradient id="goldPetalRight" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F2D898" />
      <stop offset="100%" stop-color="#C59E4E" />
    </linearGradient>
    <radialGradient id="aiCoreGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#E8C879" />
      <stop offset="80%" stop-color="#D6B56D" />
      <stop offset="100%" stop-color="#172943" stop-opacity="0" />
    </radialGradient>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Open Book Base (Foundation of Wisdom) -->
  <g id="open-book-base">
    <!-- Left Page Arc -->
    <path d="M 60,86 C 44,85 26,89 16,95 C 16,77 34,70 60,71 Z" 
          fill="url(#goldLinear)" opacity="0.9" />
    <path d="M 60,86 C 46,84 32,87 20,92 C 22,78 38,73 60,74 Z" 
          fill="#172943" opacity="0.25" />

    <!-- Right Page Arc -->
    <path d="M 60,86 C 76,85 94,89 104,95 C 104,77 86,70 60,71 Z" 
          fill="url(#goldLinear)" opacity="0.9" />
    <path d="M 60,86 C 74,84 88,87 100,92 C 98,78 82,73 60,74 Z" 
          fill="#172943" opacity="0.25" />

    <!-- Book Spine Rib -->
    <line x1="60" y1="71" x2="60" y2="88" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" opacity="0.8" />
  </g>

  <!-- 4 Elegant Lotus Petals (Programming, Mathematics, Engineering, Science) -->
  <g id="lotus-petals">
    <!-- 1. Outer Left Petal: Programming (Syntax & Computation) -->
    <path d="M 60,71 C 45,68 25,62 18,45 C 18,36 29,32 38,39 C 48,47 56,60 60,71 Z" 
          fill="url(#goldPetalLeft)" opacity="0.92" />

    <!-- 2. Inner Left Petal: Mathematics (Logic & Precision) -->
    <path d="M 60,71 C 52,58 40,44 48,22 C 55,20 60,33 60,71 Z" 
          fill="url(#goldLinear)" opacity="0.96" />

    <!-- 3. Inner Right Petal: Engineering (Systems & Design) -->
    <path d="M 60,71 C 60,33 65,20 72,22 C 80,44 68,58 60,71 Z" 
          fill="url(#goldLinear)" opacity="0.96" />

    <!-- 4. Outer Right Petal: Science (Observation & Discovery) -->
    <path d="M 60,71 C 64,60 72,47 82,39 C 91,32 102,36 102,45 C 95,62 75,68 60,71 Z" 
          fill="url(#goldPetalRight)" opacity="0.92" />
  </g>

  <!-- Central AI Geometric Core & Neural Node -->
  <g id="ai-core">
    <!-- Fine Geometric Synthesis Lines -->
    <line x1="60" y1="71" x2="60" y2="46" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="2,2" opacity="0.7" />
    <line x1="38" y1="39" x2="60" y2="46" stroke="#FFFFFF" stroke-width="0.8" opacity="0.45" />
    <line x1="48" y1="22" x2="60" y2="46" stroke="#FFFFFF" stroke-width="0.8" opacity="0.45" />
    <line x1="72" y1="22" x2="60" y2="46" stroke="#FFFFFF" stroke-width="0.8" opacity="0.45" />
    <line x1="82" y1="39" x2="60" y2="46" stroke="#FFFFFF" stroke-width="0.8" opacity="0.45" />

    <!-- Outer Diamond / Star Facet -->
    <polygon points="60,36 63.5,43.5 71,46 63.5,48.5 60,56 56.5,48.5 49,46 56.5,43.5" 
             fill="url(#goldLinear)" stroke="#FFFFFF" stroke-width="0.8" filter="url(#softGlow)" />

    <!-- Central Glowing AI Point -->
    <circle cx="60" cy="46" r="3.2" fill="url(#aiCoreGlow)" />
    <circle cx="60" cy="46" r="1.5" fill="#FFFFFF" />
  </g>
</svg>"""


# 2. FULL HORIZONTAL LOGO (LIGHT BACKGROUND)
LIGHT_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 84" width="100%" height="100%">
  <defs>
    <linearGradient id="goldLinearLt" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8C879" />
      <stop offset="50%" stop-color="#D6B56D" />
      <stop offset="100%" stop-color="#BA9447" />
    </linearGradient>
    <radialGradient id="aiCoreGlowLt" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E8C879" />
      <stop offset="100%" stop-color="#D6B56D" />
    </radialGradient>
  </defs>

  <!-- Left Lotus & Book Symbol (Scale 0.65, Offset x=8, y=3) -->
  <g transform="translate(4, 2) scale(0.68)">
    <!-- Book Base -->
    <path d="M 60,86 C 44,85 26,89 16,95 C 16,77 34,70 60,71 Z" fill="url(#goldLinearLt)" opacity="0.9" />
    <path d="M 60,86 C 76,85 94,89 104,95 C 104,77 86,70 60,71 Z" fill="url(#goldLinearLt)" opacity="0.9" />
    <line x1="60" y1="71" x2="60" y2="88" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" opacity="0.8" />
    
    <!-- Petals -->
    <path d="M 60,71 C 45,68 25,62 18,45 C 18,36 29,32 38,39 C 48,47 56,60 60,71 Z" fill="url(#goldLinearLt)" opacity="0.92" />
    <path d="M 60,71 C 52,58 40,44 48,22 C 55,20 60,33 60,71 Z" fill="url(#goldLinearLt)" opacity="0.98" />
    <path d="M 60,71 C 60,33 65,20 72,22 C 80,44 68,58 60,71 Z" fill="url(#goldLinearLt)" opacity="0.98" />
    <path d="M 60,71 C 64,60 72,47 82,39 C 91,32 102,36 102,45 C 95,62 75,68 60,71 Z" fill="url(#goldLinearLt)" opacity="0.92" />
    
    <!-- AI Core -->
    <line x1="60" y1="71" x2="60" y2="46" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="2,2" opacity="0.7" />
    <polygon points="60,36 63.5,43.5 71,46 63.5,48.5 60,56 56.5,48.5 49,46 56.5,43.5" fill="url(#goldLinearLt)" stroke="#FFFFFF" stroke-width="0.8" />
    <circle cx="60" cy="46" r="3.2" fill="url(#aiCoreGlowLt)" />
    <circle cx="60" cy="46" r="1.5" fill="#FFFFFF" />
  </g>

  <!-- Typography Block on RIGHT -->
  <g transform="translate(94, 0)">
    <!-- Brand Name SARVAVIDYA -->
    <text x="0" y="47" 
          font-family="'Roboto', -apple-system, sans-serif" 
          font-size="34" 
          font-weight="800" 
          letter-spacing="0.08em" 
          fill="#172943">
      SARVA<tspan fill="#D6B56D">VIDYA</tspan>
    </text>

    <!-- Tagline -->
    <text x="1" y="68" 
          font-family="'Roboto', -apple-system, sans-serif" 
          font-size="11.5" 
          font-weight="600" 
          letter-spacing="0.04em" 
          fill="#718096">
      One Platform. Every Subject. Infinite Knowledge.
    </text>
  </g>
</svg>"""


# 3. FULL HORIZONTAL LOGO (DARK BACKGROUND)
DARK_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 84" width="100%" height="100%">
  <defs>
    <linearGradient id="goldLinearDk" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F2D898" />
      <stop offset="50%" stop-color="#E8C879" />
      <stop offset="100%" stop-color="#D6B56D" />
    </linearGradient>
    <radialGradient id="aiCoreGlowDk" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E8C879" />
      <stop offset="100%" stop-color="#D6B56D" />
    </radialGradient>
  </defs>

  <!-- Left Lotus & Book Symbol -->
  <g transform="translate(4, 2) scale(0.68)">
    <!-- Book Base -->
    <path d="M 60,86 C 44,85 26,89 16,95 C 16,77 34,70 60,71 Z" fill="url(#goldLinearDk)" opacity="0.95" />
    <path d="M 60,86 C 76,85 94,89 104,95 C 104,77 86,70 60,71 Z" fill="url(#goldLinearDk)" opacity="0.95" />
    <line x1="60" y1="71" x2="60" y2="88" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" opacity="0.9" />
    
    <!-- Petals -->
    <path d="M 60,71 C 45,68 25,62 18,45 C 18,36 29,32 38,39 C 48,47 56,60 60,71 Z" fill="url(#goldLinearDk)" opacity="0.94" />
    <path d="M 60,71 C 52,58 40,44 48,22 C 55,20 60,33 60,71 Z" fill="url(#goldLinearDk)" opacity="0.98" />
    <path d="M 60,71 C 60,33 65,20 72,22 C 80,44 68,58 60,71 Z" fill="url(#goldLinearDk)" opacity="0.98" />
    <path d="M 60,71 C 64,60 72,47 82,39 C 91,32 102,36 102,45 C 95,62 75,68 60,71 Z" fill="url(#goldLinearDk)" opacity="0.94" />
    
    <!-- AI Core -->
    <line x1="60" y1="71" x2="60" y2="46" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.8" />
    <polygon points="60,36 63.5,43.5 71,46 63.5,48.5 60,56 56.5,48.5 49,46 56.5,43.5" fill="url(#goldLinearDk)" stroke="#FFFFFF" stroke-width="0.8" />
    <circle cx="60" cy="46" r="3.2" fill="url(#aiCoreGlowDk)" />
    <circle cx="60" cy="46" r="1.5" fill="#FFFFFF" />
  </g>

  <!-- Typography Block on RIGHT -->
  <g transform="translate(94, 0)">
    <!-- Brand Name SARVAVIDYA -->
    <text x="0" y="47" 
          font-family="'Roboto', -apple-system, sans-serif" 
          font-size="34" 
          font-weight="800" 
          letter-spacing="0.08em" 
          fill="#FFFFFF">
      SARVA<tspan fill="#E8C879">VIDYA</tspan>
    </text>

    <!-- Tagline -->
    <text x="1" y="68" 
          font-family="'Roboto', -apple-system, sans-serif" 
          font-size="11.5" 
          font-weight="600" 
          letter-spacing="0.04em" 
          fill="#D6B56D">
      One Platform. Every Subject. Infinite Knowledge.
    </text>
  </g>
</svg>"""


def generate_assets():
    os.makedirs(BRAND_DIR, exist_ok=True)

    # Write SVGs
    with open(os.path.join(BRAND_DIR, "sarvavidya_symbol.svg"), "w", encoding="utf-8") as f:
        f.write(SYMBOL_SVG.strip())

    with open(os.path.join(BRAND_DIR, "sarvavidya_logo_light.svg"), "w", encoding="utf-8") as f:
        f.write(LIGHT_LOGO_SVG.strip())

    with open(os.path.join(BRAND_DIR, "sarvavidya_logo_dark.svg"), "w", encoding="utf-8") as f:
        f.write(DARK_LOGO_SVG.strip())

    with open(os.path.join(BRAND_DIR, "sarvavidya_logo_horizontal.svg"), "w", encoding="utf-8") as f:
        f.write(LIGHT_LOGO_SVG.strip())

    # Generate crisp Favicon PNG using Pillow
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw navy rounded rectangle badge
    draw.rounded_rectangle([2, 2, size - 2, size - 2], radius=14, fill="#172943")

    # Draw gold book arc
    draw.arc([10, 40, 32, 54], start=180, end=360, fill="#D6B56D", width=3)
    draw.arc([32, 40, 54, 54], start=180, end=360, fill="#D6B56D", width=3)

    # Draw 4 gold lotus petal lines
    draw.line([32, 46, 16, 26], fill="#E8C879", width=2)
    draw.line([32, 46, 27, 16], fill="#D6B56D", width=2)
    draw.line([32, 46, 37, 16], fill="#D6B56D", width=2)
    draw.line([32, 46, 48, 26], fill="#E8C879", width=2)

    # Center glowing star
    draw.ellipse([30, 26, 34, 30], fill="#FFFFFF", outline="#E8C879", width=1)

    img.save(os.path.join(BRAND_DIR, "favicon.png"), "PNG")
    print("Brand assets generated successfully in:", BRAND_DIR)


if __name__ == "__main__":
    generate_assets()

