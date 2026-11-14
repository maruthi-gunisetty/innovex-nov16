# SARVAVIDYA: Enterprise Multi-Subject AI Learning & Cognitive Analytics

**Brand:** SARVAVIDYA  
**Tagline:** One Platform. Every Subject. Infinite Knowledge.  
**Domain:** Artificial Intelligence in Education, Educational Data Mining, Intelligent Tutoring Systems (ITS)  
**Live 24/7 Deployment (Render):** [https://innovex-nov16.onrender.com/](https://innovex-nov16.onrender.com/)

---

### 🚀 Permanent Cloud Access
* **Live Website URL:** **[https://innovex-nov16.onrender.com/](https://innovex-nov16.onrender.com/)**
* **Demo Student Account:** `student@123` / `student123`
* **Demo Faculty Account:** `teacher@123` / `teacher123`
* **Demo Admin Account:** `admin@123` / `admin123`
* **AI Engine:** Google Gemini 3.1 Flash Live + Bayesian Knowledge Tracing (BKT)

---

## 1. Executive Summary

**SARVAVIDYA** is a premium, internationally competitive multi-subject educational platform engineered to transform digital learning. Unifying **Programming** (Python & C Systems), **Mathematics** (Calculus & Linear Algebra), **Engineering**, and **Science**, SARVAVIDYA eliminates static binary scoring by deploying **Corbett & Anderson (1995) Bayesian Knowledge Tracing (BKT)** to track latent student concept mastery in real time, coupled with an explicit **Cognitive Misconception Detection Engine** diagnosing mental bugs directly from labeled distractors.

---

## 2. Brand Identity & Aesthetic Architecture

- **Symbol Composition:**
  - **Left Symbol:** Elegant golden lotus combined with an open book base.
  - **Four Petals:** Representing the four foundational disciplines: Programming, Mathematics, Engineering, and Science.
  - **AI Geometric Core:** A central radiant diamond node with neural connection traces representing cognitive synthesis.
- **Brand Palette:**
  - **Deep Navy:** `#172943`
  - **Royal Navy:** `#243B64`
  - **Premium Gold:** `#D6B56D`
  - **Soft Gold:** `#E8C879`
  - **Pure White:** `#FFFFFF`
  - **Canvas Surface:** `#F5F6F8`
  - **Border Gray:** `#E4E8ED`
- **Typography:**
  - Brand Heading: High-contrast geometric `SARVAVIDYA`
  - Subtitle / Tagline: `One Platform. Every Subject. Infinite Knowledge.`

---

## 3. Core Architecture and Intelligence Modules

### A. Bayesian Knowledge Tracing (BKT) Engine
The platform implements the standard Corbett & Anderson (1995) formulation of Bayesian Knowledge Tracing. For each student and curriculum concept across all supported subjects, the system maintains a latent mastery probability $P(L_t) \in [0.0, 1.0]$.

- **$P(L_0)$ (Initial Mastery):** Prior probability that the learner has mastered the skill prior to engaging in practice (typically $0.10$ to $0.25$).
- **$P(T)$ (Transition Probability):** Probability of acquiring mastery on an instructional or assessment opportunity ($0.15$).
- **$P(G)$ (Guess Probability):** Probability of correctly answering an item without mastery ($0.20$ for 4-option items).
- **$P(S)$ (Slip Probability):** Probability of making an accidental mistake despite latent mastery ($0.10$).

#### Mathematical Formulations:
1. **Observation Update (Posterior given observation):**
   - Correct ($obs = 1$):
     $$P(L_t \mid obs=1) = \frac{P(L_t) \times (1 - P(S))}{P(L_t) \times (1 - P(S)) + (1 - P(L_t)) \times P(G)}$$
   - Incorrect ($obs = 0$):
     $$P(L_t \mid obs=0) = \frac{P(L_t) \times P(S)}{P(L_t) \times P(S) + (1 - P(L_t)) \times (1 - P(G))}$$

2. **Transition Step (Prior for next opportunity):**
   $$P(L_{t+1}) = P(L_t \mid obs) + (1 - P(L_t \mid obs)) \times P(T)$$

3. **Mastery Classification Tiers:**
   - **Mastered:** $P(L) \ge 0.85$
   - **Proficient:** $0.65 \le P(L) < 0.85$
   - **Developing:** $0.40 \le P(L) < 0.65$
   - **Novice:** $P(L) < 0.40$

---

## 4. Multi-Subject Curricula Provisioned

| Subject Domain | Course Track | Core Concepts | Assessment Bank | Interactive Sandbox |
|---|---|---|---|---|
| **Programming** | Python Fundamentals | Variables, Conditionals, Loops, Lists, Functions, Recursion | 28 Calibrated Items | Live In-Browser Python Exec |
| **Programming** | C Systems Programming | Data Types, Control Flow, Pointers, Arrays/Strings, Memory Allocation (`malloc`/`free`), Structs | 12 Calibrated Items | C Memory Safety Analyzer |
| **Mathematics** | Calculus & Linear Algebra | Limits & Continuity, Derivatives, Integrals, Vectors, Matrices, Eigenvalues | 12 Calibrated Items | LaTeX Math Step Evaluator |
| **Engineering** | Circuits & Systems | Active Schema | Extensible via DB | Diagnostic Modeling |
| **Science** | Classical Physics | Active Schema | Extensible via DB | Diagnostic Modeling |
| **Computer Science** | Computer Architecture | Active Schema | Extensible via DB | Diagnostic Modeling |

---

## 5. Demonstration Credentials

- **Student Account:** `student@123` &bull; Password: `student123`
- **Advanced Student:** `sophia_chen` &bull; Password: `student123`
- **Faculty Account:** `dr_bennett` &bull; Password: `learnsphere123`

---

## 6. Local Execution

```powershell
python -m streamlit run app.py --server.headless=true --server.port=8501
```
Local URL: `http://localhost:8501`
