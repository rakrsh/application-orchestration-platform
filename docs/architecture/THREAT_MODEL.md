# Threat Model (STRIDE)

## 1. Overview
This document describes the threat model for the Application Orchestration Platform. It uses the STRIDE methodology to identify threats and document mitigating controls.

## 2. Architecture Context
The platform consists of:
- **Frontend (Angular):** User dashboard for managing applications.
- **Backend (FastAPI):** Core API handling business logic and storage.
- **Keycloak:** Identity Provider (IdP).
- **OpenFGA:** Fine-Grained Authorization engine.

## 3. STRIDE Analysis

| Threat | Description | Mitigating Control |
|---|---|---|
| **Spoofing** | An attacker impersonates a valid user. | OAuth2 + OIDC via Keycloak. Header-based auth validated by proxy. |
| **Tampering** | Data is modified in transit or at rest. | HTTPS/TLS required for all communication. Internal services use secure channels. |
| **Repudiation** | A user denies performing an action (e.g., scaling an app). | Comprehensive Audit Logging (Phase 2) will record user actions, timestamps, and IP addresses. |
| **Information Disclosure** | Sensitive data (secrets, tokens) is exposed. | No hardcoded secrets. Proper `.dockerignore` and `.gitignore`. |
| **Denial of Service** | An attacker overwhelms the backend API. | Rate limiting at the ingress/API gateway layer. |
| **Elevation of Privilege** | A user gains unauthorized access to resources. | OpenFGA evaluates all access requests against formal policies. Least privilege defaults. |
