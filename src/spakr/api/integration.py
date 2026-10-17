"""The API's only touch points with the configuration and database layers.

spakr.config and spakr.db belong to the database and settings work. Until
they exist this module falls back to a minimal JSON loader and "unknown"
database versions, so the API runs and reports `unknown` instead of failing.
"""

import json
import logging
from typing import Any

from spakr import paths

log = logging.getLogger("spakr.api")


def load_config() -> tuple[Any | None, str | None]:
    """Return (config, None) or (None, reason). Never raises, never a traceback."""
    try:
        from spakr import config as config_module
    except ImportError:
        return _fallback_load()
    try:
        return config_module.load_config(), None
    except config_module.ConfigError as error:
        return None, str(error)


def _fallback_load() -> tuple[Any | None, str | None]:
    path = paths.config_path()
    if not path.is_file():
        return None, (
            f"Configuration file {path} not found. Copy examples/config.json.example "
            "there and edit it."
        )
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        return None, f"Configuration file {path} cannot be read: {error}"
    if not isinstance(data, dict):
        return None, f"Configuration file {path} must contain a JSON object."
    return data, None


def database_versions(config: Any) -> tuple[int | None, int | None]:
    """Return (expected, current) database schema version; None when unknown."""
    try:
        from spakr.db import versions
    except ImportError:
        return None, None
    expected = getattr(versions, "DB_VERSION", None)
    try:
        current = versions.current_db_version(config)
    except Exception:  # database down or not initialised: report, do not crash
        log.warning("could not read the database schema version", exc_info=True)
        current = None
    return expected, current


def setting(config: Any, *keys: str, default: Any = None) -> Any:
    """Read config.a.b or config["a"]["b"], whichever the config object supports."""
    node = config
    for key in keys:
        if isinstance(node, dict):
            node = node.get(key)
        else:
            node = getattr(node, key, None)
        if node is None:
            return default
    return node
