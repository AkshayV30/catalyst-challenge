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
    log = logger.bind(stage="pipeline")
    start = time.time()

    log.info(f"Pipeline started | mode={mode}")

    config = resolve_mode_config(mode)
    score_weights = resolve_weights(config)

    structured_jd = await _parse_jd_safe(jd)

    log.debug(f"JD Parsed: {structured_jd}")

    candidates = load_candidates()
    log.info(f"Loaded candidates: {len(candidates)}")

    prefiltered = prefilter_candidates(candidates, structured_jd, config)

    log.info(f"Prefilter: {len(prefiltered)}/{len(candidates)}")

    if not prefiltered:
        log.warning("No candidates after prefilter")
        return _empty_response(structured_jd, start)

    discovery = CandidateDiscoveryAgent(prefiltered)
    retrieved = discovery.retrieve(structured_jd)

    log.info(f"Retrieved candidates: {len(retrieved)}")

    results = await asyncio.gather(*[
        _process_candidate(item["candidate"], structured_jd)
        for item in retrieved
    ])

    log.info("All candidates processed")

    ranked = rank(results, score_weights)
    final_results = postfilter_candidates(ranked)
    shortlist = build_shortlist(final_results)

    latency = round(time.time() - start, 2)

    log.info(f"Pipeline completed | latency={latency}s | shortlist={len(shortlist)}")

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
        "latency": latency
    }

# ------------------------------------------------------------------

async def _parse_jd_safe(jd: str):
    log = logger.bind(stage="jd_parser")

    try:
        raw = await parse_jd(jd)

        log.debug(f"Raw JD output:\n{raw}")

        parsed = JDOutput.model_validate(raw)

        validated = validate_jd(jd, parsed.model_dump())

        log.info(f"JD parsed successfully | role={validated.get('role')}")

        return validated

    except ValidationError as e:
        log.error(f"Schema validation failed: {e}")
        return JDOutput().model_dump()

    except Exception as e:
        log.error(f"JD parsing failed: {e}")
        return JDOutput().model_dump()


async def _process_candidate(candidate, structured_jd):
    log = logger.bind(stage="candidate", candidate_id=candidate.get("id"))

    async with SEMAPHORE:
        try:
            start = time.time()

            candidate_text = format_candidate(candidate)

            match_raw, engagement_raw = await asyncio.gather(
                match(structured_jd, candidate_text),
                engagement_agent.engage(structured_jd, candidate)
            )

            match_data = extract_json(match_raw)

            #  VALIDATION OF LLM OUTPUTS 
            if not isinstance(match_data, dict):
                log.error(f"Match JSON invalid | raw={match_raw}")
                match_data = {"match_score": 0, "reasons": []}

            if not isinstance(engagement_raw, dict):
                log.error(f"Engagement invalid | raw={engagement_raw}")
                engagement_raw = {
                    "interest_score": 0,
                    "signals": [],
                    "reply": ""
                }

            latency = time.time() - start

            log.info(
                f"Processed | match={match_data.get('match_score')} "
                f"| interest={engagement_raw.get('interest_score')} "
                f"| latency={latency:.2f}s"
            )

            # DEBUG log for raw outputs 
            log.debug(f"""
MATCH RAW:
{match_raw}

ENGAGEMENT RAW:
{engagement_raw}
""")

            return {
                "candidate": candidate,
                "match": match_data,
                "engagement": engagement_raw,
                "raw": {
                    "match": match_raw,
                    "engagement": engagement_raw
                }
            }

        except Exception as e:
            log.error(f"Candidate failed: {e}")

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