# Build and Release Process

## 1. Overview
The Application Orchestration Platform follows a secure build and release process to ensure artifact integrity and traceability, complying with the EU CRA requirements.

## 2. Continuous Integration (CI)
Every Pull Request to `main` must pass the following automated checks:
- **Linting & Formatting:** ESLint, Prettier, Ruff/Black (Python).
- **Unit Tests:** `pytest` (Backend), `Karma/Jasmine` (Frontend) with required code coverage thresholds.
- **Security Scanning:** 
  - SAST (Static Application Security Testing) via Semgrep.
  - Dependency Scanning (e.g., `pip-audit`, `npm audit`).

## 3. Continuous Deployment / Release (CD)
When a release is tagged:
1. **Build:** Artifacts (Container images, UI bundles) are built in isolated CI runners.
2. **SBOM Generation:** A Software Bill of Materials (SBOM) in CycloneDX format is generated for both the Python backend and Node.js frontend.
3. **Artifact Publishing:** Images are pushed to the registry. The SBOM is attached to the GitHub Release.
4. **(Future Phase) Signing:** Container images will be signed using tools like `cosign`.

## 4. Environment Separation
- **Development/Local:** Ephemeral, local execution (e.g., Docker Compose).
- **Staging:** Replica of production for final testing.
- **Production:** Strictly controlled environment. Deployments happen via automated CD pipelines, not manual developer actions.
