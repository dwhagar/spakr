"""Every outbound HTTP request goes through here so it carries the same User-Agent.

Format: `spakr/<software version> spakr-api/<API version> (+<contact url>)`.
"""

import urllib.request
from typing import Any
from urllib.parse import quote

from spakr.api.integration import setting
from spakr.api.versions import API_VERSION
from spakr.version import software_version


def user_agent(config: Any | None = None) -> str:
    agent = f"spakr/{software_version()} spakr-api/{API_VERSION}"
    contact = setting(config, "site", "contact_url") if config is not None else None
    if contact:
        # Parentheses would end the comment early; quote() escapes them and spaces.
        agent += f" (+{quote(str(contact), safe=':/?#[]@!$&*+,;=%-._~')})"
    return agent


def build_request(url: str, config: Any | None = None, *, allow_http: bool = False):
    if not (url.startswith("https://") or (allow_http and url.startswith("http://"))):
        raise ValueError("outbound requests must use https")
    return urllib.request.Request(url, headers={"User-Agent": user_agent(config)})


def fetch(url: str, config: Any | None = None, *, timeout: float = 10, allow_http: bool = False):
    """Open an outbound URL with the standard User-Agent and a timeout."""
    return urllib.request.urlopen(
        build_request(url, config, allow_http=allow_http), timeout=timeout
    )
