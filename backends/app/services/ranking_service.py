from app.core.loggers import logger

def rank(candidates_results, score_weights):
    log = logger.bind(stage="ranking")

    w_match = score_weights.get("match", 0.7)
    w_eng = score_weights.get("engagement", 0.3)

    log.info(f"Ranking started | weights: match={w_match}, engagement={w_eng}")

    scored = []

    for c in candidates_results:
        candidate_id = c.get("candidate", {}).get("id")
        name = c.get("candidate", {}).get("name")

        match = c.get("match", {})
        eng = c.get("engagement", {})

        try:
            match_score = float(match.get("match_score") or 0)
            engagement_score = float(eng.get("interest_score") or 0)

        except Exception as e:
            log.error(f"[{candidate_id}] Score parsing failed: {e}")
            match_score = 0
            engagement_score = 0

        # detect broken upstream
        if match_score == 0 and engagement_score == 0:
            log.warning(f"[{candidate_id}] Both scores are 0 → possible LLM/JSON failure")

        
        log.debug(f"""
[CANDIDATE SCORING]
ID: {candidate_id}
Name: {name}

Match Score: {match_score}
Engagement Score: {engagement_score}

Reasons: {match.get("reasons")}
Signals: {eng.get("signals")}
""")

        final_score = (match_score * w_match) + (engagement_score * w_eng)

        c["final_score"] = round(final_score, 2)

        c["scores"] = {
            "match": match_score,
            "engagement": engagement_score,
            "weights": score_weights,
            "final": c["final_score"]
        }

        c["explain"] = match.get("reasons", [])

        log.info(
            f"[{candidate_id}] Final Score={c['final_score']} "
            f"(match={match_score}, engagement={engagement_score})"
        )

        scored.append(c)

    log.info(f"Sorting {len(scored)} candidates")

    ranked = sorted(scored, key=lambda x: x["final_score"], reverse=True)

    # assign rank
    for idx, c in enumerate(ranked, start=1):
        c["rank"] = idx

    # top candidates preview
    log.info("Top 3 candidates preview:")
    for c in ranked[:3]:
        log.info(
            f"Rank #{c['rank']} | "
            f"{c.get('candidate', {}).get('name')} | "
            f"Score={c['final_score']}"
        )

    log.info("Ranking completed")

    return ranked