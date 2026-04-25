from app.router.llm_router import route
# import json

async def engagement(candidate, jd):
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

    return await route("engagement", prompt)