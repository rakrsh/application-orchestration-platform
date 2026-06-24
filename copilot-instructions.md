# Copilot Instructions for this Repository

Purpose: Provide guidance for the Copilot agent and contributors about repository conventions, important files, and where to find design artifacts.

Key files:
- `SOW.md` — Project Statement of Work and summary acceptance criteria.
- `architecture/C4_architecture.md` — C4-style mermaid diagrams and architectural notes.
- `README.md` — Entry point and pointers.

Development conventions:
- Backend: FastAPI + Pydantic for schema validation.
- Frontend: Angular (scaffold committed under `frontend/`). To run locally, from `frontend/` run:

```bash
npm install
npx ng serve --open
```

The scaffold uses a local `package.json` and `frontend/README.md` with details; upgrade Angular version as needed.
- Auth: Keycloak for global RBAC; OpenFGA for fine-grained ReBAC.

Agent behavior hints:
- Prefer minimal, focused edits. Open a PR for large changes.
- When modifying auth or OpenFGA models, update `architecture/C4_architecture.md` and add migration notes.
