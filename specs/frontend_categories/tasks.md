# Tasks — frontend_categories

> El implementer marca `[x]` al completar cada task. El reviewer rechaza
> si queda alguna `[ ]` sin justificación documentada.

---

- [x] T1 — Añadir tipos `WorkerDocumentType`, `UploadEmpresaFormValues`,
  `UploadTrabajadoresFormValues`, `UploadEquipoFormValues` en
  `frontend/src/lib/types.ts`. Cubre: R20.

- [x] T2 — Crear `frontend/src/components/categories/UploadEmpresaForm.tsx`
  (Client Component): react-hook-form con campos comunes + `razon_social`,
  `cif`, `actividad_economica`, `centro_trabajo`; valida PDF en cliente;
  llama a `/api/documents/upload` con `categoria="empresa"`; redirige a
  `/categories/empresa` en éxito o muestra error inline. Cubre: R10, R15,
  R16, R17, R18, R19.

- [x] T3 — Crear `frontend/src/components/categories/UploadTrabajadoresForm.tsx`
  (Client Component): react-hook-form con campos comunes + `nombre_trabajador`,
  `dni`, `puesto`, `tipo_documento` (select con los cuatro valores de
  `WorkerDocumentType`); valida PDF en cliente; llama a
  `/api/documents/upload` con `categoria="trabajadores"`; redirige o muestra
  error. Cubre: R11, R15, R16, R17, R18, R19.

- [x] T4 — Crear `frontend/src/components/categories/UploadEquiposForm.tsx`
  (Client Component): react-hook-form con campos comunes + campos base de
  equipo + select `subtipo`; campos condicionales de mantenimiento visibles
  solo cuando `subtipo === "mantenimiento"`; campos condicionales de
  inspección visibles solo cuando `subtipo === "inspeccion"`; valida PDF;
  llama a `/api/documents/upload` con `categoria="equipos"`. Cubre: R12, R13,
  R14, R15, R16, R17, R18, R19.

- [x] T5 — Crear `frontend/src/app/categories/empresa/page.tsx` (Server
  Component): carga todos los documentos, filtra por `categoria === "empresa"`,
  muestra `DocumentsTable`; botón de subida visible solo para `admin`.
  Cubre: R1, R4, R7, R8.

- [x] T6 — Crear `frontend/src/app/categories/empresa/upload/page.tsx`
  (Server Component guard): redirige a `/categories/empresa` si el rol no es
  `admin`; si es admin renderiza `UploadEmpresaForm`. Cubre: R9.

- [x] T7 — Crear `frontend/src/app/categories/trabajadores/page.tsx`
  (Server Component): carga todos los documentos, filtra por
  `categoria === "trabajadores"`, muestra `DocumentsTable`; botón condicional.
  Cubre: R2, R5, R7, R8.

- [x] T8 — Crear `frontend/src/app/categories/trabajadores/upload/page.tsx`
  (Server Component guard): redirige a `/categories/trabajadores` si viewer;
  si admin renderiza `UploadTrabajadoresForm`. Cubre: R9.

- [x] T9 — Crear `frontend/src/app/categories/equipos/page.tsx` (Server
  Component): carga todos los documentos, filtra por `categoria === "equipos"`,
  muestra `DocumentsTable`; botón condicional. Cubre: R3, R6, R7, R8.

- [x] T10 — Crear `frontend/src/app/categories/equipos/upload/page.tsx`
  (Server Component guard): redirige a `/categories/equipos` si viewer; si
  admin renderiza `UploadEquiposForm`. Cubre: R9.

- [x] T11 — Añadir tests en `frontend/tests/categories.test.tsx`:
  - `filterDocumentsByCategoria_empresa` — dado un array mixto, filtrando
    por `"empresa"` solo devuelve los de esa categoría. Cubre: R4.
  - `filterDocumentsByCategoria_trabajadores` — mismo patrón. Cubre: R5.
  - `filterDocumentsByCategoria_equipos` — mismo patrón. Cubre: R6.
  - `uploadEmpresaForm_rejectsNonPdf` — simula submit con archivo no-PDF,
    verifica que el error aparece antes del fetch. Cubre: R16.
  - `uploadEmpresaForm_rejectsMissingField` — submit sin `razon_social`,
    verifica mensaje de error en cliente. Cubre: R15.
  - `uploadEquiposForm_showsMantenimientoFields` — cuando `subtipo` es
    `"mantenimiento"` los campos de mantenimiento son visibles. Cubre: R13.
  - `uploadEquiposForm_showsInspeccionFields` — cuando `subtipo` es
    `"inspeccion"` los campos de inspección son visibles. Cubre: R14.
  - `uploadEquiposForm_hidesConditionalFieldsInitially` — sin subtipo
    seleccionado ningún campo condicional es visible. Cubre: R13, R14.

- [x] T12 — Ejecutar `npx vitest run` en `frontend/` y verificar que todos
  los tests nuevos pasan con 0 fallos. Cubre: R4, R5, R6, R13, R14, R15,
  R16.
