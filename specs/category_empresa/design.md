# Design — category_empresa

## Archivos a tocar / crear

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `backend/src/infrastructure/db/models.py` | Modificar | Añadir 4 columnas nullable a `DocumentModel` |
| `backend/src/domain/entities/document.py` | Modificar | Extender `Document` con 4 campos opcionales |
| `backend/src/application/ports/document_repository.py` | Modificar | Añadir `save_company_document` y `get_company_documents` al port |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Modificar | Implementar los nuevos métodos del port |
| `backend/src/application/use_cases/upload_company_document.py` | Crear | `UploadCompanyDocumentUseCase` |
| `backend/src/application/use_cases/list_company_documents.py` | Crear | `ListCompanyDocumentsUseCase` |
| `backend/src/presentation/schemas/document.py` | Modificar | Añadir `CompanyDocumentRequest`, `CompanyDocumentResponse` |
| `backend/src/presentation/api/v1/documents.py` | Crear router adicional | `POST /api/v1/categories/empresa/documents`, `GET /api/v1/categories/empresa/documents` |
| `backend/alembic/versions/` | Crear | Migración para las 4 nuevas columnas |

## Firmas nuevas

### `CompanyDocumentRequest` (schema Pydantic)
```python
class CompanyDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    razon_social: str
    cif: str
    actividad_economica: str | None = None
    centro_trabajo: str | None = None
```

### `CompanyDocumentResponse` (schema Pydantic)
```python
class CompanyDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "empresa"
    razon_social: str
    cif: str
    actividad_economica: str | None
    centro_trabajo: str | None
    storage_path: str
    uploaded_by: UUID | None
```

### `UploadCompanyDocumentCommand`
```python
@dataclass
class UploadCompanyDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    razon_social: str
    cif: str
    actividad_economica: str | None = None
    centro_trabajo: str | None = None
```

### `UploadCompanyDocumentUseCase.execute(command: UploadCompanyDocumentCommand) -> UploadDocumentResult`
Valida formato PDF, fecha_caducidad > fecha_validez, persiste el documento con categoria="empresa" y los 4 campos específicos.

### `ListCompanyDocumentsUseCase.execute(page: int, per_page: int, estado: str | None) -> PagedResult[Document]`
Consulta `DocumentRepository.get_company_documents(page, per_page, estado)`. Calcula el estado de cada documento comparando `fecha_caducidad` con la fecha actual.

### Nuevos métodos en `AbstractDocumentRepository`
```python
def save_company_document(self, document: Document) -> None: ...
def get_company_documents(self, page: int, per_page: int, estado: str | None) -> tuple[list[Document], int]: ...
```

## Excepciones reutilizadas
- `InvalidDocumentFormat` — cuando el archivo no es PDF
- `InvalidExpiryDate` — cuando fecha_caducidad <= fecha_validez
- `DocumentNotFound` — cuando se pide un documento que no existe

## Excepción nueva
Ninguna. Se reutilizan las existentes del dominio.

## Alternativa descartada

**Tabla separada `company_documents` con FK a `documents`.**

Se consideró modeling los campos específicos de empresa en una tabla normalizada relacionada por `document_id`. Esto cumple las reglas de forma normal (1NF, 2NF), pero añade complejidadprematura en fase MVP:

- Requiere dos transacciones para crear un documento de empresa (insert en `documents` y en `company_documents`)
- Exige JOIN en todas las consultas de listado
- La feature es simple: 4 columnas nullable sobre un documento existente

**Decisión:** añadir las 4 columnas directamente en `DocumentModel`. Si en el futuro los campos específicos de categoría crecen o se multiplican, se evaluará extraer una tabla `category_metadata` con un discriminador de tipo.