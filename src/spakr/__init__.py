"""spakr: game database web site."""

import sys

if sys.version_info < (3, 12):  # pragma: no cover
    raise RuntimeError(
        f"spakr needs Python 3.12 or newer; this is Python {sys.version.split()[0]}."
    )

BASE_VERSION = "0.0"  # MAJOR.MINOR; the real version is MAJOR.MINOR.BUILD (spakr.version)
