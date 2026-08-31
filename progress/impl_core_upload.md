# Trazabilidad — core_upload

Feature: `core_upload` (id: 1)
Estado: implementado, pendiente de revisión

## Mapa R<n> → tests

- R1 → `test_upload_non_pdf_returns_422`, `test_rejects_non_pdf_format`, `test_upload_invalid_formato_returns_422`
- R2 → `test_upload_success_returns_201`, `test_saves_file_and_metadata`
- R3 → `test_upload_missing_field_returns_422`
- R4 → `test_generates_unique_id`
- R5 → `test_rejects_invalid_expiry`, `test_upload_invalid_expiry_returns_422`, `test_expiry_date_rejects_same_date`, `test_expiry_date_rejects_earlier_caducidad`, `test_expiry_date_accepts_valid_dates`
- R6 → `test_saves_file_and_metadata`
- R7 → `test_saves_file_and_metadata`, `test_rolls_back_storage_on_db_failure`
- R8 → `test_upload_returns_500_on_unexpected_persistence_error` (integration)
- R9 → `test_upload_invalid_formato_returns_422`, `test_rejects_non_pdf_format`
- R10 → `test_upload_with_categoria`, `test_upload_without_categoria_defaults_null`, `test_upload_invalid_categoria_returns_422`
- R11 → `test_saves_file_and_metadata` (uploaded_by=None)

## Archivos creados

- `backend/pyproject.toml`
- `backend/src/domain/exceptions.py`
- `backend/src/domain/value_objects/expiry_date.py`
- `backend/src/domain/entities/document.py`
- `backend/src/application/ports/document_repository.py`
- `backend/src/application/ports/file_storage.py`
- `backend/src/application/use_cases/upload_document.py`
- `backend/src/infrastructure/db/models.py`
- `backend/src/infrastructure/db/repositories/document_repository.py`
- `backend/src/infrastructure/storage/local_file_storage.py`
- `backend/src/presentation/schemas/document.py`
- `backend/src/presentation/api/v1/documents.py`
- `backend/src/presentation/dependencies.py`
- `backend/src/main.py`
- `backend/alembic/` (inicializado, migración inicial generada)
- `backend/tests/unit/test_expiry_date.py`
- `backend/tests/unit/test_upload_document_use_case.py`
- `backend/tests/integration/conftest.py`
- `backend/tests/integration/test_upload_endpoint.py`

## Resultado

17 tests, 17 pasados, 0 fallidos. `init.sh` verde.

## Correcciones post-review (2026-05-28)

- Corrección 1: eliminado `import logging` y `log = logging.getLogger(...)` del use case `upload_document.py` (capa application no puede usar loggers).
- Corrección 2a: añadido `request_id` al `log.error(...)` en el router de presentación.
- Corrección 2b: añadido `test_upload_returns_500_on_unexpected_persistence_error` en tests de integración.
