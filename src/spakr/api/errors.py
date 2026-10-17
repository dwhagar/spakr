"""One error format for the whole API: RFC 9457 problem details.

Every error is `application/problem+json` with type, title, status, detail,
instance and request_id (plus `errors` for validation). No stack traces, SQL
or file paths ever reach the client; they go to the log.
"""

import logging
from typing import Any

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

log = logging.getLogger("spakr.api")

PROBLEM_CONTENT_TYPE = "application/problem+json"


class ApiError(Exception):
    """Raise from any route to send a problem response."""

    def __init__(
        self,
        status: int,
        title: str,
        detail: str | None = None,
        *,
        errors: list[dict[str, str]] | None = None,
        headers: dict[str, str] | None = None,
        type: str = "about:blank",
    ):
        super().__init__(title)
        self.status = status
        self.title = title
        self.detail = detail
        self.errors = errors
        self.headers = headers or {}
        self.type = type


def problem_response(
    status: int,
    title: str,
    detail: str | None = None,
    *,
    errors: list[dict[str, str]] | None = None,
    headers: dict[str, str] | None = None,
    type: str = "about:blank",
):
    body: dict[str, Any] = {"type": type, "title": title, "status": status}
    if detail:
        body["detail"] = detail
    body["instance"] = request.path
    body["request_id"] = g.get("request_id")
    if errors:
        body["errors"] = errors
    response = jsonify(body)
    response.status_code = status
    response.headers["Content-Type"] = PROBLEM_CONTENT_TYPE
    for name, value in (headers or {}).items():
        response.headers[name] = value
    return response


def validation_errors(error: Any) -> list[dict[str, str]]:
    """Turn a pydantic ValidationError into [{field, message, code}]."""
    items = []
    for item in error.errors():
        location = ".".join(str(part) for part in item.get("loc", ()))
        items.append(
            {
                "field": location,
                "message": str(item.get("msg", "invalid")),
                "code": str(item.get("type", "invalid")),
            }
        )
    return items


def spectree_before(req, resp, req_validation_error, instance, adapter=None):
    """SpecTree hook: send request validation failures as our problem+json (422)."""
    if req_validation_error is not None:
        raise ApiError(
            422,
            "Validation failed",
            "The request did not pass validation.",
            errors=validation_errors(req_validation_error),
        )


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiError)
    def _api_error(error: ApiError):
        return problem_response(
            error.status,
            error.title,
            error.detail,
            errors=error.errors,
            headers=error.headers,
            type=error.type,
        )

    @app.errorhandler(HTTPException)
    def _http_error(error: HTTPException):
        headers = {}
        if error.code == 405 and getattr(error, "valid_methods", None):
            headers["Allow"] = ", ".join(error.valid_methods)
        return problem_response(error.code or 500, error.name, error.description, headers=headers)

    @app.errorhandler(Exception)
    def _unexpected(error: Exception):
        log.error("unhandled error", exc_info=error)
        return problem_response(500, "Internal Server Error", "Something went wrong.")
