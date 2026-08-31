"""Pydantic schemas for document endpoints."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel

from domain.value_objects.worker_document_type import WorkerDocumentType
from domain.value_objects.equipment_subtype import EquipmentSubtype
from domain.value_objects.maintenance_type import MaintenanceType
from domain.value_objects.inspection_result import InspectionResult


class UploadDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str | None = None


class UploadDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    categoria: str | None = None
    uploaded_by: UUID | None = None


class CompanyDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    razon_social: str
    cif: str
    actividad_economica: str | None = None
    centro_trabajo: str | None = None


class CompanyDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "empresa"
    razon_social: str
    cif: str
    actividad_economica: str | None = None
    centro_trabajo: str | None = None
    storage_path: str
    uploaded_by: UUID | None = None


class PaginatedCompanyDocumentsResponse(BaseModel):
    items: list[CompanyDocumentResponse]
    total: int
    page: int
    per_page: int


class WorkerDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    nombre_trabajador: str
    dni: str
    puesto: str | None = None
    tipo_documento: WorkerDocumentType


class WorkerDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "trabajadores"
    nombre_trabajador: str
    dni: str
    puesto: str | None = None
    tipo_documento: WorkerDocumentType
    storage_path: str
    uploaded_by: UUID | None = None


class PaginatedWorkerDocumentsResponse(BaseModel):
    items: list[WorkerDocumentResponse]
    total: int
    page: int
    per_page: int


class EquipmentDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
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


class EquipmentDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "equipos"
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
    storage_path: str
    uploaded_by: UUID | None = None


class PaginatedEquipmentDocumentsResponse(BaseModel):
    items: list[EquipmentDocumentResponse]
    total: int
    page: int
    per_page: int
