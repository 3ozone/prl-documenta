# Requirements — auth (id: 8)
> Autenticación y autorización JWT con roles admin/viewer.
> Notación: EARS estricto. Un único `DEBE` por requirement.

---

## R1
CUANDO el sistema arranca y no existe ningún usuario con `role = "admin"` en la base de datos,
el sistema DEBE crear automáticamente un usuario con `email = "admin@prl.local"`,
`role = "admin"` e `is_active = true`, usando la contraseña definida en la variable
de entorno `DEFAULT_ADMIN_PASSWORD` (fallback: `"admin123"`).

## R2
CUANDO se recibe `POST /api/v1/auth/register` sin cabecera `Authorization`,
el sistema DEBE crear el usuario con `role = "viewer"` e ignorar cualquier valor
`role = "admin"` que venga en el body.

## R3
CUANDO se recibe `POST /api/v1/auth/register` con un token Bearer válido de un usuario `admin`,
el sistema DEBE crear el usuario con el `role` indicado en el body (`"admin"` o `"viewer"`).

## R4
CUANDO se recibe `POST /api/v1/auth/register` con un token Bearer válido de un usuario `viewer`,
el sistema DEBE devolver HTTP 403 sin crear ningún usuario.

## R5
CUANDO se recibe `POST /api/v1/auth/register` y el `email` ya existe en la base de datos,
el sistema DEBE devolver HTTP 409 sin crear un nuevo usuario.

## R6
CUANDO se recibe `POST /api/v1/auth/register` con datos válidos,
el sistema DEBE almacenar la contraseña como hash bcrypt (nunca en texto plano)
y devolver HTTP 201 con `id`, `email` y `role` del usuario creado.

## R7
CUANDO se recibe `POST /api/v1/auth/login` con `email` y `password` correctos
de un usuario con `is_active = true`,
el sistema DEBE devolver HTTP 200 con `{"access_token": "<jwt>", "token_type": "bearer"}`.

## R8
CUANDO se recibe `POST /api/v1/auth/login` con credenciales inválidas
(email inexistente, contraseña incorrecta o usuario con `is_active = false`),
el sistema DEBE devolver HTTP 401.

## R9
El sistema DEBE generar tokens JWT con algoritmo `HS256`, firmados con la clave
definida en la variable de entorno `JWT_SECRET_KEY`, con expiración de 60 minutos,
e incluyendo los claims `sub` (email), `role` y `exp`.

## R10
CUANDO un endpoint protegido recibe una petición sin cabecera `Authorization`,
el sistema DEBE devolver HTTP 401.

## R11
CUANDO un endpoint protegido recibe una cabecera `Authorization: Bearer <token>`
con un token expirado o con firma inválida,
el sistema DEBE devolver HTTP 401.

## R12
CUANDO un endpoint de escritura (`POST /documents`, `POST /categories/*/documents`)
recibe una petición con token válido de un usuario con `role = "viewer"`,
el sistema DEBE devolver HTTP 403.

## R13
CUANDO un endpoint de solo lectura (`GET /documents/{id}/download`,
`GET /categories/*/documents`, `GET /reports/status`, `GET /alerts`)
recibe una petición con token válido de cualquier usuario autenticado,
el sistema DEBE procesar la petición normalmente (HTTP 2xx).

## R14
CUANDO un endpoint de escritura recibe una petición con token válido
de un usuario con `role = "admin"`,
el sistema DEBE procesar la petición normalmente (HTTP 2xx).

## R15
El sistema DEBE proteger los siguientes endpoints con `require_admin`
(solo acceso para `role = "admin"`):
- `POST /api/v1/documents`
- `POST /api/v1/categories/empresa/documents`
- `POST /api/v1/categories/trabajadores/documents`
- `POST /api/v1/categories/equipos/documents`

## R16
El sistema DEBE proteger los siguientes endpoints con `require_viewer_or_admin`
(cualquier usuario autenticado):
- `GET /api/v1/documents/{id}/download`
- `GET /api/v1/categories/empresa/documents`
- `GET /api/v1/categories/trabajadores/documents`
- `GET /api/v1/categories/equipos/documents`
- `GET /api/v1/reports/status`
- `GET /api/v1/alerts`

## R17
El sistema DEBE almacenar los usuarios en la tabla `users` con columnas:
`id` (UUID PK), `email` (unique, not null), `hashed_password` (not null),
`role` (not null), `is_active` (not null, default true).
