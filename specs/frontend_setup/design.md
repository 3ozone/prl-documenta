# Design — frontend_setup

> Decisiones técnicas previas al código. No tocar `frontend/` hasta aprobación humana.

---

## 1. Archivos a crear

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/               # vacío (placeholder)
│   │   └── documents/        # vacío (placeholder)
│   ├── lib/
│   │   ├── api.ts
│   │   ├── fetcher.ts
│   │   ├── actions.ts
│   │   ├── types.ts
│   │   └── logger.ts
│   └── hooks/                # vacío (placeholder)
├── middleware.ts
├── tests/
│   └── lib/
│       ├── logger.test.ts
│       └── api.test.ts
├── next.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── eslint.config.mjs
├── prettier.config.mjs
├── vitest.config.ts
├── package.json
└── Dockerfile
```

No se modifica ningún archivo fuera de `frontend/`.

---

## 2. Firmas nuevas

### `lib/logger.ts`

```typescript
const log: {
  info:  (data: Record<string, unknown>, event: string) => void
  warn:  (data: Record<string, unknown>, event: string) => void
  error: (data: Record<string, unknown>, event: string) => void
}
export default log
```

Implementación: `console.log/warn/error(JSON.stringify({ level, event, ...data }))`.

### `lib/api.ts`

```typescript
export class ApiError extends Error {
  constructor(public readonly status: number, message: string) { super(message) }
}

const apiFetch = async <T>(
  path: string,
  options?: RequestInit,
  token?: string
): Promise<T>

// Funciones por recurso — vacías en este setup, se rellenan en features siguientes
```

`BASE_URL` se lee de `process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"`.

### `lib/fetcher.ts`

```typescript
export const fetcher = <T>(url: string): Promise<T> =>
  fetch(url).then((res) => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.json() as Promise<T>
  })
```

### `lib/types.ts`

```typescript
export type ApiError    = { detail: string }
export type UserRole    = "admin" | "viewer"
export type AlertLevel  = "ok" | "aviso" | "alerta" | "alerta_critica" | "caducada"
```

### `lib/actions.ts`

```typescript
"use server"
// Server Actions reales se añaden en frontend_auth y siguientes features.
```

### `middleware.ts`

```typescript
import { NextRequest, NextResponse } from "next/server"

const PUBLIC_PATHS = ["/login"]

export const middleware = (request: NextRequest): NextResponse => {
  const { pathname } = request.nextUrl
  const token = request.cookies.get("token")?.value

  if (PUBLIC_PATHS.includes(pathname)) {
    if (token) return NextResponse.redirect(new URL("/dashboard", request.url))
    return NextResponse.next()
  }

  if (!token) return NextResponse.redirect(new URL("/login", request.url))
  return NextResponse.next()
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] }
```

### `Dockerfile` multistage

```dockerfile
# ---- builder ----
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---- runtime ----
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

Requiere `output: "standalone"` en `next.config.ts`.

---

## 3. Configuraciones clave

### `tsconfig.json` (fragmento relevante)
```json
{
  "compilerOptions": {
    "strict": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

### `vitest.config.ts`
```typescript
import { defineConfig } from "vitest/config"
import path from "path"

export default defineConfig({
  test: { environment: "node" },
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
})
```

### `tailwind.config.ts`
`content` apunta a `./src/**/*.{ts,tsx}`.

---

## 4. Alternativa descartada

**Alternativa: usar `create-next-app` como base de scaffolding**

`create-next-app` generaría automáticamente la mayoría de archivos de configuración, pero introduce ruido (demo pages, SVGs de ejemplo, comentarios de bienvenida) que habría que limpiar manualmente y no se alinea con la estructura de carpetas decidida. Además, la versión exacta de cada dependencia quedaría a discreción del CLI en el momento de ejecución, lo que rompe la reproducibilidad. Se descarta en favor de scaffolding manual con versiones fijadas en `package.json`.

---

## 5. Notas de integración

- El `middleware.ts` de esta feature es el definitivo para `frontend_auth` (feature 11): solo necesitará tests de integración adicionales, no refactoring.
- `lib/api.ts` exporta funciones vacías de recurso ahora; `frontend_auth`, `frontend_dashboard`, etc. las rellenarán.
- `lib/types.ts` recibirá tipos adicionales en cada feature de dominio; los tres tipos de setup son los únicos que no dependen de features posteriores.
