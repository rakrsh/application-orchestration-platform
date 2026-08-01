---
name: build-frontend
description: How to build and serve the Angular frontend application.
---

# Build Frontend

The frontend is an Angular application located in the `frontend/` directory.

## Running the Dev Server Locally
Before serving locally, install dependencies in the frontend folder:

```powershell
cd frontend
npm install
npm start
```

This will run `npx ng serve --host 0.0.0.0 --port 4200` using the new `@angular/build` system.

## Building for Production
To build a production bundle:

```powershell
cd frontend
npm run build
```

This will compile the frontend artifacts into `frontend/dist/`.

## Notes for Dashboard Development
The Angular app now includes a state service and a dashboard UI in `frontend/src/app/components/`.
If you change form bindings or component templates, ensure `FormsModule` remains imported in `frontend/src/app/app.module.ts`.

## Serving with nginx in Production
The repository includes a production Docker image for the frontend that builds the Angular app and serves it with nginx. From the repository root, run:

```bash
docker compose build frontend
docker compose up -d frontend
```

The production UI is then available at `http://localhost:4200`.
