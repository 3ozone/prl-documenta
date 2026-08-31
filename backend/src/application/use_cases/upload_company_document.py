"""Upload company document use case."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from application.ports.document_repository import AbstractDocumentRepository
from application.ports.file_storage import AbstractFileStorage
from domain.entities.document import Document
from domain.exceptions import InvalidDocumentFormat, MissingRequiredField
from domain.value_objects.expiry_date import ExpiryDate

ALLOWED_FORMATS: frozenset[str] = frozenset({"pdf"})


@dataclass
class UploadCompanyDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    razon_social: str
    cif: str
    actividad_economica: str | None = None
    centro_trabajo: str | None = None
    uploaded_by: UUID | None = None


@dataclass
class UploadCompanyDocumentResult:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    razon_social: str
    cif: str
    uploaded_by: UUID | None = None
    actividad_economica: str | None = None
    centro_trabajo: str | None = None


class UploadCompanyDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadCompanyDocumentCommand) -> UploadCompanyDocumentResult:
        if not command.razon_social:
            raise MissingRequiredField("razon_social es obligatorio para documentos de empresa")

        if not command.cif:
            raise MissingRequiredField("cif es obligatorio para documentos de empresa")

        if command.formato not in ALLOWED_FORMATS:
            raise InvalidDocumentFormat(
                f"Formato no admitido: '{command.formato}'. "
                f"Formatos permitidos: {sorted(ALLOWED_FORMATS)}"
            )

        ExpiryDate(
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
        )

        document_id = uuid.uuid4()

        storage_path = self._storage.save(document_id, command.content)

        document = Document(
            id=document_id,
            nombre_archivo=command.nombre_archivo,
            formato=command.formato,
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
            categoria="empresa",
            uploaded_by=command.uploaded_by,
            razon_social=command.razon_social,
            cif=command.cif,
            actividad_economica=command.actividad_economica,
            centro_trabajo=command.centro_trabajo,
        )

        try:
            self._repository.save_company_document(document)
        except Exception:
            self._storage.delete(document_id)
            raise

        return UploadCompanyDocumentResult(
            id=document_id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            storage_path=storage_path,
            razon_social=document.razon_social,
            cif=document.cif,
            uploaded_by=document.uploaded_by,
            actividad_economica=document.actividad_economica,
            centro_trabajo=document.centro_trabajo,
        )