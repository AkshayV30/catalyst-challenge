from app.router.llm_router import route
from app.utils.json_utils import extract_json
from app.prompts.templates import match_prompt


async def match(jd: str, candidate: str):
    prompt = match_prompt(jd, candidate)

    raw = await route("matcher", prompt)

    return extract_json(raw)