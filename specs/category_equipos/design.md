# Design — category_equipos

## Archivos a tocar / crear

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `backend/src/infrastructure/db/models.py` | Modificar | Añadir 10 columnas nullable a `DocumentModel` |
| `backend/src/domain/entities/document.py` | Modificar | Extender `Document` con 10 campos opcionales |
| `backend/src/domain/value_objects/equipment_subtype.py` | Crear | Enum `EquipmentSubtype` con valores `mantenimiento`, `inspeccion` |
| `backend/src/domain/value_objects/maintenance_type.py` | Crear | Enum `MaintenanceType` con valores `preventivo`, `correctivo` |
| `backend/src/domain/value_objects/inspection_result.py` | Crear | Enum `InspectionResult` con valores `favorable`, `condicionado`, `desfavorable` |
| `backend/src/application/ports/document_repository.py` | Modificar | Añadir `save_equipment_document` y `get_equipment_documents` al port |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Modificar | Implementar los nuevos métodos del port |
| `backend/src/application/use_cases/upload_equipment_document.py` | Crear | `UploadEquipmentDocumentUseCase` |
| `backend/src/application/use_cases/list_equipment_documents.py` | Crear | `ListEquipmentDocumentsUseCase` |
| `backend/src/presentation/schemas/document.py` | Modificar | Añadir `EquipmentDocumentRequest`, `EquipmentDocumentResponse` |
| `backend/src/presentation/api/v1/equipment_categories.py` | Crear | Router para `equipos` |
| `backend/alembic/versions/` | Crear | Migración para las 10 nuevas columnas |

## Firmas nuevas

### `EquipmentSubtype` (value object / Enum)
```python
class EquipmentSubtype(str, Enum):
    MANTENIMIENTO = "mantenimiento"
    INSPECCION = "inspeccion"
```

### `MaintenanceType` (value object / Enum)
```python
class MaintenanceType(str, Enum):
    PREVENTIVO = "preventivo"
    CORRECTIVO = "correctivo"
```

### `InspectionResult` (value object / Enum)
```python
class InspectionResult(str, Enum):
    FAVORABLE = "favorable"
    CONDICIONADO = "condicionado"
    DESFAVORABLE = "desfavorable"
```

### `EquipmentDocumentRequest` (schema Pydantic)
```python
class EquipmentDocumentRequest(BaseModel):
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    id_equipo: str
    nombre_equipo: str
    numero_serie: str | None = None
    ubicacion: str | None = None
    subtipo: EquipmentSubtype | None = None
    # Campos mantenimiento (requeridos si subtipo = mantenimiento)
    tipo_mantenimiento: MaintenanceType | None = None
    empresa_mantenedora: str | None = None
    fecha_proximo_mantenimiento: date | None = None
    # Campos inspección (requeridos si subtipo = inspeccion)
    organismo_inspector: str | None = None
    resultado_inspeccion: InspectionResult | None = None
    fecha_proxima_inspeccion: date | None = None
```

### `EquipmentDocumentResponse` (schema Pydantic)
```python
class EquipmentDocumentResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    categoria: str = "equipos"
    id_equipo: str
    nombre_equipo: str
    numero_serie: str | None
    ubicacion: str | None
    subtipo: EquipmentSubtype | None
    tipo_mantenimiento: MaintenanceType | None
    empresa_mantenedora: str | None
    fecha_proximo_mantenimiento: date | None
    organismo_inspector: str | None
    resultado_inspeccion: InspectionResult | None
    fecha_proxima_inspeccion: date | None
    storage_path: str
    uploaded_by: UUID | None
```

### `PaginatedEquipmentDocumentsResponse` (schema Pydantic)
```python
class PaginatedEquipmentDocumentsResponse(BaseModel):
    items: list[EquipmentDocumentResponse]
    total: int
    page: int
    per_page: int
```

### `UploadEquipmentDocumentCommand`
```python
@dataclass
class UploadEquipmentDocumentCommand:
    nombre_archivo: str
    formato: str
    fecha_validez: date
    fecha_caducidad: date
    content: bytes
    id_equipo: str
    nombre_equipo: str
    numero_serie: str | None = None
    ubicacion: str | None = None
    subtipo: EquipmentSubtype | None = None
    tipo_mantenimiento: MaintenanceType | None = None
    empresa_mantenedora: str | None = None
    fecha_proximo_mantenimiento: date | None = None
    organismo_inspector: str | None = None
    resultado_inspeccion: InspectionResult | None = None
    fecha_proxima_inspeccion: date | None = None
    uploaded_by: UUID | None = None
```

### `UploadEquipmentDocumentUseCase.execute(command: UploadEquipmentDocumentCommand) -> UploadEquipmentDocumentResult`
Valida formato PDF, fecha_caducidad > fecha_validez, campos equipo requeridos, yvalida campos condicionales según subtipo:
- Si `subtipo = mantenimiento`: requiere `tipo_mantenimiento`, `empresa_mantenedora`, `fecha_proximo_mantenimiento`
- Si `subtipo = inspeccion`: requiere `organismo_inspector`, `resultado_inspeccion`, `fecha_proxima_inspeccion`

### `ListEquipmentDocumentsUseCase.execute(id_equipo: str | None, page: int, per_page: int) -> ListEquipmentDocumentsResult`
Consulta `DocumentRepository.get_equipment_documents(id_equipo, page, per_page)`. Si `id_equipo` es `None`, devuelve todos los documentos de equipos.

### Nuevos métodos en `AbstractDocumentRepository`
```python
def save_equipment_document(self, document: Document) -> None: ...
def get_equipment_documents(self, id_equipo: str | None, page: int, per_page: int) -> tuple[list[Document], int]: ...
```

## Excepciones reutilizadas
- `InvalidDocumentFormat` — cuando el archivo no es PDF
- `InvalidExpiryDate` — cuando fecha_caducidad <= fecha_validez
- `DocumentNotFound` — cuando se pide un documento que no existe
- `MissingRequiredField` — cuando falta un campo obligatorio

## Excepción nueva
Ninguna. Se reutilizan las existentes del dominio.

## Alternativa descartada

**Tabla separada `equipment_documents` con FK a `documents`.**

Se consideró modeling los campos específicos de equipo en una tabla normalizada relacionada por `document_id`. Esto cumple las reglas de forma normal (1NF, 2NF), pero añade complejidad prematura en fase MVP:

- Requiere dos transacciones para crear un documento de equipo (insert en `documents` y en `equipment_documents`)
- Exige JOIN en todas las consultas de listado
- La feature es simple: 10 columnas nullable sobre un documento existente, análogo al patrón ya aprobado en `category_empresa` y `category_trabajadores`

**Decisión:** añadir las 10 columnas directamente en `DocumentModel`. Si en el futuro los campos específicos de categoría crecen o se multiplican, se evaluará extraer una tabla `category_metadata` con un discriminador de tipo.