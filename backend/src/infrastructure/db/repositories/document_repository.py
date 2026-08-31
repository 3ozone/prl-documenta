"""SQL document repository."""
from __future__ import annotations

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from application.ports.document_repository import AbstractDocumentRepository
from domain.entities.document import Document
from infrastructure.db.models import DocumentModel


class SqlDocumentRepository(AbstractDocumentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, document: Document) -> None:
        model = DocumentModel(
            id=document.id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            categoria=document.categoria,
            uploaded_by=document.uploaded_by,
        )
        self._session.add(model)
        self._session.commit()

    def save_company_document(self, document: Document) -> None:
        model = DocumentModel(
            id=document.id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            categoria="empresa",
            uploaded_by=document.uploaded_by,
            razon_social=document.razon_social,
            cif=document.cif,
            actividad_economica=document.actividad_economica,
            centro_trabajo=document.centro_trabajo,
        )
        self._session.add(model)
        self._session.commit()

    def exists(self, document_id: UUID) -> bool:
        return self._session.get(DocumentModel, document_id) is not None

    def get_by_id(self, document_id: UUID) -> Document | None:
        model = self._session.get(DocumentModel, document_id)
        if model is None or model.deleted_at is not None:
            return None
        return Document(
            id=model.id,
            nombre_archivo=model.nombre_archivo,
            formato=model.formato,
            fecha_validez=model.fecha_validez,
            fecha_caducidad=model.fecha_caducidad,
            categoria=model.categoria,
            uploaded_by=model.uploaded_by,
        )

    def get_all_active(self) -> list[Document]:
        models = self._session.query(DocumentModel).filter(DocumentModel.deleted_at.is_(None)).all()
        return [
            Document(
                id=m.id,
                nombre_archivo=m.nombre_archivo,
                formato=m.formato,
                fecha_validez=m.fecha_validez,
                fecha_caducidad=m.fecha_caducidad,
                categoria=m.categoria,
                uploaded_by=m.uploaded_by,
            )
            for m in models
        ]

    def get_company_documents(
        self, page: int, per_page: int, estado: str | None
    ) -> tuple[list[Document], int]:
        query = self._session.query(DocumentModel).filter(
            DocumentModel.categoria == "empresa",
            DocumentModel.deleted_at.is_(None),
        )

        if estado == "vigente":
            query = query.filter(DocumentModel.fecha_caducidad > date.today())
        elif estado == "caducada":
            query = query.filter(DocumentModel.fecha_caducidad <= date.today())

        total = query.count()
        offset = (page - 1) * per_page
        models = query.offset(offset).limit(per_page).all()

        documents = [
            Document(
                id=m.id,
                nombre_archivo=m.nombre_archivo,
                formato=m.formato,
                fecha_validez=m.fecha_validez,
                fecha_caducidad=m.fecha_caducidad,
                categoria=m.categoria,
                uploaded_by=m.uploaded_by,
                razon_social=m.razon_social,
                cif=m.cif,
                actividad_economica=m.actividad_economica,
                centro_trabajo=m.centro_trabajo,
            )
            for m in models
        ]
        return documents, total

    def save_worker_document(self, document: Document) -> None:
        model = DocumentModel(
            id=document.id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            categoria="trabajadores",
            uploaded_by=document.uploaded_by,
            nombre_trabajador=document.nombre_trabajador,
            dni=document.dni,
            puesto=document.puesto,
            tipo_documento=document.tipo_documento,
        )
        self._session.add(model)
        self._session.commit()

    def get_worker_documents(
        self, dni_trabajador: str | None, page: int, per_page: int
    ) -> tuple[list[Document], int]:
        query = self._session.query(DocumentModel).filter(
            DocumentModel.categoria == "trabajadores",
            DocumentModel.deleted_at.is_(None),
        )

        if dni_trabajador is not None:
            query = query.filter(DocumentModel.dni == dni_trabajador)

        total = query.count()
        offset = (page - 1) * per_page
        models = query.offset(offset).limit(per_page).all()

        documents = [
            Document(
                id=m.id,
                nombre_archivo=m.nombre_archivo,
                formato=m.formato,
                fecha_validez=m.fecha_validez,
                fecha_caducidad=m.fecha_caducidad,
                categoria=m.categoria,
                uploaded_by=m.uploaded_by,
                nombre_trabajador=m.nombre_trabajador,
                dni=m.dni,
                puesto=m.puesto,
                tipo_documento=m.tipo_documento,
            )
            for m in models
        ]
        return documents, total

    def save_equipment_document(self, document: Document) -> None:
        model = DocumentModel(
            id=document.id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            categoria="equipos",
            uploaded_by=document.uploaded_by,
            id_equipo=document.id_equipo,
            nombre_equipo=document.nombre_equipo,
            numero_serie=document.numero_serie,
            ubicacion=document.ubicacion,
            subtipo=document.subtipo,
            tipo_mantenimiento=document.tipo_mantenimiento,
            empresa_mantenedora=document.empresa_mantenedora,
            fecha_proximo_mantenimiento=document.fecha_proximo_mantenimiento,
            organismo_inspector=document.organismo_inspector,
            resultado_inspeccion=document.resultado_inspeccion,
            fecha_proxima_inspeccion=document.fecha_proxima_inspeccion,
        )
        self._session.add(model)
        self._session.commit()

    def get_equipment_documents(
        self, id_equipo: str | None, page: int, per_page: int
    ) -> tuple[list[Document], int]:
        query = self._session.query(DocumentModel).filter(
            DocumentModel.categoria == "equipos",
            DocumentModel.deleted_at.is_(None),
        )

        if id_equipo is not None:
            query = query.filter(DocumentModel.id_equipo == id_equipo)

        total = query.count()
        offset = (page - 1) * per_page
        models = query.offset(offset).limit(per_page).all()

        documents = [
            Document(
                id=m.id,
                nombre_archivo=m.nombre_archivo,
                formato=m.formato,
                fecha_validez=m.fecha_validez,
                fecha_caducidad=m.fecha_caducidad,
                categoria=m.categoria,
                uploaded_by=m.uploaded_by,
                id_equipo=m.id_equipo,
                nombre_equipo=m.nombre_equipo,
                numero_serie=m.numero_serie,
                ubicacion=m.ubicacion,
                subtipo=m.subtipo,
                tipo_mantenimiento=m.tipo_mantenimiento,
                empresa_mantenedora=m.empresa_mantenedora,
                fecha_proximo_mantenimiento=m.fecha_proximo_mantenimiento,
                organismo_inspector=m.organismo_inspector,
                resultado_inspeccion=m.resultado_inspeccion,
                fecha_proxima_inspeccion=m.fecha_proxima_inspeccion,
            )
            for m in models
        ]
        return documents, total

    def get_expiring_documents(self, days_ahead: int, fecha: date) -> list[Document]:
        cutoff = fecha + timedelta(days=days_ahead)
        models = (
            self._session.query(DocumentModel)
            .filter(
                DocumentModel.deleted_at.is_(None),
                DocumentModel.fecha_caducidad.isnot(None),
                DocumentModel.fecha_caducidad <= cutoff,
            )
            .all()
        )
        return [
            Document(
                id=m.id,
                nombre_archivo=m.nombre_archivo,
                formato=m.formato,
                fecha_validez=m.fecha_validez,
                fecha_caducidad=m.fecha_caducidad,
                categoria=m.categoria,
                uploaded_by=m.uploaded_by,
            )
            for m in models
        ]
