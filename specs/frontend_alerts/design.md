# Design — frontend_alerts

> Feature id: 15 | Basado en `docs/architecture.md` y `docs/conventions.md`

---

## 1. Archivos a crear

| Archivo | Tipo | Descripción |
|---|---|---|
| `frontend/src/app/(dashboard)/alerts/page.tsx` | Server Component | Punto de entrada de la ruta `/alerts`. Renderiza `<AlertsClient />`. |
| `frontend/src/app/api/proxy/alerts/route.ts` | Route Handler (Next.js) | Proxy hacia `GET /alerts` del backend. Lee cookie `token` con `cookies()` de `next/headers`. |
| `frontend/src/components/alerts/AlertsClient.tsx` | Client Component (`"use client"`) | Lógica SWR, estado de filtro, render de la lista. |
| `frontend/src/components/alerts/AlertBadge.tsx` | Client Component | Badge de color según nivel. Puramente presentacional. |
| `frontend/src/components/alerts/AlertsTable.tsx` | Client Component | Tabla/lista de alertas filtradas. Recibe `alerts: AlertResponse[]`. |

## 2. Archivos a modificar

| Archivo | Cambio |
|---|---|
| `frontend/src/lib/types.ts` | Añadir (o confirmar) interfaz `AlertResponse`. |

> `frontend/src/lib/api.ts` ya dispone de `getAlerts(token)`. No se modifica para
> esta feature — el proxy lo llama internamente desde el Route Handler.

---

## 3. Interfaces y firmas nuevas

### 3.1 `AlertResponse` (en `lib/types.ts`)

```typescript
export interface AlertResponse {
  document_id: string;
  nombre_archivo: string;
  categoria: string | null;
  nivel: "caducada" | "alerta_critica" | "alerta" | "aviso";
  dias_restantes: number;
}
```

### 3.2 Route Handler — `app/api/proxy/alerts/route.ts`

```typescript
export async function GET(request: Request): Promise<Response>
```

- Lee `token` de las cookies del servidor (`cookies()` de `next/headers`).
- Si no hay token → `Response` con status `401`.
- Llama a `getAlerts(token)` (importado de `@/lib/api`).
- Devuelve `Response.json(data)` o error con el status correspondiente.

### 3.3 `AlertsClient` (Client Component)

```typescript
// Props: ninguna
// Estado interno: nivelFiltro: string ("todos" | nivel)
// SWR key: "/api/proxy/alerts"
// SWR options: { refreshInterval: 60000 }
```

Flujo interno:
1. SWR fetch → `AlertResponse[]`
2. Ordenar por `dias_restantes` asc.
3. Filtrar por `nivelFiltro`.
4. Renderizar `<AlertsTable>` o mensaje vacío/error/loading.

### 3.4 `AlertBadge`

```typescript
interface AlertBadgeProps {
  nivel: AlertResponse["nivel"];
}
```

Mapeo de colores Tailwind:
| nivel | clases |
|---|---|
| caducada | `bg-red-100 text-red-800` |
| alerta_critica | `bg-orange-100 text-orange-800` |
| alerta | `bg-yellow-100 text-yellow-800` |
| aviso | `bg-blue-100 text-blue-800` |

---

## 4. Flujo de datos

```
Usuario → /alerts (Server Component page.tsx)
    └── renderiza <AlertsClient />          [Client boundary]
            └── SWR GET /api/proxy/alerts   [cada 60 s]
                    └── Route Handler       [lee cookie token]
                            └── getAlerts(token) → FastAPI GET /alerts
```

El token nunca se expone al JavaScript del cliente; el Route Handler actúa de
intermediario conforme al patrón httpOnly cookie del proyecto.

---

## 5. Alternativa descartada

**Alternativa: fetch directo desde `AlertsClient` a FastAPI**

Se descartó porque la cookie `token` es httpOnly y no es accesible desde
JavaScript en el navegador. El patrón establecido en el proyecto
(`frontend_documents`, `frontend_dashboard`) es siempre usar un Route Handler
como proxy para operaciones que requieren el token. Mantener este patrón
garantiza coherencia de seguridad y evita exponer el JWT al cliente.

**Alternativa: fetch inicial en Server Component + hidratación**

Se descartó porque el refresco automático cada 60 s (R7) requiere que SWR
gestione el ciclo de vida de la petición en el cliente. Un Server Component no
puede suscribirse a un `refreshInterval`.
