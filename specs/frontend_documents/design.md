# Design — frontend_documents

## Contexto

Las páginas `/dashboard` y `/login` ya están implementadas. El middleware
redirige a `/login` si no hay cookie `token`. `lib/api.ts` ya expone
`getDocuments(token)`. `lib/types.ts` ya define `DocumentResponse` y
`DocumentStatus`.

---

## Archivos a crear

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `frontend/src/app/documents/page.tsx` | Server Component | Listado paginado con badge de estado y botón subida condicional |
| `frontend/src/app/documents/upload/page.tsx` | Server Component (guard) | Verifica rol admin; renderiza `UploadForm` o redirige |
| `frontend/src/components/documents/DocumentsTable.tsx` | Server Component | Tabla de documentos con paginación por `searchParams` |
| `frontend/src/components/documents/UploadForm.tsx` | Client Component (`"use client"`) | Formulario react-hook-form para subida de PDF |
| `frontend/src/app/api/proxy/documents/[id]/download/route.ts` | Route Handler | Proxy de descarga: lee cookie, llama backend, reenvía stream |
| `frontend/src/app/api/documents/upload/route.ts` | Route Handler | Proxy de subida: lee cookie, llama backend con multipart |
| `frontend/src/lib/classifyStatus.ts` | Utilidad | Función `classifyStatus(doc: DocumentResponse): DocumentStatus` |
| `frontend/tests/classifyStatus.test.ts` | Vitest | Tests unitarios de `classifyStatus` |
| `frontend/tests/documents.test.ts` | Vitest | Tests de paginación y filtrado de rol |

---

## Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `frontend/src/lib/api.ts` | Añadir `uploadDocument(formData, token)` |
| `frontend/src/lib/types.ts` | (sin cambio — tipos ya existentes son suficientes) |

---

## Firmas nuevas

### `frontend/src/lib/classifyStatus.ts`

```ts
import type { DocumentResponse, DocumentStatus } from "@/lib/types"

export const EXPIRY_WARNING_DAYS = 30

export const classifyStatus = (doc: DocumentResponse, today?: string): DocumentStatus => {
  const t = today ?? new Date().toISOString().split("T")[0]
  if (doc.fecha_caducidad < t) return "caducada"
  const diffMs = new Date(doc.fecha_caducidad).getTime() - new Date(t).getTime()
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
  return diffDays <= EXPIRY_WARNING_DAYS ? "proxima_a_caducar" : "vigente"
}
```

El parámetro `today` permite inyectar la fecha en tests sin mocks de `Date`.

### `frontend/src/lib/api.ts` (añadir)

```ts
export const uploadDocument = (formData: FormData, token: string): Promise<unknown> =>
  apiFetch<unknown>("/api/v1/documents", { method: "POST", body: formData }, token)
```

> **Nota:** para multipart, `apiFetch` NO debe inyectar `Content-Type: application/json`
> cuando `body` es `FormData`. El wrapper actual sobrescribe `Content-Type`; el Route
> Handler de subida llamará directamente a `fetch` sin pasar por `apiFetch` para evitar
> colisión de cabeceras.

### `frontend/src/app/documents/page.tsx`

```tsx
// Server Component — sin "use client"
const DocumentsPage = async ({
  searchParams,
}: {
  searchParams: { page?: string }
}) => {
  const token = (await cookies()).get("token")!.value
  const page = Number(searchParams.page ?? "1")
  const role = getRoleFromToken(token)   // decodifica sin verificar firma (servidor)
  const docs = await getDocuments(token)
  return (
    <main>
      {role === "admin" && <a href="/documents/upload">Subir documento</a>}
      <DocumentsTable docs={docs} page={page} />
    </main>
  )
}
export default DocumentsPage
```

### `getRoleFromToken` (helper servidor)

Función interna en `frontend/src/lib/auth.ts` (nuevo) que decodifica el
payload JWT en base64 (sin verificar firma — el middleware ya valida el
token):

```ts
export const getRoleFromToken = (token: string): UserRole => {
  const payload = JSON.parse(
    Buffer.from(token.split(".")[1], "base64url").toString("utf8")
  )
  return payload.role as UserRole
}
```

### `frontend/src/components/documents/DocumentsTable.tsx`

```tsx
// Server Component — sin "use client"
const DocumentsTable = ({
  docs,
  page,
}: {
  docs: DocumentResponse[]
  page: number
}) => {
  const PER_PAGE = 20
  const slice = docs.slice((page - 1) * PER_PAGE, page * PER_PAGE)
  const totalPages = Math.ceil(docs.length / PER_PAGE)
  // renderiza tabla + controles de paginación con links ?page=N
}
export { DocumentsTable }
```

### `frontend/src/components/documents/UploadForm.tsx`

```tsx
"use client"
const UploadForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<UploadFormValues>()
  const onSubmit = async (data: UploadFormValues) => { ... }
  return <form onSubmit={handleSubmit(onSubmit)}>...</form>
}
export { UploadForm }
```

Tipo local:

```ts
type UploadFormValues = {
  nombre_archivo: string
  fecha_validez: string
  fecha_caducidad: string
  file: FileList
}
```

Validaciones react-hook-form:
- `nombre_archivo`: `required`
- `fecha_validez`: `required`
- `fecha_caducidad`: `required`
- `file`: `required`, `validate: (fl) => fl[0]?.type === "application/pdf" || "Solo se permiten archivos PDF"`

### Route Handler — descarga

```ts
// frontend/src/app/api/proxy/documents/[id]/download/route.ts
export const GET = async (
  _req: Request,
  { params }: { params: { id: string } }
) => {
  const token = cookies().get("token")?.value
  if (!token) return new Response(null, { status: 401 })
  const upstream = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents/${params.id}/download`,
    { headers: { Authorization: `Bearer ${token}` } }
  )
  if (!upstream.ok) {
    if (upstream.status === 404)
      return new Response("Documento no encontrado", { status: 404 })
    return new Response(null, { status: upstream.status })
  }
  return new Response(upstream.body, {
    headers: { "Content-Type": "application/pdf" },
  })
}
```

### Route Handler — subida

```ts
// frontend/src/app/api/documents/upload/route.ts
export const POST = async (req: Request) => {
  const token = cookies().get("token")?.value
  if (!token) return Response.json({ detail: "Unauthorized" }, { status: 401 })
  const formData = await req.formData()
  const upstream = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents`,
    { method: "POST", body: formData, headers: { Authorization: `Bearer ${token}` } }
  )
  const body = await upstream.text()
  return new Response(body, { status: upstream.status })
}
```

---

## Manejo de errores

- `DocumentsPage`: si `getDocuments` lanza `ApiError`, renderiza un mensaje
  de error inline con `log.error(...)`.
- `UploadForm`: captura el error de la llamada al Route Handler y lo muestra
  bajo el botón de submit sin redirigir.
- Route Handler descarga: propaga el status del backend; 404 devuelve
  `"Documento no encontrado"`.

---

## Alternativa descartada — `<a download>` directo al backend

**Propuesta:** usar `<a href="http://backend:8000/api/v1/documents/{id}/download" download>`.

**Descartada porque:** el token JWT está en una cookie `httpOnly` — el
navegador no puede leerla desde JavaScript, y los `<a>` links no envían
cookies de otros orígenes. El backend requiere `Authorization: Bearer <token>`.
Sin el Route Handler proxy, la descarga recibiría 401.

---

## Alternativa descartada — SWR + Client Component para el listado

**Propuesta:** cargar el listado con SWR en un Client Component.

**Descartada porque:** `docs/conventions.md` reserva SWR para "datos con
refresco frecuente (alertas)". El listado de documentos es un Server
Component con paginación por `searchParams`, lo que evita estado de
React innecesario y mejora el SEO y el tiempo de carga inicial.

---

## Restricciones de convención

- Arrow functions nombradas para todos los componentes (conventions.md).
- Imports con alias `@/` (conventions.md).
- `"use client"` solo en `UploadForm.tsx`.
- Logging centralizado en `lib/logger.ts`.
- El token nunca se expone al cliente JavaScript.
