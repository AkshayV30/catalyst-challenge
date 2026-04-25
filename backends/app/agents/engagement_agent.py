from app.router.llm_router import route
from app.utils.json_utils import extract_json
from app.prompts.templates import engagement_prompt


async def engagement(candidate: str, jd: str):
    prompt = engagement_prompt(jd, candidate)

    raw = await route("engagement", prompt)

    return extract_json(raw)