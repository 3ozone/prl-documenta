# Design — core_reporting (Generación de informes de estado documental)

---

## Archivos a crear

| Archivo | Capa | Acción |
|---------|------|--------|
| `backend/src/application/use_cases/generate_report.py` | Application | Crear — caso de uso `GenerateReportUseCase` |
| `backend/src/application/ports/report_exporter.py` | Application | Crear — puerto abstracto `AbstractReportExporter` |
| `backend/src/infrastructure/export/csv_report_exporter.py` | Infrastructure | Implementar `CsvReportExporter` |
| `backend/src/infrastructure/export/pdf_report_exporter.py` | Infrastructure | Implementar `PdfReportExporter` (usar `reportlab`) |
| `backend/src/presentation/schemas/report.py` | Presentation | Crear — schemas `ReportResult`, `ReportStatusQuery` |
| `backend/src/presentation/api/v1/reports.py` | Presentation | Crear — router `GET /reports/status` |
| `backend/src/presentation/dependencies.py` | Presentation | Añadir `get_generate_report_use_case` |

---

## Firmas principales

### `domain/entities/document.py` — valor `DocumentStatus` (value object)

```python
from enum import Enum

class DocumentStatus(str, Enum):
    VIGENTE = "vigente"
    PROXIMA_A_CADUCAR = "proxima_a_caducar"
    CADUCADA = "caducada"
```

### `application/ports/document_repository.py` — método añadido

```python
class AbstractDocumentRepository(ABC):
    # ... existente ...
    @abstractmethod
    def get_all_active(self) -> list[Document]:
        """Devuelve todos los documentos con deleted_at nulo, sin filtrar por categoría."""
        ...
```

### `application/ports/report_exporter.py` — nuevo puerto

```python
from abc import ABC, abstractmethod

from application.use_cases.generate_report import ReportResult

class AbstractReportExporter(ABC):
    @abstractmethod
    def to_csv(self, result: ReportResult) -> bytes: ...

    @abstractmethod
    def to_pdf(self, result: ReportResult) -> bytes: ...
```

### `application/use_cases/generate_report.py`

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime

from domain.entities.document import Document, DocumentStatus

@dataclass
class ReportSection:
    estado: DocumentStatus
    documentos: list[Document]
    dias_hasta_caducidad: dict[str, int]  # document_id -> dias

@dataclass
class ReportResult:
    generated_at: datetime
    sections: list[ReportSection]  # una por cada estado (vigente, proxima_a_caducar, caducada)

class GenerateReportUseCase:
    UMBRAL_PROXIMA_A_CADUCAR_DIAS = 30

    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    def execute(self, categoria: str | None, fecha_referencia: date) -> ReportResult:
        all_docs = self._repository.get_all_active()
        if categoria is not None:
            all_docs = [d for d in all_docs if d.categoria == categoria]

        secciones = []
        for estado in DocumentStatus:
            docs_estado = [
                d for d in all_docs
                if self._clasificar(d.fecha_caducidad, fecha_referencia) == estado
            ]
            dias = {d.id: (d.fecha_caducidad - fecha_referencia).days for d in docs_estado}
            secciones.append(ReportSection(estado=estado, documentos=docs_estado, dias_hasta_caducidad=dias))

        return ReportResult(generated_at=datetime.utcnow(), sections=secciones)

    @staticmethod
    def _clasificar(fecha_caducidad: date, referencia: date) -> DocumentStatus:
        delta = (fecha_caducidad - referencia).days
        if delta > GenerateReportUseCase.UMBRAL_PROXIMA_A_CADUCAR_DIAS:
            return DocumentStatus.VIGENTE
        if delta < 0:
            return DocumentStatus.CADUCADA
        return DocumentStatus.PROXIMA_A_CADUCAR
```

### `infrastructure/export/csv_report_exporter.py`

```python
from application.ports.report_exporter import AbstractReportExporter
from application.use_cases.generate_report import ReportResult
import csv
import io

class CsvReportExporter(AbstractReportExporter):
    def to_csv(self, result: ReportResult) -> bytes:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "nombre_archivo", "categoria", "fecha_validez", "fecha_caducidad", "estado", "dias_hasta_caducidad"])
        for section in result.sections:
            for doc in section.documentos:
                dias = section.dias_hasta_caducidad[doc.id]
                writer.writerow([
                    str(doc.id), doc.nombre_archivo, doc.categoria or "",
                    doc.fecha_validez.isoformat(), doc.fecha_caducidad.isoformat(),
                    section.estado.value, dias
                ])
        return output.getvalue().encode("utf-8")
```

### `infrastructure/export/pdf_report_exporter.py`

```python
from application.ports.report_exporter import AbstractReportExporter
from application.use_cases.generate_report import ReportResult
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

class PdfReportExporter(AbstractReportExporter):
    def to_pdf(self, result: ReportResult) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Informe de Estado Documental", styles["Title"]))
        elements.append(Paragraph(f"Generado: {result.generated_at:%Y-%m-%d %H:%M:%S}", styles["Normal"]))

        for section in result.sections:
            elements.append(Paragraph(section.estado.value.upper(), styles["Heading2"]))
            data = [["id", "nombre_archivo", "categoria", "fecha_caducidad"]]
            for doc in section.documentos:
                data.append([str(doc.id), doc.nombre_archivo, doc.categoria or "", doc.fecha_caducidad.isoformat()])
            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

        doc.build(elements)
        return buffer.getvalue()
```

### `presentation/schemas/report.py`

```python
from datetime import date, datetime

from pydantic import BaseModel

class ReportStatusQuery(BaseModel):
    formato: str  # "csv" | "pdf"
    categoria: str | None = None

class ReportStatusResponse(BaseModel):
    generated_at: datetime
```

### `presentation/api/v1/reports.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from application.use_cases.generate_report import GenerateReportUseCase
from application.ports.report_exporter import AbstractReportExporter
from application.ports.document_repository import AbstractDocumentRepository
from presentation.dependencies import get_generate_report_use_case, get_report_exporter
from presentation.schemas.report import ReportStatusQuery

VALID_FORMATS = {"csv", "pdf"}

@router.get("/status")
async def get_report_status(
    formato: str = Query(..., description="Formato de exportación: csv o pdf"),
    categoria: str | None = Query(None, description="Filtrar por categoría"),
    use_case: GenerateReportUseCase = Depends(get_generate_report_use_case),
    exporter: AbstractReportExporter = Depends(get_report_exporter),
) -> StreamingResponse:
    if formato not in VALID_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato '{formato}' no soportado. Formatos válidos: {', '.join(sorted(VALID_FORMATS))}",
        )

    result = use_case.execute(categoria=categoria, fecha_referencia=date.today())

    if formato == "csv":
        content = exporter.to_csv(result)
        from datetime import datetime as dt
        timestamp = result.generated_at.strftime("%Y-%m-%d_%H%M%S")
        return StreamingResponse(
            iter([content]),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="informe_estado_{timestamp}.csv"',
            },
        )

    content = exporter.to_pdf(result)
    return StreamingResponse(
        iter([content]),
        media_type="application/pdf",
    )
```

---

## Decisiones de diseño

### Clasificación en el use case, no en el dominio

La lógica de clasificación por fecha vive en `GenerateReportUseCase.execute()`, no en la entidad `Document` ni en un value object. Se decidió así porque:

1. La clasificación depende de un umbral configurable (30 días) que es específico del caso de uso de informes, no una regla universal de negocio.
2. El dominio `Document` es inmutable (frozen dataclass); añadir lógica de clasificación mutaría el estado.
3. Mantener la clasificación en el use case permite cambiar el umbral sin modificar entidades.

### Repositorio con `get_all_active()`

Se añade `get_all_active()` en `AbstractDocumentRepository` en lugar de reutilizar `get_by_id()`. El motivo es que el informe necesita todos los documentos activos sin paginar; un repositorio de solo lectura para informes es el patrón más limpio.

### Alternativa descartada: clasificación en SQL

**Alternativa:** Realizar la clasificación en la query SQL usando expresiones de fecha.

**Por qué se eligió la clasificación en Python:** El código es más legible, easier to test unitariamente, y el volumen de documentos del MVP no justifica el impacto de rendimiento de clasificar en memoria. Si en el futuro el volumen crece significativamente, se puede mover la clasificación a la query con un CASE WHEN en SQL.

### Alternativa descartada: exportar a Excel

**Alternativa:** Soportar formato XLSX además de CSV y PDF.

**Por qué se eligió no soportarlo:** El enunciado de la feature solo menciona CSV y PDF. Añadir `openpyxl` como dependencia no aporta valor en el MVP.

---

## Logger

El logger vive en infraestructura. Los eventos de generación de informes se registrarán cuando la feature `audit_log` esté implementada, añadiendo el evento `report.generated` con `formato`, `categoria` y `document_count` al contexto de logging.