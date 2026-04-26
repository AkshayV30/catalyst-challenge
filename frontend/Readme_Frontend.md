#  AI Talent Scouting Dashboard (Frontend)

A lightweight recruiter dashboard UI for an **AI-Powered Talent Scouting & Engagement Agent**.

It visualizes AI outputs from a backend system that:

* Parses Job Descriptions
* Matches candidates
* Simulates engagement interest
* Produces ranked hiring decisions

---

#  Challenge Objective

Recruiters spend significant time screening profiles and evaluating candidate interest.

This system solves that by:

* Taking a **Job Description as input**
* Discovering matching candidates via AI
* Simulating conversational engagement to estimate interest
* Producing a **ranked shortlist**

Each candidate is evaluated on:

*  Match Score (skill + role alignment)
*  Interest Score (engagement simulation output)

---

# System Flow (Frontend View)

```text
JD Input (UI)
      ↓
Backend AI Pipeline Trigger
      ↓
JD Parsing + Candidate Matching
      ↓
Engagement Simulation (Interest Estimation)
      ↓
Ranking Engine
      ↓
Frontend Dashboard Rendering
```

---

#  Core UI Modules



## 1.  Job Description Input

* Paste a Job Description or select one from the jobs table below
* Choose a matching mode (controls how strictly the AI filters candidates)
* Click **Run Pipeline** to start candidate scouting

Each mode adjusts how the AI interprets the job and filters candidates:

* **very_loose** → maximum reach, very broad matching (exploration mode)
* **loose** → broad matching with slight skill preference
* **balanced** → standard recruiter behavior (recommended default)
* **default** → slightly stricter than balanced, more skill-focused
* **focused** → requires stronger skill alignment + must-have checks
* **strict** → high precision filtering, fewer but stronger candidates
* **very_strict** → extremely strict filtering, only top matches pass

---


---

## 2.  Pipeline Overview

Displays:

* Total candidates processed
* Shortlisted candidates
* Pipeline latency

---

## 3.  Ranked Candidate Shortlist

Each candidate shows:

* Rank
* Name
* Role
* Match Score
* Interest Score
* Final Score 

---

## 4.  Explainability View (Per Candidate)

Shows reasoning behind selection:

* Skill overlap with JD
* Matching logic summary
* Missing skills
* AI-generated selection rationale

---

## 5.  Scoring Logic

Each mode defines:

* How strict filtering is
* How important skills vs interest are

---

##  very_loose

* Min skills: **1**
* Must-have:  No
* Weights: **Match 50% | Interest 50%**
* Use: Maximum reach, explore all candidates

---

##  loose

* Min skills: **1**
* Must-have:  No
* Weights: **Match 55% | Interest 45%**
* Use: Broad search with slight skill preference

---

##  balanced

* Min skills: **2**
* Must-have:  No
* Weights: **Match 60% | Interest 40%**
* Use: Default recruiter mode (recommended)

---

##  default

* Min skills: **2**
* Must-have:  No
* Weights: **Match 70% | Interest 30%**
* Use: More skill-focused shortlisting

---

##  focused

* Min skills: **3**
* Must-have:  Yes
* Weights: **Match 75% | Interest 25%**
* Use: Strong skill alignment required

---

## strict

* Min skills: **3**
* Must-have:  Yes
* Weights: **Match 85% | Interest 15%**
* Use: High precision hiring

---

##  very_strict

* Min skills: **4**
* Must-have:  Yes
* Weights: **Match 90% | Interest 10%**
* Use: Only top-tier exact matches

---

#  Scoring Logic (Same for All Modes)

```text
Final Score = (Match Score × Match Weight) + (Interest Score × Interest Weight)
```

## 6.  Results Table View

Tabular view of final ranked candidates:

* Clean comparison format
* Quick recruiter decision-making interface
* Inline breakdown of scores

---

#  Tech Stack

### Core

* Vanilla JavaScript (modular architecture)
* HTML5
* CSS3
* Vite (recommended)

### Data Layer

* Fetch API
* Lightweight global store pattern

### Backend Integration

* REST API (`/scout`, `/jobs`, `/candidates`)

---

#  Project Structure

```text
frontend/
├── src/
│   ├── api/
│   │   ├── client.js
│   │   ├── data.api.js
│   │   ├── scout.api.js
│   │
│   ├── services/
│   │   └── pipelineService.js
│   │
│   ├── store/
│   │   └── appStore.js
│   │
│   ├── ui/
│   │   ├── components/
│   │   │   ├── JobInput/
│   │   │   ├── Candidates/
│   │   │   ├── Pipeline/
│   │   │   └── Tabs/
│   │   │
│   │   ├── renderers/
│   │   ├── utils/
│   │   └── app/
│   │
│   ├── main.js
│
├── index.html
├── style.css
└── README.md
```

---

#  Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-talent-dashboard.git
cd frontend
```

---

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Configure Backend

Create `.env`:

```env
VITE_API_BASE_URL=http://localhost:8008
```

---

## 4. Run Frontend

```bash
npm run dev
```

Access:

```text
http://localhost:5173
```

---

# Backend Integration

## Run Scouting Pipeline

```http
POST /scout
```

---

## Sample Response

```json
{
  "total_candidates": 14,
  "shortlist_count": 5,
  "latency": 192.19,
  "shortlist": [
    {
      "rank": 1,
      "name": "Ananya Iyer",
      "role": "DevOps Engineer",
      "match_score": 78,
      "engagement_score": 62,
      "final_score": 72,
      "matched_skills": ["Kubernetes", "CI/CD", "GCP"]
    }
  ]
}
```


