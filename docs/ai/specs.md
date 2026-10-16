# Spec Driven Development (SDD)

> Proceso que sigue el agente de IA para diseñar y construir la aplicación.
> Este documento es para la IA. La versión humana está en
> `docs/guia-diseno-aplicaciones.md`.

---

## Estructura

Cada módulo tiene su carpeta en `docs/modulos/<modulo>/`:

```bash
docs/modulos/<modulo>/
├── requirements.md   # QUÉ se necesita (RF, EARS, RNF, HU, CA, MoSCoW)
├── design.md         # CÓMO se construye (decisiones, UML, tests)
└── tasks.md          # PASOS de implementación (TDD por escenario)
```

## Estados de un módulo

| Estado         | Significado                                         |
|----------------|-----------------------------------------------------|
| `pending`      | Sin spec todavía.                                   |
| `spec_ready`   | Spec redactada. Esperando aprobación humana.        |
| `in_progress`  | Spec aprobada. Implementando.                       |
| `done`         | Código verde, tests pasan, aprobado.                |
| `blocked`      | Atascado. Documentar el motivo.                     |

## La puerta de aprobación humana

El flujo se detiene **una vez**: cuando `requirements.md` + `design.md` +
`tasks.md` están listos y el humano dice "aprobado". Solo entonces se
implementa.

## requirements.md — EARS estricto

Cada requisito es un párrafo numerado `R1`, `R2`... con uno de estos patrones:

| Patrón         | Plantilla                                                   |
|----------------|-------------------------------------------------------------|
| **Ubicuo**     | `El sistema DEBE <acción>.`                                 |
| **Evento**     | `CUANDO <disparador>, el sistema DEBE <acción>.`            |
| **Estado**     | `MIENTRAS <estado>, el sistema DEBE <acción>.`              |
| **Opcional**   | `DONDE <feature opcional>, el sistema DEBE <acción>.`       |
| **No deseado** | `SI <evento no deseado> ENTONCES el sistema DEBE <acción>.` |

Reglas duras:

- Cada requisito tiene un id estable: `R1`, `R2`, ...
- Cada requisito DEBE ser verificable por al menos un test concreto.
- No mezcles varios `DEBE` en un mismo requisito.
- No uses verbos blandos ("podría", "puede", "soporta"). Solo `DEBE` / `NO DEBE`.

## design.md — decisiones técnicas

Captura **antes** de tocar código:

- Modelo de datos (campos, tipos, relaciones).
- Contrato de la API (endpoints, request/response, errores).
- Firmas nuevas (funciones, clases, endpoints).
- Dependencias que se añaden.
- Alternativas descartadas y por qué.
- Diagramas UML (secuencia de los flujos).
- Mapa de trazabilidad `R<n>` → test.

## tasks.md — checklist TDD

Pasos discretos agrupados **por escenario**, siguiendo el ciclo TDD:

```bash
Para cada escenario:
  1. Escribir test de integración → falla
  2. Implementar el código necesario → pasa
```

Cada task referencia al menos un `R<n>`. Al terminar, todas deben estar `[x]`.

## Trazabilidad (regla dura)

- Cada test debe mapearse a un `R<n>` de su spec.
- Cada `R<n>` debe tener al menos un test concreto.

## Cuándo NO aplica SDD

Las features triviales o los ajustes menores no necesitan spec completa.
