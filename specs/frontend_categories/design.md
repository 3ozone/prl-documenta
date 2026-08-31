# Design — frontend_categories

## Contexto

`frontend_documents` (id 13) ya implementó el Route Handler
`POST /api/documents/upload`, `UploadForm.tsx` base, `lib/auth.ts`
(`getRoleFromToken`), `lib/api.ts` (`getDocuments`, `uploadDocument`) y
`lib/classifyStatus.ts`. Esta feature reutiliza todo eso añadiendo tres
nuevas páginas de categoría con formularios específicos.

---

## Archivos a crear

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `frontend/src/app/categories/empresa/page.tsx` | Server Component | Listado filtrado por `categoria="empresa"` + botón subida condicional |
| `frontend/src/app/categories/empresa/upload/page.tsx` | Server Component (guard) | Verifica rol admin; renderiza `UploadEmpresaForm` o redirige |
| `frontend/src/app/categories/trabajadores/page.tsx` | Server Component | Listado filtrado por `categoria="trabajadores"` |
| `frontend/src/app/categories/trabajadores/upload/page.tsx` | Server Component (guard) | Verifica rol admin; renderiza `UploadTrabajadoresForm` |
| `frontend/src/app/categories/equipos/page.tsx` | Server Component | Listado filtrado por `categoria="equipos"` |
| `frontend/src/app/categories/equipos/upload/page.tsx` | Server Component (guard) | Verifica rol admin; renderiza `UploadEquiposForm` |
| `frontend/src/components/categories/UploadEmpresaForm.tsx` | Client Component | react-hook-form con campos de empresa |
| `frontend/src/components/categories/UploadTrabajadoresForm.tsx` | Client Component | react-hook-form con campos de trabajador (tipo_documento como select) |
| `frontend/src/components/categories/UploadEquiposForm.tsx` | Client Component | react-hook-form con campos de equipo + campos condicionales según subtipo |
| `frontend/tests/categories.test.ts` | Vitest | Tests de filtrado por categoría y renderizado condicional |

---

## Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `frontend/src/lib/types.ts` | Añadir `UploadEmpresaFormValues`, `UploadTrabajadoresFormValues`, `UploadEquipoFormValues` |

> El Route Handler `POST /api/documents/upload` ya existe — no se modifica.
> `getDocuments(token)` ya existe — no se modifica.

---

## Firmas nuevas

### `frontend/src/lib/types.ts` (añadir)

```ts
export type WorkerDocumentType =
  | "formacion"
  | "reconocimiento_medico"
  | "entrega_epi"
  | "aptitud_medica"

// Campos comunes a todos los formularios de subida
type UploadBaseFormValues = {
  nombre_archivo: string
  fecha_validez: string
  fecha_caducidad: string
  file: FileList
}

export type UploadEmpresaFormValues = UploadBaseFormValues & {
  razon_social: string
  cif: string
  actividad_economica: string
  centro_trabajo: string
}

export type UploadTrabajadoresFormValues = UploadBaseFormValues & {
  nombre_trabajador: string
  dni: string
  puesto: string
  tipo_documento: WorkerDocumentType
}

export type UploadEquipoFormValues = UploadBaseFormValues & {
  id_equipo: string
  nombre_equipo: string
  numero_serie: string
  ubicacion: string
  subtipo: "mantenimiento" | "inspeccion"
  // Mantenimiento
  tipo_mantenimiento?: string
  empresa_mantenedora?: string
  fecha_proximo_mantenimiento?: string
  // Inspección
  organismo_inspector?: string
  resultado_inspeccion?: string
  fecha_proxima_inspeccion?: string
}
```

### Patrón de página de listado por categoría

```tsx
// frontend/src/app/categories/empresa/page.tsx
// Server Component — sin "use client"
const EmpresaPage = async () => {
  const token = (await cookies()).get("token")!.value
  const role = getRoleFromToken(token)
  const allDocs = await getDocuments(token)
  const docs = allDocs.filter((d) => d.categoria === "empresa")
  return (
    <main>
      {role === "admin" && (
        <a href="/categories/empresa/upload">Subir documento</a>
      )}
      <DocumentsTable docs={docs} page={1} />
    </main>
  )
}
export default EmpresaPage
```

> `DocumentsTable` ya existe en `frontend_documents`; se reutiliza sin
> modificaciones.

### Patrón de guard de upload por categoría

```tsx
// frontend/src/app/categories/empresa/upload/page.tsx
// Server Component — sin "use client"
import { redirect } from "next/navigation"

const EmpresaUploadPage = async () => {
  const token = (await cookies()).get("token")!.value
  const role = getRoleFromToken(token)
  if (role !== "admin") redirect("/categories/empresa")
  return <UploadEmpresaForm />
}
export default EmpresaUploadPage
```

### `UploadEmpresaForm.tsx`

```tsx
"use client"
const UploadEmpresaForm = () => {
  const { register, handleSubmit, formState: { errors } } =
    useForm<UploadEmpresaFormValues>()

  const onSubmit = async (data: UploadEmpresaFormValues) => {
    const fd = new FormData()
    fd.append("categoria", "empresa")
    fd.append("nombre_archivo", data.nombre_archivo)
    fd.append("fecha_validez", data.fecha_validez)
    fd.append("fecha_caducidad", data.fecha_caducidad)
    fd.append("file", data.file[0])
    fd.append("razon_social", data.razon_social)
    fd.append("cif", data.cif)
    fd.append("actividad_economica", data.actividad_economica)
    fd.append("centro_trabajo", data.centro_trabajo)
    const res = await fetch("/api/documents/upload", { method: "POST", body: fd })
    if (res.ok) router.push("/categories/empresa?success=1")
    else setError(await res.text())
  }
  // ...campos del formulario
}
export { UploadEmpresaForm }
```

### `UploadEquiposForm.tsx` (fragmento condicional)

```tsx
"use client"
const UploadEquiposForm = () => {
  const { register, handleSubmit, watch, formState: { errors } } =
    useForm<UploadEquipoFormValues>()
  const subtipo = watch("subtipo")

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* campos comunes + campos base equipo */}
      <select {...register("subtipo", { required: true })}>
        <option value="mantenimiento">Mantenimiento</option>
        <option value="inspeccion">Inspección</option>
      </select>

      {subtipo === "mantenimiento" && (
        <>
          <input {...register("tipo_mantenimiento")} />
          <input {...register("empresa_mantenedora")} />
          <input type="date" {...register("fecha_proximo_mantenimiento")} />
        </>
      )}

      {subtipo === "inspeccion" && (
        <>
          <input {...register("organismo_inspector")} />
          <input {...register("resultado_inspeccion")} />
          <input type="date" {...register("fecha_proxima_inspeccion")} />
        </>
      )}
    </form>
  )
}
export { UploadEquiposForm }
```

---

## Manejo de errores

- Páginas de listado: si `getDocuments` lanza `ApiError`, renderizan
  mensaje de error inline con `log.error(...)` (mismo patrón que
  `DocumentsPage`).
- Formularios de subida: capturan el error del Route Handler y lo muestran
  bajo el botón de submit sin redirigir.
- Guards de upload: usan `redirect()` de Next.js para viewers.

---

## Alternativa descartada — Ruta dinámica `/categories/[slug]/`

**Propuesta:** una única ruta dinámica
`/categories/[slug]/page.tsx` que derive el filtro y el formulario del
parámetro `slug`.

**Descartada porque:** los tres formularios tienen estructuras de tipos y
campos condicionales radicalmente distintos. Una ruta dinámica única
requeriría discriminación de tipos en runtime con casting, lo que
contradiría el principio `strict: true` de TypeScript y dificultaría la
validación de react-hook-form por formulario. La duplicación de tres
páginas es menor y permite tipos explícitos y seguros.

---

## Alternativa descartada — Filtrado en servidor (query param al backend)

**Propuesta:** llamar a `GET /api/v1/documents?categoria=empresa` en lugar
de cargar todos y filtrar en cliente.

**Descartada porque:** la decisión ya está tomada en el enunciado
("reutilizar `getDocuments(token)` filtrando en cliente — ya cargamos
todos") y es consistente con el comportamiento de `frontend_documents`.
Cambiar el contrato con el backend está fuera del alcance de esta feature.

---

## Restricciones de convención

- Arrow functions nombradas para todos los componentes.
- `"use client"` solo en los tres componentes de formulario.
- Imports con alias `@/`.
- Logging centralizado en `lib/logger.ts`.
- El token nunca se expone al cliente JavaScript.
