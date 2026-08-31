"""PDF report exporter."""
from __future__ import annotations

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from application.ports.report_exporter import AbstractReportExporter
from application.use_cases.generate_report import ReportResult


class PdfReportExporter(AbstractReportExporter):
    def to_csv(self, result: ReportResult) -> bytes:
        raise NotImplementedError("PdfReportExporter only supports PDF export")

    def to_pdf(self, result: ReportResult) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Informe de Estado Documental", styles["Title"]))
        elements.append(
            Paragraph(f"Generado: {result.generated_at:%Y-%m-%d %H:%M:%S}", styles["Normal"])
        )

        for section in result.sections:
            elements.append(Paragraph(section.estado.value.upper(), styles["Heading2"]))
            data = [["id", "nombre_archivo", "categoria", "fecha_caducidad"]]
            for doc_item in section.documentos:
                data.append(
                    [
                        str(doc_item.id),
                        doc_item.nombre_archivo,
                        doc_item.categoria or "",
                        doc_item.fecha_caducidad.isoformat(),
                    ]
                )
            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(table)

        doc.build(elements)
        return buffer.getvalue()
