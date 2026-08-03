---
name: backend-api
description: Implement, test, and evolve the FastAPI backend, storage layer, and API contracts for the orchestration platform.
---

# Backend API Development

Use this skill when changing the FastAPI service, storage adapter, request/response schemas, telemetry behavior, error handling, or orchestration-related API endpoints.

## Repository context

- API entrypoint: [backend/fastapi/app/main.py](../../backend/fastapi/app/main.py)
- Storage layer: [backend/fastapi/app/storage.py](../../backend/fastapi/app/storage.py)
- Backend tests: [backend/fastapi/tests](../../backend/fastapi/tests)
- Bootstrap and environment setup: [setup.py](../../setup.py)
- Local development guide: [docs/development-guide.md](../../docs/development-guide.md)

## Core responsibilities

- Keep FastAPI routes thin and move domain logic into services or helpers where practical.
- Preserve the existing API contract unless the change intentionally updates it and the frontend/tests/docs are adjusted in the same pass.
- Honor the current auth contract: the backend expects header-based identity and role values such as `x-auth-request-user` and `x-auth-request-roles`.
- Ensure new endpoints and payload fields are reflected in the Angular UI state service or component model when relevant.

## Required behavior and conventions

- Use Pydantic models for request/response validation where possible.
- Prefer explicit, typed function signatures and descriptive names.
- Keep changes compatible with the current storage abstraction so the app can run against both in-memory and database-backed stores.
- If an endpoint changes semantics, update tests and any architecture notes that describe request flow or authorization impact.

## Endpoint and storage checklist

1. Review the existing routes in [backend/fastapi/app/main.py](../../backend/fastapi/app/main.py) before adding new handlers.
2. Confirm whether the change belongs in the route layer, the storage layer, or both.
3. Preserve current response keys such as `applications`, `nodes`, `metrics`, and app objects expected by the dashboard UI.
4. For persistence changes, inspect [backend/fastapi/app/storage.py](../../backend/fastapi/app/storage.py) and ensure the row-to-dict mapping remains consistent.
5. Add or update tests under [backend/fastapi/tests](../../backend/fastapi/tests) for new behavior, regressions, and auth errors.

## Testing and validation

Run the backend tests from the repository root or the backend folder:

```powershell
cd backend/fastapi
python -m pytest tests/
```

For local smoke checks, start the backend with the platform bootstrap flow or with the CLI and confirm the health endpoint responds as expected:

```powershell
python setup.py
```

## Important implementation notes

- The current health endpoint should stay lightweight and return a simple success payload.
- The app creation endpoint requires roles such as `admin` or `editor`; do not loosen access control without updating tests and docs.
- If tracing is enabled, keep span names and attributes meaningful and avoid excessive noise in production-like environments.
