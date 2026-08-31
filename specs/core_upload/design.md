# Design — core_upload (Subida de documentos)

---

## Archivos a crear

| Archivo | Capa | Acción |
|---------|------|--------|
| `backend/src/domain/entities/document.py` | Domain | Crear — entidad `Document` (dataclass frozen) |
| `backend/src/domain/value_objects/expiry_date.py` | Domain | Crear — value object `ExpiryDate` |
| `backend/src/domain/exceptions.py` | Domain | Crear / ampliar — excepciones de dominio |
| `backend/src/application/ports/document_repository.py` | Application | Crear — interfaz abstracta `AbstractDocumentRepository` |
| `backend/src/application/ports/file_storage.py` | Application | Crear — interfaz abstracta `AbstractFileStorage` |
| `backend/src/application/use_cases/upload_document.py` | Application | Crear — caso de uso `UploadDocumentUseCase` |
| `backend/src/infrastructure/db/models.py` | Infrastructure | Crear — modelo SQLAlchemy `DocumentModel` |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Infrastructure | Crear — `SqlDocumentRepository` |
| `backend/src/infrastructure/storage/local_file_storage.py` | Infrastructure | Crear — `LocalFileStorage` |
| `backend/src/presentation/schemas/document.py` | Presentation | Crear — schemas Pydantic request/response |
| `backend/src/presentation/api/v1/documents.py` | Presentation | Crear — FastAPI router `POST /documents` |
| `backend/src/presentation/dependencies.py` | Presentation | Crear / ampliar — inyección de dependencias |

---

## Firmas principales

### `domain/entities/document.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID

@dataclass(frozen=True)
class Document:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str | None = None
    uploaded_by: UUID | None = None
```

### `domain/value_objects/expiry_date.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from src.domain.exceptions import InvalidExpiryDate

@dataclass(frozen=True)
class ExpiryDate:
    fecha_validez: date
    fecha_caducidad: date

    def __post_init__(self) -> None:
        if self.fecha_caducidad <= self.fecha_validez:
            raise InvalidExpiryDate(
                f"fecha_caducidad ({self.fecha_caducidad}) debe ser posterior "
                f"a fecha_validez ({self.fecha_validez})"
            )
```

### `domain/exceptions.py`

```python
class PrlError(Exception):
    """Base para errores del dominio PRL."""

class InvalidExpiryDate(PrlError):
    """fecha_caducidad <= fecha_validez."""

class InvalidDocumentFormat(PrlError):
    """El formato del documento no está permitido."""

class MissingRequiredField(PrlError):
    """Falta un campo obligatorio en la subida."""

class InvalidDocumentCategory(PrlError):
    """La categoría del documento no está entre los valores permitidos."""
```

### `application/ports/document_repository.py`

```python
from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.document import Document

class AbstractDocumentRepository(ABC):
    @abstractmethod
    def save(self, document: Document) -> None: ...

    @abstractmethod
    def exists(self, document_id: UUID) -> bool: ...
```

### `application/ports/file_storage.py`

```python
from abc import ABC, abstractmethod
from uuid import UUID

class AbstractFileStorage(ABC):
    @abstractmethod
    def save(self, document_id: UUID, content: bytes) -> str:
        """Persiste el contenido y devuelve la ruta almacenada."""
        ...

    @abstractmethod
    def delete(self, document_id: UUID) -> None: ...
```

### `application/use_cases/upload_document.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from src.domain.entities.document import Document
from src.domain.value_objects.expiry_date import ExpiryDate
from src.domain.exceptions import InvalidDocumentFormat, InvalidDocumentCategory
from src.application.ports.document_repository import AbstractDocumentRepository
from src.application.ports.file_storage import AbstractFileStorage

ALLOWED_FORMATS = frozenset({"pdf"})
ALLOWED_CATEGORIES = frozenset({"empresa", "trabajadores", "equipos"})

@dataclass
class UploadDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    file_content: bytes
    categoria: str | None = None
    uploaded_by: UUID | None = None

@dataclass
class UploadDocumentResult:
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    categoria: str | None = None

class UploadDocumentUseCase:
    def __init__(
        self,
        repository: AbstractDocumentRepository,
        storage: AbstractFileStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadDocumentCommand) -> UploadDocumentResult:
        if command.formato not in ALLOWED_FORMATS:
            raise InvalidDocumentFormat(command.formato)
        if command.categoria is not None and command.categoria not in ALLOWED_CATEGORIES:
            raise InvalidDocumentCategory(command.categoria)
        ExpiryDate(
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
        )
        document_id = uuid4()
        document = Document(
            id=document_id,
            nombre_archivo=command.nombre_archivo,
            formato=command.formato,
            fecha_validez=command.fecha_validez,
            fecha_caducidad=command.fecha_caducidad,
            categoria=command.categoria,
            uploaded_by=command.uploaded_by,
        )
        storage_path = self._storage.save(document_id, command.file_content)
        try:
            self._repository.save(document)
        except Exception:
            self._storage.delete(document_id)
            raise
        return UploadDocumentResult(
            id=document_id,
            nombre_archivo=document.nombre_archivo,
            formato=document.formato,
            fecha_validez=document.fecha_validez,
            fecha_caducidad=document.fecha_caducidad,
            storage_path=storage_path,
            categoria=document.categoria,
        )
```

### `presentation/schemas/document.py`

```python
from datetime import date
from uuid import UUID
from pydantic import BaseModel, field_validator

class UploadDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str | None = None

class UploadDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    storage_path: str
    categoria: str | None
```

### `presentation/api/v1/documents.py`

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from src.presentation.schemas.document import UploadDocumentRequest, UploadDocumentResponse
from src.application.use_cases.upload_document import UploadDocumentUseCase, UploadDocumentCommand
from src.domain.exceptions import InvalidDocumentFormat, InvalidDocumentCategory, InvalidExpiryDate

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=UploadDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    metadata: UploadDocumentRequest,
    file: UploadFile = File(...),
    use_case: UploadDocumentUseCase = Depends(...),
) -> UploadDocumentResponse:
    ...
```

---

## Modelo SQLAlchemy — `infrastructure/db/models.py`

```python
class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nombre_archivo = Column(String(255), nullable=False)
    formato = Column(String(10), nullable=False)
    fecha_validez = Column(Date, nullable=False)
    fecha_caducidad = Column(Date, nullable=False)
    categoria = Column(String(50), nullable=True)       # para category_* features (ids 4-6)
    uploaded_by = Column(UUID(as_uuid=True), nullable=True)  # para audit_log (id:17)
    deleted_at = Column(DateTime, nullable=True)         # soft delete para core_delete (id:14)
```

> **Nota:** `deleted_at` vive solo en el modelo de infraestructura; la entidad de dominio `Document` NO incluye este campo porque el soft delete es una decisión de infraestructura, no de dominio.

---

## Almacenamiento de PDFs

**Decisión para MVP:** Volumen Docker local (`LocalFileStorage`).

Los ficheros se guardan bajo la ruta `STORAGE_ROOT/{document_id}.pdf`, donde `STORAGE_ROOT` es una variable de entorno (por defecto `/data/documents`).

La interfaz `AbstractFileStorage` permite sustituir `LocalFileStorage` por `MinIOFileStorage` en el futuro sin modificar ninguna capa de dominio ni aplicación.

---

## Alternativas descartadas

### Alternativa: almacenar el PDF en base de datos (BLOB en MariaDB)

**Por qué se descartó:** Almacenar ficheros binarios grandes en MariaDB incrementa el tamaño de los backups, degrada el rendimiento de las consultas relacionales y complica la replicación. Un volumen de ficheros es el patrón estándar para documentos binarios y permite servir los PDFs directamente vía servidor de ficheros o CDN en el futuro.

### Alternativa: generar el `id` como autoincrement entero en la BD

**Por qué se descartó:** Un UUID v4 generado en la capa de aplicación permite construir la entidad `Document` antes de tocar la base de datos, facilita las pruebas unitarias sin BD y evita fugas de información sobre el volumen de documentos del sistema.

---

## Diagrama de flujo

```
POST /api/v1/documents (multipart/form-data)
   │
   ▼ Presentation: validar UploadDocumentRequest (Pydantic)
   │   → HTTP 422 si falta campo obligatorio o formato != "pdf" (R3, R9)
   │   → HTTP 422 si Content-Type del fichero != application/pdf (R1)
   │   → categoria opcional; None si se omite (R10)
   │
   ▼ Application: UploadDocumentUseCase.execute(command)
   │   → InvalidDocumentFormat    → HTTP 422 (R1, R9)
   │   → InvalidDocumentCategory  → HTTP 422 (R10)
   │   → InvalidExpiryDate        → HTTP 422 (R5)
   │   → uuid4()                  → id único (R4)
   │   → uploaded_by = None si sin sesión (R11)
   │
   ▼ Infrastructure: LocalFileStorage.save() → ruta (R6)
   ▼ Infrastructure: SqlDocumentRepository.save() (R7)
   │   → fallo → storage.delete() + re-raise → HTTP 500 (R7, R8)
   │
   ▼ HTTP 201 + UploadDocumentResponse (R2)
```
