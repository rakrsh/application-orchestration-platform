# Copilot Instructions for this Repository

## Purpose
Provide repository-specific guidance for Copilot and contributors working on this platform. Follow these instructions when editing code, docs, configuration, or architecture files.

## Repository structure
- Root docs and entry points: README.md, mkdocs.yml, docker-compose.yml, setup.py
- Backend: backend/fastapi/
  - API entrypoint: backend/fastapi/app/main.py
  - Storage layer: backend/fastapi/app/storage.py
  - Tests: backend/fastapi/tests/
- Frontend: frontend/
  - Angular app shell and components live under frontend/src/app/
- Architecture and design: architecture/C4_architecture.md
- Auth and access control docs: auth/ and docs/auth/

## Architecture guidance
- Keep the architecture aligned with the C4 model in architecture/C4_architecture.md.
- When adding or changing services, components, or interactions, update the architecture document and relevant auth docs.
- Prefer a clear separation between API routes, domain logic, storage, and infrastructure concerns.
- Preserve the intended boundaries between frontend, backend, auth, and policy services.

## Coding practices

### Python / FastAPI
- Use Python 3.11+ compatible syntax and style.
- Keep FastAPI routes thin; move business logic into services or helper modules where practical.
- Validate request and response models using Pydantic.
- Prefer explicit, typed function signatures and descriptive names.
- Do not add unnecessary docstrings or comments; code should be self-explanatory.
- Do not introduce new dependencies without a clear need; prefer standard library and existing packages.
- Use pytest for testing and keep tests focused on observable behavior.
- Add or update tests when changing behavior.
- Follow existing repository conventions in backend/fastapi/app/.

### TypeScript / Angular
- Keep Angular components focused on presentation and input/output behavior.
- Use Angular modules and components consistently with the existing scaffold under frontend/src/app/.
- Use Angular 21+ features and syntax, and follow the Angular style guide.
- Prefer small, reusable components over large inline templates.
- Keep styles scoped to component CSS files unless a shared style is clearly justified.

### Shell / DevOps
- Prefer small, idempotent scripts for local setup and build tasks.
- Keep environment-specific behavior explicit in scripts and docs.
- Use repository-relative paths rather than hard-coded absolute paths.
- **CI / GitHub Actions:** Always use the latest available major versions of GitHub Actions (e.g., `actions/checkout@v7`).
- **CI / GitHub Actions:** Do not use deprecated wrappers like `semgrep-action`; prefer invoking CLI tools (e.g., `pip install semgrep && semgrep scan`) directly within CI steps.

## Dependency management
- Keep dependencies declared in the most local place that makes sense:
  - Python requirements: backend/fastapi/requirements.txt
  - Frontend dependencies: frontend/package.json
- Avoid adding packages without documenting why they are needed.
- Prefer stable, well-supported versions and update lockfiles or package manifests intentionally.
- When introducing new services or external integrations, document the dependency and expected configuration in the relevant README or docs page.

## Documentation expectations
- Update documentation when behavior, setup steps, configuration, or architecture change.
- Primary documentation locations:
  - README.md for repository overview and quick start
  - docs/development-guide.md for local development flow
  - docs/architecture/ and architecture/ for architecture notes
  - auth/ and docs/auth/ for auth-related documentation
- Keep docs concise, accurate, and task-oriented.

## Testing expectations
- Write or update tests for backend changes when practical.
- Backend tests live under backend/fastapi/tests/.
- Use pytest-style testing and keep tests focused on observable behavior.
- When changing auth, storage, or API behavior, verify with the relevant tests and manual checks.

## Development workflow
- For local development, use the repository bootstrap flow from setup.py.
- Prefer minimal, focused edits and avoid unrelated refactors.
- If a change touches architecture, auth, or access-control semantics, include documentation updates.
- For larger changes, summarize the impact clearly and keep the scope contained.

## Instructions for Copilot
- Make the smallest change that solves the problem.
- Preserve existing conventions and do not introduce unnecessary abstractions.
- When unsure, prefer clarity and explicitness over cleverness.
- If a change affects setup, runtime behavior, or architecture, explain it briefly in the response.
- Prefer updating the relevant docs alongside the code when behavior changes.
