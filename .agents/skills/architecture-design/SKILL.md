---
name: architecture-design
description: How to maintain the platform architecture documentation, diagrams, and design decisions.
---

# Architecture Design

Use this skill when updating the platform architecture, adding new services, or changing request flows, authorization boundaries, deployment modes, or persistence concerns.

## What to keep in sync

- [architecture/C4_architecture.md](../../architecture/C4_architecture.md)
- [docs/architecture/C4_architecture.md](../../docs/architecture/C4_architecture.md)
- [skills.md](../../skills.md)
- [copilot-instructions.md](../../copilot-instructions.md)

## Required coverage for major changes

- Overall architecture overview
- System context and container diagrams
- Backend and frontend component maps
- Sequence diagrams for key user journeys
- Class or domain model updates
- Deployment-mode-specific flow changes
- Edge cases and failure scenarios
- Any impact on authentication, authorization, or persistence

## Guidance

- Prefer diagrams that explain behavior and boundaries, not just static structure.
- Include failure scenarios such as missing auth headers, denied actions, invalid uploads, and persistence failures.
- Keep the documentation aligned with the current FastAPI API surface and the Angular dashboard state model.
- If a change affects behavior or operations, update both the architecture source and the docs copy.
