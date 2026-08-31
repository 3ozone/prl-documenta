"""Upload document use case."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from application.ports.document_repository import AbstractDocumentRepository
from application.ports.file_storage import AbstractFileStorage
from domain.entities.document import Document
from domain.exceptions import InvalidDocumentCategory, InvalidDocumentFormat
from domain.value_objects.expiry_date import ExpiryDate

ALLOWED_FORMATS: frozenset[str] = frozenset({"pdf"})
ALLOWED_CATEGORIES: frozenset[str] = frozenset({"empresa", "trabajadores", "equipos"})


@dataclass
class UploadDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    categoria: str | None = None
    uploaded_by: UUID | None = None


@dataclass
class UploadDocumentResult:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    categoria: str | None = None
    uploaded_by: UUID | None = None


class UploadDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadDocumentCommand) -> UploadDocumentResult:
        if command.formato not in ALLOWED_FORMATS:
            raise InvalidDocumentFormat(
                f"Formato no admitido: '{command.formato}'. "
                f"Formatos permitidos: {sorted(ALLOWED_FORMATS)}"
            )

        if command.categoria is not None and command.categoria not in ALLOWED_CATEGORIES:
            raise InvalidDocumentCategory(
                f"Categoría no admitida: '{command.categoria}'. "
                f"Categorías permitidas: {sorted(ALLOWED_CATEGORIES)}"
            )

        # Validates dates — raises InvalidExpiryDate if invalid
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
            categoria=command.categoria,
            uploaded_by=command.uploaded_by,
        )

        try:
            self._repository.save(document)
        except Exception:
            self._storage.delete(document_id)
            raise

        return UploadDocumentResult(
            id=document_id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            storage_path=storage_path,
            categoria=document.categoria,
            uploaded_by=document.uploaded_by,
        )
