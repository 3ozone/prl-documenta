# Review — feature 3 (core_reporting)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

- **R1** (clasificación en vigente/proxima_a_caducar/caducada): [x] cubierto por
  `test_clasifica_vigente_cuando_fecha_mas_30_dias`,
  `test_clasifica_proxima_a_caducar_cuando_fecha_entre_hoy_y_30_dias`,
  `test_clasifica_caducada_cuando_fecha_antes_hoy`
  (`test_generate_report_use_case.py`)

- **R2** (excluir documentos con `deleted_at` no nulo): [x] cubierto por
  `test_excluye_documentos_con_deleted_at` (`test_generate_report_use_case.py`),
  `test_report_csv_excludes_deleted_documents` (`test_report_endpoint.py`)

- **R3** (filtrar por categoría): [x] cubierto por
  `test_filtra_por_categoria` (`test_generate_report_use_case.py`),
  `test_report_csv_filters_by_category` (`test_report_endpoint.py`)

- **R4** (CSV con Content-Type y headers correctos): [x] cubierto por
  `test_csv_contiene_cabecera_correcta`, `test_csv_contiene_columnas_por_documento`,
  `test_csv_dias_hasta_caducidad_correctos` (`test_csv_report_exporter.py`),
  `test_report_csv_returns_200_content_type_csv` (`test_report_endpoint.py`)

- **R5** (PDF con Content-Type application/pdf): [x] cubierto por
  `test_pdf_contiene_titulo`, `test_pdf_contiene_generated_at`, `test_pdf_tabla_por_estado`
  (`test_pdf_report_exporter.py`),
  `test_report_pdf_returns_200_content_type_pdf` (`test_report_endpoint.py`)

- **R6** (campo `generated_at` en la respuesta): [x] cubierto por
  `test_generated_at_esta_presente` (`test_generate_report_use_case.py`)

- **R7** (HTTP 400 para formato inválido): [x] cubierto por
  `test_report_invalid_format_returns_400` (`test_report_endpoint.py`)

## Tasks completas

- T1: [x] — `DocumentStatus` creado en `document_status.py`
- T2: [x] — re-exportado desde `document.py`
- T3: [x] — `get_all_active()` en `AbstractDocumentRepository`
- T4: [x] — `AbstractReportExporter` creado
- T5: [x] — `GenerateReportUseCase` creado con toda la lógica
- T6: [x] — `get_all_active()` implementado en `SqlDocumentRepository`
- T7: [x] — `CsvReportExporter` creado
- T8: [x] — `PdfReportExporter` creado
- T9: [x] — `reportlab` añadido a `pyproject.toml`
- T10: [x] — schemas `ReportStatusQuery` y `ReportStatusResponse` creados
- T11: [x] — dependencies `get_generate_report_use_case` y `get_report_exporter` añadidas
- T12: [x] — router `GET /reports/status` creado con validación, StreamingResponse y TODO de auth
- T13: [x] — router registrado en `__init__.py` o `main.py`
- T14: [x] — tests unitarios de `GenerateReportUseCase` (6 tests)
- T15: [x] — tests de `CsvReportExporter` (3 tests)
- T16: [x] — tests de `PdfReportExporter` (3 tests)
- T17: [x] — tests de integración del endpoint (5 tests)

todas las tasks marcadas `[x]` en `specs/core_reporting/tasks.md`.

## Arquitectura

- ❌ No se encontró ningún uso de `structlog` ni `logging.getLogger` en `domain/` ni `application/`.
- La regla de dependencia se cumple: las capas internas no importan externas.
- Los value objects son `DocumentStatus(str, Enum)` según spec.

## Checkpoints

- C1: [x] — archivos base del arnés tutti quanti
- C2: [x] — una sola feature `in_progress`; `core_reporting` tiene todos los tests asociados y pasan
- C3: [x] — estructura de carpetas respeta `architecture.md`; sin `print()` sueltos
- C4: [x] — `uv run pytest tests/ -v` pasa con 41 tests verdes
- C5: [x] — `progress/impl_core_reporting.md` documenta los archivos creados/modificados
- C6: [x] — specs/core_reporting tiene los 3 archivos (requirements, design, tasks); todos los R<n> tienen cobertura

## Ejecución

- `cd backend && uv run pytest tests/ -v` → **41 passed** ✅
- `./init.sh` → **OK** (41 passed, entorno listo) ✅
    