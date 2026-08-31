# Design — frontend_dashboard

## Contexto

La página `/dashboard` ya existe como stub en
`frontend/src/app/dashboard/page.tsx`. El layout autenticado está en
`frontend/src/app/dashboard/layout.tsx`. El middleware redirige a
`/login` si no hay cookie `token`.

---

## Archivos a crear

| Archivo | Descripción |
|---------|-------------|
| `frontend/src/components/dashboard/AlertSummaryWidget.tsx` | Server Component: conteo de alertas por nivel |
| `frontend/src/components/dashboard/CategorySummaryWidget.tsx` | Server Component: conteo de documentos por categoría |
| `frontend/src/components/dashboard/StatusSummaryWidget.tsx` | Server Component: conteo de documentos por estado |

---

## Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `frontend/src/app/dashboard/page.tsx` | Sustituir stub por composición de los tres widgets |
| `frontend/src/lib/types.ts` | Añadir `AlertResponse`, `DocumentResponse`, `DocumentStatus` |
| `frontend/src/lib/api.ts` | Añadir `getAlerts()` y `getDocuments()` |
| `frontend/tests/dashboard.test.ts` | Tests de unidad para funciones de agrupación y tipos |

---

## Firmas nuevas

### `frontend/src/lib/types.ts`

```ts
export type AlertResponse = {
  document_id: string
  nombre_archivo: string
  fecha_caducidad: string
  nivel: AlertLevel
  dias_restantes: number
}

export type DocumentResponse = {
  id: string
  nombre_archivo: string
  formato: string
  fecha_validez: string
  fecha_caducidad: string
  categoria: string | null
}

export type DocumentStatus = "vigente" | "proxima_a_caducar" | "caducada"
```

### `frontend/src/lib/api.ts`

```ts
export const getAlerts = (token: string): Promise<AlertResponse[]> =>
  apiFetch<AlertResponse[]>("/api/v1/alerts", {}, token)

export const getDocuments = (token: string): Promise<DocumentResponse[]> =>
  apiFetch<DocumentResponse[]>("/api/v1/documents?per_page=1000", {}, token)
```

### `AlertSummaryWidget.tsx`

```tsx
// Server Component — sin "use client"
const AlertSummaryWidget = async ({ token }: { token: string }) => { ... }
export { AlertSummaryWidget }
```

Internamente:
1. `try { alerts = await getAlerts(token) } catch { renderiza fallback }`
2. Agrupa por `nivel` con `Map<AlertLevel, number>` inicializado a 0 para
   los cuatro niveles relevantes: `aviso`, `alerta`, `alerta_critica`, `caducada`.
3. Renderiza tabla/grid con los conteos.

### `CategorySummaryWidget.tsx`

```tsx
const CategorySummaryWidget = async ({ token }: { token: string }) => { ... }
export { CategorySummaryWidget }
```

Internamente:
1. `try { docs = await getDocuments(token) } catch { renderiza fallback }`
2. Agrupa por `categoria` contando `empresa`, `trabajadores`, `equipos`
   (los documentos sin categoría o con categoría desconocida no se cuentan
   en ningún bucket nombrado).
3. Inicializa a 0 los tres buckets antes de contar.

### `StatusSummaryWidget.tsx`

```tsx
const StatusSummaryWidget = async ({ token }: { token: string }) => { ... }
export { StatusSummaryWidget }
```

Internamente:
1. `try { docs = await getDocuments(token) } catch { renderiza fallback }`
2. Calcula `DocumentStatus` de cada documento comparando `fecha_caducidad`
   con la fecha actual del servidor (`new Date().toISOString().split("T")[0]`):
   - `fecha_caducidad < hoy` → `caducada`
   - diferencia ≤ 30 días → `proxima_a_caducar`
   - resto → `vigente`
3. Inicializa a 0 los tres buckets.

### `DashboardPage` (actualización)

```tsx
// Server Component — sin "use client"
const DashboardPage = async () => {
  const token = (await cookies()).get("token")!.value
  return (
    <main>
      <AlertSummaryWidget token={token} />
      <CategorySummaryWidget token={token} />
      <StatusSummaryWidget token={token} />
    </main>
  )
}
export default DashboardPage
```

---

## Manejo de errores

Cada widget envuelve su `await` en `try/catch`. Si `ApiError` o cualquier
excepción es capturada, el widget devuelve JSX de fallback con el mensaje
de error acordado en R8, R9 y R10. El error se registra en consola del
servidor usando `log.error(...)` de `lib/logger.ts`.

No se usan `error.tsx` de Next.js ni `<Suspense>` — la carga es síncrona
en servidor y el fallback es inline.

---

## Umbral para `proxima_a_caducar`

El frontend calcula `DocumentStatus` de forma independiente al backend.
Se usa el mismo umbral que `CheckExpiryUseCase`: 30 días
(`THRESHOLD_AVISO = 30`). Este valor se define como constante
`EXPIRY_WARNING_DAYS = 30` en el widget o en un módulo `lib/constants.ts`.

---

## Alternativa descartada — endpoint `/api/v1/reports/status`

**Propuesta:** usar `GET /api/v1/reports/status` para obtener los conteos
de estado y categoría.

**Descartada porque:** el endpoint existente devuelve un `StreamingResponse`
(CSV o PDF) que requiere el parámetro obligatorio `?formato=`. No existe
ningún endpoint JSON que devuelva conteos precalculados. Crear un nuevo
endpoint de backend está fuera del alcance de esta feature frontal.

La alternativa elegida —derivar los conteos del listado
`GET /api/v1/documents?per_page=1000`— es suficiente para el volumen
de datos esperado en esta versión y no requiere cambios en el backend.

---

## Alternativa descartada — Client Components con SWR

**Propuesta:** implementar los widgets como Client Components con
`useSWR` para obtener los datos en el cliente.

**Descartada porque:** la tabla de estrategias de `docs/conventions.md`
reserva SWR para "datos con refresco frecuente (alertas)". El dashboard
es una vista de resumen sin refresco automático requerido. Server
Components permiten carga de datos sin estado de carga inicial (R1),
que es un criterio de aceptación explícito.

---

## Restricciones de convención

- Arrow functions nombradas para todos los componentes (conventions.md).
- Imports con alias `@/` (conventions.md).
- Sin `"use client"` en ninguno de los cuatro componentes (R19).
- Logging centralizado en `lib/logger.ts` (conventions.md).
