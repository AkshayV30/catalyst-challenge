def jd_parser_prompt(jd: str) -> str:
    return f"""
You MUST return ONLY valid JSON. No explanation. No markdown.

Schema:
{{
  "role": "string",
  "skills": ["string"],
  "experience_years": number,
  "must_have": ["string"],
  "nice_to_have": ["string"]
}}

Rules:
- Output strictly JSON
- No text before or after JSON
- No code blocks

JD:
{jd}
"""


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
- Reply must be short (max 2 lines)
- No markdown
- No explanation
- JSON only

JD:
{jd}

Candidate:
{candidate}
"""