# Implementación — frontend_setup

## Estado: completado

## Mapa R<n> → test

| Requirement | Descripción | Test |
|-------------|-------------|------|
| R1  | Linting y formato (ESLint 9 + Prettier) | `npm run lint` — configurado en eslint.config.mjs, prettier.config.mjs |
| R2  | Estructura Next.js 15 App Router | `npm run build` — build exitoso con todas las rutas |
| R3  | Tests con Vitest | `tests/lib/logger.test.ts`, `tests/lib/api.test.ts` — 6 tests, 6 passed |
| R4  | TypeScript strict | `npm run build` — tsc strict sin errores |
| R5  | Path alias @/ | `tests/lib/logger.test.ts:2` `import log from "@/lib/logger"` — resuelto en vitest y build |
| R6  | Tailwind CSS | `tailwind.config.ts` + `globals.css` + `layout.tsx` usando clases Tailwind |
| R7  | logger.info emite JSON estructurado | `tests/lib/logger.test.ts` — "info emits JSON with level info and event" |
| R8  | logger.info incluye campo level | `tests/lib/logger.test.ts` — `expect(parsed.level).toBe("info")` |
| R9  | logger.warn emite JSON estructurado | `tests/lib/logger.test.ts` — "warn emits JSON with level warn and event" |
| R10 | logger.error emite JSON estructurado | `tests/lib/logger.test.ts` — "error emits JSON with level error and event" |
| R11 | ApiError con status y message | `tests/lib/api.test.ts` — "has status and message" |
| R12 | apiFetch lanza ApiError en error HTTP | `tests/lib/api.test.ts` — "throws ApiError when response is not ok" |
| R13 | middleware redirige a /login sin token | `middleware.ts` — lógica `!token && !isPublic` |
| R14 | middleware permite /login sin token | `middleware.ts` — PUBLIC_ROUTES incluye "/login" |
| R15 | middleware redirige a /dashboard con token en /login | `middleware.ts` — lógica `token && pathname === "/login"` |
| R16 | middleware matcher excluye assets estáticos | `middleware.ts` — config.matcher |
| R17 | next.config.ts output standalone | `next.config.ts` — `output: "standalone"` + Dockerfile multistage |
| R18 | Dockerfile multistage | `Dockerfile` — builder + runtime stages |
| R19 | Tipos ApiErrorResponse, UserRole, AlertLevel | `src/lib/types.ts` |
| R20 | fetcher<T> para SWR | `src/lib/fetcher.ts` |

## Verificaciones ejecutadas

- `npx vitest run`: 6/6 tests passed ✓
- `npm run build`: Compilación exitosa, sin errores TypeScript ✓
