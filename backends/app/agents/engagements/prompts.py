def engagement_prompt(jd: str, candidate: str) -> str:
    return f"""
Simulate recruiter intent scoring.

Return ONLY valid JSON.

Schema:
{{
  "interest_score": number (0-100),
  "signals": ["string"],
  "reply": "string"
}}

Rules:
- Reply must be short (max 3 lines)
- No markdown
- No explanation
- JSON only

JD:
{jd}

Candidate:
{candidate}
"""