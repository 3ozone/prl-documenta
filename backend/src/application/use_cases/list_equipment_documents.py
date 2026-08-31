"""List equipment documents use case."""
from __future__ import annotations

from dataclasses import dataclass

from application.ports.document_repository import AbstractDocumentRepository
from domain.entities.document import Document


@dataclass
class ListEquipmentDocumentsCommand:
    id_equipo: str | None
    page: int
    per_page: int


@dataclass
class ListEquipmentDocumentsResult:
    documents: list[Document]
    total: int
    page: int
    per_page: int


class ListEquipmentDocumentsUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    def execute(self, command: ListEquipmentDocumentsCommand) -> ListEquipmentDocumentsResult:
        documents, total = self._repository.get_equipment_documents(
            id_equipo=command.id_equipo,
            page=command.page,
            per_page=command.per_page,
        )

        return ListEquipmentDocumentsResult(
            documents=documents,
            total=total,
            page=command.page,
            per_page=command.per_page,
        )