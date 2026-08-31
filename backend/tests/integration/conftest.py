"""Conftest for integration tests."""
from __future__ import annotations

import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from domain.entities.user import User, UserRole
from infrastructure.db.models import Base
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from infrastructure.db.repositories.user_repository import SqlUserRepository
from infrastructure.storage.local_file_storage import LocalFileStorage
from application.use_cases.upload_document import UploadDocumentUseCase
from application.use_cases.download_document import DownloadDocumentUseCase
from application.use_cases.generate_report import GenerateReportUseCase
from presentation.dependencies import (
    get_upload_document_use_case,
    get_download_document_use_case,
    get_generate_report_use_case,
    require_admin,
    require_viewer_or_admin,
    get_db,
)
from main import app

EQUIPMENT_COLUMNS = (
    "id_equipo", "nombre_equipo", "numero_serie", "ubicacion", "subtipo",
    "tipo_mantenimiento", "empresa_mantenedora", "fecha_proximo_mantenimiento",
    "organismo_inspector", "resultado_inspeccion", "fecha_proxima_inspeccion",
)

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _make_dummy_admin():
    return User(
        id=uuid.uuid4(),
        email="admin@test.local",
        hashed_password=_pwd_ctx.hash("admin123"),
        role=UserRole.ADMIN,
        is_active=True,
    )


def _make_dummy_viewer():
    return User(
        id=uuid.uuid4(),
        email="viewer@test.local",
        hashed_password=_pwd_ctx.hash("viewer123"),
        role=UserRole.VIEWER,
        is_active=True,
    )


def _add_equipment_columns(conn):
    """Add equipment columns to the documents table if they don't exist."""
    for col in EQUIPMENT_COLUMNS:
        try:
            conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
        except OperationalError:
            pass  # column already exists


@pytest.fixture
def engine_with_columns(tmp_path):
    """Create a test engine with all document columns including equipment fields."""
    engine = create_engine(
        "sqlite:///file::memory:?cache=shared",
        connect_args={"check_same_thread": False, "uri": True},
        isolation_level="AUTOCOMMIT",
    )
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        _add_equipment_columns(conn)
    return engine


@pytest.fixture
def client(tmp_path):
    engine = create_engine(
        "sqlite:///file::memory:?cache=shared",
        connect_args={"check_same_thread": False, "uri": True},
        isolation_level="AUTOCOMMIT",
    )
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        _add_equipment_columns(conn)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_upload_use_case():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        storage = LocalFileStorage(storage_root=str(tmp_path))
        return UploadDocumentUseCase(repository=repo, storage=storage)

    def override_download_use_case():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        storage = LocalFileStorage(storage_root=str(tmp_path))
        return DownloadDocumentUseCase(repository=repo, storage=storage)

    def override_generate_report_use_case():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        return GenerateReportUseCase(repository=repo)

    def override_require_admin():
        return _make_dummy_admin()

    def override_require_viewer_or_admin():
        return _make_dummy_admin()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
    app.dependency_overrides[get_download_document_use_case] = override_download_use_case
    app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
    app.dependency_overrides[require_admin] = override_require_admin
    app.dependency_overrides[require_viewer_or_admin] = override_require_viewer_or_admin
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_admin_headers(client):
    """Create admin user and return auth headers."""
    # Register admin via POST /api/v1/auth/register (bypass auth for registration)
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "test_admin@prl.local", "password": "admin_pass", "role": "admin"},
    )
    # May already exist from lifespan; if 409 try login
    if resp.status_code not in (201, 409):
        raise RuntimeError(f"Unexpected register response: {resp.status_code} {resp.text}")

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@prl.local", "password": "admin123"},
    )
    if login_resp.status_code != 200:
        # Try the test admin
        login_resp = client.post(
            "/api/v1/auth/login",
            json={"email": "test_admin@prl.local", "password": "admin_pass"},
        )
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_viewer_headers(client):
    """Create viewer user and return auth headers."""
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "test_viewer@prl.local", "password": "viewer_pass", "role": "viewer"},
    )
    if resp.status_code not in (201, 409):
        raise RuntimeError(f"Unexpected register response: {resp.status_code} {resp.text}")

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "test_viewer@prl.local", "password": "viewer_pass"},
    )
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
