"""Local file storage implementation."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from uuid import UUID

from application.ports.file_storage import AbstractFileStorage

log = logging.getLogger(__name__)

STORAGE_ROOT = os.environ.get("STORAGE_ROOT", "/data/documents")


class LocalFileStorage(AbstractFileStorage):
    def __init__(self, storage_root: str = STORAGE_ROOT) -> None:
        self._root = Path(storage_root)
        self._root.mkdir(parents=True, exist_ok=True)

    def save(self, document_id: UUID, content: bytes) -> str:
        path = self._root / f"{document_id}.pdf"
        path.write_bytes(content)
        log.info("Stored file at %s", path)
        return str(path)

    def delete(self, document_id: UUID) -> None:
        path = self._root / f"{document_id}.pdf"
        if path.exists():
            path.unlink()
            log.info("Deleted file at %s", path)

    def read(self, document_id: UUID) -> bytes:
        path = self._root / f"{document_id}.pdf"
        if not path.exists():
            raise FileNotFoundError(f"Fichero no encontrado: {path}")
        return path.read_bytes()
