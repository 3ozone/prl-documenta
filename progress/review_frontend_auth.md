# Review — feature 11 (frontend_auth)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

- R1: [x] cubierto por `LoginForm.test.tsx` (renderiza `LoginForm`) + existencia verificada de `login/page.tsx`
- R2: [x] cubierto por `LoginForm.test.tsx` — campos `email` y `password` con react-hook-form
- R3: [x] cubierto por `LoginForm.test.tsx` → `it("shows error when email is missing")` y `it("shows error when email is invalid")`
- R4: [x] cubierto por `LoginForm.test.tsx` → `it("shows error when password is too short")`
- R5: [x] cubierto por `actions.test.ts` → `it("sets cookie and redirects on 200")` — verifica llamada a fetch con JSON
- R6: [x] cubierto por `actions.test.ts` → `it("sets cookie and redirects on 200")` — verifica `mockCookieStore.set("token", "tok123", { httpOnly: true, ... })`
- R7: [x] cubierto por `actions.test.ts` → `it("sets cookie and redirects on 200")` — rejects con `NEXT_REDIRECT`
- R8: [x] cubierto por `actions.test.ts` → `it("returns error on 401")`
- R9: [x] cubierto por `LoginForm.test.tsx` → `it("shows server error when loginAction returns error")` — elemento con `role="alert"`
- R10: [x] cubierto por `actions.test.ts` → `it("deletes token cookie and redirects to /login")` — verifica `cookieStore.delete("token")`
- R11: [x] cubierto por `actions.test.ts` → `it("deletes token cookie and redirects to /login")` — rejects con `NEXT_REDIRECT`
- R12: [x] cubierto por inspección de `dashboard/layout.tsx` (contiene `<LogoutButton />`) + tests de middleware verdes
- R13: [x] cubierto por inspección de `LogoutButton.tsx` — `<form action={logoutAction}>`
- R14: [x] cubierto por `types.ts` línea 9-12 — tipo `TokenResponse` declarado
- R15: [x] cubierto por `middleware.test.ts` → `it("R15 — redirects to /dashboard when token is present on /login")`
- R16: [x] cubierto por `actions.test.ts` → `it("returns error on network failure")`
- R17: [x] cubierto por `actions.test.ts` — 4 casos: loginAction 200, loginAction 401, loginAction error de red, logoutAction
- R18: [x] cubierto por `LoginForm.test.tsx` — 4 casos: email requerido, email inválido, password corta, mensaje de error de servidor

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

## Checkpoints

- C1: [x] Archivos base y docs presentes; `./init.sh` termina con exit 0
- C2: [x] Solo `frontend_auth` en `in_progress`; `progress/current.md` coherente
- C3: [x] Estructura respeta `docs/architecture.md`; sin `any` en producción; sin `console.log` fuera de `lib/logger.ts`
- C4: [x] 18/18 tests verdes — 5 archivos de test, todos pasan
- C5: [x] Sin archivos temporales sospechosos; `progress/impl_frontend_auth.md` existe
- C6: [x] `specs/frontend_auth/` tiene los 3 archivos; EARS en `requirements.md`; todas las tasks `[x]`; todos los R<n> cubiertos

## Notas

- `dashboard/layout.tsx` y `login/page.tsx` usan `export default` en lugar de arrow function nombrada con `export const`. Esta es la única desviación de `docs/conventions.md` ("Componentes React: arrow functions nombradas. Nada de `export default function`"), pero está **justificada**: Next.js App Router exige que layouts y páginas exporten un `default export`. No constituye defecto sancionable.
- El atributo `secure` en la cookie de `loginAction` se condiciona a `NODE_ENV === "production"` (línea 26 de `actions.ts`), lo que facilita el desarrollo local sin HTTPS. Comportamiento correcto.
- `actions.test.ts` usa `// eslint-disable-next-line @typescript-eslint/no-explicit-any` en líneas 33 y 95 (solo en tests, no en código de producción). Aceptable.
