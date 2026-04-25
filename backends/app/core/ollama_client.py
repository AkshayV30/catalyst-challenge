import httpx
import time
from app.core.config import settings
from app.core.loggers import logger
from app.core.metrics import metrics

OLLAMA_URL = f"{settings.OLLAMA_BASE_URL}{settings.OLLAMA_GENERATE}"


async def generate(model: str, prompt: str):
    start = time.time()

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

            res.raise_for_status()
            data = res.json()

            latency = time.time() - start
            metrics.record(latency, success=True)

            logger.info(f"[{model}] success | {latency:.2f}s")

            return data.get("response", "")

        except Exception as e:
            latency = time.time() - start
            metrics.record(latency, success=False)

            logger.error(f"[{model}] failed | {latency:.2f}s | {e}")

            raise  RuntimeError(f"Ollama failed: {e}")


async def generate_stream(model: str, prompt: str):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            }
        ) as res:
            async for line in res.aiter_lines():
                if line:
                    yield line





# import requests
# from app.core.config import settings


# def run_model(model: str, prompt: str) -> str:
#     url = f"{settings.OLLAMA_BASE_URL}{settings.OLLAMA_GENERATE}"

#     for attempt in range(settings.RETRY_COUNT):
#         try:
#             response = requests.post(
#                 url,
#                 json={
#                     "model": model,
#                     "prompt": prompt,
#                     "stream": False,
#                 },
#                 timeout=settings.REQUEST_TIMEOUT,
#             )

#             response.raise_for_status()

#             data = response.json()

#             return data.get("response", "")

#         except requests.exceptions.RequestException as e:
#             if attempt == settings.RETRY_COUNT - 1:
#                 raise RuntimeError(f"Ollama failed: {e}")

# def run_chat_model(model: str, messages: list) -> str:
#     url = f"{settings.OLLAMA_BASE_URL}{settings.OLLAMA_CHAT}"

#     for attempt in range(settings.RETRY_COUNT):
#         try:
#             response = requests.post(
#                 url,
#                 json={
#                     "model": model,
#                     "messages": messages,
#                     "stream":True,
#                 },
#                 timeout=settings.REQUEST_TIMEOUT,
#             )

#             response.raise_for_status()

#             data = response.json()

#             return data.get("response", "")

#         except requests.exceptions.RequestException as e:
#             if attempt == settings.RETRY_COUNT - 1:
#                 raise RuntimeError(f"Ollama chat failed: {e}")

# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

# def run_model(model: str, prompt: str):
#     response = requests.post(OLLAMA_URL, json={
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     })

#     return response.json()["response"] 
