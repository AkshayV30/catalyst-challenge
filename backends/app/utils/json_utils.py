import json
import re
from typing import Any, Dict
from app.core.loggers import logger


def extract_json(text: str) -> dict:
    """
    Extracts first valid JSON object from LLM response.
    Handles:
    - Markdown ```json blocks
    - Raw text before/after JSON
    - Partial garbage output
    """

    if not text:
        return {}

    try:
        # direct parse
        return json.loads(text)
    except:
        pass

    # remove markdown fences
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # find JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except Exception as e:
            logger.warning(f"JSON parse failed: {e} | data={text[:200]}")

    return {}