# Keycloak (Quickstart Notes)

This file contains quickstart notes for running Keycloak locally for CapOS development. The repository includes a `docker-compose.yml` that launches a dev Keycloak instance on port `8080` (admin/admin).

Access Keycloak Admin Console: http://localhost:8080

Notes:
- For production, configure Keycloak in HA mode and secure admin credentials in a secrets manager.
- Create a realm and client for OAuth2 Proxy and the SPA; configure redirect URIs accordingly.
