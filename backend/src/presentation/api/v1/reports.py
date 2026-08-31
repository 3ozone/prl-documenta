"""Reports router."""
from __future__ import annotations

import logging
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from application.use_cases.generate_report import GenerateReportUseCase
from application.ports.report_exporter import AbstractReportExporter
from presentation.dependencies import get_generate_report_use_case, get_report_exporter, require_viewer_or_admin
from domain.entities.user import User

log = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["reports"])

VALID_FORMATS = {"csv", "pdf"}


@router.get("/status")
async def get_report_status(
    request: Request,
    formato: str = Query(..., description="Formato de exportación: csv o pdf"),
    categoria: str | None = Query(None, description="Filtrar por categoría"),
    use_case: GenerateReportUseCase = Depends(get_generate_report_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> StreamingResponse:
    # TODO: cuando auth (id:9) esté, añadir Depends(get_current_session)
    if formato not in VALID_FORMATS:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "report.invalid_format",
            extra={"request_id": request_id, "formato": formato},
        )
        raise HTTPException(
            status_code=400,
            detail=f"Formato '{formato}' no soportado. Formatos válidos: {', '.join(sorted(VALID_FORMATS))}",
        )

    exporter: AbstractReportExporter = get_report_exporter(formato)
    result = use_case.execute(categoria=categoria, fecha_referencia=date.today())

    if formato == "csv":
        content = exporter.to_csv(result)
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
