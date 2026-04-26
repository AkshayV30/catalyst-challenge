import time
import asyncio

from pydantic import ValidationError

from app.agents.jd_parser.llm_adapter import parse_jd
from app.agents.candidates.matcher import match
from app.agents.candidates.discovery import CandidateDiscoveryAgent
from app.agents.engagements import EngagementAgent

from app.services.ranking_service import rank
from app.services.shortlist_service import build_shortlist

from app.utils.data_loader import load_candidates
from app.utils.formatter import format_candidate
from app.utils.filters import prefilter_candidates, postfilter_candidates
from app.utils.score_weights import resolve_weights
from app.utils.mode_resolver import resolve_mode_config
from app.utils.json_utils import extract_json  
from app.validators.jd_validator import validate_jd
from app.schemas.jd import JDOutput

from app.core.loggers import logger
from app.router.llm_router import route


SEMAPHORE = asyncio.Semaphore(5)
engagement_agent = EngagementAgent(llm_router=route)

async def run_pipeline(jd: str, mode: str = "default"):
    start = time.time()

    config = resolve_mode_config(mode)
    score_weights = resolve_weights(config)
 

    structured_jd = await _parse_jd_safe(jd)

    candidates = load_candidates()

    prefiltered = prefilter_candidates(candidates, structured_jd, config)

    logger.info(
        f"Prefilter ({mode}): {len(prefiltered)}/{len(candidates)}"
    )

    if not prefiltered:
        return _empty_response(structured_jd, start)

    discovery = CandidateDiscoveryAgent(prefiltered)
    retrieved = discovery.retrieve(structured_jd)

    results = await asyncio.gather(*[
        _process_candidate(item["candidate"], structured_jd)
        for item in retrieved
    ])
        
    ranked = rank(results, score_weights)

    final_results = postfilter_candidates(ranked)

    shortlist = build_shortlist(final_results)

    return {
        "parsed_jd": structured_jd,
        "mode": mode,
        "weights": score_weights,

        "total_candidates": len(candidates),
        "after_prefilter": len(prefiltered),
        "after_retrieval": len(retrieved),
        "shortlist_count": len(shortlist),

        "shortlist": shortlist,
        "results_raw": final_results,

        "latency": round(time.time() - start, 2)
    }

# ------------------------------------------------------------------


async def _parse_jd_safe(jd: str):
    try:
        raw = await parse_jd(jd)

        parsed = JDOutput.model_validate(raw)

        return validate_jd(jd, parsed.model_dump())

    except ValidationError as e:
        logger.error(f"JD schema validation failed: {e}")

        return JDOutput().model_dump()

    except Exception as e:
        logger.error(f"JD parsing failed: {e}")

        return JDOutput().model_dump()


async def _process_candidate(candidate, structured_jd):
    async with SEMAPHORE:
        try:
            candidate_text = format_candidate(candidate)

            match_raw, engagement_raw = await asyncio.gather(
                match(structured_jd, candidate_text),
                engagement_agent.engage(structured_jd, candidate)
            )


            return {
                "candidate": candidate,
                "match": extract_json(match_raw),
                "engagement":engagement_raw,
                "raw": {
                    "match": match_raw,
                    "engagement": engagement_raw
                }
            }

        except Exception as e:
            logger.error(f"Candidate {candidate.get('id')} failed: {e}")

            return {
                "candidate": candidate,
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