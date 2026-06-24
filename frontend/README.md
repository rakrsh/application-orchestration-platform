# Angular Frontend (minimal scaffold)

This folder contains a minimal Angular application scaffold.

Quick start:

1. From `frontend/` run:

```bash
npm install
npx ng serve --open
```

This will start the dev server at http://localhost:4200.

If you prefer to use a global Angular CLI installation, run `ng serve` instead of `npx ng serve`.

Pre-commit hooks

Install developer tooling and enable pre-commit hooks:

```bash
python -m pip install --user pre-commit black isort flake8
pre-commit install
```

To run hooks across the repository:

```bash
pre-commit run --all-files
```
