"""Documents router."""
from __future__ import annotations

import logging
from datetime import date
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from application.use_cases.upload_document import UploadDocumentCommand, UploadDocumentUseCase
from application.use_cases.download_document import DownloadDocumentUseCase
from domain.exceptions import DocumentNotFound, InvalidDocumentCategory, InvalidDocumentFormat, InvalidExpiryDate
from presentation.dependencies import get_upload_document_use_case, get_download_document_use_case, require_admin, require_viewer_or_admin, get_db
from domain.entities.user import User
from presentation.schemas.document import UploadDocumentResponse
from infrastructure.db.repositories.document_repository import SqlDocumentRepository
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[UploadDocumentResponse])
async def list_documents(
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_viewer_or_admin),
) -> JSONResponse:
    repository = SqlDocumentRepository(db)
    docs = repository.get_all_active()
    return JSONResponse(
        status_code=200,
        content=[
            UploadDocumentResponse(
                id=doc.id,
                nombre_archivo=doc.nombre_archivo,
                formato=doc.formato,
                fecha_validez=doc.fecha_validez,
                fecha_caducidad=doc.fecha_caducidad,
                storage_path=doc.storage_path,
                categoria=doc.categoria,
                uploaded_by=doc.uploaded_by,
            ).model_dump(mode="json")
            for doc in docs
        ],
    )


@router.post("", status_code=201, response_model=UploadDocumentResponse)
async def upload_document(
    request: Request,
    nombre_archivo: str = Form(...),
    formato: str = Form(...),
    fecha_validez: date = Form(...),
    fecha_caducidad: date = Form(...),
    categoria: str | None = Form(default=None),
    file: UploadFile = ...,
    use_case: UploadDocumentUseCase = Depends(get_upload_document_use_case),
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
            UploadDocumentCommand(
                nombre_archivo=nombre_archivo,
                formato=formato,
                fecha_validez=fecha_validez,
                fecha_caducidad=fecha_caducidad,
                content=content,
                categoria=categoria,
            )
        )
    except InvalidDocumentFormat as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except InvalidDocumentCategory as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except InvalidExpiryDate as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "Unexpected error during document upload",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return JSONResponse(
        status_code=201,
        content=UploadDocumentResponse(
            id=result.id,
            nombre_archivo=result.nombre_archivo,
            formato=result.formato,
            fecha_validez=result.fecha_validez,
            fecha_caducidad=result.fecha_caducidad,
            storage_path=result.storage_path,
            categoria=result.categoria,
            uploaded_by=result.uploaded_by,
        ).model_dump(mode="json"),
    )


@router.get("/{document_id}/download")
async def download_document(
    request: Request,
    document_id: UUID,
    use_case: DownloadDocumentUseCase = Depends(get_download_document_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> StreamingResponse:
    try:
        result = use_case.execute(document_id)
    except DocumentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return StreamingResponse(
        iter([result.content]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{result.nombre_archivo}"',
        },
    )
