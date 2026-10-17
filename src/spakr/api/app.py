"""Flask application factory for the /api/v1 API."""

import logging
import re
import time
import uuid
from dataclasses import dataclass
from typing import Any

from flask import Flask, g, jsonify, request
from spectree import SpecTree

from spakr.api import health, integration
from spakr.api.errors import ApiError, register_error_handlers, spectree_before
from spakr.api.versions import API_VERSION
from spakr.logs import configure_logging

URL_PREFIX = "/api/v1"
_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{8,64}")
# Routes that work without a configuration file.
_OPEN_ENDPOINTS = {"health.health", "openapi"}

log = logging.getLogger("spakr.api")


@dataclass
class AppState:
    config: Any | None = None
    problem: str | None = None


def create_app(config: Any | None = None) -> Flask:
    """Build the app. Pass `config` in tests; otherwise it is loaded from /data/config.json.

    A missing or invalid configuration does not stop the app: it starts, logs the
    reason, answers /health with `not_configured` and every other route with a 503.
    """
    configure_logging()
    app = Flask("spakr")
    app.json.sort_keys = False
    state = AppState()
    app.extensions["spakr"] = state
    _load(state, config)

    spec = SpecTree(
        "flask",
        title="spakr API",
        version=str(API_VERSION),
        mode="strict",
        annotations=True,
        before=spectree_before,
    )
    app.register_blueprint(health.make_blueprint(spec), url_prefix=URL_PREFIX)
    spec.app = app

    @app.get(f"{URL_PREFIX}/openapi.json", endpoint="openapi")
    def openapi():
        return jsonify(spec.spec)

    app.extensions["spakr_spec"] = spec
    register_error_handlers(app)
    _register_hooks(app, config_given=config is not None)
    return app


def _load(state: AppState, config: Any | None) -> None:
    if config is not None:
        state.config, state.problem = config, None
        return
    state.config, state.problem = integration.load_config()
    if state.config is None:
        log.error("not configured: %s", state.problem)


def _register_hooks(app: Flask, *, config_given: bool) -> None:
    state: AppState = app.extensions["spakr"]

    @app.before_request
    def _begin():
        supplied = request.headers.get("X-Request-ID", "")
        g.request_id = supplied if _REQUEST_ID.fullmatch(supplied) else uuid.uuid4().hex
        g.started = time.monotonic()
        if state.config is None and not config_given:
            _load(state, None)  # the file may have been fixed since start-up
        if state.config is None and request.endpoint not in _OPEN_ENDPOINTS:
            raise ApiError(
                503,
                "Not configured",
                "The server has no valid configuration yet. See the server log.",
                headers={"Retry-After": "60"},
            )
        has_body = request.method in ("POST", "PUT", "PATCH") and request.content_length
        if has_body and not (request.is_json or request.mimetype == "multipart/form-data"):
            raise ApiError(415, "Unsupported Media Type", "Send application/json.")

    @app.after_request
    def _finish(response):
        response.headers["X-Request-ID"] = g.get("request_id", "")
        response.headers["X-API-Version"] = str(API_VERSION)
        response.headers.setdefault("Cache-Control", "no-store")
        response.headers.add("Vary", "Cookie, Authorization")
        started = g.get("started")
        log.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,  # never the query string
                "status": response.status_code,
                "duration_ms": round((time.monotonic() - started) * 1000, 1) if started else None,
            },
        )
        return response
