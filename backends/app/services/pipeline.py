import time
from app.agents.jd_parser import parse_jd
from app.agents.matcher import match
from app.agents.engagement import engagement
from app.services.ranking import rank


CANDIDATES = [
    {"id": 1, "text": "Python dev with FastAPI and AWS experience"},
    {"id": 2, "text": "Frontend React developer with UI/UX skills"},
]


def run_pipeline(jd: str):
    start = time.time()

    structured_jd = parse_jd(jd)

    results = []

    for c in CANDIDATES:
        try:
            match_result = match(structured_jd, c["text"])
            engagement_result = engagement(c["text"], structured_jd)

            results.append({
                "candidate": c,
                "match": match_result,
                "engagement": engagement_result
            })

        except Exception as e:
            results.append({
                "candidate": c,
                "error": str(e)
            })

    ranked = rank(results)

    return {
        "jd": structured_jd,
        "results": ranked,
        "latency": round(time.time() - start, 2)
    }