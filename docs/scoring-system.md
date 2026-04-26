

#  Scoring System — AI Talent Scouting & Engagement Agent

This document explains how candidates are evaluated, scored, and ranked in the system.

---

#  Overview

Each candidate is evaluated on **two core dimensions**:

1.  **Match Score** → How well the candidate fits the Job Description
2.  **Engagement Score** → How interested the candidate is in the opportunity

These are combined into a final ranking score.

---

#  Final Scoring Formula

```text id="final_score"
Final Score = (Match Score × Wm) + (Engagement Score × We)
```

Where:

* **Wm** = Match weight
* **We** = Engagement weight
* Weights depend on recruiter-selected mode

---

#  Score Components

## 1.  Match Score (0–100)

### What it measures:

How well a candidate fits the Job Description.

### Computed using:

* Skill overlap
* Role alignment
* Must-have matching
* Experience compatibility
* LLM reasoning (semantic fit)

### Output:

```json id="match_score"
{
  "match_score": 78,
  "reasons": [
    "Strong Kubernetes experience",
    "AWS + CI/CD alignment",
    "3+ years DevOps exposure"
  ]
}
```

---

## 2.  Engagement Score (0–100)

### What it measures:

Likelihood of candidate interest in the role.

### Computed using:

* Simulated recruiter conversation
* LLM-generated responses (or fallback logic)
* Behavioral signals

### Signals:

* willingness to switch
* tone of response
* engagement strength

### Output:

```json id="engagement_score"
{
  "interest_score": 65,
  "reply": "I am open to discussing this opportunity",
  "signals": [
    "skill_overlap=3",
    "positive_tone"
  ]
}
```

---

#  Mode-Based Weighting System

The system dynamically adjusts scoring based on recruiter intent.

| Mode        | Match Weight | Engagement Weight | Behavior              |
| ----------- | ------------ | ----------------- | --------------------- |
| very_loose  | 0.50         | 0.50              | exploratory hiring    |
| loose       | 0.55         | 0.45              | flexible screening    |
| balanced    | 0.60         | 0.40              | standard hiring       |
| default     | 0.70         | 0.30              | safe default          |
| focused     | 0.75         | 0.25              | skill-heavy filtering |
| strict      | 0.85         | 0.15              | precision hiring      |
| very_strict | 0.90         | 0.10              | elite filtering       |

---

#  Why Two Scores?

Traditional ATS systems only measure:

>  "Does this candidate match the JD?"

This system also measures:

>  "Will this candidate actually respond and engage?"

This creates a more **real-world hiring signal**.

---

#  Example Calculation

## Input Scores:

* Match Score = 80
* Engagement Score = 60

## Mode: balanced

```text id="example_calc"
Final Score =
(80 × 0.6) + (60 × 0.4)
= 48 + 24
= 72
```

---

#  Ranking Behavior

After scoring:

1. All candidates receive Match + Engagement scores
2. Final Score is computed
3. Candidates are sorted descending
4. Top N candidates are selected for shortlist

---

#  Explainability Layer

Each score includes reasoning:

### Match Explanation:

* Skill overlap details
* Missing skills
* Role alignment

### Engagement Explanation:

* Conversation response
* Behavioral signals
* Interest indicators

---

#  Prefilter Impact (Before Scoring)

Before scoring, candidates may be filtered using:

* Minimum skill overlap
* Must-have requirements
* Mode-based constraints

This reduces noise before LLM evaluation.

---

#  Scoring Pipeline Flow

```text id="score_flow"
Candidate Pool
      ↓
Prefilter (fast rules)
      ↓
Match Score (LLM + rules)
      ↓
Engagement Score (LLM/simulation)
      ↓
Weight Application
      ↓
Final Score
      ↓
Ranking
```

---

#  Key Design Principles

* Hybrid scoring (LLM + deterministic rules)
* Dual-dimensional evaluation (fit + interest)
* Mode-driven adaptability
* Explainability-first scoring
* Robust fallback handling
* Production-safe ranking logic

---

#  Summary

The scoring system ensures:

 - Candidates are technically relevant
 - Candidates are likely to respond
 - Recruiters can adjust strictness dynamically
- Final ranking is explainable and reproducible

---
