


#  Setup Guide — AI Talent Scouting Backend

This guide explains how to set up and run the **AI-Powered Talent Scouting & Engagement Agent** locally.

---

# Prerequisites

Before starting, ensure you have:

* Python **3.10+**
* pip / virtualenv
* Node.js (only if running frontend)
* Docker (optional, for Ollama)
* Ollama installed (for local LLM inference)

---

#  Project Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-talent-scouting.git
cd backend
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate:

### Windows:

```bash
venv\Scripts\activate
```

### Mac/Linux:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the backend root:

```env
APP_NAME=AI Talent Scouting Agent

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GENERATE=/api/generate

# Performance tuning
REQUEST_TIMEOUT=30
RETRY_COUNT=2

# Optional model overrides per task
JD_PARSER_MODELS=llama3,gemma
MATCHER_MODELS=llama3
ENGAGEMENT_MODELS=llama3
```

---

#  LLM Setup (Ollama)

## 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 2. Pull Required Models

```bash
ollama pull llama3
ollama pull gemma
```

---

## 3. Start Ollama Server

```bash
ollama serve
```

Default endpoint:

```text
http://localhost:11434
```

---

#  Run Backend Server

## Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Server will run at:

```text
http://localhost:8000
```

---

# 🔌 API Quick Test

## Health Check

```http
GET /
```

---

## Run AI Pipeline

```http
POST /scout
```

### Example Request:

```json id="setup_req"
{
  "jd": "Senior DevOps Engineer with Kubernetes, AWS, CI/CD experience",
  "mode": "balanced"
}
```

---

#  Verify System Health

## Metrics Endpoint

```http
GET /metrics
```

Returns:

* API calls
* failure rate
* average latency

---

## Debug Data

```http
GET /candidates
GET /jobs
```

---

#  Debug Logging System

Logs are stored in:

```text
logs/
```

### Key Logs:

* `app.log` → general system logs
* `pipeline.log` → full pipeline execution
* `llm_raw.log` → raw model outputs
* `ranking.log` → scoring details
* `engagement.log` → conversation logs

---

# ⚙️ System Modes

You can control pipeline behavior using:

| Mode        | Description       |
| ----------- | ----------------- |
| very_loose  | broad matching    |
| loose       | relaxed filtering |
| balanced    | default mode      |
| default     | safe fallback     |
| focused     | strict skills     |
| strict      | high precision    |
| very_strict | ultra filtering   |

---


#  Common Issues

## 1. Ollama not responding

```bash
ollama serve
```

---

## 2. Empty LLM response

Check:

* model pulled correctly
* correct model name in `.env`

---

## 3. FastAPI not starting

Ensure:

```bash
pip install -r requirements.txt
```

---

## 4. JSON parsing errors

Check:

* LLM output logs in `llm_raw.log`
* fallback extractor is active

---



#  Status After Setup

If everything is correct:

- Backend running
- LLM router active
- Candidate pipeline working
- Ranking system functional
- Shortlist generation live

---

