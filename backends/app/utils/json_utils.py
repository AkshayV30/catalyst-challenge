import json
import re
from app.core.loggers import logger


def extract_json(text: str) -> dict:
    if not text:
        return {}

    if isinstance(text, dict):
        return text

    if not isinstance(text, str):
        return {}

    # 1. remove markdown fences safely
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "").strip()

    # 2. try direct parse first (fast path)
    try:
        return json.loads(text)
    except:
        pass

    # 3. extract multiple JSON candidates 
    candidates = re.findall(r"\{[\s\S]*?\}", text)

    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue

    logger.warning(f"No valid JSON found | data={text[:300]}")
    return {}