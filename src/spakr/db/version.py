"""The integer database schema version.

It counts up by one with every migration. Migration files are named
NNNN_<name>.py with revision id "NNNN"; SCHEMA_VERSION is the number of the
newest one, and a test keeps the two in step. The applied version is stored in
the one-row table schema_version and set by each migration.
"""

from sqlalchemy import Engine, inspect, text

SCHEMA_VERSION = 2
TABLE = "schema_version"


def get_schema_version(engine: Engine) -> int | None:
    """Return the applied schema version, or None if the database has none yet.

    Connection errors propagate so callers (health checks) can report them.
    """
    with engine.connect() as conn:
        if TABLE not in inspect(conn).get_table_names():
            return None
        row = conn.execute(text(f"SELECT version FROM {TABLE} WHERE id = 1")).first()
    return None if row is None else int(row[0])


def schema_status(engine: Engine) -> str:
    """One of: "uninitialised", "needs-upgrade", "ok", "newer-than-code"."""
    applied = get_schema_version(engine)
    if applied is None:
        return "uninitialised"
    if applied < SCHEMA_VERSION:
        return "needs-upgrade"
    if applied > SCHEMA_VERSION:
        return "newer-than-code"
    return "ok"
