# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.
> Las herramientas concretas viven en `tech_stack.md`.
> Las convenciones de código viven en `conventions.md`.

## Estilo arquitectónico: Clean Architecture

El sistema se organiza en **cuatro capas concéntricas**. La regla de
dependencia es estricta: las capas internas nunca importan las externas.

```bash
┌─────────────────────────────────────────┐
│           Presentation                  │  ← FastAPI routers / Next.js pages
│  ┌───────────────────────────────────┐  │
│  │         Application               │  │  ← Casos de uso (services)
│  │  ┌─────────────────────────────┐  │  │
│  │  │         Domain              │  │  │  ← Entidades, reglas de negocio
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│           Infrastructure                │  ← DB, almacenamiento, email, logger
└─────────────────────────────────────────┘
```

| Capa | Qué contiene | Puede importar |
|------|------------- |----------------|
| `domain/` | Entidades (`Document`, `Employee`, `Company`), reglas de caducidad, excepciones de dominio | Nada externo |
| `application/` | Casos de uso (`UploadDocument`, `GenerateReport`, `CheckExpiry`) | `domain/` |
| `infrastructure/` | SQLAlchemy repos, almacenamiento de PDFs, email, **logger** | `domain/`, `application/` |
| `presentation/` | FastAPI routers, schemas Pydantic, Next.js pages/components | `application/`, `infrastructure/` |

## Principios

1. **Regla de dependencia.** El dominio no sabe que existe FastAPI, MariaDB
   ni `structlog`. Si una entidad de dominio importa una librería externa,
   es un defecto de arquitectura.

2. **Errores explícitos.** Las funciones que pueden fallar lanzan excepciones
   nombradas del dominio, no devuelven `None`. La capa de presentación las
   captura y transforma en respuestas HTTP o mensajes de usuario.

3. **Inmutabilidad en el dominio.** Las entidades de dominio son
   `@dataclass(frozen=True)`. Modificar = crear una nueva instancia.

4. **El logger vive en infraestructura.** La capa de dominio y aplicación
   nunca instancian un logger directamente. Si necesitan registrar algo,
   lanzan un evento o devuelven un resultado que la capa superior loguea.

5. **Atomicidad en escrituras críticas.** Toda operación que modifica estado
   (subida de PDF, cambio de estado de documento) debe ser transaccional.
   Nunca dejar la base de datos o el almacenamiento en estado inconsistente.

## Flujo de datos — subida de documento

```bash
Usuario (browser)
   │  POST /documents  (multipart/form-data)
   ▼
presentation/ FastAPI router
   │  valida schema Pydantic
   ▼
application/ UploadDocumentUseCase
   │  construye entidad Document, aplica reglas de dominio
   ▼
infrastructure/ DocumentRepository (SQLAlchemy)
   │  persiste metadatos en MariaDB
infrastructure/ FileStorage
   │  guarda PDF en volumen / MinIO
infrastructure/ logger (structlog)
      registra evento con request_id
```

## Flujo de datos — alertas de caducidad

```bash
Scheduler (cron / GitHub Actions)
   ▼
application/ CheckExpiryUseCase
   │  consulta documentos próximos a caducar
   ▼
infrastructure/ DocumentRepository
infrastructure/ NotificationService (email / panel)
```

## Qué NO hacer

- No importar SQLAlchemy, `structlog` ni FastAPI desde `domain/`.
- No poner lógica de negocio (cálculo de caducidad, validaciones) en los
  routers de FastAPI ni en los componentes de Next.js.
- No usar `print()` para errores. Usa el logger de infraestructura y los
  códigos de estado HTTP apropiados.
- No mezclar casos de uso en un mismo servicio de aplicación. Un caso de
  uso = una clase / función.

## Estructura de carpetas

```bash
prl-documenta/
├── backend/
│   ├── src/
│   │   ├── domain/
│   │   │   ├── entities/           # Document, Employee, Company, Equipment
│   │   │   ├── exceptions.py       # PrlError, DocumentNotFound, InvalidExpiryDate…
│   │   │   └── value_objects/      # ExpiryDate, DocumentStatus, Cadence
│   │   ├── application/
│   │   │   ├── use_cases/          # UploadDocument, DownloadDocument,
│   │   │   │                       # GenerateReport, CheckExpiry
│   │   │   └── ports/              # Interfaces abstractas de repos y servicios
│   │   ├── infrastructure/
│   │   │   ├── db/
│   │   │   │   ├── models.py       # Modelos SQLAlchemy
│   │   │   │   └── repositories/   # Implementaciones concretas de ports/
│   │   │   ├── storage/            # Almacenamiento de PDFs (local / MinIO)
│   │   │   ├── notifications/      # Email, panel interno
│   │   │   └── logging.py          # Configuración logging stdlib (JsonFormatter)
│   │   └── presentation/
│   │       ├── api/
│   │       │   └── v1/             # FastAPI routers por dominio
│   │       ├── schemas/            # Pydantic request/response schemas
│   │       └── dependencies.py     # Inyección de dependencias FastAPI
│   ├── alembic/                    # Migraciones de base de datos
│   │   └── versions/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── pyproject.toml              # Dependencias + config Ruff + pytest
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router
│   │   │   ├── (dashboard)/        # Páginas autenticadas (sin segmento de URL)
│   │   │   ├── documents/
│   │   │   └── alerts/
│   │   ├── components/
│   │   │   ├── ui/                 # Botones, tablas, modales genéricos
│   │   │   └── documents/          # Componentes de dominio PRL
│   │   ├── lib/
│   │   │   ├── api.ts              # Cliente HTTP hacia FastAPI
│   │   │   ├── logger.ts           # Configuración pino
│   │   │   └── types.ts            # Tipos TypeScript compartidos
│   │   └── hooks/                  # Custom React hooks
│   ├── tests/
│   ├── package.json
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       ├── ci-backend.yml          # pytest + Ruff
│       └── ci-frontend.yml         # Vitest + ESLint
│
├── docker-compose.yml              # backend + frontend + MariaDB
├── docs/
├── specs/
├── progress/
├── feature_list.json
├── AGENTS.md
└── init.sh
```

### Reglas sobre la estructura

- `ports/` en `application/` define las interfaces que `infrastructure/` implementa.
  Es el mecanismo que aísla el dominio de SQLAlchemy y el sistema de ficheros.
- `alembic/` va al nivel de `backend/`, no dentro de `src/`. Es una herramienta
  de operaciones, no código de aplicación.
- `v1/` en los routers desde el inicio. Versionar la API no tiene coste ahora
  y evita migraciones dolorosas después.
- Los componentes React no conocen la estructura de capas del backend. Solo
  consumen `lib/api.ts`.
