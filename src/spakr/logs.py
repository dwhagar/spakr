"""Small structured (JSON lines) logging to stderr, with the request id on every line.

mod_wsgi writes stderr into the Apache error log. Never log passwords, tokens,
API keys, cookies, the Authorization header, request bodies or query strings.
"""

import json
import logging
import sys

from flask import g, has_request_context

_CONFIGURED = False
_EXTRA = ("method", "path", "status", "duration_ms")


class _RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = g.get("request_id") if has_request_context() else None
        return True


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if getattr(record, "request_id", None):
            entry["request_id"] = record.request_id
        for key in _EXTRA:
            if hasattr(record, key):
                entry[key] = getattr(record, key)
        if record.exc_info:
            entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(entry, default=str)


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Attach the JSON stderr handler to the "spakr" logger once."""
    global _CONFIGURED
    logger = logging.getLogger("spakr")
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(_JsonFormatter())
        handler.addFilter(_RequestIdFilter())
        logger.addHandler(handler)
        logger.propagate = False
        _CONFIGURED = True
    logger.setLevel(level)
    return logger
