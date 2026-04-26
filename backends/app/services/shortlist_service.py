def build_shortlist(results):
    shortlist = []

    for c in results:
        candidate = c.get("candidate", {})
        scores = c.get("scores", {})

        shortlist.append({
            "rank": c.get("rank"),
            "candidate_id": candidate.get("id"),
            "name": candidate.get("name"),
            "role": candidate.get("role"),
            "experience": candidate.get("experience_years"),

            "final_score": c.get("final_score", 0),

            "match_score": scores.get("match", 0),
            "engagement_score": scores.get("engagement", 0),

            "top_skills": candidate.get("skills", [])[:5],
            "why_selected": c.get("explain", [])
        })

    return shortlist