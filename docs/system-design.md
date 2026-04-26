

# System Design — AI-Powered Talent Scouting & Engagement Agent

This document explains the **end-to-end system architecture, components, data flow, and design decisions** behind the AI Talent Scouting platform.

---

#  Problem Statement

Recruiters spend significant time:

* Parsing job descriptions
* Searching candidate databases
* Assessing skill fit manually
* Engaging candidates one-by-one
* Ranking subjective fit vs interest

---

# Solution Overview

We design an **AI multi-agent pipeline system** that:

```text
Job Description → AI Understanding → Candidate Discovery → Matching → Engagement Simulation → Ranking → Shortlist
```

Outputs:

* Ranked candidates
* Explainable match reasoning
* Engagement score (interest probability)
* Final recruiter-ready shortlist

---

# High-Level Architecture

```text
                 ┌────────────────────┐
                 │   Frontend UI      │
                 │ (React/Vite)       │
                 └────────┬───────────┘
                          │ /scout API
                          ▼
              ┌──────────────────────────┐
              │     FastAPI Backend      │
              └────────┬─────────────────┘
                       │
        ┌──────────────┼──────────────────────┐
        ▼              ▼                      ▼
 ┌────────────┐ ┌──────────────┐   ┌─────────────────┐
 │ JD Parser  │ │ Candidate DB │   │ LLM Router      │
 │ (LLM)      │ │ (JSON/Data)  │   │ (multi-model)   │
 └────┬───────┘ └─────┬────────┘   └────────┬────────┘
      ▼               ▼                     ▼
 ┌────────────┐ ┌──────────────┐   ┌─────────────────┐
 │ Validator  │ │ Retrieval     │   │ Engagement Agent│
 │ Pipeline   │ │ Engine        │   │ (LLM + fallback)│
 └────┬───────┘ └─────┬────────┘   └────────┬────────┘
      ▼               ▼                     ▼
        ┌────────────────────────────────────────┐
        │         Ranking Engine                │
        │ (Match Score + Engagement Score)      │
        └────────────────┬──────────────────────┘
                         ▼
                ┌───────────────────┐
                │ Shortlist Builder │
                └───────────────────┘
                         ▼
                 API Response JSON
```

---

#  Core System Components

---

## 1.  JD Parser (LLM-based)

**Responsibility:**

* Extract structured fields from Job Description

### Output Schema

```json
{
  "role": "",
  "skills": [],
  "must_have": [],
  "nice_to_have": [],
  "experience_years": 0
}
```

### Features:

* Mode-based prompting (very_loose → very_strict)
* JSON extraction + repair logic
* Validation pipeline (anti-hallucination layer)

---

## 2.  Validation Layer

Ensures LLM output consistency:

* Skill existence validation
* Must-have filtering
* Role consistency check
* Noise removal

 Prevents hallucinated skills from affecting ranking

---

## 3.  Candidate Discovery Engine

### Function:

* Loads candidate dataset
* Computes initial similarity score

### Logic:

```text
skill_overlap + experience_boost → retrieval_score
```

### Output:

Top-K candidate pool for deeper processing

---

## 4.  Prefilter System

Reduces candidate space before expensive LLM calls:

### Config-driven:

```python
min_skill_overlap
must_have_required
```

### Purpose:

* Reduce LLM cost
* Improve latency
* Eliminate irrelevant candidates early

---

## 5.  Matching Agent (LLM)

### Input:

* JD (structured)
* Candidate profile

### Output:

```json
{
  "match_score": 0-100,
  "reasons": []
}
```

### Responsibilities:

* Deep semantic matching
* Skill-role alignment reasoning
* Explainability generation

---

## 6.  Engagement Agent

Simulates recruiter-candidate interaction:

### Two modes:

*  LLM-based engagement
* Fallback simulation engine

### Output:

```json
{
  "interest_score": 0-100,
  "reply": "",
  "signals": []
}
```

### Signals include:

* Skill overlap
* Role relevance
* Candidate responsiveness prediction

---

## 7.  Ranking Engine

### Core Formula:

\text{Final Score} = (\text{Match Score} \times w_m) + (\text{Engagement Score} \times w_e)

### Mode-driven weights:

| Mode        | Match | Engagement |
| ----------- | ----- | ---------- |
| loose       | 0.55  | 0.45       |
| balanced    | 0.6   | 0.4        |
| default     | 0.7   | 0.3        |
| strict      | 0.85  | 0.15       |
| very_strict | 0.9   | 0.1        |

---

## 8.  Shortlist Builder

Produces recruiter-facing output:

* Clean candidate cards
* Top skills
* Explainability reasons
* Final rank ordering

---

#  Mode System Design

Each mode controls:

### 1. Filtering Strictness

### 2. LLM Interpretation Style

### 3. Scoring Weights

---

## Mode Behavior Map

| Mode        | Behavior                   |
| ----------- | -------------------------- |
| very_loose  | Exploratory, high recall   |
| loose       | Relaxed filtering          |
| balanced    | Production default         |
| default     | Same as balanced           |
| focused     | Strong constraint matching |
| strict      | Precision-heavy ranking    |
| very_strict | Only exact matches         |

---

# End-to-End Data Flow

```text
JD Input
   ↓
JD Parser (LLM)
   ↓
Validation Layer
   ↓
Candidate Loader
   ↓
Prefilter Engine
   ↓
Retrieval Scoring
   ↓
Match Agent (LLM)
   ↓
Engagement Agent (LLM / fallback)
   ↓
Ranking Engine
   ↓
Shortlist Builder
   ↓
API Response
```

---

#  Performance Design

### Concurrency

* `asyncio.gather` for parallel candidate processing
* Semaphore limit = 5

### Optimization

* Prefilter reduces LLM calls
* Cached candidate dataset
* Early rejection filters

---

#  Fault Tolerance

### Fallback layers:

| Component      | Fallback                |
| -------------- | ----------------------- |
| LLM Match      | 0-score default         |
| Engagement LLM | Simulation engine       |
| JSON parsing   | Regex + recovery parser |
| JD parsing     | Empty safe schema       |

---

#  Scalability Considerations

### Current:

* Single FastAPI instance
* Local JSON candidate DB
* Ollama LLM backend

### Future scaling:

* Candidate DB → PostgreSQL / Vector DB
* LLM → distributed inference (GPU cluster)
* Queue system → Redis / Kafka
* Microservices split:

```text
JD Service
Matching Service
Engagement Service
Ranking Service
```

---

#  Reliability Design

* Retry-enabled LLM router
* Timeout protection (28s cap)
* Structured logging (Loguru)
* Metrics tracking layer

---

#  Key Design Philosophy

- Explainability over black-box ranking
- Multi-stage filtering to reduce cost
- Hybrid LLM + deterministic scoring
- Mode-driven system adaptability
- Safe fallback at every layer

---

#  Summary

This system is a **multi-agent AI hiring pipeline** combining:

* LLM reasoning
* Rule-based filtering
* Retrieval scoring
* Engagement simulation
* Weighted ranking



---

