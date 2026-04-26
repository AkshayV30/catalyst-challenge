import json
import re
from app.core.loggers import logger


def extract_json(text: str) -> dict:
    log = logger.bind(stage="json_parser")

    if not text:
        log.warning("Empty input")
        return {}

    if isinstance(text, dict):
        return text

    if not isinstance(text, str):
        log.error(f"Invalid type: {type(text)}")
        return {}

    cleaned = _clean_text(text)

    # ---- FAST PATH ----
    parsed = _try_parse(cleaned)
    if parsed:
        return parsed

    # ---- STRUCTURED EXTRACTION ----
    for candidate in _extract_candidates(cleaned):
        parsed = _try_parse(candidate)
        if parsed:
            return parsed

    log.warning(f"No valid JSON found | preview={cleaned[:200]}")
    return {}


# ---------------- HELPERS ----------------

def _clean_text(text: str) -> str:
    """
    Removes markdown fences and trims text
    """
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")
    return text.strip()


def _try_parse(text: str) -> dict:
    """
    Attempts JSON parsing with minor fixes
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fix common LLM issue: trailing commas
        text = re.sub(r",\s*}", "}", text)
        text = re.sub(r",\s*]", "]", text)

        try:
            return json.loads(text)
        except Exception:
            return None


def _extract_candidates(text: str):
    """
    Extracts balanced JSON objects from text
    """
    stack = []
    start = None

    for i, ch in enumerate(text):
        if ch == "{":
            if not stack:
                start = i
            stack.append(ch)

        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    yield text[start:i + 1]