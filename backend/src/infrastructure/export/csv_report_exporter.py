"""CSV report exporter."""
from __future__ import annotations

import csv
import io

from application.ports.report_exporter import AbstractReportExporter
from application.use_cases.generate_report import ReportResult


class CsvReportExporter(AbstractReportExporter):
    def to_pdf(self, result: ReportResult) -> bytes:
        raise NotImplementedError("CsvReportExporter only supports CSV export")

    def to_csv(self, result: ReportResult) -> bytes:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "id",
                "nombre_archivo",
                "categoria",
                "fecha_validez",
                "fecha_caducidad",
                "estado",
                "dias_hasta_caducidad",
            ]
        )
        for section in result.sections:
            for doc in section.documentos:
                dias = section.dias_hasta_caducidad[str(doc.id)]
                writer.writerow(
                    [
                        str(doc.id),
                        doc.nombre_archivo,
                        doc.categoria or "",
                        doc.fecha_validez.isoformat(),
                        doc.fecha_caducidad.isoformat(),
                        section.estado.value,
                        dias,
                    ]
                )
        return output.getvalue().encode("utf-8")
