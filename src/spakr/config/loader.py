"""Load and validate config.json.

Search order: explicit path; $SPAKR_CONFIG (when set it is the only candidate);
otherwise ./config.json, config.json in the application root, /etc/spakr/config.json.
The configuration never lives under the data directory.
Keys starting with an underscore are comments and are ignored. Error messages
name keys and rules, never values.
"""

import json
import os
import stat
from pathlib import Path

from spakr.paths import DEFAULT_DATA_DIR, app_root
from spakr.config.secret import Secret
from spakr.config.settings import (
    DatabaseSettings,
    MailSettings,
    PathSettings,
    RedisSettings,
    SecretSettings,
    Settings,
    SiteSettings,
)

ENV_CONFIG = "SPAKR_CONFIG"
ENV_DATA_DIR = "SPAKR_DATA_DIR"
SYSTEM_CONFIG = Path("/etc/spakr/config.json")
PLACEHOLDER = "CHANGE-ME"
TLS_MODES = ("none", "starttls", "tls")


class ConfigError(Exception):
    """The configuration is missing or invalid; the message is safe to show."""


# section -> key -> (type, default); a default of None means required.
_SECTIONS: dict[str, dict[str, tuple[type, object]]] = {
    "database": {"host": (str, "127.0.0.1"), "port": (int, 3306), "name": (str, None),
                 "user": (str, None), "password": (str, None), "socket": (str, "")},
    "secrets": {"secret_key": (str, None), "mail_password": (str, ""),
                "redis_password": (str, "")},
    "mail": {"host": (str, ""), "port": (int, 587), "tls": (str, "starttls"),
             "username": (str, ""), "sender": (str, "")},
    "redis": {"host": (str, "127.0.0.1"), "port": (int, 6379), "db": (int, 0)},
    "paths": {"data_dir": (str, DEFAULT_DATA_DIR), "content_repo": (str, ""),
              "media": (str, ""), "media_originals": (str, ""), "cache": (str, ""),
              "uploads": (str, "")},
    "site": {"name": (str, "spakr"), "base_url": (str, ""), "contact_url": (str, "")},
}


def find_config_path(path=None) -> Path:
    """Return the config file to use, or raise ConfigError listing where we looked."""
    if path is not None:
        candidates = [Path(path)]
    elif os.environ.get(ENV_CONFIG):
        candidates = [Path(os.environ[ENV_CONFIG])]
    else:
        candidates = [Path("config.json"), app_root() / "config.json", SYSTEM_CONFIG]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    looked = ", ".join(str(c) for c in candidates)
    raise ConfigError(
        f"No configuration file found (looked in: {looked}). "
        f"Copy examples/config.json.example to config.json, fill in the database "
        f"section and keep it mode 0600, or set {ENV_CONFIG} to its location."
    )


def _check_mode(path: Path) -> None:
    mode = path.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise ConfigError(
            f"{path} is accessible by other users (mode {stat.S_IMODE(mode):04o}); "
            f"it holds secrets. Run: chmod 600 {path}"
        )


def _section(raw: dict, name: str, spec: dict) -> dict:
    data = raw.get(name, {})
    if not isinstance(data, dict):
        raise ConfigError(f"'{name}' must be an object.")
    out = {}
    for key, (typ, default) in spec.items():
        if key not in data:
            if default is None:
                raise ConfigError(f"Missing required setting '{name}.{key}'.")
            out[key] = default
            continue
        value = data[key]
        if isinstance(value, bool) or not isinstance(value, typ):
            raise ConfigError(f"'{name}.{key}' must be {'a number' if typ is int else 'text'}.")
        out[key] = value
    unknown = [k for k in data if not k.startswith("_") and k not in spec]
    if unknown:
        raise ConfigError(f"Unknown setting '{name}.{unknown[0]}'.")
    return out


def load_settings(path=None, *, check_mode: bool = True) -> Settings:
    """Load settings; every problem is raised as ConfigError."""
    config_path = find_config_path(path)
    if check_mode:
        _check_mode(config_path)
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"Cannot read {config_path}: {exc.strerror}.") from None
    except ValueError as exc:
        raise ConfigError(f"{config_path} is not valid JSON: {exc}.") from None
    if not isinstance(raw, dict):
        raise ConfigError(f"{config_path} must contain a JSON object.")
    unknown = [k for k in raw if not k.startswith("_") and k not in _SECTIONS]
    if unknown:
        raise ConfigError(f"Unknown section '{unknown[0]}'.")

    s = {name: _section(raw, name, spec) for name, spec in _SECTIONS.items()}

    if PLACEHOLDER in s["database"]["password"]:
        raise ConfigError("'database.password' still holds the example placeholder; set the real MySQL password.")
    key = s["secrets"]["secret_key"]
    if PLACEHOLDER in key or len(key) < 16:
        raise ConfigError("'secrets.secret_key' must be a long random value (16+ characters, not the example placeholder).")
    if not 1 <= s["database"]["port"] <= 65535:
        raise ConfigError("'database.port' must be between 1 and 65535.")
    if s["mail"]["tls"] not in TLS_MODES:
        raise ConfigError(f"'mail.tls' must be one of: {', '.join(TLS_MODES)}.")

    p = s["paths"]
    data_dir = Path(os.environ.get(ENV_DATA_DIR) or p["data_dir"])
    if not data_dir.is_absolute():
        raise ConfigError("'paths.data_dir' must be an absolute path.")
    paths = PathSettings(
        data_dir=data_dir,
        content_repo=Path(p["content_repo"] or data_dir / "content.git"),
        media=Path(p["media"] or data_dir / "media"),
        media_originals=Path(p["media_originals"] or data_dir / "media-originals"),
        cache=Path(p["cache"] or data_dir / "cache"),
        uploads=Path(p["uploads"] or data_dir / "uploads"),
    )

    return Settings(
        database=DatabaseSettings(**{**s["database"], "password": Secret(s["database"]["password"])}),
        secrets=SecretSettings(**{k: Secret(v) for k, v in s["secrets"].items()}),
        mail=MailSettings(**s["mail"]),
        redis=RedisSettings(**s["redis"]),
        paths=paths,
        site=SiteSettings(**s["site"]),
        source=config_path,
    )
