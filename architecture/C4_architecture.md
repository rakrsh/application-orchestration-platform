# Application Orchestration Platform Architecture

## 1. Purpose and scope

The Application Orchestration Platform is a multi-tenant, multi-OS control plane for application lifecycle operations. It combines an Angular dashboard, a FastAPI backend, identity and authorization services, and deployment-mode aware workflows for Kubernetes, Docker Compose, and bare-metal/systemd environments.

### Core goals
- Provide a unified dashboard for applications, projects, nodes, telemetry, and creation flows.
- Support multiple personas: platform admin, developer, and auditor.
- Adapt the UI and backend semantics to deployment mode and operating system.
- Enforce role-aware actions and authorization policies for create, scale, redeploy, and audit use cases.

## 2. Overall architecture

```mermaid
flowchart LR
    User[Platform User]
    Proxy[oauth2-proxy]
    Web[Angular SPA]
    API[FastAPI Backend]
    Store[(PostgreSQL / SQLite for local)]
    Keycloak[Keycloak]
    OpenFGA[OpenFGA]

    User --> Proxy
    Proxy --> Web
    Web --> API
    API --> Store
    API --> Keycloak
    API --> OpenFGA
```

### Runtime responsibilities
- Frontend: dashboard state, persona selection, deployment-mode switching, wizard interactions.
- Backend: request validation, role checks, state retrieval, orchestration payload assembly, app lifecycle commands.
- Auth layer: identity, role propagation, and fine-grained authorization.
- Persistence: application/project metadata plus audit-trace friendly records.

## 3. System context

```mermaid
%%{init: {"securityLevel": "loose"}}%%
C4Context
    title AOP System Context
    Enterprise_Boundary(b0, "Organization Network") {
      Person(user, "Platform User", "Uses the orchestration dashboard")
      System(ke, "Keycloak", "Identity Provider")
      System(ofga, "OpenFGA", "Fine-grained authorization engine")
      System_Boundary(aop, "AOP") {
        System(web, "Angular SPA", "Frontend UI")
        System(api, "FastAPI Backend", "REST API and orchestration services")
        System(oauth2, "OAuth2 Proxy", "Ingress and header enforcement")
      }
    }
    Rel(user, oauth2, "HTTPS", "Authenticates with Keycloak")
    Rel(oauth2, web, "HTTP", "Forwards session context")
    Rel(web, api, "HTTP", "Dashboard API calls")
    Rel(api, ke, "REST", "User and role management")
    Rel(api, ofga, "HTTP/gRPC", "Policy checks and writes")
```

## 4. Container diagram

```mermaid
%%{init: {"securityLevel": "loose"}}%%
C4Container
    title AOP Container Diagram
    System_Boundary(aop, "AOP") {
      Container(web, "Angular SPA", "Angular", "Dashboard shell, filters, wizard, state management")
      Container(api, "FastAPI", "Python", "REST API, header parsing, orchestration payload assembly")
      Container(oauth2, "OAuth2 Proxy", "oauth2-proxy", "Session enforcement and header injection")
      Container(ke, "Keycloak", "Keycloak", "Identity and RBAC")
      Container(ofga, "OpenFGA", "OpenFGA", "Fine-grained authorization")
      Container(db, "PostgreSQL", "Postgres", "Application and project metadata")
    }
    Rel(web, oauth2, "HTTPS", "User sessions")
    Rel(oauth2, api, "HTTP", "Authenticated requests with forwarded headers")
    Rel(api, db, "SQL", "Reads and writes orchestration state")
    Rel(api, ofga, "HTTP", "Authorization checks")
    Rel(api, ke, "REST", "Provisioning and role sync")
```

## 5. Backend component view

```mermaid
flowchart TD
    MW[Auth Header Middleware]
    Routes[Route Handlers]
    Store[App Store / Repository]
    Policy[OpenFGA Client]
    Keycloak[Keycloak Admin Client]
    DB[(Database)]

    MW --> Routes
    Routes --> Store
    Routes --> Policy
    Routes --> Keycloak
    Store --> DB
```

### Component responsibilities
- Auth Header Middleware: injects user and roles from forwarded headers.
- Route Handlers: expose the dashboard APIs for applications, orchestration payloads, and creation flows.
- App Store: serializes and retrieves application data in a deployment-mode agnostic shape.
- Policy client: enforce persona and resource rules.
- Keycloak client: manage provisioning and role mapping when needed.

## 6. Frontend component map

```mermaid
flowchart TD
    App[App Root]
    State[OrchestrationStateService]
    Header[Header Component]
    Overview[Overview Tab]
    AppCard[Application Card]
    ProjectCard[Project Card]
    Slider[Replica Slider]
    Wizard[Create App Wizard]

    App --> State
    App --> Header
    App --> Overview
    App --> Wizard
    Overview --> AppCard
    AppCard --> ProjectCard
    ProjectCard --> Slider
```

## 7. Observability architecture

```mermaid
flowchart LR
    Web[Angular SPA] -->|trace event| API[FastAPI Backend]
    API -->|OTLP spans| Collector[OTLP Collector / backend]
    Collector -->|visualization| Observability[Grafana / Jaeger / Tempo]
```

The OpenTelemetry pipeline is intentionally lightweight: the backend auto-instruments FastAPI request handling and emits explicit spans for key app lifecycle operations, while the frontend emits a bootstrap span from the Angular shell. When `OTEL_EXPORTER_OTLP_ENDPOINT` is set, the backend exports spans to an OTLP HTTP receiver.

## 8. Sequence diagrams

### 7.1 Application creation via Git import

```mermaid
sequenceDiagram
    actor User
    participant Web as Angular SPA
    participant API as FastAPI
    participant Store as App Store
    participant Auth as OpenFGA/Keycloak

    User->>Web: Fill Git import form
    Web->>API: POST /api/apps {name, gitUrl, branch, targetOs}
    API->>Auth: Validate persona and permissions
    Auth-->>API: Allowed / Denied
    alt Allowed
        API->>Store: Create application record
        Store-->>API: Persisted app payload
        API-->>Web: 201 Created
        Web-->>User: Show success state
    else Denied
        API-->>Web: 403 Forbidden
        Web-->>User: Show access error
    end
```

### 7.2 ZIP upload and runtime detection

```mermaid
sequenceDiagram
    actor User
    participant Web as Angular SPA
    participant API as FastAPI
    participant Store as App Store

    User->>Web: Drop ZIP archive
    Web->>Web: Detect file metadata and runtime hints
    Web->>API: POST /api/apps {importType: zip, detectedRuntime, targetOs}
    API->>Store: Persist application metadata
    Store-->>API: Return created app
    API-->>Web: 201 Created
    Web-->>User: Show detected runtime and environment variables
```

### 7.3 Persona-based access control

```mermaid
sequenceDiagram
    actor User
    participant Web as Angular SPA
    participant API as FastAPI
    participant Auth as OpenFGA

    User->>Web: Select Developer or Auditor persona
    Web->>API: Request scaling or deployment-mode change
    API->>Auth: Evaluate action against persona
    Auth-->>API: Allow or deny
    API-->>Web: Restricted or permitted response
```

## 8. Class diagram for the core domain model

```mermaid
classDiagram
    class Application {
        +string id
        +string name
        +string description
        +string environment
        +HealthStatus status
        +string[] tags
        +ProjectService[] projects
        +string createdAt
    }

    class ProjectService {
        +string id
        +string name
        +string appId
        +OperatingSystem osTarget
        +string runtime
        +HealthStatus status
        +int replicas
        +int targetReplicas
        +float cpuLimitRatio
        +int memoryUsageMb
        +int latencyP95Ms
        +float errorRatePercent
        +string lastDeployedAt
    }

    class OSNode {
        +string id
        +string name
        +OperatingSystem os
        +string ip
        +int cpuUsage
        +int memoryUsage
        +string status
        +string agentVersion
    }

    class PlatformMetrics {
        +int activeNodesCount
        +int totalCpuPercent
        +int totalMemoryPercent
        +int activeDeployments
        +float globalErrorRate
        +int p95LatencyMs
    }

    class AppCreationPayload {
        +string name
        +string description
        +string environment
        +string importType
        +string gitUrl
        +string gitBranch
        +string buildfilePath
        +File zipFile
        +OperatingSystem targetOs
        +string detectedRuntime
        +Record envVariables
    }

    class AppStore {
        +list_apps()
        +create_app(payload)
    }

    Application "1" --> "0..*" ProjectService
    AppStore --> Application
```

## 9. Deployment-mode aware flow

```mermaid
flowchart TD
    Mode[Deployment Mode Selector]
    K8s[Kubernetes Mode]
    Docker[Docker Compose Mode]
    Bare[Bare Metal Mode]

    Mode --> K8s
    Mode --> Docker
    Mode --> Bare

    K8s -->|UI labels| Pods[Pods / ReplicaSets / Ingress]
    Docker -->|UI labels| Containers[Containers / Compose stacks / Volumes]
    Bare -->|UI labels| Services[Systemd units / daemons / sockets]
```

## 10. Request flow and state transitions

```mermaid
flowchart TD
    A[Incoming Request]
    B[Middleware parses auth headers]
    C{User present?}
    D{Has required role?}
    E[Route handler]
    F[Persist / update state]
    G[Return payload]
    H[401 or 403 error]

    A --> B --> C
    C -->|No| H
    C -->|Yes| D
    D -->|No| H
    D -->|Yes| E --> F --> G
```

## 11. Edge cases and failure scenarios

### 11.1 Authentication and authorization
- Missing authentication headers should return 401 and block the request before state mutation.
- Unsupported persona or insufficient role should return 403 and keep the UI in a read-only mode.
- Auditor persona should be prevented from changing deployment mode, scaling replicas, or editing secrets.

### 11.2 Creation flows
- Invalid Git URL or missing branch should fail validation and show targeted errors.
- ZIP uploads that are empty, malformed, or too large should be rejected with a clear message.
- Runtime detection should fall back to a generic runtime label when auto-detection fails.

### 11.3 Runtime and deployment health
- Offline or degraded nodes should be displayed with the correct status and reduce confidence in deployment health.
- Scaling requests that exceed safe bounds should be capped or flagged for review.
- Failed deployments should preserve the last known healthy state and expose rollback guidance.

### 11.4 Persistence and data consistency
- If the database is unavailable, the system should return an explicit service error rather than silently succeeding.
- Partial or stale data from upstream metrics should not overwrite the last known healthy state without a reconciliation step.
- Application records should remain traceable with timestamps and ownership metadata.

## 12. Design notes for future implementation
- Separate API routes, domain services, and persistence concerns to avoid mixing UI state with business logic.
- Keep the orchestration payload shape stable so the frontend and backend evolve independently.
- Extend authorization checks in one place rather than scattering role conditions throughout route handlers.
- Treat deployment-mode terminology as a presentation concern to support Kubernetes, Docker Compose, and bare-metal modes from the same domain model.
