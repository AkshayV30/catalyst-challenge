

#  System Architecture

##  AI-Powered Talent Scouting & Engagement Agent

This document explains the **end-to-end architecture** of the AI recruitment system, covering data flow, services, and intelligence layers.

---

#  High-Level Architecture

```text id="z9qk2a"
                ┌──────────────────────┐
                │   Job Description    │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   JD Parser (LLM)    │
                └─────────┬────────────┘
                          ↓
        ┌────────────────────────────────────┐
        │ Structured JD (skills, role, etc.) │
        └─────────┬──────────────────────────┘
                  ↓
        ┌────────────────────────────────────┐
        │ Candidate Discovery Engine         │
        │ (Skill-based retrieval + scoring)  │
        └─────────┬──────────────────────────┘
                  ↓
        ┌────────────────────────────────────┐
        │ Matching Engine (LLM + rules)      │
        │ Engagement Engine (simulated/LLM)  │
        └─────────┬──────────────────────────┘
                  ↓
        ┌────────────────────────────────────┐
        │ Ranking Engine (Dual Score System) │
        └─────────┬──────────────────────────┘
                  ↓
        ┌────────────────────────────────────┐
        │ Explainable Shortlist Output       │
        └────────────────────────────────────┘
```

---

#  Core System Layers

## 1.  Input Layer (Job Description)

### Responsibility:

Accept raw job descriptions from recruiters.

### Output:

* Unstructured JD text

### Example:

```text
Senior DevOps Engineer with Kubernetes and AWS experience...
```

---

## 2.  JD Parsing Layer (LLM Engine)

### Responsibility:

Convert raw JD → structured schema.

### Extracted Fields:

* Role
* Skills
* Must-have skills
* Nice-to-have skills
* Experience requirement

### Behavior Modes:

* very_loose → broad extraction
* balanced → standard extraction
* strict → precise constraint extraction

---

## 3.  Candidate Discovery Layer

### Responsibility:

Pre-filter candidate pool before LLM processing.

### Mechanisms:

* Skill overlap scoring
* Tool matching
* Experience boost factor
* Configurable thresholds

### Output:

Ranked candidate subset

---

## 4.  Matching Engine (Fit Intelligence)

### Responsibility:

Evaluate how well a candidate matches the JD.

### Output:

```text
Match Score (0–100)
Explainability Reasons
```

### Inputs:

* Structured JD
* Candidate profile

### Logic:

* Skill alignment
* Role similarity
* Requirement coverage

---

## 5.  Engagement Engine (Interest Simulation)

### Responsibility:

Simulate recruiter–candidate interaction.

### Output:

```text
Interest Score (0–100)
Conversation Logs
Behavior Signals
```

### Modes:

* LLM-based response generation
* Fallback rule-based simulation

### Signals:

* willingness
* response tone
* engagement strength

---

## 6.  Ranking Engine (Decision Layer)

### Responsibility:

Combine signals into final decision score.

### Formula:

```text id="ranking_formula"
Final Score =
(Match Score × weight) +
(Engagement Score × weight)
```

### Weights depend on mode:

* strict → match-heavy
* loose → balanced
* very_loose → engagement-heavy

---

## 7.  Explainability Layer (XAI)

### Responsibility:

Make AI decisions transparent.

### Outputs:

* Why candidate was selected
* Skill overlap breakdown
* Matching reasoning
* Engagement signals

 Ensures **no black-box hiring decisions**

---

#  Mode Configuration System

The system supports dynamic recruiter strategies:

| Mode        | Purpose          | Behavior           |
| ----------- | ---------------- | ------------------ |
| very_loose  | exploration      | broad matching     |
| loose       | flexible hiring  | relaxed filtering  |
| balanced    | default hiring   | balanced scoring   |
| default     | fallback mode    | safe standard      |
| focused     | precision hiring | strict skills      |
| strict      | high confidence  | hard constraints   |
| very_strict | elite filtering  | only exact matches |

---

#  Service Architecture

```text id="svc_arch"
FastAPI Layer
        ↓
Pipeline Orchestrator
        ↓
LLM Router (Multi-model fallback)
        ↓
Agent System:
   ├── JD Parser Agent
   ├── Candidate Discovery Agent
   ├── Matching Agent
   ├── Engagement Agent
   ├── Ranking Service
        ↓
Output Layer (Explainable Shortlist)
```

---

#  LLM Router Design

### Features:

* Multi-model fallback support
* Retry mechanism
* Timeout handling
* Task-based routing

### Tasks:

* JD parsing
* Candidate matching
* Engagement simulation

---

# Reliability & Safety Design

## 1. JSON Recovery Layer

* fixes malformed LLM outputs
* removes markdown
* extracts structured objects

## 2. Validation Pipeline

* ensures role correctness
* validates skill lists
* removes hallucinated fields

## 3. Fallback Systems

* simulated engagement if LLM fails
* safe default scoring
* partial pipeline recovery

---

# Data Flow Summary

```text id="flow_summary"
JD → Parser → Structured JD
         ↓
Candidate Pool
         ↓
Prefilter (fast rules)
         ↓
LLM Matching + Engagement
         ↓
Scoring Engine
         ↓
Ranking + Explainability
         ↓
Final Shortlist
```

---

