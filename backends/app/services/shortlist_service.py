from app.core.loggers import logger


def build_shortlist(results):
    log = logger.bind(stage="shortlist")

    log.info(f"Building shortlist from {len(results)} candidates")

    shortlist = []

    for c in results:
        candidate = c.get("candidate", {})
        scores = c.get("scores", {})

        candidate_id = candidate.get("id")
        name = candidate.get("name")

        match_score = scores.get("match", 0)
        engagement_score = scores.get("engagement", 0)
        final_score = c.get("final_score", 0)

        #  detect weak / broken entries
        if final_score == 0:
            log.warning(f"[{candidate_id}] Final score is 0")

        if not c.get("explain"):
            log.warning(f"[{candidate_id}] Missing explainability (why_selected empty)")

        if not candidate.get("skills"):
            log.warning(f"[{candidate_id}] Missing skills data")

        # DEBUG: full candidate snapshot 
        log.debug(f"""
[SHORTLIST ENTRY]
ID: {candidate_id}
Name: {name}

Scores:
  Match: {match_score}
  Engagement: {engagement_score}
  Final: {final_score}

Top Skills: {candidate.get("skills", [])[:5]}
Why Selected: {c.get("explain", [])}
""")

        shortlist.append({
            "rank": c.get("rank"),
            "candidate_id": candidate_id,
            "name": name,
            "role": candidate.get("role"),
            "experience": candidate.get("experience_years"),

            "final_score": final_score,

            "match_score": match_score,
            "engagement_score": engagement_score,

            "top_skills": candidate.get("skills", [])[:5],
            "why_selected": c.get("explain", [])
        })

    # summary logs 
    log.info(f"Shortlist built: {len(shortlist)} candidates")

    # preview top 3
    log.info("Top shortlist preview:")
    for c in shortlist[:3]:
        log.info(
            f"Rank #{c['rank']} | {c['name']} | "
            f"Final={c['final_score']} | "
            f"M={c['match_score']} | E={c['engagement_score']}"
        )

    return shortlist