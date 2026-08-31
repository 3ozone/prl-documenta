"""Upload equipment document use case."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from application.ports.document_repository import AbstractDocumentRepository
from application.ports.file_storage import AbstractFileStorage
from domain.entities.document import Document
from domain.exceptions import InvalidDocumentFormat, MissingRequiredField
from domain.value_objects.expiry_date import ExpiryDate
from domain.value_objects.equipment_subtype import EquipmentSubtype
from domain.value_objects.maintenance_type import MaintenanceType
from domain.value_objects.inspection_result import InspectionResult

ALLOWED_FORMATS: frozenset[str] = frozenset({"pdf"})


@dataclass
class UploadEquipmentDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    id_equipo: str
    nombre_equipo: str
    numero_serie: str | None = None
    ubicacion: str | None = None
    subtipo: EquipmentSubtype | None = None
    tipo_mantenimiento: MaintenanceType | None = None
    empresa_mantenedora: str | None = None
    fecha_proximo_mantenimiento: date | None = None
    organismo_inspector: str | None = None
    resultado_inspeccion: InspectionResult | None = None
    fecha_proxima_inspeccion: date | None = None
    uploaded_by: UUID | None = None


@dataclass
class UploadEquipmentDocumentResult:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    id_equipo: str
    nombre_equipo: str
    numero_serie: str | None
    ubicacion: str | None
    subtipo: EquipmentSubtype | None
    tipo_mantenimiento: MaintenanceType | None
    empresa_mantenedora: str | None
    fecha_proximo_mantenimiento: date | None
    organismo_inspector: str | None
    resultado_inspeccion: InspectionResult | None
    fecha_proxima_inspeccion: date | None
    uploaded_by: UUID | None = None


class UploadEquipmentDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadEquipmentDocumentCommand) -> UploadEquipmentDocumentResult:
        if not command.id_equipo:
            raise MissingRequiredField("id_equipo es obligatorio para documentos de equipo")

        if not command.nombre_equipo:
            raise MissingRequiredField("nombre_equipo es obligatorio para documentos de equipo")

        if command.formato not in ALLOWED_FORMATS:
            raise InvalidDocumentFormat(
                f"Formato no admitido: '{command.formato}'. "
                f"Formatos permitidos: {sorted(ALLOWED_FORMATS)}"
            )

        ExpiryDate(
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
        )

        if command.subtipo == EquipmentSubtype.MANTENIMIENTO:
            if not command.tipo_mantenimiento:
                raise MissingRequiredField("tipo_mantenimiento es obligatorio para subtipo mantenimiento")
            if not command.empresa_mantenedora:
                raise MissingRequiredField("empresa_mantenedora es obligatorio para subtipo mantenimiento")
            if not command.fecha_proximo_mantenimiento:
                raise MissingRequiredField("fecha_proximo_mantenimiento es obligatorio para subtipo mantenimiento")

        if command.subtipo == EquipmentSubtype.INSPECCION:
            if not command.organismo_inspector:
                raise MissingRequiredField("organismo_inspector es obligatorio para subtipo inspeccion")
            if not command.resultado_inspeccion:
                raise MissingRequiredField("resultado_inspeccion es obligatorio para subtipo inspeccion")
            if not command.fecha_proxima_inspeccion:
                raise MissingRequiredField("fecha_proxima_inspeccion es obligatorio para subtipo inspeccion")

        document_id = uuid.uuid4()

        storage_path = self._storage.save(document_id, command.content)

        document = Document(
            id=document_id,
            nombre_archivo=command.nombre_archivo,
            formato=command.formato,
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
            categoria="equipos",
            uploaded_by=command.uploaded_by,
            id_equipo=command.id_equipo,
            nombre_equipo=command.nombre_equipo,
            numero_serie=command.numero_serie,
            ubicacion=command.ubicacion,
            subtipo=command.subtipo.value if command.subtipo else None,
            tipo_mantenimiento=command.tipo_mantenimiento.value if command.tipo_mantenimiento else None,
            empresa_mantenedora=command.empresa_mantenedora,
            fecha_proximo_mantenimiento=command.fecha_proximo_mantenimiento,
            organismo_inspector=command.organismo_inspector,
            resultado_inspeccion=command.resultado_inspeccion.value if command.resultado_inspeccion else None,
            fecha_proxima_inspeccion=command.fecha_proxima_inspeccion,
        )

        try:
            self._repository.save_equipment_document(document)
        except Exception:
            self._storage.delete(document_id)
            raise

        return UploadEquipmentDocumentResult(
            id=document_id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            storage_path=storage_path,
            id_equipo=document.id_equipo or "",
            nombre_equipo=document.nombre_equipo or "",
            numero_serie=document.numero_serie,
            ubicacion=document.ubicacion,
            subtipo=command.subtipo,
            tipo_mantenimiento=command.tipo_mantenimiento,
            empresa_mantenedora=command.empresa_mantenedora,
            fecha_proximo_mantenimiento=command.fecha_proximo_mantenimiento,
            organismo_inspector=command.organismo_inspector,
            resultado_inspeccion=command.resultado_inspeccion,
            fecha_proxima_inspeccion=command.fecha_proxima_inspeccion,
            uploaded_by=document.uploaded_by,
        )