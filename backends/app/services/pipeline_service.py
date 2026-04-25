import time
import asyncio

from app.agents.jd_parser import parse_jd
from app.agents.candidate_matcher import match
from app.agents.engagement_agent import engagement

from app.services.ranking_service import rank

from app.utils.data_loader import load_candidates
from app.utils.formatter import format_candidate
from app.core.loggers import logger



SEMAPHORE = asyncio.Semaphore(5)


async def run_pipeline(jd: str):
    start = time.time()


    structured_jd = await parse_jd(jd)

    if not structured_jd:
        raise ValueError("JD parsing failed")

  
    candidates = load_candidates()

    async def process_candidate(c):
        async with SEMAPHORE: 
            try:
                candidate_text = format_candidate(c)

                match_task = asyncio.create_task(
                    match(structured_jd, candidate_text)
                )

                engagement_task = asyncio.create_task(
                    engagement(candidate_text, structured_jd)
                )

                match_result, engagement_result = await asyncio.gather(
                    match_task,
                    engagement_task
                )

                return {
                    "candidate": c,
                    "match": match_result,
                    "engagement": engagement_result
                }

            except Exception as e:
                logger.error(f"Candidate {c.get('id')} failed: {e}")

                return {
                    "candidate": c,
                    "error": str(e),
                    "match": {},
                    "engagement": {}
                }

  
    results = await asyncio.gather(
        *[process_candidate(c) for c in candidates],
        return_exceptions=False
    )


    ranked = rank(results)

    return {
        "jd": structured_jd,
        "total_candidates": len(candidates),
        "results": ranked,
        "latency": round(time.time() - start, 2)
    }