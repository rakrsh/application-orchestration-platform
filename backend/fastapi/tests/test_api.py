import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient  # noqa: E402

from backend.fastapi.app import storage  # noqa: E402
from backend.fastapi.app.main import app as orchestration_app  # noqa: E402


class OrchestrationStoreTests(unittest.TestCase):
    def test_create_and_list_applications(self):
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

        self.assertEqual(created["environment"], "staging")
        self.assertEqual(created["status"], "provisioning")
        self.assertEqual(created["tags"], ["linux"])

        applications = store.list_applications()
        self.assertEqual(applications[0]["id"], created["id"])
        self.assertEqual(applications[0]["projects"], [])

    def test_orchestration_endpoint_exposes_dashboard_payload(self):
        client = TestClient(orchestration_app)
        response = client.get(
            "/api/orchestration",
            headers={
                "x-auth-request-user": "alice",
                "x-auth-request-roles": "admin",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("applications", payload)
        self.assertIn("nodes", payload)
        self.assertIn("metrics", payload)
        self.assertGreaterEqual(len(payload["applications"]), 1)
        self.assertGreaterEqual(len(payload["nodes"]), 1)

    def test_create_app_endpoint_accepts_richer_payload(self):
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

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["name"], "billing-service")
        self.assertEqual(payload["environment"], "production")
        self.assertEqual(payload["targetOs"], "windows")

    def test_telemetry_endpoint_exposes_jaeger_and_aspire_data(self):
        client = TestClient(orchestration_app)
        response = client.get(
            "/api/telemetry",
            headers={
                "x-auth-request-user": "alice",
                "x-auth-request-roles": "admin",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("jaeger", payload)
        self.assertIn("aspire", payload)
        self.assertGreaterEqual(len(payload["jaeger"]["traces"]), 1)
        self.assertGreaterEqual(len(payload["aspire"]["resources"]), 1)


if __name__ == "__main__":
    unittest.main()
