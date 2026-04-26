from app.utils.filters import skill_overlap_score
from app.core.loggers import logger


class CandidateDiscoveryAgent:
    def __init__(self, candidates):
        self.candidates = candidates

    def retrieve(self, jd, top_k=10):
        log = logger.bind(stage="candidate")

        jd_skills = jd.get("skills", [])
        log.info(f"Retrieval started | JD skills={jd_skills} | total={len(self.candidates)}")

        scored = []

        for c in self.candidates:
            c_log = log.bind(
                candidate_id=c.get("id"),
                name=c.get("name")
            )

            try:
                candidate_skills = c.get("skills", []) + c.get("tools", [])

                overlap_score = skill_overlap_score(jd_skills, candidate_skills)

                level = c.get("level", "beginner")
                level_boost = {
                    "beginner": 0,
                    "intermediate": 0.5,
                    "advanced": 1
                }.get(level, 0)

                final_score = overlap_score + level_boost

                c_log.debug(
                    f"""
SKILL MATCH:
JD: {jd_skills}
Candidate: {candidate_skills}

Scores:
overlap={overlap_score}
level={level} (+{level_boost})
final={final_score}
"""
                )

                scored.append({
                    "candidate": c,
                    "retrieval_score": final_score
                })

            except Exception as e:
                c_log.error(f"Retrieval failed: {e}")

        ranked = sorted(
            scored,
            key=lambda x: x["retrieval_score"],
            reverse=True
        )[:top_k]

        log.info(f"Retrieval completed | returned={len(ranked)}")

        # Log top results for visibility
        for i, item in enumerate(ranked[:5], start=1):
            c = item["candidate"]
            log.info(
                f"Top {i} | {c.get('name')} | score={item['retrieval_score']}"
            )

        return ranked