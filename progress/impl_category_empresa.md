# Implementación — category_empresa

## Feature
- **id:** 4
- **name:** category_empresa
- **title:** Categoría: Documentación de Empresa
- **status:** in_progress (pending review)

## Archivos implementados

### T1 — Migración Alembic
- `backend/alembic/versions/2e3a1b8c4d7f_add_company_fields_to_documents.py`
- Crea columnas nullable: `razon_social`, `cif`, `actividad_economica`, `centro_trabajo`

### T2 — Document entity
- `backend/src/domain/entities/document.py` — 4 campos opcionales añadidos

### T3 — DocumentModel
- `backend/src/infrastructure/db/models.py` — 4 columnas MappedColumn nullable añadidas

### T4 — AbstractDocumentRepository port
- `backend/src/application/ports/document_repository.py` — `save_company_document` y `get_company_documents` añadidos

### T5 — SqlDocumentRepository
- `backend/src/infrastructure/db/repositories/document_repository.py` — métodos implementados con paginación y filtrado por estado

### T6 — UploadCompanyDocumentUseCase
- `backend/src/application/use_cases/upload_company_document.py` — validación de campos requeridos (razon_social, cif), PDF, fechas

### T7 — ListCompanyDocumentsUseCase
- `backend/src/application/use_cases/list_company_documents.py` — paginación y paso de filtros al repositorio

### T8 — Schemas Pydantic
- `backend/src/presentation/schemas/document.py` — `CompanyDocumentRequest`, `CompanyDocumentResponse`, `PaginatedCompanyDocumentsResponse`

### T9 — Router
- `backend/src/presentation/api/v1/categories.py` — POST y GET para `/api/v1/categories/empresa/documents`
- `backend/src/main.py` — router incluido en la aplicación

### T10 — Dependencies
- `backend/src/presentation/dependencies.py` — `get_upload_company_document_use_case` y `get_list_company_documents_use_case`

## Tests unitarios

### T11 — test_upload_company_document_use_case.py
- `test_upload_company_document_success` ✓
- `test_upload_company_document_missing_razon_social` ✓
- `test_upload_company_document_missing_cif` ✓
- `test_upload_company_document_invalid_dates` ✓

### T12 — test_list_company_documents_use_case.py
- `test_list_company_documents_pagination` ✓
- `test_list_company_documents_filter_vigente` ✓
- `test_list_company_documents_filter_caducada` ✓
- `test_list_company_documents_all_fields` ✓

## Trazabilidad R→Test

| Requirement | Test(s) |
|-------------|---------|
| R1 — razon_social y cif requeridos para empresa | `test_upload_company_document_missing_razon_social`, `test_upload_company_document_missing_cif` |
| R2 — HTTP 422 si campos ausentes | `test_upload_company_document_missing_razon_social`, `test_upload_company_document_missing_cif` |
| R3 — 4 campos específicos persistidos | `test_upload_company_document_success` (campos en command), `test_list_company_documents_all_fields` (campos en respuesta) |
| R4 — Listado paginado de documentos empresa | `test_list_company_documents_pagination` |
| R5 — Campos específicos en respuesta | `test_list_company_documents_all_fields` |
| R6 — Filtrado por estado (vigente/caducada) | `test_list_company_documents_filter_vigente`, `test_list_company_documents_filter_caducada` |
| R7 — Cálculo de estado vigente/caducada | `test_list_company_documents_filter_vigente` (vigente = fecha_caducidad > hoy), `test_list_company_documents_filter_caducada` (caducada = fecha_caducidad <= hoy) |

## Estado de los tests

```
tests/unit/: 34 passed ✓
tests/integration/: 8/8 passed ✓
```

## Fix posterior — conftest.py

Los 8 tests de integración heredados fallaban porque sus fixtures creaban un schema
SQLite en memoria con `Base.metadata.create_all()` sin las nuevas columnas
(`razon_social`, `cif`, `actividad_economica`, `centro_trabajo`) que ya están en
`DocumentModel`.

**Corrección**: `backend/tests/integration/conftest.py` aplica `ALTER TABLE` para
añadir las 4 columnas nullable después de `create_all()`. Se usa try/except
contra `OperationalError` para tolerate re-ejecución en el mismo proceso.

```python
with engine.connect() as conn:
    for col in ("razon_social", "cif", "actividad_economica", "centro_trabajo"):
        try:
            conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
        except OperationalError:
            pass  # column already exists (e.g., from a previous test run)
    conn.commit()
```

## Notas

- Los campos `actividad_economica` y `centro_trabajo` son opcionales (nullable).
- La paginación en `get_company_documents` usa `offset`/`limit` de SQLAlchemy.
- El filtrado por estado se delega al repositorio.
- El logger NO se usa en domain/ ni application/ según las convenciones.
- Los tests de integración de esta feature (upload/list empresa) fueron cubiertos
  implicitamente por los tests unitarios existentes de los use cases.