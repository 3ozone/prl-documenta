# Review — feature category_empresa (id: 4)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| R1 — razon_social y cif requeridos para empresa | `test_upload_company_document_missing_razon_social`, `test_upload_company_document_missing_cif` | [x] |
| R2 — HTTP 422 si campos ausentes | `test_upload_company_document_missing_razon_social`, `test_upload_company_document_missing_cif` | [x] |
| R3 — 4 campos específicos persistidos | `test_upload_company_document_success`, `test_list_company_documents_all_fields` | [x] |
| R4 — Listado paginado de documentos empresa | `test_list_company_documents_pagination` | [x] |
| R5 — Campos específicos en respuesta | `test_list_company_documents_all_fields` | [x] |
| R6 — Filtrado por estado (vigente/caducada) | `test_list_company_documents_filter_vigente`, `test_list_company_documents_filter_caducada` | [x] |
| R7 — Cálculo de estado vigente/caducada | `test_list_company_documents_filter_vigente`, `test_list_company_documents_filter_caducada` | [x] |

## Tasks completas

- T1: [x] — Migración Alembic creada (`2e3a1b8c4d7f_add_company_fields_to_documents.py`)
- T2: [x] — Document entity con 4 campos opcionales
- T3: [x] — DocumentModel con 4 columnas MappedColumn nullable
- T4: [x] — AbstractDocumentRepository con save_company_document y get_company_documents
- T5: [x] — SqlDocumentRepository implementa los nuevos métodos
- T6: [x] — UploadCompanyDocumentUseCase creado
- T7: [x] — ListCompanyDocumentsUseCase creado
- T8: [x] — Schemas CompanyDocumentRequest/CompanyDocumentResponse
- T9: [x] — Router en presentation/api/v1/categories.py
- T10: [x] — Dependencies registradas
- T11: [x] — 4 tests unitarios para UploadCompanyDocumentUseCase
- T12: [x] — 4 tests unitarios para ListCompanyDocumentsUseCase

## Arquitectura

- domain/ y application/: [x] Sin logger (sin `structlog`, sin `logging.getLogger`)
- Capas respetadas según `docs/architecture.md`: [x]

## Checkpoints

- C1: [x] Archivos base y docs existen
- C2: [x] Una feature en `in_progress` (category_empresa), feature_list.json coherente
- C3: [x] backend/src/ con capas correctas, sin print() ni console.log()
- C4: [x] Todos los tests verdes — 49 passed (34 unit + 15 integration)
- C5: [x] Sin archivos temporales sospechosos (solo `.opencode/` modificado por agentes, sin relación con la feature)
- C6: [x] Todas las tasks marcadas `[x]` en specs/category_empresa/tasks.md; cada R<n> cubierto por al menos un test

## Fix verificado — conftest.py

El problema del primer review está resuelto. `tests/integration/conftest.py` aplica ahora
`ALTER TABLE` para añadir las 4 columnas (`razon_social`, `cif`, `actividad_economica`,
`centro_trabajo`) **después** de `Base.metadata.create_all()` y **antes** de que cualquier
test use el engine:

```python
Base.metadata.create_all(bind=engine)
with engine.connect() as conn:
    for col in ("razon_social", "cif", "actividad_economica", "centro_trabajo"):
        try:
            conn.execute(text(f"ALTER TABLE documents ADD COLUMN {col} TEXT"))
        except OperationalError:
            pass  # column already exists (e.g., from a previous test run)
    conn.commit()
```

Esto tolerancia re-ejecuciones en el mismo proceso y corrige los 8 tests de integración
heredados que antes fallaban con `table documents has no column named razon_social`.

## Resultado de tests

```
backend/: 49 passed ✓
init.sh:  OK — todos los checks verdes
```
