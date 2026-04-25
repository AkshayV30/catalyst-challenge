from app.core.ollama_client import generate
from app.core.loggers import logger
from app.configs.llm_config import LLM_CONFIG


async def route(task: str, prompt: str):
    config = LLM_CONFIG.get(task)

    if not config:
        raise ValueError(f"Unknown task: {task}")

    seen = set()

    for model in config.models:
        if  model in seen:
            continue
        seen.add(model)

        try:
            return await generate(model, prompt)

        except Exception as e:
            logger.warning(f"[{task}] model failed: {model} → {e}")
            continue

    raise RuntimeError(f"{task}: all models failed")