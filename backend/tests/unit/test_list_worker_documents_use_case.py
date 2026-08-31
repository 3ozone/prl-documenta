"""Tests for ListWorkerDocumentsUseCase."""
from __future__ import annotations

from datetime import date
from uuid import uuid4

from unittest.mock import MagicMock

import pytest

from application.use_cases.list_worker_documents import (
    ListWorkerDocumentsCommand,
    ListWorkerDocumentsUseCase,
)
from domain.entities.document import Document


class TestListWorkerDocumentsUseCase:
    def _make_use_case(self, documents: list[Document], total: int):
        repository = MagicMock()
        repository.get_worker_documents.return_value = (documents, total)
        return ListWorkerDocumentsUseCase(repository=repository)

    def test_list_worker_documents_by_dni(self):
        docs = [
            Document(
                id=uuid4(),
                nombre_archivo="doc1.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 12, 31),
                categoria="trabajadores",
                nombre_trabajador="Juan Pérez",
                dni="12345678A",
                puesto="Operario",
                tipo_documento="formacion",
            ),
        ]
        use_case = self._make_use_case(docs, total=1)

        result = use_case.execute(ListWorkerDocumentsCommand(dni_trabajador="12345678A", page=1, per_page=20))

        assert result.total == 1
        assert len(result.documents) == 1
        assert result.documents[0].dni == "12345678A"
        use_case._repository.get_worker_documents.assert_called_with(dni_trabajador="12345678A", page=1, per_page=20)

    def test_list_worker_documents_pagination(self):
        docs = [
            Document(
                id=uuid4(),
                nombre_archivo="doc1.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 12, 31),
                categoria="trabajadores",
                nombre_trabajador="Juan Pérez",
                dni="12345678A",
                puesto="Operario",
                tipo_documento="formacion",
            ),
        ]
        use_case = self._make_use_case(docs, total=50)

        result = use_case.execute(ListWorkerDocumentsCommand(dni_trabajador=None, page=2, per_page=10))

        assert result.page == 2
        assert result.per_page == 10
        assert result.total == 50
        assert len(result.documents) == 1
        use_case._repository.get_worker_documents.assert_called_with(dni_trabajador=None, page=2, per_page=10)

    def test_list_worker_documents_all_fields(self):
        doc_id = uuid4()
        docs = [
            Document(
                id=doc_id,
                nombre_archivo="doc_completo.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 6, 1),
                categoria="trabajadores",
                nombre_trabajador="María García",
                dni="87654321B",
                puesto="Técnico",
                tipo_documento="reconocimiento_medico",
            ),
        ]
        use_case = self._make_use_case(docs, total=1)

        result = use_case.execute(ListWorkerDocumentsCommand(dni_trabajador=None, page=1, per_page=20))

        assert len(result.documents) == 1
        doc = result.documents[0]
        assert doc.nombre_trabajador == "María García"
        assert doc.dni == "87654321B"
        assert doc.puesto == "Técnico"
        assert doc.tipo_documento == "reconocimiento_medico"
