# LearnSphere AI: Adaptive Intelligence for Personalized Learning and Misconception Detection

**Domain:** Artificial Intelligence in Education, Educational Data Mining, Intelligent Tutoring Systems (ITS)

---

## 1. Executive Summary

LearnSphere AI is a production-grade, intelligent educational web application engineered to solve the core limitation of conventional e-learning: static binary scoring. Instead of treating assessments as generic percentage scores that obscure why a student failed, LearnSphere AI integrates **Bayesian Knowledge Tracing (BKT)** to infer latent concept mastery in real time, coupled with an explicit **Cognitive Misconception Detection Engine** that diagnoses specific programming mental bugs directly from labeled distractors.

The platform provides role-based interfaces for students and faculty, interactive learning modules covering Python programming, dynamic prerequisite-driven roadmaps, and longitudinal learning analytics powered by Plotly.

---

## 2. Core Architecture and Intelligence Modules

### A. Bayesian Knowledge Tracing (BKT) Engine
The platform implements the standard Corbett & Anderson (1995) formulation of Bayesian Knowledge Tracing. For each student and curriculum concept, the system maintains a latent mastery probability $P(L_t) \in [0.0, 1.0]$.

- **$P(L_0)$ (Initial Mastery):** Prior probability that the learner has mastered the skill prior to engaging in practice (configured per concept based on difficulty, typically $0.10$ to $0.25$).
- **$P(T)$ (Transition Probability):** Probability of transitioning from an unmastered state to a mastered state during an instructional or assessment opportunity (typically $0.10$ to $0.18$).
- **$P(G)$ (Guess Probability):** Probability of correctly answering an item despite not having mastered the latent concept (set to $0.20$ for 4-option multiple choice questions).
- **$P(S)$ (Slip Probability):** Probability of making an error despite possessing latent mastery (set between $0.08$ and $0.14$).

#### Mathematical Update Formulations:
1. **Observation Update (Posterior given observation):**
   - If response is correct ($obs = 1$):
     $$P(L_t \mid obs=1) = \frac{P(L_t) \times (1 - P(S))}{P(L_t) \times (1 - P(S)) + (1 - P(L_t)) \times P(G)}$$
   - If response is incorrect ($obs = 0$):
     $$P(L_t \mid obs=0) = \frac{P(L_t) \times P(S)}{P(L_t) \times P(S) + (1 - P(L_t)) \times (1 - P(G))}$$

2. **Transition Step (Prior for next opportunity):**
   $$P(L_{t+1}) = P(L_t \mid obs) + (1 - P(L_t \mid obs)) \times P(T)$$

3. **Mastery Classification Tiers:**
   - **Mastered:** $P(L) \ge 0.85$
   - **Proficient:** $0.65 \le P(L) < 0.85$
   - **Developing:** $0.40 \le P(L) < 0.65$
   - **Novice:** $P(L) < 0.40$

### B. Cognitive Misconception Detection Engine
Rather than relying on uninterpretable NLP hallucinations, LearnSphere AI utilizes an explicit, rule-verified taxonomy of programming misconceptions based on computer science education research (CSEd). Each distractor option in the question bank is tagged with a structured diagnostic code:

| Diagnostic Code | Category | Cognitive Bug Description | Pedagogical Remediation |
|---|---|---|---|
| `OFF_BY_ONE_INDEX` | Data Structures | Confusing 0-based indexing with length or range stop inclusivity | Review half-open intervals `[start, stop)` and slice bounds |
| `TYPE_COERCION_CONFUSION` | Data Types | Assuming implicit string-to-number coercion or `input()` returns numbers | Always cast explicit numeric types via `int()` or `float()` |
| `VARIABLE_MUTATION_CONFUSION` | Variables | Believing string operations mutate objects in place without reassignment | Strings are immutable in Python; assign returned copies |
| `BOOLEAN_SHORT_CIRCUIT` | Logic | Writing `if x == 1 or 2` expecting equality comparison across both terms | Disjunction evaluates `bool(2) == True`; use `if x in (1, 2)` |
| `LOOP_TERMINATION_STEP` | Control Flow | Misunderstanding loop entry condition checks or range step arguments | Trace state invariants monotonically approaching the bound |
| `LIST_ALIASING_SHADOWING` | Data Structures | Believing assignment `b = a` copies a list rather than aliasing references | Assignment binds pointers; use `a.copy()` to clone lists |
| `RETURN_VALUE_OMISSION` | Functions | Treating `print()` as returning a value to caller expressions | `print()` returns `None`; use explicit `return` for computation |
| `SCOPE_LEAKAGE` | Functions | Expecting function-local variables to persist into caller or global scope | Local namespaces are discarded when the call frame exits |
| `BASE_CASE_OMISSION` | Recursion | Omitting or misplacing the termination condition, causing stack overflow | Ensure base case returns prior to recursive descent |
| `RECURSIVE_ACCUMULATOR_RETURN` | Recursion | Invoking recursive call without returning or capturing its result | Every branch in recursive computation must return the value |

### C. Adaptive Recommendation and Learning Path Engine
- **Prerequisite Dependency Graph (DAG):**
  - Variables & Data Types (`VAR`)
  - Conditional Statements (`COND`) &rarr; requires `VAR`
  - Loops (`LOOP`) &rarr; requires `VAR`, `COND`
  - Lists and Arrays (`LIST`) &rarr; requires `VAR`, `LOOP`
  - Functions (`FUNC`) &rarr; requires `VAR`, `COND`, `LOOP`
  - Recursion (`REC`) &rarr; requires `FUNC`, `COND`
- **Prerequisite Gap Detection:** If a student encounters repeated failures in an advanced topic (e.g. Recursion), the recommender evaluates foundational prerequisites and blocks advancement until prerequisites meet the $60\%$ mastery threshold.
- **Adaptive Difficulty Selection:** Matches question difficulty (Beginner, Intermediate, Advanced) dynamically to current BKT mastery to sustain the learner within their Zone of Proximal Development.

---

## 3. Database Architecture (SQLite)

The persistence layer uses SQLite with write-ahead logging (WAL), foreign key constraints, and parameterized SQL queries to prevent injection vulnerabilities:

1. **`users`:** Stores student and faculty profiles, salt, PBKDF2 password hashes (100,000 iterations), roles, and study goals.
2. **`concepts`:** Curriculum units with BKT parameters ($P(L_0), P(T), P(G), P(S)$) and prerequisite lists.
3. **`questions`:** Calibrated question bank with code snippets, 4 answer options, and labeled misconception codes.
4. **`learning_content`:** Deep educational content with code demonstrations, common errors, and practice drills.
5. **`assessment_attempts`:** Full telemetry logging question id, selected option, correctness, latency (seconds), misconception code, and prior/posterior mastery.
6. **`student_mastery`:** Persistent BKT mastery estimates per student and concept.
7. **`lesson_progress`:** Module completion tracking.
8. **`learning_recommendations`:** Dynamically prioritized pedagogical recommendations.

---

## 4. Demonstration Profiles for Live Evaluation

LearnSphere AI includes built-in demonstration accounts pre-seeded with distinct cognitive histories:

### Student Persona 1: Primary Requested Account
- **Email / Username:** `student@123`
- **Password:** `student123`
- **Profile:** Demonstrates mastered foundational topics (Variables: 88%, Conditionals: 72%), but exhibits repeating cognitive misconceptions in Loops (Off-by-One indexing errors) and Recursion (Base case omission).
- **Use Case:** Showcases how the Misconception Diagnostics and Recommendation engines flag specific mental errors and recommend prerequisite remediation.

### Student Persona 2: Sophia Chen
- **Username:** `sophia_chen`
- **Password:** `student123`
- **Profile:** Advanced proficient student with high mastery across core modules (Variables: 94%, Conditionals: 91%, Loops: 86%, Lists: 82%, Functions: 78%), currently practicing advanced Recursion.
- **Use Case:** Showcases adaptive question difficulty routing to advanced questions and curriculum milestone completion.

### Teacher Persona: Dr. Sarah Bennett
- **Username:** `dr_bennett`
- **Password:** `learnsphere123`
- **Profile:** Faculty account with full access to cohort mastery distributions, class-wide misconception bottlenecks, and individual student diagnostic inspection.
- **Use Case:** Demonstrates institutional analytics, systemic misconception detection, and individualized office hour support.

---

## 5. UI Design System Guidelines

- **Color Palette:** Clean white/slate background (`#f8fafc`, `#ffffff`) with deep navy text (`#0f172a`, `#1e293b`) and indigo/purple accents (`#4f46e5`, `#6366f1`).
- **Typography:** Inter, readable hierarchy, standardized card containers and metric cards.
- **No Emojis:** Replaced entirely with clean semantic badges and Lucide SVG icons.
- **No Decorative Hyphens:** Clean headings, structured labels, and readable prose.
- **Visualizations:** Interactive Plotly charts (BKT radar chart, longitudinal mastery lines, latency histograms, and cohort bar charts).

---

## 6. Setup, Installation, and Local Execution

### Prerequisites
- Python 3.10+ (Verified on Python 3.15)
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/maruthi-gunisetty/innovex-nov16.git
   cd innovex-nov16
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Initialize the database (optional, runs automatically on startup):**
   ```bash
   python database/seed_data.py
   ```

4. **Launch the web application:**
   ```bash
   python -m streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 7. Automated Test Suite

LearnSphere AI includes a comprehensive unit testing suite verifying all algorithmic and database functions:

```bash
python -m unittest discover tests
```

### Test Coverage:
- **`tests/test_bkt.py`:** Verifies Corbett & Anderson mathematical formulas, correct/incorrect observation updates, next-prior transitions, and classification boundaries.
- **`tests/test_misconception.py`:** Verifies taxonomy lookups, diagnostic mapping, and pattern frequency aggregation.
- **`tests/test_recommender.py`:** Verifies prerequisite graph validation, adaptive difficulty assignment, and recommendation prioritization.
- **`tests/test_db.py`:** Verifies SQLite connection management, PBKDF2 password hashing, user authentication, attempt recording, and concept retrieval.

All 17 tests pass with zero errors.

---

## 8. Deployment to Streamlit Community Cloud

To deploy to Streamlit Community Cloud:
1. Push this repository to GitHub (`maruthi-gunisetty/innovex-nov16`).
2. Log into [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub repository:
   - **Repository:** `maruthi-gunisetty/innovex-nov16`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**. The application will automatically install packages from `requirements.txt`, initialize the SQLite database, and launch.

