from app.router.llm_router import route
import json

async  def match(jd, candidate):
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

    return await route("matcher", prompt)