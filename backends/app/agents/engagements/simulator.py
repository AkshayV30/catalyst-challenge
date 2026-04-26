import random
from app.utils.filters import skill_overlap_score


def simulate_response(jd, candidate):
    overlap = skill_overlap_score(
        jd.get("skills", []),
        candidate.get("skills", [])
    )

    if overlap >= 4:
        score = 85 + random.randint(0, 10)
        reply = "Yes, this aligns strongly with my experience."
    elif overlap >= 2:
        score = 60 + random.randint(0, 20)
        reply = "I may be open depending on details."
    else:
        score = 30 + random.randint(0, 30)
        reply = "Not a strong fit but open to discuss."

    return {
        "interest_score": score,
        "reply": reply,
        "signals": [
            f"skill_overlap={overlap}",
            f"role={candidate.get('role')}"
        ]
    }