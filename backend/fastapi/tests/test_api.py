import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient  # noqa: E402

from backend.fastapi.app import storage  # noqa: E402
from backend.fastapi.app.main import app as orchestration_app  # noqa: E402


def test_create_and_list_applications():
    store = storage.InMemoryAppStore()

    created = store.create_app(
        {
            "name": "demo-app",
            "description": "demo",
            "environment": "staging",
            "importType": "git",
            "targetOs": "linux",
            "detectedRuntime": "Node.js 20",
            "envVariables": {"NODE_ENV": "staging"},
        }
    )

    assert created["environment"] == "staging"
    assert created["status"] == "provisioning"
    assert created["tags"] == ["linux"]

    applications = store.list_applications()
    assert applications[0]["id"] == created["id"]
    assert applications[0]["projects"] == []


def test_orchestration_endpoint_exposes_dashboard_payload():
    client = TestClient(orchestration_app)
    response = client.get(
        "/api/orchestration",
        headers={
            "x-auth-request-user": "alice",
            "x-auth-request-roles": "admin",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "applications" in payload
    assert "nodes" in payload
    assert "metrics" in payload
    assert len(payload["applications"]) >= 1
    assert len(payload["nodes"]) >= 1


def test_create_app_endpoint_accepts_richer_payload():
    client = TestClient(orchestration_app)
    response = client.post(
        "/api/apps",
        json={
            "name": "billing-service",
            "description": "Handles billing workflows",
            "environment": "production",
            "importType": "zip",
            "targetOs": "windows",
            "detectedRuntime": "Python 3.12",
            "envVariables": {"PYTHON_ENV": "production"},
        },
        headers={
            "x-auth-request-user": "alice",
            "x-auth-request-roles": "admin",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "billing-service"
    assert payload["environment"] == "production"
    assert payload["targetOs"] == "windows"


def test_telemetry_endpoint_exposes_jaeger_and_aspire_data():
    client = TestClient(orchestration_app)
    response = client.get(
        "/api/telemetry",
        headers={
            "x-auth-request-user": "alice",
            "x-auth-request-roles": "admin",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "jaeger" in payload
    assert "aspire" in payload
    assert len(payload["jaeger"]["traces"]) >= 1
    assert len(payload["aspire"]["resources"]) >= 1
