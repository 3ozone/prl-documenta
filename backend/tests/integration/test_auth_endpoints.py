"""Integration tests for auth endpoints."""
from __future__ import annotations

import io
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from application.use_cases.download_document import DownloadDocumentUseCase
from application.use_cases.upload_document import UploadDocumentUseCase
from infrastructure.db.models import Base
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from infrastructure.storage.local_file_storage import LocalFileStorage
from main import app
from presentation.dependencies import (
    get_db,
    get_download_document_use_case,
    get_upload_document_use_case,
)

EQUIPMENT_COLUMNS = (
    "id_equipo", "nombre_equipo", "numero_serie", "ubicacion", "subtipo",
    "tipo_mantenimiento", "empresa_mantenedora", "fecha_proximo_mantenimiento",
    "organismo_inspector", "resultado_inspeccion", "fecha_proxima_inspeccion",
)

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _add_equipment_columns(conn):
    for col in EQUIPMENT_COLUMNS:
        try:
            conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
        except OperationalError:
            pass


@pytest.fixture
def auth_client(tmp_path):
    """Client with real auth deps (no override for require_admin/require_viewer_or_admin)."""
    db_file = tmp_path / "auth_test.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        _add_equipment_columns(conn)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

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

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
    app.dependency_overrides[get_download_document_use_case] = override_download_use_case
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _register_and_login(client: TestClient, email: str, password: str, role: str = "viewer", admin_token: str | None = None) -> str:
    headers = {"Authorization": f"Bearer {admin_token}"} if admin_token else {}
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "role": role},
        headers=headers,
    )
    assert resp.status_code in (201, 409), f"Register failed: {resp.text}"
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    return login_resp.json()["access_token"]


def test_register_returns_201(auth_client):
    resp = auth_client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@test.com", "password": "pass", "role": "viewer"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "newuser@test.com"
    assert body["role"] == "viewer"


def test_register_duplicate_returns_409(auth_client):
    auth_client.post(
        "/api/v1/auth/register",
        json={"email": "dup@test.com", "password": "pass", "role": "viewer"},
    )
    resp = auth_client.post(
        "/api/v1/auth/register",
        json={"email": "dup@test.com", "password": "pass2", "role": "viewer"},
    )
    assert resp.status_code == 409


def test_login_returns_token(auth_client):
    auth_client.post(
        "/api/v1/auth/register",
        json={"email": "loginuser@test.com", "password": "secret", "role": "viewer"},
    )
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "loginuser@test.com", "password": "secret"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password_returns_401(auth_client):
    auth_client.post(
        "/api/v1/auth/register",
        json={"email": "wp@test.com", "password": "correct", "role": "viewer"},
    )
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "wp@test.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_protected_endpoint_without_token_returns_401(auth_client):
    resp = auth_client.get("/api/v1/alerts")
    assert resp.status_code == 401


def test_protected_endpoint_with_expired_token_returns_401(auth_client):
    payload = {
        "sub": "user@test.com",
        "role": "viewer",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
    }
    expired_token = jwt.encode(payload, "dev-secret-change-me", algorithm="HS256")
    resp = auth_client.get(
        "/api/v1/alerts",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert resp.status_code == 401


def test_viewer_cannot_upload_returns_403(auth_client):
    # Get admin token (bootstrap creates admin@prl.local)
    login_resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@prl.local", "password": "admin123"},
    )
    assert login_resp.status_code == 200
    admin_token = login_resp.json()["access_token"]

    viewer_token = _register_and_login(auth_client, "viewer2@test.com", "pass", "viewer", admin_token=None)

    resp = auth_client.post(
        "/api/v1/documents",
        data={
            "nombre_archivo": "test_doc",
            "formato": "pdf",
            "fecha_validez": "2025-01-01",
            "fecha_caducidad": "2025-12-31",
        },
        files=[("file", ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf"))],
        headers={"Authorization": f"Bearer {viewer_token}"},
    )
    assert resp.status_code == 403


def test_viewer_can_download_returns_200(auth_client, tmp_path):
    """Viewer can download: first upload as admin then download as viewer."""
    login_resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@prl.local", "password": "admin123"},
    )
    assert login_resp.status_code == 200
    admin_token = login_resp.json()["access_token"]

    # Upload as admin
    upload_resp = auth_client.post(
        "/api/v1/documents",
        data={
            "nombre_archivo": "test_doc",
            "formato": "pdf",
            "fecha_validez": "2025-01-01",
            "fecha_caducidad": "2025-12-31",
        },
        files=[("file", ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf"))],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert upload_resp.status_code == 201
    doc_id = upload_resp.json()["id"]

    # Download as viewer
    viewer_token = _register_and_login(auth_client, "dl_viewer@test.com", "pass")
    resp = auth_client.get(
        f"/api/v1/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {viewer_token}"},
    )
    assert resp.status_code == 200


def test_admin_can_upload_returns_201(auth_client):
    login_resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@prl.local", "password": "admin123"},
    )
    assert login_resp.status_code == 200
    admin_token = login_resp.json()["access_token"]

    resp = auth_client.post(
        "/api/v1/documents",
        data={
            "nombre_archivo": "admin_doc",
            "formato": "pdf",
            "fecha_validez": "2025-01-01",
            "fecha_caducidad": "2025-12-31",
        },
        files=[("file", ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf"))],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 201
