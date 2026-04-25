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
   
    try:
        return json.loads(text)
    except:
        pass

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()
   
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        candidate = match.group(0)

        try:
            return json.loads(candidate)
        except Exception as e:
            logger.warning(f"JSON parse failed: {e} | data={candidate[:200]}")

  
    logger.warning(f"No valid JSON found | data={text[:200]}")
    return {}