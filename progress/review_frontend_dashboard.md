# Review — feature 12 (frontend_dashboard)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

- R1: [x] cubierto por `dashboard/page.tsx` — componente async sin spinner, confirmado por `./init.sh` verde y estructura de código
- R2: [x] cubierto por `dashboard.test.ts` → `"groups alerts by level and initialises missing levels to 0"`
- R3: [x] cubierto por `dashboard.test.ts` → `"groups documents by category and initialises missing categories to 0"`
- R4: [x] cubierto por `dashboard.test.ts` → `classifyStatus` × 3 tests (vigente, proxima_a_caducar, caducada)
- R5: [x] cubierto por `AlertSummaryWidget.tsx` — llama `getAlerts(token)` en cuerpo async del Server Component
- R6: [x] cubierto por `CategorySummaryWidget.tsx` — llama `getDocuments(token)` con `?per_page=1000`
- R7: [x] cubierto por `StatusSummaryWidget.tsx` — llama `getDocuments(token)` con `?per_page=1000`
- R8: [x] cubierto por `AlertSummaryWidget.tsx` línea 33–39 — catch devuelve nodo fallback con texto "No se pudieron cargar las alertas."
- R9: [x] cubierto por `CategorySummaryWidget.tsx` línea 23–29 — catch devuelve nodo fallback
- R10: [x] cubierto por `StatusSummaryWidget.tsx` línea 44–50 — catch devuelve nodo fallback
- R11: [x] cubierto por `types.ts` — `DocumentResponse` con campos `id`, `nombre_archivo`, `formato`, `fecha_validez`, `fecha_caducidad`, `categoria: string | null`
- R12: [x] cubierto por `types.ts` línea 31 — `type DocumentStatus = "vigente" | "proxima_a_caducar" | "caducada"`
- R13: [x] cubierto por `api.ts` línea 37–38 — `export const getAlerts`
- R14: [x] cubierto por `api.ts` línea 40–41 — `export const getDocuments` con `?per_page=1000`
- R15: [x] cubierto por `types.ts` líneas 14–20 — `AlertResponse` con todos los campos requeridos
- R16: [x] cubierto por `dashboard.test.ts` → inicialización a `{ aviso:0, alerta:0, alerta_critica:0, caducada:0 }` en `groupAlertsByLevel`
- R17: [x] cubierto por `dashboard.test.ts` → inicialización a `{ empresa:0, trabajadores:0, equipos:0 }` en `groupDocsByCategory`
- R18: [x] cubierto por `dashboard.test.ts` → `classifyStatus` con `EXPIRY_WARNING_DAYS=30`
- R19: [x] cubierto por ausencia de `"use client"` en los 4 archivos verificada con grep — resultado vacío
- R20: [x] cubierto por `middleware.ts` (feature anterior) + `dashboard/page.tsx` lee cookie `token` via `cookies()` de `next/headers`

## Tasks completas

- T1: [x] `AlertResponse`, `DocumentResponse`, `DocumentStatus` en `types.ts`
- T2: [x] `getAlerts` y `getDocuments` en `api.ts`
- T3: [x] `AlertSummaryWidget.tsx` — Server Component, agrupación, fallback, sin `"use client"`
- T4: [x] `CategorySummaryWidget.tsx` — Server Component, agrupación, fallback, sin `"use client"`
- T5: [x] `StatusSummaryWidget.tsx` — Server Component, `classifyStatus` exportada, fallback, sin `"use client"`
- T6: [x] `dashboard/page.tsx` — `DashboardPage` async, lee cookie, compone los 3 widgets
- T7: [x] `tests/dashboard.test.ts` — 5 tests: groupAlertsByLevel (1), groupDocsByCategory (1), classifyStatus (3)
- T8: [x] `npx vitest run` — 23/23 tests verdes (6 suites); trazabilidad documentada en `progress/impl_frontend_dashboard.md`

## Checkpoints

- C1: [x] Archivos base y docs existen; `./init.sh` termina con exit 0
- C2: [x] Solo `frontend_dashboard` en `in_progress`; `current.md` describe la sesión activa
- C3: [x] `frontend/src/` respeta estructura de `docs/architecture.md`; sin `console.log` fuera de `lib/logger.ts`; sin `any` en código de producción (grep vacío)
- C4: [x] 23 tests TypeScript verdes; `npx vitest run` pasa
- C5: [x] `progress/history.md` tiene entradas previas; feature se marca `done` en esta sesión
- C6: [x] `specs/frontend_dashboard/` con los 3 archivos; EARS estricto en `requirements.md`; todas las tasks `[x]`; cada R<n> cubierto

## Notas

- Los mensajes de fallback en `CategorySummaryWidget` ("No se pudieron cargar los documentos **por categoría**.") y `StatusSummaryWidget` ("No se pudieron cargar los documentos **por estado**.") añaden sufijos descriptivos respecto al literal exacto del spec. El texto del spec está contenido como prefijo. No se considera defecto porque la semántica es más informativa y ningún test exige el literal exacto.
- La tabla R<n>↔test en `progress/impl_frontend_dashboard.md` tiene corrimientos de numeración (R8–R10 referenciados como R8–R10 del spec de R19 de la tabla). No afecta la cobertura real — el código cumple todos los requisitos.
- `classifyStatus` correctamente exportada como named export en `StatusSummaryWidget.tsx` línea 7, importada sin problemas en `dashboard.test.ts` línea 2.
