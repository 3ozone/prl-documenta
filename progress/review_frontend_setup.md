# Review — feature 10 (frontend_setup)

**Veredicto:** CHANGES_REQUESTED

---

## Trazabilidad requirements ↔ tests

- R1:  [x] Cubierto por estructura de `package.json` + `eslint.config.mjs` + `prettier.config.mjs` (verificable con `npm run lint` y `npm run build`)
- R2:  [x] Cubierto por `npm run build` — build verde con 4 rutas generadas
- R3:  [x] Cubierto por `tests/lib/logger.test.ts` + `tests/lib/api.test.ts` — 6/6 pasan
- R4:  [x] Cubierto por `tsconfig.json` (`"strict": true`) + `npm run build` sin errores tsc
- R5:  [x] Cubierto por `tests/lib/logger.test.ts:2` (`import log from "@/lib/logger"`) resuelto en vitest y build
- R6:  [x] Cubierto por `src/app/layout.tsx:11` (`className="bg-white min-h-screen"`) — Tailwind procesa el archivo
- R7:  [x] Cubierto por `tests/lib/logger.test.ts` — "info emits JSON with level info and event"
- R8:  [x] Cubierto por `tests/lib/logger.test.ts` — `expect(parsed.level).toBe("info")`
- R9:  [x] Cubierto por `tests/lib/logger.test.ts` — `expect(parsed.level).toBe("warn")`
- R10: [x] Cubierto por `tests/lib/logger.test.ts` — `expect(parsed.level).toBe("error")`
- R11: [x] Cubierto por `tests/lib/api.test.ts` — "has status and message"
- R12: [x] Cubierto por `tests/lib/api.test.ts` — "throws ApiError when response is not ok"
- R13: [ ] ← **Sin test en `tests/`**. `middleware.ts` existe y la lógica es correcta, pero `CHECKPOINTS.md` C6 exige test concreto en `tests/` por cada R<n>.
- R14: [ ] ← **Sin test en `tests/`**. El comportamiento (redirect a `/login` sin cookie) no está cubierto por ningún test automatizado.
- R15: [ ] ← **Sin test en `tests/`**. El comportamiento (redirect a `/dashboard` con cookie en `/login`) no está cubierto por ningún test automatizado.
- R16: [ ] ← **Sin test en `tests/`**. El comportamiento (dejar pasar con cookie en ruta protegida) no está cubierto por ningún test automatizado.
- R17: [x] Cubierto por `next.config.ts` (`output: "standalone"`) + `Dockerfile` multistage con `npm ci` + `npm run build` + `npm start`
- R18: [ ] ← Sin test automatizado. `docker build` no se ejecutó como parte de la suite verificable. Se acepta como cobertura débil dado que requiere Docker daemon, pero debe documentarse como limitación en `impl_frontend_setup.md`.
- R19: [ ] ← **Nombre incorrecto**. `specs/frontend_setup/design.md:94` especifica `export type ApiError = { detail: string }`, pero `src/lib/types.ts:1` exporta `ApiErrorResponse` en su lugar. R19 dice explícitamente "exporte los tipos `ApiError`, `UserRole` y `AlertLevel`". El tipo `ApiError` no existe en `types.ts`. La clase `ApiError` de `api.ts` es una entidad distinta.
- R20: [x] Cubierto por `src/lib/fetcher.ts` — `fetcher<T>(url: string): Promise<T>` con lanzamiento de `Error` cuando `!res.ok`

---

## Tasks completas

- T1–T22: [x] Todas marcadas `[x]` en `specs/frontend_setup/tasks.md`

Sin embargo, T18 (`frontend/tests/lib/logger.test.ts`) y T19 (`frontend/tests/lib/api.test.ts`) existen y pasan. **T17 no tiene test asociado** a pesar de que tasks.md la marca `[x]` — la task dice "Crear `frontend/middleware.ts`", no "crear test para middleware". El problema es que ninguna task cubre la creación de `frontend/tests/middleware.test.ts`, y R13–R16 quedan sin cobertura de test.

---

## Checkpoints

- C1: [x] Archivos base y docs presentes; `./init.sh` pendiente de verificar en este contexto (build y tests pasan)
- C2: [x] Solo `frontend_setup` en `in_progress`; `progress/current.md` describe sesión activa
- C3: [x] `frontend/src/` respeta arquitectura; no hay `console.log` fuera de `lib/logger.ts`; no hay `print()` ni `any`; no hay `export default function` en componentes (layout usa arrow function + `export default`)
- C4: [ ] ← `frontend/tests/` solo cubre `lib/logger` y `lib/api`. No hay tests para `middleware.ts`. R13–R16 sin cobertura de test.
- C5: [ ] ← `progress/history.md` no tiene entrada para esta sesión (feature aún `in_progress`, cierre pendiente)
- C6: [ ] ← R13, R14, R15, R16 y R19 sin cobertura de test o con nombre incorrecto (ver arriba)

---

## Cambios requeridos

1. **Crear `frontend/tests/middleware.test.ts`** con al menos 3 casos:
   - `it("redirects to /login when token cookie is absent")` → cubre R14
   - `it("redirects to /dashboard when token cookie is present and path is /login")` → cubre R15
   - `it("allows request to pass when token cookie is present on protected route")` → cubre R16
   - (R13 queda cubierto implícitamente por los anteriores)
   
   Usar mocks de `NextRequest` con `vi.fn()` o construir instancias con `new Request(...)`.

2. **Corregir el nombre del tipo en `frontend/src/lib/types.ts`**: renombrar `ApiErrorResponse` a `ApiError` (o documentar en `impl_frontend_setup.md` por qué se desvía del spec — colisión de nombres con la clase `ApiError` de `api.ts` — y actualizar R19 en `requirements.md` si el cambio es intencionado).
   - Archivo afectado: `frontend/src/lib/types.ts:1`
   - Especificación original: `specs/frontend_setup/design.md:94`

3. **Añadir una task T23 en `specs/frontend_setup/tasks.md`** que cubra los tests de middleware (R13–R16), o documentar en `impl_frontend_setup.md` la justificación de por qué no hay tests automatizados para el middleware (e.g., limitación de entorno de test con Next.js middleware).

4. (Menor) **R18 / Dockerfile**: documentar explícitamente en `impl_frontend_setup.md` que el test de `docker build` no es automatizable en la suite de Vitest y que la verificación fue manual, para que el criterio quede justificado.
