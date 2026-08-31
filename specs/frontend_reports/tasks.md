# Tasks — frontend_reports

> Feature id: 16 | Cada task es atómica y verificable. El implementer marca `[x]` al completar.

---

- [x] **T1** — Añadir tipos `ReportFormat` y `ReportCategoria` en
  `frontend/src/lib/types.ts`.
  Cubre: **R3, R4**.
  _Test: `frontend/tests/lib/types.test.ts` — verifica que los tipos aceptan
  únicamente los valores declarados (narrowing de TypeScript en tiempo de
  compilación; test de integración que asigna valores válidos e inválidos)._

---

- [x] **T2** — Crear el Route Handler proxy
  `frontend/src/app/api/proxy/reports/route.ts` con la función `GET` que:
  - Lee `formato` y `categoria` de query params.
  - Lee la cookie `token` y devuelve `401` si no existe.
  - Reenvía la petición al backend con `Authorization: Bearer`.
  - Retransmite el blob con `Content-Type` y `Content-Disposition`.
  - Devuelve `502` ante errores 5xx del backend.
  Cubre: **R7, R8, R11, R12**.
  _Test: `frontend/tests/app/api/proxy/reports/route.test.ts` — mockea `fetch`
  del backend y verifica cada rama (200, 401, 403, 500)._

---

- [x] **T3** — Crear el Client Component
  `frontend/src/app/(dashboard)/reports/ReportsForm.tsx` con:
  - Estado interno `formato`, `categoria`, `loading`, `error`.
  - Selector de formato (CSV / PDF, default CSV).
  - Selector de categoría (todas / empresa / trabajadores / equipos, default todas).
  - Botón "Generar informe" deshabilitado durante `loading`.
  - Indicador de carga visible mientras `loading === true`.
  Cubre: **R3, R4, R5, R10**.
  _Test: `frontend/tests/app/(dashboard)/reports/ReportsForm.test.tsx` —
  renderiza el componente y verifica valores por defecto de los selectores y
  estado inicial del botón._

---

- [x] **T4** — Implementar el handler de clic en `ReportsForm` que:
  - Llama a `fetch("/api/proxy/reports?formato=…&categoria=…")`.
  - Activa `loading = true` antes de la petición.
  - Al recibir `200`, crea un object URL, inyecta `<a download>` y lo hace
    click automático, luego invoca `URL.revokeObjectURL`.
  - Desactiva `loading = false` en el bloque `finally`.
  Cubre: **R5, R6, R9, R10**.
  _Test: `ReportsForm.test.tsx` — mockea `fetch` para devolver un blob 200 y
  verifica que se llama a `URL.createObjectURL` y que `loading` vuelve a
  `false` al finalizar._

---

- [x] **T5** — Implementar el manejo de errores en el handler de clic de
  `ReportsForm`:
  - Si la respuesta es `401` / `403`, establece `error = "No tienes permiso
    para generar informes."`.
  - Si la respuesta es cualquier otro código no-2xx, establece
    `error = "Error al generar el informe. Inténtalo de nuevo."`.
  - Renderiza el mensaje de error en `<p role="alert">`.
  Cubre: **R11, R12**.
  _Test: `ReportsForm.test.tsx` — mockea `fetch` para 401, 403 y 500;
  verifica el texto del mensaje de error en el DOM._

---

- [x] **T6** — Crear la página Server Component
  `frontend/src/app/(dashboard)/reports/page.tsx` que importe y renderice
  `<ReportsForm />`. Verificar que el middleware existente protege la ruta
  (sin cookie → redirect a `/login`).
  Cubre: **R1, R2**.
  _Test: `frontend/tests/app/(dashboard)/reports/page.test.tsx` — renderiza la
  página y comprueba que `ReportsForm` está presente. La protección del
  middleware se verifica en el test de integración de middleware existente
  ampliando su suite para incluir la ruta `/reports`._

---

- [x] **T7** — Ampliar la suite de tests del middleware
  (`frontend/tests/middleware.test.ts`) para incluir la ruta `/reports` entre
  las rutas protegidas que deben redirigir a `/login` sin cookie válida.
  Cubre: **R1, R2**.
  _Test: verifica que una petición a `/reports` sin cookie devuelve redirect
  a `/login`._
