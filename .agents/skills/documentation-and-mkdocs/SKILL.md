---
name: documentation-and-mkdocs
description: Maintain repository docs, architecture explanations, auth notes, and the MkDocs site so the documentation stays aligned with the platform implementation.
---

# Documentation and MkDocs Maintenance

Use this skill when updating documentation, architecture writeups, auth notes, local setup steps, or the published MkDocs site content.

## Repository context

- Root documentation index: [README.md](../../README.md)
- Development guide: [docs/development-guide.md](../../docs/development-guide.md)
- Architecture docs: [architecture/C4_architecture.md](../../architecture/C4_architecture.md) and [docs/architecture/C4_architecture.md](../../docs/architecture/C4_architecture.md)
- Auth docs: [auth](../../auth) and [docs/auth](../../docs/auth)
- MkDocs config: [mkdocs.yml](../../mkdocs.yml)
- Skills index: [skills.md](../../skills.md)

## Documentation expectations

- Update docs whenever behavior, setup steps, configuration, or architecture changes.
- Prefer concise, task-oriented documentation that tells the reader what to do and what to expect.
- Keep the docs aligned with the codebase rather than describing a hypothetical or outdated setup.
- When you change auth, storage, API behavior, or startup flow, update the relevant docs in the same change.

## Content areas to keep in sync

- Setup and bootstrap instructions
- Backend API contract changes
- Frontend dashboard behavior changes
- Auth and access-control notes
- Deployment or operational workflow changes
- Architecture diagrams and edge cases

## MkDocs workflow

Preview the docs locally with:

```powershell
.venv\Scripts\python -m mkdocs serve
```

The documentation site should be checked after local content changes to ensure navigation and formatting remain intact.

## Documentation checklist

1. Determine whether the change is user-facing, developer-facing, or architectural.
2. Update the most relevant source document in the repo rather than only the generated site output.
3. If the behavior is significant, update both the source documentation and the mirrored documentation under [docs](../../docs).
4. Ensure the skills index and repository overview remain accurate if new workflows or capabilities are introduced.

## Good documentation practices

- Use plain language and include exact commands where applicable.
- Link to the relevant source files and docs pages instead of duplicating too much implementation detail.
- Keep examples consistent with the current local environment and commands used by the repository.
- Preserve architecture boundaries and avoid overspecifying internal implementation details when the docs should stay conceptual.
