# Implementación — category_equipos

> Feature id: 6 | Estado: done | Fecha: 2026-05-29

## Trazabilidad Requirements → Tasks → Tests

| Requirement | Descripción | Task(s) | Test(s) |
|---|---|---|---|
| R1 | `id_equipo` y `nombre_equipo` requeridos para categoría equipos | T7, T10 | `test_upload_equipment_document_missing_id_equipo`, `test_upload_equipment_document_missing_nombre_equipo` |
| R2 | Error 422 si faltan campos obligatorios | T7, T10 | `test_upload_equipment_document_missing_id_equipo`, `test_upload_equipment_document_missing_nombre_equipo` |
| R3 | Subtipo mantenimiento requiere campos específicos | T3, T7, T10 | `test_upload_equipment_document_maintenance_subtype_success`, `test_upload_equipment_document_maintenance_subtype_missing_fields` |
| R4 | Error 422 si faltan campos de mantenimiento | T7, T10 | `test_upload_equipment_document_maintenance_subtype_missing_fields` |
| R5 | Subtipo inspección requiere campos específicos | T3, T7, T10 | `test_upload_equipment_document_inspection_subtype_success`, `test_upload_equipment_document_inspection_subtype_missing_fields` |
| R6 | Error 422 si faltan campos de inspección | T7, T10 | `test_upload_equipment_document_inspection_subtype_missing_fields` |
| R7 | Persistencia de los 11 campos de equipo | T1, T2, T4, T5, T6, T7, T9 | `test_upload_equipment_document_success`, `test_upload_equipment_document_all_fields` |
| R8 | Listado filtrado por `id_equipo` | T5, T6, T8, T10 | `test_list_equipment_documents_filter_by_id_equipo` |
| R9 | Respuesta incluye todos los campos específicos | T5, T6, T8, T9, T10 | `test_list_equipment_documents_all_fields` |
| R10 | Listado sin filtro devuelve todos los documentos de equipos | T5, T6, T8, T10 | `test_list_equipment_documents_pagination` |

## Trazabilidad Tasks → Requirements

| Task | Descripción | Requirements cubiertos |
|---|---|---|
| T1 | Migración de base de datos | R7 |
| T2 | Extender `Document` entity | R7 |
| T3 | Crear value objects | R3, R5 |
| T4 | Extender `DocumentModel` | R7 |
| T5 | Extender `AbstractDocumentRepository` port | R7, R8, R9, R10 |
| T6 | Implementar métodos en `SqlDocumentRepository` | R7, R8, R9, R10 |
| T7 | Crear `UploadEquipmentDocumentUseCase` | R1, R2, R3, R4, R5, R6, R7 |
| T8 | Crear `ListEquipmentDocumentsUseCase` | R8, R9, R10 |
| T9 | Añadir schemas Pydantic | R1, R2, R3, R4, R5, R6, R7, R9 |
| T10 | Crear router de equipos | R1, R2, R3, R4, R5, R6, R8, R9, R10 |
| T11 | Registrar use cases en dependencies | (wiring) |
| T12 | Tests de `UploadEquipmentDocumentUseCase` | R1, R2, R3, R4, R5, R6, R7 |
| T13 | Tests de `ListEquipmentDocumentsUseCase` | R8, R9, R10 |

## Archivos creados/modificados

### Nuevos
- `backend/alembic/versions/4a7b9c2d8e3f_add_equipment_fields_to_documents.py` — migración Alembic
- `backend/src/domain/value_objects/equipment_subtype.py` — Enum EquipmentSubtype
- `backend/src/domain/value_objects/maintenance_type.py` — Enum MaintenanceType
- `backend/src/domain/value_objects/inspection_result.py` — Enum InspectionResult
- `backend/src/application/use_cases/upload_equipment_document.py` — UploadEquipmentDocumentUseCase
- `backend/src/application/use_cases/list_equipment_documents.py` — ListEquipmentDocumentsUseCase
- `backend/src/presentation/api/v1/equipment_categories.py` — Router para equipos
- `backend/tests/unit/test_upload_equipment_document_use_case.py` — 8 tests
- `backend/tests/unit/test_list_equipment_documents_use_case.py` — 3 tests

### Modificados
- `backend/src/domain/entities/document.py` — +11 campos al dataclass
- `backend/src/infrastructure/db/models.py` — +11 columnas MappedColumn
- `backend/src/application/ports/document_repository.py` — nuevos métodos abstractos
- `backend/src/infrastructure/db/repositories/document_repository.py` — implementación
- `backend/src/presentation/schemas/document.py` — schemas EquipmentDocument*
- `backend/src/presentation/dependencies.py` — factories para los nuevos use cases
- `backend/tests/integration/conftest.py` — columnas de equipo para tests
- `backend/tests/integration/test_download_endpoint.py` — adaptado para columnas de equipo
- `backend/tests/integration/test_report_endpoint.py` — adaptado para columnas de equipo

## Endpoints nuevos

- `POST /api/v1/categories/equipos/documents` — subida de documento de equipo
- `GET /api/v1/categories/equipos/documents?id_equipo=&page=&per_page=` — listado

## Notas

- Los tests de integración que usan SQLite en memoria requieren ALTER TABLE para las columnas de equipo ya que `Base.metadata.create_all()` no recrea columnas si la tabla ya existe
- Todos los 69 tests pasan