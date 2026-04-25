def rank(candidates_results, score_weights):
    w_match = score_weights.get("match", 0.7)
    w_eng = score_weights.get("engagement", 0.3)

    scored = []

    for c in candidates_results:
        match = c.get("match", {})
        eng = c.get("engagement", {})

        match_score = float(match.get("match_score", 0))
        engagement_score = float(eng.get("interest_score", 0))

        final_score = (match_score * w_match) + (engagement_score * w_eng)

        c["final_score"] = round(final_score, 2)

        c["scores"] = {
            "match": match_score,
            "engagement": engagement_score,
            "weights": score_weights,
            "final": c["final_score"]
        }

        c["explain"] = match.get("reasons", [])

        scored.append(c)

    ranked = sorted(scored, key=lambda x: x["final_score"], reverse=True)

    for idx, c in enumerate(ranked, start=1):
        c["rank"] = idx

    return ranked