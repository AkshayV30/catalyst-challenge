from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # App
    APP_NAME = os.getenv("APP_NAME", "AI Backend")

    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_GENERATE = os.getenv("OLLAMA_GENERATE")
    OLLAMA_CHAT = os.getenv("OLLAMA_CHAT")

    # Models
    MODEL_JD_PARSER = os.getenv("MODEL_JD_PARSER")
    MODEL_MATCHER = os.getenv("MODEL_MATCHER")
    MODEL_ENGAGEMENT = os.getenv("MODEL_ENGAGEMENT")

    # Performance
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 2))


settings = Settings()


MODELS = {
    "jd_parser": settings.MODEL_JD_PARSER,
    "matcher": settings.MODEL_MATCHER,
    "engagement": settings.MODEL_ENGAGEMENT,
}

# MODELS = {
#     "jd_parser": "phi:latest",
#     "matcher": "mistral:latest",
#     "engagement": "gemma:2b-instruct"
# }