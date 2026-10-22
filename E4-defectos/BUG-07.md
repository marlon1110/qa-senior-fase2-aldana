# BUG-07 — El sistema permite un cuarto intento de verificación

**Severidad propuesta:** Alta  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** CA-08 y OpenAPI POST /v1/identity/sessions: máximo 3 intentos por dispositivo y comercio en 24 horas

## Descripción y precondiciones

M-NORTE activo; dispositivo nuevo con `X-Device-Id` idéntico en cuatro solicitudes; sesiones no canceladas.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Definir un X-Device-Id nuevo.
2. Hacer 4 POST consecutivos `/v1/identity/sessions` en M-NORTE usando el mismo dispositivo.
3. Registrar los cuatro códigos HTTP.

## Resultado esperado

Códigos `[201, 201, 201, 409]` y error `ATTEMPTS_EXHAUSTED` en el cuarto intento.

## Resultado obtenido

Se recibieron `[201, 201, 201, 201]`, lo que permite iniciar una cuarta sesión.

## Justificación de severidad y prioridad

Debilita el control antifraude y el límite configurable. Este escenario NO cancela intentos: el contrato exceptúa expresamente a las sesiones canceladas.

## Evidencia

`test_cuarto_intento_bloqueado` en `e5-completo.txt`.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
