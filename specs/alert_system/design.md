# Design — alert_system

## 1. Archivos a crear

| Archivo | Descripción |
|---|---|
| `backend/src/domain/value_objects/alert_level.py` | Enum `AlertLevel` |
| `backend/src/domain/value_objects/document_alert.py` | Dataclass `DocumentAlert` |
| `backend/src/application/ports/notification_service.py` | Port `AbstractNotificationService` |
| `backend/src/application/use_cases/check_expiry.py` | Use case `CheckExpiryUseCase` |
| `backend/src/infrastructure/notifications/email_notifier.py` | `EmailNotifier` (stub) |
| `backend/src/infrastructure/notifications/panel_notifier.py` | `InternalPanelNotifier` |
| `backend/src/presentation/api/v1/alerts.py` | FastAPI router `GET /api/v1/alerts` |
| `backend/src/presentation/schemas/alert_schemas.py` | Pydantic response schemas |
| `backend/tests/unit/test_alert_level.py` | Tests unitarios de lógica de umbral |
| `backend/tests/unit/test_check_expiry.py` | Tests unitarios del use case |
| `backend/tests/unit/test_email_notifier.py` | Tests del stub de email |
| `backend/tests/unit/test_panel_notifier.py` | Tests del notificador de panel |
| `backend/tests/integration/test_alerts_endpoint.py` | Tests del endpoint REST |

## 2. Archivos a modificar

| Archivo | Cambio |
|---|---|
| `backend/src/application/ports/document_repository.py` | Añadir método abstracto `get_expiring_documents` |
| `backend/src/infrastructure/db/repositories/document_repository.py` | Implementar `get_expiring_documents` |
| `backend/src/presentation/api/v1/__init__.py` o router principal | Registrar el router de alertas |

## 3. Firmas nuevas

### `domain/value_objects/alert_level.py`

```python
from enum import Enum

class AlertLevel(str, Enum):
    OK = "ok"
    AVISO = "aviso"
    ALERTA = "alerta"
    ALERTA_CRITICA = "alerta_critica"
    CADUCADA = "caducada"
```

### `domain/value_objects/document_alert.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from domain.entities.document import Document
from domain.value_objects.alert_level import AlertLevel

@dataclass(frozen=True)
class DocumentAlert:
    document: Document
    level: AlertLevel
    dias_restantes: int  # negativo si ya caducado
```

### `application/ports/document_repository.py` (adición)

```python
@abstractmethod
def get_expiring_documents(self, days_ahead: int, fecha: date) -> list[Document]:
    """Devuelve documentos con fecha_caducidad <= fecha + days_ahead y deleted_at nulo.
    Incluye documentos ya caducados (fecha_caducidad < fecha)."""
```

### `application/ports/notification_service.py`

```python
from abc import ABC, abstractmethod
from domain.value_objects.document_alert import DocumentAlert

class AbstractNotificationService(ABC):
    @abstractmethod
    def notify(self, alerts: list[DocumentAlert]) -> None: ...
```

### `application/use_cases/check_expiry.py`

```python
from datetime import date
from application.ports.document_repository import AbstractDocumentRepository
from domain.value_objects.alert_level import AlertLevel
from domain.value_objects.document_alert import DocumentAlert

THRESHOLD_CADUCADA = 0
THRESHOLD_ALERTA_CRITICA = 5
THRESHOLD_ALERTA = 15
THRESHOLD_AVISO = 30

class CheckExpiryUseCase:
    def __init__(self, repo: AbstractDocumentRepository) -> None: ...

    def execute(self, fecha_referencia: date) -> list[DocumentAlert]:
        """Obtiene documentos con caducidad en los próximos THRESHOLD_AVISO días
        (o ya caducados) y calcula el nivel de alerta de cada uno.
        Devuelve lista ordenada por dias_restantes ascendente."""
    
    @staticmethod
    def _compute_level(dias: int) -> AlertLevel:
        """Función pura: dado dias_restantes, retorna el AlertLevel."""
```

### `infrastructure/notifications/email_notifier.py`

```python
class EmailNotifier(AbstractNotificationService):
    """MVP stub: registra un log INFO por cada alerta. No envía email real."""
    def __init__(self, enabled: bool = True) -> None: ...
    def notify(self, alerts: list[DocumentAlert]) -> None: ...
    # log.info("alert.email_stub", extra={"document_id": ..., "nivel": ..., "dias_restantes": ...})
```

### `infrastructure/notifications/panel_notifier.py`

```python
class InternalPanelNotifier(AbstractNotificationService):
    """Almacena alertas en memoria para ser expuestas por el endpoint REST."""
    def __init__(self, enabled: bool = True) -> None: ...
    def notify(self, alerts: list[DocumentAlert]) -> None: ...
    def get_alerts(self) -> list[DocumentAlert]: ...
```

### `presentation/api/v1/alerts.py`

```python
# GET /api/v1/alerts?nivel={nivel}
# Parámetro `nivel` opcional. Valores permitidos: aviso, alerta, alerta_critica, caducada.
# Response: list[AlertResponse] (HTTP 200)
```

### `presentation/schemas/alert_schemas.py`

```python
from pydantic import BaseModel
from uuid import UUID
from datetime import date

class AlertResponse(BaseModel):
    document_id: UUID
    nombre_archivo: str
    fecha_caducidad: date
    nivel: str
    dias_restantes: int
```

## 4. Excepciones

No se añaden excepciones nuevas de dominio. El endpoint devuelve `422` si el
parámetro `nivel` recibe un valor fuera de los permitidos (validación Pydantic
automática con `Literal` o `Enum`).

## 5. Constantes de umbral

Los umbrales (`THRESHOLD_AVISO = 30`, etc.) se declaran como constantes de
módulo en `application/use_cases/check_expiry.py`. No se leen de base de datos
en MVP. La configuración por cadencia definida en `expiration_rules` del
`feature_list.json` queda como trabajo futuro (fuera del alcance de esta
feature).

## 6. Alternativas descartadas

### A. Calcular nivel en la entidad `Document`

Se descartó porque haría que `Document` dependa de `date.today()` o de un
parámetro de fecha de referencia externo, rompiendo la inmutabilidad del
dominio y acoplando la entidad al tiempo de ejecución. La función pura
`_compute_level` en el use case mantiene el dominio sin efectos secundarios.

### B. Tabla de alertas en base de datos

Se descartó para MVP porque añade complejidad de migraciones y sincronización.
`InternalPanelNotifier` usa almacenamiento en memoria; la instancia se gestiona
como singleton en la inyección de dependencias de FastAPI. Para producción se
puede reemplazar con una implementación persistente sin cambiar la interfaz.

### C. Scheduler automático (cron/celery) en MVP

Se descartó para MVP. El endpoint `GET /api/v1/alerts` computa las alertas
en tiempo real en cada petición. El scheduler se contempla como mejora futura.
