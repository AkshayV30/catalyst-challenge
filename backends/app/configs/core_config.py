from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "AI Backend")

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_GENERATE = os.getenv("OLLAMA_GENERATE")

    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 2))


settings = Settings()