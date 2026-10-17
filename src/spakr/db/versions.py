"""Database version helpers in the shape the API's health endpoint reads.

DB_VERSION is the schema version this code expects; current_db_version(settings)
connects with the configured credentials and returns the applied version, or
None if the database has not been initialised. Connection errors propagate.
"""

from spakr.db.engine import create_db_engine
from spakr.db.version import SCHEMA_VERSION, get_schema_version

DB_VERSION = SCHEMA_VERSION


def current_db_version(settings) -> int | None:
    engine = create_db_engine(settings)
    try:
        return get_schema_version(engine)
    finally:
        engine.dispose()
