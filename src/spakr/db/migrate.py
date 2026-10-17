"""Run schema migrations and keep the integer schema version in step.

Every migration revision id is its number ("0001", "0002", ...). After each one
runs, schema_version.version is set to that number, so the integer counts up
with every change to the database.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, text

from spakr.db.version import SCHEMA_VERSION, TABLE, get_schema_version

MIGRATIONS_DIR = Path(__file__).with_name("migrations")


def _config(connection) -> Config:
    cfg = Config()
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.attributes["connection"] = connection
    return cfg


def head_version() -> int:
    """The newest migration number found on disk."""
    head = ScriptDirectory(str(MIGRATIONS_DIR)).get_current_head()
    return int(head)


def upgrade(engine: Engine, target: str = "head") -> int:
    """Apply pending migrations and return the resulting schema version.

    MySQL DDL is not transactional: take a backup first on a real install.
    """
    with engine.connect() as conn:
        cfg = _config(conn)
        script = ScriptDirectory(str(MIGRATIONS_DIR))
        revisions = [r for r in reversed(list(script.walk_revisions()))]
        current = get_schema_version(engine) or 0
        for rev in revisions:
            number = int(rev.revision)
            if number <= current:
                continue
            command.upgrade(cfg, rev.revision)
            conn.execute(text(f"UPDATE {TABLE} SET version = :v, updated_at = CURRENT_TIMESTAMP WHERE id = 1"),
                         {"v": number})
            conn.commit()
            if target != "head" and rev.revision == target:
                break
    return get_schema_version(engine) or 0


def check_in_step() -> bool:
    return head_version() == SCHEMA_VERSION
