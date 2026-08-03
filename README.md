# application-orchestration-platform

A platform to host and manage web applications.

## Shared persistence

The local stack now includes a PostgreSQL service for shared storage across the FastAPI app, Keycloak, and OpenFGA. Start everything with Docker Compose and the data will persist in the `postgres-data` volume between runs.

Primary docs and artifacts:

- Statement of Work: [SOW.md](SOW.md)
- Architecture diagrams and C4 mermaid models: [architecture/C4_architecture.md](architecture/C4_architecture.md)
- Copilot instructions and agent/skill docs: [copilot-instructions.md](copilot-instructions.md), [agents.md](agents.md), [skills.md](skills.md)

See the repository docs folder for detailed API contracts and deployment notes.

## Development mode

Use the root-level Python bootstrap script to start the platform locally:

```powershell
python setup.py
```

The script starts the shared Docker services, installs the backend and frontend dependencies, and launches the FastAPI API and Angular frontend in development mode.

For a prerequisite-only check without launching anything, run:

```powershell
python setup.py --check-only
```

## Production frontend serving

On Windows, running the local setup script now downloads the latest nginx release, builds the Angular UI for production, and starts nginx so the UI is served at http://localhost:4200.

To serve the UI in production mode with nginx, build and run the frontend container directly:

```bash
docker compose build frontend
docker compose up -d frontend
```

The UI will then be available at http://localhost:4200.

## Observability

The platform now includes a built-in observability experience with a Jaeger-style trace view and an Aspire-style resource dashboard. After starting the stack, open the Angular UI and switch to the Telemetry tab to inspect:

- recent Jaeger-like traces for backend operations such as app listing and app creation
- Aspire-style resource cards for the FastAPI API, Angular UI, and database service
- health and alert summaries that mirror the current platform status

The backend uses OpenTelemetry tracing for health checks, app listing, and app creation. To enable exporting spans to an OTLP collector, configure the endpoint before starting the backend:

```powershell
$env:OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
```

The frontend also emits a lightweight dashboard initialization span when the app bootstraps.

## Documentation

The MkDocs documentation site is published to GitHub Pages through the GitHub Actions workflow in [.github/workflows/docs.yml](.github/workflows/docs.yml).
