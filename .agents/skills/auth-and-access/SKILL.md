---
name: auth-and-access
description: Work with Keycloak, OAuth2 Proxy, OpenFGA, and header-based auth flow for local and platform-integrated access control.
---

# Authentication and Access Control

Use this skill when changing identity, role handling, header injection, authorization policy, or local auth integration for the platform.

## Repository context

- Keycloak notes: [auth/KEYCLOAK_README.md](../../auth/KEYCLOAK_README.md)
- OAuth2 Proxy notes: [auth/OAUTH2_PROXY_README.md](../../auth/OAUTH2_PROXY_README.md)
- OpenFGA notes: [auth/OPENFGA_README.md](../../auth/OPENFGA_README.md)
- Backend auth expectations: [backend/fastapi/app/main.py](../../backend/fastapi/app/main.py)
- Docker-based local stack: [docker-compose.yml](../../docker-compose.yml)

## What this repository currently assumes

- Authentication is not implemented as a full end-to-end login flow in the FastAPI app itself.
- The backend expects upstream identity information through request headers, especially:
  - `x-auth-request-user`
  - `x-auth-request-roles`
- The local demo stack includes Keycloak and OAuth2 Proxy as reference services for header injection and identity integration.
- OpenFGA is documented as a future or reference authorization policy layer.

## Change guidance

- When altering access control, keep the behavior explicit and easy to audit.
- Preserve the current rule that create-app operations require a role in `admin` or `editor`.
- If a change adds new roles or permissions, document how the backend reads them from headers and how the UI should reflect that state.
- For real deployments, do not rely on placeholder secrets or demo credentials; replace them with secure values and proper realm/client configuration.

## Recommended workflow

1. Review the relevant auth documentation before editing behavior.
2. Verify the expected headers and role values in the FastAPI middleware and route handlers.
3. Update the backend tests to cover missing headers, missing roles, and valid role scenarios.
4. If the change touches integration services, update the corresponding docs under [auth](../../auth) and the architecture notes.

## Local development notes

- Keycloak is available in the local stack and is intended for demo or development testing.
- OAuth2 Proxy should be treated as an example of header injection; it is not a substitute for a production-ready identity gateway.
- OpenFGA is still a reference integration point; avoid assuming it is fully wired into runtime behavior unless the code and docs are updated together.

## Validation checklist

- Missing user header returns an auth error.
- Valid user header populates request state correctly.
- Role lists are parsed consistently.
- New auth semantics are reflected in architecture and documentation updates.
