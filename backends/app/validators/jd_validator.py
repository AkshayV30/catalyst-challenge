from typing import Dict, Callable

def validate_skills(original, parsed):
    text = original.lower()

    parsed["skills"] = [
        s for s in parsed.get("skills", [])
        if s.lower() in text
    ]
    return parsed


def validate_must_have(original, parsed):
    text = original.lower()

    parsed["must_have"] = [
        s for s in parsed.get("must_have", [])
        if s.lower() in text
    ]
    return parsed


def validate_nice_to_have(original, parsed):
    text = original.lower()

    parsed["nice_to_have"] = [
        s for s in parsed.get("nice_to_have", [])
        if s.lower() in text
    ]
    return parsed


def validate_role(original, parsed):
    text = original.lower()
    role = parsed.get("role")

    if role and role.lower() not in text:
        parsed["role"] = None

    return parsed



VALIDATION_PIPELINE: Dict[str, Callable] = {
    "skills": validate_skills,
    "must_have": validate_must_have,
    "nice_to_have": validate_nice_to_have,
    "role": validate_role,
}



def validate_jd(original_jd: str, parsed: Dict) -> Dict:
    """
    Runs structured JD validation pipeline (anti-hallucination layer)
    """

    for validator in VALIDATION_PIPELINE.values():
        parsed = validator(original_jd, parsed)

    return parsed