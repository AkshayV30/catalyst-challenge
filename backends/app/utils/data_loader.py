import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_candidates():
    with open(BASE_DIR / "data/candidates.json") as f:
        return json.load(f)

def load_jobs():
    with open(BASE_DIR / "data/job_descriptions.json") as f:
        return json.load(f)