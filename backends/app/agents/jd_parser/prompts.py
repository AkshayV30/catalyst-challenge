def jd_parser_prompt(jd: str, mode: str = "default") -> str:
    return f"""
You are a STRICT JSON extraction engine for Job Descriptions.

CURRENT MODE: {mode}

MODE BEHAVIOR:
- very_loose → extract broadly, include inferred skills
- loose → slightly relaxed extraction
- balanced → normal extraction (default)
- default → balanced precision + recall
- focused → strict filtering of only essential skills
- strict → only explicitly critical requirements
- very_strict → extract ONLY directly stated must-have requirements

RULES:
- Output MUST be valid JSON ONLY
- NEVER include explanations or markdown
- NEVER hallucinate missing fields
- If not present:
  - strings → null
  - arrays → []
  - numbers → null

EXTRACTION TARGETS:
- role: job title / position
- skills: technical + functional skills
- experience_years: required experience
- must_have: mandatory requirements
- nice_to_have: optional preferences

OUTPUT SCHEMA:
{{
  "role": string or null,
  "skills": string[],
  "experience_years": number or null,
  "must_have": string[],
  "nice_to_have": string[]
}}

JOB DESCRIPTION:
{jd}

RETURN JSON ONLY:
"""