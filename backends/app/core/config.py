# import os


# class Settings:
#     OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
#     OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
#     USE_CLOUD = os.getenv("USE_CLOUD", "false")


# settings = Settings()

MODELS = {
    "jd_parser": "phi:latest",
    "matcher": "mistral:latest",
    "engagement": "gemma:2b-instruct"
}