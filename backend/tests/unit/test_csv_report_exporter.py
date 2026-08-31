"""Tests for CsvReportExporter."""
from __future__ import annotations

import csv
from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from domain.entities.document import Document
from domain.entities.document_status import DocumentStatus
from application.use_cases.generate_report import ReportSection, ReportResult
from infrastructure.export.csv_report_exporter import CsvReportExporter


class TestCsvReportExporter:
    def test_csv_contiene_cabecera_correcta(self) -> None:
        result = ReportResult(
            generated_at=datetime.now(timezone.utc),
            sections=[
                ReportSection(estado=DocumentStatus.VIGENTE, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.PROXIMA_A_CADUCAR, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.CADUCADA, documentos=[], dias_hasta_caducidad={}),
            ],
        )
        exporter = CsvReportExporter()
        content = exporter.to_csv(result)
        lines = content.decode("utf-8").strip().split("\n")

        assert lines[0] == "id,nombre_archivo,categoria,fecha_validez,fecha_caducidad,estado,dias_hasta_caducidad"

    def test_csv_contiene_columnas_por_documento(self) -> None:
        doc_id = uuid4()
        result = ReportResult(
            generated_at=datetime.now(timezone.utc),
            sections=[
                ReportSection(
                    estado=DocumentStatus.VIGENTE,
                    documentos=[
                        Document(
                            id=doc_id,
                            nombre_archivo="test_doc.pdf",
                            formato="pdf",
                            fecha_validez=date(2025, 1, 1),
                            fecha_caducidad=date(2027, 1, 1),
                            categoria="empresa",
                        )
                    ],
                    dias_hasta_caducidad={str(doc_id): 730},
                ),
                ReportSection(estado=DocumentStatus.PROXIMA_A_CADUCAR, documentos=[], dias_hasta_caducidad={}),
                ReportSection(estado=DocumentStatus.CADUCADA, documentos=[], dias_hasta_caducidad={}),
            ],
        )
        exporter = CsvReportExporter()
        content = exporter.to_csv(result)
        lines = content.decode("utf-8").strip().split("\n")

        # Header + 1 data row
        assert len(lines) == 2
        row = next(csv.reader([lines[1]]))
        assert row[0] == str(doc_id)
        assert row[1] == "test_doc.pdf"
        assert row[2] == "empresa"
        assert row[3] == "2025-01-01"
        assert row[4] == "2027-01-01"
        assert row[5] == "vigente"
        assert row[6] == "730"

    def test_csv_dias_hasta_caducidad_correctos(self) -> None:
        doc1 = Document(
            id=uuid4(),
            nombre_archivo="doc1.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2025, 6, 1),
            categoria=None,
        )
        doc2 = Document(
            id=uuid4(),
            nombre_archivo="doc2.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2025, 3, 1),
            categoria=None,
        )
        doc3 = Document(
            id=uuid4(),
            nombre_archivo="doc3.pdf",
            formato="pdf",
            fecha_validez=date(2024, 1, 1),
            fecha_caducidad=date(2024, 6, 1),
            categoria=None,
        )
        result = ReportResult(
            generated_at=datetime.now(timezone.utc),
            sections=[
                ReportSection(
                    estado=DocumentStatus.VIGENTE,
                    documentos=[doc1],
                    dias_hasta_caducidad={str(doc1.id): (doc1.fecha_caducidad - date(2025, 1, 1)).days},
                ),
                ReportSection(
                    estado=DocumentStatus.PROXIMA_A_CADUCAR,
                    documentos=[doc2],
                    dias_hasta_caducidad={str(doc2.id): (doc2.fecha_caducidad - date(2025, 1, 1)).days},
                ),
                ReportSection(
                    estado=DocumentStatus.CADUCADA,
                    documentos=[doc3],
                    dias_hasta_caducidad={str(doc3.id): (doc3.fecha_caducidad - date(2025, 1, 1)).days},
                ),
            ],
        )
        exporter = CsvReportExporter()
        content = exporter.to_csv(result)
        lines = content.decode("utf-8").strip().split("\n")

        # Header + 3 data rows
        assert len(lines) == 4
        rows = [next(csv.reader([line])) for line in lines[1:]]
        assert rows[0][5] == "vigente"
        assert rows[0][6] == str((doc1.fecha_caducidad - date(2025, 1, 1)).days)
        assert rows[1][5] == "proxima_a_caducar"
        assert rows[1][6] == str((doc2.fecha_caducidad - date(2025, 1, 1)).days)
        assert rows[2][5] == "caducada"
        assert rows[2][6] == str((doc3.fecha_caducidad - date(2025, 1, 1)).days)
