from dataclasses import dataclass
from typing import Dict, List
import os
from dotenv import load_dotenv
from app.core.loggers import logger  # your loguru logger

load_dotenv()


@dataclass(frozen=True)
class TaskConfig:
    models: List[str]


class ConfigError(ValueError):
    pass


def parse_env_list(key: str, default: List[str]) -> List[str]:
    value = os.getenv(key)
    return [v.strip() for v in value.split(",") if v.strip()] if value else default


TASKS = ["jd_parser", "matcher", "engagement"]


def load_config(task: str) -> TaskConfig:
    models = (
        parse_env_list(f"{task.upper()}_MODELS", [])
        or parse_env_list(f"DEFAULT_{task.upper()}_MODELS", [])
    )

    if not models:
        msg = f"[CONFIG_ERROR] No models configured for task='{task}'"

        #  structured logging (this is the important part)
        logger.error(msg)
        logger.error(
            f"Expected env: {task.upper()}_MODELS or DEFAULT_{task.upper()}_MODELS"
        )

        raise ConfigError(msg)

    logger.info(f"[CONFIG] {task} loaded with models={models}")

    return TaskConfig(models=models)


try:
    LLM_CONFIG: Dict[str, TaskConfig] = {
        task: load_config(task)
        for task in TASKS
    }

    logger.info("[CONFIG] LLM configuration loaded successfully")

except ConfigError as e:
    logger.critical(f"[CONFIG_BOOT_FAIL] {e}")
    raise