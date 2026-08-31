# Review — feature 13 (frontend_documents)

**Veredicto:** APPROVED

---

## Trazabilidad requirements ↔ tests

| R     | Estado | Evidencia |
|-------|--------|-----------|
| R1  | [x] | `tests/components/DocumentsTable.test.tsx` — "R1 — shows vigente badge for future document", "R1 — shows caducada badge for expired document" |
| R2  | [x] | `tests/components/DocumentsTable.test.tsx` — "R2 — renders all column headers", "R2 — renders document row with download link", "R2 — shows empty state when no documents" |
| R3  | [x] | `tests/classifyStatus.test.ts` — 4 casos: caducada, proxima_a_caducar ×2, vigente |
| R4  | [x] | `tests/documents.test.ts` — "returns first 20 on page 1", "correct slice on page 2", "remaining on last page" |
| R5  | [x] | `tests/documents.test.ts` — `getRoleFromToken` devuelve `viewer` para JWT viewer |
| R6  | [x] | `tests/documents.test.ts` — `getRoleFromToken` devuelve `admin` para JWT admin |
| R7  | [x] | `tests/documents.test.ts` — `getRoleFromToken` devuelve `viewer` para token inválido/vacío |
| R8  | [x] | `tests/documents.test.ts` — "R8 — getRoleFromToken returns viewer for viewer JWT" (upload page guard) |
| R9  | [x] | `tests/components/UploadForm.test.tsx` — "R9 — renders all required fields" |
| R10 | [x] | `tests/components/UploadForm.test.tsx` — "R10 — shows error when non-PDF file is selected" |
| R11 | [x] | `tests/components/UploadForm.test.tsx` — "R11 — shows required errors when submitting empty form" |
| R12 | [x] | `tests/api/upload-route.test.ts` — "R12 — includes Authorization Bearer header when token exists" |
| R13 | [x] | `tests/components/UploadForm.test.tsx` — "R13 — shows success message after successful upload" |
| R14 | [x] | `tests/components/UploadForm.test.tsx` — "R14 — shows backend error message when upload fails" |
| R15 | [x] | `tests/api/download-route.test.ts` — "R15 — returns application/pdf content-type on success" |
| R16 | [x] | `tests/api/download-route.test.ts` — "R16 — returns 404 with 'Documento no encontrado' when backend returns 404" |
| R17 | [x] | `tests/middleware.test.ts` — redirige a /login sin cookie |
| R18 | [x] | `tests/documents.test.ts` — "R18 — ApiError is thrown and has status property" |

**Resultado: 18/18 cubiertos.**

---

## Tasks completas

- T1: [x]
- T2: [x]
- T3: [x]
- T4: [x]
- T5: [x]
- T6: [x]
- T7: [x]
- T8: [x]
- T9: [x]
- T10: [x]
- T11: [x]

---

## Checkpoints

- C1: [x] Archivos base y docs existen. `./init.sh` termina con exit code 0.
- C2: [x] Solo feature 13 en `in_progress`. `progress/current.md` describe la sesión activa.
- C3: [x] Sin `any` en producción (`grep ": any"` vacío en `frontend/src/`). Sin `"use client"` en layouts. `UploadForm.tsx` tiene `"use client"` correctamente. Sin `console.log` sueltos fuera de `lib/logger.ts`.
- C4: [x] 49/49 tests verdes en 12 suites. Todos los R1–R18 cubiertos con tests concretos.
- C5: [x] `progress/history.md` actualizado con entrada para esta sesión.
- C6: [x] `specs/frontend_documents/` con 3 archivos. T1–T11 todos `[x]`. Cada R1–R18 cubierto por test en `tests/`.

---

## Cambios requeridos

Ninguno.
