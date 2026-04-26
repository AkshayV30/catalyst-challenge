#  API Reference — AI Talent Scouting & Engagement Agent

This document describes all backend APIs exposed by the **AI-Powered Talent Scouting System**.

---

#  Base URL

```text
http://localhost:8000
```

---

#  Authentication

Currently **no authentication is required** (development mode).

> Future: JWT / API Key-based auth can be added.

---

#  Core API Endpoints

---

# 1.  Run Talent Scouting Pipeline

## POST `/scout`

Runs the full AI pipeline:

* JD parsing
* Candidate retrieval
* Matching
* Engagement simulation
* Ranking + shortlist generation

---

## Request Body

```json
{
  "jd": "string (Job Description text)",
  "mode": "default | balanced | strict | loose | very_loose | focused | very_strict"
}
```

---

## Example Request

```json
{
  "jd": "We are looking for a DevOps Engineer with Kubernetes, Docker and AWS experience",
  "mode": "balanced"
}
```

---

## Response

```json
{
  "parsed_jd": {
    "role": "DevOps Engineer",
    "skills": ["Kubernetes", "Docker", "AWS"],
    "experience_years": 3,
    "must_have": ["Kubernetes"],
    "nice_to_have": ["Terraform"]
  },

  "mode": "balanced",

  "weights": {
    "match": 0.6,
    "engagement": 0.4
  },

  "total_candidates": 120,
  "after_prefilter": 35,
  "after_retrieval": 10,

  "shortlist_count": 5,

  "shortlist": [
    {
      "rank": 1,
      "candidate_id": "C102",
      "name": "John Doe",
      "role": "DevOps Engineer",
      "experience": 4,

      "final_score": 82.5,
      "match_score": 85,
      "engagement_score": 78,

      "top_skills": ["Kubernetes", "AWS", "Docker"],

      "why_selected": [
        "Strong Kubernetes experience",
        "Matches AWS + Docker requirements"
      ]
    }
  ],

  "latency": 3.42
}
```

---

##  What This Endpoint Does Internally

```text
JD → Parser → Validator → Candidate Loader
   → Prefilter → Retrieval Agent
   → Matching LLM
   → Engagement Agent (LLM/Simulation)
   → Ranking Engine
   → Shortlist Builder
```

---

# 2.  Metrics API

## GET `/metrics`

Returns system performance stats.

---

## Response

```json
{
  "calls": 120,
  "failures": 3,
  "avg_latency": 2.87
}
```

---

# 3.  Get Candidates (Debug)

## GET `/candidates`

Returns all available candidate data.

---

## Response

```json
{
  "candidates": [
    {
      "id": "C101",
      "name": "Alice",
      "skills": ["Python", "Docker"]
    }
  ]
}
```

---

# 4.  Get Jobs (Debug)

## GET `/jobs`

Returns sample job descriptions.

---

## Response

```json
{
  "jobs": [
    {
      "id": "J1",
      "role": "DevOps Engineer",
      "skills": ["Kubernetes", "AWS"]
    }
  ]
}
```

---

# 5.  Health Check

## GET `/`

Simple backend status page.

---

## Response

```html
Backend API is Running
Status: OK
```

---

# Mode System 

Each mode controls:

### 1. Filtering Strictness

### 2. Scoring Weights

### 3. JD Interpretation Style

---

## Supported Modes

| Mode        | Behavior                    |
| ----------- | --------------------------- |
| very_loose  | Broad matching, exploratory |
| loose       | Relaxed filtering           |
| balanced    | Default production mode     |
| default     | Same as balanced            |
| focused     | Strong constraints          |
| strict      | High precision matching     |
| very_strict | Only exact matches          |

---

## Internal Effect

```text
Mode → Filter Rules + Score Weights + JD Parsing Style
```

Example:

```json
"balanced": {
  "filter": { "min_skill_overlap": 2 },
  "weights": { "match": 0.6, "engagement": 0.4 }
}
```

---

#  Scoring System (Backend Usage)

Final ranking formula:

```text
Final Score =
( Match Score × match_weight )
+
( Engagement Score × engagement_weight )
```

---

## Example (Balanced Mode)

```text
Final Score =
( Match × 0.6 ) + ( Engagement × 0.4 )
```

---

#  Data Flow Summary

```text
JD Input
   ↓
LLM JD Parser
   ↓
Validation Layer
   ↓
Candidate Loader
   ↓
Prefilter Engine
   ↓
Retrieval Agent
   ↓
Match LLM
   ↓
Engagement Agent
   ↓
Ranking Engine
   ↓
Shortlist Builder
   ↓
API Response
```

---

#  Error Handling

All endpoints return structured errors:

```json
{
  "error": "Missing 'jd' field"
}
```

or

```json
{
  "error": "Invalid JSON body"
}
```

---

# Performance Notes

* Async candidate processing (`asyncio.gather`)
* Semaphore-based concurrency control
* LLM router fallback system
* Multi-model retry support
* Structured logging (Loguru)

---

#  Dev Notes

This API is designed for:

* AI agent evaluation systems
* Hiring automation pipelines
* LLM orchestration experiments
* Talent ranking research systems

---
