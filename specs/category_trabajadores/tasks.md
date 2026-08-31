# Tasks — category_trabajadores

> Cada task cubre al menos un R<n>. El implementer marca `[x]` al completar.

## Backend

### T1 — Migración de base de datos
- [x] Crear migración Alembic que añada las columnas `nombre_trabajador`, `dni`, `puesto`, `tipo_documento` (todas nullable String) a la tabla `documents`.
- Cubre: R4.

### T2 — Extender `Document` entity
- [x] Añadir los 4 campos opcionales al dataclass `Document` en `domain/entities/document.py`.
- Cubre: R4.

### T3 — Crear `WorkerDocumentType` value object
- [x] Crear `domain/value_objects/worker_document_type.py` con el Enum `WorkerDocumentType` con los 4 valores: `formacion`, `reconocimiento_medico`, `entrega_epi`, `aptitud_medica`.
- Cubre: R3.

### T4 — Extender `DocumentModel`
- [x] Añadir las 4 columnas `MappedColumn` nullable en `infrastructure/db/models.py`.
- Cubre: R4.

### T5 — Extender `AbstractDocumentRepository` port
- [x] Añadir `save_worker_document(document: Document)` y `get_worker_documents(dni_trabajador: str | None, page, per_page) -> tuple[list[Document], int]` al port.
- Cubre: R4, R5, R6, R7.

### T6 — Implementar métodos en `SqlDocumentRepository`
- [x] Implementar `save_worker_document` y `get_worker_documents` en `infrastructure/db/repositories/document_repository.py`.
- Cubre: R4, R5, R6, R7.

### T7 — Crear `UploadWorkerDocumentUseCase`
- [x] Crear `application/use_cases/upload_worker_document.py` con `UploadWorkerDocumentCommand`, `UploadWorkerDocumentUseCase`.
- Validaciones: PDF, fecha_caducidad > fecha_validez, `tipo_documento` válido, campos trabajador requeridos.
- Cubre: R1, R2, R3, R4.

### T8 — Crear `ListWorkerDocumentsUseCase`
- [x] Crear `application/use_cases/list_worker_documents.py` con `ListWorkerDocumentsUseCase`, `ListWorkerDocumentsCommand`, `ListWorkerDocumentsResult`.
- Filtra por `dni_trabajador` si se proporciona, paginación siempre presente.
- Cubre: R5, R6, R7.

### T9 — Añadir schemas Pydantic
- [x] Añadir `WorkerDocumentRequest`, `WorkerDocumentResponse` y `PaginatedWorkerDocumentsResponse` en `presentation/schemas/document.py`.
- Cubre: R1, R2, R3, R4, R6.

### T10 — Crear router de trabajadores
- [x] Crear router en `presentation/api/v1/worker_categories.py` con:
  - `POST /api/v1/categories/trabajadores/documents`
  - `GET /api/v1/categories/trabajadores/documents?dni_trabajador=&page=1&per_page=20`
- Cubre: R1, R2, R3, R5, R6, R7.

### T11 — Registrar use cases en dependencies
- [x] Añadir `get_upload_worker_document_use_case` y `get_list_worker_documents_use_case` en `presentation/dependencies.py`.
- Cubre: (wiring).

## Tests

### T12 — Tests de `UploadWorkerDocumentUseCase`
- [x] `test_upload_worker_document_success` — verifica que se guarda con los 4 campos.
- [x] `test_upload_worker_document_missing_nombre_trabajador` — verifica que lanza `MissingRequiredField`.
- [x] `test_upload_worker_document_missing_dni` — verifica que lanza `MissingRequiredField`.
- [x] `test_upload_worker_document_missing_tipo_documento` — verifica que lanza `MissingRequiredField`.
- [x] `test_upload_worker_document_invalid_dates` — verifica `InvalidExpiryDate`.
- [x] `test_upload_worker_document_all_types` — verifica los 4 tipos válidos.
- Cubre: R1, R2, R3, R4.

### T13 — Tests de `ListWorkerDocumentsUseCase`
- [x] `test_list_worker_documents_pagination` — verifica paginación sin filtro.
- [x] `test_list_worker_documents_filter_by_dni` — devuelve solo documentos del DNI solicitado.
- [x] `test_list_worker_documents_all_fields` — verifica que los campos de trabajador se devuelven.
- Cubre: R5, R6, R7.
