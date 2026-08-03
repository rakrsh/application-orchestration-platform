---
name: platform-operations
description: Start, stop, troubleshoot, and maintain the full local platform stack including the CLI, backend, frontend, and asset services.
---

# Platform Operations

Use this skill when managing local runtime services, diagnosing startup issues, or changing the orchestration workflow around the CLI and bootstrap scripts.

## Repository context

- Platform CLI: [cli.py](../../cli.py)
- Bootstrap script: [setup.py](../../setup.py)
- Docker compose stack: [docker-compose.yml](../../docker-compose.yml)
- Service manifest: [assets/service-manifest.json](../../assets/service-manifest.json)
- Logs and operational state: [logs](../../logs) and [.platform_state.json](../../.platform_state.json)
- Development guide: [docs/development-guide.md](../../docs/development-guide.md)

## Primary commands

### Start the full stack

```powershell
python setup.py
```

This will create the virtual environment, install backend and frontend dependencies, and launch the platform services.

### Start via the platform CLI

```powershell
python cli.py start
# or
.\platform start
```

The CLI starts:
- the FastAPI backend on port 8000
- the Angular frontend on port 4200
- any asset services declared in the manifest

### Stop the running stack

```powershell
python cli.py stop
# or
.\platform stop
```

Use this to ensure managed processes are terminated and the state file is cleaned up.

## Operational expectations

- The CLI writes process IDs to `.platform_state.json` and uses log files under `logs/` for troubleshooting.
- On Windows, the startup flow may download and configure nginx for local production-style serving.
- The frontend and backend should be treated as a coupled development experience; changing one side often requires validating the other side.

## Troubleshooting checklist

- If the backend fails to start, verify the virtual environment exists and that Python dependencies were installed successfully.
- If the frontend fails to start, confirm Node dependencies were installed in [frontend](../../frontend) and that the Angular dev server can bind to port 4200.
- If asset services do not launch, inspect [assets/service-manifest.json](../../assets/service-manifest.json) and ensure the referenced scripts or binaries exist.
- If a previous run left processes behind, stop the stack with the CLI and inspect the state file before starting again.

## Production-style frontend serving

For a production-style local serve using nginx:

```powershell
docker compose build frontend
docker compose up -d frontend
```

The UI is then available at `http://localhost:4200`.

## Change guidance

- Before changing startup behavior, understand whether the change affects bootstrap, runtime orchestration, or deployment packaging.
- If a change alters service startup order, ports, or logging, update both the CLI behavior and the docs in [docs/development-guide.md](../../docs/development-guide.md).
- Keep operational scripts idempotent wherever practical so repeated runs remain predictable.
