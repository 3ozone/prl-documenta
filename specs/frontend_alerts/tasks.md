# Tasks — frontend_alerts

> Feature id: 15 | Ejecutar en orden. Marcar `[x]` al completar cada tarea.

---

- [x] T1 — Añadir / confirmar interfaz `AlertResponse` en
  `frontend/src/lib/types.ts`.
  Cubre: **R15**.

- [x] T2 — Crear Route Handler `frontend/src/app/api/proxy/alerts/route.ts`:
  lee cookie `token`, llama a `getAlerts(token)`, devuelve JSON o 401/5xx.
  Cubre: **R3**, **R14**.

- [x] T3 — Crear componente `frontend/src/components/alerts/AlertBadge.tsx`
  con mapeo de colores Tailwind por nivel.
  Cubre: **R5**.

- [x] T4 — Crear componente `frontend/src/components/alerts/AlertsTable.tsx`
  que recibe `alerts: AlertResponse[]` y renderiza la tabla con
  `nombre_archivo`, `categoria`, `dias_restantes` y `<AlertBadge>`.
  Cubre: **R4**.

- [x] T5 — Crear `frontend/src/components/alerts/AlertsClient.tsx`
  (`"use client"`): SWR con `refreshInterval: 60000`, ordenación por
  `dias_restantes` asc, estado `nivelFiltro`, controles de filtro, manejo de
  loading / error / lista vacía.
  Cubre: **R2**, **R6**, **R7**, **R8**, **R9**, **R10**, **R11**, **R12**, **R13**.

- [x] T6 — Crear Server Component `frontend/src/app/alerts/page.tsx`
  que renderiza `<AlertsClient />`.
  Cubre: **R1**.

- [x] T7 — Escribir tests en
  `frontend/tests/alerts.test.tsx`:
  - `test_renders_alert_list` — lista con datos → tabla visible. Cubre: **R2**, **R4**.
  - `test_empty_list_message` — lista vacía → "No hay alertas activas". Cubre: **R6**.
  - `test_loading_state` — SWR pendiente → indicador de carga. Cubre: **R12**.
  - `test_error_state` — SWR error → mensaje de error. Cubre: **R13**.
  - `test_filter_by_nivel` — seleccionar nivel → solo alertas de ese nivel. Cubre: **R9**.
  - `test_filter_all` — seleccionar "Todos" → todas las alertas. Cubre: **R10**.
  - `test_filter_no_match` — filtro sin coincidencias → "No hay alertas activas". Cubre: **R11**.
  - `test_sorted_by_dias_restantes` — lista desordenada → renderizada en orden asc. Cubre: **R2**.

- [x] T8 — Tests de AlertBadge en `frontend/tests/alerts.test.tsx`:
  - `test_badge_color_caducada` → clase `bg-red-*`. Cubre: **R5**.
  - `test_badge_color_alerta_critica` → clase `bg-orange-*`. Cubre: **R5**.
  - `test_badge_color_alerta` → clase `bg-yellow-*`. Cubre: **R5**.
  - `test_badge_color_aviso` → clase `bg-blue-*`. Cubre: **R5**.

---

## Trazabilidad rápida

| Requirement | Task(s) |
|---|---|
| R1 | T6 |
| R2 | T5, T7 |
| R3 | T2 |
| R4 | T4, T7 |
| R5 | T3, T8 |
| R6 | T5, T7 |
| R7 | T5 |
| R8 | T5 |
| R9 | T5, T7 |
| R10 | T5, T7 |
| R11 | T5, T7 |
| R12 | T5, T7 |
| R13 | T5, T7 |
| R14 | T2 |
| R15 | T1 |
