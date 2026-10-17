import re

from spakr import paths
from spakr.version import software_version


def test_software_version_shape():
    assert re.fullmatch(r"\d+\.\d+\.\d+", software_version())


def test_data_dir_default_and_override(monkeypatch, tmp_path):
    monkeypatch.delenv("SPAKR_DATA_DIR", raising=False)
    monkeypatch.delenv("SPAKR_CONFIG", raising=False)
    assert str(paths.data_dir()) == "/data"
    assert paths.config_path() == paths.app_root() / "config.json"
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path))
    assert paths.config_path() == paths.app_root() / "config.json"  # never under the data dir
    monkeypatch.setenv("SPAKR_CONFIG", "/x/c.json")
    assert str(paths.config_path()) == "/x/c.json"
