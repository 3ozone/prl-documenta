# Tech Stack — Qué usamos y por qué

> Este fichero cataloga las herramientas elegidas. Responde al *¿qué?* y al
> *¿por qué?*. El *¿cómo se usa en el código?* vive en `conventions.md`.
> El *¿en qué capa vive?* vive en `architecture.md`.

---

## Backend

| Herramienta | Versión mínima | Rol | Justificación |
|-------------|---------------|-----|---------------|
| **Python** | 3.13+ | Lenguaje | Tipado mejorado (`PEP 695`), `asyncio` maduro, ecosistema PRL/empresarial. |
| **FastAPI** | 0.115+ | Framework web | Tipado estricto con Pydantic, OpenAPI automático, async nativo para subida de PDFs. |
| **SQLAlchemy** | 2.x | ORM | Mapeo relacional tipado, compatible con MariaDB, requerido por Alembic. |
| **Alembic** | 1.13+ | Migraciones | Control de versiones del esquema de base de datos. |
| **MariaDB** | 11.x | Base de datos | Modelo relacional encaja con entidades (empresa, trabajador, equipo, documento). |
| **logging** | stdlib | Logging | Módulo estándar de Python. Sin dependencia externa. Configurado con `JsonFormatter` para salida JSON en producción. |
| **Ruff** | 0.4+ | Linting + formato | Reemplaza flake8 + isort + black en un solo binario. Velocidad 10-100× mayor. |
| **pytest** | 8.x | Tests | Ver `verification.md`. |

## Frontend

| Herramienta | Versión mínima | Rol | Justificación |
|-------------|---------------|-----|---------------|
| **TypeScript** | 5.x | Lenguaje | Tipado estricto para el dashboard de alertas y formularios de documentos. |
| **Next.js** | 15.x | Framework | App Router, SSR/SSG, API routes. Coherente con el ecosistema React actual. |
| **console** | built-in | Logging | Sin dependencia externa. `console.log/warn/error` con objetos estructurados. Suficiente para el MVP; Next.js serializa automáticamente en entornos cloud (Vercel, etc.). |
| **Vitest** | 2.x | Tests unitarios | API compatible con Jest, integración nativa con Vite/Next.js, más rápido. |
| **ESLint** | 9.x | Linting | Estándar del ecosistema TS/Next.js. |
| **Prettier** | 3.x | Formato | Formato consistente sin discusiones de estilo. |

## Infraestructura

| Herramienta | Rol | Justificación |
|-------------|-----|---------------|
| **Docker** | Contenedores | Entorno reproducible para backend, frontend y MariaDB. |
| **Docker Compose** | Orquestación local | Un solo `docker compose up` levanta todo el stack en desarrollo. |
| **GitHub Actions** | CI/CD | Pipeline de tests (pytest + Vitest), lint (Ruff + ESLint) y build en cada PR. |

## Almacenamiento de ficheros PDF

> Decisión pendiente de confirmar antes de implementar `core_upload`.

| Opción | Cuándo elegirla |
|--------|----------------|
| **Volumen Docker local** | MVP / entorno on-premise simple. |
| **MinIO** (S3-compatible) | Si se necesita escalabilidad o acceso desde múltiples instancias. |

## Autenticación

> Decisión pendiente de confirmar antes de implementar `core_download`.

| Opción | Cuándo elegirla |
|--------|----------------|
| **JWT propio (FastAPI + python-jose)** | Si el sistema gestiona sus propios usuarios. |
| **OAuth2 / Keycloak** | Si existe un proveedor de identidad corporativo. |
