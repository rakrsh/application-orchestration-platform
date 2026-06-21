# Application Orchestration Platform Architecture (C4-style)

## System Context

```mermaid
%%{init: {"securityLevel": "loose"}}%%
C4Context
    title AOP System Context
    Enterprise_Boundary(b0, "Organization Network") {
      Person(user, "Platform User", "Uses the AOP dashboard to manage applications and projects")
      System(ke, "Keycloak", "Identity Provider")
      System(ofga, "OpenFGA", "Fine-grained authorization engine")
      System_Boundary(aop, "AOP") {
        System(web, "Angular SPA", "Frontend UI")
        System(api, "FastAPI Backend", "REST API and orchestration")
        System(oauth2, "OAuth2 Proxy", "Ingress and session enforcement")
      }
    }
    Rel(user, oauth2, "HTTPS", "Authenticates via Keycloak cookie")
    Rel(oauth2, web, "HTTP (internal)", "Forwards headers and traffic")
    Rel(web, api, "HTTP", "API calls via internal network")
    Rel(api, ke, "REST", "Keycloak Admin API for user provisioning")
    Rel(api, ofga, "gRPC/HTTP", "OpenFGA policy checks and tuple writes")
```

## Container Diagram

```mermaid
%%{init: {"securityLevel": "loose"}}%%
C4Container
    title AOP Container Diagram
    System_Boundary(aop, "AOP") {
      Container(web, "Angular SPA", "Angular 17+", "User interface and client routing")
      Container(api, "FastAPI", "Python (FastAPI)", "Stateless API, header ingestion, ReBAC checks")
      Container(oauth2, "OAuth2 Proxy", "oauth2-proxy", "Session enforcement and header injection")
      Container(ke, "Keycloak", "Keycloak", "Global RBAC and authentication")
      Container(ofga, "OpenFGA", "OpenFGA", "Fine-grained authorization engine")
      Container(db, "PostgreSQL", "Postgres", "Primary persistence")
    }
    Rel(web, oauth2, "HTTPS", "User sessions")
    Rel(oauth2, api, "HTTP", "Forwards authenticated requests with headers")
    Rel(api, db, "JDBC/SQL", "Reads/Writes application and project data")
    Rel(api, ofga, "gRPC/HTTP", "Policy checks and tuple writes")
    Rel(api, ke, "REST", "Admin provisioning calls")
```

## Component Diagram (API)

```mermaid
%%{init: {"securityLevel": "loose"}}%%
C4Component
    title FastAPI Components
    Container(api, "FastAPI", "Python", "Backend") {
      Component(mw, "Auth Header Middleware", "Middleware", "Parses `X-Auth-Request-*` headers and attaches identity to request")
      Component(appsrv, "Application Service", "Service", "CRUD operations and business logic for applications")
      Component(projectsrv, "Project Service", "Service", "Flattened project query and project-level actions")
      Component(authz, "OpenFGA Client", "Client", "Policy checks and tuple writes")
      Component(keyadmin, "Keycloak Admin Client", "Client", "User provisioning and role assignment")
    }
    Rel(api.mw, appsrv, "passes identity")
    Rel(appsrv, authz, "check/write")
    Rel(appsrv, db, "persist")
    Rel(keyadmin, ke, "calls")
```

## Notes
- The diagrams use C4-style notation in Mermaid blocks. If your renderer does not support `C4Context/C4Container/C4Component`, you can render as standard flowcharts or use external C4 tooling.
- Keep OpenFGA model and tuple migrations alongside these diagrams.
