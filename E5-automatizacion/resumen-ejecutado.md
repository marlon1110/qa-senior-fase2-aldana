# E5 — Resumen de la ejecución en Mac

**Herramientas:** Python 3.9.6, pytest 8.4.2, requests, jsonschema, PyYAML. Servicio local Node.js v24.22.1.

| Suite | Ejecutadas | PASSED | FAILED | Deseleccionadas | Tiempo |
|---|---:|---:|---:|---:|---:|
| Smoke `pytest -m smoke` | 10 | 1 | 9 | 8 | 3.57 s |
| Completa `pytest` | 18 | 8 | 10 | 0 | 3.64 s |

El código de salida de la suite completa fue 1 porque las aserciones detectaron discrepancias. Se preservaron las expectativas y **no** se alteraron para hacer pasar la suite. Apareció una advertencia `NotOpenSSLWarning` relativa a LibreSSL de Python; no explica las respuestas de la API local por HTTP.

**Fallos principales:** habilitación por comercio (dos casos), esquema de alta (`economicActivity`), umbral facial, expiración de KYC, tope de intentos, aislamiento multicomercio, firma de webhook, concurrencia e incompatibilidad del esquema `images.selfie` en rechazo por DPI vencido.

**Evidencia original:** `e5-smoke.txt/xml` y `e5-completo.txt/xml` en carpeta privada del candidato. Para GitHub, generar copia depurada que elimine rutas de usuario, tokens y datos sensibles; no publicar la carpeta privada completa.

**Límite:** el test de concurrencia probó dos IDs en respuestas. Hace falta un conteo SQL de la misma corrida para confirmar dos filas persistidas; no confundirlo con el historial de duplicados `M-ESTE`.
