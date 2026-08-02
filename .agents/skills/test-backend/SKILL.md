---
name: test-backend
description: How to run unit tests and testing suites for the FastAPI backend.
---

# Test Backend

The backend is built with FastAPI and uses Pytest for unit testing. 

## Running Tests
To run the backend test suite, navigate to the backend directory and run pytest:

```powershell
cd backend/fastapi
python -m pytest tests/
```

You can also run pytest with verbosity or coverage flags if configured. Make sure the virtual environment (`.venv` in the root) is activated when manually executing these tests.

## Architecture awareness
When changing API contract, auth behavior, or persistence, update the architecture notes in `architecture/C4_architecture.md` and the docs version in `docs/architecture/C4_architecture.md` so the request flow, edge cases, and authorization model stay in sync.
