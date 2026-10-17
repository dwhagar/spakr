"""The running software version, MAJOR.MINOR.BUILD.

Sources, first match wins:
1. src/spakr/_version.txt, written at install time by `scripts/version.sh --write`
2. scripts/version.sh run in a git checkout (counts commits since VERSION changed)
3. the VERSION file with build 0
4. "0.0.0" when nothing is available
"""

import subprocess
from functools import lru_cache
from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PACKAGE_DIR.parent.parent


@lru_cache(maxsize=1)
def software_version() -> str:
    stamped = _PACKAGE_DIR / "_version.txt"
    if stamped.is_file():
        text = stamped.read_text().strip()
        if text:
            return text
    script = _REPO_ROOT / "scripts" / "version.sh"
    if script.is_file():
        try:
            out = subprocess.run(
                ["sh", str(script)], capture_output=True, text=True, timeout=5, check=True
            ).stdout.strip()
            if out:
                return out
        except (OSError, subprocess.SubprocessError):
            pass
    base = _REPO_ROOT / "VERSION"
    if base.is_file():
        text = base.read_text().strip()
        if text:
            return f"{text}.0"
    return "0.0.0"
