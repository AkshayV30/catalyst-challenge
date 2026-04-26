def match_prompt(jd: str, candidate: str) -> str:
    return f"""
You are a technical recruiter.

Return ONLY valid JSON.

Schema:
{{
  "match_score": number (0-100),
  "reasons": ["string"]
}}

Rules:
- No explanation
- No markdown
- No code blocks
- Output JSON only

JD:
{jd}

Candidate:
{candidate}
"""


