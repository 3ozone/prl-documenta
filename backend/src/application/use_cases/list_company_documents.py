"""List company documents use case."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.ports.document_repository import AbstractDocumentRepository
from domain.entities.document import Document


@dataclass
class ListCompanyDocumentsCommand:
    page: int
    per_page: int
    estado: str | None = None


@dataclass
class ListCompanyDocumentsResult:
    documents: list[Document]
    total: int
    page: int
    per_page: int


class ListCompanyDocumentsUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    def execute(self, command: ListCompanyDocumentsCommand) -> ListCompanyDocumentsResult:
        documents, total = self._repository.get_company_documents(
            page=command.page,
            per_page=command.per_page,
            estado=command.estado,
        )

        return ListCompanyDocumentsResult(
            documents=documents,
            total=total,
            page=command.page,
            per_page=command.per_page,
        )