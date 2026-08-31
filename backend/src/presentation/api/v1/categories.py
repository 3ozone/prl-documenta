"""Categories router for company documents."""
from __future__ import annotations

import logging
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from application.use_cases.upload_company_document import (
    UploadCompanyDocumentCommand,
    UploadCompanyDocumentUseCase,
)
from application.use_cases.list_company_documents import (
    ListCompanyDocumentsCommand,
    ListCompanyDocumentsUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField
from domain.entities.user import User
from presentation.dependencies import get_upload_company_document_use_case, get_list_company_documents_use_case, require_admin, require_viewer_or_admin
from presentation.schemas.document import (
    CompanyDocumentResponse,
    PaginatedCompanyDocumentsResponse,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/categories/empresa", tags=["categories"])


@router.post("/documents", status_code=201, response_model=CompanyDocumentResponse)
async def upload_company_document(
    request: Request,
    nombre_archivo: str = Form(...),
    formato: str = Form(...),
    fecha_validez: date = Form(...),
    fecha_caducidad: date = Form(...),
    razon_social: str = Form(...),
    cif: str = Form(...),
    actividad_economica: str | None = Form(default=None),
    centro_trabajo: str | None = Form(default=None),
    file: UploadFile = ...,
    use_case: UploadCompanyDocumentUseCase = Depends(get_upload_company_document_use_case),
    _current_user: User = Depends(require_admin),
) -> JSONResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=422,
            detail=f"Content-Type no admitido: '{file.content_type}'. Se requiere application/pdf.",
        )

    content = await file.read()

    try:
        result = use_case.execute(
            UploadCompanyDocumentCommand(
                nombre_archivo=nombre_archivo,
                formato=formato,
                fecha_validez=fecha_validez,
                fecha_caducidad=fecha_caducidad,
                content=content,
                razon_social=razon_social,
                cif=cif,
                actividad_economica=actividad_economica,
                centro_trabajo=centro_trabajo,
            )
        )
    except MissingRequiredField as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except InvalidDocumentFormat as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except InvalidExpiryDate as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "Unexpected error during company document upload",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return JSONResponse(
        status_code=201,
        content=CompanyDocumentResponse(
            id=result.id,
            nombre_archivo=result.nombre_archivo,
            formato=result.formato,
            fecha_validez=result.fecha_validez,
            fecha_caducidad=result.fecha_caducidad,
            categoria=result.categoria,
            razon_social=result.razon_social,
            cif=result.cif,
            actividad_economica=result.actividad_economica,
            centro_trabajo=result.centro_trabajo,
            storage_path=result.storage_path,
            uploaded_by=result.uploaded_by,
        ).model_dump(mode="json"),
    )


@router.get("/documents", response_model=PaginatedCompanyDocumentsResponse)
async def list_company_documents(
    request: Request,
    page: int = 1,
    per_page: int = 20,
    estado: str | None = None,
    use_case: ListCompanyDocumentsUseCase = Depends(get_list_company_documents_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> JSONResponse:
    if estado is not None and estado not in ("vigente", "caducada"):
        raise HTTPException(
            status_code=422,
            detail="Parámetro 'estado' debe ser 'vigente' o 'caducada'",
        )

    try:
        result = use_case.execute(
            ListCompanyDocumentsCommand(
                page=page,
                per_page=per_page,
                estado=estado,
            )
        )
    except Exception as exc:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "Unexpected error during company document listing",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    items = [
        CompanyDocumentResponse(
            id=doc.id,
            nombre_archivo=doc.nombre_archivo,
            formato=doc.formato,
            fecha_validez=doc.fecha_validez,
            fecha_caducidad=doc.fecha_caducidad,
            categoria=doc.categoria or "empresa",
            razon_social=doc.razon_social or "",
            cif=doc.cif or "",
            actividad_economica=doc.actividad_economica,
            centro_trabajo=doc.centro_trabajo,
            storage_path="",  # not exposed in list response
            uploaded_by=doc.uploaded_by,
        )
        for doc in result.documents
    ]

    return JSONResponse(
        status_code=200,
        content=PaginatedCompanyDocumentsResponse(
            items=items,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
        ).model_dump(mode="json"),
    )