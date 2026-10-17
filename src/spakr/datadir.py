"""Create and check the data directory (/data by default)."""

import os

from spakr.config import ConfigError, Settings

MODE = 0o750


def ensure_data_dirs(settings: Settings) -> None:
    """Create the data folders; raise ConfigError with a fix if they are not writable."""
    p = settings.paths
    for path in (p.data_dir, p.media, p.media_originals, p.cache, p.uploads):
        try:
            path.mkdir(mode=MODE, parents=True, exist_ok=True)
        except OSError as exc:
            raise ConfigError(
                f"Cannot create {path} ({exc.strerror}). Create it and make it writable by "
                f"the spakr user, or set paths.data_dir / SPAKR_DATA_DIR to another folder."
            ) from None
        if not os.access(path, os.W_OK | os.X_OK):
            raise ConfigError(f"{path} is not writable by this user.")
