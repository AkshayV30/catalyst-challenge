from app.utils.filters import skill_overlap_score

class CandidateDiscoveryAgent:
    def __init__(self, candidates):
        self.candidates = candidates

    def retrieve(self, jd, top_k=10):
        jd_skills = jd.get("skills", [])

        scored = []

        for c in self.candidates:
             candidate_skills = c.get("skills", []) + c.get("tools", [])

             score = skill_overlap_score(jd_skills, candidate_skills)

             level_boost = {
                "beginner": 0,
                "intermediate": 0.5,
                "advanced": 1
            }.get(c.get("level", "beginner"), 0)

             score += level_boost

             scored.append({
                "candidate": c,
                "retrieval_score": score
            })

        return sorted(
            scored,
            key=lambda x: x["retrieval_score"],
            reverse=True
        )[:top_k]