# Tasks — frontend_auth

> El implementer marca `[x]` cada task al completarla.
> El reviewer rechaza si queda alguna `[ ]` sin justificación documentada.

---

- [x] T1 — Añadir `TokenResponse` a `frontend/src/lib/types.ts`. Cubre: R14.

- [x] T2 — Implementar `loginAction` y `logoutAction` en `frontend/src/lib/actions.ts` con manejo de 200, 401/422 y error de red. Cubre: R5, R6, R7, R8, R10, R11, R16.

- [x] T3 — Crear `frontend/src/components/auth/LoginForm.tsx` (Client Component) con campos `email` y `password`, validaciones de `react-hook-form` y renderizado del error de servidor. Cubre: R2, R3, R4, R9.

- [x] T4 — Crear `frontend/src/app/login/page.tsx` (Server Component) que importe y renderice `LoginForm`. Cubre: R1.

- [x] T5 — Crear `frontend/src/components/auth/LogoutButton.tsx` (Client Component) con `<form action={logoutAction}>`. Cubre: R13.

- [x] T6 — Crear `frontend/src/app/dashboard/layout.tsx` (Server Component) que incluya `LogoutButton` en el header. Cubre: R12.

- [x] T7 — Crear `frontend/tests/lib/actions.test.ts` con los cuatro casos: `loginAction` 200, `loginAction` 401, `loginAction` error de red, `logoutAction`. Cubre: R5, R6, R7, R8, R10, R11, R16, R17.

- [x] T8 — Crear `frontend/tests/components/LoginForm.test.tsx` con los cuatro casos: email requerido, email inválido, password corta, mensaje de error de servidor visible. Cubre: R3, R4, R9, R18.

- [x] T9 — Añadir test de middleware en `frontend/tests/middleware.test.ts` (o fichero existente) que verifique que una petición a `/login` con cookie `token` redirige a `/dashboard`. Cubre: R15.

- [x] T10 — Ejecutar `npx vitest run` y verificar que todos los tests pasan en verde. Cubre: R17, R18.
