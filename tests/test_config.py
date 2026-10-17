import json
import pickle
import subprocess
import sys
from pathlib import Path

import pytest

from spakr.config import ConfigError, Secret, load_settings


def test_loads_valid_config(write_config, data_dir):
    s = load_settings(write_config())
    assert s.database.name == "spakr_test"
    assert s.database.password.reveal() == "s3cret-db-password"
    assert s.paths.data_dir == data_dir
    assert s.paths.media == data_dir / "media"
    assert s.paths.content_repo == data_dir / "content.git"


def test_default_data_dir_is_slash_data(write_config, monkeypatch):
    monkeypatch.delenv("SPAKR_DATA_DIR", raising=False)
    assert load_settings(write_config()).paths.data_dir == Path("/data")


def test_config_data_dir_and_explicit_path(write_config, monkeypatch, tmp_path):
    monkeypatch.delenv("SPAKR_DATA_DIR", raising=False)
    s = load_settings(write_config({"paths": {"data_dir": str(tmp_path / "d"), "cache": "/elsewhere/cache"}}))
    assert s.paths.data_dir == tmp_path / "d"
    assert s.paths.cache == Path("/elsewhere/cache")


def test_missing_file_is_clear(tmp_path, monkeypatch):
    monkeypatch.delenv("SPAKR_CONFIG", raising=False)
    with pytest.raises(ConfigError, match="No configuration file found"):
        load_settings(tmp_path / "nope.json")


def test_env_var_locates_file(write_config, monkeypatch):
    monkeypatch.setenv("SPAKR_CONFIG", str(write_config()))
    assert load_settings().database.user == "spakr"


def test_group_readable_refused(write_config):
    with pytest.raises(ConfigError, match="chmod 600"):
        load_settings(write_config(mode=0o640))


def test_invalid_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{ nope")
    path.chmod(0o600)
    with pytest.raises(ConfigError, match="not valid JSON"):
        load_settings(path)


@pytest.mark.parametrize("overrides, message", [
    ({"database": {"password": "CHANGE-ME (secret)"}}, "placeholder"),
    ({"secrets": {"secret_key": "short"}}, "secret_key"),
    ({"database": {"port": "3306"}}, "database.port"),
    ({"database": {"port": 70000}}, "between"),
    ({"mail": {"tls": "weird"}}, "mail.tls"),
    ({"paths": {"data_dir": "relative/dir"}}, "absolute"),
    ({"site": {"bogus": 1}}, "Unknown setting"),
])
def test_validation_errors(write_config, data_dir, monkeypatch, overrides, message):
    monkeypatch.delenv("SPAKR_DATA_DIR", raising=False)
    with pytest.raises(ConfigError, match=message):
        load_settings(write_config(overrides))


def test_missing_required_key(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"secrets": {"secret_key": "k" * 40}}))
    path.chmod(0o600)
    with pytest.raises(ConfigError, match="database.name"):
        load_settings(path)


def test_underscore_keys_ignored_and_example_loads(tmp_path, data_dir):
    example = Path(__file__).resolve().parents[1] / "examples" / "config.json.example"
    raw = json.loads(example.read_text())
    raw["database"]["password"] = "real"
    raw["secrets"]["secret_key"] = "x" * 40
    path = tmp_path / "config.json"
    path.write_text(json.dumps(raw))
    path.chmod(0o600)
    assert load_settings(path).site.name == "spakr"


def test_errors_never_contain_values(write_config):
    with pytest.raises(ConfigError) as info:
        load_settings(write_config({"secrets": {"secret_key": "tooshort"}}))
    assert "tooshort" not in str(info.value)


def test_secret_hidden_everywhere(write_config, data_dir):
    s = load_settings(write_config())
    for text in (repr(s), str(s), repr(s.database), repr(s.secrets)):
        assert "s3cret-db-password" not in text
        assert "kkkk" not in text
    with pytest.raises(TypeError):
        pickle.dumps(Secret("x"))


def test_cli_missing_config_exits_nonzero_without_traceback(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "spakr", "--config", str(tmp_path / "missing.json"), "check-config"],
        capture_output=True, text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), "PATH": ""},
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "error" in result.stderr


def test_cli_version():
    result = subprocess.run(
        [sys.executable, "-m", "spakr", "version"], capture_output=True, text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), "PATH": ""},
    )
    assert result.returncode == 0
    assert result.stdout.strip().count(".") == 2
