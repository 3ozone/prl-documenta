# Sesión actual

_Sin sesión activa. Todos los features del proyecto están en estado `done`._

## Estado del proyecto (2026-05-29)

- Features completados: 16/16
- Tests frontend: 101/101 (17 archivos)
- Tests backend: 103/103
- feature_list.json: todos `"status": "done"`

## Cambios de esta sesión (runtime bug fixes)

### 1. `loginAction` — `redirect()` fuera de try/catch (`frontend/src/lib/actions.ts`)
- La cookie httpOnly ahora se establece y el redirect ocurre **después** del bloque try/catch,
  conforme a la documentación de Next.js 15. Antes, `redirect()` dentro del catch podía
  impedir que la cookie llegase al browser correctamente.

### 2. `signupAction` — nueva Server Action (`frontend/src/lib/actions.ts`)
- Añadida `signupAction` que llama al backend desde el servidor (no desde el browser).
- `SignupForm.tsx` actualizado para usar `signupAction` en lugar del `fetch` directo al
  backend, eliminando el error CORS en el browser. Se eliminó la dependencia de `useRouter`.

### 3. CORS middleware — backend (`backend/src/main.py`)
- Añadido `CORSMiddleware` con `allow_origins` configurado via env var `CORS_ORIGINS`
  (default `http://localhost:3000`), `allow_credentials=True`.

### 4. Login page — mensaje de éxito tras registro (`frontend/src/app/login/page.tsx`)
- La página ahora es async y lee `searchParams` correctamente (Next.js 15).
- Muestra un banner verde cuando `?registered=1` está presente en la URL.

### 5. Tests (`frontend/tests/lib/actions.test.ts`)
- Importado `signupAction`.
- Añadida suite `signupAction` con 4 tests: éxito (redirect), 409 duplicado, fallo de red,
  error genérico 422.
- Total frontend: 97 → 101 tests.

## Notas previas

- El "bug activo" de `dashboard.alerts.fetch_failed` anotado en sesiones anteriores era
  un falso positivo: la causa real era una DB SQLite local obsoleta (le faltaban las
  columnas `razon_social`, `cif`, etc. añadidas en features posteriores), lo que
  producía un 500, no un 401.
- Solución: borrar `backend/prl_documenta.db` y `backend/prl_dev.db`; el backend
  recrea el schema completo en el próximo arranque vía `Base.metadata.create_all()`.
- `./init.sh` pasa 100% (103 backend + 101 frontend).
