import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC = str(Path(__file__).resolve().parents[1] / "src")
MYSQL_URL = os.environ.get("SPAKR_TEST_DATABASE_URL")


def run(*args, env=None):
    return subprocess.run([sys.executable, "-m", "spakr", *args], capture_output=True, text=True,
                          env={"PYTHONPATH": SRC, "PATH": "", **(env or {})})


def test_init_db_unreachable_database_fails_gracefully(write_config, data_dir):
    config = write_config({"database": {"host": "127.0.0.1", "port": 1}})
    result = run("--config", str(config), "init-db", env={"SPAKR_DATA_DIR": str(data_dir)})
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "Cannot use the database" in result.stderr
    assert "s3cret-db-password" not in result.stderr


@pytest.mark.skipif(not MYSQL_URL, reason="SPAKR_TEST_DATABASE_URL not set")
def test_init_db_and_db_version_on_mysql(tmp_path, data_dir):
    from sqlalchemy.engine import make_url

    url = make_url(MYSQL_URL)
    config = tmp_path / "config.json"
    config.write_text(json.dumps({
        "database": {"host": url.host, "port": url.port or 3306, "name": url.database,
                     "user": url.username, "password": url.password},
        "secrets": {"secret_key": "k" * 40},
    }))
    config.chmod(0o600)
    env = {"SPAKR_DATA_DIR": str(data_dir)}
    first = run("--config", str(config), "init-db", env=env)
    assert first.returncode == 0, first.stderr
    assert (data_dir / "media").is_dir()
    shown = run("--config", str(config), "db-version", env=env)
    assert "applied: 2" in shown.stdout and "expected: 2" in shown.stdout
