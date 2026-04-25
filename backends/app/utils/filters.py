from typing import List, Dict


def normalize(skills: List[str]) -> set:
    return set(s.lower().strip() for s in (skills or []))


def prefilter_candidates(
    candidates: List[Dict],
    jd: Dict,
    mode: str = "default"
) -> List[Dict]:
    """
    Fast deterministic filtering BEFORE LLM
    Mode-aware filtering (strict vs loose hiring)
    """

    MIN_OVERLAP_MAP = {
        "very_loose": 0,
        "loose": 1,
        "balanced": 2,
        "default": 2,
        "focused": 3,
        "strict": 3,
        "very_strict": 4,
    }

    min_skill_overlap = MIN_OVERLAP_MAP.get(mode, 2)

    jd_skills = normalize(jd.get("skills"))
    jd_must_have = normalize(jd.get("must_have"))
    jd_exp = jd.get("experience_years")

    filtered = []

    for c in candidates:
        candidate_skills = normalize(c.get("skills"))
        candidate_exp = c.get("experience_years", 0)

        overlap = jd_skills.intersection(candidate_skills)

     
        if len(overlap) < min_skill_overlap:
            continue

       
        if not experience_match(candidate_exp, jd_exp):
            continue

      
        if mode in ["strict", "very_strict"]:
            if not must_have_match(candidate_skills, jd_must_have):
                continue

        c["_prefilter"] = {
            "skill_overlap": list(overlap),
            "overlap_score": len(overlap),
            "mode": mode
        }

        filtered.append(c)

    return filtered


def postfilter_candidates(
    candidates: List[Dict],
    max_results: int = 10
) -> List[Dict]:
    """
    Final pruning AFTER LLM scoring
    """

    return sorted(
        candidates,
        key=lambda x: (
            x.get("final_score", 0),
            x.get("_prefilter", {}).get("overlap_score", 0)
        ),
        reverse=True
    )[:max_results]


def experience_match(candidate_exp, jd_exp):
    if not jd_exp:
        return True

    try:
        return abs(float(candidate_exp) - float(jd_exp)) <= 2
    except:
        return True


def must_have_match(candidate_skills, jd_must_have):
    if not jd_must_have:
        return True

    return all(skill in candidate_skills for skill in jd_must_have)