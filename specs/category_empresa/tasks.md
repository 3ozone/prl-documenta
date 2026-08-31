# Tasks — category_empresa

> Cada task cubre al menos un R<n>. El implementer marca `[x]` al completar.

## Backend

### T1 — Migración de base de datos
- [x] Crear migración Alembic que añada las columnas `razon_social`, `cif`, `actividad_economica`, `centro_trabajo` (todas nullable String) a la tabla `documents`.
- Cubre: R3.

### T2 — Extender `Document` entity
- [x] Añadir los 4 campos opcionales al dataclass `Document` en `domain/entities/document.py`.
- Cubre: R3.

### T3 — Extender `DocumentModel`
- [x] Añadir las 4 columnas `MappedColumn` nullable en `infrastructure/db/models.py`.
- Cubre: R3.

### T4 — Extender `AbstractDocumentRepository` port
- [x] Añadir `save_company_document(document: Document)` y `get_company_documents(page, per_page, estado) -> tuple[list[Document], int]` al port.
- Cubre: R3, R4, R6, R7.

### T5 — Implementar métodos en `SqlDocumentRepository`
- [x] Implementar `save_company_document` y `get_company_documents` en `infrastructure/db/repositories/document_repository.py`.
- Cubre: R3, R4, R6, R7.

### T6 — Crear `UploadCompanyDocumentUseCase`
- [x] Crear `application/use_cases/upload_company_document.py` con `UploadCompanyDocumentCommand`, `UploadCompanyDocumentUseCase`.
- Validaciones: PDF, fecha_caducidad > fecha_validez, campos empresa requeridos.
- Cubre: R1, R2, R3, R5.

### T7 — Crear `ListCompanyDocumentsUseCase`
- [x] Crear `application/use_cases/list_company_documents.py` con `ListCompanyDocumentsUseCase`.
- Lógica de cálculo de estado (vigente/caducada) según `fecha_caducidad` vs `date.today()`.
- Cubre: R4, R5, R6, R7.

### T8 — Añadir schemas Pydantic
- [x] Añadir `CompanyDocumentRequest` y `CompanyDocumentResponse` en `presentation/schemas/document.py`.
- Cubre: R1, R2, R3, R5.

### T9 — Crear router de empresa
- [x] Crear router en `presentation/api/v1/categories.py` (o añadir a `documents.py`) con:
  - `POST /api/v1/categories/empresa/documents`
  - `GET /api/v1/categories/empresa/documents?page=1&per_page=20&estado=vigente`
- Cubre: R1, R2, R4, R5, R6.

### T10 — Registrar use cases en dependencies
- [x] Añadir `get_upload_company_document_use_case` y `get_list_company_documents_use_case` en `presentation/dependencies.py`.
- Cubre: ( wiring ).

## Tests

### T11 — Tests de `UploadCompanyDocumentUseCase`
- [x] `test_upload_company_document_success` — verifica que se guarda con los 4 campos.
- [x] `test_upload_company_document_missing_razon_social` — verifica que lanza `ValidationError`.
- [x] `test_upload_company_document_missing_cif` — verifica que lanza `ValidationError`.
- [x] `test_upload_company_document_invalid_dates` — verifica `InvalidExpiryDate`.
- Cubre: R1, R2, R3.

### T12 — Tests de `ListCompanyDocumentsUseCase`
- [x] `test_list_company_documents_pagination` — verifica paginación.
- [x] `test_list_company_documents_filter_vigente` — devuelve solo vigentes.
- [x] `test_list_company_documents_filter_caducada` — devuelve solo caducadas.
- [x] `test_list_company_documents_all_fields` — verifica que los campos de empresa se devuelven.
- Cubre: R4, R5, R6, R7.