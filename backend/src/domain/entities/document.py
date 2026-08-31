"""Document entity."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from domain.entities.document_status import DocumentStatus


@dataclass(frozen=True)
class Document:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str | None = None
    uploaded_by: UUID | None = None
    razon_social: str | None = None
    cif: str | None = None
    actividad_economica: str | None = None
    centro_trabajo: str | None = None
    nombre_trabajador: str | None = None
    dni: str | None = None
    puesto: str | None = None
    tipo_documento: str | None = None
    id_equipo: str | None = None
    nombre_equipo: str | None = None
    numero_serie: str | None = None
    ubicacion: str | None = None
    subtipo: str | None = None
    tipo_mantenimiento: str | None = None
    empresa_mantenedora: str | None = None
    fecha_proximo_mantenimiento: date | None = None
    organismo_inspector: str | None = None
    resultado_inspeccion: str | None = None
    fecha_proxima_inspeccion: date | None = None


__all__ = ["Document", "DocumentStatus"]
