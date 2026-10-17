"""Where spakr keeps its files.

Articles and system data (content store, media, caches, uploads) live under
one folder, /data by default; it is ignored by version control. Override with
SPAKR_DATA_DIR (tests, development). The configuration file is config.json in
the application root (the checkout or install folder), never under /data;
SPAKR_CONFIG points at one somewhere else.
"""

import os
from pathlib import Path

DEFAULT_DATA_DIR = "/data"


def data_dir() -> Path:
    return Path(os.environ.get("SPAKR_DATA_DIR") or DEFAULT_DATA_DIR)


def app_root() -> Path:
    """The application root: the folder holding pyproject.toml, VERSION and examples/."""
    return Path(__file__).resolve().parents[2]


def config_path() -> Path:
    override = os.environ.get("SPAKR_CONFIG")
    return Path(override) if override else app_root() / "config.json"
