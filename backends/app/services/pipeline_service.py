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
from app.utils.score_weights import resolve_weights
from app.utils.mode_resolver import resolve_mode_config

from app.validators.jd_validator import validate_jd

from app.core.loggers import logger


SEMAPHORE = asyncio.Semaphore(5)


async def run_pipeline(jd: str, mode: str = "default"):
    start = time.time()

    mode_config = resolve_mode_config(mode)
    score_weights = resolve_weights(mode_config)
 

    structured_jd = await _parse_jd_safe(jd)

    candidates = load_candidates()


    prefiltered = prefilter_candidates(candidates, structured_jd, mode_config)

    logger.info(
        f"Prefilter ({mode}): {len(prefiltered)}/{len(candidates)}"
    )

    if not prefiltered:
        return _empty_response(structured_jd, start)

    results = await asyncio.gather(
        *[_process_candidate(c, structured_jd) for c in prefiltered]
    )

    ranked = rank(results, score_weights)

    final_results = postfilter_candidates(ranked, max_results=10)

    shortlist = build_shortlist(final_results)

    return {
        "parsed_jd": structured_jd,
        "mode": mode,
        "weights": score_weights,

        "total_candidates": len(prefiltered),
        "shortlist_count": len(shortlist),

        "shortlist": shortlist,
        "results_raw": final_results,

        "latency": round(time.time() - start, 2)
    }




async def _parse_jd_safe(jd: str):
    try:
        raw = await parse_jd(jd)

       
        if isinstance(raw, dict):
            return raw

      
        elif isinstance(raw, str):
            parsed = extract_json(raw)

            if not parsed:
                raise ValueError("Empty JD JSON")

            return validate_jd(jd, parsed) 

        
        raise TypeError(f"Unsupported JD response type: {type(raw)}")

    except Exception as e:
        logger.error(f"JD parsing failed: {e}")
        return {
            "role": None,
            "skills": [],
            "experience_years": None,
            "must_have": [],
            "nice_to_have": []
            }


async def _process_candidate(c, structured_jd):
    async with SEMAPHORE:
        try:
            candidate_text = format_candidate(c)

            match_task = asyncio.create_task(
                match(structured_jd, candidate_text)
            )

            engagement_task = asyncio.create_task(
                engagement(structured_jd, candidate_text)
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
                "match": {"match_score": 0, "reasons": []},
                "engagement": {"interest_score": 0, "signals": [], "reply": ""}
            }


def _empty_response(jd, start):
    return {
        "parsed_jd": jd,
        "total_candidates": 0,
        "shortlist_count": 0,
        "shortlist": [],
        "results_raw": [],
        "latency": round(time.time() - start, 2),
        "message": "No candidates passed prefilter"
    }