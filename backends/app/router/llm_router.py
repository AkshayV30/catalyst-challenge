from app.core.config import MODELS
from app.core.ollama_client import generate
from app.core.loggers import logger


MODEL_PRIORITY = {
    "jd_parser": [MODELS["jd_parser"], "gemma:2b-instruct"],
    "matcher": [MODELS["matcher"], "phi:latest"],
    "engagement": [MODELS["engagement"], "mistral:latest"]
}


async def route(task: str, prompt: str):
    models = MODEL_PRIORITY.get(task, [])

    for model in models:
        try:
            return await generate(model, prompt)
        except Exception:
            logger.warning(f"Fallback triggered → {model}")
            continue

    raise RuntimeError("All models failed")