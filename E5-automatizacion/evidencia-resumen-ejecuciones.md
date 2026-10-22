# E5 — Evidencia resumida de ejecuciones reales

Esta hoja reconstruye el **resumen de consola** compartido por el candidato tras ejecutar el ambiente local. No representa una ejecución realizada al generar el paquete. Los `.txt` y `.xml` originales se conservaron privadamente para no publicar rutas personales ni cargas con información sensible.

## Ejecución Smoke

**Comando:** `python -m pytest -q -m smoke E5-automatizacion/tests`

```text
.FFFFFFFFF                                                               [100%]
9 failed, 1 passed, 8 deselected, 1 warning in 3.57s
```

## Ejecución completa

**Comando:** `python -m pytest -q -ra E5-automatizacion/tests`

```text
.FFFFFFFFF....F...                                                       [100%]
10 failed, 8 passed, 1 warning in 3.64s
Código de salida: 1
```

### Casos fallidos en la suite completa

| Test de pytest | Observación |
|---|---|
| `test_impedir_sesion_en_comercio_desactivado[QA_APP_SUR]` | Esperado 409; obtenido 201 |
| `test_impedir_sesion_en_comercio_desactivado[QA_APP_OESTE]` | Esperado 409; obtenido 201 |
| `test_alta_exitosa_y_esquemas` | `economicActivity` devuelto como `null`; OpenAPI exige string |
| `test_puntaje_facial_inferior_al_umbral` | Esperado `REJECTED`; obtenido `APPROVED` |
| `test_verificacion_vencida_no_crea_alta` | Esperado 409; obtenido 201 tras avanzar 31 minutos |
| `test_cuarto_intento_bloqueado` | Cuatro respuestas 201; la cuarta debía ser 409 |
| `test_verificacion_no_visible_para_otro_tenant` | Esperado 404; obtenido 200 |
| `test_webhook_sin_firma_se_rechaza` | Esperado 401; obtenido 200 |
| `test_idempotencia_concurrente` | Dos respuestas con `signupId` diferentes; persistencia simultánea no comprobada |
| `test_rechazos_del_proveedor[document_expired-DOCUMENT_EXPIRED]` | `images.selfie=null` incumple esquema de URI de OpenAPI |

**Interpretación:** 10 fallos de pruebas automatizadas no equivalen necesariamente a 10 defectos distintos. La divergencia del contrato de dos comercios corresponde al mismo BUG-01; hay fallos de esquema y de reglas de negocio. La advertencia local de LibreSSL no explica los HTTP de la API.

## Evidencia de persistencia CP09

Resultado reportado por consulta de solo lectura al respaldo de las pruebas manuales:

```text
Cantidad de altas CP09: 1
sgn_887343af0d8e  M-NORTE  kyc_62d15c1663cd  CONSUMED
face_match_score: 0.72; face_match_threshold: 0.80
código de invitación: 1, CONSUMED
```

La documentación de E6 distingue explícitamente el respaldo inicial de los registros creados durante la prueba.
