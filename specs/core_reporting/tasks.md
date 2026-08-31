# Tasks — core_reporting (Generación de informes de estado documental)

Cada tarea DEBE completarse en orden. El implementer marca `[x]` al terminarla.

---

## Dominio

- [x] T1 — Crear `backend/src/domain/entities/document_status.py` con `DocumentStatus(str, Enum)` con valores `VIGENTE`, `PROXIMA_A_CADUCAR`, `CADUCADA`. Cubre: R1.
- [x] T2 — Importar y re-exportar `DocumentStatus` desde `backend/src/domain/entities/document.py` para mantener la API existente. Cubre: R1.

## Application — Ports

- [x] T3 — Añadir método `get_all_active() -> list[Document]` a `backend/src/application/ports/document_repository.py` en `AbstractDocumentRepository`. Cubre: R2, R3.
- [x] T4 — Crear `backend/src/application/ports/report_exporter.py` con `AbstractReportExporter` abstracto y métodos `to_csv(result: ReportResult) -> bytes` y `to_pdf(result: ReportResult) -> bytes`. Cubre: R4, R5.

## Application — Use Case

- [x] T5 — Crear `backend/src/application/use_cases/generate_report.py` con:
  - `ReportSection(estado: DocumentStatus, documentos: list[Document], dias_hasta_caducidad: dict[str, int])`
  - `ReportResult(generated_at: datetime, sections: list[ReportSection])`
  - `GenerateReportUseCase.execute(categoria: str | None, fecha_referencia: date) -> ReportResult`
  - El método DEBE invocar `repository.get_all_active()`, filtrar por `categoria` si se proporciona, y clasificar cada documento según la lógica de R1.
  Cubre: R1, R2, R3, R6.

## Infrastructure — Base de datos

- [x] T6 — Implementar `get_all_active() -> list[Document]` en `backend/src/infrastructure/db/repositories/document_repository.py`. El método DEBE devolver todos los `DocumentModel` con `deleted_at` nulo, mapeados a entidades `Document`. Cubre: R2, R3.

## Infrastructure — Exportación

- [x] T7 — Crear `backend/src/infrastructure/export/csv_report_exporter.py` con `CsvReportExporter` que implemente `to_csv(result: ReportResult) -> bytes`. El CSV DEBE incluir la cabecera y filas especificadas en requirements.md. Cubre: R4.
- [x] T8 — Crear `backend/src/infrastructure/export/pdf_report_exporter.py` con `PdfReportExporter` que implemente `to_pdf(result: ReportResult) -> bytes` usando `reportlab`. El PDF DEBE contener título, `generated_at`, y una tabla por cada estado. Cubre: R5.
- [x] T9 — Añadir `uv add reportlab` en `backend/` para instalar la librería PDF. Cubre: R5.

## Presentation

- [x] T10 — Crear `backend/src/presentation/schemas/report.py` con `ReportStatusQuery(formato: str, categoria: str | None)` y `ReportStatusResponse(generated_at: datetime)`. Cubre: R6, R7.
- [x] T11 — Añadir `get_generate_report_use_case(db: Session) -> GenerateReportUseCase` y `get_report_exporter(formato: str) -> AbstractReportExporter` en `backend/src/presentation/dependencies.py`. Cubre: R4, R5, R7.
- [x] T12 — Crear `backend/src/presentation/api/v1/reports.py` con router y endpoint `GET /reports/status?formato=csv|pdf&categoria=...`. El endpoint DEBE:
  - Validar que `formato` sea `csv` o `pdf`; devolver HTTP 400 si no (R7)
  - Invocar `use_case.execute(categoria, date.today())` (R1, R2, R3)
  - Devolver `StreamingResponse` con el content type y headers apropiados (R4, R5)
  - Añadir comentario `# TODO: cuando auth (id:9) esté, añadir Depends(get_current_session)` Cubre: R4, R5, R6, R7.
- [x] T13 — Registrar el router `reports` en `backend/src/presentation/api/v1/__init__.py` o en el router principal de la aplicación. Cubre: R4, R5, R6, R7.

## Tests unitarios

- [x] T14 — Crear `backend/tests/unit/test_generate_report_use_case.py` con:
  - `test_clasifica_vigente_cuando_fecha_mas_30_dias` (R1)
  - `test_clasifica_proxima_a_caducar_cuando_fecha_entre_hoy_y_30_dias` (R1)
  - `test_clasifica_caducada_cuando_fecha_antes_hoy` (R1)
  - `test_excluye_documentos_con_deleted_at` (R2)
  - `test_filtra_por_categoria` (R3)
  - `test_generated_at_esta_presente` (R6)
  Cubre: R1, R2, R3, R6.

- [x] T15 — Crear `backend/tests/unit/test_csv_report_exporter.py` con:
  - `test_csv_contiene_cabecera_correcta`
  - `test_csv_contiene_columnas_por_documento`
  - `test_csv_dias_hasta_caducidad_correctos`
  Cubre: R4.

- [x] T16 — Crear `backend/tests/unit/test_pdf_report_exporter.py` con:
  - `test_pdf_contiene_titulo`
  - `test_pdf_contiene_generated_at`
  - `test_pdf_tabla_por_estado`
  Cubre: R5.

## Tests de integración

- [x] T17 — Crear `backend/tests/integration/test_report_endpoint.py` con:
  - `test_report_csv_returns_200_content_type_csv` (R4)
  - `test_report_pdf_returns_200_content_type_pdf` (R5)
  - `test_report_invalid_format_returns_400` (R7)
  - `test_report_csv_excludes_deleted_documents` (R2)
  - `test_report_csv_filters_by_category` (R3)
  Cubre: R2, R3, R4, R5, R7.

---

## Dependencias externas

| Paquete | Versión | Justificación |
|---------|---------|---------------|
| `reportlab` | 4.x | Generación de PDF ligero, sin dependencias externas adicionales |
