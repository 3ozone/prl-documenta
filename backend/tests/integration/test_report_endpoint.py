"""Integration tests for GET /api/v1/reports/status."""
from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from domain.entities.user import User, UserRole
from infrastructure.db.models import Base, DocumentModel
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from infrastructure.storage.local_file_storage import LocalFileStorage
from application.use_cases.upload_document import UploadDocumentUseCase
from application.use_cases.generate_report import GenerateReportUseCase
from presentation.dependencies import (
    get_upload_document_use_case,
    get_generate_report_use_case,
    require_admin,
    require_viewer_or_admin,
)
from main import app

EQUIPMENT_COLUMNS = (
    "id_equipo", "nombre_equipo", "numero_serie", "ubicacion", "subtipo",
    "tipo_mantenimiento", "empresa_mantenedora", "fecha_proximo_mantenimiento",
    "organismo_inspector", "resultado_inspeccion", "fecha_proxima_inspeccion",
)


def _dummy_admin():
    return User(id=uuid.uuid4(), email="a@a.com", hashed_password="x", role=UserRole.ADMIN, is_active=True)


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


class TestReportEndpoint:
    def test_report_csv_returns_200_content_type_csv(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_upload_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return UploadDocumentUseCase(repository=repo, storage=storage)

        def override_generate_report_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            return GenerateReportUseCase(repository=repo)

        app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
        app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            response = client.get("/api/v1/reports/status?formato=csv")
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/csv; charset=utf-8"
            assert "attachment" in response.headers["content-disposition"]
            assert "informe_estado_" in response.headers["content-disposition"]
            assert response.headers["content-disposition"].endswith('.csv"')
        app.dependency_overrides.clear()

    def test_report_pdf_returns_200_content_type_pdf(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_upload_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return UploadDocumentUseCase(repository=repo, storage=storage)

        def override_generate_report_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            return GenerateReportUseCase(repository=repo)

        app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
        app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            response = client.get("/api/v1/reports/status?formato=pdf")
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/pdf"
            assert response.content.startswith(b"%PDF")
        app.dependency_overrides.clear()

    def test_report_invalid_format_returns_400(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_upload_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return UploadDocumentUseCase(repository=repo, storage=storage)

        def override_generate_report_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            return GenerateReportUseCase(repository=repo)

        app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
        app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            response = client.get("/api/v1/reports/status?formato=xml")
            assert response.status_code == 400
            assert "no soportado" in response.json()["detail"]
            assert "csv" in response.json()["detail"]
            assert "pdf" in response.json()["detail"]
        app.dependency_overrides.clear()

    def test_report_csv_excludes_deleted_documents(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_upload_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return UploadDocumentUseCase(repository=repo, storage=storage)

        def override_generate_report_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            return GenerateReportUseCase(repository=repo)

        app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
        app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            db = TestingSessionLocal()
            storage = LocalFileStorage(storage_root=str(tmp_path))

            # Active document
            active_id = uuid4()
            storage.save(active_id, b"%PDF-1.4 content")
            db.add(
                DocumentModel(
                    id=active_id,
                    nombre_archivo="active_doc.pdf",
                    formato="pdf",
                    fecha_validez=date.today(),
                    fecha_caducidad=date.today() + timedelta(days=31),
                    categoria="empresa",
                    deleted_at=None,
                )
            )

            # Deleted document
            deleted_id = uuid4()
            storage.save(deleted_id, b"%PDF-1.4 content")
            db.add(
                DocumentModel(
                    id=deleted_id,
                    nombre_archivo="deleted_doc.pdf",
                    formato="pdf",
                    fecha_validez=date.today(),
                    fecha_caducidad=date.today() + timedelta(days=31),
                    categoria="empresa",
                    deleted_at=datetime.now(timezone.utc),
                )
            )
            db.commit()

            response = client.get("/api/v1/reports/status?formato=csv")
            assert response.status_code == 200
            content = response.content.decode("utf-8")
            assert "active_doc.pdf" in content
            assert "deleted_doc.pdf" not in content
        app.dependency_overrides.clear()

    def test_report_csv_filters_by_category(self, tmp_path) -> None:
        engine = _create_test_engine()
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_upload_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            storage = LocalFileStorage(storage_root=str(tmp_path))
            return UploadDocumentUseCase(repository=repo, storage=storage)

        def override_generate_report_use_case():
            db = TestingSessionLocal()
            repo = SqlDocumentRepository(db)
            return GenerateReportUseCase(repository=repo)

        app.dependency_overrides[get_upload_document_use_case] = override_upload_use_case
        app.dependency_overrides[get_generate_report_use_case] = override_generate_report_use_case
        app.dependency_overrides[require_admin] = _dummy_admin
        app.dependency_overrides[require_viewer_or_admin] = _dummy_admin
        with TestClient(app) as client:
            db = TestingSessionLocal()
            storage = LocalFileStorage(storage_root=str(tmp_path))

            # Insert empresa document
            doc_empresa_id = uuid4()
            storage.save(doc_empresa_id, b"%PDF-1.4 content")
            db.add(
                DocumentModel(
                    id=doc_empresa_id,
                    nombre_archivo="empresa_doc.pdf",
                    formato="pdf",
                    fecha_validez=date.today(),
                    fecha_caducidad=date.today() + timedelta(days=31),
                    categoria="empresa",
                    deleted_at=None,
                )
            )

            # Insert trabajadores document
            doc_trabajadores_id = uuid4()
            storage.save(doc_trabajadores_id, b"%PDF-1.4 content")
            db.add(
                DocumentModel(
                    id=doc_trabajadores_id,
                    nombre_archivo="trabajadores_doc.pdf",
                    formato="pdf",
                    fecha_validez=date.today(),
                    fecha_caducidad=date.today() + timedelta(days=31),
                    categoria="trabajadores",
                    deleted_at=None,
                )
            )
            db.commit()

            response = client.get("/api/v1/reports/status?formato=csv&categoria=empresa")
            assert response.status_code == 200
            content = response.content.decode("utf-8")
            assert "empresa_doc.pdf" in content
            assert "trabajadores_doc.pdf" not in content
        app.dependency_overrides.clear()
