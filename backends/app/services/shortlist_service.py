def build_shortlist(results):
    shortlist = []

    for c in results:
        candidate = c.get("candidate", {})

        shortlist.append({
            "rank": c.get("rank"),
            "candidate_id": candidate.get("id"),
            "name": candidate.get("name"),
            "role": candidate.get("role"),
            "experience": candidate.get("experience_years"),

            "final_score": c.get("final_score"),

            "match_score": c.get("scores", {}).get("match"),
            "engagement_score": c.get("scores", {}).get("engagement"),

            "top_skills": candidate.get("skills", [])[:5],

            "why_selected": c.get("explain", []),

            "prefilter_overlap": candidate.get("_prefilter", {}).get("skill_overlap", [])
        })

    return shortlist