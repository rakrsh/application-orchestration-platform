import os

from app.storage import DatabaseAppStore
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
    description: str = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/apps")
async def list_apps(request: Request):
    return app_store.list_apps()


@app.post("/api/apps", status_code=201)
async def create_app(payload: AppIn, request: Request):
    roles = request.state.roles
    if not any(r in roles for r in ("admin", "editor")):
        raise HTTPException(status_code=403, detail="insufficient role")
    return app_store.create_app(
        name=payload.name,
        description=payload.description,
        owner=request.state.user,
    )
