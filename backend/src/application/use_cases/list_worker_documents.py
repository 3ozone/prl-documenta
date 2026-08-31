"""List worker documents use case."""
from __future__ import annotations

from dataclasses import dataclass

from application.ports.document_repository import AbstractDocumentRepository
from domain.entities.document import Document


@dataclass
class ListWorkerDocumentsCommand:
    dni_trabajador: str | None
    page: int
    per_page: int


@dataclass
class ListWorkerDocumentsResult:
    documents: list[Document]
    total: int
    page: int
    per_page: int


class ListWorkerDocumentsUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    def execute(self, command: ListWorkerDocumentsCommand) -> ListWorkerDocumentsResult:
        documents, total = self._repository.get_worker_documents(
            dni_trabajador=command.dni_trabajador,
            page=command.page,
            per_page=command.per_page,
        )

        return ListWorkerDocumentsResult(
            documents=documents,
            total=total,
            page=command.page,
            per_page=command.per_page,
        )
