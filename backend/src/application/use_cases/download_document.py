"""Download document use case."""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from application.ports.document_repository import AbstractDocumentRepository
from application.ports.file_storage import AbstractFileStorage
from domain.exceptions import DocumentNotFound


@dataclass
class DownloadDocumentResult:
    content: bytes
    nombre_archivo: str


class DownloadDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, document_id: UUID) -> DownloadDocumentResult:
        document = self._repository.get_by_id(document_id)
        if document is None:
            raise DocumentNotFound(f"Documento con id '{document_id}' no encontrado.")

        content = self._storage.read(document_id)
        return DownloadDocumentResult(
            content=content,
            nombre_archivo=document.nombre_archivo,
        )
