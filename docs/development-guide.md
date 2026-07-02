# Development Guide

## Local setup

```bash
docker compose up -d
```

## Useful commands

- Build the FastAPI image: `docker compose build fastapi`
- View running services: `docker compose ps`
- Stop the stack: `docker compose down`

## Documentation build

```bash
.
.venv\Scripts\python -m mkdocs serve
```

Use the above command to preview the documentation locally in the browser.
