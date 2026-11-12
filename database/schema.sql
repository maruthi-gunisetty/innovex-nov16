-- LearnSphere AI Database Schema
-- Scalable multi-subject schema for student performance, BKT mastery, and misconception tracking
-- Supports Programming, Mathematics, Engineering, Science, and Computer Science

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin')),
    is_demo INTEGER DEFAULT 0,
    target_difficulty TEXT DEFAULT 'adaptive' CHECK(target_difficulty IN ('beginner', 'intermediate', 'advanced', 'adaptive')),
    daily_goal INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Programming', 'Mathematics', 'Engineering', 'Science', 'Computer Science')),
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    order_index INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty_level TEXT DEFAULT 'All Levels',
    is_active INTEGER DEFAULT 1,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    course_id INTEGER,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    p_init REAL DEFAULT 0.20,
    p_transit REAL DEFAULT 0.15,
    p_guess REAL DEFAULT 0.20,
    p_slip REAL DEFAULT 0.10,
    prerequisites TEXT DEFAULT '[]', -- JSON array of concept codes
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    difficulty TEXT NOT NULL CHECK(difficulty IN ('beginner', 'intermediate', 'advanced')),
    title TEXT NOT NULL,
    prompt TEXT NOT NULL,
    code_snippet TEXT,
    options_json TEXT NOT NULL, -- JSON array of {index, text, is_correct, misconception_code, misconception_name, explanation}
    explanation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS learning_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    reading_time_min INTEGER DEFAULT 8,
    introduction TEXT NOT NULL,
    learning_objectives_json TEXT NOT NULL, -- JSON array of strings
    detailed_explanation TEXT NOT NULL,
    code_examples_json TEXT NOT NULL, -- JSON array of {title, code, output, notes}
    common_mistakes_json TEXT NOT NULL, -- JSON array of {title, wrong_code, correct_code, misconception_code, explanation}
    practice_exercises_json TEXT NOT NULL, -- JSON array of {prompt, hint, solution}
    order_index INTEGER NOT NULL,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assessment_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    selected_option_index INTEGER NOT NULL,
    is_correct INTEGER NOT NULL CHECK(is_correct IN (0, 1)),
    difficulty TEXT NOT NULL,
    response_time_sec REAL NOT NULL,
    misconception_code TEXT,
    prior_mastery REAL NOT NULL,
    posterior_mastery REAL NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_mastery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    mastery_prob REAL NOT NULL DEFAULT 0.20,
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, concept_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS learning_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    recommendation_type TEXT NOT NULL, -- 'prerequisite_gap', 'misconception_revision', 'practice_drill', 'next_advancement'
    title TEXT NOT NULL,
    reason TEXT NOT NULL,
    priority_score REAL DEFAULT 1.0,
    is_completed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_id INTEGER NOT NULL,
    is_completed INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES learning_content(id) ON DELETE CASCADE
);

-- ==========================================
-- SARVAVIDYA REWARDS ECOSYSTEM SCHEMA
-- ==========================================

CREATE TABLE IF NOT EXISTS student_wallets (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    available_coins INTEGER NOT NULL DEFAULT 0 CHECK(available_coins >= 0),
    lifetime_earned_coins INTEGER NOT NULL DEFAULT 0,
    lifetime_spent_coins INTEGER NOT NULL DEFAULT 0,
    current_level TEXT NOT NULL DEFAULT 'Bronze Learner',
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_active_date TEXT,
    streak_freeze_tokens INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coin_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('EARN', 'SPEND', 'BONUS', 'FREEZE_USED')),
    amount INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,
    source_activity TEXT NOT NULL,
    entity_id TEXT,
    description TEXT NOT NULL,
    idempotency_key TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    reward_coins INTEGER NOT NULL,
    target_count INTEGER DEFAULT 1,
    mission_type TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS student_mission_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mission_id INTEGER NOT NULL REFERENCES daily_missions(id) ON DELETE CASCADE,
    date TEXT NOT NULL,
    current_count INTEGER DEFAULT 0,
    is_completed INTEGER DEFAULT 0,
    is_claimed INTEGER DEFAULT 0,
    claimed_at TIMESTAMP,
    UNIQUE(user_id, mission_id, date)
);

CREATE TABLE IF NOT EXISTS reward_store_items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('avatar', 'frame', 'theme', 'badge', 'powerup', 'exclusive_challenge')),
    description TEXT NOT NULL,
    coin_price INTEGER NOT NULL,
    icon TEXT NOT NULL,
    is_consumable INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS student_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_id TEXT NOT NULL REFERENCES reward_store_items(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    is_equipped INTEGER DEFAULT 0,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, item_id)
);

CREATE TABLE IF NOT EXISTS reward_claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    claim_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    date_str TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, claim_type, entity_id, date_str)
);

