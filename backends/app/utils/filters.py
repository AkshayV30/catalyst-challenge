from typing import List, Dict


def normalize(skills: List[str]) -> set:
    return set(s.lower().strip() for s in (skills or []))


def prefilter_candidates(
    candidates: List[Dict],
    jd: Dict,
    mode_config: dict
) -> List[Dict]:
   

    filter_cfg = mode_config["filter"]
    min_skill_overlap = filter_cfg["min_skill_overlap"]
    must_have_required = filter_cfg["must_have_required"]

    jd_skills = normalize(jd.get("skills"))
    jd_must_have = normalize(jd.get("must_have"))
    jd_exp = jd.get("experience_years")

    filtered = []

    for c in candidates:
        candidate_skills = normalize(c.get("skills"))
        candidate_exp = c.get("experience_years", 0)

     
        if jd_skills:
            overlap = jd_skills.intersection(candidate_skills)

            if len(overlap) < min_skill_overlap:
                continue
        else:
            overlap = set()

     
        if not experience_match(candidate_exp, jd_exp):
            continue

  
        if must_have_required:
            if not must_have_match(candidate_skills, jd_must_have):
                continue


        candidate_copy = c.copy()

        candidate_copy["_prefilter"] = {
            "skill_overlap": list(overlap),
            "overlap_score": len(overlap),
            "mode": mode_config
        }

        filtered.append(candidate_copy)

    return filtered


def postfilter_candidates(
    candidates: List[Dict],
    max_results: int = 10
) -> List[Dict]:
  
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

    return jd_must_have.issubset(candidate_skills)