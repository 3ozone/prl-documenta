"""Equipment categories router for equipment documents."""
from __future__ import annotations

import logging
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from application.use_cases.upload_equipment_document import (
    UploadEquipmentDocumentCommand,
    UploadEquipmentDocumentUseCase,
)
from application.use_cases.list_equipment_documents import (
    ListEquipmentDocumentsCommand,
    ListEquipmentDocumentsUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField
from domain.value_objects.equipment_subtype import EquipmentSubtype
from domain.value_objects.maintenance_type import MaintenanceType
from domain.value_objects.inspection_result import InspectionResult
from presentation.dependencies import get_upload_equipment_document_use_case, get_list_equipment_documents_use_case, require_admin, require_viewer_or_admin
from domain.entities.user import User
from presentation.schemas.document import (
    EquipmentDocumentResponse,
    PaginatedEquipmentDocumentsResponse,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/categories/equipos", tags=["categories"])


@router.post("/documents", status_code=201, response_model=EquipmentDocumentResponse)
async def upload_equipment_document(
    request: Request,
    nombre_archivo: str = Form(...),
    formato: str = Form(...),
    fecha_validez: date = Form(...),
    fecha_caducidad: date = Form(...),
    id_equipo: str = Form(...),
    nombre_equipo: str = Form(...),
    numero_serie: str | None = Form(default=None),
    ubicacion: str | None = Form(default=None),
    subtipo: str | None = Form(default=None),
    tipo_mantenimiento: str | None = Form(default=None),
    empresa_mantenedora: str | None = Form(default=None),
    fecha_proximo_mantenimiento: date | None = Form(default=None),
    organismo_inspector: str | None = Form(default=None),
    resultado_inspeccion: str | None = Form(default=None),
    fecha_proxima_inspeccion: date | None = Form(default=None),
    file: UploadFile = ...,
    use_case: UploadEquipmentDocumentUseCase = Depends(get_upload_equipment_document_use_case),
    _current_user: User = Depends(require_admin),
) -> JSONResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=422,
            detail=f"Content-Type no admitido: '{file.content_type}'. Se requiere application/pdf.",
        )

    content = await file.read()

    subtipo_enum = None
    if subtipo:
        try:
            subtipo_enum = EquipmentSubtype(subtipo)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Subtipo '{subtipo}' no válido. Valores permitidos: mantenimiento, inspeccion.",
            )

    tipo_mantenimiento_enum = None
    if tipo_mantenimiento:
        try:
            tipo_mantenimiento_enum = MaintenanceType(tipo_mantenimiento)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Tipo mantenimiento '{tipo_mantenimiento}' no válido. Valores permitidos: preventivo, correctivo.",
            )

    resultado_inspeccion_enum = None
    if resultado_inspeccion:
        try:
            resultado_inspeccion_enum = InspectionResult(resultado_inspeccion)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Resultado inspeccion '{resultado_inspeccion}' no válido. Valores permitidos: favorable, condicionado, desfavorable.",
            )

    try:
        result = use_case.execute(
            UploadEquipmentDocumentCommand(
                nombre_archivo=nombre_archivo,
                formato=formato,
                fecha_validez=fecha_validez,
                fecha_caducidad=fecha_caducidad,
                content=content,
                id_equipo=id_equipo,
                nombre_equipo=nombre_equipo,
                numero_serie=numero_serie,
                ubicacion=ubicacion,
                subtipo=subtipo_enum,
                tipo_mantenimiento=tipo_mantenimiento_enum,
                empresa_mantenedora=empresa_mantenedora,
                fecha_proximo_mantenimiento=fecha_proximo_mantenimiento,
                organismo_inspector=organismo_inspector,
                resultado_inspeccion=resultado_inspeccion_enum,
                fecha_proxima_inspeccion=fecha_proxima_inspeccion,
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
            "Unexpected error during equipment document upload",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return JSONResponse(
        status_code=201,
        content=EquipmentDocumentResponse(
            id=result.id,
            nombre_archivo=result.nombre_archivo,
            formato=result.formato,
            fecha_validez=result.fecha_validez,
            fecha_caducidad=result.fecha_caducidad,
            categoria="equipos",
            id_equipo=result.id_equipo,
            nombre_equipo=result.nombre_equipo,
            numero_serie=result.numero_serie,
            ubicacion=result.ubicacion,
            subtipo=result.subtipo,
            tipo_mantenimiento=result.tipo_mantenimiento,
            empresa_mantenedora=result.empresa_mantenedora,
            fecha_proximo_mantenimiento=result.fecha_proximo_mantenimiento,
            organismo_inspector=result.organismo_inspector,
            resultado_inspeccion=result.resultado_inspeccion,
            fecha_proxima_inspeccion=result.fecha_proxima_inspeccion,
            storage_path=result.storage_path,
            uploaded_by=result.uploaded_by,
        ).model_dump(mode="json"),
    )


@router.get("/documents", response_model=PaginatedEquipmentDocumentsResponse)
async def list_equipment_documents(
    request: Request,
    page: int = 1,
    per_page: int = 20,
    id_equipo: str | None = None,
    use_case: ListEquipmentDocumentsUseCase = Depends(get_list_equipment_documents_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> JSONResponse:
    try:
        result = use_case.execute(
            ListEquipmentDocumentsCommand(
                id_equipo=id_equipo,
                page=page,
                per_page=per_page,
            )
        )
    except Exception as exc:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        log.error(
            "Unexpected error during equipment document listing",
            extra={"request_id": request_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    items = [
        EquipmentDocumentResponse(
            id=doc.id,
            nombre_archivo=doc.nombre_archivo,
            formato=doc.formato,
            fecha_validez=doc.fecha_validez,
            fecha_caducidad=doc.fecha_caducidad,
            categoria=doc.categoria or "equipos",
            id_equipo=doc.id_equipo or "",
            nombre_equipo=doc.nombre_equipo or "",
            numero_serie=doc.numero_serie,
            ubicacion=doc.ubicacion,
            subtipo=EquipmentSubtype(doc.subtipo) if doc.subtipo else None,
            tipo_mantenimiento=MaintenanceType(doc.tipo_mantenimiento) if doc.tipo_mantenimiento else None,
            empresa_mantenedora=doc.empresa_mantenedora,
            fecha_proximo_mantenimiento=doc.fecha_proximo_mantenimiento,
            organismo_inspector=doc.organismo_inspector,
            resultado_inspeccion=InspectionResult(doc.resultado_inspeccion) if doc.resultado_inspeccion else None,
            fecha_proxima_inspeccion=doc.fecha_proxima_inspeccion,
            storage_path="",
            uploaded_by=doc.uploaded_by,
        )
        for doc in result.documents
    ]

    return JSONResponse(
        status_code=200,
        content=PaginatedEquipmentDocumentsResponse(
            items=items,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
        ).model_dump(mode="json"),
    )