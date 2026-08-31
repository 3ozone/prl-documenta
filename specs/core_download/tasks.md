# Tasks — core_download (Descarga de documentos)

Cada tarea DEBE completarse en orden. El implementer marca `[x]` al terminarla.

---

## Dominio

- [x] T1 — Añadir `DocumentNotFound` en `backend/src/domain/exceptions.py`. Cubre: R2, R3.

## Application — Ports

- [x] T2 — Añadir método `read(document_id: UUID) -> bytes` a `backend/src/application/ports/file_storage.py` en `AbstractFileStorage`. Cubre: R1.
- [x] T3 — Añadir método `get_by_id(document_id: UUID) -> Document | None` a `backend/src/application/ports/document_repository.py` en `AbstractDocumentRepository`. El método DEBE devolver `None` si el documento no existe o si `deleted_at` no es nulo. Cubre: R2, R3.

## Application — Use Case

- [x] T4 — Crear `backend/src/application/use_cases/download_document.py` con `DownloadDocumentResult` (campos `content: bytes`, `nombre_archivo: str`), `DownloadDocumentUseCase` con `execute(document_id: UUID) -> DownloadDocumentResult`. El use case DEBE invocar `repository.get_by_id()` y lanzar `DocumentNotFound` si devuelve `None`; luego invocar `storage.read()`. Cubre: R1, R2, R3.

## Infrastructure — Almacenamiento

- [x] T5 — Implementar `read(document_id: UUID) -> bytes` en `backend/src/infrastructure/storage/local_file_storage.py`. El método DEBE leer el fichero `{STORAGE_ROOT}/{document_id}.pdf` y devolver sus bytes; DEBE lanzar `FileNotFoundError` si el fichero no existe en disco. Cubre: R1.

## Infrastructure — Base de datos

- [x] T6 — Implementar `get_by_id(document_id: UUID) -> Document | None` en `backend/src/infrastructure/db/repositories/document_repository.py`. El método DEBE devolver `None` si `self._session.get(DocumentModel, document_id)` devuelve `None` o si `model.deleted_at` no es nulo; en caso contrario, construir y devolver la entidad `Document`. Cubre: R2, R3.

## Presentation

- [x] T7 — Añadir `get_download_document_use_case(db: Session)` en `backend/src/presentation/dependencies.py` que construya y devuelva `DownloadDocumentUseCase(repository=SqlDocumentRepository(db), storage=LocalFileStorage(...))`. Cubre: R1.
- [x] T8 — Añadir `GET /documents/{document_id}/download` en `backend/src/presentation/api/v1/documents.py`. El endpoint DEBE: depender de `DownloadDocumentUseCase` (T7); invocar `use_case.execute(document_id)`; capturar `DocumentNotFound` → HTTP 404; devolver `StreamingResponse` con `media_type="application/pdf"` y header `Content-Disposition: attachment; filename="{nombre_archivo}"`. Añadir comentario `# TODO: cuando auth (id:9) esté, añadir Depends(get_current_session) y verificar 401`. Cubre: R1, R2, R3, R4, R5.

## Tests unitarios

- [x] T9 — Crear `backend/tests/unit/test_download_document_use_case.py` con: `test_raises_document_not_found_when_id_not_exists`, `test_raises_document_not_found_when_deleted_at_not_null`, `test_returns_content_and_filename_when_document_exists`. Cubre: R2, R3, R5.

## Tests de integración

- [x] T10 — Crear `backend/tests/integration/test_download_endpoint.py` con: `test_download_success_returns_200_and_pdf`, `test_download_missing_id_returns_404`, `test_download_deleted_document_returns_404`, `test_download_non_uuid_returns_422`. Cubre: R1, R2, R3, R4, R5.
