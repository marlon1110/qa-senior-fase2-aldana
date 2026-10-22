# BUG-03 — El backend permite crear altas con verificaciones vencidas

**Severidad propuesta:** Crítica  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** CA-06; OpenAPI POST /v1/signups (409 VERIFICATION_EXPIRED)

## Descripción y precondiciones

Sesión nueva en M-NORTE; escenario approved; reloj adelantado 31 minutos mediante el control del sandbox.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Crear una sesión en M-NORTE.
2. Completar el escenario `approved` y verificar `APPROVED`.
3. Adelantar el reloj 31 minutos con `POST /v1/_sandbox/clock`.
4. Solicitar `POST /v1/signups` con datos de negocio válidos y nueva clave idempotente.
5. Verificar HTTP, cuerpo y ausencia de alta.

## Resultado esperado

`409` y error `VERIFICATION_EXPIRED`; no crear ni consumir alta.

## Resultado obtenido

La suite completa y el smoke recibieron `201 Created` al intentar crear el alta tras los 31 minutos.

## Justificación de severidad y prioridad

La verificación tiene una vigencia obligatoria. Permitir una cuenta fuera de la ventana compromete el gate de identidad.

## Evidencia

`test_verificacion_vencida_no_crea_alta` en `e5-completo.txt`. Complementar con request/response saneados si se presenta en video.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
