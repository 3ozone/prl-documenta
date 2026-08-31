"""Worker categories router for worker documents."""
from __future__ import annotations

import logging
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from application.use_cases.upload_worker_document import (
    UploadWorkerDocumentCommand,
    UploadWorkerDocumentUseCase,
)
from application.use_cases.list_worker_documents import (
    ListWorkerDocumentsCommand,
    ListWorkerDocumentsUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField
from domain.value_objects.worker_document_type import WorkerDocumentType
from domain.entities.user import User
from presentation.dependencies import (
    get_upload_worker_document_use_case,
    get_list_worker_documents_use_case,
    require_admin,
    require_viewer_or_admin,
)
from presentation.schemas.document import (
    WorkerDocumentResponse,
    PaginatedWorkerDocumentsResponse,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/categories/trabajadores", tags=["categories"])


@router.post("/documents", status_code=201, response_model=WorkerDocumentResponse)
async def upload_worker_document(
    request: Request,
    nombre_archivo: str = Form(...),
    formato: str = Form(...),
    fecha_validez: date = Form(...),
    fecha_caducidad: date = Form(...),
    nombre_trabajador: str = Form(...),
    dni: str = Form(...),
    puesto: str | None = Form(default=None),
    tipo_documento: str = Form(...),
    file: UploadFile = ...,
    use_case: UploadWorkerDocumentUseCase = Depends(get_upload_worker_document_use_case),
    _current_user: User = Depends(require_admin),
) -> JSONResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=422,
            detail=f"Content-Type no admitido: '{file.content_type}'. Se requiere application/pdf.",
        )

    try:
        tipo_enum = WorkerDocumentType(tipo_documento)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"tipo_documento no válido: '{tipo_documento}'. "
            f"Valores permitidos: {[e.value for e in WorkerDocumentType]}",
        )

    content = await file.read()

    try:
        result = use_case.execute(
            UploadWorkerDocumentCommand(
                nombre_archivo=nombre_archivo,
                formato=formato,
                fecha_validez=fecha_validez,
                fecha_caducidad=fecha_caducidad,
                content=content,
                nombre_trabajador=nombre_trabajador,
                dni=dni,
                puesto=puesto,
                tipo_documento=tipo_enum,
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
            "Unexpected error during worker document upload",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return JSONResponse(
        status_code=201,
        content=WorkerDocumentResponse(
            id=result.id,
            nombre_archivo=result.nombre_archivo,
            formato=result.formato,
            fecha_validez=result.fecha_validez,
            fecha_caducidad=result.fecha_caducidad,
            categoria="trabajadores",
            nombre_trabajador=result.nombre_trabajador,
            dni=result.dni,
            puesto=result.puesto,
            tipo_documento=result.tipo_documento,
            storage_path=result.storage_path,
            uploaded_by=result.uploaded_by,
        ).model_dump(mode="json"),
    )


@router.get("/documents", response_model=PaginatedWorkerDocumentsResponse)
async def list_worker_documents(
    request: Request,
    dni_trabajador: str | None = None,
    page: int = 1,
    per_page: int = 20,
    use_case: ListWorkerDocumentsUseCase = Depends(get_list_worker_documents_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> JSONResponse:
    try:
        result = use_case.execute(
            ListWorkerDocumentsCommand(
                dni_trabajador=dni_trabajador,
                page=page,
                per_page=per_page,
            )
        )
    except Exception as exc:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "Unexpected error during worker document listing",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    items = [
        WorkerDocumentResponse(
            id=doc.id,
            nombre_archivo=doc.nombre_archivo,
            formato=doc.formato,
            fecha_validez=doc.fecha_validez,
            fecha_caducidad=doc.fecha_caducidad,
            categoria=doc.categoria or "trabajadores",
            nombre_trabajador=doc.nombre_trabajador or "",
            dni=doc.dni or "",
            puesto=doc.puesto,
            tipo_documento=WorkerDocumentType(doc.tipo_documento) if doc.tipo_documento else WorkerDocumentType.FORMACION,
            storage_path="",
            uploaded_by=doc.uploaded_by,
        )
        for doc in result.documents
    ]

    return JSONResponse(
        status_code=200,
        content=PaginatedWorkerDocumentsResponse(
            items=items,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
        ).model_dump(mode="json"),
    )
