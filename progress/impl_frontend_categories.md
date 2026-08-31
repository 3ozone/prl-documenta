# Trazabilidad — frontend_categories

## Mapa R → test

| Requirement | Test |
|-------------|------|
| R1 — Página /categories/empresa existe y muestra documentos filtrados | categories.empresa/page.tsx (Server Component) — cubierto por R4 filter test |
| R2 — Página /categories/trabajadores | categories.trabajadores/page.tsx — cubierto por R5 filter test |
| R3 — Página /categories/equipos | categories.equipos/page.tsx — cubierto por R6 filter test |
| R4 — Filtro empresa | `filterDocumentsByCategoria > empresa` en categories.test.tsx |
| R5 — Filtro trabajadores | `filterDocumentsByCategoria > trabajadores` en categories.test.tsx |
| R6 — Filtro equipos | `filterDocumentsByCategoria > equipos` en categories.test.tsx |
| R7 — DocumentsTable render | Heredado de DocumentsTable.test.tsx |
| R8 — Botón subida solo admin | Server Component guard con getRoleFromToken |
| R9 — Redirect a /categories/<cat> si viewer intenta upload | Server Component redirect en upload/page.tsx |
| R10 — Campos empresa en formulario | UploadEmpresaForm.tsx (razon_social, cif, actividad_economica, centro_trabajo) |
| R11 — Campos trabajadores en formulario | UploadTrabajadoresForm.tsx (nombre_trabajador, dni, puesto, tipo_documento) |
| R12 — Campos equipos base | UploadEquiposForm.tsx (id_equipo, nombre_equipo, numero_serie, ubicacion) |
| R13 — Campos mantenimiento condicionales | `UploadEquiposForm > R13 shows mantenimiento fields` en categories.test.tsx; `R13-R14 hides conditional fields initially` |
| R14 — Campos inspección condicionales | `UploadEquiposForm > R14 shows inspeccion fields` en categories.test.tsx |
| R15 — Validación campos requeridos | `UploadEmpresaForm > R15 shows error when razon_social is missing` en categories.test.tsx |
| R16 — Validación solo PDF | `UploadEmpresaForm > R16 rejects non-PDF file` en categories.test.tsx |
| R17 — Envío FormData con categoria | onSubmit en cada form (empresa/trabajadores/equipos) |
| R18 — Redirección en éxito | router.push en onSubmit de cada form |
| R19 — Error inline en fallo | serverError state en cada form |
| R20 — Tipos TypeScript exportados | frontend/src/lib/types.ts — WorkerDocumentType, UploadEmpresaFormValues, UploadTrabajadoresFormValues, UploadEquipoFormValues |

## Resultado tests

```
Test Files  13 passed (13)
Tests       57 passed (57)
```
