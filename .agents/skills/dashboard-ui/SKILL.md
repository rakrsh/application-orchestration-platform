---
name: dashboard-ui
description: How to develop and maintain the new Angular orchestration dashboard UI.
---

# Dashboard UI

The repository now includes a new Angular orchestration dashboard in `frontend/src/app/components/`.

## Key Components

- `frontend/src/app/components/layout/header.component.*`
  - Deployment mode selector
  - OS filter pills
  - Persona toggle
  - Dashboard tabs
- `frontend/src/app/components/dashboard/overview-tab.component.*`
  - Aggregates applications and filters services by OS
- `frontend/src/app/components/dashboard/application-card.component.*`
  - Accordion card layout for applications and nested project services
- `frontend/src/app/components/dashboard/project-card.component.*`
  - Service cards with status, latency, error rate, and action buttons
- `frontend/src/app/components/dashboard/replica-slider.component.*`
  - Slider for replica scaling and estimated resource display
- `frontend/src/app/components/dashboard/create-app-wizard.component.*`
  - Dual-mode Git import and ZIP upload creation wizard

## Development Notes

- The app now uses a shared state service at `frontend/src/app/services/orchestration-state.service.ts`.
- `FormsModule` is required in `frontend/src/app/app.module.ts` for form bindings and the wizard.
- The dashboard uses a dark glassmorphism aesthetic; keep styling consistent with the existing `glass-panel` approach.
- Feature behavior to validate:
  - Persona selection should restrict editing capabilities for Developer/Auditor.
  - Deployment mode changes should modify UI terminology (pods vs containers vs services).
  - OS filters should update the visible project/service list.
  - ZIP upload should support drag-and-drop and show selected file metadata.

## Running and Testing

Use the Angular frontend build instructions from `build-frontend`.
If you need to preview only the dashboard, run the dev server from `frontend/` and navigate to `http://localhost:4200`.
