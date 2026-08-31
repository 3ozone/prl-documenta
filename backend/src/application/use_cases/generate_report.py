"""Generate report use case."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from domain.entities.document import Document, DocumentStatus
from application.ports.document_repository import AbstractDocumentRepository


@dataclass
class ReportSection:
    estado: DocumentStatus
    documentos: list[Document]
    dias_hasta_caducidad: dict[str, int]


@dataclass
class ReportResult:
    generated_at: datetime
    sections: list[ReportSection]


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
            dias = {str(d.id): (d.fecha_caducidad - fecha_referencia).days for d in docs_estado}
            secciones.append(ReportSection(estado=estado, documentos=docs_estado, dias_hasta_caducidad=dias))

        return ReportResult(generated_at=datetime.now(timezone.utc), sections=secciones)

    @staticmethod
    def _clasificar(fecha_caducidad: date, referencia: date) -> DocumentStatus:
        delta = (fecha_caducidad - referencia).days
        if delta > GenerateReportUseCase.UMBRAL_PROXIMA_A_CADUCAR_DIAS:
            return DocumentStatus.VIGENTE
        if delta < 0:
            return DocumentStatus.CADUCADA
        return DocumentStatus.PROXIMA_A_CADUCAR
