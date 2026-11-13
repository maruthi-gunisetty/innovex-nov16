"""
Generates retro pop-art style SVG illustrations for the new Quiz / Learning Dashboard UI.
Matches the design reference:
- Hero banner study group with vintage stationery & confetti
- Subject thumbnails with duotone collage elements & retro accents
- High performance, pure scalable SVG, zero external network dependency.
"""

import os

UI_DIR = os.path.dirname(os.path.abspath(__file__))

def create_hero_collage():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 320" width="100%" height="100%">
  <defs>
    <!-- Background subtle shapes -->
    <filter id="retro-shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="3" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="warm-glow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE8B3" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#FFD6A5" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Ambient light -->
  <circle cx="340" cy="140" r="140" fill="url(#warm-glow)" />

  <!-- Floating Confetti & Retro Stationery -->
  <!-- Confetti strips -->
  <rect x="290" y="45" width="6" height="24" rx="3" transform="rotate(25 290 45)" fill="#FFB800"/>
  <rect x="340" y="30" width="7" height="28" rx="3" transform="rotate(-18 340 30)" fill="#111111"/>
  <rect x="380" y="60" width="8" height="32" rx="4" transform="rotate(32 380 60)" fill="#FF5238"/>
  <rect x="420" y="38" width="6" height="26" rx="3" transform="rotate(-30 420 38)" fill="#FFB800"/>
  <rect x="445" y="70" width="7" height="30" rx="3" transform="rotate(15 445 70)" fill="#111111"/>
  <rect x="310" y="95" width="6" height="22" rx="3" transform="rotate(-40 310 95)" fill="#FF5238"/>
  <rect x="460" y="110" width="7" height="26" rx="3" transform="rotate(45 460 110)" fill="#FFB800"/>

  <!-- Starburst explosion marks -->
  <path d="M 295 75 L 305 75 M 300 70 L 300 80" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 435 105 L 445 105 M 440 100 L 440 110" stroke="#FF5238" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 335 25 L 343 20 M 345 28 L 350 22" stroke="#FFB800" stroke-width="2" stroke-linecap="round"/>

  <!-- Pop art pencil/ruler strips -->
  <g transform="translate(370, 75) rotate(-12)">
    <rect x="0" y="0" width="10" height="55" rx="3" fill="#FFB800" stroke="#111" stroke-width="1.5"/>
    <polygon points="0,55 10,55 5,66" fill="#111"/>
  </g>
  <g transform="translate(415, 80) rotate(22)">
    <rect x="0" y="0" width="9" height="50" rx="3" fill="#FF5238" stroke="#111" stroke-width="1.5"/>
    <polygon points="0,50 9,50 4.5,60" fill="#FFB800"/>
  </g>

  <!-- Retro Desk Microphone / Speaker Box -->
  <g transform="translate(410, 210)" filter="url(#retro-shadow)">
    <rect x="0" y="0" width="62" height="65" rx="8" fill="#18181B"/>
    <circle cx="31" cy="32" r="22" fill="#27272A" stroke="#52525B" stroke-width="2"/>
    <line x1="16" y1="17" x2="46" y2="47" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
    <line x1="46" y1="17" x2="16" y2="47" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  </g>

  <!-- Main Figures: Monochrome & Stylized High-Contrast Group -->
  <!-- Figure 1 (Left - Inquisitive student in blazer) -->
  <g transform="translate(250, 140)" filter="url(#retro-shadow)">
    <!-- Body / Suit -->
    <path d="M 20 70 C 25 45, 55 45, 60 70 L 68 150 L 12 150 Z" fill="#27272A"/>
    <!-- Collar & Shirt -->
    <polygon points="35,68 40,95 45,68" fill="#FFFFFF"/>
    <polygon points="30,68 38,78 40,68" fill="#E4E4E7"/>
    <polygon points="50,68 42,78 40,68" fill="#E4E4E7"/>
    <!-- Head -->
    <ellipse cx="40" cy="40" rx="16" ry="20" fill="#E4D5C7"/>
    <!-- Curly Hair -->
    <circle cx="30" cy="30" r="14" fill="#18181B"/>
    <circle cx="48" cy="28" r="13" fill="#18181B"/>
    <circle cx="40" cy="22" r="14" fill="#18181B"/>
    <!-- Glasses & Smile -->
    <circle cx="36" cy="40" r="4" fill="none" stroke="#18181B" stroke-width="1.8"/>
    <circle cx="46" cy="40" r="4" fill="none" stroke="#18181B" stroke-width="1.8"/>
    <line x1="40" y1="40" x2="42" y2="40" stroke="#18181B" stroke-width="1.8"/>
    <path d="M 38 48 Q 41 52 44 48" stroke="#18181B" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  </g>

  <!-- Figure 2 (Center-Right - Excited Teacher/Mentor) -->
  <g transform="translate(325, 95)" filter="url(#retro-shadow)">
    <!-- Body -->
    <path d="M 15 80 C 25 40, 75 40, 85 80 L 95 190 L 5 190 Z" fill="#18181B"/>
    <path d="M 40 75 L 50 110 L 60 75 Z" fill="#FFFFFF"/>
    <!-- Head -->
    <ellipse cx="50" cy="42" rx="19" ry="23" fill="#EDDEC8"/>
    <!-- Hair bun / classic retro updo -->
    <ellipse cx="50" cy="22" rx="17" ry="12" fill="#18181B"/>
    <ellipse cx="32" cy="35" rx="9" ry="14" fill="#18181B"/>
    <ellipse cx="68" cy="35" rx="9" ry="14" fill="#18181B"/>
    <!-- Joyful expression -->
    <circle cx="44" cy="42" r="2.5" fill="#18181B"/>
    <circle cx="58" cy="42" r="2.5" fill="#18181B"/>
    <path d="M 45 52 Q 51 62 57 52 Z" fill="#18181B"/>
    <!-- Pearl necklace -->
    <circle cx="44" cy="74" r="2.5" fill="#FFFFFF"/>
    <circle cx="49" cy="76" r="2.5" fill="#FFFFFF"/>
    <circle cx="54" cy="76" r="2.5" fill="#FFFFFF"/>
    <circle cx="58" cy="74" r="2.5" fill="#FFFFFF"/>
  </g>

  <!-- Figure 3 (Center-Left - Attentive Scholar) -->
  <g transform="translate(290, 160)" filter="url(#retro-shadow)">
    <!-- Body in grey patterned coat -->
    <path d="M 10 50 C 15 25, 55 25, 60 50 L 65 130 L 5 130 Z" fill="#52525B"/>
    <!-- White collar -->
    <polygon points="30,48 35,70 40,48" fill="#FFFFFF"/>
    <!-- Head -->
    <ellipse cx="35" cy="24" rx="14" ry="17" fill="#E4D5C7"/>
    <!-- Sleek black bob -->
    <path d="M 20 22 C 20 8, 50 8, 50 22 C 50 26, 48 32, 48 36 L 44 26 C 36 26, 26 26, 24 36 Z" fill="#18181B"/>
    <!-- Focused side profile -->
    <circle cx="38" cy="24" r="2" fill="#18181B"/>
    <path d="M 37 32 Q 40 34 42 32" stroke="#18181B" stroke-width="1.5" fill="none"/>
  </g>

  <!-- Desk & Learning Materials -->
  <rect x="230" y="275" width="260" height="15" rx="4" fill="#111111"/>
  <rect x="250" y="265" width="40" height="10" rx="2" fill="#FFFFFF" stroke="#111" stroke-width="1.5"/>
  <rect x="254" y="260" width="35" height="6" rx="2" fill="#FF5238"/>
  <rect x="360" y="268" width="35" height="7" rx="2" fill="#FFB800" stroke="#111" stroke-width="1.5"/>
</svg>"""


def create_subject_thumb(subject_type, color_bg):
    # Generates a retro pop-art card thumbnail for each subject
    icons = {
        "tech": """
          <!-- Retro Computer & Keyboard -->
          <rect x="40" y="28" width="60" height="46" rx="6" fill="#FFFFFF" stroke="#111" stroke-width="2.5"/>
          <rect x="46" y="34" width="48" height="34" rx="4" fill="#18181B"/>
          <!-- Terminal green line -->
          <line x1="52" y1="44" x2="72" y2="44" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="52" y1="52" x2="84" y2="52" stroke="#22C55E" stroke-width="2" stroke-linecap="round"/>
          <polygon points="76,50 80,52 76,54" fill="#22C55E"/>
          <!-- Computer base -->
          <rect x="62" y="74" width="16" height="12" fill="#E4E4E7" stroke="#111" stroke-width="2"/>
          <rect x="35" y="86" width="70" height="10" rx="3" fill="#FFFFFF" stroke="#111" stroke-width="2"/>
          <!-- Pop student behind desk -->
          <circle cx="106" cy="46" r="14" fill="#EDDEC8" stroke="#111" stroke-width="2"/>
          <path d="M 94 40 C 94 28, 118 28, 118 40 Z" fill="#111"/>
          <!-- Glasses -->
          <circle cx="103" cy="46" r="3.5" fill="none" stroke="#111" stroke-width="1.5"/>
          <circle cx="111" cy="46" r="3.5" fill="none" stroke="#111" stroke-width="1.5"/>
          <line x1="106" y1="46" x2="108" y2="46" stroke="#111" stroke-width="1.5"/>
          <!-- Student hoodie -->
          <path d="M 92 62 C 96 55, 118 55, 122 62 L 126 95 L 88 95 Z" fill="#111"/>
        """,
        "science": """
          <!-- Science Flask & Molecule -->
          <path d="M 58 35 L 68 35 L 68 48 L 84 76 C 88 82, 82 90, 74 90 L 52 90 C 44 90, 38 82, 42 76 L 58 48 Z" fill="#FFFFFF" stroke="#111" stroke-width="2.5"/>
          <path d="M 46 76 L 80 76 L 74 86 L 52 86 Z" fill="#10B981"/>
          <circle cx="58" cy="80" r="2.5" fill="#FFFFFF"/>
          <circle cx="68" cy="74" r="2" fill="#FFFFFF"/>
          <!-- Orbit -->
          <ellipse cx="105" cy="50" rx="20" ry="8" transform="rotate(-30 105 50)" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="4,3"/>
          <circle cx="105" cy="50" r="6" fill="#111"/>
          <circle cx="118" cy="42" r="3.5" fill="#FFB800" stroke="#111" stroke-width="1.5"/>
          <!-- Retro scholar silhouette -->
          <circle cx="30" cy="50" r="10" fill="#EDDEC8" stroke="#111" stroke-width="1.5"/>
          <path d="M 20 62 C 22 56, 38 56, 40 62 L 42 90 L 18 90 Z" fill="#111"/>
        """,
        "math": """
          <!-- Geometry & Compass / Golden Spiral -->
          <circle cx="65" cy="58" r="28" fill="#FFFFFF" stroke="#111" stroke-width="2.5"/>
          <polygon points="65,34 88,74 42,74" fill="none" stroke="#FF5238" stroke-width="2.5"/>
          <!-- Integral symbol & Sigma -->
          <text x="100" y="55" font-family="'Anton', Impact, sans-serif" font-size="28" font-weight="900" fill="#111">∫</text>
          <text x="96" y="85" font-family="'Anton', Impact, sans-serif" font-size="24" font-weight="900" fill="#FFB800">∑</text>
          <!-- Confetti lines -->
          <line x1="28" y1="36" x2="38" y2="30" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="32" y1="80" x2="40" y2="84" stroke="#FF5238" stroke-width="2.5" stroke-linecap="round"/>
        """,
        "physics": """
          <!-- Atomic Core & Force Vectors -->
          <circle cx="70" cy="60" r="14" fill="#111"/>
          <ellipse cx="70" cy="60" rx="34" ry="12" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
          <ellipse cx="70" cy="60" rx="34" ry="12" transform="rotate(60 70 60)" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
          <ellipse cx="70" cy="60" rx="34" ry="12" transform="rotate(-60 70 60)" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
          <circle cx="70" cy="26" r="4" fill="#FFB800" stroke="#111" stroke-width="1.5"/>
          <circle cx="98" cy="74" r="4" fill="#FF5238" stroke="#111" stroke-width="1.5"/>
        """,
        "electronics": """
          <!-- Microchip & Circuit Lines -->
          <rect x="45" y="38" width="46" height="46" rx="6" fill="#18181B" stroke="#FFFFFF" stroke-width="2.5"/>
          <circle cx="68" cy="61" r="10" fill="#3B82F6"/>
          <!-- Chip Pins -->
          <line x1="38" y1="46" x2="45" y2="46" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <line x1="38" y1="56" x2="45" y2="56" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <line x1="38" y1="66" x2="45" y2="66" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <line x1="91" y1="46" x2="98" y2="46" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <line x1="91" y1="56" x2="98" y2="56" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <line x1="91" y1="66" x2="98" y2="66" stroke="#FFB800" stroke-width="3" stroke-linecap="round"/>
          <circle cx="112" cy="40" r="5" fill="#FF5238" stroke="#111" stroke-width="1.5"/>
          <line x1="98" y1="56" x2="110" y2="56" stroke="#FFFFFF" stroke-width="2"/>
        """,
        "dsa": """
          <!-- Binary Tree & Graph Nodes -->
          <circle cx="68" cy="36" r="11" fill="#111" stroke="#FFFFFF" stroke-width="2"/>
          <line x1="62" y1="44" x2="48" y2="64" stroke="#111" stroke-width="2.5"/>
          <line x1="74" y1="44" x2="88" y2="64" stroke="#111" stroke-width="2.5"/>
          <circle cx="44" cy="72" r="10" fill="#FF5238" stroke="#FFFFFF" stroke-width="2"/>
          <circle cx="92" cy="72" r="10" fill="#FFB800" stroke="#FFFFFF" stroke-width="2"/>
          <text x="64" y="40" font-family="sans-serif" font-size="10" font-weight="900" fill="#FFF">N</text>
          <text x="40" y="76" font-family="sans-serif" font-size="10" font-weight="900" fill="#FFF">L</text>
          <text x="88" y="76" font-family="sans-serif" font-size="10" font-weight="900" fill="#111">R</text>
        """
    }

    icon_content = icons.get(subject_type, icons["tech"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 110" width="100%" height="100%">
  <!-- Rounded Card Base with Coral/Warm Background -->
  <rect x="0" y="0" width="160" height="110" rx="14" fill="{color_bg}"/>
  
  <!-- Subtle Retro Collage Confetti Elements -->
  <rect x="18" y="14" width="4" height="14" rx="2" transform="rotate(30 18 14)" fill="#FFB800"/>
  <rect x="135" y="16" width="5" height="16" rx="2" transform="rotate(-25 135 16)" fill="#FFFFFF" opacity="0.8"/>
  <rect x="140" y="75" width="4" height="14" rx="2" transform="rotate(18 140 75)" fill="#111111" opacity="0.7"/>
  <circle cx="24" cy="85" r="3" fill="#FFB800"/>
  <circle cx="125" cy="88" r="2.5" fill="#FFFFFF"/>

  {icon_content}
</svg>"""

def main():
    # 1. Hero banner illustration
    hero_path = os.path.join(UI_DIR, "hero_study_collage.svg")
    with open(hero_path, "w", encoding="utf-8") as f:
        f.write(create_hero_collage())
    print("Created:", hero_path)

    # 2. Subject thumbnails
    configs = [
        ("thumb_python.svg", "tech", "#FF5238"),
        ("thumb_c_prog.svg", "tech", "#FF6B4A"),
        ("thumb_calculus.svg", "math", "#FF5238"),
        ("thumb_dsa.svg", "dsa", "#FF5238"),
        ("thumb_electronics.svg", "electronics", "#FF5238"),
        ("thumb_physics.svg", "physics", "#FF5238"),
        ("thumb_social.svg", "science", "#0D8A5E"),
        ("popular_tech.svg", "tech", "#FF5238"),
        ("popular_science.svg", "science", "#0D8A5E"),
    ]

    for fname, stype, bg in configs:
        fpath = os.path.join(UI_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(create_subject_thumb(stype, bg))
        print("Created:", fpath)

if __name__ == "__main__":
    main()
