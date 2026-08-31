"""Abstract file storage port."""
from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class AbstractFileStorage(ABC):
    @abstractmethod
    def save(self, document_id: UUID, content: bytes) -> str: ...

    @abstractmethod
    def delete(self, document_id: UUID) -> None: ...

    @abstractmethod
    def read(self, document_id: UUID) -> bytes:
        """Returns the PDF file content as bytes."""
