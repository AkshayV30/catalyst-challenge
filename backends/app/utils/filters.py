from app.utils.text_utils import normalize

def _to_set(items):
    return {normalize(i) for i in (items or []) if i}


def _intersection_size(a, b):
    return len(_to_set(a) & _to_set(b))


def _has_intersection(a, b):
    return _intersection_size(a, b) > 0

# -------------------------------------------------------------------------------
def soft_match(required, available):
    return True if not required else _has_intersection(required, available)


def skill_overlap_score(jd_skills, candidate_skills):
    return _intersection_size(jd_skills, candidate_skills)


def must_have_score(candidate_skills, jd_must_have):
    return _intersection_size(jd_must_have, candidate_skills)


def must_have_match(candidate_skills, jd_must_have):
    if not jd_must_have:
        return True
    return _to_set(jd_must_have).issubset(_to_set(candidate_skills))


def experience_match(candidate_exp, jd_exp):
    if jd_exp is None:
        return True
    try:
        return abs(float(candidate_exp or 0) - float(jd_exp)) <= 2
    except:
        return True


# -------------------------------------------------------------------------------

def prefilter_candidates(candidates, jd, config):
    jd_skills = jd.get("skills") or []
    jd_must = jd.get("must_have") or []

    min_overlap = config["filter"].get("min_skill_overlap", 1)
    must_required = config["filter"].get("must_have_required", False)

    # safety fallback
    if not jd_skills and not jd_must:
        return candidates[:10]

    filtered = []

    for c in candidates:
        skills = (c.get("skills") or []) + (c.get("tools") or [])

        overlap_score = skill_overlap_score(jd_skills, skills)
        must_score = must_have_score(skills, jd_must)

        total_score = overlap_score + (2 * must_score)

        c["_prefilter"] = {
            "overlap_score": overlap_score,
            "must_score": must_score,
            "total_score": total_score
        }

        # hard constraint
        if must_required and jd_must and must_score == 0:
            continue

        if total_score >= min_overlap:
            filtered.append(c)

    return filtered or candidates[:5]



def postfilter_candidates(candidates, max_results=10):
    valid = [c for c in candidates if "final_score" in c]

    if not valid:
        valid = candidates  # fallback to all if no scores

    return sorted(
        valid,
        key=lambda x: x.get("final_score", 0),
        reverse=True
    )[:max_results]