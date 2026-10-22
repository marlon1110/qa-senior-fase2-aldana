# BUG-08 — Existe un alta histórica asociada a una verificación rechazada

**Severidad propuesta:** Crítica (histórico)  
**Prioridad propuesta:** P1  
**Estado:** Abierto / pendiente de triage  
**Fuente:** CA-06; KYC debe estar aprobado antes del alta

## Descripción y precondiciones

Respaldo original `qa-inicial.db` de los registros del sprint anterior; ejecución SQL de solo lectura.

## Datos utilizados

Únicamente tokens y datos ficticios del ambiente QA. Para reproducir utilizar las variables de ambiente de E5; no publicar credenciales ni CUI completos.

## Pasos para reproducir / comprobar

1. Abrir el respaldo original de SQLite en modo lectura.
2. Relacionar `signups.kyc_check_id` con `kyc_checks.id`.
3. Filtrar las altas cuyas verificaciones no tienen estado `CONSUMED`.
4. Investigar el registro `sgn_h02` y su verificación `kyc_h02` sin publicar el CUI.

## Resultado esperado

Ninguna alta asociada a verificación rechazada o sin aprobación previa. La tabla debe conservar estados coherentes.

## Resultado obtenido

El registro histórico `sgn_h02` enlaza con `kyc_h02`, cuyo estado actual es `REJECTED`, aun cuando `consumed_by_signup_id = sgn_h02`.

## Justificación de severidad y prioridad

Se observa una inconsistencia histórica grave de integridad, aunque no se ha reproducido su origen vía API; evitar atribuirla a un endpoint específico.

## Evidencia

Salida `e6-complementaria.txt`; consulta H07 en `E6-resultados-consolidados.md`.

**Límite de la evidencia:** documentar todo comportamiento adicional con una ejecución independiente, sin inventar capturas, códigos de error o persistencia.
