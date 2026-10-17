"""The API's only touch points with the configuration and database layers.

spakr.config and spakr.db belong to the database and settings work. Until
spakr.db exists, database versions are reported as `unknown` instead of failing.
"""

import logging
from typing import Any

from spakr.config import ConfigError, Settings, load_settings

log = logging.getLogger("spakr.api")


def load_config() -> tuple[Settings | None, str | None]:
    """Return (settings, None) or (None, reason). Never raises, never a traceback."""
    try:
        return load_settings(), None
    except ConfigError as error:
        return None, str(error)


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
