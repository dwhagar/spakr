import json
import os

import pytest

BASE_CONFIG = {
    "database": {"host": "127.0.0.1", "port": 3306, "name": "spakr_test",
                 "user": "spakr", "password": "s3cret-db-password"},
    "secrets": {"secret_key": "k" * 40},
}


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    path = tmp_path / "data"
    monkeypatch.setenv("SPAKR_DATA_DIR", str(path))
    return path


@pytest.fixture
def write_config(tmp_path):
    def _write(overrides=None, mode=0o600, name="config.json"):
        config = json.loads(json.dumps(BASE_CONFIG))
        for section, values in (overrides or {}).items():
            config.setdefault(section, {}).update(values)
        path = tmp_path / name
        path.write_text(json.dumps(config))
        os.chmod(path, mode)
        return path

    return _write
