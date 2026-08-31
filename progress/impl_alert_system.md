# Implementación: alert_system

**Feature:** 7 — alert_system  
**Fecha:** 2026-05-29  
**Estado:** implementado, pendiente de revisión

## Mapa R → Test

| Req | Descripción | Test |
|-----|-------------|------|
| R1  | Nivel AVISO a ≤30 días | `test_alert_level_aviso` |
| R2  | Nivel ALERTA a ≤15 días | `test_alert_level_alerta` |
| R3  | Nivel ALERTA_CRITICA a ≤5 días | `test_alert_level_critica` |
| R4  | Nivel CADUCADA cuando dias≤0 | `test_alert_level_expired` |
| R5  | Nivel OK cuando dias>30 | `test_alert_level_ok` |
| R6  | Endpoint GET /api/v1/alerts devuelve alertas activas | `test_alerts_endpoint_returns_active_alerts` |
| R7  | Respuesta incluye document_id, nombre_archivo, fecha_caducidad, nivel, dias_restantes | `test_alerts_endpoint_returns_active_alerts` |
| R8  | Solo documentos no borrados con fecha_caducidad no nula | `test_alerts_excludes_deleted_documents` |
| R9  | InternalPanelNotifier almacena alertas en memoria | `test_panel_notifier_stores_alerts` |
| R10 | AbstractNotificationService.notify es invocable | `test_email_notifier_logs_info`, `test_panel_notifier_stores_alerts` |
| R11 | EmailNotifier deshabilitado no emite logs | `test_email_notifier_disabled_no_log` |
| R12 | PanelNotifier deshabilitado no almacena | `test_panel_notifier_disabled_no_store` |
| R13 | CheckExpiryUseCase usa fecha_referencia inyectada | `test_check_expiry_uses_reference_date` |
| R14 | Filtro opcional por nivel via query param | `test_alerts_endpoint_filter_by_nivel` |

## Archivos creados

- `backend/src/domain/value_objects/alert_level.py`
- `backend/src/domain/value_objects/document_alert.py`
- `backend/src/application/ports/notification_service.py`
- `backend/src/application/use_cases/check_expiry.py`
- `backend/src/infrastructure/notifications/email_notifier.py`
- `backend/src/infrastructure/notifications/panel_notifier.py`
- `backend/src/presentation/schemas/alert_schemas.py`
- `backend/src/presentation/api/v1/alerts.py`

## Archivos modificados

- `backend/src/application/ports/document_repository.py` — añadido `get_expiring_documents`
- `backend/src/infrastructure/db/repositories/document_repository.py` — implementado `get_expiring_documents`
- `backend/src/presentation/dependencies.py` — añadido `get_check_expiry_use_case`
- `backend/src/main.py` — registrado `alerts_router`

## Tests: 83 passed, 0 failed
