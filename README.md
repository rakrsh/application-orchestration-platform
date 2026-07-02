# application-orchestration-platform

A platform to host and manage web applications.

## Shared persistence

The local stack now includes a PostgreSQL service for shared storage across the FastAPI app, Keycloak, and OpenFGA. Start everything with Docker Compose and the data will persist in the `postgres-data` volume between runs.

Primary docs and artifacts:

- Statement of Work: [SOW.md](SOW.md)
- Architecture diagrams and C4 mermaid models: [architecture/C4_architecture.md](architecture/C4_architecture.md)
- Copilot instructions and agent/skill docs: [copilot-instructions.md](copilot-instructions.md), [agents.md](agents.md), [skills.md](skills.md)

See the repository docs folder for detailed API contracts and deployment notes.
