import os
import sys
import tomllib
import pathlib
from pathlib import Path

SERVICE_NAME = "filesystem-api"
SYSTEM_CONFIG_PATH = Path(f"/etc/{SERVICE_NAME}/config.toml")
DEFAULT_CONFIG_PATH = Path("config.toml")

_config: dict = {}


def _load_toml(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Warning: failed to read {path}: {exc}", file=sys.stderr)
        return {}


def load_config(explicit_path: str | None = None) -> dict:
    merged: dict = {}

    if SYSTEM_CONFIG_PATH.is_file():
        merged.update(_load_toml(SYSTEM_CONFIG_PATH))

    config_path = Path(explicit_path) if explicit_path else Path(
        os.getenv("FILESYSTEM_API_CONFIG_FILE", DEFAULT_CONFIG_PATH)
    )
    if config_path.is_file():
        merged.update(_load_toml(config_path))

    return merged


def init(explicit_path: str | None = None) -> dict:
    global _config
    if _config:
        return _config
    _config = load_config(explicit_path)
    return _config


def _resolve_file_env(name: str):
    file_path = os.getenv(name)
    if not file_path:
        return None
    try:
        return Path(file_path).read_text(encoding="utf-8").strip()
    except Exception as exc:
        print(f"Warning: failed to read env file {name} at {file_path}: {exc}", file=sys.stderr)
        return None


def get(key: str, default=None):
    return _config.get(key, default)


def env_or_config(*env_names: str, config_key: str | None = None, default=None):
    for env_name in env_names:
        if env_name.endswith("_FILE"):
            value = _resolve_file_env(env_name)
        else:
            value = os.getenv(env_name)
        if value is not None:
            return value
    if config_key:
        config_value = get(config_key)
        if config_value is not None:
            return config_value
    return default


init()

STORAGE_PATH = env_or_config("STORAGE_PATH", config_key="storage_path", default="/storage")
ALLOWED_DIRECTORIES_RAW = env_or_config(
    "ALLOWED_DIRECTORIES",
    config_key="allowed_directories",
    default=STORAGE_PATH,
)
ALLOWED_DIRECTORIES = [
    str(pathlib.Path(os.path.expanduser(path.strip())).resolve())
    for path in ALLOWED_DIRECTORIES_RAW.split(",")
]
FILESYSTEM_API_KEY = env_or_config(
    "FILESYSTEM_API_KEY",
    "FILESYSTEM_API_KEY_FILE",
    "API_KEY",
    "API_KEY_FILE",
    config_key="api_key",
    default=None,
)
ALLOWED_ORIGINS = env_or_config(
    "ALLOWED_ORIGINS",
    config_key="allowed_origins",
    default="http://localhost,http://127.0.0.1",
)
DOMAIN = env_or_config("DOMAIN", "FILESYSTEM_API_DOMAIN", config_key="domain", default="filesystem-api")

# Validate that all allowed directories exist
for directory in ALLOWED_DIRECTORIES:
    path_obj = pathlib.Path(directory)
    if not path_obj.exists():
        raise ValueError(f"ALLOWED_DIRECTORY does not exist: {directory}")
    if not path_obj.is_dir():
        raise ValueError(f"ALLOWED_DIRECTORY is not a directory: {directory}")

# Optional: Log the configured directories (for debugging)
print(f"Filesystem API configured with {len(ALLOWED_DIRECTORIES)} allowed directories:")
for directory in ALLOWED_DIRECTORIES:
    print(f"  - {directory}")
