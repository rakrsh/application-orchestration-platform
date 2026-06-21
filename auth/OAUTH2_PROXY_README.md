# OAuth2 Proxy (Quickstart Notes)

The `docker-compose.yml` includes a minimal `oauth2-proxy` service used to demonstrate header injection. The example uses environment variables and placeholder client secrets — replace these values for any real testing.

Configure `OAUTH2_PROXY_OIDC_ISSUER_URL` to point at Keycloak (e.g., `http://keycloak:8080`).
