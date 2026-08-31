"""Abstract document repository port."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, timedelta
from uuid import UUID

from domain.entities.document import Document


class AbstractDocumentRepository(ABC):
    @abstractmethod
    def save(self, document: Document) -> None: ...

    @abstractmethod
    def exists(self, document_id: UUID) -> bool: ...

    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document | None:
        """Returns the document if it exists and is not deleted (deleted_at is null), None otherwise."""

    @abstractmethod
    def get_all_active(self) -> list[Document]:
        """Returns all documents with deleted_at null, without filtering by category."""

    @abstractmethod
    def save_company_document(self, document: Document) -> None: ...

    @abstractmethod
    def get_company_documents(
        self, page: int, per_page: int, estado: str | None
    ) -> tuple[list[Document], int]: ...

    @abstractmethod
    def save_worker_document(self, document: Document) -> None: ...

    @abstractmethod
    def get_worker_documents(
        self, dni_trabajador: str | None, page: int, per_page: int
    ) -> tuple[list[Document], int]: ...

    @abstractmethod
    def save_equipment_document(self, document: Document) -> None: ...

    @abstractmethod
    def get_equipment_documents(
        self, id_equipo: str | None, page: int, per_page: int
    ) -> tuple[list[Document], int]: ...

    @abstractmethod
    def get_expiring_documents(self, days_ahead: int, fecha: date) -> list[Document]:
        """Documentos con fecha_caducidad <= fecha + timedelta(days_ahead) y deleted_at IS NULL.
        Incluye ya caducados."""
