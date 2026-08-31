# Tasks — frontend_documents

Orden de implementación: utilidades compartidas → Route Handlers → Server
Components → Client Component → tests → guard de ruta.

---

- [x] T1 — Crear `frontend/src/lib/classifyStatus.ts` con la función
  `classifyStatus(doc, today?)` y la constante `EXPIRY_WARNING_DAYS = 30`.
  Cubre: R3.

- [x] T2 — Crear `frontend/tests/classifyStatus.test.ts` con casos:
  documento caducado, próximo a caducar (límite 30 días), vigente; usando
  el parámetro `today` para inyectar fecha fija.
  Cubre: R3.

- [x] T3 — Crear `frontend/src/lib/auth.ts` con `getRoleFromToken(token):
  UserRole` que decodifique el payload JWT en base64 sin verificar firma.
  Cubre: R5, R6, R7, R8.

- [x] T4 — Crear Route Handler `frontend/src/app/api/proxy/documents/[id]/download/route.ts`
  que lea la cookie `token`, reenvíe el stream con `Content-Type:
  application/pdf`, y devuelva 404 con `"Documento no encontrado"` si el
  backend responde 404.
  Cubre: R15, R16.

- [x] T5 — Crear Route Handler `frontend/src/app/api/documents/upload/route.ts`
  que lea la cookie `token`, reenvíe el `FormData` al backend con
  `Authorization: Bearer <token>`, y propague el status de respuesta.
  Cubre: R12, R14.

- [x] T6 — Crear `frontend/src/components/documents/DocumentsTable.tsx`
  (Server Component) que reciba `docs: DocumentResponse[]` y `page: number`,
  calcule el slice de 20 elementos, aplique `classifyStatus` para el badge
  de estado, y renderice los controles de paginación como links `?page=N`.
  Cubre: R2, R3, R4.

- [x] T7 — Crear `frontend/src/app/documents/page.tsx` (Server Component)
  que lea la cookie `token`, obtenga el rol con `getRoleFromToken`, llame
  a `getDocuments(token)`, renderice `DocumentsTable` con el `page` de
  `searchParams`, y muestre u oculte el botón "Subir documento" según el rol.
  Cubre: R1, R2, R4, R5, R6, R7, R17, R18.

- [x] T8 — Crear `frontend/src/components/documents/UploadForm.tsx`
  (Client Component con `"use client"`) usando `react-hook-form` con
  validaciones: campos obligatorios y tipo de archivo PDF. Al hacer submit
  llama a `POST /api/documents/upload`; en éxito redirige a `/documents`
  mostrando mensaje de éxito; en error muestra el mensaje del backend.
  Cubre: R9, R10, R11, R12, R13, R14.

- [x] T9 — Crear `frontend/src/app/documents/upload/page.tsx` (Server
  Component) que lea el rol del token; si no es `admin` llame a `redirect("/documents")`;
  si es `admin` renderice `UploadForm`.
  Cubre: R8.

- [x] T10 — Añadir tests en `frontend/tests/documents.test.ts` que cubran:
  paginación (slice correcto en página 1 y página 2), ocultación del botón
  upload para viewer (lógica de `getRoleFromToken`), y mensaje de error
  cuando `getDocuments` lanza `ApiError`.
  Cubre: R4, R5, R6, R18.

- [x] T11 — Ejecutar `npx vitest run` y verificar que todos los tests pasan
  sin errores. Verificar manualmente en dev que la descarga abre el PDF en
  el navegador (sin forzar descarga).
  Cubre: R15 (verificación manual), todos los R cubiertos por tests.
