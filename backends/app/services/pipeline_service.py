# app/services/pipeline_service.py

import time
import asyncio

from app.agents.jd_parser import parse_jd
from app.agents.candidate_matcher import match
from app.agents.engagement_agent import engagement

from app.services.ranking_service import rank
from app.services.shortlist_service import build_shortlist

from app.utils.data_loader import load_candidates
from app.utils.formatter import format_candidate
from app.utils.json_utils import extract_json
from app.utils.filters import prefilter_candidates, postfilter_candidates

from app.core.loggers import logger


SEMAPHORE = asyncio.Semaphore(5)


async def run_pipeline(jd: str, score_weights: dict):
    start = time.time()

  
    structured_jd = await _parse_jd_safe(jd)


    candidates = load_candidates()
    prefiltered = prefilter_candidates(candidates, structured_jd)

    logger.info(f"Prefilter: {len(prefiltered)}/{len(candidates)}")

    if not prefiltered:
        return _empty_response(structured_jd, start)


    results = await asyncio.gather(
        *[_process_candidate(c, structured_jd) for c in prefiltered]
    )


    ranked = rank(results, score_weights)


    final_results = postfilter_candidates(ranked, max_results=10)

   
    shortlist = build_shortlist(final_results)

 
    return {
        "jd": structured_jd,
        "total_candidates": len(prefiltered),
        "shortlist_count": len(shortlist),
        "shortlist": shortlist,
        "results_raw": final_results,
        "latency": round(time.time() - start, 2)
    }




async def _parse_jd_safe(jd: str):
    try:
        raw = await parse_jd(jd)
        parsed = extract_json(raw)

        if not parsed:
            raise ValueError("Empty JD JSON")

        return parsed

    except Exception as e:
        logger.error(f"JD parsing failed: {e}")
        raise ValueError("JD parsing failed")


async def _process_candidate(c, structured_jd):
    async with SEMAPHORE:
        try:
            candidate_text = format_candidate(c)

            match_task = asyncio.create_task(
                match(structured_jd, candidate_text)
            )

            engagement_task = asyncio.create_task(
                engagement(candidate_text, structured_jd)
            )

            match_raw, engagement_raw = await asyncio.gather(
                match_task, engagement_task
            )

            return {
                "candidate": c,
                "match": extract_json(match_raw),
                "engagement": extract_json(engagement_raw),
                "raw": {
                    "match": match_raw,
                    "engagement": engagement_raw
                }
            }

        except Exception as e:
            logger.error(f"Candidate {c.get('id')} failed: {e}")

            return {
                "candidate": c,
                "error": str(e),
                "match": {},
                "engagement": {}
            }


def _empty_response(jd, start):
    return {
        "jd": jd,
        "total_candidates": 0,
        "shortlist_count": 0,
        "shortlist": [],
        "results_raw": [],
        "latency": round(time.time() - start, 2),
        "message": "No candidates passed prefilter"
    }