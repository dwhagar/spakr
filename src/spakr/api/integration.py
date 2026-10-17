"""The API's only touch points with the configuration and database layers.

spakr.config and spakr.db belong to the database and settings work.
"""

import logging
from typing import Any

from spakr.config import ConfigError, Settings, load_settings
from spakr.db import SCHEMA_VERSION, create_db_engine, get_schema_version

log = logging.getLogger("spakr.api")
_ENGINES: dict[int, Any] = {}  # one database engine per loaded configuration


def load_config() -> tuple[Settings | None, str | None]:
    """Return (settings, None) or (None, reason). Never raises, never a traceback."""
    try:
        return load_settings(), None
    except ConfigError as error:
        return None, str(error)


def database_versions(config: Any) -> tuple[int | None, int | None, str]:
    """Return (expected, current, state) for the database schema version.

    state is one of ok, needs-upgrade, newer-than-code, uninitialised (as
    spakr.db.schema_status) or unavailable when the database cannot be reached.
    """
    expected = SCHEMA_VERSION
    try:
        engine = _ENGINES.get(id(config))
        if engine is None:
            engine = _ENGINES[id(config)] = create_db_engine(config)
        current = get_schema_version(engine)
    except Exception:  # database down: report it, do not crash the health check
        log.warning("could not read the database schema version", exc_info=True)
        return expected, None, "unavailable"
    return expected, current, schema_state(expected, current)


def schema_state(expected: int, current: int | None) -> str:
    if current is None:
        return "uninitialised"
    if current < expected:
        return "needs-upgrade"
    return "newer-than-code" if current > expected else "ok"


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
