# Trazabilidad R<n> → test — feature 13 (frontend_documents)

## Mapa completo

| R    | Test |
|------|------|
| R1   | `tests/components/DocumentsTable.test.tsx` — "shows vigente badge" / "shows caducada badge" |
| R2   | `tests/components/DocumentsTable.test.tsx` — "renders all column headers", "renders document row with download link", "shows empty state" |
| R3   | `tests/classifyStatus.test.ts` — 4 casos |
| R4   | `tests/documents.test.ts` — paginación (3 tests) |
| R5   | `tests/documents.test.ts` — "returns viewer for a valid viewer JWT" |
| R6   | `tests/documents.test.ts` — "returns admin for a valid admin JWT" |
| R7   | `tests/documents.test.ts` — "returns viewer for an invalid token" |
| R8   | `tests/documents.test.ts` — "R8 — getRoleFromToken returns viewer for viewer JWT" |
| R9   | `tests/components/UploadForm.test.tsx` — "R9 — renders all required fields" |
| R10  | `tests/components/UploadForm.test.tsx` — "R10 — shows error when non-PDF file is selected" |
| R11  | `tests/components/UploadForm.test.tsx` — "R11 — shows required errors when submitting empty form" |
| R12  | `tests/api/upload-route.test.ts` — "R12 — includes Authorization Bearer header when token exists" |
| R13  | `tests/components/UploadForm.test.tsx` — "R13 — shows success message after successful upload" |
| R14  | `tests/components/UploadForm.test.tsx` — "R14 — shows backend error message when upload fails" |
| R15  | `tests/api/download-route.test.ts` — "R15 — returns application/pdf content-type on success" |
| R16  | `tests/api/download-route.test.ts` — "R16 — returns 404 with 'Documento no encontrado'" |
| R17  | `tests/middleware.test.ts` — redirige a /login sin cookie |
| R18  | `tests/documents.test.ts` — "R18 — ApiError is thrown and has status property" |

## Resultado: 18/18 cubiertos

Todos los tests pasan: 49/49 ✅
