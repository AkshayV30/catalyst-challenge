import asyncio

from app.core.ollama_client import generate
from app.core.loggers import logger
from app.configs.llm_config import LLM_CONFIG


MAX_RETRIES_PER_MODEL = 2
MODEL_TIMEOUT = 28  


async def route(task: str, prompt: str):
    config = LLM_CONFIG.get(task)

    if not config or not config.models:
        raise ValueError(f"[router] No models configured for task: {task}")

    seen = set()

    for model in config.models:

        if model in seen:
            continue
        seen.add(model)

        for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
            try:
                logger.info(f"[{task}] using model={model}, attempt={attempt}")

                return await asyncio.wait_for(
                    generate(model, prompt),
                    timeout=MODEL_TIMEOUT
                )

            except asyncio.TimeoutError:
                logger.warning(
                    f"[{task}] timeout model={model} attempt={attempt}"
                )

            except Exception as e:
                logger.warning(
                    f"[{task}] failure model={model} attempt={attempt} → {e}"
                )

    raise RuntimeError(f"[router] {task}: all models failed")