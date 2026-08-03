# Angular Frontend

This folder contains the Angular orchestration dashboard for the platform, including the overview experience and the new telemetry view.

Quick start:

1. From `frontend/` run:

```bash
npm install
npx ng serve --open
```

This will start the dev server at http://localhost:4200.

Once the app is running, use the header tabs to switch between:

- Overview for application and service cards
- Telemetry for the Jaeger-style trace view and Aspire-style resource dashboard
- Create App for the application creation wizard

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
