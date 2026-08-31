# Tasks — auth (id: 8)

El implementer marca `[x]` cada task al completarla.
El reviewer rechaza si queda alguna `[ ]` sin justificación documentada.

---

## Bloque 1 — Dependencias y dominio

- [x] T1 — Añadir `python-jose[cryptography]>=3.3` y `passlib[bcrypt]>=1.7`
  en `backend/pyproject.toml` (sección `dependencies`).
  Cubre: R9.

- [x] T2 — Crear `backend/src/domain/entities/user.py` con `UserRole` enum
  y `User` dataclass (`frozen=True`) según el diseño.
  Cubre: R6, R17.

- [x] T3 — Añadir excepciones `UserAlreadyExists`, `InvalidCredentials`,
  `InactiveUser`, `InsufficientPermissions` en
  `backend/src/domain/exceptions.py`.
  Cubre: R5, R8, R12.

---

## Bloque 2 — Capa Application (ports + use cases)

- [x] T4 — Crear `backend/src/application/ports/user_repository.py` con
  `AbstractUserRepository` (métodos: `save`, `get_by_email`, `get_by_id`,
  `exists_any_admin`).
  Cubre: R1, R5, R7.

- [x] T5 — Crear `backend/src/application/use_cases/register_user.py` con
  `RegisterUserCommand` y `RegisterUserUseCase`. La lógica DEBE:
  - Hashear la contraseña con bcrypt antes de guardar.
  - Si `requester` es None o `viewer`, forzar `role = viewer`.
  - Si `requester` es `viewer` e intenta crear admin, lanzar `InsufficientPermissions`.
  - Si el email ya existe, lanzar `UserAlreadyExists`.
  Cubre: R2, R3, R4, R5, R6.

- [x] T6 — Crear `backend/src/application/use_cases/login_user.py` con
  `LoginCommand` y `LoginUseCase`. La lógica DEBE verificar hash bcrypt,
  lanzar `InvalidCredentials` si email no existe o password incorrecto, y
  lanzar `InactiveUser` si `is_active = false`.
  Cubre: R7, R8.

- [x] T7 — Crear `backend/src/application/use_cases/get_current_user.py`
  con `GetCurrentUserUseCase`. Decodifica el token JWT, extrae el email del
  claim `sub`, busca el usuario en repositorio; lanza `InvalidCredentials`
  si el token es inválido/expirado o el usuario no existe.
  Cubre: R10, R11.

---

## Bloque 3 — Infraestructura

- [x] T8 — Añadir `UserModel` en `backend/src/infrastructure/db/models.py`
  (tabla `users`, columnas `id`, `email` unique, `hashed_password`, `role`,
  `is_active`).
  Cubre: R17.

- [x] T9 — Crear `backend/src/infrastructure/db/repositories/user_repository.py`
  con `SqlUserRepository` que implementa `AbstractUserRepository`.
  Cubre: R1, R5, R7, R17.

- [x] T10 — Crear `backend/src/infrastructure/auth/jwt_token_service.py`
  con `JwtTokenService`. Métodos: `create_token(email, role) -> str` y
  `decode_token(token) -> dict`. Secreto desde env `JWT_SECRET_KEY`.
  Algoritmo HS256, expiración 60 min. `decode_token` lanza `InvalidCredentials`
  si token inválido o expirado.
  Cubre: R9, R11.

---

## Bloque 4 — Presentación

- [x] T11 — Crear `backend/src/presentation/schemas/auth.py` con:
  - `RegisterRequest(email, password, role="viewer")`
  - `LoginRequest(email, password)`
  - `TokenResponse(access_token, token_type="bearer")`
  - `UserResponse(id, email, role)`
  Cubre: R6, R7.

- [x] T12 — Crear `backend/src/presentation/api/v1/auth.py` con router
  prefix `/auth` y dos endpoints:
  - `POST /register` → llama `RegisterUserUseCase`; HTTP 201 con `UserResponse`.
    Sin token → viewer. Con token admin → respeta role. Con token viewer → 403.
    Email duplicado → 409.
  - `POST /login` → llama `LoginUseCase`; HTTP 200 con `TokenResponse`.
    Credenciales inválidas → 401.
  Cubre: R2, R3, R4, R5, R6, R7, R8.

- [x] T13 — Añadir en `backend/src/presentation/dependencies.py`:
  - `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`
  - `get_current_user(token, db) -> User` — usa `GetCurrentUserUseCase`; 401 si falla.
  - `require_admin(user) -> User` — 403 si `role != admin`.
  - `require_viewer_or_admin(user) -> User` — acepta cualquier usuario autenticado.
  - `get_user_repository(db) -> SqlUserRepository`
  - `get_jwt_token_service() -> JwtTokenService`
  Cubre: R10, R11, R12, R13, R14.

- [x] T14 — Añadir `Depends(require_admin)` en los endpoints POST de:
  `documents.py`, `categories.py`, `worker_categories.py`,
  `equipment_categories.py`.
  Cubre: R12, R15.

- [x] T15 — Añadir `Depends(require_viewer_or_admin)` en:
  - `GET /documents/{id}/download` en `documents.py`
  - `GET` endpoints de `categories.py`, `worker_categories.py`,
    `equipment_categories.py`
  - `GET /reports/status` en `reports.py`
  - `GET /alerts` en `alerts.py`
  Cubre: R13, R16.

- [x] T16 — Registrar el router `auth` en `backend/src/main.py` con prefijo
  `/api/v1` y añadir la llamada al bootstrap de admin tras
  `Base.metadata.create_all`.
  Cubre: R1.

---

## Bloque 5 — Tests unitarios

- [x] T17 — Crear `backend/tests/unit/test_register_user.py`:
  - `test_register_creates_viewer_without_requester` → cubre R2.
  - `test_register_admin_requires_admin_requester` → cubre R3.
  - `test_register_viewer_cannot_create_admin` → cubre R4.
  - `test_register_duplicate_email_raises` → cubre R5.
  - `test_register_hashes_password` → cubre R6.

- [x] T18 — Crear `backend/tests/unit/test_login.py`:
  - `test_login_returns_token_for_valid_credentials` → cubre R7.
  - `test_login_raises_for_wrong_password` → cubre R8.
  - `test_login_raises_for_inactive_user` → cubre R8.

- [x] T19 — Crear `backend/tests/unit/test_jwt_token_service.py`:
  - `test_create_and_decode_token_round_trip` → cubre R9.
  - `test_decode_expired_token_raises` → cubre R11.
  - `test_decode_invalid_signature_raises` → cubre R11.

---

## Bloque 6 — Tests de integración

- [x] T20 — Actualizar `backend/tests/conftest.py` para añadir fixtures:
  - `auth_admin_headers` → realiza login como admin y devuelve
    `{"Authorization": "Bearer <token>"}`.
  - `auth_viewer_headers` → ídem para un viewer.
  Cubre: R7, R9.

- [x] T21 — Crear `backend/tests/integration/test_auth_endpoints.py`:
  - `test_register_returns_201` → cubre R6.
  - `test_register_duplicate_returns_409` → cubre R5.
  - `test_login_returns_token` → cubre R7.
  - `test_login_wrong_password_returns_401` → cubre R8.
  - `test_protected_endpoint_without_token_returns_401` → cubre R10.
  - `test_protected_endpoint_with_expired_token_returns_401` → cubre R11.
  - `test_viewer_cannot_upload_returns_403` → cubre R12.
  - `test_viewer_can_download_returns_200` → cubre R13.
  - `test_admin_can_upload_returns_201` → cubre R14.
  Cubre: R5, R6, R7, R8, R10, R11, R12, R13, R14.

---

## Trazabilidad rápida

| Requirement | Tasks que lo cubren |
|---|---|
| R1 | T4, T9, T16 |
| R2 | T5, T12, T17 |
| R3 | T5, T12, T17 |
| R4 | T5, T12, T17 |
| R5 | T5, T12, T17, T21 |
| R6 | T5, T11, T12, T17, T21 |
| R7 | T6, T11, T12, T18, T20, T21 |
| R8 | T6, T12, T18, T21 |
| R9 | T10, T19, T20 |
| R10 | T13, T21 |
| R11 | T7, T10, T13, T19, T21 |
| R12 | T13, T14, T21 |
| R13 | T13, T15, T21 |
| R14 | T13, T14, T21 |
| R15 | T14 |
| R16 | T15 |
| R17 | T8, T9 |
