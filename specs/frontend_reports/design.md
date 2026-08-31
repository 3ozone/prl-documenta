# Design — frontend_reports

> Feature id: 16 | Decisiones técnicas previas a la implementación.

---

## 1. Archivos a crear / modificar

| Archivo | Acción | Motivo |
|---------|--------|--------|
| `frontend/src/app/(dashboard)/reports/page.tsx` | Crear | Página `/reports`. Server Component ligero que renderiza `ReportsForm`. |
| `frontend/src/app/(dashboard)/reports/ReportsForm.tsx` | Crear | Client Component con estado de carga y lógica de descarga. |
| `frontend/src/app/api/proxy/reports/route.ts` | Crear | Route Handler proxy: lee cookie, reenvía al backend, retransmite blob. |
| `frontend/src/lib/types.ts` | Modificar | Añadir tipos `ReportFormat` y `ReportCategoria`. |

No se modifica `lib/api.ts` porque la descarga de binarios requiere acceso
directo al blob y no encaja con el wrapper `apiFetch<T>` que deserializa JSON.
El componente usa `fetch("/api/proxy/reports?…")` directamente (este es el
único caso permitido de `fetch` en un Client Component, dado que la ruta de
proxy es interna al propio Next.js, no una llamada directa a FastAPI).

---

## 2. Tipos nuevos en `lib/types.ts`

```typescript
export type ReportFormat = "csv" | "pdf"
export type ReportCategoria = "todas" | "empresa" | "trabajadores" | "equipos"
```

---

## 3. Firmas nuevas

### `ReportsForm` (Client Component)

```typescript
// frontend/src/app/(dashboard)/reports/ReportsForm.tsx
"use client"

interface ReportsFormProps {}   // sin props — estado interno

const ReportsForm = (): JSX.Element => { … }
export { ReportsForm }
```

Estado interno:

| Variable | Tipo | Valor inicial |
|----------|------|---------------|
| `formato` | `ReportFormat` | `"csv"` |
| `categoria` | `ReportCategoria` | `"todas"` |
| `loading` | `boolean` | `false` |
| `error` | `string \| null` | `null` |

### Route Handler proxy

```typescript
// frontend/src/app/api/proxy/reports/route.ts
import { NextRequest, NextResponse } from "next/server"

export const GET = async (req: NextRequest): Promise<NextResponse> => { … }
```

Flujo interno del Route Handler:

1. Lee `formato` y `categoria` de `req.nextUrl.searchParams`.
2. Lee cookie `token` con `req.cookies.get("token")?.value`.
3. Si no hay token → devuelve `NextResponse` con status `401`.
4. Llama a `fetch(`${BACKEND_URL}/reports?formato=…&categoria=…`, { headers: { Authorization: "Bearer …" } })`.
5. Si `!backendRes.ok` → retransmite el status original (mapeando 5xx a 502).
6. Retransmite el blob con `Content-Type` y `Content-Disposition` del backend.

### `page.tsx` (Server Component)

```typescript
// frontend/src/app/(dashboard)/reports/page.tsx
import { ReportsForm } from "./ReportsForm"

const ReportsPage = (): JSX.Element => <ReportsForm />
export default ReportsPage
```

No necesita `cookies()` porque el Route Handler se encarga del token.

---

## 4. Flujo de datos completo

```
Usuario (browser)
  │  Selecciona formato + categoría → clic "Generar informe"
  ▼
ReportsForm (Client Component)
  │  fetch GET /api/proxy/reports?formato=csv&categoria=todas
  ▼
Route Handler /api/proxy/reports/route.ts  (Next.js server)
  │  Lee cookie token (httpOnly) → llama a FastAPI
  ▼
FastAPI GET /reports?formato=csv&categoria=todas
  │  Devuelve blob binario (CSV / PDF)
  ▼
Route Handler → retransmite blob + Content-Type + Content-Disposition
  ▼
ReportsForm
  │  Crea object URL → <a download> → click programático → descarga
  │  Revoca object URL con URL.revokeObjectURL()
  ▼
Usuario recibe el archivo
```

---

## 5. Manejo de errores (frontend)

| Código recibido | Mensaje al usuario |
|-----------------|--------------------|
| `401` / `403` | "No tienes permiso para generar informes." |
| Cualquier otro no-2xx | "Error al generar el informe. Inténtalo de nuevo." |

El error se muestra en un `<p role="alert">` bajo el botón. No se usa toast
ni modal (MVP — sin librería de notificaciones).

---

## 6. Alternativa descartada: `<a href>` directo al backend

**Opción:** Construir `<a href="http://backend:8000/reports?…&token=…" download>`
pasando el JWT como query param.

**Por qué se descarta:**

1. Expone el token JWT en la URL (logs del navegador, historial, Referer header).
2. Viola la convención del proyecto: "El token JWT se guarda en cookie httpOnly.
   Los Client Components con SWR usan `/api/` route handlers como proxy".
3. No permite mostrar un estado de carga controlado desde React.

---

## 7. Alternativa descartada: Server Action para la descarga

**Opción:** Usar un Server Action que llame al backend y devuelva el blob.

**Por qué se descarta:**

Los Server Actions están diseñados para mutaciones que devuelven JSON o
redirigen. Devolver un blob binario de gran tamaño a través del canal de
Server Actions no es el patrón recomendado por Next.js y puede suponer
problemas de serialización. El Route Handler proxy es la alternativa canónica
para este caso.

---

## 8. Logging

- El Route Handler registra errores del backend via `console.error` (se
  centraliza en `lib/logger.ts` si se importa en el contexto del servidor).
- El Client Component usa `log.error` de `lib/logger.ts` antes de mostrar el
  mensaje de error al usuario.
