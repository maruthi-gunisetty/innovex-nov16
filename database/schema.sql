-- LearnSphere AI Database Schema
-- Robust schema for student performance, BKT mastery, and misconception tracking

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

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    p_init REAL DEFAULT 0.20,
    p_transit REAL DEFAULT 0.15,
    p_guess REAL DEFAULT 0.20,
    p_slip REAL DEFAULT 0.10,
    prerequisites TEXT DEFAULT '[]' -- JSON array of concept codes
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

