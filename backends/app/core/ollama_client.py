import httpx
import time

from app.configs.core_config import settings
from app.core.loggers import logger
from app.core.metrics import metrics

OLLAMA_URL = f"{settings.OLLAMA_BASE_URL}{settings.OLLAMA_GENERATE}"


async def generate(model: str, prompt: str, stage: str = "llm"):
    log = logger.bind(stage=stage)

    start = time.time()

    log.debug(f"[REQUEST] model={model}")
    log.debug(f"[PROMPT PREVIEW]\n{prompt[:500]}")  # avoid huge logs

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        try:
            res = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            latency = time.time() - start
            metrics.record(latency, success=True)

            log.debug(f"[HTTP STATUS] {res.status_code}")

            res.raise_for_status()
            data = res.json()

            response_text = data.get("response", "")

            log.info(f"[SUCCESS] model={model} latency={latency:.2f}s")

            # RAW LLM output (goes to llm_raw.log)
            log.debug(f"[RAW OUTPUT]\n{response_text[:1000]}")

            return response_text

        except httpx.TimeoutException:
            latency = time.time() - start
            metrics.record(latency, success=False)

            log.warning(f"[TIMEOUT] model={model} latency={latency:.2f}s")
            raise RuntimeError(f"{model} timeout")

        except httpx.HTTPStatusError as e:
            latency = time.time() - start
            metrics.record(latency, success=False)

            log.error(f"[HTTP ERROR] {e.response.status_code} | {e.response.text}")
            raise RuntimeError(f"{model} HTTP error")

        except Exception as e:
            latency = time.time() - start
            metrics.record(latency, success=False)

            log.exception(f"[FAILED] model={model} latency={latency:.2f}s")
            raise RuntimeError(f"Ollama failed: {e}")
