"""Upload worker document use case."""
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
from domain.value_objects.worker_document_type import WorkerDocumentType

ALLOWED_FORMATS: frozenset[str] = frozenset({"pdf"})


@dataclass
class UploadWorkerDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    nombre_trabajador: str
    dni: str
    tipo_documento: WorkerDocumentType
    puesto: str | None = None
    uploaded_by: UUID | None = None


@dataclass
class UploadWorkerDocumentResult:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    nombre_trabajador: str
    dni: str
    tipo_documento: WorkerDocumentType
    puesto: str | None = None
    uploaded_by: UUID | None = None


class UploadWorkerDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadWorkerDocumentCommand) -> UploadWorkerDocumentResult:
        if not command.nombre_trabajador:
            raise MissingRequiredField("nombre_trabajador es obligatorio para documentos de trabajador")

        if not command.dni:
            raise MissingRequiredField("dni es obligatorio para documentos de trabajador")

        if not command.tipo_documento:
            raise MissingRequiredField("tipo_documento es obligatorio para documentos de trabajador")

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
            categoria="trabajadores",
            uploaded_by=command.uploaded_by,
            nombre_trabajador=command.nombre_trabajador,
            dni=command.dni,
            puesto=command.puesto,
            tipo_documento=command.tipo_documento.value,
        )

        try:
            self._repository.save_worker_document(document)
        except Exception:
            self._storage.delete(document_id)
            raise

        return UploadWorkerDocumentResult(
            id=document_id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            storage_path=storage_path,
            nombre_trabajador=document.nombre_trabajador,
            dni=document.dni,
            puesto=document.puesto,
            tipo_documento=command.tipo_documento,
            uploaded_by=document.uploaded_by,
        )
