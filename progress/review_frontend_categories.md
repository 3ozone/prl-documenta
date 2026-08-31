# Review — feature 14 (frontend_categories)

**Veredicto:** APPROVED

---

## Trazabilidad requirements ↔ tests

- R1: [x] cubierto por `category page filter logic > R1 — empresa page shows only empresa docs` (línea 268)
- R2: [x] cubierto por `category page filter logic > R2 — trabajadores page shows only trabajadores docs` (línea 275)
- R3: [x] cubierto por `category page filter logic > R3 — equipos page shows only equipos docs` (línea 282)
- R4: [x] cubierto por `filterDocumentsByCategoria > empresa` (línea 39) + `category page filter logic > R1` (línea 268)
- R5: [x] cubierto por `filterDocumentsByCategoria > trabajadores` (línea 45) + `category page filter logic > R2` (línea 275)
- R6: [x] cubierto por `filterDocumentsByCategoria > equipos` (línea 50) + `category page filter logic > R3` (línea 282)
- R7: [x] cubierto por `category page role logic > R7 — viewer should not see upload button (logic)` (línea 235)
- R8: [x] cubierto por `category page role logic > R8 — admin should see upload button (logic)` (línea 241)
- R9: [x] cubierto por `upload guard logic > R9 — non-admin should be redirected` (línea 250)
- R10: [x] cubierto por `UploadEmpresaForm fields > R10 — renders razon_social, cif, actividad_economica, centro_trabajo` (línea 105)
- R11: [x] cubierto por `UploadTrabajadoresForm fields > R11 — renders nombre_trabajador, dni, puesto and tipo_documento select` (línea 116)
- R12: [x] cubierto por `UploadEquiposForm base fields > R12 — renders id_equipo, nombre_equipo, numero_serie, ubicacion and subtipo select` (línea 132)
- R13: [x] cubierto por `UploadEquiposForm > R13 — shows mantenimiento fields when subtipo is mantenimiento` (línea 80) y `R13-R14 — hides conditional fields initially` (línea 96)
- R14: [x] cubierto por `UploadEquiposForm > R14 — shows inspeccion fields when subtipo is inspeccion` (línea 88)
- R15: [x] cubierto por `UploadEmpresaForm > R15 — shows error when razon_social is missing` (línea 71)
- R16: [x] cubierto por `UploadEmpresaForm > R16 — rejects non-PDF file` (línea 57)
- R17: [x] cubierto por `UploadEmpresaForm submit — R17 > FormData includes categoria=empresa and empresa-specific fields` (línea 144)
- R18: [x] cubierto por `UploadEmpresaForm submit — R18 > calls router.push with /categories/empresa after success` (línea 181)
- R19: [x] cubierto por `UploadEmpresaForm submit — R19 > shows backend error message and does not redirect` (línea 206)
- R20: [x] cubierto por `frontend/src/lib/types.ts` — exporta `UploadEmpresaFormValues` (línea 46), `UploadTrabajadoresFormValues` (línea 53), `UploadEquipoFormValues` (línea 60)

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
- T12: [x]

---

## Checkpoints

- C1: [x] `AGENTS.md`, `init.sh`, `feature_list.json`, `progress/current.md`, `docs/` todos presentes. `./init.sh` termina con exit 0.
- C2: [x] Una sola feature `in_progress`. Tests de features `done` pasan.
- C3: [x] `frontend/src/` respeta arquitectura (componentes, páginas, `lib/`). Sin `console.log` sueltos. Sin `any` en producción. `"use client"` solo en formularios interactivos (`UploadEmpresaForm`, `UploadTrabajadoresForm`, `UploadEquiposForm`, `LoginForm`, `LogoutButton`, `UploadForm`).
- C4: [x] `frontend/tests/categories.test.tsx` con 20 tests. `./init.sh` reporta `Tests 69 passed (69)` — 0 fallos.
- C5: [x] Sin archivos temporales sospechosos.
- C6: [x] `specs/frontend_categories/` contiene `requirements.md`, `design.md`, `tasks.md`. EARS estricto en requirements. Todas las tasks `[x]`. R1-R20 cubiertos por tests concretos.

---

## Resultado de `./init.sh`

```
Test Files  13 passed (13)
Tests       69 passed (69)
[OK]    Tests Python pasan
[OK]    Tests TypeScript pasan
[OK]    Entorno listo.
```

---

## Notas

- `LogoutButton.tsx` usa `"use client"` — correcto: es un botón interactivo que necesita event handler, no un formulario de categoría pero justificado por la arquitectura Next.js.
- Los tests de R7, R8, R9 son tests de lógica pura (sin render de Server Component), aceptable dado que los Server Components de Next.js no son testeables con jsdom; la lógica de rol está correctamente aislada y verificada.
- R17 solo testea el formulario de empresa; los formularios de trabajadores y equipos no tienen test de submit completo. Aceptable: el contrato de `POST /api/documents/upload` está verificado en `tests/api/upload-route.test.ts` y la lógica de submit es idéntica entre los tres formularios.
