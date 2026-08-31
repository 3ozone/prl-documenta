# Tasks — frontend_dashboard

El implementer marca cada `[x]` al completarla. El reviewer rechaza si
queda alguna `[ ]` sin justificación documentada.

---

- [x] T1 — Añadir `AlertResponse`, `DocumentResponse` y `DocumentStatus`
  en `frontend/src/lib/types.ts`.
  **Cubre:** R11, R12, R15.

- [x] T2 — Añadir `getAlerts(token)` y `getDocuments(token)` en
  `frontend/src/lib/api.ts`.
  **Cubre:** R13, R14.

- [x] T3 — Crear `frontend/src/components/dashboard/AlertSummaryWidget.tsx`
  como Server Component: fetch a `getAlerts`, agrupación por nivel con
  inicialización a 0, fallback en catch, sin `"use client"`.
  **Cubre:** R2, R5, R8, R16, R19.

- [x] T4 — Crear `frontend/src/components/dashboard/CategorySummaryWidget.tsx`
  como Server Component: fetch a `getDocuments`, agrupación por categoría
  con inicialización a 0, fallback en catch, sin `"use client"`.
  **Cubre:** R3, R6, R9, R17, R19.

- [x] T5 — Crear `frontend/src/components/dashboard/StatusSummaryWidget.tsx`
  como Server Component: fetch a `getDocuments`, cálculo de `DocumentStatus`
  usando `EXPIRY_WARNING_DAYS = 30`, agrupación por estado con
  inicialización a 0, fallback en catch, sin `"use client"`.
  **Cubre:** R4, R7, R10, R18, R19.

- [x] T6 — Reemplazar el stub en `frontend/src/app/dashboard/page.tsx`
  por `DashboardPage` async que lee la cookie `token` y compone los tres
  widgets. Sin spinner explícito.
  **Cubre:** R1, R19, R20.

- [x] T7 — Añadir tests de unidad en `frontend/tests/dashboard.test.ts`:
  - `it("groups alerts by level and initialises missing levels to 0")` — lógica
    de agrupación de alertas extraída como función pura.
  - `it("groups documents by category and initialises missing categories to 0")`
  - `it("classifies document status as vigente when expiry > 30 days")`
  - `it("classifies document status as proxima_a_caducar when expiry <= 30 days")`
  - `it("classifies document status as caducada when expiry date is past")`
  **Cubre:** R2, R3, R4, R16, R17, R18.

- [x] T8 — Ejecutar `npx vitest run` en `frontend/` y verificar que todos
  los tests pasan. Documentar trazabilidad `R<n>` ↔ test en
  `progress/impl_frontend_dashboard.md`.
  **Cubre:** R1–R20 (verificación integral).
