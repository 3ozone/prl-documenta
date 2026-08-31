# Requirements — frontend_auth

> EARS estricto. Cada `R<n>` es verificable por al menos un test de Vitest.
> Cubre todos los acceptance criteria de `feature_list.json` id 11.

---

## R1

El sistema DEBE incluir el archivo `frontend/src/app/login/page.tsx` que
exporte un Server Component `LoginPage` el cual renderice el componente
`LoginForm`.

## R2

El sistema DEBE incluir el archivo `frontend/src/components/auth/LoginForm.tsx`
que declare `"use client"` y exporte un componente `LoginForm` con dos campos
controlados por `react-hook-form`: `email` (tipo `email`) y `password` (tipo
`password`).

## R3

CUANDO el campo `email` esté vacío o no tenga formato de correo electrónico
válido, el sistema DEBE mostrar un mensaje de error de validación en cliente
antes de enviar el formulario.

## R4

CUANDO el campo `password` tenga menos de 6 caracteres, el sistema DEBE
mostrar un mensaje de error de validación en cliente antes de enviar el
formulario.

## R5

El sistema DEBE incluir el archivo `frontend/src/lib/actions.ts` con la Server
Action `loginAction(formData: FormData): Promise<void>` que llame a
`POST /api/v1/auth/login` con `Content-Type: application/json` y cuerpo
`{ email, password }` extraídos del `formData`.

## R6

CUANDO `loginAction` recibe una respuesta HTTP 200 del backend, el sistema
DEBE establecer una cookie `token` con los atributos `httpOnly: true`,
`secure: true`, `sameSite: "lax"` y valor igual al campo `access_token` de la
respuesta JSON.

## R7

CUANDO `loginAction` establece la cookie `token` correctamente, el sistema
DEBE redirigir al usuario a la ruta `/dashboard`.

## R8

CUANDO `loginAction` recibe una respuesta HTTP 401 o 422 del backend, el
sistema DEBE devolver un objeto `{ error: string }` con el mensaje de error
para que `LoginForm` lo muestre al usuario.

## R9

CUANDO `LoginForm` recibe un error de `loginAction`, el sistema DEBE mostrar
el mensaje de error en un elemento visible dentro del formulario (aria-live o
rol alert).

## R10

El sistema DEBE incluir en `frontend/src/lib/actions.ts` la Server Action
`logoutAction(): Promise<void>` que elimine la cookie `token`.

## R11

CUANDO `logoutAction` se ejecuta, el sistema DEBE redirigir al usuario a la
ruta `/login`.

## R12

El sistema DEBE incluir el archivo `frontend/src/app/dashboard/layout.tsx`
que exporte un Server Component `DashboardLayout` conteniendo un botón de
logout que invoque `logoutAction` mediante un elemento `<form action={logoutAction}>`.

## R13

El botón de logout del `DashboardLayout` DEBE ser un Client Component
`LogoutButton` ubicado en `frontend/src/components/auth/LogoutButton.tsx`.

## R14

El sistema DEBE incluir en `frontend/src/lib/types.ts` el tipo
`TokenResponse` definido como `{ access_token: string; token_type: string }`.

## R15

MIENTRAS el usuario autenticado navega a `/login`, el sistema DEBE
redirigirlo automáticamente a `/dashboard` (comportamiento ya implementado
en `middleware.ts`; esta feature DEBE añadir un test que lo verifique).

## R16

SI `loginAction` lanza una excepción de red (fetch falla), ENTONCES el
sistema DEBE devolver `{ error: "Error de conexión. Inténtalo de nuevo." }` en
lugar de propagar la excepción.

## R17

El sistema DEBE incluir tests de Vitest en
`frontend/tests/lib/actions.test.ts` que cubran:
`loginAction` con respuesta 200, `loginAction` con respuesta 401,
`loginAction` con error de red, y `logoutAction`.

## R18

El sistema DEBE incluir tests de Vitest en
`frontend/tests/components/LoginForm.test.tsx` que cubran: validación de
`email` requerido, validación de `email` inválido, validación de `password`
con menos de 6 caracteres, y renderizado del mensaje de error devuelto por
`loginAction`.
