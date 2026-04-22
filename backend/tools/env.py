import os
from pathlib import Path

from dotenv import load_dotenv


_ENV_LOADED = False


def ensure_env_loaded() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    repo_root = Path(__file__).resolve().parents[2]
    env_path = repo_root / ".env"
    load_dotenv(dotenv_path=env_path, override=False)
    _ENV_LOADED = True


def get_env(key: str, default: str | None = None) -> str | None:
    ensure_env_loaded()
    return os.getenv(key, default)
