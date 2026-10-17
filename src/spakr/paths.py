"""Where spakr keeps its data. Everything lives under one folder, /data by default.

/data is git-ignored. Override with SPAKR_DATA_DIR (tests, development) and
SPAKR_CONFIG (a config file somewhere else).
"""

import os
from pathlib import Path

DEFAULT_DATA_DIR = "/data"


def data_dir() -> Path:
    return Path(os.environ.get("SPAKR_DATA_DIR") or DEFAULT_DATA_DIR)


def config_path() -> Path:
    override = os.environ.get("SPAKR_CONFIG")
    return Path(override) if override else data_dir() / "config.json"
