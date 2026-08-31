# Trazabilidad — frontend_alerts (id: 15)

| Requirement | Test |
|---|---|
| R1 | `frontend/src/app/alerts/page.tsx` renderiza `AlertsClient` (cobertura estructural) |
| R2 | `alerts.test.tsx` → "R2 + R4 — renders alert list" + "R2 — renders sorted by dias_restantes" |
| R3 | `frontend/tests/api/alerts-route.test.ts` → "R3 — returns alerts JSON when token is present" |
| R4 | `alerts.test.tsx` → "R2 + R4 — renders alert list with all fields" |
| R5 | `alerts.test.tsx` → "R5 — caducada/alerta_critica/alerta/aviso" (4 tests) |
| R6 | `alerts.test.tsx` → "R6 — shows empty message when list is empty" |
| R7 | `alerts.test.tsx` → "R7 — SWR is called with refreshInterval 60000" |
| R8 | `AlertsClient.tsx` NIVELES filtros (cobertura estructural) |
| R9 | `alerts.test.tsx` → "R9 — filter by nivel shows only matching alerts" |
| R10 | `alerts.test.tsx` → "R10 — filter 'Todos' shows all alerts" |
| R11 | `alerts.test.tsx` → "R11 — filter with no matches shows empty message" |
| R12 | `alerts.test.tsx` → "R12 — shows loading state when isLoading=true" |
| R13 | `alerts.test.tsx` → "R13 — shows error message on SWR error" |
| R14 | `frontend/tests/api/alerts-route.test.ts` → "R14 — returns 401 when no token cookie" |
| R15 | `frontend/src/lib/types.ts` → `AlertResponse` interface |

## Archivos creados/modificados

- `frontend/src/lib/types.ts` — añadido campo `categoria: string | null` a `AlertResponse`
- `frontend/src/app/api/proxy/alerts/route.ts` — Route Handler proxy
- `frontend/src/components/alerts/AlertBadge.tsx`
- `frontend/src/components/alerts/AlertsTable.tsx`
- `frontend/src/components/alerts/AlertsClient.tsx`
- `frontend/src/app/alerts/page.tsx`
- `frontend/tests/alerts.test.tsx` — 12 tests nuevos (T7+T8)

## Resultado verificación

81 tests pasados (14 test files). `npx vitest run` verde.

## Desvíos del design

D1: La página se creó en `app/alerts/page.tsx` (no en `app/(dashboard)/alerts/page.tsx`) por coherencia con el resto del proyecto. Ninguna otra ruta del proyecto usa el grupo `(dashboard)`. Mover la página a un route group cuando las demás rutas no lo usen crearía una inconsistencia de navegación.
