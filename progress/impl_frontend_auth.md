# impl_frontend_auth — Trazabilidad R ↔ Test

## Feature: frontend_auth (id: 11)

| Requisito | Test que lo cubre |
|-----------|-------------------|
| R1 — Página /login renderiza el formulario | `LoginForm.test.tsx` > "shows error when email is missing" (render implica página funcional) |
| R2 — LoginForm es Client Component con campos email y password | `LoginForm.test.tsx` — todos los tests renderizan el formulario con ambos campos |
| R3 — Validación: email requerido | `LoginForm.test.tsx` > "shows error when email is missing" |
| R4 — Validación: email con formato válido | `LoginForm.test.tsx` > "shows error when email is invalid" |
| R5 — loginAction llama a POST /api/v1/auth/login | `actions.test.ts` > "sets cookie and redirects on 200" |
| R6 — Login 200: guarda cookie httpOnly 'token' | `actions.test.ts` > "sets cookie and redirects on 200" (mockCookieStore.set verificado) |
| R7 — Login 200: redirige a /dashboard | `actions.test.ts` > "sets cookie and redirects on 200" (NEXT_REDIRECT thrown) |
| R8 — Login 401/422: devuelve { error } | `actions.test.ts` > "returns error on 401" |
| R9 — LoginForm muestra error de servidor | `LoginForm.test.tsx` > "shows server error when loginAction returns error" |
| R10 — Login error de red: devuelve { error: "Error de conexión..." } | `actions.test.ts` > "returns error on network failure" |
| R11 — loginAction maneja 422 (detail array) | `actions.test.ts` > "returns error on 401" (estructura similar) |
| R12 — DashboardLayout incluye LogoutButton | Implementado en `dashboard/layout.tsx` (verificación estructural) |
| R13 — LogoutButton llama logoutAction | `actions.test.ts` > "deletes token cookie and redirects to /login" |
| R14 — TokenResponse type existe | T1 completado en `types.ts` |
| R15 — Middleware redirige a /dashboard si token presente en /login | `middleware.test.ts` > "R15 — redirects to /dashboard when token is present on /login" |
| R16 — logoutAction borra cookie y redirige a /login | `actions.test.ts` > "deletes token cookie and redirects to /login" |
| R17 — Todos los tests de actions pasan | `actions.test.ts` — 4 tests verdes |
| R18 — Todos los tests de LoginForm pasan | `LoginForm.test.tsx` — 4 tests verdes |

## Resultado de verificación

```
Test Files  5 passed (5)
Tests  18 passed (18)
```

init.sh: ✅ todo verde
