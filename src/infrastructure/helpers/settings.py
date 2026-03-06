from pathlib import Path
from typing import Any

import yaml

SETTINGS_FILE_PATH = Path("config") / "settings.yml"
DEFAULT_BGWORKER_CONCURRENCY = 1


def get_bgworker_concurrency() -> int:
    settings = _load_settings()
    worker_settings = settings.get("bgworker")
    if not isinstance(worker_settings, dict):
        return DEFAULT_BGWORKER_CONCURRENCY

    raw_concurrency = worker_settings.get("concurrency")
    if isinstance(raw_concurrency, bool):
        return DEFAULT_BGWORKER_CONCURRENCY

    try:
        concurrency = int(raw_concurrency)
    except (TypeError, ValueError):
        return DEFAULT_BGWORKER_CONCURRENCY

    return max(1, concurrency)


def _load_settings() -> dict[str, Any]:
    if not SETTINGS_FILE_PATH.exists():
        return {}

    payload = yaml.safe_load(SETTINGS_FILE_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload
