# Design — frontend_auth

> Decisiones técnicas previas al código. No tocar `frontend/` hasta aprobación humana.

---

## 1. Archivos a crear / modificar

```
frontend/
├── src/
│   ├── app/
│   │   ├── login/
│   │   │   └── page.tsx                        CREAR  (Server Component, renderiza LoginForm)
│   │   └── dashboard/
│   │       └── layout.tsx                      CREAR  (Server Component, contiene LogoutButton)
│   ├── components/
│   │   └── auth/
│   │       ├── LoginForm.tsx                   CREAR  (Client Component, react-hook-form)
│   │       └── LogoutButton.tsx                CREAR  (Client Component, <form action={logoutAction}>)
│   └── lib/
│       ├── actions.ts                          MODIFICAR (añadir loginAction + logoutAction)
│       └── types.ts                            MODIFICAR (añadir TokenResponse)
└── tests/
    ├── lib/
    │   └── actions.test.ts                     CREAR
    └── components/
        └── LoginForm.test.tsx                  CREAR
```

No se toca ningún archivo fuera de `frontend/`.

---

## 2. Firmas nuevas

### `lib/actions.ts`

```typescript
"use server"

import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import log from "@/lib/logger"

export type ActionResult = { error: string } | void

export const loginAction = async (formData: FormData): Promise<ActionResult>
export const logoutAction = async (): Promise<void>
```

**Detalle de `loginAction`:**

1. Extrae `email` y `password` de `formData`.
2. Llama a `fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }) })`.
3. Si `res.status === 200` → `cookies().set("token", data.access_token, { httpOnly: true, secure: true, sameSite: "lax" })` → `redirect("/dashboard")`.
4. Si `res.status === 401 | 422` → `return { error: data.detail ?? "Credenciales incorrectas." }`.
5. Si `fetch` lanza → captura en try/catch → `return { error: "Error de conexión. Inténtalo de nuevo." }`.
6. Logging: `log.info` en éxito, `log.warn` en 401/422, `log.error` en excepción de red.

**Detalle de `logoutAction`:**

1. `cookies().delete("token")`.
2. `redirect("/login")`.

### `lib/types.ts` (adición)

```typescript
export type TokenResponse = {
  access_token: string
  token_type: string
}
```

### `components/auth/LoginForm.tsx`

```typescript
"use client"

import { useForm } from "react-hook-form"
import { loginAction } from "@/lib/actions"

type LoginFields = { email: string; password: string }

export const LoginForm = () => {
  const { register, handleSubmit, formState: { errors }, setError } = useForm<LoginFields>()
  const [serverError, setServerError] = useState<string | null>(null)

  const onSubmit = async (data: LoginFields) => {
    const formData = new FormData()
    formData.set("email", data.email)
    formData.set("password", data.password)
    const result = await loginAction(formData)
    if (result?.error) setServerError(result.error)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* campos + mensajes de error + serverError con role="alert" */}
    </form>
  )
}
```

Validaciones de `react-hook-form`:
- `email`: `required: true`, `pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- `password`: `required: true`, `minLength: 6`

### `components/auth/LogoutButton.tsx`

```typescript
"use client"

import { logoutAction } from "@/lib/actions"

export const LogoutButton = () => (
  <form action={logoutAction}>
    <button type="submit">Cerrar sesión</button>
  </form>
)
```

### `app/login/page.tsx`

```typescript
import { LoginForm } from "@/components/auth/LoginForm"

const LoginPage = () => (
  <main>
    <LoginForm />
  </main>
)

export default LoginPage
```

### `app/dashboard/layout.tsx`

```typescript
import { LogoutButton } from "@/components/auth/LogoutButton"

const DashboardLayout = ({ children }: { children: React.ReactNode }) => (
  <div>
    <header>
      <LogoutButton />
    </header>
    <main>{children}</main>
  </div>
)

export default DashboardLayout
```

---

## 3. Contrato con el backend

El backend (`backend/src/presentation/api/v1/auth.py`) acepta `LoginRequest`
como JSON con `{ email: string, password: string }` y devuelve
`TokenResponse = { access_token: string, token_type: string }`.

> **Nota:** El enunciado inicial mencionaba `application/x-www-form-urlencoded`
> con `username`/`password` (OAuth2PasswordRequestForm), pero el backend real
> usa `LoginRequest` con JSON y campos `email`/`password`. El spec sigue el
> código real.

Errores que devuelve el backend:
- `401` → `{ detail: string }` (credenciales inválidas o usuario inactivo)
- `422` → `{ detail: [...] }` (validación de Pydantic; `loginAction` tomará
  el primer mensaje o un texto genérico)

---

## 4. Alternativa descartada

**Alternativa: usar `<form action={loginAction}>` directamente en el Server
Component `LoginPage`, sin `react-hook-form`.**

Descartada porque la validación en cliente antes de enviar el formulario
(R3, R4) requiere acceso a los errores de `react-hook-form` en tiempo real
(`formState.errors`), lo cual exige estado de React y, por tanto, `"use client"`.
Un Server Component puro enviaría el formulario al servidor sin ninguna
validación previa en el navegador, lo que incumple directamente el acceptance
criterion _"Formulario /login valida email y password en cliente antes de enviar"_.

---

## 5. Notas de integración

- `middleware.ts` ya redirige `/login` → `/dashboard` si hay cookie `token`
  (implementado en `frontend_setup`). Esta feature añade tests (R15) pero no
  modifica el middleware.
- `lib/api.ts` no se toca: `loginAction` llama a `fetch` directamente porque
  es una Server Action (no un Server Component que pasa token a `apiFetch`).
- `lib/types.ts` ya tiene `ApiErrorResponse`, `UserRole` y `AlertLevel`.
  Solo se añade `TokenResponse`.
