# Tasks — core_upload (Subida de documentos)

Cada tarea DEBE completarse en orden. El implementer marca `[x]` al terminarla.

---

## Dominio

- [x] T1 — Crear `backend/src/domain/exceptions.py` con `PrlError`, `InvalidExpiryDate`, `InvalidDocumentFormat`, `MissingRequiredField`, `InvalidDocumentCategory`. Cubre: R3, R5, R1, R9, R10.
- [x] T2 — Crear `backend/src/domain/value_objects/expiry_date.py` con `ExpiryDate` (dataclass frozen, lanza `InvalidExpiryDate` si `fecha_caducidad <= fecha_validez`). Cubre: R5.
- [x] T3 — Crear `backend/src/domain/entities/document.py` con `Document` (dataclass frozen, incluye `categoria: str | None` y `uploaded_by: UUID | None`). Cubre: R2, R4, R10, R11.

## Application — Ports

- [x] T4 — Crear `backend/src/application/ports/document_repository.py` con `AbstractDocumentRepository` (métodos `save`, `exists`). Cubre: R7.
- [x] T5 — Crear `backend/src/application/ports/file_storage.py` con `AbstractFileStorage` (métodos `save`, `delete`). Cubre: R6, R7.

## Application — Use Case

- [x] T6 — Crear `backend/src/application/use_cases/upload_document.py` con `UploadDocumentCommand` (incluye `categoria: str | None` y `uploaded_by: UUID | None`), `UploadDocumentResult` (incluye `categoria: str | None`) y `UploadDocumentUseCase.execute()`. El caso de uso debe: validar formato (R1, R9), validar `categoria` contra valores permitidos o None (R10), almacenar `uploaded_by` tal cual (R11), construir `ExpiryDate` (R5), generar UUID v4 (R4), llamar a `storage.save()` (R6), llamar a `repository.save()` con rollback de storage ante fallo (R7). Cubre: R1, R2, R4, R5, R6, R7, R9, R10, R11.

## Infrastructure — Base de datos

- [x] T7 — Crear `backend/src/infrastructure/db/models.py` con `DocumentModel` (SQLAlchemy, tabla `documents`, columnas: `id UUID PK`, `nombre_archivo`, `formato`, `fecha_validez`, `fecha_caducidad`, `categoria VARCHAR NULL`, `uploaded_by UUID NULL`, `deleted_at DATETIME NULL`). Cubre: R7, R10, R11.
- [x] T8 — Crear `backend/src/infrastructure/db/repositories/document_repository.py` con `SqlDocumentRepository` que implementa `AbstractDocumentRepository`. Cubre: R7.
- [x] T9 — Crear migración Alembic inicial para la tabla `documents`. Cubre: R7.

## Infrastructure — Almacenamiento

- [x] T10 — Crear `backend/src/infrastructure/storage/local_file_storage.py` con `LocalFileStorage` que implementa `AbstractFileStorage`. Ruta: `{STORAGE_ROOT}/{document_id}.pdf`. Cubre: R6, R7.

## Presentation

- [x] T11 — Crear `backend/src/presentation/schemas/document.py` con `UploadDocumentRequest` (incluye `categoria: str | None = None`) y `UploadDocumentResponse` (incluye `categoria: str | None` y `uploaded_by: UUID | None`) (Pydantic). Cubre: R2, R3, R10, R11.
- [x] T12 — Crear `backend/src/presentation/api/v1/documents.py` con `POST /documents`. El router debe: validar `Content-Type` del fichero (R1), capturar `InvalidDocumentFormat` → HTTP 422 (R1, R9), capturar `InvalidExpiryDate` → HTTP 422 (R5), capturar errores inesperados → HTTP 500 con log `ERROR` (R8), devolver HTTP 201 en éxito (R2). Cubre: R1, R2, R3, R5, R8, R9.
- [x] T13 — Crear / ampliar `backend/src/presentation/dependencies.py` para inyectar `UploadDocumentUseCase` con sus dependencias concretas. Cubre: R2.

## Tests unitarios

- [x] T14 — Crear `backend/tests/unit/test_expiry_date.py`: `test_expiry_date_rejects_same_date`, `test_expiry_date_rejects_earlier_caducidad`, `test_expiry_date_accepts_valid_dates`. Cubre: R5.
- [x] T15 — Crear `backend/tests/unit/test_upload_document_use_case.py`: `test_rejects_non_pdf_format`, `test_rejects_invalid_expiry`, `test_generates_unique_id`, `test_saves_file_and_metadata`, `test_rolls_back_storage_on_db_failure`. Cubre: R1, R4, R5, R6, R7, R9.

## Tests de integración

- [x] T16 — Crear `backend/tests/integration/test_upload_endpoint.py`: `test_upload_success_returns_201`, `test_upload_missing_field_returns_422`, `test_upload_non_pdf_returns_422`, `test_upload_invalid_expiry_returns_422`, `test_upload_invalid_formato_returns_422`. Cubre: R1, R2, R3, R5, R9.

## Tests unitarios — categoría y usuario

- [x] T17 — Añadir en `backend/tests/unit/test_upload_document_use_case.py`: `test_upload_with_categoria`, `test_upload_without_categoria_defaults_null`, `test_upload_invalid_categoria_returns_422`. Cubre: R10.
