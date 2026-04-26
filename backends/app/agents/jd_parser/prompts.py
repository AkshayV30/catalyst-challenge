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