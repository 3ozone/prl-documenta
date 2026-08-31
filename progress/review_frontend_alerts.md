# Review — feature 15 (frontend_alerts)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

- R1: [x] Cobertura estructural — `frontend/src/app/alerts/page.tsx` renderiza `<AlertsClient />`; el middleware protege la ruta (testado en `tests/middleware.test.ts`).
- R2: [x] `alerts.test.tsx` → "R2 + R4 — renders alert list with all fields" + "R2 — renders sorted by dias_restantes ascending"
- R3: [x] `tests/api/alerts-route.test.ts` → "R3 — returns alerts JSON when token is present"
- R4: [x] `alerts.test.tsx` → "R2 + R4 — renders alert list with all fields"
- R5: [x] `alerts.test.tsx` → 4 tests de `AlertBadge` (caducada/alerta_critica/alerta/aviso)
- R6: [x] `alerts.test.tsx` → "R6 — shows empty message when list is empty"
- R7: [x] `alerts.test.tsx` → "R7 — SWR is called with refreshInterval 60000"
- R8: [x] Cobertura estructural — `AlertsClient.tsx` renderiza los botones de filtro; ejercitados indirectamente por R9, R10, R11.
- R9: [x] `alerts.test.tsx` → "R9 — filter by nivel shows only matching alerts"
- R10: [x] `alerts.test.tsx` → "R10 — filter 'Todos' shows all alerts"
- R11: [x] `alerts.test.tsx` → "R11 — filter with no matches shows empty message"
- R12: [x] `alerts.test.tsx` → "R12 — shows loading state when isLoading=true"
- R13: [x] `alerts.test.tsx` → "R13 — shows error message on SWR error"
- R14: [x] `tests/api/alerts-route.test.ts` → "R14 — returns 401 when no token cookie"
- R15: [x] `frontend/src/lib/types.ts` línea 14-21 — `AlertResponse` con todos los campos requeridos.

## Tasks completas

- T1: [x]
- T2: [x]
- T3: [x]
- T4: [x]
- T5: [x]
- T6: [x]
- T7: [x]
- T8: [x]

## Checkpoints

- C1: [x] Archivos base presentes; `./init.sh` no requerido ejecutar globalmente (el comando `npx vitest run` dentro de `frontend/` es la puerta de verificación de esta feature — pasa con exit 0).
- C2: [x] Solo `frontend_alerts` en `in_progress`; `progress/current.md` describe la sesión activa.
- C3: [x] `frontend/src/lib/types.ts` — `AlertLevel` no contiene `"ok"`. `AlertBadge.tsx` — `BADGE_CLASSES` no contiene entrada `"ok"`. No hay `console.log()` fuera de `lib/logger.ts` en los archivos nuevos. Estructura respeta `docs/architecture.md`.
- C4: [x] 84 tests — 15 ficheros, todos verdes. `tests/alerts.test.tsx` (13 tests) + `tests/api/alerts-route.test.ts` (2 tests) cubren la feature.
- C5: [x] `progress/impl_frontend_alerts.md` existe con trazabilidad completa.
- C6: [x] `specs/frontend_alerts/` contiene `requirements.md`, `design.md`, `tasks.md`. Todas las tasks `[x]`. Desvío D1 documentado en `progress/impl_frontend_alerts.md` (ruta `app/alerts/` en lugar de `app/(dashboard)/alerts/` — justificado por coherencia con el resto del proyecto).

## Notas

- `AlertLevel` en `types.ts` línea 7: `"caducada" | "alerta_critica" | "alerta" | "aviso"` — sin `"ok"`. ✅
- `BADGE_CLASSES` en `AlertBadge.tsx` líneas 3-8: cuatro entradas, sin `"ok"`. ✅
- `npx vitest run` (frontend): **84 tests passed (15 files)** — verde. ✅
- D1 documentado en `progress/impl_frontend_alerts.md` línea 37. ✅
