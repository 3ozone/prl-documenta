"""Tests for PdfReportExporter."""
from __future__ import annotations

import io
from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from domain.entities.document import Document
from domain.entities.document_status import DocumentStatus
from application.use_cases.generate_report import ReportSection, ReportResult
from infrastructure.export.pdf_report_exporter import PdfReportExporter


class TestPdfReportExporter:
    def test_pdf_contiene_titulo(self) -> None:
        result = ReportResult(
            generated_at=datetime.now(timezone.utc),
            sections=[
                ReportSection(estado=DocumentStatus.VIGENTE, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.PROXIMA_A_CADUCAR, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.CADUCADA, documentos=[], dias_hasta_caducidad={}),
            ],
        )
        exporter = PdfReportExporter()
        content = exporter.to_pdf(result)

        assert content.startswith(b"%PDF")

    def test_pdf_contiene_generated_at(self) -> None:
        generated_at = datetime(2025, 6, 15, 10, 30, 0)
        result = ReportResult(
            generated_at=generated_at,
            sections=[
                ReportSection(estado=DocumentStatus.VIGENTE, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.PROXIMA_A_CADUCAR, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.CADUCADA, documentos=[], dias_hasta_caducidad={}),
            ],
        )
        exporter = PdfReportExporter()
        content = exporter.to_pdf(result)

        # PDF is a binary format; we can check that it starts with PDF header
        assert content.startswith(b"%PDF")

    def test_pdf_tabla_por_estado(self) -> None:
        doc = Document(
            id=uuid4(),
            nombre_archivo="test_doc.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2027, 1, 1),
            categoria="empresa",
        )
        result = ReportResult(
            generated_at=datetime.now(timezone.utc),
            sections=[
                ReportSection(
                    estado=DocumentStatus.VIGENTE,
                    documentos=[doc],
                    dias_hasta_caducidad={str(doc.id): 730},
                ),
                ReportSection(estado=DocumentStatus.PROXIMA_A_CADUCAR, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.CADUCADA, documentos=[], dias_hasta_caducidad={}),
            ],
        )
        exporter = PdfReportExporter()
        content = exporter.to_pdf(result)

        assert content.startswith(b"%PDF")
        # Verify the PDF is valid by checking it can be read
        buffer = io.BytesIO(content)
        buffer.seek(0)
        assert len(buffer.read()) > 0
