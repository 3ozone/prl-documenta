"""Integration tests for GET /api/v1/alerts endpoint."""
from __future__ import annotations

import uuid
from datetime import date, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from domain.entities.user import User, UserRole
from infrastructure.db.models import Base
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from application.use_cases.check_expiry import CheckExpiryUseCase
from application.use_cases.upload_document import UploadDocumentUseCase
from application.use_cases.download_document import DownloadDocumentUseCase
from application.use_cases.generate_report import GenerateReportUseCase
from infrastructure.storage.local_file_storage import LocalFileStorage
from presentation.dependencies import (
    get_upload_document_use_case,
    get_download_document_use_case,
    get_generate_report_use_case,
    get_check_expiry_use_case,
    require_viewer_or_admin,
    require_admin,
)
from main import app

EQUIPMENT_COLUMNS = (
    "id_equipo", "nombre_equipo", "numero_serie", "ubicacion", "subtipo",
    "tipo_mantenimiento", "empresa_mantenedora", "fecha_proximo_mantenimiento",
    "organismo_inspector", "resultado_inspeccion", "fecha_proxima_inspeccion",
)


def _add_equipment_columns(conn):
    for col in EQUIPMENT_COLUMNS:
        try:
            conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
        except OperationalError:
            pass


@pytest.fixture
def alerts_client(tmp_path):
    engine = create_engine(
        "sqlite:///file:alertstest?mode=memory&cache=shared&uri=true",
        connect_args={"check_same_thread": False, "uri": True},
    )
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        _add_equipment_columns(conn)
        conn.commit()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_upload():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        storage = LocalFileStorage(storage_root=str(tmp_path))
        return UploadDocumentUseCase(repository=repo, storage=storage)

    def override_download():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        storage = LocalFileStorage(storage_root=str(tmp_path))
        return DownloadDocumentUseCase(repository=repo, storage=storage)

    def override_report():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        return GenerateReportUseCase(repository=repo)

    def override_check_expiry():
        db = TestingSessionLocal()
        repo = SqlDocumentRepository(db)
        return CheckExpiryUseCase(repo)

    app.dependency_overrides[get_upload_document_use_case] = override_upload
    app.dependency_overrides[get_download_document_use_case] = override_download
    app.dependency_overrides[get_generate_report_use_case] = override_report
    app.dependency_overrides[get_check_expiry_use_case] = override_check_expiry
    app.dependency_overrides[require_viewer_or_admin] = lambda: User(
        id=uuid.uuid4(), email="admin@test.local", hashed_password="x",
        role=UserRole.ADMIN, is_active=True,
    )
    app.dependency_overrides[require_admin] = lambda: User(
        id=uuid.uuid4(), email="admin@test.local", hashed_password="x",
        role=UserRole.ADMIN, is_active=True,
    )

    # Expose session for direct DB inserts
    _sessions = []

    def get_session():
        db = TestingSessionLocal()
        _sessions.append(db)
        return db

    yield TestClient(app), get_session, engine
    for s in _sessions:
        s.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def _insert_document(engine, doc_id, nombre, fecha_caducidad, deleted_at=None):
    from infrastructure.db.models import DocumentModel
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        model = DocumentModel(
            id=doc_id,
            nombre_archivo=nombre,
            formato="pdf",
            fecha_validez=date(2020, 1, 1),
            fecha_caducidad=fecha_caducidad,
            deleted_at=deleted_at,
        )
        session.add(model)
        session.commit()

def test_alerts_endpoint_empty_list(alerts_client):
    client, _, _ = alerts_client
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert response.json() == []


def test_alerts_endpoint_returns_active_alerts(alerts_client):
    client, _, engine = alerts_client
    doc_id = uuid4()
    fecha_cad = date.today() + timedelta(days=10)
    _insert_document(engine, doc_id, "contrato.pdf", fecha_cad)

    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nivel"] == "alerta"
    assert data[0]["document_id"] == str(doc_id)


def test_alerts_endpoint_filter_by_nivel(alerts_client):
    client, _, engine = alerts_client
    # alerta_critica: 3 days
    id1 = uuid4()
    _insert_document(engine, id1, "critico.pdf", date.today() + timedelta(days=3))
    # aviso: 25 days
    id2 = uuid4()
    _insert_document(engine, id2, "aviso.pdf", date.today() + timedelta(days=25))

    response = client.get("/api/v1/alerts?nivel=alerta_critica")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nivel"] == "alerta_critica"


def test_alerts_excludes_deleted_documents(alerts_client):
    client, _, engine = alerts_client
    from datetime import datetime
    doc_id = uuid4()
    fecha_cad = date.today() + timedelta(days=5)
    _insert_document(engine, doc_id, "borrado.pdf", fecha_cad, deleted_at=datetime.now())

    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert response.json() == []
