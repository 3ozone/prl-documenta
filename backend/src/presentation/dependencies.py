"""FastAPI dependency injection."""
from __future__ import annotations

import os
import tempfile

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from application.use_cases.upload_document import UploadDocumentUseCase
from application.use_cases.upload_company_document import UploadCompanyDocumentUseCase
from application.use_cases.list_company_documents import ListCompanyDocumentsUseCase
from application.use_cases.upload_worker_document import UploadWorkerDocumentUseCase
from application.use_cases.list_worker_documents import ListWorkerDocumentsUseCase
from application.use_cases.upload_equipment_document import UploadEquipmentDocumentUseCase
from application.use_cases.list_equipment_documents import ListEquipmentDocumentsUseCase
from application.use_cases.check_expiry import CheckExpiryUseCase
from application.use_cases.download_document import DownloadDocumentUseCase
from application.use_cases.generate_report import GenerateReportUseCase
from application.ports.report_exporter import AbstractReportExporter
from domain.entities.user import User, UserRole
from infrastructure.db.models import Base
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from infrastructure.db.repositories.user_repository import SqlUserRepository
from infrastructure.auth.jwt_token_service import JwtTokenService
from infrastructure.storage.local_file_storage import LocalFileStorage
from infrastructure.export.csv_report_exporter import CsvReportExporter
from infrastructure.export.pdf_report_exporter import PdfReportExporter

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./prl_documenta.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_jwt_token_service() -> JwtTokenService:
    return JwtTokenService()


def get_user_repository(db: Session = Depends(get_db)) -> SqlUserRepository:
    return SqlUserRepository(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    from application.use_cases.get_current_user import GetCurrentUserUseCase
    from domain.exceptions import InvalidCredentials
    try:
        return GetCurrentUserUseCase(SqlUserRepository(db), JwtTokenService()).execute(token)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Se requiere rol admin")
    return current_user


def require_viewer_or_admin(current_user: User = Depends(get_current_user)) -> User:
    return current_user


def get_upload_document_use_case(
    db: Session = Depends(get_db),
) -> UploadDocumentUseCase:
    storage_root = os.environ.get("STORAGE_ROOT", tempfile.gettempdir())
    repository = SqlDocumentRepository(db)
    storage = LocalFileStorage(storage_root=storage_root)
    return UploadDocumentUseCase(repository=repository, storage=storage)


def get_download_document_use_case(
    db: Session = Depends(get_db),
) -> DownloadDocumentUseCase:
    storage_root = os.environ.get("STORAGE_ROOT", tempfile.gettempdir())
    repository = SqlDocumentRepository(db)
    storage = LocalFileStorage(storage_root=storage_root)
    return DownloadDocumentUseCase(repository=repository, storage=storage)


def get_generate_report_use_case(db: Session = Depends(get_db)) -> GenerateReportUseCase:
    repository = SqlDocumentRepository(db)
    return GenerateReportUseCase(repository=repository)


def get_report_exporter(formato: str) -> AbstractReportExporter:
    if formato == "csv":
        return CsvReportExporter()
    if formato == "pdf":
        return PdfReportExporter()
    raise ValueError(f"Formato '{formato}' no soportado")


def get_upload_company_document_use_case(
    db: Session = Depends(get_db),
) -> UploadCompanyDocumentUseCase:
    storage_root = os.environ.get("STORAGE_ROOT", tempfile.gettempdir())
    repository = SqlDocumentRepository(db)
    storage = LocalFileStorage(storage_root=storage_root)
    return UploadCompanyDocumentUseCase(repository=repository, storage=storage)


def get_list_company_documents_use_case(
    db: Session = Depends(get_db),
) -> ListCompanyDocumentsUseCase:
    repository = SqlDocumentRepository(db)
    return ListCompanyDocumentsUseCase(repository=repository)


def get_upload_worker_document_use_case(
    db: Session = Depends(get_db),
) -> UploadWorkerDocumentUseCase:
    storage_root = os.environ.get("STORAGE_ROOT", tempfile.gettempdir())
    repository = SqlDocumentRepository(db)
    storage = LocalFileStorage(storage_root=storage_root)
    return UploadWorkerDocumentUseCase(repository=repository, storage=storage)


def get_list_worker_documents_use_case(
    db: Session = Depends(get_db),
) -> ListWorkerDocumentsUseCase:
    repository = SqlDocumentRepository(db)
    return ListWorkerDocumentsUseCase(repository=repository)


def get_upload_equipment_document_use_case(
    db: Session = Depends(get_db),
) -> UploadEquipmentDocumentUseCase:
    storage_root = os.environ.get("STORAGE_ROOT", tempfile.gettempdir())
    repository = SqlDocumentRepository(db)
    storage = LocalFileStorage(storage_root=storage_root)
    return UploadEquipmentDocumentUseCase(repository=repository, storage=storage)


def get_list_equipment_documents_use_case(
    db: Session = Depends(get_db),
) -> ListEquipmentDocumentsUseCase:
    repository = SqlDocumentRepository(db)
    return ListEquipmentDocumentsUseCase(repository=repository)


def get_check_expiry_use_case(db: Session = Depends(get_db)) -> CheckExpiryUseCase:
    repo = SqlDocumentRepository(db)
    return CheckExpiryUseCase(repo)
