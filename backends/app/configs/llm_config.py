from dataclasses import dataclass
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class TaskConfig:
    models: List[str]

def parse_env_list(key: str, default: List[str]) -> List[str]:
    value = os.getenv(key)
    if not value:
        return default
    return [v.strip() for v in value.split(",") if v.strip()]

_TASKS = ["jd_parser", "matcher", "engagement"]


def _load_task_config(task: str) -> TaskConfig:
    return TaskConfig(
        models=parse_env_list(
            f"{task.upper()}_MODELS",
            parse_env_list(
                f"DEFAULT_{task.upper()}_MODELS",
                []
            )
        )
    )


LLM_CONFIG: Dict[str, TaskConfig] = {
    task: _load_task_config(task)
    for task in _TASKS
}

