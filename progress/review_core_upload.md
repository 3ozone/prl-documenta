# Review — feature core_upload (id: 1)

**Veredicto:** APPROVED

---

## Trazabilidad requirements ↔ tests

- R1: [x] cubierto por `test_upload_non_pdf_returns_422` (integration), `test_rejects_non_pdf_format` (unit), `test_upload_invalid_formato_returns_422` (integration)
- R2: [x] cubierto por `test_upload_success_returns_201` (integration), `test_saves_file_and_metadata` (unit)
- R3: [x] cubierto por `test_upload_missing_field_returns_422` (integration)
- R4: [x] cubierto por `test_generates_unique_id` (unit)
- R5: [x] cubierto por `test_rejects_invalid_expiry` (unit), `test_upload_invalid_expiry_returns_422` (integration), `test_expiry_date_rejects_same_date`, `test_expiry_date_rejects_earlier_caducidad`, `test_expiry_date_accepts_valid_dates`
- R6: [x] cubierto por `test_saves_file_and_metadata` (unit — verifica que `storage.save` se llama)
- R7: [x] cubierto por `test_saves_file_and_metadata` (unit), `test_rolls_back_storage_on_db_failure` (unit)
- R8: [x] cubierto por `test_upload_returns_500_on_unexpected_persistence_error` (integration, línea 70). El router (`documents.py` líneas 58–63) registra `request_id` en el `extra={}` del `log.error`.
- R9: [x] cubierto por `test_upload_invalid_formato_returns_422` (integration), `test_rejects_non_pdf_format` (unit)
- R10: [x] cubierto por `test_upload_with_categoria`, `test_upload_without_categoria_defaults_null`, `test_upload_invalid_categoria_returns_422` (unit)
- R11: [x] cubierto por `test_saves_file_and_metadata` (unit, verifica `uploaded_by=None`)

---

## Tasks completas

- T1: [x]
- T2: [x]
- T3: [x]
- T4: [x]
- T5: [x]
- T6: [x]
- T7: [x]
- T8: [x]
- T9: [x]
- T10: [x]
- T11: [x]
- T12: [x]
- T13: [x]
- T14: [x]
- T15: [x]
- T16: [x]
- T17: [x]

Todas las tasks están marcadas `[x]` en `specs/core_upload/tasks.md`.

---

## Checkpoints

- C1: [x] Archivos base presentes (`AGENTS.md`, `init.sh`, `feature_list.json`, `progress/current.md`, docs). `./init.sh` termina con exit code 0.
- C2: [x] Solo una feature `in_progress`. `progress/current.md` coherente.
- C3: [x] `backend/src/application/use_cases/upload_document.py` no contiene `import logging` ni `logging.getLogger`. Logger instanciado solo en `presentation/api/v1/documents.py` (capa presentación). Sin `print()` de debug.
- C4: [x] 17 tests, 17 verdes (`uv run pytest tests/ -v`). R8 cubierto por `test_upload_returns_500_on_unexpected_persistence_error`.
- C5: [ ] No evaluable hasta que la feature se cierre como `done` (estado actual: `in_progress`).
- C6: [x] Specs presentes con los 3 archivos. Tasks todas `[x]`. Todos los `R<n>` cubiertos por tests.

---

## Cambios requeridos

Ninguno. Los dos bloqueantes de la revisión anterior han sido resueltos:

1. ✅ `import logging` y `log = logging.getLogger(...)` eliminados de `upload_document.py` (capa application). El use case no instancia ningún logger.
2. ✅ `request_id` incluido en el `log.error(...)` del router (`documents.py` línea 61: `extra={"request_id": request_id}`). Test `test_upload_returns_500_on_unexpected_persistence_error` verifica HTTP 500 y ausencia de stack trace en el body.
