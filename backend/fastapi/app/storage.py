import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


class AppRecord(Base):
    __tablename__ = "apps"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner = Column(String, nullable=False)
    environment = Column(String, nullable=False, default="development")
    import_type = Column(String, nullable=True)
    target_os = Column(String, nullable=True)
    detected_runtime = Column(String, nullable=True)
    env_variables = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="provisioning")
    tags = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class InMemoryAppStore:
    def __init__(self) -> None:
        self._apps: List[dict] = []

    def _clone_app(self, app: Dict[str, Any]) -> Dict[str, Any]:
        return dict(app)

    def _build_app(
        self,
        payload: Optional[Dict[str, Any]] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        data = dict(payload or {})
        data.update(kwargs)
        env = data.get("environment") or "development"
        target_os = data.get("targetOs") or data.get("target_os") or "linux"
        import_type = data.get("importType") or data.get("import_type") or "git"
        detected_runtime = data.get("detectedRuntime") or data.get("detected_runtime")
        env_variables = data.get("envVariables") or data.get("env_variables") or {}
        tags = data.get("tags") or [target_os]
        created_at = data.get("createdAt") or datetime.now(timezone.utc).isoformat()
        return {
            "id": data.get("id") or f"app-{len(self._apps) + 1}",
            "name": data.get("name") or name or "sample-app",
            "description": data.get("description") or description,
            "environment": env,
            "status": data.get("status") or "provisioning",
            "importType": import_type,
            "targetOs": target_os,
            "detectedRuntime": detected_runtime,
            "envVariables": dict(env_variables),
            "tags": list(tags),
            "createdAt": created_at,
            "owner": data.get("owner") or owner or "system",
            "projects": data.get("projects") or [],
        }

    def list_applications(self) -> List[dict]:
        return [self._clone_app(app) for app in self._apps]

    def list_apps(self) -> List[dict]:
        return self.list_applications()

    def create_app(
        self,
        payload: Optional[Dict[str, Any]] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        **kwargs: Any,
    ) -> dict:
        app = self._build_app(
            payload,
            name=name,
            description=description,
            owner=owner,
            **kwargs,
        )
        self._apps.append(app)
        return self._clone_app(app)


class DatabaseAppStore:
    def __init__(self, database_url: Optional[str] = None) -> None:
        self.database_url = (
            database_url
            or os.getenv(
                "DATABASE_URL",
                "postgresql://appuser:apppass@postgres:5432/appdb",
            )
        )
        if self.database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
            if ":memory:" in self.database_url:
                connect_args["check_same_thread"] = False
            self.engine = create_engine(
                self.database_url,
                connect_args=connect_args,
                poolclass=StaticPool,
            )
        else:
            self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def _session(self) -> Session:
        return self.session_factory()

    def _row_to_app(self, row: AppRecord) -> dict:
        env_variables = {}
        if row.env_variables:
            env_variables = {
                item.split("=", 1)[0]: item.split("=", 1)[1]
                for item in row.env_variables.split("|")
                if "=" in item
            }
        return {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "environment": row.environment,
            "status": row.status,
            "importType": row.import_type,
            "targetOs": row.target_os,
            "detectedRuntime": row.detected_runtime,
            "envVariables": env_variables,
            "tags": [row.target_os] if row.target_os else [],
            "createdAt": row.created_at.isoformat() if row.created_at else None,
            "owner": row.owner,
            "projects": [],
        }

    def list_applications(self) -> List[dict]:
        with self._session() as session:
            rows = (
                session.query(AppRecord)
                .order_by(AppRecord.created_at.asc())
                .all()
            )
            return [self._row_to_app(row) for row in rows]

    def list_apps(self) -> List[dict]:
        return self.list_applications()

    def create_app(
        self,
        payload: Optional[Dict[str, Any]] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        **kwargs: Any,
    ) -> dict:
        data = dict(payload or {})
        data.update(kwargs)
        env = data.get("environment") or "development"
        target_os = data.get("targetOs") or data.get("target_os") or "linux"
        import_type = data.get("importType") or data.get("import_type") or "git"
        detected_runtime = data.get("detectedRuntime") or data.get("detected_runtime")
        env_variables = data.get("envVariables") or data.get("env_variables") or {}
        with self._session() as session:
            record = AppRecord(
                id=f"app-{int(datetime.utcnow().timestamp() * 1000)}",
                name=data.get("name") or name or "sample-app",
                description=data.get("description") or description,
                owner=data.get("owner") or owner or "system",
                environment=env,
                import_type=import_type,
                target_os=target_os,
                detected_runtime=detected_runtime,
                env_variables="|".join(
                    f"{key}={value}" for key, value in env_variables.items()
                ),
                status=data.get("status") or "provisioning",
                tags=",".join([target_os]),
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return self._row_to_app(record)
