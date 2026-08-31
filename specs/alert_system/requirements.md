# Requirements — alert_system

> EARS notation estricta. Cada `R<n>` es verificable por un test concreto.
> Acceptance criteria de origen cubiertos: A1–A5 (todos).

---

## R1
CUANDO el sistema calcula el nivel de alerta de un documento y `dias_hasta_caducidad <= 0`,
el sistema DEBE asignar el nivel `CADUCADA`.

> Cubre A4. Verificable: `test_alert_level_expired`.

---

## R2
CUANDO el sistema calcula el nivel de alerta de un documento y `1 <= dias_hasta_caducidad <= 5`,
el sistema DEBE asignar el nivel `ALERTA_CRITICA`.

> Cubre A3. Verificable: `test_alert_level_critica`.

---

## R3
CUANDO el sistema calcula el nivel de alerta de un documento y `6 <= dias_hasta_caducidad <= 15`,
el sistema DEBE asignar el nivel `ALERTA`.

> Cubre A2. Verificable: `test_alert_level_alerta`.

---

## R4
CUANDO el sistema calcula el nivel de alerta de un documento y `16 <= dias_hasta_caducidad <= 30`,
el sistema DEBE asignar el nivel `AVISO`.

> Cubre A1. Verificable: `test_alert_level_aviso`.

---

## R5
CUANDO el sistema calcula el nivel de alerta de un documento y `dias_hasta_caducidad > 30`,
el sistema DEBE asignar el nivel `OK`.

> Verificable: `test_alert_level_ok`.

---

## R6
CUANDO se ejecuta `GET /api/v1/alerts`, el sistema DEBE devolver la lista de
`DocumentAlert` para todos los documentos con nivel distinto de `OK`
(`AVISO`, `ALERTA`, `ALERTA_CRITICA`, `CADUCADA`), ordenada por
`dias_restantes` ascendente.

> Verificable: `test_alerts_endpoint_returns_active_alerts`.

---

## R7
CUANDO se ejecuta `GET /api/v1/alerts?nivel=<nivel>`, el sistema DEBE devolver
únicamente los `DocumentAlert` cuyo nivel coincida con el parámetro indicado.

> Verificable: `test_alerts_endpoint_filter_by_nivel`.

---

## R8
El sistema DEBE excluir de los resultados de `GET /api/v1/alerts` cualquier
documento cuyo campo `deleted_at` no sea nulo.

> Cubre R6 implícitamente. Verificable: `test_alerts_excludes_deleted_documents`.

---

## R9
DONDE la notificación `panel_interno` esté habilitada, el sistema DEBE incluir
las alertas activas en la respuesta de `GET /api/v1/alerts` como lista
estructurada.

> Cubre A5 (configurabilidad panel). Verificable: `test_panel_notifier_stores_alerts`.

---

## R10
DONDE la notificación `email` esté habilitada, el sistema DEBE registrar un
mensaje de nivel `INFO` con el destinatario y el identificador del documento
por cada alerta activa (stub para MVP).

> Cubre A5 (configurabilidad email). Verificable: `test_email_notifier_logs_info`.

---

## R11
SI la notificación `email` está deshabilitada, ENTONCES el sistema NO DEBE
emitir ningún log de email ni intentar enviar correo.

> Cubre A5. Verificable: `test_email_notifier_disabled_no_log`.

---

## R12
SI la notificación `panel_interno` está deshabilitada, ENTONCES el sistema NO DEBE
almacenar alertas en el panel ni exponerlas en `GET /api/v1/alerts` a través
del notificador de panel.

> Cubre A5. Verificable: `test_panel_notifier_disabled_no_store`.

---

## R13
El sistema DEBE calcular `dias_hasta_caducidad` como
`(document.fecha_caducidad - fecha_referencia).days`, donde `fecha_referencia`
es la fecha inyectada en el caso de uso (no `date.today()` directamente en
el dominio).

> Verificable: `test_check_expiry_uses_reference_date`.

---

## R14
El sistema DEBE responder a `GET /api/v1/alerts` con código HTTP 200 y una
lista vacía (`[]`) cuando no existen documentos con alerta activa.

> Verificable: `test_alerts_endpoint_empty_list`.
