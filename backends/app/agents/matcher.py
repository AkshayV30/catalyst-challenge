from app.core.ollama_client import run_model
from app.core.config import MODELS

def match(jd, candidate):
    prompt = f"""
You are a technical recruiter.

Compare JD and candidate.

Return JSON:
{{
  "match_score": 0-100,
  "reasons": []
}}

JD:
{jd}

Candidate:
{candidate}
"""

    return run_model(MODELS["matcher"], prompt)