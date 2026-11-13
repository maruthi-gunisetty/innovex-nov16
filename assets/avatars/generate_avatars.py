"""
SARVAVIDYA AVATARVERSE: Asset Generator for 10-Level 3D Cartoon Avatars
Generates 10 distinct, Snapchat Bitmoji-inspired 3D cartoon avatar SVGs.
Each avatar features custom hairstyles, facial features, accessories, lighting, and attire.
"""

import os

AVATAR_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(AVATAR_DIR, exist_ok=True)

AVATAR_DEFINITIONS = [
    {
        "id": "avatar_1_mystic_scholar",
        "level": 1,
        "name": "Mystic Scholar",
        "tier": "Epic",
        "price": 800,
        "gender": "Female",
        "accent": "#6366F1",
        "bg_glow": "#4338CA",
        "hair_color": "#2C1B4D",
        "skin_tone": "#F5D0B5",
        "clothing_color": "#3730A3",
        "clothing_trim": "#818CF8",
        "accessory_svg": """
            <!-- Tortoiseshell Spectacles -->
            <rect x="135" y="165" width="46" height="34" rx="10" fill="none" stroke="#6D28D9" stroke-width="4.5"/>
            <rect x="219" y="165" width="46" height="34" rx="10" fill="none" stroke="#6D28D9" stroke-width="4.5"/>
            <path d="M181 178 Q200 172 219 178" fill="none" stroke="#6D28D9" stroke-width="4.5" stroke-linecap="round"/>
            <line x1="135" y1="178" x2="115" y2="170" stroke="#6D28D9" stroke-width="3.5" stroke-linecap="round"/>
            <line x1="265" y1="178" x2="285" y2="170" stroke="#6D28D9" stroke-width="3.5" stroke-linecap="round"/>
            <!-- Open Mystic Book Crest -->
            <path d="M185 330 Q200 324 215 330 L220 348 Q200 342 180 348 Z" fill="#818CF8"/>
            <path d="M185 330 L200 344 L215 330" fill="none" stroke="#D6B56D" stroke-width="2"/>
        """,
        "hair_svg": """
            <!-- Sleek Top Bun & Soft Framing Strands -->
            <circle cx="200" cy="85" r="38" fill="url(#hairGrad1)"/>
            <path d="M125 150 Q130 95 200 95 Q270 95 275 150 Q285 220 270 230 Q255 170 245 150 Q200 135 155 150 Q145 170 130 230 Q115 220 125 150 Z" fill="url(#hairGrad1)"/>
            <!-- Hair highlight -->
            <path d="M150 115 Q200 102 245 118" fill="none" stroke="#A78BFA" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
        """
    },
    {
        "id": "avatar_2_celestial_dreamer",
        "level": 2,
        "name": "Celestial Dreamer",
        "tier": "Epic",
        "price": 850,
        "gender": "Male",
        "accent": "#8B5CF6",
        "bg_glow": "#6D28D9",
        "hair_color": "#1E293B",
        "skin_tone": "#FAD8C0",
        "clothing_color": "#1E1B4B",
        "clothing_trim": "#A78BFA",
        "accessory_svg": """
            <!-- Cosmic Lilac Headphones around neck -->
            <path d="M130 250 Q200 280 270 250" fill="none" stroke="#8B5CF6" stroke-width="12" stroke-linecap="round"/>
            <rect x="110" y="225" width="28" height="42" rx="12" fill="#A78BFA" stroke="#6D28D9" stroke-width="3"/>
            <rect x="262" y="225" width="28" height="42" rx="12" fill="#A78BFA" stroke="#6D28D9" stroke-width="3"/>
            <!-- Celestial Star Lapel Pin -->
            <path d="M200 322 L203 330 L211 331 L205 336 L207 344 L200 339 L193 344 L195 336 L189 331 L197 330 Z" fill="#FDE047"/>
        """,
        "hair_svg": """
            <!-- Tousled Wavy Dreamer Hair -->
            <path d="M128 155 Q120 90 200 82 Q280 90 272 155 Q260 110 200 110 Q140 110 128 155 Z" fill="url(#hairGrad2)"/>
            <path d="M140 105 Q175 75 220 90 Q250 80 265 105 Q240 92 205 94 Q170 94 140 105 Z" fill="#334155"/>
            <!-- Starlight streak -->
            <path d="M165 95 Q195 85 235 98" fill="none" stroke="#C4B5FD" stroke-width="3.5" stroke-linecap="round"/>
        """
    },
    {
        "id": "avatar_3_cyber_sage",
        "level": 3,
        "name": "Cyber Sage",
        "tier": "Epic",
        "price": 900,
        "gender": "Gender-Neutral",
        "accent": "#06B6D4",
        "bg_glow": "#0891B2",
        "hair_color": "#334155",
        "skin_tone": "#E8B298",
        "clothing_color": "#0F172A",
        "clothing_trim": "#06B6D4",
        "accessory_svg": """
            <!-- Augmented Reality Cyber Visor -->
            <rect x="126" y="166" width="148" height="30" rx="8" fill="url(#cyanGlow)" opacity="0.88"/>
            <rect x="126" y="166" width="148" height="30" rx="8" fill="none" stroke="#22D3EE" stroke-width="3"/>
            <line x1="140" y1="181" x2="260" y2="181" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 4" opacity="0.9"/>
            <circle cx="250" cy="181" r="3" fill="#67E8F9"/>
            <!-- Cyber Collar Nodes -->
            <circle cx="165" cy="310" r="4" fill="#22D3EE"/>
            <circle cx="235" cy="310" r="4" fill="#22D3EE"/>
            <line x1="165" y1="310" x2="235" y2="310" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 3"/>
        """,
        "hair_svg": """
            <!-- Modern Cyber Crop Hair with Teal Highlights -->
            <path d="M125 155 Q125 80 200 78 Q275 80 275 155 Q265 105 200 102 Q135 105 125 155 Z" fill="url(#hairGrad3)"/>
            <path d="M135 110 L160 88 L185 100 L215 82 L245 98 L265 112 Q200 90 135 110 Z" fill="#22D3EE" opacity="0.75"/>
        """
    },
    {
        "id": "avatar_4_tech_wizard",
        "level": 4,
        "name": "Tech Wizard",
        "tier": "Epic",
        "price": 950,
        "gender": "Female",
        "accent": "#3B82F6",
        "bg_glow": "#1D4ED8",
        "hair_color": "#9A3412",
        "skin_tone": "#FDE2D0",
        "clothing_color": "#1E3A8A",
        "clothing_trim": "#60A5FA",
        "accessory_svg": """
            <!-- Stylus behind ear -->
            <rect x="264" y="130" width="8" height="48" rx="3" transform="rotate(25 264 130)" fill="#60A5FA" stroke="#1D4ED8" stroke-width="1.5"/>
            <!-- Circuit Board Embroidery on Varsity Collar -->
            <path d="M175 305 L175 325 L160 335" fill="none" stroke="#93C5FD" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="160" cy="335" r="3" fill="#60A5FA"/>
            <path d="M225 305 L225 325 L240 335" fill="none" stroke="#93C5FD" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="240" cy="335" r="3" fill="#60A5FA"/>
            <!-- Hologram Sparkle -->
            <polygon points="200,325 203,333 211,335 204,339 205,347 200,342 195,347 196,339 189,335 197,333" fill="#FDE047"/>
        """,
        "hair_svg": """
            <!-- Dynamic Auburn Hair with High Ponytail -->
            <circle cx="255" cy="98" r="28" fill="url(#hairGrad4)"/>
            <path d="M125 155 Q125 85 200 85 Q275 85 275 155 Q265 110 200 115 Q135 110 125 155 Z" fill="url(#hairGrad4)"/>
            <path d="M130 140 Q138 215 152 235 Q145 170 148 140 Z" fill="url(#hairGrad4)"/>
            <path d="M270 140 Q262 215 248 235 Q255 170 252 140 Z" fill="url(#hairGrad4)"/>
        """
    },
    {
        "id": "avatar_5_quantum_learner",
        "level": 5,
        "name": "Quantum Learner",
        "tier": "Epic",
        "price": 1000,
        "gender": "Male",
        "accent": "#10B981",
        "bg_glow": "#059669",
        "hair_color": "#18181B",
        "skin_tone": "#D4A373",
        "clothing_color": "#064E3B",
        "clothing_trim": "#34D399",
        "accessory_svg": """
            <!-- 3D Quantum Atom Orbital Pin -->
            <ellipse cx="200" cy="328" rx="20" ry="8" fill="none" stroke="#34D399" stroke-width="2" transform="rotate(30 200 328)"/>
            <ellipse cx="200" cy="328" rx="20" ry="8" fill="none" stroke="#34D399" stroke-width="2" transform="rotate(-30 200 328)"/>
            <circle cx="200" cy="328" r="5" fill="#FDE047"/>
            <circle cx="214" cy="322" r="2.5" fill="#A7F3D0"/>
            <!-- Crisp Gold Trim Lapels -->
            <path d="M165 290 L185 350 L200 350" fill="none" stroke="#D6B56D" stroke-width="2"/>
            <path d="M235 290 L215 350 L200 350" fill="none" stroke="#D6B56D" stroke-width="2"/>
        """,
        "hair_svg": """
            <!-- Sharp Modern Fade & Quiff -->
            <path d="M130 155 Q130 85 200 78 Q270 85 270 155 Q262 105 200 102 Q138 105 130 155 Z" fill="url(#hairGrad5)"/>
            <path d="M150 90 Q200 68 250 88 Q210 74 150 90 Z" fill="#3F3F46"/>
        """
    },
    {
        "id": "avatar_6_shadow_knight",
        "level": 6,
        "name": "Shadow Knight",
        "tier": "Legendary",
        "price": 1500,
        "gender": "Female",
        "accent": "#7C3AED",
        "bg_glow": "#4C1D95",
        "hair_color": "#0F172A",
        "skin_tone": "#FCE7DB",
        "clothing_color": "#09090B",
        "clothing_trim": "#A855F7",
        "accessory_svg": """
            <!-- Violet Shadow Pendant & Glowing Trim -->
            <path d="M185 295 L200 325 L215 295 Z" fill="#7C3AED" stroke="#C084FC" stroke-width="2"/>
            <circle cx="200" cy="310" r="3.5" fill="#FFFFFF"/>
            <!-- Sleek Night Velvet Collar Glow -->
            <path d="M140 280 Q200 310 260 280" fill="none" stroke="#A855F7" stroke-width="3" opacity="0.8"/>
            <polygon points="200,335 204,343 213,344 206,350 208,359 200,354 192,359 194,350 187,344 196,343" fill="#E879F9"/>
        """,
        "hair_svg": """
            <!-- Jet Black Bob with Violet Highlights -->
            <path d="M120 160 Q120 78 200 76 Q280 78 280 160 Q290 240 268 250 Q260 170 248 150 Q200 130 152 150 Q140 170 132 250 Q110 240 120 160 Z" fill="url(#hairGrad6)"/>
            <path d="M260 180 Q275 230 265 245" fill="none" stroke="#C084FC" stroke-width="4" stroke-linecap="round"/>
            <path d="M140 180 Q125 230 135 245" fill="none" stroke="#C084FC" stroke-width="4" stroke-linecap="round"/>
        """
    },
    {
        "id": "avatar_7_phoenix_aura",
        "level": 7,
        "name": "Phoenix Aura",
        "tier": "Legendary",
        "price": 1600,
        "gender": "Gender-Neutral",
        "accent": "#F59E0B",
        "bg_glow": "#D97706",
        "hair_color": "#451A03",
        "skin_tone": "#E5B896",
        "clothing_color": "#78350F",
        "clothing_trim": "#F59E0B",
        "accessory_svg": """
            <!-- Warm Amber Phoenix Scarf -->
            <path d="M140 270 Q200 310 260 270 Q270 315 250 335 Q200 340 150 335 Q130 315 140 270 Z" fill="url(#amberGlow)"/>
            <path d="M185 305 L200 338 L215 305" fill="none" stroke="#FDE68A" stroke-width="2.5" stroke-linecap="round"/>
            <!-- Phoenix Crest Medallion -->
            <circle cx="200" cy="335" r="9" fill="#B45309" stroke="#FDE047" stroke-width="2"/>
            <path d="M196 338 Q200 328 204 338 Q200 334 196 338 Z" fill="#FDE047"/>
        """,
        "hair_svg": """
            <!-- Warm Auburn Tousled Hair with Sunlit Highlights -->
            <path d="M125 155 Q125 80 200 75 Q275 80 275 155 Q265 105 200 100 Q135 105 125 155 Z" fill="url(#hairGrad7)"/>
            <path d="M150 95 Q190 75 230 82 Q255 72 265 95 Q230 82 195 86 Q165 86 150 95 Z" fill="#F59E0B" opacity="0.6"/>
        """
    },
    {
        "id": "avatar_8_star_guardian",
        "level": 8,
        "name": "Star Guardian",
        "tier": "Legendary",
        "price": 1700,
        "gender": "Male",
        "accent": "#3B82F6",
        "bg_glow": "#1D4ED8",
        "hair_color": "#1E293B",
        "skin_tone": "#F1C5A8",
        "clothing_color": "#172554",
        "clothing_trim": "#D6B56D",
        "accessory_svg": """
            <!-- Gold Guardian Shoulder Epaulettes -->
            <rect x="100" y="275" width="35" height="12" rx="4" fill="#D6B56D" stroke="#B45309" stroke-width="1.5"/>
            <rect x="265" y="275" width="35" height="12" rx="4" fill="#D6B56D" stroke="#B45309" stroke-width="1.5"/>
            <!-- 8-Point Radiant Star Medal -->
            <g transform="translate(200,325)">
                <polygon points="0,-14 4,-4 14,0 4,4 0,14 -4,4 -14,0 -4,-4" fill="#FDE047" stroke="#D6B56D" stroke-width="1.5"/>
                <circle cx="0" cy="0" r="3.5" fill="#1D4ED8"/>
            </g>
            <!-- Royal Gold Neck Trim -->
            <path d="M165 268 Q200 290 235 268" fill="none" stroke="#D6B56D" stroke-width="4"/>
        """,
        "hair_svg": """
            <!-- Classic Academic Part & Volume -->
            <path d="M128 150 Q125 80 200 76 Q275 80 272 150 Q265 105 200 102 Q135 105 128 150 Z" fill="url(#hairGrad8)"/>
            <path d="M140 100 Q180 80 230 85 Q260 88 268 110 Q240 92 195 94 Q160 94 140 100 Z" fill="#334155"/>
        """
    },
    {
        "id": "avatar_9_royal_enigma",
        "level": 9,
        "name": "Royal Enigma",
        "tier": "Legendary",
        "price": 1800,
        "gender": "Female",
        "accent": "#9333EA",
        "bg_glow": "#6B21A8",
        "hair_color": "#171717",
        "skin_tone": "#FCE0D2",
        "clothing_color": "#3B0764",
        "clothing_trim": "#D6B56D",
        "accessory_svg": """
            <!-- Imperial Purple Collar with Gold Filigree -->
            <path d="M150 280 L200 345 L250 280" fill="none" stroke="#D6B56D" stroke-width="3" stroke-linecap="round"/>
            <polygon points="200,335 203,342 210,343 205,348 206,355 200,351 194,355 195,348 190,343 197,342" fill="#FDE047"/>
            <!-- Gold Earring Hoops -->
            <circle cx="120" cy="190" r="7" fill="none" stroke="#FDE047" stroke-width="2.5"/>
            <circle cx="280" cy="190" r="7" fill="none" stroke="#FDE047" stroke-width="2.5"/>
            <!-- Elegant Eyebrow Arch -->
            <path d="M140 152 Q158 142 176 150" fill="none" stroke="#262626" stroke-width="3" stroke-linecap="round"/>
            <path d="M224 150 Q242 142 260 152" fill="none" stroke="#262626" stroke-width="3" stroke-linecap="round"/>
        """,
        "hair_svg": """
            <!-- Sleek Center Part & Royal Braids -->
            <path d="M120 155 Q120 78 200 78 Q280 78 280 155 Q285 240 270 260 Q258 180 250 155 Q200 135 150 155 Q142 180 130 260 Q115 240 120 155 Z" fill="url(#hairGrad9)"/>
            <circle cx="132" cy="235" r="4" fill="#D6B56D"/>
            <circle cx="268" cy="235" r="4" fill="#D6B56D"/>
        """
    },
    {
        "id": "avatar_10_legendary_ace",
        "level": 10,
        "name": "Legendary Ace",
        "tier": "Legendary",
        "price": 2000,
        "gender": "Gender-Neutral",
        "accent": "#EAB308",
        "bg_glow": "#CA8A04",
        "hair_color": "#1C1917",
        "skin_tone": "#F5C89F",
        "clothing_color": "#1E3A8A",
        "clothing_trim": "#FDE047",
        "accessory_svg": """
            <!-- Imperial Gold Laurel Wreath Crown -->
            <g transform="translate(200, 78)">
                <!-- Left Laurel Leaves -->
                <path d="M-5 5 Q-35 -5 -55 20 Q-45 10 -25 15 Q-15 10 -5 5 Z" fill="#FDE047" stroke="#B45309" stroke-width="1.5"/>
                <path d="M-20 2 Q-45 -18 -60 5 Q-45 0 -30 8 Z" fill="#FACC15" stroke="#B45309" stroke-width="1.5"/>
                <path d="M-35 8 Q-58 -10 -65 18 Q-52 10 -40 15 Z" fill="#FDE047" stroke="#B45309" stroke-width="1.5"/>
                <!-- Right Laurel Leaves -->
                <path d="M5 5 Q35 -5 55 20 Q45 10 25 15 Q15 10 5 5 Z" fill="#FDE047" stroke="#B45309" stroke-width="1.5"/>
                <path d="M20 2 Q45 -18 60 5 Q45 0 30 8 Z" fill="#FACC15" stroke="#B45309" stroke-width="1.5"/>
                <path d="M35 8 Q58 -10 65 18 Q52 10 40 15 Z" fill="#FDE047" stroke="#B45309" stroke-width="1.5"/>
                <!-- Center Gem -->
                <polygon points="0,-8 6,0 0,8 -6,0" fill="#3B82F6" stroke="#FFFFFF" stroke-width="1.5"/>
            </g>
            <!-- Royal Ace Sash & Golden Laurels -->
            <path d="M120 280 L260 370" stroke="#FDE047" stroke-width="22" stroke-linecap="round" opacity="0.95"/>
            <path d="M120 280 L260 370" stroke="#B45309" stroke-width="2" stroke-linecap="round"/>
            <!-- Gold Crest Star -->
            <g transform="translate(190, 325)">
                <polygon points="0,-12 3.5,-3.5 12,0 3.5,3.5 0,12 -3.5,3.5 -12,0 -3.5,-3.5" fill="#FFFFFF"/>
                <circle cx="0" cy="0" r="3" fill="#EAB308"/>
            </g>
        """,
        "hair_svg": """
            <!-- Royal Voluminous Styled Hair -->
            <path d="M126 150 Q122 75 200 70 Q278 75 274 150 Q265 102 200 98 Q135 102 126 150 Z" fill="url(#hairGrad10)"/>
            <path d="M140 95 Q180 72 235 80 Q265 82 270 105 Q240 86 195 90 Q160 90 140 95 Z" fill="#44403C"/>
        """
    }
]


def generate_avatar_svg(avatar: dict) -> str:
    """Builds a crisp, spherical 3D Bitmoji-style avatar SVG."""
    av_id = avatar["id"]
    accent = avatar["accent"]
    bg_glow = avatar["bg_glow"]
    hair_c = avatar["hair_color"]
    skin_c = avatar["skin_tone"]
    cloth_c = avatar["clothing_color"]
    cloth_trim = avatar["clothing_trim"]
    hair_svg = avatar["hair_svg"]
    acc_svg = avatar.get("accessory_svg", "")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
    <defs>
        <!-- Background Radial 3D Sphere Glow -->
        <radialGradient id="bgSphere_{av_id}" cx="40%" cy="35%" r="65%">
            <stop offset="0%" stop-color="{accent}" stop-opacity="0.35"/>
            <stop offset="50%" stop-color="{bg_glow}" stop-opacity="0.15"/>
            <stop offset="100%" stop-color="#0B132B" stop-opacity="0"/>
        </radialGradient>

        <!-- 3D Skin Gradient (Shadow to Highlight) -->
        <radialGradient id="skinGrad_{av_id}" cx="40%" cy="38%" r="55%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22"/>
            <stop offset="40%" stop-color="{skin_c}"/>
            <stop offset="100%" stop-color="{skin_c}" stop-opacity="0.82"/>
        </radialGradient>

        <!-- Torso Clothing Gradient -->
        <linearGradient id="clothGrad_{av_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{cloth_trim}"/>
            <stop offset="35%" stop-color="{cloth_c}"/>
            <stop offset="100%" stop-color="#0B132B"/>
        </linearGradient>

        <!-- Hair Gradients -->
        <linearGradient id="hairGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#4C1D95"/><stop offset="100%" stop-color="#1E1B4B"/>
        </linearGradient>
        <linearGradient id="hairGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0F172A"/>
        </linearGradient>
        <linearGradient id="hairGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0891B2"/><stop offset="100%" stop-color="#0F172A"/>
        </linearGradient>
        <linearGradient id="hairGrad4" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#C2410C"/><stop offset="100%" stop-color="#7C2D12"/>
        </linearGradient>
        <linearGradient id="hairGrad5" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#27272A"/><stop offset="100%" stop-color="#09090B"/>
        </linearGradient>
        <linearGradient id="hairGrad6" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#581C87"/><stop offset="100%" stop-color="#09090B"/>
        </linearGradient>
        <linearGradient id="hairGrad7" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#D97706"/><stop offset="100%" stop-color="#451A03"/>
        </linearGradient>
        <linearGradient id="hairGrad8" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#0F172A"/>
        </linearGradient>
        <linearGradient id="hairGrad9" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#7E22CE"/><stop offset="100%" stop-color="#171717"/>
        </linearGradient>
        <linearGradient id="hairGrad10" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#EAB308"/><stop offset="100%" stop-color="#1C1917"/>
        </linearGradient>

        <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#3B82F6" stop-opacity="0.8"/>
        </linearGradient>
        <linearGradient id="amberGlow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#F59E0B"/><stop offset="100%" stop-color="#B45309"/>
        </linearGradient>
    </defs>

    <!-- Outer Soft Spherical Aura Glow -->
    <circle cx="200" cy="200" r="190" fill="url(#bgSphere_{av_id})"/>
    <circle cx="200" cy="200" r="185" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="8 6" opacity="0.4"/>

    <!-- Soft Drop Shadow below character -->
    <ellipse cx="200" cy="385" rx="110" ry="12" fill="#050B18" opacity="0.6"/>

    <!-- ==================== TORSO / CLOTHING ==================== -->
    <path d="M100 395 C100 310, 140 280, 200 280 C260 280, 300 310, 300 395 Z" fill="url(#clothGrad_{av_id})"/>
    <!-- Collar / Neck Trim -->
    <path d="M165 280 Q200 310 235 280" fill="none" stroke="{cloth_trim}" stroke-width="4.5" stroke-linecap="round"/>
    <!-- Center Placket -->
    <line x1="200" y1="298" x2="200" y2="395" stroke="{cloth_trim}" stroke-width="2.5" opacity="0.75"/>

    <!-- ==================== NECK ==================== -->
    <rect x="180" y="225" width="40" height="65" rx="10" fill="{skin_c}"/>
    <path d="M180 245 Q200 260 220 245 L220 280 L180 280 Z" fill="#000000" opacity="0.12"/>

    <!-- ==================== EARS ==================== -->
    <circle cx="125" cy="185" r="16" fill="{skin_c}"/>
    <circle cx="125" cy="185" r="9" fill="#000000" opacity="0.08"/>
    <circle cx="275" cy="185" r="16" fill="{skin_c}"/>
    <circle cx="275" cy="185" r="9" fill="#000000" opacity="0.08"/>

    <!-- ==================== 3D HEAD ==================== -->
    <ellipse cx="200" cy="180" rx="72" ry="82" fill="url(#skinGrad_{av_id})"/>

    <!-- Cheeks (Friendly Student Blush) -->
    <circle cx="150" cy="205" r="12" fill="#FF7B90" opacity="0.25"/>
    <circle cx="250" cy="205" r="12" fill="#FF7B90" opacity="0.25"/>

    <!-- ==================== FACIAL FEATURES ==================== -->
    <!-- Eyebrows -->
    <path d="M142 152 Q160 144 178 152" fill="none" stroke="{hair_c}" stroke-width="3.8" stroke-linecap="round"/>
    <path d="M222 152 Q240 144 258 152" fill="none" stroke="{hair_c}" stroke-width="3.8" stroke-linecap="round"/>

    <!-- Big Expressive Cartoon Eyes -->
    <ellipse cx="160" cy="178" rx="13" ry="16" fill="#FFFFFF"/>
    <ellipse cx="240" cy="178" rx="13" ry="16" fill="#FFFFFF"/>
    <!-- Irises -->
    <circle cx="162" cy="178" r="9.5" fill="#1E293B"/>
    <circle cx="242" cy="178" r="9.5" fill="#1E293B"/>
    <!-- Colored Ring -->
    <circle cx="162" cy="178" r="9.5" fill="none" stroke="{accent}" stroke-width="2.2"/>
    <circle cx="242" cy="178" r="9.5" fill="none" stroke="{accent}" stroke-width="2.2"/>
    <!-- Catchlights -->
    <circle cx="159" cy="174" r="3.5" fill="#FFFFFF"/>
    <circle cx="165" cy="181" r="1.8" fill="#FFFFFF"/>
    <circle cx="239" cy="174" r="3.5" fill="#FFFFFF"/>
    <circle cx="245" cy="181" r="1.8" fill="#FFFFFF"/>

    <!-- Cute Stylized Nose -->
    <path d="M196 195 Q200 200 204 195" fill="none" stroke="#C2886A" stroke-width="2.5" stroke-linecap="round"/>

    <!-- Friendly Student Smile -->
    <path d="M182 216 Q200 230 218 216" fill="none" stroke="#A84E32" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M186 217 Q200 225 214 217" fill="#FFFFFF" opacity="0.9"/>

    <!-- ==================== DISTINCT HAIR ==================== -->
    {hair_svg}

    <!-- ==================== DISTINCT ACCESSORY ==================== -->
    {acc_svg}

    <!-- Rarity Level Badge Bottom Indicator -->
    <rect x="150" y="360" width="100" height="24" rx="12" fill="#0F172A" stroke="{accent}" stroke-width="1.8"/>
    <text x="200" y="376" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="800" fill="{accent}" text-anchor="middle" letter-spacing="0.5">LEVEL {avatar['level']}</text>
</svg>"""


def main():
    for av in AVATAR_DEFINITIONS:
        fname = f"{av['id']}.svg"
        fpath = os.path.join(AVATAR_DIR, fname)
        svg_content = generate_avatar_svg(av)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated: {fname} (Level {av['level']}: {av['name']} - {av['tier']} {av['price']} coins)")


if __name__ == "__main__":
    main()
