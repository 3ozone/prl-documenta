# Tasks — frontend_setup

> El implementer marca `[x]` cada task al completarla.
> El reviewer rechaza si queda alguna `[ ]` sin justificación documentada.

---

- [x] T1 — Crear `frontend/package.json` con dependencias fijadas: `next@15.x`, `react`, `react-dom`, `typescript`, `tailwindcss`, `eslint`, `prettier`, `vitest`, `@vitejs/plugin-react`, `swr`. Incluir scripts `dev`, `build`, `start`, `lint`, `test`. Cubre: R1, R2, R3.

- [x] T2 — Crear `frontend/tsconfig.json` con `"strict": true` y path alias `"@/*": ["./src/*"]`. Cubre: R4, R5.

- [x] T3 — Crear `frontend/next.config.ts` con `output: "standalone"` y soporte de path aliases. Cubre: R2, R17.

- [x] T4 — Crear `frontend/tailwind.config.ts` con `content: ["./src/**/*.{ts,tsx}"]`. Cubre: R6.

- [x] T5 — Crear `frontend/eslint.config.mjs` (ESLint 9 flat config) y `frontend/prettier.config.mjs`. Cubre: R1.

- [x] T6 — Crear `frontend/vitest.config.ts` con `environment: "node"` y alias `@` → `./src`. Cubre: R3, R5.

- [x] T7 — Crear `frontend/src/app/layout.tsx`: Root layout con `<html>`, `<body className="bg-white">` y `{children}`. Sin `"use client"`. Cubre: R6.

- [x] T8 — Crear `frontend/src/app/page.tsx`: Server Component que redirige a `/dashboard` con `redirect("/dashboard")`. Cubre: R2.

- [x] T9 — Crear `frontend/src/app/login/page.tsx`: Placeholder Server Component con comentario `// Implementado en frontend_auth`. Cubre: R2.

- [x] T10 — Crear `frontend/src/app/dashboard/page.tsx`: Placeholder Server Component con comentario `// Implementado en frontend_dashboard`. Cubre: R2.

- [x] T11 — Crear `frontend/src/lib/logger.ts` con el objeto `log` (métodos `info`, `warn`, `error`) que emite JSON estructurado. Cubre: R7, R8, R9, R10.

- [x] T12 — Crear `frontend/src/lib/api.ts` con la clase `ApiError(status, message)` y la función `apiFetch<T>`. Cubre: R11, R12.

- [x] T13 — Crear `frontend/src/lib/fetcher.ts` con la función `fetcher<T>`. Cubre: R20.

- [x] T14 — Crear `frontend/src/lib/types.ts` con los tipos `ApiError`, `UserRole` y `AlertLevel`. Cubre: R19.

- [x] T15 — Crear `frontend/src/lib/actions.ts` con `"use server"` y comentario placeholder. Cubre: R2.

- [x] T16 — Crear directorios vacíos: `frontend/src/components/ui/`, `frontend/src/components/documents/`, `frontend/src/hooks/`. Añadir `.gitkeep` en cada uno. Cubre: R2.

- [x] T17 — Crear `frontend/middleware.ts` con lógica de rutas públicas `/login`, redirección a `/login` sin token, redirección a `/dashboard` si hay token en `/login`. Cubre: R13, R14, R15, R16.

- [x] T18 — Crear `frontend/tests/lib/logger.test.ts` con `describe("log")` + `it` para cada método (`info`, `warn`, `error`) verificando que el output es JSON con `level` y `event` correctos. Cubre: R7, R8, R9, R10.

- [x] T19 — Crear `frontend/tests/lib/api.test.ts` con tests para: (a) `ApiError` tiene `status` y `message`, (b) `apiFetch` lanza `ApiError` cuando `res.ok === false`. Cubre: R11, R12.

- [x] T20 — Crear `frontend/Dockerfile` multistage (`builder`: `npm ci` + `npm run build`; `runtime`: `npm start`, puerto 3000). Cubre: R17, R18.

- [x] T21 — Ejecutar `npx vitest run` en `frontend/` y verificar que todos los tests pasan (código de salida 0). Cubre: R3, R8, R9, R10, R11, R12.

- [x] T22 — Verificar que `npm run build` en `frontend/` completa sin errores TypeScript ni de compilación. Cubre: R2, R4, R5.

- [x] T23 — Crear `frontend/tests/middleware.test.ts` con 4 casos: R14 (redirect `/login` sin token), R15 (redirect `/dashboard` con token en `/login`), R16 (dejar pasar con token en ruta protegida), R13 (`/login` sin token → `NextResponse.next()`). Cubre: R13, R14, R15, R16.

---

## Trazabilidad rápida

| Requirement | Task(s) |
|-------------|---------|
| R1          | T1, T5  |
| R2          | T1, T3, T7, T8, T9, T10, T15, T16, T22 |
| R3          | T1, T6, T21 |
| R4          | T2, T22 |
| R5          | T2, T6 |
| R6          | T4, T7 |
| R7          | T11, T18 |
| R8          | T11, T18 |
| R9          | T11, T18 |
| R10         | T11, T18 |
| R11         | T12, T19 |
| R12         | T12, T19 |
| R13         | T17, T23 |
| R14         | T17, T23 |
| R15         | T17, T23 |
| R16         | T17, T23 |
| R17         | T3, T20 |
| R18         | T20 (verificación manual — docker build no automatizable en Vitest) |
| R19         | T14 |
| R20         | T13 |
