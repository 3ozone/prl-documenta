"""SQLAlchemy models."""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy.types import Date, Uuid


class Base(DeclarativeBase):
    pass


class DocumentModel(Base):
    __tablename__ = "documents"

    id: MappedColumn[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_archivo: MappedColumn[str] = mapped_column(String(255), nullable=False)
    formato: MappedColumn[str] = mapped_column(String(20), nullable=False)
    fecha_validez: MappedColumn[date] = mapped_column(Date, nullable=False)
    fecha_caducidad: MappedColumn[date] = mapped_column(Date, nullable=False)
    categoria: MappedColumn[str | None] = mapped_column(String(50), nullable=True)
    uploaded_by: MappedColumn[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    deleted_at: MappedColumn[datetime | None] = mapped_column(DateTime, nullable=True)
    razon_social: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    cif: MappedColumn[str | None] = mapped_column(String(20), nullable=True)
    actividad_economica: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    centro_trabajo: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    nombre_trabajador: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    dni: MappedColumn[str | None] = mapped_column(String(20), nullable=True)
    puesto: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    tipo_documento: MappedColumn[str | None] = mapped_column(String(50), nullable=True)
    id_equipo: MappedColumn[str | None] = mapped_column(String(100), nullable=True)
    nombre_equipo: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    numero_serie: MappedColumn[str | None] = mapped_column(String(100), nullable=True)
    ubicacion: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    subtipo: MappedColumn[str | None] = mapped_column(String(50), nullable=True)
    tipo_mantenimiento: MappedColumn[str | None] = mapped_column(String(50), nullable=True)
    empresa_mantenedora: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    fecha_proximo_mantenimiento: MappedColumn[date | None] = mapped_column(Date, nullable=True)
    organismo_inspector: MappedColumn[str | None] = mapped_column(String(255), nullable=True)
    resultado_inspeccion: MappedColumn[str | None] = mapped_column(String(50), nullable=True)
    fecha_proxima_inspeccion: MappedColumn[date | None] = mapped_column(Date, nullable=True)


class UserModel(Base):
    __tablename__ = "users"

    id: MappedColumn[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: MappedColumn[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: MappedColumn[str] = mapped_column(String(255), nullable=False)
    role: MappedColumn[str] = mapped_column(String(20), nullable=False)
    is_active: MappedColumn[bool] = mapped_column(nullable=False, default=True)
