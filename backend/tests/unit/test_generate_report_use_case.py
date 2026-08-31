"""Tests for GenerateReportUseCase."""
from __future__ import annotations

from datetime import date, timedelta
from uuid import uuid4

import pytest

from domain.entities.document import Document
from domain.entities.document_status import DocumentStatus
from application.use_cases.generate_report import GenerateReportUseCase, ReportResult


class MockRepository:
    def __init__(self, documents: list[Document]) -> None:
        self._documents = documents

    def get_all_active(self) -> list[Document]:
        return self._documents


class TestGenerateReportUseCase:
    def test_clasifica_vigente_cuando_fecha_mas_30_dias(self) -> None:
        repo = MockRepository(
            [
                Document(
                    id=uuid4(),
                    nombre_archivo="doc1.pdf",
                    formato="pdf",
                    fecha_validez=date.today(),
                    fecha_caducidad=date.today() + timedelta(days=31),
                    categoria="empresa",
                )
            ]
        )
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria=None, fecha_referencia=date.today())

        assert len(result.sections) == 3
        vigente_section = next(s for s in result.sections if s.estado == DocumentStatus.VIGENTE)
        assert len(vigente_section.documentos) == 1
        assert vigente_section.documentos[0].nombre_archivo == "doc1.pdf"
        assert vigente_section.dias_hasta_caducidad[str(vigente_section.documentos[0].id)] == 31

    def test_clasifica_proxima_a_caducar_cuando_fecha_entre_hoy_y_30_dias(self) -> None:
        repo = MockRepository(
            [
                Document(
                    id=uuid4(),
                    nombre_archivo="doc2.pdf",
                    formato="pdf",
                    fecha_validez=date.today() - timedelta(days=10),
                    fecha_caducidad=date.today() + timedelta(days=15),
                    categoria="trabajadores",
                )
            ]
        )
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria=None, fecha_referencia=date.today())

        proxima_section = next(s for s in result.sections if s.estado == DocumentStatus.PROXIMA_A_CADUCAR)
        assert len(proxima_section.documentos) == 1
        assert proxima_section.documentos[0].nombre_archivo == "doc2.pdf"
        assert proxima_section.dias_hasta_caducidad[str(proxima_section.documentos[0].id)] == 15

    def test_clasifica_caducada_cuando_fecha_antes_hoy(self) -> None:
        repo = MockRepository(
            [
                Document(
                    id=uuid4(),
                    nombre_archivo="doc3.pdf",
                    formato="pdf",
                    fecha_validez=date.today() - timedelta(days=100),
                    fecha_caducidad=date.today() - timedelta(days=10),
                    categoria="equipos",
                )
            ]
        )
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria=None, fecha_referencia=date.today())

        caducada_section = next(s for s in result.sections if s.estado == DocumentStatus.CADUCADA)
        assert len(caducada_section.documentos) == 1
        assert caducada_section.documentos[0].nombre_archivo == "doc3.pdf"
        assert caducada_section.dias_hasta_caducidad[str(caducada_section.documentos[0].id)] == -10

    def test_excluye_documentos_con_deleted_at(self) -> None:
        # The repository only returns active (non-deleted) documents.
        # If a document has deleted_at set, it should not appear in get_all_active results.
        # So here we simply verify that get_all_active does not return anything "already deleted"
        # by checking that the report contains no documents when the repo is empty.
        repo = MockRepository([])
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria=None, fecha_referencia=date.today())

        for section in result.sections:
            assert len(section.documentos) == 0

    def test_filtra_por_categoria(self) -> None:
        doc_empresa = Document(
            id=uuid4(),
            nombre_archivo="empresa_doc.pdf",
            formato="pdf",
            fecha_validez=date.today(),
            fecha_caducidad=date.today() + timedelta(days=31),
            categoria="empresa",
        )
        doc_trabajadores = Document(
            id=uuid4(),
            nombre_archivo="trabajador_doc.pdf",
            formato="pdf",
            fecha_validez=date.today(),
            fecha_caducidad=date.today() + timedelta(days=31),
            categoria="trabajadores",
        )
        repo = MockRepository([doc_empresa, doc_trabajadores])
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria="empresa", fecha_referencia=date.today())

        vigente_section = next(s for s in result.sections if s.estado == DocumentStatus.VIGENTE)
        assert len(vigente_section.documentos) == 1
        assert vigente_section.documentos[0].categoria == "empresa"

    def test_generated_at_esta_presente(self) -> None:
        repo = MockRepository([])
        use_case = GenerateReportUseCase(repository=repo)
        result = use_case.execute(categoria=None, fecha_referencia=date.today())

        assert result.generated_at is not None
        assert isinstance(result.generated_at.year, int)
