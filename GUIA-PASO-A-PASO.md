# Guía de trabajo — Caso Practico-Plaza QA Sr.

Esta guía es un instructivo metodológico de preparación y reproducción; los resultados reales están en E3, E4, E5, E6 y E7. Algunos pasos describen actividades ya completadas.

## 0. Preparación
1. Guarda el enunciado y la carpeta `ambiente/` fuera del repositorio público (por ejemplo, en `~/qa-sr-privado/ambiente`).
2. Abre Terminal, ejecuta `node --version` y comprueba >=22.13; si falta, instala Node actualizado.
3. Desde `ambiente/`, lee `README.md` y `openapi.yaml` completos.
4. Inicia con `node server.mjs`; comprueba `GET http://localhost:4010/v1/_sandbox/scenarios`.
5. No cierres la Terminal que mantiene el servicio; usa una segunda Terminal para probarlo.
6. Antes de la primera prueba toma copia de la base original o usa `DB_PATH` alternativo. El reinicio recrea la base.

## E1. Análisis
1. Abre la HU, CA-01...CA-10, reglas, estados y `openapi.yaml` lado a lado.
2. Registra contradicciones, ambigüedades y vacíos; da prioridad por impacto.
3. Por fila deja fuentes exactas, riesgo operativo, supuesto temporal y una pregunta al PO.
4. Los dos conflictos preliminares en E1 deben validarse frente al contrato.

## E2. Estrategia
1. Presenta el alcance, las exclusiones, los riesgos, las técnicas y los criterios de entrada y salida de forma concisa.
2. Prioriza fraude/gate de servidor, segregación de comercios, idempotencia/concurrencia, expiración e integridad.
3. Describe particiones, límites, decisiones, transiciones, negativos y prueba de concurrencia.
4. Distingue API+BD ejecutables frente a cámara/permisos/red/background/dispositivos solo diseñados.
5. Define entrada, salida y condición No-Go.

## E3. Casos de prueba
1. Revisa la matriz CSV preliminar, especialmente técnicas y riesgos.
2. Agrega endpoint, método, HTTP esperado y JSON válidos solo después de leer OpenAPI.
3. Mantén 15-25 casos de mayor riesgo. Marca SMOKE los indispensables.
4. Justifica cobertura CA-01...CA-10 y reglas relevantes.
5. Diseña (no finjas ejecutar) los casos móviles porque no hay aplicación móvil.

## E4. Ejecución
1. Reinicia y prepara la sesión/caso según el escenario.
2. Guarda comandos/scripts enviados, respuesta (sin datos sensibles), hora y resultado.
3. Compara siempre contra HU y OpenAPI; no uses tus suposiciones como certeza.
4. Crea los reportes completos de los hasta ocho defectos más graves encontrados.
5. Si encuentras menos de ocho defectos, no inventes más; documenta lo observado.
6. Evita capturar CUI, tokens, secretos o datos privados en screenshots de publicación.

## E5. Automatización
1. Elegir pytest + requests + jsonschema + PyYAML (o una herramienta que puedas defender).
2. Configurar URL base y credenciales de QA como variables de entorno locales, no subidas a GitHub.
3. Implementar helpers de crear sesión, completar escenario y consultar estado.
4. Agregar validaciones de esquema de OpenAPI para respuestas.
5. Cubrir casos aprobados y negativos críticos; los negativos deben fallar si el defecto existe.
6. Agregar prueba de concurrencia con la misma Idempotency-Key.
7. Separar smoke por marcador (`pytest -m smoke`) y suite completa (`pytest`).
8. Verificar ejecución desde reset y documentar comandos exactos.

## E6. Datos
1. Antes de probar, conservar copia de `qa.db` con registros del sprint previo.
2. Inspeccionar esquema SQLite y relaciones reales (no suponer nombres de tablas).
3. Preparar SQL de unicidad por tenant+CUI, código consumido, estado de verificación, idempotencia y duplicados.
4. Consultar altas del 2026-10-15 convertidas correctamente a hora Guatemala: comprobar timezone de los timestamps originales.
5. Ejecutar consultas y guardar resultados anonimizados e interpretación.
6. Diferenciar registros precargados de registros propios mediante baseline/identificadores.

## E7. Informe
1. Escribir después de E4/E5/E6; máximo una página.
2. Contar pruebas ejecutadas, pass/fail/block y defectos por severidad.
3. Explicar riesgo residual y recomendación Go / Go condicionado / No-Go.
4. Añadir exactamente cinco líneas en inglés al CTO.

## E8. Bitácora
1. Registrar herramienta, uso concreto y entregable tocado mientras trabajas.
2. Registrar ChatGPT/IA con alcance real: diseño, revisión, scripts o documentación según ocurra.
3. Guardar una propuesta específica de IA que revisaste y corregiste de verdad.
4. Nunca atribuirte pruebas no realizadas ni afirmar una corrección hipotética como si hubiera sucedido.

## E9. Video
**Estado de esta entrega:** video grabado y enlace incorporado en `E9-video.md` y `README.md`. Esta sección describe cómo se realizó la demostración.

1. Graba pantalla con una ejecución REAL de un smoke y una prueba negativa.
2. Incluye qué esperabas, qué obtuviste y qué significa.
3. Explica SQL o evidencias y tu decisión de liberación.
4. Duración objetivo 5 minutos (límite 7), visibilidad por enlace, no listado.
5. URL ya incorporada: https://youtu.be/o1ufeCWFcyQ. Comprobar en incógnito la reproducción y el audio antes de enviar.

## Entrega final
1. Revisar `.gitignore`, ejecutar `git status` y confirmar que NO hay ambiente, bases, secretos, enunciado ni videos locales.
2. Subir a rama `main`, verificar archivos y enlace de video en incógnito.
3. Enviar URL antes del plazo preventivo.
