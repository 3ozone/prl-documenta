# impl_auth — Trazabilidad Requirements → Tests

Feature: auth (id: 8)
Estado: implementación completa, tests verdes (103 tests)

## Mapa R<n> → test

| Requirement | Test(s) |
|---|---|
| R1 (bootstrap admin) | `test_admin_can_upload_returns_201`, `test_login_returns_token` (usa admin@prl.local) |
| R2 (register viewer sin requester) | `test_register_creates_viewer_without_requester`, `test_register_returns_201` |
| R3 (solo admin puede crear admins) | `test_register_admin_requires_admin_requester` |
| R4 (viewer no puede crear admin) | `test_register_viewer_cannot_create_admin` |
| R5 (email duplicado → error) | `test_register_duplicate_email_raises`, `test_register_duplicate_returns_409` |
| R6 (user tiene id/email/role) | `test_register_hashes_password`, `test_register_returns_201` |
| R7 (login devuelve JWT) | `test_login_returns_token_for_valid_credentials`, `test_login_returns_token` |
| R8 (credenciales inválidas → error) | `test_login_raises_for_wrong_password`, `test_login_raises_for_inactive_user`, `test_login_wrong_password_returns_401` |
| R9 (JWT HS256, 60min) | `test_create_and_decode_token_round_trip` |
| R10 (sin token → 401) | `test_protected_endpoint_without_token_returns_401` |
| R11 (token expirado/inválido → 401) | `test_decode_expired_token_raises`, `test_decode_invalid_signature_raises`, `test_protected_endpoint_with_expired_token_returns_401` |
| R12 (viewer no puede upload → 403) | `test_viewer_cannot_upload_returns_403` |
| R13 (viewer puede download) | `test_viewer_can_download_returns_200` |
| R14 (admin puede upload) | `test_admin_can_upload_returns_201` |
| R15 (POST endpoints requieren admin) | endpoints documents/categories/workers/equipos tienen `Depends(require_admin)` |
| R16 (GET endpoints requieren viewer_or_admin) | endpoints download/list/reports/alerts tienen `Depends(require_viewer_or_admin)` |
| R17 (tabla users en BD) | `UserModel` en models.py, `SqlUserRepository` |

## Notas de implementación

- `bcrypt<4.0` añadida como constraint (incompatibilidad passlib + bcrypt>=4)
- Lifespan de FastAPI bootstrap admin@prl.local (contraseña configurable por env `DEFAULT_ADMIN_PASSWORD`)
- Tests existentes actualizados con override de `require_admin`/`require_viewer_or_admin` para no romper
- `auth_client` fixture usa SQLite de archivo por `tmp_path` para aislamiento completo entre tests
