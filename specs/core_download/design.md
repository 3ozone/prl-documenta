# Design — core_download (Descarga de documentos)

---

## Archivos a crear

| Archivo | Capa | Acción |
|---------|------|--------|
| `backend/src/domain/exceptions.py` | Domain | Añadir `DocumentNotFound` |
| `backend/src/application/ports/file_storage.py` | Application | Añadir método `read(document_id) -> bytes` a `AbstractFileStorage` |
| `backend/src/application/ports/document_repository.py` | Application | Añadir método `get_by_id(document_id) -> Document \| None` a `AbstractDocumentRepository` |
| `backend/src/application/use_cases/download_document.py` | Application | Crear — caso de uso `DownloadDocumentUseCase` |
| `backend/src/infrastructure/storage/local_file_storage.py` | Infrastructure | Implementar `read(document_id) -> bytes` |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Infrastructure | Implementar `get_by_id(document_id) -> Document \| None` |
| `backend/src/presentation/api/v1/documents.py` | Presentation | Añadir router `GET /documents/{document_id}/download` |
| `backend/src/presentation/dependencies.py` | Presentation | Añadir `get_download_document_use_case` |

---

## Firmas principales

### `domain/exceptions.py` — adición

```python
class DocumentNotFound(PrlError):
    """Se lanza cuando se busca un documento que no existe o está borrado."""
```

### `application/ports/file_storage.py` — método añadido

```python
class AbstractFileStorage(ABC):
    # ... existente ...
    @abstractmethod
    def read(self, document_id: UUID) -> bytes:
        """Devuelve el contenido del fichero PDF."""
        ...
```

### `application/ports/document_repository.py` — método añadido

```python
class AbstractDocumentRepository(ABC):
    # ... existente ...
    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document | None:
        """Devuelve el documento si existe y no está borrado lógicamente, None si no existe o deleted_at no es nulo."""
        ...
```

### `application/use_cases/download_document.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID

from application.ports.document_repository import AbstractDocumentRepository
from application.ports.file_storage import AbstractFileStorage
from domain.exceptions import DocumentNotFound


@dataclass
class DownloadDocumentResult:
    content: bytes
    nombre_archivo: str


class DownloadDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, document_id: UUID) -> DownloadDocumentResult:
        document = self._repository.get_by_id(document_id)
        if document is None:
            raise DocumentNotFound(f"Documento con id '{document_id}' no encontrado.")

        content = self._storage.read(document_id)
        return DownloadDocumentResult(
            content=content,
            nombre_archivo=document.nombre_archivo,
        )
```

### `infrastructure/storage/local_file_storage.py` — método añadido

```python
def read(self, document_id: UUID) -> bytes:
    path = self._root / f"{document_id}.pdf"
    if not path.exists():
        raise FileNotFoundError(f"Fichero no encontrado: {path}")
    return path.read_bytes()
```

### `infrastructure/db/repositories/document_repository.py` — método añadido

```python
def get_by_id(self, document_id: UUID) -> Document | None:
    model = self._session.get(DocumentModel, document_id)
    if model is None or model.deleted_at is not None:
        return None
    return Document(
        id=model.id,
        nombre_archivo=model.nombre_archivo,
        formato=model.formato,
        fecha_validez=model.fecha_validez,
        fecha_caducidad=model.fecha_caducidad,
        categoria=model.categoria,
        uploaded_by=model.uploaded_by,
    )
```

### `presentation/api/v1/documents.py` — endpoint añadido

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from application.use_cases.download_document import DownloadDocumentUseCase
from domain.exceptions import DocumentNotFound
from presentation.dependencies import get_download_document_use_case

@router.get("/{document_id}/download")
async def download_document(
    request: Request,
    document_id: UUID,
    use_case: DownloadDocumentUseCase = Depends(get_download_document_use_case),
    # TODO: cuando auth (id:9) esté implementado, añadir:
    # session: Session = Depends(get_current_session),
) -> StreamingResponse:
    # PLACEHOLDER: cuando auth esté, verificar session y devolver 401 si es None
    try:
        result = use_case.execute(document_id)
    except DocumentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return StreamingResponse(
        iter([result.content]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{result.nombre_archivo}"',
        },
    )
```

---

## Decisiones de diseño

### StreamingResponse vs. FileResponse

Se usa `StreamingResponse` con `iter([result.content])` en lugar de `FileResponse` directa por dos razones:

1. `FileResponse` requiere una ruta del sistema de ficheros accesible al proceso. Si en el futuro se cambia `LocalFileStorage` por `MinIOFileStorage`, `FileResponse` ya no serviría. `StreamingResponse` funciona con cualquier fuente de bytes.
2. La cantidad de RAM consumida es proporcional al tamaño del PDF. Para el MVP con volúmenes locales, cargar el PDF completo en memoria es aceptable; si el tamaño fuera un problema, se implementaría chunking dentro del `iter()`.

### Alternativa descartada: URL firmada

**Alternativa:** Devolver una URL prefirmada (por ejemplo, URL de MinIO con caducidad) para que el cliente descargue directamente desde el almacenamiento.

**Por qué se eligió streaming:** En el MVP con almacenamiento local, no existe un servicio de URLs prefirmadas. Además, las URLs firmadas introducen complejidad de infraestructura (tokenización, caducidad, revocación) que no aporta valor en esta fase. El streaming HTTP directo es el patrón más sencillo que satisface los requisitos.

### Excepción `DocumentNotFound` vs. `None`

La firma de `AbstractDocumentRepository.get_by_id` devuelve `Document | None`. Sin embargo, el use case lanza `DocumentNotFound` (excepción de dominio). Esto es coherente con la regla de arquitectura: *"las funciones que pueden fallar lanzan excepciones nombradas del dominio, no devuelven `None`"*. El `None` interno es un detalle de infraestructura; la excepción es la interfaz de la capa de aplicación.

---

## Logger

El logger vive en infraestructura. Los eventos de download se registrarán cuando la feature `audit_log` (id: 17) esté implementada, añadiendo el evento `document.download` con `document_id` y `user_id` al contexto de logging.
