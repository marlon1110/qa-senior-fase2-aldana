# BUG-06 — Respuestas concurrentes generan dos identificadores de alta

**Severidad propuesta:** Crítica  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** CA-07 y CA-10; OpenAPI POST /v1/signups: solicitudes simultáneas no generan dos altas

## Descripción y precondiciones

Sesión M-NORTE aprobada con documento ficticio fijo C. Dos solicitudes iguales con mismo verificationId, Idempotency-Key y payload.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Crear sesión de identidad con documento fijo C.
2. Completar `approved`.
3. Preparar dos solicitudes idénticas `POST /v1/signups`.
4. Enviarlas concurrentemente con dos trabajadores.
5. Comparar códigos y los `signupId` devueltos.
6. Consultar SQLite inmediatamente después, sin reset intermedio, para establecer cuántas filas se persistieron.

## Resultado esperado

Única alta efectiva y respuestas compatibles con la idempotencia contratada, sin creación de duplicados.

## Resultado obtenido

Dos respuestas con `signupId` distintos: `sgn_2b6f6f5d3c26` y `sgn_24fe37e91ee4` en la suite completa. **Persistencia simultánea en SQLite aún pendiente de comprobar en la Mac del candidato.**

## Justificación de severidad y prioridad

Riesgo de duplicidades y consumo inconsistente de códigos al recibir reintentos simultáneos. La falla en los identificadores está demostrada, pero no atribuir dos filas persistidas sin SQL.

## Evidencia

`test_idempotencia_concurrente` en `e5-completo.txt`; falta evidencia de DB en esa misma corrida.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
