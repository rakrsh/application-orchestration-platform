---
name: cra-compliance
description: Guides the agent on implementing and maintaining EU Cybersecurity Resilience Act (CRA) compliance measures based on COMPLIANCE_CRA_PLAN.md.
---

# CRA Compliance Skill

This skill provides instructions for achieving and maintaining compliance with the EU Cybersecurity Resilience Act (CRA).

## Context
The platform must adhere to the EU CRA requirements outlined in `docs/COMPLIANCE_CRA_PLAN.md`.

## Execution Workflow
When tasked with implementing CRA compliance, break the work into the defined phases. Start with Phase 1 (Foundation):

1.  **Phase 1: Foundation (Weeks 1-6)**
    *   **SSDLC:** Ensure security requirements, threat models (C4/STRIDE), and secure coding guidelines are documented in the `docs/` folder.
    *   **Security Testing:** Use `pytest` for backend testing. Implement SAST (Semgrep, Bandit), dependency scanning, and container scanning in GitHub Actions (`.github/workflows/`). Ensure 80% coverage.
    *   **SBOM:** Generate SBOMs in CycloneDX format during releases. Ensure dependency lock files exist (`requirements.lock`, `package-lock.json`).
    *   **Vulnerability Management:** Establish a security contact (`.well-known/security.txt`), incident response plans, and a disclosure policy.

2.  **Phase 2 & 3**
    *   Address audit logging, secrets management, and access controls in subsequent steps.

## Specific Instructions
- When creating documentation, refer to the expected deliverables in `COMPLIANCE_CRA_PLAN.md`.
- When modifying tests, migrate from `unittest` to `pytest` and use `pytest-cov`.
- Create GitHub Actions using standard open-source security tools (Semgrep, Trivy, Dependabot, etc.).
