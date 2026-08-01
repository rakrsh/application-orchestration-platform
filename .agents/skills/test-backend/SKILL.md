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
