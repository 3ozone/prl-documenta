# Requirements — frontend_alerts

> Feature id: 15 | Notación: EARS estricto

---

## R1
El sistema DEBE renderizar la página `/alerts` dentro del layout de dashboard
y protegerla con autenticación (middleware existente redirige a `/login` si no
hay cookie `token`).

## R2
CUANDO el componente `AlertsClient` se monta, el sistema DEBE realizar una
petición `GET /api/proxy/alerts` y mostrar la lista de alertas devuelta por el
backend, ordenada por `dias_restantes` ascendente.

## R3
El sistema DEBE crear un Route Handler en
`frontend/src/app/api/proxy/alerts/route.ts` que, al recibir `GET`, reenvíe la
petición a `GET /alerts` del backend adjuntando el token de la cookie httpOnly
del servidor, y devuelva la respuesta al cliente.

## R4
CUANDO la respuesta de `GET /api/proxy/alerts` es exitosa y contiene al menos
una alerta, el sistema DEBE mostrar por cada alerta: `nombre_archivo`,
`categoria` (o "—" si es `null`), `dias_restantes` y un badge de color según
el nivel.

## R5
El sistema DEBE aplicar los siguientes colores de badge por nivel:
- `caducada` → rojo (`red`)
- `alerta_critica` → naranja (`orange`)
- `alerta` → amarillo (`yellow`)
- `aviso` → azul (`blue`)

## R6
CUANDO la respuesta de `GET /api/proxy/alerts` es exitosa y la lista está
vacía, el sistema DEBE mostrar el mensaje "No hay alertas activas".

## R7
El sistema DEBE refrescar automáticamente los datos cada 60 segundos mediante
SWR (`refreshInterval: 60000`), sin intervención del usuario.

## R8
El sistema DEBE proporcionar un control de filtro (selector o botones) con las
opciones: "Todos", "caducada", "alerta_critica", "alerta", "aviso".

## R9
CUANDO el usuario selecciona un nivel en el filtro, el sistema DEBE mostrar
únicamente las alertas cuyo campo `nivel` coincida con el seleccionado, sin
recargar la página ni realizar una nueva petición de red.

## R10
CUANDO el usuario selecciona "Todos" en el filtro, el sistema DEBE mostrar
todas las alertas disponibles.

## R11
MIENTRAS el filtro activo no coincide con ninguna alerta de la lista cargada,
el sistema DEBE mostrar el mensaje "No hay alertas activas".

## R12
MIENTRAS `AlertsClient` está esperando la primera respuesta de SWR, el sistema
DEBE mostrar un indicador de carga (skeleton o spinner) en lugar de la tabla.

## R13
SI la petición a `GET /api/proxy/alerts` devuelve un error HTTP o falla de red,
ENTONCES el sistema DEBE mostrar un mensaje de error ("Error al cargar las
alertas") y NO renderizar la tabla.

## R14
SI el Route Handler no puede leer la cookie `token` o el backend devuelve 401,
ENTONCES el Route Handler DEBE devolver `401` al cliente.

## R15
El sistema DEBE exportar desde `frontend/src/lib/types.ts` (o el archivo de
tipos existente) la interfaz `AlertResponse` con los campos:
`document_id`, `nombre_archivo`, `categoria`, `nivel` y `dias_restantes`.
