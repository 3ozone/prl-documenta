# Design — category_trabajadores

## Archivos a tocar / crear

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `backend/src/infrastructure/db/models.py` | Modificar | Añadir 4 columnas nullable a `DocumentModel` |
| `backend/src/domain/entities/document.py` | Modificar | Extender `Document` con 4 campos opcionales |
| `backend/src/domain/value_objects/worker_document_type.py` | Crear | Enum `WorkerDocumentType` con valores permitidos |
| `backend/src/application/ports/document_repository.py` | Modificar | Añadir `save_worker_document` y `get_worker_documents` al port |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Modificar | Implementar los nuevos métodos del port |
| `backend/src/application/use_cases/upload_worker_document.py` | Crear | `UploadWorkerDocumentUseCase` |
| `backend/src/application/use_cases/list_worker_documents.py` | Crear | `ListWorkerDocumentsUseCase` |
| `backend/src/presentation/schemas/document.py` | Modificar | Añadir `WorkerDocumentRequest`, `WorkerDocumentResponse` |
| `backend/src/presentation/api/v1/worker_categories.py` | Crear | Router para `trabajadores` |
| `backend/alembic/versions/` | Crear | Migración para las 4 nuevas columnas |

## Firmas nuevas

### `WorkerDocumentType` (value object / Enum)
```python
class WorkerDocumentType(str, Enum):
    FORMACION = "formacion"
    RECONOCIMIENTO_MEDICO = "reconocimiento_medico"
    ENTREGA_EPI = "entrega_epi"
    APTITUD_MEDICA = "aptitud_medica"
```

### `WorkerDocumentRequest` (schema Pydantic)
```python
class WorkerDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    nombre_trabajador: str
    dni: str
    puesto: str | None = None
    tipo_documento: WorkerDocumentType
```

### `WorkerDocumentResponse` (schema Pydantic)
```python
class WorkerDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "trabajadores"
    nombre_trabajador: str
    dni: str
    puesto: str | None
    tipo_documento: WorkerDocumentType
    storage_path: str
    uploaded_by: UUID | None
```

### `PaginatedWorkerDocumentsResponse` (schema Pydantic)
```python
class PaginatedWorkerDocumentsResponse(BaseModel):
    items: list[WorkerDocumentResponse]
    total: int
    page: int
    per_page: int
```

### `UploadWorkerDocumentCommand`
```python
@dataclass
class UploadWorkerDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    nombre_trabajador: str
    dni: str
    puesto: str | None = None
    tipo_documento: WorkerDocumentType
    uploaded_by: UUID | None = None
```

### `UploadWorkerDocumentUseCase.execute(command: UploadWorkerDocumentCommand) -> UploadWorkerDocumentResult`
Valida formato PDF, fecha_caducidad > fecha_validez, `tipo_documento` válido, persiste el documento con categoria="trabajadores" y los 4 campos específicos.

### `ListWorkerDocumentsUseCase.execute(dni_trabajador: str | None, page: int, per_page: int) -> ListWorkerDocumentsResult`
Consulta `DocumentRepository.get_worker_documents(dni_trabajador, page, per_page)`. Si `dni_trabajador` es `None`, devuelve todos los documentos de trabajadores.

### Nuevos métodos en `AbstractDocumentRepository`
```python
def save_worker_document(self, document: Document) -> None: ...
def get_worker_documents(self, dni_trabajador: str | None, page: int, per_page: int) -> tuple[list[Document], int]: ...
```

## Excepciones reutilizadas
- `InvalidDocumentFormat` — cuando el archivo no es PDF
- `InvalidExpiryDate` — cuando fecha_caducidad <= fecha_validez
- `DocumentNotFound` — cuando se pide un documento que no existe
- `MissingRequiredField` — cuando falta un campo obligatorio

## Excepción nueva
Ninguna. Se reutilizan las existentes del dominio.

## Alternativa descartada

**Tabla separada `worker_documents` con FK a `documents`.**

Se consideró modeling los campos específicos de trabajador en una tabla normalizada relacionada por `document_id`. Esto cumple las reglas de forma normal (1NF, 2NF), pero añade complejidadprematura en fase MVP:

- Requiere dos transacciones para crear un documento de trabajador (insert en `documents` y en `worker_documents`)
- Exige JOIN en todas las consultas de listado
- La feature es simple: 4 columnas nullable sobre un documento existente, análogo al patrón ya aprobado en `category_empresa`

**Decisión:** añadir las 4 columnas directamente en `DocumentModel`. Si en el futuro los campos específicos de categoría crecen o se multiplican, se evaluará extraer una tabla `category_metadata` con un discriminador de tipo.
