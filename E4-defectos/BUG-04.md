# BUG-04 — Un comercio consulta la verificación de identidad de otro comercio

**Severidad propuesta:** Crítica  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** OpenAPI introducción: recursos de otro tenant responden 404

## Descripción y precondiciones

Verificación creada y aprobada para M-NORTE; token de aplicación de M-ESTE.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Crear una sesión usando M-NORTE y registrar su `verificationId`.
2. Ejecutar escenario `approved`.
3. Consultar `GET /v1/identity/verifications/{id}` con el token de M-ESTE.
4. Comparar la respuesta con el contrato.

## Resultado esperado

`404` sin divulgar información de la verificación de otro comercio.

## Resultado obtenido

Se recibió `200 OK` al solicitar con M-ESTE una verificación perteneciente a M-NORTE.

## Justificación de severidad y prioridad

Rompe aislamiento entre comercios y puede exponer datos personales.

## Evidencia

`test_verificacion_no_visible_para_otro_tenant` en `e5-completo.txt`. No publicar contenido personal del cuerpo JSON.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
