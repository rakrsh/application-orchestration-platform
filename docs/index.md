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
2. Start the local services with `docker compose up -d`.
3. Open the frontend or backend endpoints as needed for local development.

## Documentation map

- Architecture overview: [Architecture](architecture/C4_architecture.md)
- Backend service notes: [Backend](backend/fastapi/README.md)
- Frontend setup: [Frontend](frontend/README.md)
- Authentication and authorization docs: [Auth](auth/KEYCLOAK_README.md)
