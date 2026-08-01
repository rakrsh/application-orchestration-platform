# Conceptual Agents

This file documents the conceptual agent roles for automation and code-assist workflows in the Application Orchestration Platform (AOP) repository.

## Defined Agents

### Backend Developer
- **Role**: Specialized in FastAPI, Pydantic, database interactions, and backend logic.
- **Responsibilities**:
  - Implement and maintain REST APIs in `backend/fastapi`.
  - Write unit tests for backend code.
  - Manage database schemas and state.

### Frontend Developer
- **Role**: Specialized in Angular, RxJS, component structuring, and UI aesthetics.
- **Responsibilities**:
  - Implement and maintain the frontend web application in `frontend/`.
  - Adhere to the established dynamic and premium design aesthetics.
  - Ensure correct Angular builder configuration and TS/Angular compilation.

### Platform Architect
- **Role**: High-level orchestrator focusing on project architecture, integration, and platform tooling.
- **Responsibilities**:
  - Maintain the `cli.py` platform orchestration script.
  - Ensure backend, frontend, and asset services can run concurrently.
  - Review cross-component changes.
