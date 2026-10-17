import json
import logging
import re

import pytest
from pydantic import BaseModel
from spectree import Response

from spakr import outbound
from spakr.api import API_VERSION, create_app, integration
from spakr.version import software_version

_REAL_DATABASE_VERSIONS = integration.database_versions

VALID_CONFIG = {
    "database": {"name": "t", "user": "u", "password": "pw"},
    "secrets": {"secret_key": "k" * 40},
}


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    """No config from the environment, the working directory or the data folder."""
    monkeypatch.delenv("SPAKR_CONFIG", raising=False)
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.chdir(tmp_path)


@pytest.fixture(autouse=True)
def _database_up(monkeypatch):
    """Health tests do not need a live MySQL: report a database at the expected version."""
    monkeypatch.setattr(integration, "database_versions", lambda config: (2, 2, "ok"))


@pytest.fixture
def client():
    return create_app(config={"site": {"contact_url": "https://x.example/c"}}).test_client()


@pytest.fixture
def unconfigured():
    return create_app()


def test_health_reports_versions(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert body["configured"] is True
    assert body["api_version"] == API_VERSION
    assert body["software_version"] == software_version()
    assert set(body["database_version"]) == {"expected", "current", "state"}
    assert response.headers["X-API-Version"] == str(API_VERSION)


def test_health_degraded_when_database_unreachable(client, monkeypatch):
    monkeypatch.setattr(integration, "database_versions", lambda config: (2, None, "unavailable"))
    response = client.get("/api/v1/health")
    assert response.status_code == 503
    assert response.get_json()["database_version"]["state"] == "unavailable"


def test_no_config_file_fails_gracefully(unconfigured):
    client = unconfigured.test_client()
    health = client.get("/api/v1/health")
    assert health.status_code == 503
    assert health.get_json()["status"] == "not_configured"
    assert health.get_json()["api_version"] == API_VERSION
    other = client.get("/api/v1/nothing")
    assert other.status_code == 503
    assert other.content_type == "application/problem+json"
    assert "Traceback" not in other.get_data(as_text=True)


def test_config_fixed_without_restart(monkeypatch, tmp_path):
    good = tmp_path / "elsewhere.json"
    monkeypatch.setenv("SPAKR_CONFIG", str(good))
    client = create_app().test_client()
    assert client.get("/api/v1/health").status_code == 503
    good.write_text(json.dumps(VALID_CONFIG))
    good.chmod(0o600)
    assert client.get("/api/v1/health").status_code == 200


def test_invalid_config_is_reported_not_raised(monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    monkeypatch.setenv("SPAKR_CONFIG", str(bad))
    bad.write_text("{not json")
    bad.chmod(0o600)
    response = create_app().test_client().get("/api/v1/health")
    assert response.get_json()["status"] == "not_configured"


def test_problem_json_for_unknown_route(client):
    response = client.get("/api/v1/missing", headers={"X-Request-ID": "abcdef123456"})
    body = response.get_json()
    assert response.status_code == 404
    assert response.content_type == "application/problem+json"
    assert body["status"] == 404 and body["instance"] == "/api/v1/missing"
    assert body["request_id"] == "abcdef123456" == response.headers["X-Request-ID"]


def test_request_id_generated_and_bad_one_replaced(client):
    response = client.get("/api/v1/health", headers={"X-Request-ID": "bad id!"})
    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["X-Request-ID"])


def test_method_not_allowed_has_allow_header(client):
    response = client.post("/api/v1/health", json={})
    assert response.status_code == 405
    assert "GET" in response.headers["Allow"]


def test_unsupported_content_type(client):
    response = client.post("/api/v1/health", data="x", content_type="text/plain")
    assert response.status_code == 415


def test_unexpected_error_hides_details(caplog):
    app = create_app(config={})

    @app.get("/boom")
    def boom():
        raise RuntimeError("secret detail /srv/path")

    app.config["PROPAGATE_EXCEPTIONS"] = False
    with caplog.at_level(logging.ERROR):
        response = app.test_client().get("/boom")
    assert response.status_code == 500
    assert "secret" not in response.get_data(as_text=True)
    assert response.content_type == "application/problem+json"


def test_validation_errors_use_problem_json():
    from flask import Blueprint

    class Query(BaseModel):
        limit: int

    app = create_app(config={})
    spec = app.extensions["spakr_spec"]
    bp = Blueprint("t", __name__)

    @bp.get("/q")
    @spec.validate(query=Query, resp=Response(HTTP_200=None))
    def q():
        return {}

    app.register_blueprint(bp)
    response = app.test_client().get("/q?limit=abc")
    assert response.status_code == 422
    assert response.content_type == "application/problem+json"
    assert response.get_json()["errors"][0]["field"] == "limit"


def test_logs_have_no_query_string(client, capsys):
    client.get("/api/v1/health?token=hunter2")
    assert "hunter2" not in capsys.readouterr().err


def test_user_agent():
    agent = outbound.user_agent({"site": {"contact_url": "https://x.example/a (b)"}})
    assert agent.startswith(
        f"spakr/{software_version()} spakr-api/{API_VERSION} (+https://x.example/"
    )
    assert "(b)" not in agent
    assert outbound.user_agent().endswith(f"spakr-api/{API_VERSION}")
    with pytest.raises(ValueError):
        outbound.build_request("http://example.org/")


def test_wsgi_module_imports_without_config():
    import importlib

    from spakr import wsgi

    importlib.reload(wsgi)
    assert wsgi.application.test_client().get("/api/v1/health").status_code == 503


def test_openapi_served(client):
    spec = client.get("/api/v1/openapi.json").get_json()
    assert spec["openapi"].startswith("3.1")
    assert "/api/v1/health" in spec["paths"]
    json.dumps(spec)


@pytest.mark.parametrize(
    ("applied", "state"),
    [(None, "uninitialised"), (1, "needs-upgrade"), (2, "ok"), (3, "newer-than-code")],
)
def test_database_versions_states(monkeypatch, applied, state):
    monkeypatch.setattr(integration, "database_versions", _REAL_DATABASE_VERSIONS)
    monkeypatch.setattr(integration, "SCHEMA_VERSION", 2)
    monkeypatch.setattr(integration, "create_db_engine", lambda settings: object())
    monkeypatch.setattr(integration, "get_schema_version", lambda engine: applied)
    assert integration.database_versions(object()) == (2, applied, state)


def test_database_versions_unreachable(monkeypatch):
    def boom(settings):
        raise OSError("down")

    monkeypatch.setattr(integration, "database_versions", _REAL_DATABASE_VERSIONS)
    monkeypatch.setattr(integration, "create_db_engine", boom)
    _, current, state = integration.database_versions(object())
    assert (current, state) == (None, "unavailable")


def test_health_uses_the_real_integration(client, monkeypatch):
    monkeypatch.setattr(integration, "database_versions", _REAL_DATABASE_VERSIONS)
    monkeypatch.setattr(integration, "SCHEMA_VERSION", 2)
    monkeypatch.setattr(integration, "create_db_engine", lambda settings: object())
    monkeypatch.setattr(integration, "get_schema_version", lambda engine: 1)
    body = client.get("/api/v1/health").get_json()
    assert body["database_version"] == {"expected": 2, "current": 1, "state": "needs-upgrade"}


def test_health_not_ok_when_database_needs_upgrade(client, monkeypatch):
    monkeypatch.setattr(integration, "database_versions", lambda c: (3, 2, "needs-upgrade"))
    response = client.get("/api/v1/health")
    assert response.status_code == 503
    assert response.get_json()["status"] == "degraded"
