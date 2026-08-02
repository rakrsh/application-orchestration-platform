import os

from app.storage import DatabaseAppStore
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="CapOS FastAPI Stub")
app_store = DatabaseAppStore(os.getenv("DATABASE_URL"))


@app.middleware("http")
async def auth_header_middleware(request: Request, call_next):
    user = request.headers.get("x-auth-request-user")
    roles = request.headers.get("x-auth-request-roles")
    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing X-Auth-Request-User header"},
        )
    request.state.user = user
    request.state.roles = (
        [r.strip() for r in roles.split(",")] if roles else []
    )
    return await call_next(request)


class AppIn(BaseModel):
    name: str
    description: str | None = None
    environment: str = "development"
    importType: str = "git"
    targetOs: str = "linux"
    detectedRuntime: str | None = None
    envVariables: dict[str, str] = Field(default_factory=dict)
    owner: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/apps")
async def list_apps(request: Request):
    return app_store.list_apps()


@app.get("/api/orchestration")
async def orchestration_payload(request: Request):
    applications = app_store.list_apps()
    if not applications:
        app_store.create_app(
            payload={
                "name": "E-Commerce Platform",
                "description": "Checkout workflow, catalog delivery, and payment orchestration.",
                "environment": "production",
                "importType": "git",
                "targetOs": "linux",
                "detectedRuntime": "Node.js 20",
                "envVariables": {"NODE_ENV": "production"},
            },
            owner=request.state.user,
        )
        applications = app_store.list_apps()
    return {
        "applications": applications,
        "nodes": [
            {
                "id": "node-linux-01",
                "name": "runner-linux-01",
                "os": "linux",
                "ip": "10.0.10.11",
                "cpuUsage": 58,
                "memoryUsage": 67,
                "status": "online",
                "agentVersion": "1.4.2",
            },
            {
                "id": "node-windows-01",
                "name": "runner-windows-01",
                "os": "windows",
                "ip": "10.0.10.22",
                "cpuUsage": 41,
                "memoryUsage": 53,
                "status": "degraded",
                "agentVersion": "1.4.2",
            },
        ],
        "metrics": {
            "activeNodesCount": 2,
            "totalCpuPercent": 99,
            "totalMemoryPercent": 120,
            "activeDeployments": 4,
            "globalErrorRate": 0.8,
            "p95LatencyMs": 195,
        },
    }


@app.post("/api/apps", status_code=201)
async def create_app(payload: AppIn, request: Request):
    roles = request.state.roles
    if not any(r in roles for r in ("admin", "editor")):
        raise HTTPException(status_code=403, detail="insufficient role")
    return app_store.create_app(
        payload=payload.model_dump() if hasattr(payload, "model_dump") else payload.dict(),
        owner=payload.owner or request.state.user,
    )
