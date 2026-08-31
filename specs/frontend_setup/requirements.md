# Requirements — frontend_setup

> Feature id: 10 | EARS estricto | Cada R<n> es verificable por al menos un test concreto.

---

## R1
El sistema DEBE contener un `package.json` en `frontend/` que declare las dependencias `next` (15.x), `react`, `react-dom`, `typescript` (strict), `tailwindcss`, `vitest` y `eslint`.

## R2
CUANDO el desarrollador ejecuta `npm run dev` dentro de `frontend/`, el sistema DEBE arrancar el servidor de desarrollo de Next.js sin errores en stdout ni stderr.

## R3
CUANDO el desarrollador ejecuta `npx vitest run` dentro de `frontend/`, el sistema DEBE ejecutar la suite de tests y terminar con código de salida 0.

## R4
El sistema DEBE incluir un `tsconfig.json` en `frontend/` con `"strict": true` y un path alias `"@/*"` que apunte a `./src/*`.

## R5
CUANDO un módulo TypeScript importa desde `@/lib/logger`, el sistema DEBE resolver la importación sin errores de compilación.

## R6
El sistema DEBE incluir `frontend/src/app/layout.tsx` con una clase de Tailwind CSS aplicada en el elemento `<body>` (p.ej. `className="bg-white"`), de modo que Tailwind procese el archivo.

## R7
El sistema DEBE incluir `frontend/src/lib/logger.ts` que exporte un objeto `log` por defecto con los métodos `info`, `warn` y `error`, cada uno con la firma `(data: Record<string, unknown>, event: string) => void`.

## R8
CUANDO se llama a `log.info(data, event)`, el sistema DEBE escribir en stdout un objeto JSON con al menos los campos `level: "info"` y `event`.

## R9
CUANDO se llama a `log.warn(data, event)`, el sistema DEBE escribir en stderr un objeto JSON con al menos los campos `level: "warn"` y `event`.

## R10
CUANDO se llama a `log.error(data, event)`, el sistema DEBE escribir en stderr un objeto JSON con al menos los campos `level: "error"` y `event`.

## R11
El sistema DEBE incluir `frontend/src/lib/api.ts` que exporte la clase `ApiError` con los campos de instancia `status: number` y `message: string`.

## R12
CUANDO `apiFetch` recibe una respuesta con `res.ok === false`, el sistema DEBE lanzar una instancia de `ApiError` con el `status` HTTP correcto.

## R13
El sistema DEBE incluir `frontend/middleware.ts` que intercepte todas las rutas excepto `/login`.

## R14
CUANDO una petición llega a cualquier ruta protegida (distinta de `/login`) sin la cookie `token`, el sistema DEBE redirigir la respuesta a `/login`.

## R15
CUANDO una petición llega a `/login` con la cookie `token` presente, el sistema DEBE redirigir la respuesta a `/dashboard`.

## R16
CUANDO una petición llega a cualquier ruta protegida con la cookie `token` presente, el sistema DEBE dejar continuar la petición sin redirigir.

## R17
El sistema DEBE incluir un `Dockerfile` multistage en `frontend/` que en la etapa `builder` ejecute `npm ci` y `npm run build`, y en la etapa `runtime` ejecute `npm start` en el puerto 3000.

## R18
CUANDO se construye la imagen Docker con `docker build -t frontend-test frontend/`, el sistema DEBE completar el build sin errores.

## R19
El sistema DEBE incluir `frontend/src/lib/types.ts` que exporte los tipos `ApiErrorResponse` (shape `{ detail: string }`), `UserRole` y `AlertLevel` con los valores indicados en la descripción de la feature.
> **Nota:** el nombre del tipo es `ApiErrorResponse` (no `ApiError`) para evitar colisión de nombres con la clase `ApiError` de `api.ts`.

## R20
El sistema DEBE incluir `frontend/src/lib/fetcher.ts` que exporte la función `fetcher<T>(url: string): Promise<T>` y lance un `Error` cuando la respuesta HTTP no sea `ok`.
