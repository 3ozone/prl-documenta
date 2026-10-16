# Requirements — Registro

> Módulo de registro de empresas y autónomos en prlDocumenta.
> EARS — cada requirement es verificable por un test concreto.

---

## Requisitos funcionales (EARS)

### R1 — Título de la pantalla

El sistema DEBE mostrar el título "Registro de coordinación de actividades entre empresas".

### R2 — Campos del formulario

El sistema DEBE ofrecer los campos: nombre de empresa, CIF/DNI, actividad a la que se dedica, riesgos asociados, email de contacto, teléfono de contacto y contraseña.

### R3 — Mensaje de la ley PRL

El sistema DEBE mostrar debajo del formulario un mensaje mencionando la ley de PRL.

### R4 — Check de Política de Privacidad

El sistema DEBE ofrecer un check con el texto "He leído y acepto la Política de Privacidad".

### R5 — Privacidad obligatoria

SI el usuario envía el registro sin marcar el check de Política de Privacidad ENTONCES el sistema NO DEBE completar el registro y DEBE mostrar un mensaje advirtiendo de que es obligatorio aceptarla.

### R6 — Check de información comercial

El sistema DEBE ofrecer un check con el texto "Deseo recibir información comercial de productos y servicios".

### R7 — Registro exitoso

CUANDO el usuario envía el formulario con todos los campos válidos, el sistema DEBE crear la empresa y el usuario, y DEBE redirigir a la página principal.

### R8 — Campo obligatorio vacío

SI el usuario envía el formulario con un campo obligatorio vacío ENTONCES el sistema DEBE mostrar un mensaje indicando qué campo falta.

### R9 — Validación de contraseña

CUANDO el usuario introduce una contraseña, el sistema DEBE verificar que tiene al menos 10 caracteres e incluye mayúsculas, minúsculas, números y caracteres especiales.

### R10 — Error de contraseña

SI la contraseña no cumple los requisitos ENTONCES el sistema DEBE mostrar un mensaje con las reglas que debe seguir.

### R11 — Validación de email

CUANDO el usuario introduce un email, el sistema DEBE verificar que contiene "@" y un dominio válido.

### R12 — Validación de CIF/DNI

CUANDO el usuario introduce un CIF o DNI, el sistema DEBE comprobar que los dígitos de control son correctos.

### R13 — Validación de teléfono

CUANDO el usuario introduce un teléfono, el sistema DEBE verificar que corresponde a un teléfono fijo o móvil.

### R14 — Mensajes de error junto al campo

SI un campo no cumple las reglas de validación ENTONCES el sistema DEBE mostrar un mensaje de error específico junto al campo incumplido.

---

## Requisitos no funcionales (EARS)

### RNF1 — Tiempo de registro

El sistema DEBE completar el registro en menos de 500ms.

### RNF2 — Tiempo de mensajes

El sistema DEBE mostrar los mensajes de información en menos de 200ms.

---

## Requisitos de negocio

RC1 — Disponer de los datos de las empresas y autónomos registrados genera una base de datos de potenciales clientes.

---

## Historias de usuario y criterios de aceptación

> Cada historia de usuario agrupa los criterios de aceptación que definen
> cuándo está cumplida. Cada CA referencia el requisito `R<n>` que verifica.

### HU1 — Conocer los datos de registro

**Como** cliente que se registra, **quiero** conocer los datos que se piden en el registro **para** poder acceder a la aplicación.

- **CA1** (R1) — DADO que accedo al formulario de registro CUANDO se carga la pantalla ENTONCES veo el título "Registro de coordinación de actividades entre empresas".
- **CA2** (R2) — DADO que accedo al formulario de registro CUANDO se carga la pantalla ENTONCES veo los campos: nombre de empresa, CIF/DNI, actividad, riesgos, email, teléfono y contraseña.
- **CA3** (R4) — DADO que accedo al formulario de registro CUANDO se carga la pantalla ENTONCES veo el check "He leído y acepto la Política de Privacidad".
- **CA4** (R6) — DADO que accedo al formulario de registro CUANDO se carga la pantalla ENTONCES veo el check "Deseo recibir información comercial de productos y servicios".
- **CA5** (R5) — DADO que relleno el formulario sin marcar el check de privacidad CUANDO pulso "Registrarse" ENTONCES el sistema no me registra y muestra un mensaje avisando de que debo aceptar la política.
- **CA6** (R7) — DADO que relleno todos los campos correctamente y acepto la privacidad CUANDO pulso "Registrarse" ENTONCES se crea la empresa y el usuario, y soy redirigido a la página principal.

### HU2 — Saber si los datos son correctos

**Como** cliente que se registra, **quiero** saber si los datos que he introducido son correctos **para** poder registrarme correctamente.

- **CA7** (R8) — DADO que relleno el formulario dejando un campo obligatorio vacío CUANDO pulso "Registrarse" ENTONCES veo un mensaje indicando qué campo falta.
- **CA8** (R9) — DADO que introduzco una contraseña con 10+ caracteres, mayúsculas, minúsculas, números y caracteres especiales ENTONCES el sistema la acepta.
- **CA9** (R10) — DADO que introduzco una contraseña que no cumple los requisitos CUANDO pulso "Registrarse" ENTONCES veo un mensaje con las reglas de la contraseña.
- **CA10** (R11) — DADO que introduzco un email sin "@" o sin dominio CUANDO pulso "Registrarse" ENTONCES veo un mensaje de error en el campo email.
- **CA11** (R12) — DADO que introduzco un CIF/DNI con dígitos de control incorrectos CUANDO pulso "Registrarse" ENTONCES veo un mensaje de error en el campo CIF/DNI.
- **CA12** (R13) — DADO que introduzco un teléfono que no es fijo ni móvil válido CUANDO pulso "Registrarse" ENTONCES veo un mensaje de error en el campo teléfono.
- **CA13** (R14) — DADO que un campo no cumple las reglas CUANDO pulso "Registrarse" ENTONCES veo el mensaje de error específico junto a ese campo.

### HU3 — Entender por qué piden los datos

**Como** cliente que se registra, **quiero** saber por qué me piden todos estos datos **para** poder registrarme con confianza.

- **CA14** (R3) — DADO que accedo al formulario de registro CUANDO se carga la pantalla ENTONCES veo un mensaje sobre la ley de PRL debajo del formulario.

### HU4 — Que el registro sea rápido

**Como** cliente que se registra, **quiero** que el registro y los mensajes sean rápidos **para** no tener que esperar.

- **CA15** (RNF1) — DADO que envío un registro válido CUANDO el sistema lo procesa ENTONCES tarda menos de 500ms.
- **CA16** (RNF2) — DADO que un campo no cumple las reglas CUANDO el sistema muestra el mensaje de error ENTONCES este aparece en menos de 200ms.

---

## Priorización (MoSCoW)

| Categoría | Requisitos |
|-----------|-----------|
| **Must** | R1-R14 (HU1, HU2, HU3) |
| **Should** | — |
| **Could** | RNF1, RNF2 (HU4) |
| **Won't** | — |

---

## Casos de uso

### CU-1 — Registro

**Actor**: Usuario y Sistema

**Flujo principal**:

1. El usuario accede al registro.
2. El usuario rellena el formulario de registro.
3. Pulsa el botón "Registrarse".
4. El sistema verifica que todos los datos del formulario cumplen las reglas.
5. El sistema registra al usuario.
6. El sistema redirige al usuario a la página principal.

**Flujo alternativo**:

1. Si los datos del formulario no cumplen los requisitos, el sistema notifica al usuario que los datos introducidos no son correctos o no cumplen los requisitos.
