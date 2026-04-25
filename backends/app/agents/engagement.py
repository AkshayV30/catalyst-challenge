from app.core.ollama_client import run_model
from app.core.config import MODELS

def engagement(candidate, jd):
    prompt = f"""
Simulate recruiter outreach and candidate intent.

Return JSON:
{{
  "interest_score": 0-100,
  "signals": [],
  "reply": ""
}}

JD:
{jd}

Candidate:
{candidate}
"""

    return run_model(MODELS["engagement"], prompt)