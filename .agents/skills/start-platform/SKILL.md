---
name: start-platform
description: How to start and stop the platform services (frontend, backend, assets) using the cli.py script.
---

# Start Platform

The repository includes a custom Python script (`cli.py`) for managing all platform services at once.

## Starting the Platform
To start the platform, run:
```powershell
python cli.py start
# OR
.\platform start
```
This command starts:
- The FastAPI backend (running at `localhost:8000`)
- The Angular frontend (running at `localhost:4200`)
- Any asset services specified in `assets/service-manifest.json`

The frontend now includes a dashboard UI with orchestration controls, app/project cards, replica scaling, and a creation wizard.
If dependencies are missing, install them first in the `frontend/` folder with `npm install`.

For the production UI container, the repository also supports running the frontend through nginx via Docker Compose:
```bash
docker compose up -d frontend
```
This serves the built Angular bundle on `http://localhost:4200`.

The CLI creates a `.platform_state.json` file to keep track of the process IDs, and all logs are written to the `logs/` directory.

## Stopping the Platform
To stop all platform services, run:
```powershell
python cli.py stop
# OR
.\platform stop
```
This safely kills the processes tracked in `.platform_state.json` and deletes the state file. Always use this to ensure you don't leave zombie processes running in the background.
