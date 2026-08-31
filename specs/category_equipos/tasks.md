# Tasks — category_equipos

> Cada task cubre al menos un R<n>. El implementer marca `[x]` al completar.

## Backend

### T1 — Migración de base de datos
- [x] Crear migración Alembic que añada las columnas `id_equipo`, `nombre_equipo`, `numero_serie`, `ubicacion`, `subtipo`, `tipo_mantenimiento`, `empresa_mantenedora`, `fecha_proximo_mantenimiento`, `organismo_inspector`, `resultado_inspeccion`, `fecha_proxima_inspeccion` (todas nullable String / Date / Enum) a la tabla `documents`.
- Cubre: R7.

### T2 — Extender `Document` entity
- [x] Añadir los 10 campos opcionales al dataclass `Document` en `domain/entities/document.py`.
- Cubre: R7.

### T3 — Crear value objects
- [x] Crear `domain/value_objects/equipment_subtype.py` con Enum `EquipmentSubtype` (`mantenimiento`, `inspeccion`).
- [x] Crear `domain/value_objects/maintenance_type.py` con Enum `MaintenanceType` (`preventivo`, `correctivo`).
- [x] Crear `domain/value_objects/inspection_result.py` con Enum `InspectionResult` (`favorable`, `condicionado`, `desfavorable`).
- Cubre: R3, R5.

### T4 — Extender `DocumentModel`
- [x] Añadir las 11 columnas `MappedColumn` nullable en `infrastructure/db/models.py`.
- Cubre: R7.

### T5 — Extender `AbstractDocumentRepository` port
- [x] Añadir `save_equipment_document(document: Document)` y `get_equipment_documents(id_equipo: str | None, page, per_page) -> tuple[list[Document], int]` al port.
- Cubre: R7, R8, R9, R10.

### T6 — Implementar métodos en `SqlDocumentRepository`
- [x] Implementar `save_equipment_document` y `get_equipment_documents` en `infrastructure/db/repositories/document_repository.py`.
- Cubre: R7, R8, R9, R10.

### T7 — Crear `UploadEquipmentDocumentUseCase`
- [x] Crear `application/use_cases/upload_equipment_document.py` con `UploadEquipmentDocumentCommand`, `UploadEquipmentDocumentUseCase`.
- Validaciones: PDF, fecha_caducidad > fecha_validez, `id_equipo` requerido, `nombre_equipo` requerido.
- Validación condicional: si `subtipo = mantenimiento`, requiere `tipo_mantenimiento`, `empresa_mantenedora`, `fecha_proximo_mantenimiento`.
- Validación condicional: si `subtipo = inspeccion`, requiere `organismo_inspector`, `resultado_inspeccion`, `fecha_proxima_inspeccion`.
- Cubre: R1, R2, R3, R4, R5, R6, R7.

### T8 — Crear `ListEquipmentDocumentsUseCase`
- [x] Crear `application/use_cases/list_equipment_documents.py` con `ListEquipmentDocumentsUseCase`, `ListEquipmentDocumentsCommand`, `ListEquipmentDocumentsResult`.
- Filtra por `id_equipo` si se proporciona, paginación siempre presente.
- Cubre: R8, R9, R10.

### T9 — Añadir schemas Pydantic
- [x] Añadir `EquipmentDocumentRequest`, `EquipmentDocumentResponse` y `PaginatedEquipmentDocumentsResponse` en `presentation/schemas/document.py`.
- Cubre: R1, R2, R3, R4, R5, R6, R7, R9.

### T10 — Crear router de equipos
- [x] Crear router en `presentation/api/v1/equipment_categories.py` con:
  - `POST /api/v1/categories/equipos/documents`
  - `GET /api/v1/categories/equipos/documents?id_equipo=&page=1&per_page=20`
- Cubre: R1, R2, R3, R4, R5, R6, R8, R9, R10.

### T11 — Registrar use cases en dependencies
- [x] Añadir `get_upload_equipment_document_use_case` y `get_list_equipment_documents_use_case` en `presentation/dependencies.py`.
- Cubre: (wiring).

## Tests

### T12 — Tests de `UploadEquipmentDocumentUseCase`
- [x] `test_upload_equipment_document_success` — verifica que se guarda con los campos base.
- [x] `test_upload_equipment_document_missing_id_equipo` — verifica que lanza `MissingRequiredField`.
- [x] `test_upload_equipment_document_missing_nombre_equipo` — verifica que lanza `MissingRequiredField`.
- [x] `test_upload_equipment_document_maintenance_subtype_success` — verifica que se guarda con campos mantenimiento cuando subtipo=mantenimiento.
- [x] `test_upload_equipment_document_maintenance_subtype_missing_fields` — verifica 422 si faltan campos mantenimiento.
- [x] `test_upload_equipment_document_inspection_subtype_success` — verifica que se guarda con campos inspección cuando subtipo=inspeccion.
- [x] `test_upload_equipment_document_inspection_subtype_missing_fields` — verifica 422 si faltan campos inspección.
- [x] `test_upload_equipment_document_invalid_dates` — verifica `InvalidExpiryDate`.
- Cubre: R1, R2, R3, R4, R5, R6, R7.

### T13 — Tests de `ListEquipmentDocumentsUseCase`
- [x] `test_list_equipment_documents_pagination` — verifica paginación sin filtro.
- [x] `test_list_equipment_documents_filter_by_id_equipo` — devuelve solo documentos del id_equipo solicitado.
- [x] `test_list_equipment_documents_all_fields` — verifica que los campos de equipo se devuelven en la respuesta.
- Cubre: R8, R9, R10.