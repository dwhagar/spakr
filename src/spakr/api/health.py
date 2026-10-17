"""GET /api/v1/health: liveness, configuration state and the three versions."""

from flask import Blueprint, current_app
from pydantic import BaseModel
from spectree import Response

from spakr.api import integration
from spakr.api.versions import API_VERSION
from spakr.version import software_version


class DatabaseVersion(BaseModel):
    expected: int | None
    current: int | None
    state: str  # ok | outdated | unavailable | unknown


class Health(BaseModel):
    status: str  # ok | not_configured | degraded
    configured: bool
    software_version: str
    api_version: int
    database_version: DatabaseVersion


def database_state(expected: int | None, current: int | None) -> str:
    if expected is None:
        return "unknown"
    if current is None:
        return "unavailable"
    return "ok" if current == expected else "outdated"


def make_blueprint(spec) -> Blueprint:
    bp = Blueprint("health", __name__)

    @bp.get("/health")
    @spec.validate(resp=Response(HTTP_200=Health, HTTP_503=Health))
    def health():
        state = current_app.extensions["spakr"]
        configured = state.config is not None
        expected, current = (
            integration.database_versions(state.config) if configured else (None, None)
        )
        db_state = database_state(expected, current) if configured else "unknown"
        if not configured:
            status = "not_configured"
        elif db_state in ("outdated", "unavailable"):
            status = "degraded"
        else:
            status = "ok"
        body = Health(
            status=status,
            configured=configured,
            software_version=software_version(),
            api_version=API_VERSION,
            database_version=DatabaseVersion(expected=expected, current=current, state=db_state),
        )
        return body.model_dump(), (200 if status == "ok" else 503)

    return bp
