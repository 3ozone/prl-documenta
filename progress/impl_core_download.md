# Impl — core_download (id: 2)

## Trazabilidad R → test

- **R1** → `test_download_success_returns_200_and_pdf`, `test_returns_content_and_filename_when_document_exists`
- **R2** → `test_raises_document_not_found_when_id_not_exists`, `test_download_missing_id_returns_404`
- **R3** → `test_raises_document_not_found_when_deleted_at_not_null`, `test_download_deleted_document_returns_404`
- **R4** → (placeholder — requiere auth id:9)
- **R5** → `test_download_success_returns_200_and_pdf` (verifica Content-Disposition en headers)

## Tasks completadas

| Task | Description | Estado |
|------|-------------|--------|
| T1 | Añadir `DocumentNotFound` en `domain/exceptions.py` | ✅ |
| T2 | Añadir método `read` a `AbstractFileStorage` | ✅ |
| T3 | Añadir método `get_by_id` a `AbstractDocumentRepository` | ✅ |
| T4 | Crear `DownloadDocumentUseCase` + `DownloadDocumentResult` | ✅ |
| T5 | Implementar `read` en `LocalFileStorage` | ✅ |
| T6 | Implementar `get_by_id` en `SqlDocumentRepository` | ✅ |
| T7 | Añadir `get_download_document_use_case` en `dependencies.py` | ✅ |
| T8 | Añadir endpoint `GET /documents/{document_id}/download` | ✅ |
| T9 | Tests unitarios `test_download_document_use_case.py` | ✅ |
| T10 | Tests integración `test_download_endpoint.py` | ✅ |

## Tests

- Unitarios (3): todos ✅
- Integración (4): todos ✅
- Total: 24 passed ✅
