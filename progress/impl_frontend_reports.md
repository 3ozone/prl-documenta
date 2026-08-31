# Trazabilidad — frontend_reports (id: 16)

## Mapa R<n> → test

| Req | Descripción | Test |
|-----|-------------|------|
| R1  | Ruta /reports protegida por middleware | `tests/middleware.test.ts` — "R1/R2 — redirects /reports to /login when token is absent" |
| R2  | Sin sesión redirige a /login | `tests/middleware.test.ts` — mismo test |
| R3  | Selector de formato CSV/PDF, default CSV | `tests/reports.test.tsx` — "R3 — default format is CSV", "R3 — has both CSV and PDF options" |
| R4  | Selector de categoría, default todas | `tests/reports.test.tsx` — "R4 — default category is 'todas'", "R4 — has all 4 category options" |
| R5  | Botón deshabilitado durante carga | `tests/reports.test.tsx` — "R5 — button is disabled while loading" |
| R6  | Descarga automática del archivo | `tests/reports.test.tsx` — "R9/R10 — on success, createObjectURL is called" |
| R7  | Route handler requiere token | `tests/api/reports-route.test.ts` — "R7/R11 — returns 401 when no token" |
| R8  | Route handler retransmite blob con headers correctos | `tests/api/reports-route.test.ts` — "R8 — returns blob with correct headers on 200" |
| R9  | createObjectURL llamado en éxito | `tests/reports.test.tsx` — "R9/R10 — on success, createObjectURL is called" |
| R10 | URL revocada tras descarga | `tests/reports.test.tsx` — "R9/R10 — on success, createObjectURL is called and button re-enabled" |
| R11 | Error permiso en 401/403 | `tests/reports.test.tsx` — "R11 — shows permission error on 401"; `tests/api/reports-route.test.ts` — "R11 — returns 403" |
| R12 | Error genérico en 5xx | `tests/reports.test.tsx` — "R12 — shows generic error on 500"; `tests/api/reports-route.test.ts` — "R12 — returns 502" |

## Archivos creados/modificados

- `frontend/src/lib/types.ts` — añadidos `ReportFormat`, `ReportCategoria`
- `frontend/src/app/api/proxy/reports/route.ts` — Route Handler GET proxy
- `frontend/src/app/reports/ReportsForm.tsx` — Client Component
- `frontend/src/app/reports/page.tsx` — Server Component página
- `frontend/tests/api/reports-route.test.ts` — tests Route Handler (4 tests)
- `frontend/tests/reports.test.tsx` — tests ReportsForm (8 tests)
- `frontend/tests/middleware.test.ts` — añadido test ruta /reports (1 test)

## Resultado

97 tests verdes (17 test files). T1-T7 marcadas [x].
