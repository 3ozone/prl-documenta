# Design — auth (id: 8)

## Archivos a crear

### Domain
| Archivo | Contenido |
|---|---|
| `backend/src/domain/entities/user.py` | `User` dataclass (frozen), `UserRole` enum |
| `backend/src/domain/exceptions.py` | Añadir `UserAlreadyExists`, `InvalidCredentials`, `InactiveUser` |
| `backend/src/application/ports/user_repository.py` | `AbstractUserRepository` ABC |
| `backend/src/application/use_cases/register_user.py` | `RegisterUserUseCase` |
| `backend/src/application/use_cases/login_user.py` | `LoginUseCase` |
| `backend/src/application/use_cases/get_current_user.py` | `GetCurrentUserUseCase` |
| `backend/src/infrastructure/db/models.py` | Añadir `UserModel` |
| `backend/src/infrastructure/db/repositories/user_repository.py` | `SqlUserRepository` |
| `backend/src/infrastructure/auth/jwt_token_service.py` | `JwtTokenService` |
| `backend/src/presentation/api/v1/auth.py` | Router `/auth/register` y `/auth/login` |
| `backend/src/presentation/schemas/auth.py` | `RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserResponse` |

## Archivos a modificar

| Archivo | Cambio |
|---|---|
| `backend/src/presentation/dependencies.py` | Añadir `get_current_user`, `require_admin`, `require_viewer_or_admin`, `get_user_repository`, `get_jwt_token_service` |
| `backend/src/presentation/api/v1/documents.py` | Añadir `Depends(require_admin)` en POST, `Depends(require_viewer_or_admin)` en GET download |
| `backend/src/presentation/api/v1/categories.py` | Añadir guards según método |
| `backend/src/presentation/api/v1/worker_categories.py` | Añadir guards según método |
| `backend/src/presentation/api/v1/equipment_categories.py` | Añadir guards según método |
| `backend/src/presentation/api/v1/reports.py` | Añadir `Depends(require_viewer_or_admin)` |
| `backend/src/presentation/api/v1/alerts.py` | Añadir `Depends(require_viewer_or_admin)` |
| `backend/src/main.py` | Registrar router auth + bootstrap admin |
| `backend/pyproject.toml` | Añadir `python-jose[cryptography]` y `passlib[bcrypt]` |

## Firmas nuevas

### `domain/entities/user.py`
```python
from enum import Enum
from dataclasses import dataclass
import uuid

class UserRole(str, Enum):
    ADMIN = "admin"
    VIEWER = "viewer"

@dataclass(frozen=True)
class User:
    id: uuid.UUID
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool
```

### `application/ports/user_repository.py`
```python
class AbstractUserRepository(ABC):
    def save(self, user: User) -> User: ...
    def get_by_email(self, email: str) -> User | None: ...
    def get_by_id(self, user_id: uuid.UUID) -> User | None: ...
    def exists_any_admin(self) -> bool: ...
```

### `application/use_cases/register_user.py`
```python
@dataclass
class RegisterUserCommand:
    email: str
    password: str
    role: UserRole
    requester: User | None  # None = registro anónimo (fuerza viewer)

class RegisterUserUseCase:
    def execute(self, cmd: RegisterUserCommand) -> User: ...
    # Lanza: UserAlreadyExists, InsufficientPermissions
```

### `application/use_cases/login_user.py`
```python
@dataclass
class LoginCommand:
    email: str
    password: str

class LoginUseCase:
    def execute(self, cmd: LoginCommand) -> str:  # devuelve JWT
    # Lanza: InvalidCredentials, InactiveUser
```

### `application/use_cases/get_current_user.py`
```python
class GetCurrentUserUseCase:
    def execute(self, token: str) -> User: ...
    # Lanza: InvalidCredentials (token inválido/expirado)
```

### `infrastructure/auth/jwt_token_service.py`
```python
class JwtTokenService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60): ...
    def create_token(self, email: str, role: str) -> str: ...
    def decode_token(self, token: str) -> dict: ...
    # decode_token lanza InvalidCredentials si token inválido/expirado
```

### `infrastructure/db/models.py` — UserModel añadido
```python
class UserModel(Base):
    __tablename__ = "users"
    id: MappedColumn[uuid.UUID]
    email: MappedColumn[str]  # unique
    hashed_password: MappedColumn[str]
    role: MappedColumn[str]
    is_active: MappedColumn[bool]
```

### `presentation/dependencies.py` — nuevas funciones
```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User: ...

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    # Lanza HTTP 403 si role != admin

def require_viewer_or_admin(current_user: User = Depends(get_current_user)) -> User:
    # Permite cualquier usuario autenticado (viewer o admin)
```

## Excepciones de dominio (nuevas)
Añadir en `backend/src/domain/exceptions.py`:

```python
class UserAlreadyExists(PrlError):
    """Se lanza cuando se intenta registrar un email ya existente."""

class InvalidCredentials(PrlError):
    """Se lanza cuando las credenciales de login son incorrectas o el token es inválido."""

class InactiveUser(PrlError):
    """Se lanza cuando se intenta autenticar un usuario con is_active=False."""

class InsufficientPermissions(PrlError):
    """Se lanza cuando un usuario no tiene permisos para la operación."""
```

## Bootstrap al arrancar
En `main.py`, después de `Base.metadata.create_all`:

```python
async def _bootstrap_admin(db: Session) -> None:
    repo = SqlUserRepository(db)
    if not repo.exists_any_admin():
        password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")
        RegisterUserUseCase(repo, JwtTokenService(...)).execute(
            RegisterUserCommand(
                email="admin@prl.local",
                password=password,
                role=UserRole.ADMIN,
                requester=None,  # bypass de permisos en bootstrap
            )
        )
```

> El bootstrap NO pasa por la validación de permisos (requester=None fuerza
> la creación aunque no haya admin previo).

## Dependencias a añadir en `pyproject.toml`
```toml
"python-jose[cryptography]>=3.3"
"passlib[bcrypt]>=1.7"
```

## Alternativa descartada: OAuth2 con servidor externo (Keycloak / Auth0)
**Motivo del descarte:** El proyecto es un sistema interno con un número
reducido de usuarios (operadores PRL). Introducir un servidor de identidad
externo añade complejidad operacional (infraestructura extra, configuración
OIDC) sin beneficio real a esta escala. JWT auto-contenido firmado con
secreto propio cubre todos los requisitos de seguridad del caso de uso.

## Alternativa descartada: sesiones con cookies (server-side sessions)
**Motivo del descarte:** La API es consumida potencialmente por un frontend
Next.js desacoplado y por llamadas programáticas (workers, scripts). Bearer
JWT es stateless, no requiere almacenamiento de sesión en servidor y es el
estándar de facto para APIs REST.
