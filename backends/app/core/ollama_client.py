import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

def run_model(model: str, prompt: str):
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"] 