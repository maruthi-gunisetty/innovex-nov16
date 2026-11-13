"""
SARVAVIDYA AVATARVERSE: 10-Level 3D Avatar Catalog & Database Synchronization
Defines the official 10-level student & teacher avatar collection:
- Level 1-5: EPIC (Mystic Scholar, Celestial Dreamer, Cyber Sage, Tech Wizard, Quantum Learner)
- Level 6-10: LEGENDARY (Shadow Knight, Phoenix Aura, Star Guardian, Royal Enigma, Legendary Ace)
- Integrates with SQLite reward_store_items and student_inventory
"""

import os
from typing import List, Dict, Any, Optional
from database.db import get_db_connection

AVATAR_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "avatar_1_mystic_scholar",
        "level": 1,
        "name": "Mystic Scholar",
        "tier": "Epic",
        "coin_price": 800,
        "gender": "Female",
        "title": "Thoughtful Academic Explorer",
        "description": "A dedicated scholar in deep indigo study hoodie, stylish spectacles, and an illuminated study book.",
        "icon": "📚",
        "accent_color": "#6366F1",
        "border_color": "#818CF8",
        "badge_bg": "#EEF2FF",
        "asset_rel": "assets/avatars/avatar_1_mystic_scholar.svg"
    },
    {
        "id": "avatar_2_celestial_dreamer",
        "level": 2,
        "name": "Celestial Dreamer",
        "tier": "Epic",
        "coin_price": 850,
        "gender": "Male",
        "title": "Cosmic Visionary & Stargazer",
        "description": "Tousled navy hair, starlight reflections, lilac college headphones, and a radiant star constellation pin.",
        "icon": "✨",
        "accent_color": "#8B5CF6",
        "border_color": "#A78BFA",
        "badge_bg": "#F5F3FF",
        "asset_rel": "assets/avatars/avatar_2_celestial_dreamer.svg"
    },
    {
        "id": "avatar_3_cyber_sage",
        "level": 3,
        "name": "Cyber Sage",
        "tier": "Epic",
        "coin_price": 900,
        "gender": "Gender-Neutral",
        "title": "Next-Gen Algorithmic Architect",
        "description": "Sleek crop hair with cyan highlights, augmented reality visor HUD, and a modern graphite cyber turtleneck.",
        "icon": "⚡",
        "accent_color": "#06B6D4",
        "border_color": "#22D3EE",
        "badge_bg": "#ECFEFF",
        "asset_rel": "assets/avatars/avatar_3_cyber_sage.svg"
    },
    {
        "id": "avatar_4_tech_wizard",
        "level": 4,
        "name": "Tech Wizard",
        "tier": "Epic",
        "coin_price": 950,
        "gender": "Female",
        "title": "Hands-On STEM Builder",
        "description": "Auburn ponytail with digital stylus tucked behind the ear, royal blue varsity jacket, and gold circuit embroidery.",
        "icon": "🔮",
        "accent_color": "#3B82F6",
        "border_color": "#60A5FA",
        "badge_bg": "#EFF6FF",
        "asset_rel": "assets/avatars/avatar_4_tech_wizard.svg"
    },
    {
        "id": "avatar_5_quantum_learner",
        "level": 5,
        "name": "Quantum Learner",
        "tier": "Epic",
        "coin_price": 1000,
        "gender": "Male",
        "title": "Theoretical Science Pioneer",
        "description": "Sharp fade haircut, emerald lapel blazer, and a spinning 3D atomic orbital pin symbolizing mastery.",
        "icon": "🔬",
        "accent_color": "#10B981",
        "border_color": "#34D399",
        "badge_bg": "#ECFDF5",
        "asset_rel": "assets/avatars/avatar_5_quantum_learner.svg"
    },
    {
        "id": "avatar_6_shadow_knight",
        "level": 6,
        "name": "Shadow Knight",
        "tier": "Legendary",
        "coin_price": 1500,
        "gender": "Female",
        "title": "Stealth Night-Owl Strategist",
        "description": "Jet-black bob with violet tips, obsidian velvet hoodie with an amethyst pendant, and laser-sharp focus.",
        "icon": "🗡️",
        "accent_color": "#7C3AED",
        "border_color": "#A855F7",
        "badge_bg": "#FAF5FF",
        "asset_rel": "assets/avatars/avatar_6_shadow_knight.svg"
    },
    {
        "id": "avatar_7_phoenix_aura",
        "level": 7,
        "name": "Phoenix Aura",
        "tier": "Legendary",
        "coin_price": 1600,
        "gender": "Gender-Neutral",
        "title": "Unyielding Master of Resilience",
        "description": "A student who learns through mistakes, wearing a radiant amber-gold phoenix scarf and inspiring confidence.",
        "icon": "🔥",
        "accent_color": "#F59E0B",
        "border_color": "#FBBF24",
        "badge_bg": "#FFFBEB",
        "asset_rel": "assets/avatars/avatar_7_phoenix_aura.svg"
    },
    {
        "id": "avatar_8_star_guardian",
        "level": 8,
        "name": "Star Guardian",
        "tier": "Legendary",
        "coin_price": 1700,
        "gender": "Male",
        "title": "Academic Honor Leader",
        "description": "Midnight blue college blazer with gold epaulettes and an 8-point radiant star medal representing leadership.",
        "icon": "⭐",
        "accent_color": "#3B82F6",
        "border_color": "#D6B56D",
        "badge_bg": "#EFF6FF",
        "asset_rel": "assets/avatars/avatar_8_star_guardian.svg"
    },
    {
        "id": "avatar_9_royal_enigma",
        "level": 9,
        "name": "Royal Enigma",
        "tier": "Legendary",
        "coin_price": 1800,
        "gender": "Female",
        "title": "Prodigy of Infinite Knowledge",
        "description": "Imperial purple cloak with gold filigree, royal braids with gold bead accents, and a gold quill emblem.",
        "icon": "👑",
        "accent_color": "#9333EA",
        "border_color": "#D6B56D",
        "badge_bg": "#FDF4FF",
        "asset_rel": "assets/avatars/avatar_9_royal_enigma.svg"
    },
    {
        "id": "avatar_10_legendary_ace",
        "level": 10,
        "name": "Legendary Ace",
        "tier": "Legendary",
        "coin_price": 2000,
        "gender": "Gender-Neutral",
        "title": "Supreme All-Subject Polymath",
        "description": "Crowned with the Imperial Gold Laurel Wreath, draped in a royal blue and gold sash, commanding top mastery.",
        "icon": "🏆",
        "accent_color": "#EAB308",
        "border_color": "#FACC15",
        "badge_bg": "#FEFCE8",
        "asset_rel": "assets/avatars/avatar_10_legendary_ace.svg"
    }
]

AVATAR_BY_ID = {a["id"]: a for a in AVATAR_CATALOG}


def seed_avatarverse_items() -> None:
    """Synchronizes the 10 official avatars into reward_store_items in SQLite."""
    with get_db_connection() as conn:
        with conn:
            cur = conn.cursor()
            for av in AVATAR_CATALOG:
                cur.execute(
                    """INSERT INTO reward_store_items (id, name, category, description, coin_price, icon, is_consumable, is_active)
                       VALUES (?, ?, 'avatar', ?, ?, ?, 0, 1)
                       ON CONFLICT(id) DO UPDATE SET 
                           name = excluded.name,
                           description = excluded.description,
                           coin_price = excluded.coin_price,
                           icon = excluded.icon,
                           is_active = 1""",
                    (av["id"], av["name"], av["description"], av["coin_price"], av["icon"])
                )


def get_user_avatar_state(user_id: int) -> Dict[str, Any]:
    """
    Fetches ownership, equipped status, and metadata for all 10 avatars for the given user.
    Thread-safe and fast.
    """
    seed_avatarverse_items()
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT item_id, is_equipped, quantity, purchased_at 
               FROM student_inventory 
               WHERE user_id = ? AND item_id LIKE 'avatar_%'""",
            (user_id,)
        )
        owned_rows = {r["item_id"]: dict(r) for r in cur.fetchall()}

    result = []
    equipped_avatar = None
    for av in AVATAR_CATALOG:
        av_copy = dict(av)
        inv = owned_rows.get(av["id"])
        if inv:
            av_copy["is_owned"] = True
            av_copy["is_equipped"] = bool(inv.get("is_equipped", 0))
            av_copy["purchased_at"] = inv.get("purchased_at")
            if av_copy["is_equipped"]:
                equipped_avatar = av_copy
        else:
            av_copy["is_owned"] = False
            av_copy["is_equipped"] = False
            av_copy["purchased_at"] = None

        result.append(av_copy)

    return {
        "avatars": result,
        "equipped": equipped_avatar,
        "total_owned": len(owned_rows)
    }
