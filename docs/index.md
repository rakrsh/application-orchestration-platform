# Application Orchestration Platform

This project provides a reference platform for hosting and managing web applications with a modern authentication and authorization stack.

## What is included

- FastAPI backend service
- Angular frontend scaffold
- Keycloak identity provider
- OAuth2 Proxy
- OpenFGA authorization service
- Docker Compose-based local development environment

## Quick start

1. Clone the repository.
2. Run `python setup.py` to install dependencies and create the platform CLI wrappers.
3. Start the local services with `.\platform.bat start` (or `./platform start` on Unix). This will automatically open the UI in your browser.
4. When finished, stop the services with `.\platform.bat stop`.

## Documentation map

- Architecture overview: [Architecture](architecture/C4_architecture.md)
- Backend service notes: [Backend](backend/fastapi/README.md)
- Frontend setup: [Frontend](frontend/README.md)
- Authentication and authorization docs: [Auth](auth/KEYCLOAK_README.md)
