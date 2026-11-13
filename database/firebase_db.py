"""
SARVAVIDYA: Firebase Firestore Cloud Integration
Provides connection management and real-time cloud database synchronization
for student records, wallets, BKT cognitive mastery, and learning telemetry.
"""

import os
import json
from typing import Optional, Dict, Any, List

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    _FIREBASE_AVAILABLE = True
except ImportError:
    _FIREBASE_AVAILABLE = False


_FIREBASE_APP = None
_FIRESTORE_DB = None


def get_credentials_path() -> Optional[str]:
    """Finds service account key file in project directory or from environment."""
    candidates = [
        os.getenv("FIREBASE_CREDENTIALS_PATH"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "firebase_credentials.json"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "serviceAccountKey.json"),
        os.path.join(os.getcwd(), "firebase_credentials.json"),
        os.path.join(os.getcwd(), "serviceAccountKey.json"),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def init_firebase() -> Optional[Any]:
    """Initializes Firebase Admin SDK using service account credentials."""
    global _FIREBASE_APP, _FIRESTORE_DB
    if not _FIREBASE_AVAILABLE:
        return None

    if _FIRESTORE_DB is not None:
        return _FIRESTORE_DB

    cred_path = get_credentials_path()
    if not cred_path:
        return None

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            _FIREBASE_APP = firebase_admin.initialize_app(cred)
        else:
            _FIREBASE_APP = firebase_admin.get_app()

        _FIRESTORE_DB = firestore.client()
        return _FIRESTORE_DB
    except Exception as e:
        print(f"[Firebase] Initialization warning: {e}")
        return None


def is_firebase_connected() -> bool:
    """Returns True if Firebase is initialized and connected to Cloud Firestore."""
    db = init_firebase()
    return db is not None


def sync_user_to_firestore(user: Dict[str, Any]) -> bool:
    """Syncs a single user profile to Firestore 'users' collection."""
    db = init_firebase()
    if not db:
        return False
    try:
        user_id = str(user["id"])
        doc_data = {
            "id": user["id"],
            "username": user.get("username"),
            "email": user.get("email"),
            "full_name": user.get("full_name"),
            "role": user.get("role", "student"),
            "grade_level": user.get("grade_level", "Grade 10"),
            "school_name": user.get("school_name", "SARVAVIDYA Academy"),
            "last_synced": firestore.SERVER_TIMESTAMP
        }
        db.collection("users").document(user_id).set(doc_data, merge=True)
        return True
    except Exception as e:
        print(f"[Firebase Sync] Error syncing user {user.get('id')}: {e}")
        return False


def sync_wallet_to_firestore(user_id: int, wallet: Dict[str, Any]) -> bool:
    """Syncs student wallet and rewards status to Firestore 'wallets' collection."""
    db = init_firebase()
    if not db:
        return False
    try:
        doc_data = {
            "user_id": user_id,
            "available_coins": wallet.get("available_coins", 0),
            "lifetime_earned_coins": wallet.get("lifetime_earned_coins", 0),
            "lifetime_spent_coins": wallet.get("lifetime_spent_coins", 0),
            "current_level": wallet.get("current_level", "Bronze Learner"),
            "current_streak": wallet.get("current_streak", 0),
            "longest_streak": wallet.get("longest_streak", 0),
            "last_synced": firestore.SERVER_TIMESTAMP
        }
        db.collection("wallets").document(str(user_id)).set(doc_data, merge=True)
        return True
    except Exception as e:
        print(f"[Firebase Sync] Error syncing wallet {user_id}: {e}")
        return False


def sync_sqlite_to_firestore() -> Dict[str, int]:
    """Bulk synchronizes SQLite database records to Firebase Cloud Firestore."""
    db = init_firebase()
    if not db:
        return {"status": "unconnected", "synced_users": 0, "synced_wallets": 0}

    from database.db import get_db_connection

    synced_users = 0
    synced_wallets = 0

    with get_db_connection() as conn:
        cur = conn.cursor()
        
        # 1. Sync Users
        cur.execute("SELECT id, username, email, full_name, role, grade_level, school_name FROM users")
        users = [dict(r) for r in cur.fetchall()]
        batch = db.batch()
        for idx, u in enumerate(users):
            doc_ref = db.collection("users").document(str(u["id"]))
            batch.set(doc_ref, {**u, "last_synced": firestore.SERVER_TIMESTAMP}, merge=True)
            synced_users += 1
            if (idx + 1) % 450 == 0:
                batch.commit()
                batch = db.batch()
        batch.commit()

        # 2. Sync Wallets
        cur.execute("SELECT * FROM student_wallets")
        wallets = [dict(r) for r in cur.fetchall()]
        batch = db.batch()
        for idx, w in enumerate(wallets):
            doc_ref = db.collection("wallets").document(str(w["user_id"]))
            batch.set(doc_ref, {**w, "last_synced": firestore.SERVER_TIMESTAMP}, merge=True)
            synced_wallets += 1
            if (idx + 1) % 450 == 0:
                batch.commit()
                batch = db.batch()
        batch.commit()

    return {
        "status": "success",
        "synced_users": synced_users,
        "synced_wallets": synced_wallets
    }

