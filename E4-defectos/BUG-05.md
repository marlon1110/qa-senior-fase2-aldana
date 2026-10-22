# BUG-05 — Webhook sin firma HMAC es aceptado

**Severidad propuesta:** Crítica  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** OpenAPI POST /v1/webhooks/idv: sin firma responde 401 y no se procesa

## Descripción y precondiciones

Una sesión de verificación válida, aún PENDING; eventId ficticio único y providerSessionId correcto.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Crear una sesión con token de M-NORTE.
2. Preparar JSON con `eventId`, `sessionId`, `type=check.completed` y `status=approved`.
3. Ejecutar `POST /v1/webhooks/idv` SIN `X-Idv-Signature`.
4. Revisar HTTP y verificar que no se procese el evento.

## Resultado esperado

`401 Unauthorized` y sin efecto del evento sobre la verificación.

## Resultado obtenido

La ejecución automatizada recibió `200 OK` para el webhook sin firma.

## Justificación de severidad y prioridad

Permite aceptar eventos no autenticados del proveedor y debilita la cadena de confianza del KYC. El estado posterior debe verificarse en prueba adicional antes de atribuirle cambios de estado concretos.

## Evidencia

`test_webhook_sin_firma_se_rechaza` en `e5-completo.txt`.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
