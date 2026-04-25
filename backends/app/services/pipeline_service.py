import time
import asyncio
from app.agents.jd_parser import parse_jd
from app.agents.candidate_matcher import match
from app.agents.engagement_agent import engagement
from app.services.ranking_service import rank


CANDIDATES = [
    {"id": 1, "text": "Python dev with FastAPI and AWS experience"},
    {"id": 2, "text": "Frontend React developer with UI/UX skills"},
]


async def run_pipeline(jd: str):
    start = time.time()

    structured_jd = await parse_jd(jd)

    results = []

    async def process_candidate(c):
        try:
            match_result = await match(structured_jd, c["text"])
            engagement_result = await engagement(c["text"], structured_jd)

            return {
                "candidate": c,
                "match": match_result,
                "engagement": engagement_result
            }

        except Exception as e:
            return {
                "candidate": c,
                "error": str(e),
                "match": "{}",
                "engagement": "{}"
            }

    results = await asyncio.gather(
        *[process_candidate(c) for c in CANDIDATES]
    )

    ranked = rank(results)

    return {
        "jd": structured_jd,
        "results": ranked,
        "latency": round(time.time() - start, 2)
    }