# Security Testing Checklist

Before any major release, ensure the following security tests have passed:

- [ ] **SAST:** Semgrep rules have passed without high/critical findings.
- [ ] **Dependency Scanning:** `pip-audit` and `npm audit` show no known critical vulnerabilities.
- [ ] **Container Scanning:** Docker images have been scanned with Trivy or similar, with no critical OS package vulnerabilities.
- [ ] **Unit Tests:** `pytest` code coverage is >80% for backend services.
- [ ] **Authentication Checks:** Keycloak login flows have been manually tested.
- [ ] **Authorization Checks:** OpenFGA policies apply correctly (users cannot access resources they don't own).
