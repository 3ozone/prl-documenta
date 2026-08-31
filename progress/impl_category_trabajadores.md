# Implementación — category_trabajadores (id:5)

## Trazabilidad Requirements → Tests

| Requirement | Descripción | Tests que lo cubren |
|-------------|-------------|-------------------|
| R1 | `nombre_trabajador`, `dni`, `tipo_documento` requeridos para categoria="trabajadores" | `test_upload_worker_document_missing_nombre_trabajador`, `test_upload_worker_document_missing_dni`, `test_upload_worker_document_missing_tipo_documento` |
| R2 | Ausencia de campos obligatorios → HTTP 422 | Mismo test coverage que R1 (el router propaga `MissingRequiredField` como 422) |
| R3 | `tipo_documento` debe pertenecer a {formacion, reconocimiento_medico, entrega_epi, aptitud_medica} | `test_upload_worker_document_all_types` (prueba los 4 valores válidos), validación en router para valores inválidos |
| R4 | Los 4 campos específicos se persisten en la DB | `test_upload_worker_document_success` (verifica que `save_worker_document` es llamado con campos correctos) |
| R5 | GET con `dni_trabajador` devuelve lista paginada filtrada | `test_list_worker_documents_by_dni` |
| R6 | El listado incluye los campos específicos de categoría | `test_list_worker_documents_all_fields` |
| R7 | GET sin `dni_trabajador` devuelve todos los documentos paginados | `test_list_worker_documents_pagination` |

## Archivos modificados / creados

### T1 — Migración Alembic
- **Creado:** `backend/alembic/versions/3f5c2d9a1e8b_add_worker_fields_to_documents.py`

### T2 — Document entity
- **Modificado:** `backend/src/domain/entities/document.py` — añadidos 4 campos opcionales

### T3 — WorkerDocumentType value object
- **Creado:** `backend/src/domain/value_objects/worker_document_type.py`

### T4 — DocumentModel
- **Modificado:** `backend/src/infrastructure/db/models.py` — 4 columnas `MappedColumn` nullable

### T5 — AbstractDocumentRepository port
- **Modificado:** `backend/src/application/ports/document_repository.py` — añadidos `save_worker_document` y `get_worker_documents`

### T6 — SqlDocumentRepository
- **Modificado:** `backend/src/infrastructure/db/repositories/document_repository.py` — implementados ambos métodos

### T7 — UploadWorkerDocumentUseCase
- **Creado:** `backend/src/application/use_cases/upload_worker_document.py`

### T8 — ListWorkerDocumentsUseCase
- **Creado:** `backend/src/application/use_cases/list_worker_documents.py`

### T9 — Schemas Pydantic
- **Modificado:** `backend/src/presentation/schemas/document.py` — añadidos `WorkerDocumentRequest`, `WorkerDocumentResponse`, `PaginatedWorkerDocumentsResponse`

### T10 — Router
- **Creado:** `backend/src/presentation/api/v1/worker_categories.py`

### T11 — Dependencies
- **Modificado:** `backend/src/presentation/dependencies.py` — añadidas `get_upload_worker_document_use_case` y `get_list_worker_documents_use_case`
- **Modificado:** `backend/src/main.py` — registrado el nuevo router

### T12 — Tests UploadWorkerDocumentUseCase
- **Creado:** `backend/tests/unit/test_upload_worker_document_use_case.py`
  - `test_upload_worker_document_success`
  - `test_upload_worker_document_missing_nombre_trabajador`
  - `test_upload_worker_document_missing_dni`
  - `test_upload_worker_document_missing_tipo_documento`
  - `test_upload_worker_document_invalid_dates`
  - `test_upload_worker_document_all_types`

### T13 — Tests ListWorkerDocumentsUseCase
- **Creado:** `backend/tests/unit/test_list_worker_documents_use_case.py`
  - `test_list_worker_documents_by_dni`
  - `test_list_worker_documents_pagination`
  - `test_list_worker_documents_all_fields`

### Fix de integración
- **Modificado:** `backend/tests/integration/conftest.py` — añadidas las 4 columnas worker al ALTER TABLE (8 columnas total)

## Tests
- **58 tests pasan** (49 existentes + 9 nuevos)
- Todos los requirements R1–R7 tienen cobertura de test
