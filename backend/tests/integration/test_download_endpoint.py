"""Integration tests for GET /api/v1/documents/{document_id}/download."""
from __future__ import annotations

import io
import uuid
from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from infrastructure.db.models import Base, DocumentModel
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from infrastructure.storage.local_file_storage import LocalFileStorage
from application.use_cases.download_document import DownloadDocumentUseCase
from domain.entities.user import User, UserRole
from presentation.dependencies import (
    get_download_document_use_case,
    require_admin,
    require_viewer_or_admin,
)
from main import app


def _dummy_admin():
    return User(id=uuid.uuid4(), email="a@a.com", hashed_password="x", role=UserRole.ADMIN, is_active=True)

EQUIPMENT_COLUMNS = (
    "id_equipo", "nombre_equipo", "numero_serie", "ubicacion", "subtipo",
    "tipo_mantenimiento", "empresa_mantenedora", "fecha_proximo_mantenimiento",
    "organismo_inspector", "resultado_inspeccion", "fecha_proxima_inspeccion",
)


def _create_test_engine():
    """Create a test engine with all columns including equipment fields."""
    engine = create_engine(
        "sqlite:///file::memory:?cache=shared",
        connect_args={"check_same_thread": False, "uri": True},
        isolation_level="AUTOCOMMIT",
    )
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        for col in EQUIPMENT_COLUMNS:
            try:
                conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
            except OperationalError:
                pass
    return engine


def _pdf_file(filename: str = "test.pdf"):
    return ("file", (filename, io.BytesIO(b"%PDF-1.4 test"), "application/pdf"))


def _form_data(**kwargs):
    defaults = {
        "nombre_archivo": "test_doc",
        "formato": "pdf",
        "fecha_validez": "2025-01-01",
        "fecha_caducidad": "2025-12-31",
    }
    defaults.update(kwargs)
    return defaults


class TestDownloadEndpoint:
    def test_download_success_returns_200_and_pdf(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return DownloadDocumentUseCase(repository=repo, storage=storage)

        app.dependency_overrides[get_download_document_use_case] = override_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin

        with TestClient(app) as client:
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))

            doc_id = uuid.uuid4()
            storage.save(doc_id, b"%PDF-1.4 test content")
            repo.save(
                type("Document", (), {
                    "id": doc_id,
                    "nombre_archivo": "mi_documento.pdf",
                    "formato": "pdf",
                    "fecha_validez": date(2025, 1, 1),
                    "fecha_caducidad": date(2025, 12, 31),
                    "categoria": None,
                    "uploaded_by": None,
                })()
            )

            resp = client.get(f"/api/v1/documents/{doc_id}/download")
            assert resp.status_code == 200
            assert resp.headers["content-type"] == "application/pdf"
            assert "attachment" in resp.headers["content-disposition"]
            assert "mi_documento.pdf" in resp.headers["content-disposition"]

        app.dependency_overrides.clear()

    def test_download_missing_id_returns_404(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return DownloadDocumentUseCase(repository=repo, storage=storage)

        app.dependency_overrides[get_download_document_use_case] = override_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin

        with TestClient(app) as client:
            fake_id = uuid.uuid4()
            resp = client.get(f"/api/v1/documents/{fake_id}/download")
            assert resp.status_code == 404

        app.dependency_overrides.clear()

    def test_download_deleted_document_returns_404(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return DownloadDocumentUseCase(repository=repo, storage=storage)

        app.dependency_overrides[get_download_document_use_case] = override_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin

        with TestClient(app) as client:
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))

            doc_id = uuid.uuid4()
            storage.save(doc_id, b"%PDF-1.4 test content")

            # Manually create a model with deleted_at set
            model = DocumentModel(
                id=doc_id,
                nombre_archivo="deleted_doc.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2025, 12, 31),
                categoria=None,
                uploaded_by=None,
                deleted_at=datetime.now(),
            )
            db.add(model)
            db.commit()

            resp = client.get(f"/api/v1/documents/{doc_id}/download")
            assert resp.status_code == 404

        app.dependency_overrides.clear()

    def test_download_non_uuid_returns_422(self) -> None:
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            resp = client.get("/api/v1/documents/not-a-uuid/download")
            assert resp.status_code == 422
        app.dependency_overrides.clear()
