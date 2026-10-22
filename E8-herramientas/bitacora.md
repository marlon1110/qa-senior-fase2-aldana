# E8 — Bitácora de herramientas y asistencia con IA

**Periodo de trabajo:** 19–22 de octubre de 2026; los registros del servicio incluyen fechas UTC de la madrugada del 22.

| Herramienta | Uso realizado | Entregables y comprobación |
|---|---|---|
| Visual Studio Code y Terminal de macOS | Organizar el proyecto, ejecutar `curl`, crear y revisar documentos y comandos | E1–E9; capturas locales del flujo manual |
| Node.js y simulador QA | Levantar el servicio local `localhost:4010` y ejecutar escenarios `approved` y `face_borderline` | E4; sin exponer ni modificar código del backend |
| `curl` | Consultar configuración, crear sesiones, simular webhook, consultar KYC y solicitar alta | E4 BUG-01/BUG-02; HTTP 201 del alta indebida |
| Python 3.9, `pytest`, `requests`, `PyYAML`, `jsonschema` | Ejecutar la suite de caja negra, smoke y validaciones OpenAPI | E5; smoke 1 PASS/9 FAIL, completa 8 PASS/10 FAIL |
| SQLite desde Python (`sqlite3`) | Ejecutar consultas de solo lectura sobre respaldo original y respaldo manual | E6; 2 altas el 15/10 GT, inconsistencias y CP09 persistido |
| Numbers y CSV | Mantener la matriz de 24 casos y contrastar resultado real contra expectativas | E3; distinguir parcial de no ejecutado |
| Grabación de pantalla en macOS y YouTube | Grabación y publicación de la demostración E9, con su enlace externo incorporado a la entrega | [Video E9](https://youtu.be/o1ufeCWFcyQ); no se adjunta el archivo audiovisual al repositorio |
| ChatGPT (IA generativa) | Apoyo sustancial para estructurar E1–E9, redactar documentos y defectos, preparar el código de pruebas `pytest`, consultas SQL, scripts de auditoría e instrucciones operativas; revisión posterior del ZIP | La IA NO ejecutó la suite en esta Mac. Las ejecuciones, capturas, consola y respaldos provienen del trabajo local. Las conclusiones se contrastaron con salidas de curl, pytest y SQLite |

## Ejemplos de revisión crítica de propuestas y borradores

**1. Identificadores de verificación de ejemplo.** En los primeros intentos de CP09 se utilizaron literales de sustitución como `REEMPLAZAR_ID`; el servicio devolvió 404. Se distinguió un error de preparación del test frente a un defecto del backend, se repitió la prueba con los identificadores reales de la sesión y se obtuvo la evidencia válida.

**2. BUG-02: evidencia nueva que cambió la conclusión.** Un borrador afirmaba que no se había demostrado crear un alta. Se ejecutó `POST /v1/signups`, se observó HTTP 201, y luego se comprobó en SQLite el alta `sgn_887343af0d8e`, la coincidencia facial 0.72 frente a 0.80 y el código CONSUMED. El reporte fue corregido para no dejar una conclusión desactualizada.

**3. Contrato y reglas de intentos.** El análisis inicial suponía contar todas las sesiones; al contrastar OpenAPI se detectó que las sesiones canceladas tienen una excepción. Se documentó la contradicción HU/contrato y la prueba del cuarto intento se ejecutó sin cancelar ninguna sesión.

## Alcance, autoría y límites

El uso de IA fue **de elaboración y apoyo técnico**, no solamente ortográfico: incluyó generación de borradores y código. El juicio de calidad debe basarse en resultados realmente reproducidos y documentación contrastada por quien presenta la prueba. Los hallazgos de SQLite histórico indican inconsistencias, pero no permiten asegurar cómo fueron creadas. Las pruebas móviles se diseñaron, pero no se ejecutaron por ausencia de una app móvil.

**Para la entrega:** revisar personalmente que esta descripción represente fielmente el trabajo realizado y mencionar en el video cómo se contrastaron las sugerencias de IA con las evidencias.
