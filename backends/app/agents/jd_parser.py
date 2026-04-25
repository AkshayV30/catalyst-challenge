from app.core.ollama_client import run_model
from app.core.config import MODELS
import json


def parse_jd(jd: str):
    prompt = f"""
Extract structured JSON:

{{
  "role": "",
  "skills": [],
  "experience_years": "",
  "must_have": [],
  "nice_to_have": []
}}

JD:
{jd}
"""

    return run_model(MODELS["jd_parser"], prompt)
