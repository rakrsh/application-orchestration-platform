---
name: build-frontend
description: How to build and serve the Angular frontend application.
---

# Build Frontend

The frontend is an Angular application located in the `frontend/` directory.

## Running the Dev Server Locally
To serve the frontend independently of the `cli.py` platform orchestration, navigate to the `frontend/` directory and use npm:

```powershell
cd frontend
npm start
```

This will run `ng serve --host 0.0.0.0 --port 4200` using the new `@angular/build` system.

## Building for Production
To build a production bundle:

```powershell
cd frontend
npm run build
```

This will compile the frontend artifacts into `frontend/dist/`.

## Serving with nginx in Production
The repository includes a production Docker image for the frontend that builds the Angular app and serves it with nginx. From the repository root, run:

```bash
docker compose build frontend
docker compose up -d frontend
```

The production UI is then available at `http://localhost:4200`.
