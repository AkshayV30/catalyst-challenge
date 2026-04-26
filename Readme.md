# AI Talent Scouting & Engagement Agent

An end-to-end **AI-powered recruitment system** that automates:

* Job Description understanding
* Candidate discovery
* Skill matching
* Engagement simulation
* Explainable ranking

---

# Repository Structure Overview

This repository is organized into **4 main modules**:

```text id="repo_tree"
.
├── backends/        → AI engine (FastAPI + LLM pipeline)
├── frontend/       → Recruiter dashboard UI
├── docs/           → Architecture + setup documentation
└── backends/data/           → Sample datasets (jobs + candidates)
```

---

#  What Each Folder Does

##  `/backends` — AI Engine (Core System)

This is the **brain of the system**.

### Contains:

```text id="backend_tree"
backend/
├── app/
│   ├── agents/        → JD parsing, matching, engagement agents
│   ├── services/      → ranking, shortlist, pipeline logic
│   ├── utils/         → filters, scoring, helpers
│   ├── configs/       → mode config, LLM config
│   ├── router/        → LLM routing system
│   ├── core/          → logging, metrics, ollama client
│   ├── schemas/       → Pydantic models
│   └── api/           → FastAPI routes
│
├── data/              → local dummy datasets
├── logs/              → system logs (auto-generated)
├── main.py            → FastAPI entry point
└── requirements.txt
```

### Responsibilities:

* Runs full AI pipeline
* Handles LLM orchestration
* Computes match + engagement scores
* Produces ranked shortlist

---

##  `/frontend` — Recruiter Dashboard

UI layer for recruiters.

### Contains:

```text id="frontend_tree"
frontend/
├── src/
│   ├── ui/            → dashboard components
│   ├── api/           → backend API calls
│   ├── services/      → pipeline service layer
│   ├── store/         → state management
│   └── main.js
│
├── index.html
├── style.css
└── README.md
```

### Responsibilities:

* Submit Job Descriptions
* Trigger AI pipeline
* View ranked candidates
* Inspect explainability + scores

---

##  `/docs` — System Documentation

### Contains:

* System architecture diagrams
* Design decisions
* API documentation
* Scoring logic explanation
* LLM routing design

### files:

```text id="docs_tree"
docs/
├── architecture.md
├── scoring-system.md
├── api-ref.md
└── system-design.md
```

---

## `backends/data` — Sample Dataset

Used for local testing and development.

```text id="data_tree"
data/
├── candidates.json   → sample candidate profiles
├── job_descriptions.json → sample JDs
```



#  How the System Works 

```text id="flow"
Frontend (JD Input)
        ↓
Backend API (/scout)
        ↓
JD Parser (LLM)
        ↓
Candidate Discovery
        ↓
Matching + Engagement
        ↓
Ranking Engine
        ↓
Explainable Shortlist
        ↓
Frontend Dashboard
```

---

#  Quick Start

## 1. Clone Repo

```bash id="clone"
git clone https://github.com/your-org/ai-talent-scouting.git
cd ai-talent-scouting
```

---

## 2. Start Backend

```bash id="backend_run"
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 3. Start Frontend

```bash id="frontend_run"
cd frontend
npm install
npm run dev
```

---

## 4. Open Dashboard

```text id="ui_url"
http://localhost:5173
```

---

# 🧠 Core Capabilities

* 🧾 JD Parsing (LLM-based structured extraction)
* 🔎 Candidate discovery engine
* 🧠 Match scoring system
* 💬 Engagement simulation
* 📊 Dual-score ranking system
* 🧾 Explainable AI decisions
* 🔁 Multi-model LLM routing

---

# ⚙️ System Design Principles

* Modular microservice-style backend
* LLM abstraction layer (router-based)
* Config-driven scoring system
* Fast prefilter → expensive LLM later
* Explainability-first AI design
* Fully testable with dummy data

---

# 📌 Environment Summary

| Component | Technology          |
| --------- | ------------------- |
| Backend   | FastAPI + Python    |
| AI Layer  | Ollama / LLM Router |
| Frontend  | Vanilla JS / Vite   |
| Data      | JSON datasets       |
| Logging   | Loguru              |
| Config    | ENV-based system    |

---

# 🏁 Project Status

* ✅ Backend pipeline complete
* ✅ LLM routing system active
* ✅ Candidate ranking system working
* ✅ Engagement simulation integrated
* ⚠️ Frontend UI enhancements ongoing
* ⚠️ Real-time streaming optional upgrade

---

# 📈 Future Enhancements

* WebSocket real-time pipeline
* Resume upload + parsing
* Bias detection system
* Advanced analytics dashboard
* Docker + Kubernetes deployment
* Cloud LLM integration (OpenAI / Vertex AI)

---

If you want next upgrade, I can also generate:

* 🎯 **super polished “one-page startup pitch README”**
* 🧭 **interactive architecture diagram (SVG / draw.io)**
* 🐳 **full Dockerized production setup**
* 📊 **system design interview explanation script**
