from app.configs.mode_config import MODE_CONFIG

DEFAULT_MODE = "default"

def resolve_mode_config(mode: str | None) -> dict:
    return MODE_CONFIG.get(mode , MODE_CONFIG[DEFAULT_MODE])