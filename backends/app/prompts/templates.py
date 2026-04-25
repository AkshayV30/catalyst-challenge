def jd_parser_prompt(jd: str) -> str:
    return f"""
You are a strict information extraction system.

RULES:
- Extract ONLY what is explicitly present in the text
- Do NOT infer or assume anything
- If a field is missing, return empty list or null
- Do NOT add explanations
- Output MUST be valid JSON only

SCHEMA:
{{
  "role": string | null,
  "skills": string[],
  "experience_years": number | null,
  "must_have": string[],
  "nice_to_have": string[]
}}

JOB DESCRIPTION:
{jd}

Return ONLY JSON:
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