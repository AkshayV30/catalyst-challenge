#  AI-Powered Talent Scouting & Engagement Agent (Backend)

An **AI-driven recruitment engine** that automates candidate discovery, evaluates job fit, simulates engagement, and produces a **ranked, explainable shortlist**.

It replaces manual screening by combining:

* JD understanding (LLM-based parsing)
* Skill-based candidate retrieval
* Explainable matching
* Simulated conversational engagement
* Dual-score ranking system

---

#  Problem It Solves

Recruiters spend significant time:

* Reading and interpreting Job Descriptions
* Searching candidate databases
* Evaluating technical fit manually
* Contacting candidates to gauge interest
* Shortlisting based on incomplete signals

This system automates the entire flow.

---

#  Core Workflow

```text
Job Description (Input)
        ↓
JD Parser (LLM)
        ↓
Structured JD (skills, must-have, experience)
        ↓
Candidate Discovery (skill-based retrieval)
        ↓
Matching Engine (LLM + scoring)
        ↓
Engagement Simulation (LLM / fallback)
        ↓
Ranking Engine (dual-score weighting)
        ↓
Explainable Shortlist (Output)
```

---

#  Key Capabilities (Mapped to Challenge)

## 1. JD Parsing (Understanding Layer)

Extracts structured information from raw JD:

* Role
* Skills
* Must-have requirements
* Nice-to-have requirements
* Experience level

Supports multiple parsing strictness modes via LLM routing.

---

## 2. Candidate Discovery (Retrieval Layer)

Filters and ranks candidates using:

* Skill overlap scoring
* Tool/technology matching
* Experience level boost
* Configurable prefilter rules

Ensures only relevant candidates proceed to LLM stages.

---

## 3. Matching Engine (Fit Score)

Each candidate is evaluated using:

```text
Match Score (0–100)
```

Generated using LLM reasoning:

* Skill alignment
* Role match
* Experience fit
* Requirement overlap

Includes explainability reasons for transparency.

---

## 4. Engagement Engine (Interest Score)

Simulates recruiter outreach:

```text
Interest Score (0–100)
```

Two modes:

*  LLM-based conversational response
*  Deterministic fallback simulation

Captures:

* Candidate willingness
* Response signals
* Message behavior

---

## 5. Ranking Engine (Final Decision Layer)

Combines both signals:

```text
Final Score =
(Match Score × weight) +
(Engagement Score × weight)
```

Weights are dynamically controlled by mode configuration.

---

## 6. Explainability Layer (XAI)

Every shortlisted candidate includes:

* Why they were selected
* Skill overlap breakdown
* Matching rationale
* Engagement signals

Ensures **transparent AI hiring decisions**.

---

#  Mode-Based Scoring System

The system supports multiple recruiter strategies:

| Mode        | Filter Strictness  | Match Weight | Engagement Weight |
| ----------- | ------------------ | ------------ | ----------------- |
| very_loose  | Minimal filtering  | 0.50         | 0.50              |
| loose       | relaxed matching   | 0.55         | 0.45              |
| balanced    | standard (default) | 0.60         | 0.40              |
| default     | balanced fallback  | 0.70         | 0.30              |
| focused     | strict skills      | 0.75         | 0.25              |
| strict      | high precision     | 0.85         | 0.15              |
| very_strict | hard filtering     | 0.90         | 0.10              |

### Filter Behavior

* Controls minimum skill overlap
* Optionally enforces must-have constraints
* Impacts candidate eligibility before LLM processing

---

#  API Endpoints

## POST `/scout`

Runs full AI pipeline.

### Request

```json
{
  "jd": "Job Description text here",
  "mode": "balanced"
}
```

### Response

```json
{
  "parsed_jd": {},
  "mode": "balanced",
  "weights": {
    "match": 0.6,
    "engagement": 0.4
  },
  "total_candidates": 120,
  "after_prefilter": 45,
  "after_retrieval": 10,
  "shortlist_count": 5,
  "shortlist": [],
  "latency": 3.42
}
```

---

## GET `/candidates`

Returns dataset of candidates.

## GET `/jobs`

Returns job dataset.

## GET `/metrics`

System performance metrics:

* API calls
* Failure rate
* Avg latency

---

# Architecture Overview

```text
FastAPI Backend
        ↓
LLM Router (multi-model fallback system)
        ↓
Pipeline Orchestrator
 ├── JD Parser Agent
 ├── Candidate Discovery Agent
 ├── Matching Agent (LLM)
 ├── Engagement Agent (LLM + fallback)
 ├── Ranking Service
        ↓
Explainable Shortlist Output
```

---

#  Core Components

## Agents

* JD Parser Agent (structured extraction)
* Candidate Discovery Agent (retrieval)
* Matching Agent (fit scoring)
* Engagement Agent (interest simulation)

## Services

* Ranking Service
* Shortlist Builder
* Pipeline Orchestrator

##  LLM Layer

* Multi-model router fallback
* Timeout + retry system
* JSON extraction + validation layer

---

#  Reliability & Safety Layers

##  JSON Guardrails

* strict parsing
* markdown removal
* fallback recovery

##  Validation Pipeline

* role validation
* skill validation
* must-have filtering
* experience sanity checks

##  Failure Handling

* fallback candidate scoring
* simulated engagement fallback
* safe empty-state responses

---

#  Scoring System

## Match Score

Derived from:

* Skill overlap
* JD alignment
* LLM reasoning

## Engagement Score

Derived from:

* simulated / LLM response
* candidate willingness signals

## Final Score

Used for ranking shortlist.

---
