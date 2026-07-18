import os
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


class AppRecord(Base):
    __tablename__ = "apps"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class InMemoryAppStore:
    def __init__(self) -> None:
        self._apps: List[dict] = []

    def list_apps(self) -> List[dict]:
        return [dict(app) for app in self._apps]

    def create_app(
        self,
        name: str,
        description: Optional[str],
        owner: str,
    ) -> dict:
        app = {
            "id": f"app-{len(self._apps) + 1}",
            "name": name,
            "description": description,
            "owner": owner,
        }
        self._apps.append(app)
        return dict(app)


class DatabaseAppStore:
    def __init__(self, database_url: Optional[str] = None) -> None:
        self.database_url = (
            database_url
            or os.getenv(
                "DATABASE_URL",
                "postgresql://appuser:apppass@postgres:5432/appdb",
            )
        )
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def _session(self) -> Session:
        return self.session_factory()

    def list_apps(self) -> List[dict]:
        with self._session() as session:
            rows = (
                session.query(AppRecord)
                .order_by(AppRecord.created_at.asc())
                .all()
            )
            return [
                {
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "owner": row.owner,
                }
                for row in rows
            ]

    def create_app(
        self,
        name: str,
        description: Optional[str],
        owner: str,
    ) -> dict:
        with self._session() as session:
            record = AppRecord(
                id=f"app-{int(datetime.utcnow().timestamp() * 1000)}",
                name=name,
                description=description,
                owner=owner,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return {
                "id": record.id,
                "name": record.name,
                "description": record.description,
                "owner": record.owner,
            }
