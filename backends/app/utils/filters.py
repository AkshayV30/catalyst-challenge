from typing import List, Dict


def normalize(text: str) -> str:
    return text.lower().replace(" ", "")

def soft_match(required, available):
    return any(
        normalize(r) in normalize(a) or normalize(a) in normalize(r)
        for r in required
        for a in available
    )

def prefilter_candidates(candidates, jd, mode_config):
    filtered = []

    jd_skills = jd.get("skills", [])
    must_have = jd.get("must_have", [])

    threshold = mode_config.filter.get("min_score", 1) if hasattr(mode_config, "filter") else 1

    for c in candidates:

       
        candidate_skills = c.get("skills", [])
        candidate_tools = c.get("tools", [])
        all_skills = candidate_skills + candidate_tools

        
        overlap = [
            s for s in all_skills
            if any(
                normalize(s) in normalize(j) or normalize(j) in normalize(s)
                for j in jd_skills
            )
        ]

        overlap_score = len(overlap)

       
        must_have_hits = 1 if soft_match(must_have, all_skills) else 0

       
        score = overlap_score + (must_have_hits * 2)

       
        c["_prefilter"] = {
            "overlap": overlap,
            "score": score,
            "must_have_hits": must_have_hits
        }

       
        if score >= threshold:
            filtered.append(c)

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