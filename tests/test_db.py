"""Database layer tests.

Always run on SQLite (fast, no services). When SPAKR_TEST_DATABASE_URL points at a
throwaway MySQL 8 schema (for example mysql+pymysql://spakr:pw@127.0.0.1/spakr_test),
the same tests run on MySQL too; every table in that schema is dropped first.
"""

import os
import re
from pathlib import Path

import pytest
from sqlalchemy import MetaData, create_engine, event, inspect, text
from sqlalchemy.exc import IntegrityError

from spakr.config import load_settings
from spakr.db import SCHEMA_VERSION, create_db_engine, database_url, get_schema_version, schema_status
from spakr.db.migrate import MIGRATIONS_DIR, head_version, upgrade

MYSQL_URL = os.environ.get("SPAKR_TEST_DATABASE_URL")


def _fresh_engine(kind, tmp_path):
    if kind == "sqlite":
        engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")

        @event.listens_for(engine, "connect")
        def _fk(dbapi_conn, _):
            dbapi_conn.execute("PRAGMA foreign_keys=ON")

        return engine
    engine = create_engine(MYSQL_URL)
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        meta = MetaData()
        meta.reflect(conn)
        meta.drop_all(conn)
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    return engine


@pytest.fixture(params=["sqlite", pytest.param("mysql", marks=pytest.mark.skipif(
    not MYSQL_URL, reason="SPAKR_TEST_DATABASE_URL not set"))])
def engine(request, tmp_path):
    engine = _fresh_engine(request.param, tmp_path)
    yield engine
    engine.dispose()


def test_version_constant_matches_migrations():
    files = sorted(p.name for p in (MIGRATIONS_DIR / "versions").glob("[0-9]*.py"))
    numbers = [int(re.match(r"(\d+)_", f).group(1)) for f in files]
    assert numbers == list(range(1, len(numbers) + 1)), "migration numbers must count up with no gaps"
    assert head_version() == SCHEMA_VERSION == len(numbers)


def test_uninitialised_database(engine):
    assert get_schema_version(engine) is None
    assert schema_status(engine) == "uninitialised"


def test_upgrade_sets_integer_version(engine):
    assert upgrade(engine) == SCHEMA_VERSION
    assert get_schema_version(engine) == SCHEMA_VERSION
    assert schema_status(engine) == "ok"


def test_upgrade_is_repeatable(engine):
    upgrade(engine)
    assert upgrade(engine) == SCHEMA_VERSION


def test_version_counts_up_per_migration(engine):
    assert upgrade(engine, target="0001") == 1
    assert schema_status(engine) == "needs-upgrade"
    assert upgrade(engine) == 2


def test_newer_database_is_flagged(engine):
    upgrade(engine)
    with engine.begin() as conn:
        conn.execute(text("UPDATE schema_version SET version = :v WHERE id = 1"), {"v": SCHEMA_VERSION + 1})
    assert schema_status(engine) == "newer-than-code"


def test_expected_tables_exist(engine):
    upgrade(engine)
    tables = set(inspect(engine).get_table_names())
    assert {"schema_version", "config", "user", "role", "permission", "role_permission",
            "user_role", "setting", "audit_log", "page", "page_alias", "page_revision",
            "tag", "page_tag", "page_setting", "relation_kind", "relation", "page_link"} <= tables


def test_seed_data(engine):
    upgrade(engine)
    with engine.connect() as conn:
        roles = {r[0] for r in conn.execute(text("SELECT name FROM role"))}
        settings = {r[0] for r in conn.execute(text("SELECT code FROM setting"))}
        admin_perms = conn.execute(text(
            "SELECT COUNT(*) FROM role_permission rp JOIN role r ON r.id = rp.role_id WHERE r.name = 'admin'")).scalar()
        total_perms = conn.execute(text("SELECT COUNT(*) FROM permission")).scalar()
        kinds = conn.execute(text("SELECT COUNT(*) FROM relation_kind")).scalar()
    assert roles == {"reader", "editor", "gm", "mod", "admin"}
    assert settings == {"high_fantasy", "modern_horror", "scifi"}
    assert admin_perms == total_perms
    assert kinds >= 6


def test_page_constraints(engine):
    upgrade(engine)
    insert = "INSERT INTO page (type, slug, title) VALUES ('race', 'elf', 'Elf')"
    with engine.begin() as conn:
        conn.execute(text(insert))
        conn.execute(text("INSERT INTO page (type, slug, title) VALUES ('item', 'elf', 'Elf item')"))
    with pytest.raises(IntegrityError):
        with engine.begin() as conn:
            conn.execute(text(insert))
    with engine.connect() as conn:
        assert conn.execute(text("SELECT visibility FROM page WHERE type='race'")).scalar() == "public"


def test_foreign_keys_enforced(engine):
    upgrade(engine)
    with pytest.raises(IntegrityError):
        with engine.begin() as conn:
            conn.execute(text("INSERT INTO user_role (user_id, role_id) VALUES (999, 999)"))


def test_database_url_never_leaks_password(write_config, data_dir):
    settings = load_settings(write_config({"database": {"socket": ""}}))
    url = database_url(settings)
    assert url.drivername == "mysql+pymysql"
    assert url.query["charset"] == "utf8mb4"
    assert "s3cret-db-password" not in repr(url)
    assert "s3cret-db-password" not in str(create_db_engine(settings).url)


def test_socket_connection_url(write_config, data_dir):
    settings = load_settings(write_config({"database": {"socket": "/run/mysqld/mysqld.sock"}}))
    url = database_url(settings)
    assert url.query["unix_socket"] == "/run/mysqld/mysqld.sock"
    assert url.host is None


def test_migration_files_packaged():
    assert (Path(MIGRATIONS_DIR) / "env.py").is_file()
    assert (Path(MIGRATIONS_DIR) / "script.py.mako").is_file()
