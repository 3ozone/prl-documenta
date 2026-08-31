# Trazabilidad — frontend_dashboard

Feature: 12 — frontend_dashboard  
Fecha: 2026-05-29  
Tests ejecutados: `npx vitest run` → 23 tests, 6 suites, todo verde.

## Mapa R<n> → test

| Requirement | Test |
|-------------|------|
| R1 — DashboardPage async con widgets | T6 (código) — `dashboard/page.tsx` compone los 3 widgets |
| R2 — Alertas agrupadas por nivel | `dashboard.test.ts` → "groups alerts by level and initialises missing levels to 0" |
| R3 — Documentos por categoría | `dashboard.test.ts` → "groups documents by category and initialises missing categories to 0" |
| R4 — Documentos por estado (vigente/proxima/caducada) | `dashboard.test.ts` → classifyStatus × 3 tests |
| R5 — Widget alertas muestra niveles aviso/alerta/alerta_critica/caducada | T3 (código) — `AlertSummaryWidget.tsx` |
| R6 — Widget categorías muestra empresa/trabajadores/equipos | T4 (código) — `CategorySummaryWidget.tsx` |
| R7 — Widget estado muestra vigente/proxima_a_caducar/caducada | T5 (código) — `StatusSummaryWidget.tsx` |
| R8 — AlertSummaryWidget sin "use client" | T3 (código) — Server Component |
| R9 — CategorySummaryWidget sin "use client" | T4 (código) — Server Component |
| R10 — StatusSummaryWidget sin "use client" | T5 (código) — Server Component |
| R11 — Tipo AlertResponse definido | T1 (código) — `types.ts` |
| R12 — Tipo DocumentResponse definido | T1 (código) — `types.ts` |
| R13 — getAlerts(token) en api.ts | T2 (código) — `api.ts` |
| R14 — getDocuments(token) en api.ts | T2 (código) — `api.ts` |
| R15 — Tipo DocumentStatus definido | T1 (código) — `types.ts` |
| R16 — Inicialización a 0 niveles faltantes | `dashboard.test.ts` → "groups alerts by level and initialises missing levels to 0" |
| R17 — Inicialización a 0 categorías faltantes | `dashboard.test.ts` → "groups documents by category and initialises missing categories to 0" |
| R18 — classifyStatus con EXPIRY_WARNING_DAYS=30 | `dashboard.test.ts` → classifyStatus × 3 tests |
| R19 — Fallback en catch en todos los widgets | T3/T4/T5 (código) — bloque try/catch con mensaje de error |
| R20 — Token leído de cookie httpOnly en DashboardPage | T6 (código) — `cookies().get("token")` |

## Resultado final

- 6 test suites, 23 tests — ✅ todo verde
- Sin `"use client"` en ningún widget
- Sin `any` en código de producción
- Arrow functions en todos los componentes
