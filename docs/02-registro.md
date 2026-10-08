# Requisitos

## Modulo de Auth

## Registro

### Requisitos Funcionales

RF1 - Registro:
    RF1a: Llevará como título: "Registro de coordinación de actividades entre empresas".
    RF1b: Nombre empresa.
    RF1c: Cif o dni.
    RF1d: Que actividad se dedica.
    RF1e: Riesgos asociados a tu actividad laboral.
    RF1f: Usuario, es el correo de la persona de contacto.
    RF1g: tel, de la persona de contacto.
    RF1h: contraseña (minimo 10 caracteres con min, may, num y carácteres especiales).
    RF1i: Añadir un mensaje debajo del registro mencionando la ley de la prl.
    RF1j: Debe haber un check que diga "He leído y acepto la Política de Privacidad", si no lo acepta no puede seguir con el registro.
    RF1k: Debe haber un check que diga "Deseo recibir información comercial de productos y servicios".
RF2 - Mensajes:
    RF2a: Si no se rellena alguno de estos campos debe avisar de que falta añadir la información en el campo en concreto.
    RF2b: Si alguno de los campos que se rellena no cumple con los requisitos marcados debe salir un mensaje informando de que si quiere registrarse debe seguir las reglas.
RF3 - Reglas en los campos:
    RF3a: contraseña (minimo 10 caracteres con min, may, num y carácteres especiales).
    RF3b: mail, debe tener "@" y el domino.
    RF3c: Cif/DNI, parsearlo para comprobar que son los números identificativos correctos.
    RF3d: Tel, verificar que es un teléfono fijo o móvil.
    RF3e: Si no acepta la política de Privacidad de datos debe salir un mensaje advirtiendo que es obligatorio aceptarlo para su registro.

### Requisitos No Funcionales

RNF1 - Registro: El registro debe durar menos de 500ms en hacerse completamente.
RNF2 - Mensajes: Los mensajes de información deben aparecer en menos de 200ms.

### Requisitos De Negocios

RC1 - Registro: Tener los datos de las empresas o autónomos que entran nos dan una base de datos de potenciales clientes.

### Escribir Requisitos - Historia de usuario

R1 - Como cliente que se registra, quiero saber los datos de registro para poder acceder a la aplicación.
R2 - Como cliente que se registra, quiero saber si los datos que he puesto son los correctos para poder registrame correctamente.
R3 - Como cliente que se registra, quiero saber por que me piden todos estos datos para poder registrarme. => Lei de la PRL.

Como [USUARIO], quiero [OBJETIVO] para
[BENEFICIO]
Ejemplo:
Como CLIENTE REGISTRADO, quiero VER MI
HISTORIAL DE PEDIDOS para REPETIR COMPRAS

### Criterios de Aceptación

CA1 - DADO que me registro CUANDO añado todos los datos correctamente ENTONCES entro en la aplicación.
CA2 - DADO que me registro CUANDO no añado bien los datos ENTONCES recibo un mensaje donde me explica donde me he equivocado.
CA3 - DADO que me registro CUANDO me dejo un dato obligatorio ENTONCES recibo un mensaje que explica que campo me he dejado de rellenar.
CA4 - DADO que me registro CUANDO me dejo el check de aceptación de las Políticas de Privacidad ENTONCES recibo un mensaje que me dice que debo aceptar las políticas para poder registrarm.

Criterios de Aceptación
Given - When - Then
Ejemplo:
DADO que inicio sesión Given
CUANDO entro en “Mis Pedidosˮ When
ENTONCES veo la lista de pedidos con fecha e
importe (THEN)

## Priorizar Requisitos

MoSCoW
Must
Should
Could
Wonʼt

Must -  RF1, RF2, RF3 - CA1, CA2, CA3, CA4
could - RNF1, RNF2

## Entrevista con usuarios

Preguntas a los usuarios

## Casos de uso

### Actores

### Condiciones

### Flujo principal/Alternativo

Caso de uso: CU-1 Registro
Actor: Usuario y Sistema
Flujo Principal:
    1. El usuario accede al registro
    2. El usuario rellena el formulario de registro
    3. Pulsa el botón registrarse.
    4. El sistema verifica que todos los datos del formulario cumplen con las reglas.
    5. El sistema registra al usuario.
    6. Una vez registrado el sistema le envía a la página principal.
Alternativos:
    1. Si los datos del formulario no cumples los requisitos se notifica al usuario que los datos introducidos, o no son correctos o no cumplen los requisitos.

## Design Docs y RFC´s
