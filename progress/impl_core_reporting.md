# Implementación — core_reporting (id: 3)

## Trazabilidad R → test

| Requirement | Test(s) |
|------------|---------|
| R1 — Clasificación en vigente / proxima_a_caducar / caducada | `test_clasifica_vigente_cuando_fecha_mas_30_dias` (`test_generate_report_use_case.py`)<br>`test_clasifica_proxima_a_caducar_cuando_fecha_entre_hoy_y_30_dias` (`test_generate_report_use_case.py`)<br>`test_clasifica_caducada_cuando_fecha_antes_hoy` (`test_generate_report_use_case.py`) |
| R2 — Excluir documentos con `deleted_at` no nulo | `test_excluye_documentos_con_deleted_at` (`test_generate_report_use_case.py`)<br>`test_report_csv_excludes_deleted_documents` (`test_report_endpoint.py`) |
| R3 — Filtrar por categoría cuando se proporciona | `test_filtra_por_categoria` (`test_generate_report_use_case.py`)<br>`test_report_csv_filters_by_category` (`test_report_endpoint.py`) |
| R4 — CSV con Content-Type y headers correctos | `test_csv_contiene_cabecera_correcta` (`test_csv_report_exporter.py`)<br>`test_csv_contiene_columnas_por_documento` (`test_csv_report_exporter.py`)<br>`test_csv_dias_hasta_caducidad_correctos` (`test_csv_report_exporter.py`)<br>`test_report_csv_returns_200_content_type_csv` (`test_report_endpoint.py`) |
| R5 — PDF con Content-Type application/pdf | `test_pdf_contiene_titulo` (`test_pdf_report_exporter.py`)<br>`test_pdf_contiene_generated_at` (`test_pdf_report_exporter.py`)<br>`test_pdf_tabla_por_estado` (`test_pdf_report_exporter.py`)<br>`test_report_pdf_returns_200_content_type_pdf` (`test_report_endpoint.py`) |
| R6 — Campo `generated_at` en la respuesta | `test_generated_at_esta_presente` (`test_generate_report_use_case.py`) |
| R7 — HTTP 400 para formato inválido | `test_report_invalid_format_returns_400` (`test_report_endpoint.py`) |

## Archivos creados / modificados

### Nuevos
- `backend/src/domain/entities/document_status.py`
- `backend/src/application/ports/report_exporter.py`
- `backend/src/application/use_cases/generate_report.py`
- `backend/src/infrastructure/export/csv_report_exporter.py`
- `backend/src/infrastructure/export/pdf_report_exporter.py`
- `backend/src/presentation/schemas/report.py`
- `backend/src/presentation/api/v1/reports.py`
- `backend/tests/unit/test_generate_report_use_case.py`
- `backend/tests/unit/test_csv_report_exporter.py`
- `backend/tests/unit/test_pdf_report_exporter.py`
- `backend/tests/integration/test_report_endpoint.py`

### Modificados
- `backend/src/domain/entities/document.py` — re-exporta `DocumentStatus`
- `backend/src/application/ports/document_repository.py` — añade `get_all_active()`
- `backend/src/infrastructure/db/repositories/document_repository.py` — implementa `get_all_active()`
- `backend/src/presentation/dependencies.py` — añade `get_generate_report_use_case` y `get_report_exporter`
- `backend/src/main.py` — registra router de reports
- `backend/src/infrastructure/export/csv_report_exporter.py` — añade stub `to_pdf`
- `backend/src/infrastructure/export/pdf_report_exporter.py` — añade stub `to_csv`
- `backend/tests/integration/conftest.py` — añade override para `get_generate_report_use_case`
- `backend/pyproject.toml` — añade `reportlab` y `pytest`, `httpx`, `anyio` en dev
