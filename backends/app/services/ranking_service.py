def rank(candidates_results):
    for c in candidates_results:
        match = c.get("match", {})
        eng = c.get("engagement", {})

        match_score = match.get("match_score", 0)
        interest_score = eng.get("interest_score", 0)

        c["final_score"] = (match_score * 0.7) + (interest_score * 0.3)
        c["explain"] = match.get("reasons", [])

    return sorted(candidates_results, key=lambda x: x["final_score"], reverse=True)