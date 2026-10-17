"""The Flask API served under /api/v1."""

from spakr.api.app import create_app
from spakr.api.versions import API_VERSION

__all__ = ["API_VERSION", "create_app"]
