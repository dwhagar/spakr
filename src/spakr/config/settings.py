"""Settings objects (frozen) built from config.json."""

from dataclasses import dataclass
from pathlib import Path

from spakr.config.secret import Secret


@dataclass(frozen=True)
class DatabaseSettings:
    """Manual-only: never editable through the API or UI."""

    host: str
    port: int
    name: str
    user: str
    password: Secret
    socket: str = ""


@dataclass(frozen=True)
class SecretSettings:
    secret_key: Secret
    mail_password: Secret
    redis_password: Secret


@dataclass(frozen=True)
class MailSettings:
    host: str
    port: int
    tls: str
    username: str
    sender: str


@dataclass(frozen=True)
class RedisSettings:
    host: str
    port: int
    db: int


@dataclass(frozen=True)
class PathSettings:
    """Everything lives under data_dir (default /data, git-ignored)."""

    data_dir: Path
    content_repo: Path
    media: Path
    media_originals: Path
    cache: Path
    uploads: Path


@dataclass(frozen=True)
class SiteSettings:
    name: str
    base_url: str
    contact_url: str


@dataclass(frozen=True)
class Settings:
    database: DatabaseSettings
    secrets: SecretSettings
    mail: MailSettings
    redis: RedisSettings
    paths: PathSettings
    site: SiteSettings
    source: Path
