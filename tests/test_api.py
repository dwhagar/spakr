import json
import logging
import re

import pytest
from pydantic import BaseModel
from spectree import Response

from spakr import outbound
from spakr.api import API_VERSION, create_app
from spakr.version import software_version

VALID_CONFIG = {
    "database": {"name": "t", "user": "u", "password": "pw"},
    "secrets": {"secret_key": "k" * 40},
}


@pytest.fixture(autouse=True)
def _no_ambient_config(monkeypatch):
    monkeypatch.delenv("SPAKR_CONFIG", raising=False)


@pytest.fixture
def client():
    return create_app(config={"site": {"contact_url": "https://x.example/c"}}).test_client()


@pytest.fixture
def unconfigured(monkeypatch, tmp_path):
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("SPAKR_CONFIG", raising=False)
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
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path))
    client = create_app().test_client()
    assert client.get("/api/v1/health").status_code == 503
    good = tmp_path / "config.json"
    good.write_text(json.dumps(VALID_CONFIG))
    good.chmod(0o600)
    assert client.get("/api/v1/health").status_code == 200


def test_invalid_config_is_reported_not_raised(monkeypatch, tmp_path):
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path))
    bad = tmp_path / "config.json"
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


def test_wsgi_module_imports_without_config(monkeypatch, tmp_path):
    monkeypatch.setenv("SPAKR_DATA_DIR", str(tmp_path))
    import importlib

    from spakr import wsgi

    importlib.reload(wsgi)
    assert wsgi.application.test_client().get("/api/v1/health").status_code == 503


def test_openapi_served(client):
    spec = client.get("/api/v1/openapi.json").get_json()
    assert spec["openapi"].startswith("3.1")
    assert "/api/v1/health" in spec["paths"]
    json.dumps(spec)


def test_database_version_reported_when_db_layer_present(monkeypatch):
    import sys
    import types

    fake = types.ModuleType("spakr.db")
    fake.SCHEMA_VERSION = 3
    fake.create_db_engine = lambda settings: object()
    fake.get_schema_version = lambda engine: 2
    monkeypatch.setitem(sys.modules, "spakr.db", fake)
    response = create_app(config={}).test_client().get("/api/v1/health")
    assert response.status_code == 503
    body = response.get_json()
    assert body["status"] == "degraded"
    assert body["database_version"] == {"expected": 3, "current": 2, "state": "outdated"}
