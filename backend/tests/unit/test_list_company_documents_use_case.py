"""Tests for ListCompanyDocumentsUseCase."""
from __future__ import annotations

from datetime import date
from uuid import uuid4

from unittest.mock import MagicMock

import pytest

from application.use_cases.list_company_documents import (
    ListCompanyDocumentsCommand,
    ListCompanyDocumentsUseCase,
)
from domain.entities.document import Document


class TestListCompanyDocumentsUseCase:
    def _make_use_case(self, documents: list[Document], total: int):
        repository = MagicMock()
        repository.get_company_documents.return_value = (documents, total)
        return ListCompanyDocumentsUseCase(repository=repository)

    def test_list_company_documents_pagination(self):
        docs = [
            Document(
                id=uuid4(),
                nombre_archivo="doc1.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 12, 31),
                categoria="empresa",
                razon_social="Acme SL",
                cif="A12345678",
                actividad_economica="Construcción",
                centro_trabajo="Madrid",
            ),
        ]
        use_case = self._make_use_case(docs, total=50)

        result = use_case.execute(ListCompanyDocumentsCommand(page=2, per_page=10))

        assert result.page == 2
        assert result.per_page == 10
        assert result.total == 50
        assert len(result.documents) == 1

    def test_list_company_documents_filter_vigente(self):
        docs = [
            Document(
                id=uuid4(),
                nombre_archivo="doc_vigente.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2099, 12, 31),
                categoria="empresa",
                razon_social="Acme SL",
                cif="A12345678",
                actividad_economica=None,
                centro_trabajo=None,
            ),
        ]
        use_case = self._make_use_case(docs, total=1)

        result = use_case.execute(ListCompanyDocumentsCommand(page=1, per_page=20, estado="vigente"))

        assert len(result.documents) == 1
        use_case._repository.get_company_documents.assert_called_with(page=1, per_page=20, estado="vigente")

    def test_list_company_documents_filter_caducada(self):
        docs = [
            Document(
                id=uuid4(),
                nombre_archivo="doc_caducado.pdf",
                formato="pdf",
                fecha_validez=date(2020, 1, 1),
                fecha_caducidad=date(2021, 1, 1),
                categoria="empresa",
                razon_social="Old Corp",
                cif="B87654321",
                actividad_economica=None,
                centro_trabajo=None,
            ),
        ]
        use_case = self._make_use_case(docs, total=1)

        result = use_case.execute(ListCompanyDocumentsCommand(page=1, per_page=20, estado="caducada"))

        assert len(result.documents) == 1
        use_case._repository.get_company_documents.assert_called_with(page=1, per_page=20, estado="caducada")

    def test_list_company_documents_all_fields(self):
        doc_id = uuid4()
        docs = [
            Document(
                id=doc_id,
                nombre_archivo="doc_completo.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 6, 1),
                categoria="empresa",
                razon_social="Empresa Total",
                cif="C12345678",
                actividad_economica="Servicios",
                centro_trabajo="Barcelona",
            ),
        ]
        use_case = self._make_use_case(docs, total=1)

        result = use_case.execute(ListCompanyDocumentsCommand(page=1, per_page=20))

        assert len(result.documents) == 1
        doc = result.documents[0]
        assert doc.razon_social == "Empresa Total"
        assert doc.cif == "C12345678"
        assert doc.actividad_economica == "Servicios"
        assert doc.centro_trabajo == "Barcelona"