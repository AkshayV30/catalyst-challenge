from app.router.llm_router import route
from app.utils.json_utils import extract_json
from app.agents.jd_parser.prompts import jd_parser_prompt
from app.core.loggers import logger

async def parse_jd(jd: str):
    log = logger.bind(stage="jd_parser")

    prompt = jd_parser_prompt(jd)

    log.info("Starting JD parsing")

    raw = await route("jd_parser", prompt)
    parsed = extract_json(raw)

   
    log.debug(f"""
[JD PARSER RAW OUTPUT]
{raw}
""")

    if parsed:
        log.info(f"""
[JD PARSER SUCCESS]
Role: {parsed.get("role")}
Skills: {len(parsed.get("skills", []))} extracted
Experience: {parsed.get("experience_years")}
Must Have: {len(parsed.get("must_have", []))}
Nice To Have: {len(parsed.get("nice_to_have", []))}
""")
    else:
        log.error(f"""
[JD PARSER FAILED]
Reason: Could not extract valid JSON

Raw Output:
{raw}
""")

    return parsed or {
        "role": None,
        "skills": [],
        "experience_years": None,
        "must_have": [],
        "nice_to_have": []
    }