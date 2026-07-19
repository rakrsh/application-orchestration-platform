# Development Guide

## Local setup

For a full local development environment, run the bootstrap script from the repository root:

```powershell
python setup.py
```

The script starts the Docker-based infrastructure services and launches both the backend and frontend in development mode.

To validate the prerequisites without starting services, use:

```powershell
python setup.py --check-only
```

## Useful commands

- Build the FastAPI image: `docker compose build fastapi`
- View running services: `docker compose ps`
- Stop the stack: `docker compose down`

## Documentation build

```bash
.
.venv\Scripts\python -m mkdocs serve
```

Use the above command to preview the documentation locally in the browser.
