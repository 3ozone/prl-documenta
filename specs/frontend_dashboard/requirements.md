# Requirements — frontend_dashboard

> Notación EARS estricta. Cada `R<n>` es verificable por un test concreto.

---

## R1

CUANDO el usuario autenticado navega a `/dashboard`, el sistema DEBE
renderizar la página como Server Component sin emitir ningún spinner
ni estado de carga visible en el HTML inicial.

---

## R2

CUANDO el usuario autenticado navega a `/dashboard`, el sistema DEBE
mostrar el widget **AlertSummaryWidget** con el conteo de alertas
agrupadas por nivel para los niveles `aviso`, `alerta`, `alerta_critica`
y `caducada`.

---

## R3

CUANDO el usuario autenticado navega a `/dashboard`, el sistema DEBE
mostrar el widget **CategorySummaryWidget** con el conteo de documentos
agrupados por categoría para las categorías `empresa`, `trabajadores`
y `equipos`.

---

## R4

CUANDO el usuario autenticado navega a `/dashboard`, el sistema DEBE
mostrar el widget **StatusSummaryWidget** con el conteo de documentos
agrupados por estado para los estados `vigente`, `proxima_a_caducar`
y `caducada`.

---

## R5

CUANDO el sistema construye el widget **AlertSummaryWidget** en servidor,
el sistema DEBE obtener los datos llamando a `GET /api/v1/alerts` usando
el token JWT leído de la cookie `token` vía `cookies()` de `next/headers`.

---

## R6

CUANDO el sistema construye el widget **CategorySummaryWidget** en
servidor, el sistema DEBE obtener los datos llamando a
`GET /api/v1/documents?per_page=1000` usando el token JWT leído de la
cookie `token` vía `cookies()` de `next/headers`.

---

## R7

CUANDO el sistema construye el widget **StatusSummaryWidget** en servidor,
el sistema DEBE obtener los datos llamando a
`GET /api/v1/documents?per_page=1000` usando el token JWT leído de la
cookie `token` vía `cookies()` de `next/headers`.

> Nota: no existe endpoint `/api/v1/reports/status` que devuelva conteos;
> `GET /api/v1/reports/status` devuelve un `StreamingResponse` CSV/PDF
> (requiere `?formato=`). Los conteos por estado se derivan del listado
> de documentos en cliente del servidor.

---

## R8

SI la llamada a `GET /api/v1/alerts` falla (excepción de red o
`ApiError`), ENTONCES el sistema DEBE renderizar el widget
**AlertSummaryWidget** mostrando un mensaje de fallback
`"No se pudieron cargar las alertas"` en lugar de propagar el error.

---

## R9

SI la llamada a `GET /api/v1/documents` falla (excepción de red o
`ApiError`) al construir **CategorySummaryWidget**, ENTONCES el sistema
DEBE renderizar el widget mostrando un mensaje de fallback
`"No se pudieron cargar los documentos"`.

---

## R10

SI la llamada a `GET /api/v1/documents` falla (excepción de red o
`ApiError`) al construir **StatusSummaryWidget**, ENTONCES el sistema
DEBE renderizar el widget mostrando un mensaje de fallback
`"No se pudieron cargar los documentos"`.

---

## R11

El sistema DEBE definir el tipo TypeScript `DocumentResponse` en
`frontend/src/lib/types.ts` con al menos los campos:
`id: string`, `nombre_archivo: string`, `formato: string`,
`fecha_validez: string`, `fecha_caducidad: string`,
`categoria: string | null`.

---

## R12

El sistema DEBE definir el tipo TypeScript `DocumentStatus` en
`frontend/src/lib/types.ts` como unión literal:
`"vigente" | "proxima_a_caducar" | "caducada"`.

---

## R13

El sistema DEBE añadir la función `getAlerts(token: string): Promise<AlertResponse[]>`
en `frontend/src/lib/api.ts` que llame a `GET /api/v1/alerts` via `apiFetch`.

---

## R14

El sistema DEBE añadir la función `getDocuments(token: string): Promise<DocumentResponse[]>`
en `frontend/src/lib/api.ts` que llame a `GET /api/v1/documents?per_page=1000`
via `apiFetch`.

---

## R15

El sistema DEBE definir el tipo TypeScript `AlertResponse` en
`frontend/src/lib/types.ts` con los campos:
`document_id: string`, `nombre_archivo: string`,
`fecha_caducidad: string`, `nivel: AlertLevel`, `dias_restantes: number`.

---

## R16

MIENTRAS el widget **AlertSummaryWidget** renderiza conteos,
el sistema DEBE mostrar el valor `0` para cualquier nivel que no tenga
ninguna alerta activa (en lugar de omitir el nivel).

---

## R17

MIENTRAS el widget **CategorySummaryWidget** renderiza conteos,
el sistema DEBE mostrar el valor `0` para cualquier categoría que no
tenga documentos (en lugar de omitir la categoría).

---

## R18

MIENTRAS el widget **StatusSummaryWidget** renderiza conteos,
el sistema DEBE mostrar el valor `0` para cualquier estado que no
tenga documentos (en lugar de omitir el estado).

---

## R19

El sistema NO DEBE usar `"use client"` en `DashboardPage`,
`AlertSummaryWidget`, `CategorySummaryWidget` ni `StatusSummaryWidget`.

---

## R20

CUANDO el usuario no autenticado intenta acceder a `/dashboard`,
el sistema DEBE redirigir a `/login` (comportamiento ya garantizado
por `middleware.ts`; el spec lo registra para trazabilidad de tests).
