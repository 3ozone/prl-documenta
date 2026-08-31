# Tasks — alert_system

Orden de ejecución estricto. El implementer marca `[x]` al completar cada tarea.

---

- [x] T1 — Crear `backend/src/domain/value_objects/alert_level.py` con el enum
  `AlertLevel` (OK, AVISO, ALERTA, ALERTA_CRITICA, CADUCADA).
  Cubre: R1, R2, R3, R4, R5.

- [x] T2 — Crear `backend/src/domain/value_objects/document_alert.py` con el
  dataclass `DocumentAlert(document, level, dias_restantes)`.
  Cubre: R1, R2, R3, R4, R5.

- [x] T3 — Añadir método abstracto `get_expiring_documents(days_ahead, fecha)`
  en `backend/src/application/ports/document_repository.py`.
  Cubre: R6, R8.

- [x] T4 — Implementar `get_expiring_documents` en
  `backend/src/infrastructure/db/repositories/document_repository.py`
  (filtra `fecha_caducidad <= fecha + timedelta(days_ahead)` y `deleted_at IS NULL`).
  Cubre: R6, R8.

- [x] T5 — Crear `backend/src/application/ports/notification_service.py` con
  `AbstractNotificationService.notify(alerts)`.
  Cubre: R9, R10.

- [x] T6 — Crear `backend/src/application/use_cases/check_expiry.py` con
  `CheckExpiryUseCase` y función pura `_compute_level(dias)`.
  Cubre: R1, R2, R3, R4, R5, R13.

- [x] T7 — Crear `backend/src/infrastructure/notifications/email_notifier.py`
  con `EmailNotifier` (stub: log INFO por alerta, sin envío real).
  Cubre: R10, R11.

- [x] T8 — Crear `backend/src/infrastructure/notifications/panel_notifier.py`
  con `InternalPanelNotifier` (almacenamiento en memoria, `get_alerts()`).
  Cubre: R9, R12.

- [x] T9 — Crear `backend/src/presentation/schemas/alert_schemas.py` con
  `AlertResponse` (Pydantic: document_id, nombre_archivo, fecha_caducidad,
  nivel, dias_restantes).
  Cubre: R6, R7.

- [x] T10 — Crear `backend/src/presentation/api/v1/alerts.py` con
  `GET /api/v1/alerts?nivel=` que invoca `CheckExpiryUseCase` y filtra por
  nivel opcional. Devuelve `list[AlertResponse]` (HTTP 200).
  Cubre: R6, R7, R14.

- [x] T11 — Registrar el router de alertas en el router principal de la API
  (`backend/src/presentation/api/v1/` o `app.py`).
  Cubre: R6.

- [x] T12 — Escribir tests unitarios `backend/tests/unit/test_alert_level.py`:
  `test_alert_level_expired`, `test_alert_level_critica`, `test_alert_level_alerta`,
  `test_alert_level_aviso`, `test_alert_level_ok`, `test_check_expiry_uses_reference_date`.
  Cubre: R1, R2, R3, R4, R5, R13.

- [x] T13 — Escribir tests unitarios `backend/tests/unit/test_email_notifier.py`:
  `test_email_notifier_logs_info`, `test_email_notifier_disabled_no_log`.
  Cubre: R10, R11.

- [x] T14 — Escribir tests unitarios `backend/tests/unit/test_panel_notifier.py`:
  `test_panel_notifier_stores_alerts`, `test_panel_notifier_disabled_no_store`.
  Cubre: R9, R12.

- [x] T15 — Escribir tests de integración `backend/tests/integration/test_alerts_endpoint.py`:
  `test_alerts_endpoint_returns_active_alerts`, `test_alerts_endpoint_filter_by_nivel`,
  `test_alerts_excludes_deleted_documents`, `test_alerts_endpoint_empty_list`.
  Cubre: R6, R7, R8, R14.
