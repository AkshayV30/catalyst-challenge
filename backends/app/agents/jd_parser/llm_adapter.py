from app.router.llm_router import route
from app.utils.json_utils import extract_json
from app.agents.jd_parser.prompts import jd_parser_prompt


async def parse_jd(jd: str):
    prompt = jd_parser_prompt(jd)

    raw = await route("jd_parser", prompt)

    return extract_json(raw)